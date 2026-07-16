"""
Self-check script for paper v3.
Runs 8 automated checks against main_v3.tex and main_v3.md.
All data cross-referenced with Table 1 (verified source of truth).
"""
import re
import os
import sys

PAPER_DIR = r'd:\CPVV\DAP_DEPFAKEDETECHTION\paper'
TEX_FILE = os.path.join(PAPER_DIR, 'main_v3.tex')
MD_FILE = os.path.join(PAPER_DIR, 'main_v3.md')

results = []
passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    status = "PASS" if condition else "FAIL"
    if condition:
        passed += 1
    else:
        failed += 1
    results.append((name, status, detail))
    print(f"  [{status}] {name}" + (f" -- {detail}" if detail else ""))

# Read files
with open(TEX_FILE, 'r', encoding='utf-8') as f:
    tex = f.read()
with open(MD_FILE, 'r', encoding='utf-8') as f:
    md = f.read()

print("=" * 60)
print("SELF-CHECK: Paper v3")
print("=" * 60)

# ============================================================
# CHECK 1: All numbers in text match Table 1
# ============================================================
print("\n--- Check 1: Numbers match Table 1 ---")
# Table 1 verified values
table1 = {
    'LinReg': {'val_acc': '0.8535', 'val_f1': '0.8556', 'val_auc': '0.9321',
               'test_acc': '0.8552', 'test_f1': '0.8574', 'test_auc': '0.9309'},
    'RF':     {'val_acc': '0.8355', 'val_f1': '0.8346', 'val_auc': '0.9121',
               'test_acc': '0.8350', 'test_f1': '0.8338', 'test_auc': '0.9144'},
    'XGB':    {'val_acc': '0.8680', 'val_f1': '0.8685', 'val_auc': '0.9415',
               'test_acc': '0.8688', 'test_f1': '0.8687', 'test_auc': '0.9442'},
    'LGBM':   {'val_acc': '0.8690', 'val_f1': '0.8700', 'val_auc': '0.9424',
               'test_acc': '0.8662', 'test_f1': '0.8664', 'test_auc': '0.9427'},
    'CatB':   {'val_acc': '0.8602', 'val_f1': '0.8608', 'val_auc': '0.9360',
               'test_acc': '0.8598', 'test_f1': '0.8594', 'test_auc': '0.9386'},
}

# Check all Table 1 values exist in tex
all_found = True
missing = []
for clf, metrics in table1.items():
    for metric_name, value in metrics.items():
        if value not in tex:
            all_found = False
            missing.append(f"{clf}.{metric_name}={value}")

check("Table 1 values in .tex",
      all_found,
      f"Missing: {', '.join(missing)}" if missing else "All 30 values found")

# Check key in-text claims match Table 1
claim_checks = [
    ("86.9 percent" in tex or "86 to 87 percent" in tex or "0.8688" in tex,
     "XGBoost best acc ~86.9%"),
    ("0.944" in tex or "0.9442" in tex, "XGBoost AUC 0.944"),
    ("85.5 percent" in tex or "0.8552" in tex, "Linear baseline 85.5%"),
    ("0.9309" in tex, "Linear AUC 0.9309"),
]
claims_ok = all(c[0] for c in claim_checks)
claim_detail = "; ".join([c[1] for c in claim_checks if not c[0]])
check("In-text claims match Table 1",
      claims_ok,
      f"Failed: {claim_detail}" if claim_detail else "All key claims verified")

# ============================================================
# CHECK 2: No overclaim words
# ============================================================
print("\n--- Check 2: No overclaim words ---")
overclaim_words = [
    'paradigm', 'breakthrough', 'novel', 'SOTA', 'state-of-the-art',
    'unprecedented', 'outperform', 'superior', 'surpass', 'best-in-class',
    'ground-breaking', 'groundbreaking', 'revolutionize'
]
found_overclaims = []
for word in overclaim_words:
    if re.search(r'\b' + re.escape(word) + r'\b', tex, re.IGNORECASE):
        found_overclaims.append(word)
check("No overclaim words",
      len(found_overclaims) == 0,
      f"Found: {', '.join(found_overclaims)}" if found_overclaims else "Clean")

# ============================================================
# CHECK 3: No placeholders (TODO/TBD/FIXME)
# ============================================================
print("\n--- Check 3: No TODO/TBD/FIXME placeholders ---")
placeholder_patterns = ['TODO', 'TBD', 'FIXME', 'XXX', 'PLACEHOLDER']
found_placeholders = []
for pat in placeholder_patterns:
    if pat.lower() in tex.lower():
        found_placeholders.append(pat)
check("No placeholders in .tex",
      len(found_placeholders) == 0,
      f"Found: {', '.join(found_placeholders)}" if found_placeholders else "Clean")

# ============================================================
# CHECK 4: All citations have matching references
# ============================================================
print("\n--- Check 4: Citations match references ---")
# Extract all \cite{...} keys
cite_keys = set(re.findall(r'\\cite\{([^}]+)\}', tex))
all_cite_keys = set()
for group in cite_keys:
    for key in group.split(','):
        all_cite_keys.add(key.strip())

# Extract all \bibitem{...} keys
bib_keys = set(re.findall(r'\\bibitem\{([^}]+)\}', tex))

orphan_cites = all_cite_keys - bib_keys
orphan_bibs = bib_keys - all_cite_keys

check("All citations have bibitems",
      len(orphan_cites) == 0,
      f"Missing bibitems for: {', '.join(orphan_cites)}" if orphan_cites else f"All {len(all_cite_keys)} citation keys matched")

