import os
import re
import time
import difflib
import requests
import urllib.parse
from pathlib import Path

BASE_DIR = Path(r"D:\CPV-VIP\DAP_DEPFAKEDETECHTION")
NOTES_DIR = BASE_DIR / "notes"
PAPERS_DIR = BASE_DIR / "papers"
MD_FILE = NOTES_DIR / "related-work-papers.md"
REPORT_FILE = NOTES_DIR / "downloaded_papers_status_openalex.md"
SKIPPED_FILE = NOTES_DIR / "related-work-skipped-unverifiable.md"

# Minimum title similarity (difflib.SequenceMatcher ratio) between the cleaned
# candidate title from related-work-papers.md and an OpenAlex result before we
# accept it. Below this, a real-but-wrong paper (topic drift on a noisy query)
# is more likely than a genuine match. Empirically: exact-title hits score
# 0.9+, genuine paraphrase/variant titles typically 0.6-0.8, unrelated-but-
# lexically-similar papers (the original bug) scored ~0.3-0.4.
TITLE_SIM_THRESHOLD = 0.45
YEAR_TOLERANCE = 1


def parse_markdown(file_path):
    papers = []
    skipped = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r'\*\*\[(\d+)\]\*\*\s+(.*?)\n(.*?)(?=\n\*\*\[\d+\]\*\*|\n##\s|\Z)', re.DOTALL)
    matches = pattern.finditer(content)
    for match in matches:
        paper_id = match.group(1)
        title_raw = match.group(2).strip()
        details_text = match.group(3)

        # Step 1: strip parenthetical asides, e.g. "Title (FD for X)"
        title = re.sub(r'\(.*?\)', '', title_raw).strip()

        # Step 2: strip a glued ", Author et al., YEAR, Venue" suffix that some
        # entries carry on the same line as the title (mixed format in the
        # source file). This raw glued string used to be sent whole to
        # OpenAlex and caused topic-drift false matches (root cause, see
        # notes/review-deepfake-status-report.md addendum).
        title = re.sub(
            r',\s*[A-Z][\w.\-]*(?:\s+[A-Z][\w.\-]*)*\s+et al\.?,?\s*\d{4}.*$',
            '', title
        ).strip()
        # Fallback: a trailing ", YEAR, Venue..." with no "et al." (e.g. ", 2023")
        title = re.sub(r',\s*\d{4}[^,]*(,.*)?$', '', title).strip()
        title = title.rstrip(',').strip()

        authors = "Unknown"
        author_match = re.search(r'-\s+Authors:\s+(.*?)\n', details_text)
        if author_match:
            authors = author_match.group(1).strip()
        else:
            glued_author = re.search(r',\s*([A-Z][\w.\-]*(?:\s+[A-Z][\w.\-]*)*\s+et al\.?)', title_raw)
            if glued_author:
                authors = glued_author.group(1).strip()

        year = "Unknown"
        year_match = re.search(r'-\s+Year:\s+(.*?)\n', details_text)
        if year_match:
            year = year_match.group(1).strip()
            year_clean = re.search(r'(\d{4})', year)
            if year_clean:
                year = year_clean.group(1)
        else:
            glued_year = re.search(r'(\d{4})', title_raw)
            if glued_year:
                year = glued_year.group(1)

        if any(g.lower() in authors.lower() for g in
               ["various", "multiple", "[group]", "unknown", "[various]", "[multiple]", "benchmark group"]):
            skipped.append({"id": paper_id, "title_raw": title_raw, "authors": authors,
                             "reason": "unverifiable author field (various/multiple/group/unknown)"})
            continue

        if not title:
            skipped.append({"id": paper_id, "title_raw": title_raw, "authors": authors,
                             "reason": "title empty after cleaning"})
            continue

        papers.append({"id": paper_id, "title_raw": title_raw, "title": title,
                        "authors": authors, "year": year})
    return papers, skipped


def query_openalex(title):
    """Strict title-field search. Returns up to 3 candidates (not a blind
    top-1) so pick_best_candidate() can score them instead of trusting
    OpenAlex's relevance ranking blindly."""
    query = urllib.parse.quote(f'title.search:{title}')
    url = f"https://api.openalex.org/works?filter={query}&per-page=3&mailto=agent@example.com"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
    except Exception as e:
        print(f"  [ERROR] OpenAlex query failed for '{title}': {e}")
    return []


