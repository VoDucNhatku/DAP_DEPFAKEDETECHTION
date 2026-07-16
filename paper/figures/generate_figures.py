"""
Generate figures for Paper v3 — Deepfake Detection via PCA-Residual Features
All data sourced EXCLUSIVELY from Table 1 (verified, no fabrication).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================================
# DATA — copied verbatim from Table 1 (paper/main_v2.md)
# Verified against paper/reports/self-evaluator.md §6
# ============================================================
classifiers = [
    'Linear Reg.\n(thresholded)',
    'Random\nForest',
    'XGBoost',
    'LightGBM',
    'CatBoost'
]
short_names = ['LinReg', 'RF', 'XGB', 'LGBM', 'CatB']

val_acc  = [0.8535, 0.8355, 0.8680, 0.8690, 0.8602]
val_f1   = [0.8556, 0.8346, 0.8685, 0.8700, 0.8608]
val_auc  = [0.9321, 0.9121, 0.9415, 0.9424, 0.9360]

test_acc = [0.8552, 0.8350, 0.8688, 0.8662, 0.8598]
test_f1  = [0.8574, 0.8338, 0.8687, 0.8664, 0.8594]
test_auc = [0.9309, 0.9144, 0.9442, 0.9427, 0.9386]

OUTPUT_DIR = r'd:\CPVV\DAP_DEPFAKEDETECHTION\paper\figures'

# Style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.dpi': 300,
})

COLORS = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']

# ============================================================
# FIGURE 2: Grouped Bar Chart — Test Accuracy + Test AUC
# ============================================================
fig, ax1 = plt.subplots(figsize=(8, 4.5))

x = np.arange(len(classifiers))
width = 0.35

bars1 = ax1.bar(x - width/2, test_acc, width, label='Test Accuracy',
                color='#4E79A7', edgecolor='white', linewidth=0.5)
bars2 = ax1.bar(x + width/2, test_auc, width, label='Test AUC',
                color='#E15759', edgecolor='white', linewidth=0.5)

# Annotate values on bars
for bar, val in zip(bars1, test_acc):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.003,
             f'{val:.4f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
for bar, val in zip(bars2, test_auc):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.003,
             f'{val:.4f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Baseline
ax1.axhline(y=0.50, color='gray', linestyle='--', linewidth=0.8, label='Random baseline (0.50)')

ax1.set_ylabel('Score')
ax1.set_title('Test Performance of Five Classifiers on 187-dim PCA-Residual Features')
ax1.set_xticks(x)
ax1.set_xticklabels(classifiers, fontsize=8.5)
ax1.set_ylim(0.45, 1.0)
ax1.legend(loc='lower right', fontsize=8)

# Highlight best
ax1.annotate('Best', xy=(2 - width/2, test_acc[2]), xytext=(2 - width/2, test_acc[2] + 0.025),
             arrowprops=dict(arrowstyle='->', color='#4E79A7'), fontsize=7, color='#4E79A7',
             ha='center')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'fig_test_performance.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✓ Figure 2 saved: fig_test_performance.png")


# ============================================================
# FIGURE 3: Heatmap — Val-Test Stability (|val - test|)
# ============================================================
fig, ax = plt.subplots(figsize=(6, 3.5))

# Compute absolute gaps
gaps = np.array([
    [abs(va - ta) for va, ta in zip(val_acc, test_acc)],
    [abs(vf - tf) for vf, tf in zip(val_f1, test_f1)],
    [abs(vu - tu) for vu, tu in zip(val_auc, test_auc)],
])

im = ax.imshow(gaps, cmap='YlOrRd', aspect='auto', vmin=0, vmax=0.01)

# Labels
ax.set_xticks(np.arange(len(short_names)))
ax.set_xticklabels(short_names, fontsize=9)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['|ΔAcc|', '|ΔF1|', '|ΔAUC|'], fontsize=9)

# Annotate each cell
for i in range(3):
    for j in range(5):
        text_color = 'white' if gaps[i, j] > 0.006 else 'black'
        ax.text(j, i, f'{gaps[i,j]:.4f}', ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=text_color)

ax.set_title('Validation–Test Gap per Classifier (lower = more stable)',
             fontsize=10, pad=10)

cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Absolute Gap', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'fig_val_test_stability.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✓ Figure 3 saved: fig_val_test_stability.png")


# ============================================================
# FIGURE 4: Side-by-side Val vs Test Comparison (3 metrics)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=False)

metrics = [
    ('Accuracy', val_acc, test_acc),
    ('F1 Score', val_f1, test_f1),
    ('AUC', val_auc, test_auc),
]

for ax, (metric_name, val_data, test_data) in zip(axes, metrics):
    x = np.arange(len(short_names))
    width = 0.35

    bars_val = ax.bar(x - width/2, val_data, width, label='Validation',
                      color='#76B7B2', edgecolor='white', linewidth=0.5)
    bars_test = ax.bar(x + width/2, test_data, width, label='Test',
                       color='#E15759', edgecolor='white', linewidth=0.5)

    ax.set_title(metric_name, fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, fontsize=8)

    # Dynamic y-axis
    all_vals = val_data + test_data
    ymin = min(all_vals) - 0.02
    ymax = max(all_vals) + 0.015
    ax.set_ylim(ymin, ymax)

    # Annotate
    for bar, val in zip(bars_val, val_data):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.002,
                f'{val:.3f}', ha='center', va='bottom', fontsize=6.5, rotation=45)
    for bar, val in zip(bars_test, test_data):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.002,
                f'{val:.3f}', ha='center', va='bottom', fontsize=6.5, rotation=45)

    if ax == axes[0]:
        ax.legend(fontsize=7, loc='lower left')

fig.suptitle('Validation vs Test Performance Across All Classifiers', fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'fig_val_vs_test.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✓ Figure 4 saved: fig_val_vs_test.png")

print("\n=== All 3 figures generated from verified Table 1 data ===")
print(f"Output directory: {OUTPUT_DIR}")