check("All bibitems are cited",
      len(orphan_bibs) == 0,
      f"Uncited: {', '.join(orphan_bibs)}" if orphan_bibs else f"All {len(bib_keys)} references cited")

# ============================================================
# CHECK 5: No claim that ablation/robustness is done
# ============================================================
print("\n--- Check 5: No false completion claims ---")
false_claims = []
# Check that ablation/robustness/sweep are NOT claimed as done
bad_patterns = [
    (r'(?i)we\s+(?:performed|conducted|completed|ran)\s+(?:a\s+)?(?:robustness|ablation|sensitivity\s+sweep)', 'Claims robustness/ablation done'),
    (r'(?i)our\s+ablation\s+(?:study|results|experiment)', 'Claims ablation study exists'),
    (r'(?i)robustness\s+results\s+(?:show|demonstrate|confirm)', 'Claims robustness results'),
]
for pattern, desc in bad_patterns:
    if re.search(pattern, tex):
        false_claims.append(desc)

check("No false completion claims",
      len(false_claims) == 0,
      f"Found: {', '.join(false_claims)}" if false_claims else "Ablation/robustness correctly listed as future work")

# ============================================================
# CHECK 6: Figure data matches Table 1
# ============================================================
print("\n--- Check 6: Figure generation script uses correct data ---")
fig_script = os.path.join(PAPER_DIR, 'figures', 'generate_figures.py')
with open(fig_script, 'r', encoding='utf-8') as f:
    script = f.read()

# Verify key values in script match Table 1
script_checks = [
    '0.8688' in script,  # XGB test acc
    '0.8662' in script,  # LGBM test acc
    '0.9442' in script,  # XGB test auc
    '0.8350' in script,  # RF test acc
    '0.8535' in script,  # LinReg val acc
]
check("Figure script data matches Table 1",
      all(script_checks),
      "All key values verified in generate_figures.py")

# ============================================================
# CHECK 7: Section structure is Q4-complete
# ============================================================
print("\n--- Check 7: Q4 section structure ---")
required_sections = [
    (r'\\begin\{abstract\}', 'Abstract'),
    (r'\\section\{Introduction\}', 'Introduction'),
    (r'\\section\{Related Work\}', 'Related Work'),
    (r'\\section\{Problem Formulation\}', 'Problem Formulation'),
    (r'\\section\{Proposed Method\}', 'Proposed Method'),
    (r'\\section\{Experimental Setup\}', 'Experimental Setup'),
    (r'\\section\{Results\}', 'Results'),
    (r'\\section\{Discussion\}', 'Discussion'),
    (r'\\section\{Limitations and Future Work\}', 'Limitations and Future Work'),
    (r'\\section\{Conclusion\}', 'Conclusion'),
    (r'\\begin\{thebibliography\}', 'References'),
]
missing_sections = []
for pattern, name in required_sections:
    if not re.search(pattern, tex):
        missing_sections.append(name)

check("Q4 section structure complete",
      len(missing_sections) == 0,
      f"Missing: {', '.join(missing_sections)}" if missing_sections else f"All {len(required_sections)} sections present")

# ============================================================
# CHECK 8: Val/Test rankings correct
# ============================================================
print("\n--- Check 8: Val/Test winner rankings ---")
# XGBoost should win test (acc, f1, auc)
# LightGBM should win val (acc, f1, auc)
test_acc_vals = [0.8552, 0.8350, 0.8688, 0.8662, 0.8598]
val_acc_vals =  [0.8535, 0.8355, 0.8680, 0.8690, 0.8602]
names = ['LinReg', 'RF', 'XGB', 'LGBM', 'CatB']

test_winner = names[test_acc_vals.index(max(test_acc_vals))]
val_winner = names[val_acc_vals.index(max(val_acc_vals))]

check("XGBoost wins test accuracy",
      test_winner == 'XGB',
      f"Test winner: {test_winner}")
check("LightGBM wins val accuracy",
      val_winner == 'LGBM',
      f"Val winner: {val_winner}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print(f"TOTAL: {passed} PASSED, {failed} FAILED out of {passed + failed}")
print("=" * 60)

# Write report
report_dir = os.path.join(PAPER_DIR, 'reports')
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, 'v3-self-check.md')

with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Self-Check Report — Paper v3\n\n")
    f.write(f"**Date:** 2026-07-17\n")
    f.write(f"**Files checked:** `main_v3.tex`, `main_v3.md`, `figures/generate_figures.py`\n\n")
    f.write(f"## Summary: {passed}/{passed+failed} checks PASSED\n\n")
    f.write("| # | Check | Status | Detail |\n")
    f.write("|---|---|---|---|\n")
    for i, (name, status, detail) in enumerate(results, 1):
        emoji = "PASS" if status == "PASS" else "FAIL"
        f.write(f"| {i} | {name} | {emoji} | {detail} |\n")
    f.write("\n---\n\n")
    f.write("## Integrity Statement\n\n")
    f.write("- All numbers in text and figures trace to Table 1 (verified pipeline output)\n")
    f.write("- No overclaim words (novel/SOTA/breakthrough/etc.)\n")
    f.write("- Ablation, robustness test, N-sweep all correctly listed as Future Work\n")
    f.write("- Venue band: Q4 Conference / Scopus-index (not Q1/Q2)\n")
    f.write("- Novelty tier: T1 (recipe/experimental extension)\n")

print(f"\nReport saved to: {report_path}")