def extract_author_surnames(authors_str):
    """Pull plausible surnames out of a free-text authors field like
    'Durall, Keuper, Schall (the FFT-focused paper)' or 'Rössler et al. (2019)'
    or 'Wang, Kortylewski, Yuille (2022, extended from 2020)'."""
    if not authors_str or authors_str == "Unknown":
        return []
    s = re.sub(r'\(.*?\)', '', authors_str)
    # NOTE: intentionally no trailing \b after \.? here - "et al." followed by
    # a non-word char (space/end) makes \.?\b backtrack to avoid a non-boundary,
    # leaving a dangling "." that silently breaks the later substring match
    # (empirically caught: "Rössler et al." -> leftover "Rössler ." rejected a
    # correct match). Matching "et\s+al\.?" without the trailing \b consumes
    # the period cleanly.
    s = re.sub(r'\bet\s+al\.?', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\bor\b', ',', s, flags=re.IGNORECASE)
    s = re.sub(r'\band\b', ',', s, flags=re.IGNORECASE)
    parts = re.split(r'[,&/]', s)
    cleaned = []
    for p in parts:
        p = re.sub(r'[\s.]+$', '', p.strip())
        if len(p) > 1:
            cleaned.append(p)
    return cleaned


def candidate_author_names(candidate):
    names = []
    for a in candidate.get('authorships', []):
        nm = (a.get('author') or {}).get('display_name', '')
        if nm:
            names.append(nm)
    return names


def author_matches(expected_authors_str, candidate):
    """Returns (matches: bool, detail: str). If the entry's author field is
    unusable ('Unknown'), we can't verify by author, so this check is skipped
    (title+year gating already applies) rather than blocking everything."""
    surnames = extract_author_surnames(expected_authors_str)
    if not surnames:
        return True, "author_unverifiable_skipped"
    cand_names_lower = " ; ".join(candidate_author_names(candidate)).lower()
    if not cand_names_lower:
        return True, "candidate_has_no_author_data_skipped"
    for sn in surnames:
        if sn.lower() in cand_names_lower:
            return True, f"matched_on({sn})"
    return False, f"none_of({surnames})_in_candidate_authors({candidate_author_names(candidate)})"


def pick_best_candidate(title, year, authors, candidates):
    """Score every candidate by title similarity; reject rather than blindly
    accept candidates[0]. Also cross-checks the entry's stated author surnames
    against OpenAlex's actual authorship list -- a title-only match is NOT
    enough (empirically caught a real case: entry attributed to 'Durall,
    Keuper, Schall' title-matched a real OpenAlex paper that is actually by
    Wang/Wang/Zhang/Owens/Efros -- confirmed by reading the downloaded PDF
    content directly). Returns (candidate_or_None, best_sim, reason)."""
    if not candidates:
        return None, 0.0, "no_candidates_returned"

    best = None
    best_sim = 0.0
    for c in candidates:
        c_title = c.get('title') or c.get('display_name') or ''
        sim = difflib.SequenceMatcher(None, title.lower(), c_title.lower()).ratio()
        if sim > best_sim:
            best_sim = sim
            best = c

    if best is None or best_sim < TITLE_SIM_THRESHOLD:
        return None, best_sim, f"title_sim_too_low({best_sim:.2f})"

    if year != "Unknown":
        c_year = best.get('publication_year')
        if c_year is not None and abs(int(c_year) - int(year)) > YEAR_TOLERANCE:
            return None, best_sim, f"year_mismatch(expected={year},got={c_year})"

    ok, detail = author_matches(authors, best)
    if not ok:
        return None, best_sim, f"author_mismatch({detail})"

    return best, best_sim, "ok"


def check_code_availability(title):
    url = f"https://paperswithcode.com/api/v1/papers/?title={urllib.parse.quote(title)}"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data.get('count', 0) > 0:
                pwc_paper = data['results'][0]
                return f"[PWC]({pwc_paper.get('url', 'https://paperswithcode.com/')})"
    except Exception:
        pass
    return ""


def download_pdf(url, output_path):
    """Downloads url, but ONLY writes to disk if the response body actually
    starts with the %PDF magic bytes. Previously this saved whatever bytes
    came back regardless of content-type, silently writing HTML bot-
    verification/redirect pages to disk with a .pdf extension (~40% of the
    original papers/ folder was this failure mode)."""
    if not url:
        return False, "no_url"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=25)
        if response.status_code != 200:
            return False, f"http_{response.status_code}"
        content = response.content
        if not content[:1024].lstrip().startswith(b'%PDF'):
            return False, "not_a_real_pdf(no_%PDF_header)"
        with open(output_path, 'wb') as f:
            f.write(content)
        return True, "ok"
    except Exception as e:
        return False, f"exception({e})"


def sanitize_filename(s, max_len=60):
    s = re.sub(r'[^a-zA-Z0-9_\-]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s[:max_len]


def main():
    print(f"Parsing {MD_FILE}")
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    papers, skipped = parse_markdown(MD_FILE)
    print(f"Parsed {len(papers)} candidate papers, skipped {len(skipped)} unverifiable entries.")

    rows = []
    accepted = 0
    rejected = 0
    downloaded = 0
    download_failed = 0

    for p in papers:
        pid, title, authors, year = p['id'], p['title'], p['authors'], p['year']
        print(f"\n[{pid}] Querying OpenAlex: '{title}'")
        candidates = query_openalex(title)
        best, sim, reason = pick_best_candidate(title, year, authors, candidates)

        if best is None:
            rejected += 1
            print(f"  -> Rejected ({reason})")
            rows.append({
                "id": pid, "cleaned_title": title, "authors": authors, "year": year,
                "oa_title": "-", "title_sim": f"{sim:.2f}",
                "status": f"Not Found / Rejected ({reason})", "code": "", "file": ""
            })
            time.sleep(0.3)
            continue

        accepted += 1
        oa_title = best.get('title') or best.get('display_name') or "Unknown Title"
        pdf_url = None
        oa = best.get('open_access') or {}
        if oa.get('is_oa') and oa.get('oa_url'):
            pdf_url = oa['oa_url']
        else:
            loc = best.get('best_oa_location') or {}
            if loc:
                pdf_url = loc.get('pdf_url')

        code_url = check_code_availability(title)

        surnames = extract_author_surnames(authors)
        author_snippet = sanitize_filename(surnames[0].split(' ')[0]) if surnames else "Unknown"
        safe_title = sanitize_filename(title[:40])
        filename = f"[{pid}]_{year}_{author_snippet}_{safe_title}.pdf"
        output_path = PAPERS_DIR / filename

        status = "No OA PDF URL"
        file_note = ""
        if pdf_url:
            ok, dl_reason = download_pdf(pdf_url, output_path)
            if ok:
                downloaded += 1
                status = "Downloaded (validated %PDF header)"
                file_note = f"papers/{filename}"
            else:
                download_failed += 1
                status = f"Failed Download ({dl_reason})"
        print(f"  -> Accepted (title_sim={sim:.2f}) OpenAlex title='{oa_title[:70]}' status={status}")

        rows.append({
            "id": pid, "cleaned_title": title, "authors": authors, "year": year,
            "oa_title": oa_title, "title_sim": f"{sim:.2f}",
            "status": status, "code": code_url, "file": file_note
        })
        time.sleep(0.5)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Bao cao Tai Bai bao bang OpenAlex (Downloaded Papers Status) - regenerated after Bug A/B fix\n\n")
        f.write(f"Total candidates parsed: {len(papers)} | Skipped (unverifiable author): {len(skipped)} | "
                f"Accepted (passed title/year validation): {accepted} | Rejected: {rejected} | "
                f"Downloaded (validated %PDF): {downloaded} | Download failed: {download_failed}\n\n")
        f.write(f"Validation thresholds: TITLE_SIM_THRESHOLD={TITLE_SIM_THRESHOLD}, YEAR_TOLERANCE={YEAR_TOLERANCE}\n\n")
        f.write("| ID | Cleaned Title (query sent to OpenAlex) | Authors | Year | OpenAlex Title | TitleSim | Status | Code | File |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['id']} | {r['cleaned_title']} | {r['authors']} | {r['year']} | "
                    f"{r['oa_title']} | {r['title_sim']} | {r['status']} | {r['code']} | {r['file']} |\n")

    with open(SKIPPED_FILE, 'w', encoding='utf-8') as f:
        f.write("# Skipped entries - unverifiable author field or empty title after cleaning\n\n")
        f.write("Previously these entries were silently `continue`d past with no record. "
                "Logged here now so they can be manually resolved instead of silently disappearing.\n\n")
        f.write("| ID | Title (raw) | Authors | Reason |\n")
        f.write("|---|---|---|---|\n")
        for s in skipped:
            f.write(f"| {s['id']} | {s['title_raw']} | {s['authors']} | {s['reason']} |\n")

    print(f"\nDone. Report: {REPORT_FILE}")
    print(f"Skipped log: {SKIPPED_FILE}")
    print(f"Summary: parsed={len(papers)} skipped={len(skipped)} accepted={accepted} rejected={rejected} "
          f"downloaded={downloaded} download_failed={download_failed}")


if __name__ == "__main__":
    main()
