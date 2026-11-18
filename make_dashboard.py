"""Generate ALP-ttbar v2.3/v2.4/v2.5 comparison dashboard as a multi-chart PNG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Style ──
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 0.8,
    'xtick.color': '#555555',
    'ytick.color': '#555555',
    'grid.color': '#e8e8e8',
    'grid.linewidth': 0.6,
    'figure.facecolor': '#fafafa',
    'axes.facecolor': '#ffffff',
    'legend.fontsize': 10,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '#dddddd',
})

BLUE = '#2a78d6'
ORANGE = '#eb6834'
AQUA = '#1baf7a'
VIOLET = '#6250d6'
MAGENTA = '#e87ba4'
RED = '#e34948'
GREEN = '#008300'
YELLOW = '#eda100'

# ── Data ──
masses = [17, 50, 100, 200]
mass_labels = ['17', '50', '100', '200']

v23_hv  = [1.06, 1.06, 1.06, 1.03]
v24_hv  = [1.094, 1.099, 1.093, 1.036]
v23_tag = [1.62, 1.14, 1.05, 1.03]
v24_tag = [1.682, 1.170, 1.068, 1.038]

etas = [1.5, 1.7, 2.0, 2.3, 2.5]
eta_hv    = [1.097, 1.097, 1.094, 1.098, 1.094]
eta_tag   = [1.380, 1.397, 1.682, 2.654, 3.334]
eta_ratio = [1.258, 1.274, 1.538, 2.416, 3.048]

nsig = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
cov9  = [3.4, 3.8, 4.2, 4.6, 5.4, 6.2, 7.0]
cov17 = [4.8, 5.6, 6.3, 7.0, 8.5, 10.0, 11.5]

# Coverage-degradation scatter
cov_points = [(5.4, 0.058, '9-disk Endcap'), (8.5, 0.094, '17-band Endcap'), (43.5, 25.74, 'Barrel C3')]

barrel_hv  = [26.74, 8.83, 3.28, 1.09]
barrel_tag = [25.63, 8.73, 2.71, 1.09]

# ── Figure: 3 rows × 2 cols ──
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('ALP-ttbar Toy MC — v2.3 / v2.4 / v2.5 Comparison Dashboard',
             fontsize=18, fontweight='bold', y=0.98)
fig.text(0.5, 0.965,
         'Displaced Light ALP → e⁺e⁻ in tt̄ · Resolution Deconflation · W. S. Paik, 2026-11-18',
         ha='center', fontsize=11, color='#777777')

# ═══════════════════════════════════════════
# (0,0) HV Mass Scan: v2.3 vs v2.4
# ═══════════════════════════════════════════
ax = axes[0, 0]
x = np.arange(len(masses))
w = 0.32
bars1 = ax.bar(x - w/2, v23_hv, w, color=BLUE, label='v2.3 (9-disk)', zorder=3,
               edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + w/2, v24_hv, w, color=ORANGE, label='v2.4 (17-band)', zorder=3,
               edgecolor='white', linewidth=0.5)
# Value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9, color=BLUE)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9, color=ORANGE)
ax.set_xticks(x)
ax.set_xticklabels([f'{m} MeV' for m in masses])
ax.set_ylabel('Degradation Factor')
ax.set_title('① HV Degradation: v2.3 vs v2.4')
ax.set_ylim(1.0, 1.13)
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.5)
ax.set_axisbelow(True)

# ═══════════════════════════════════════════
# (0,1) Tag Mass Scan: v2.3 vs v2.4
# ═══════════════════════════════════════════
ax = axes[0, 1]
bars1 = ax.bar(x - w/2, v23_tag, w, color=BLUE, label='v2.3 (9-disk)', zorder=3,
               edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + w/2, v24_tag, w, color=ORANGE, label='v2.4 (17-band)', zorder=3,
               edgecolor='white', linewidth=0.5)
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9, color=BLUE)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
            f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9, color=ORANGE)
ax.set_xticks(x)
ax.set_xticklabels([f'{m} MeV' for m in masses])
ax.set_ylabel('Degradation Factor')
ax.set_title('② Tag Degradation: v2.3 vs v2.4')
ax.set_ylim(1.0, 1.80)
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.5)
ax.set_axisbelow(True)

# ═══════════════════════════════════════════
# (1,0) η Scan: Tag, HV, Tag/HV
# ═══════════════════════════════════════════
ax = axes[1, 0]
ax.plot(etas, eta_tag, 'o-', color=ORANGE, linewidth=2.5, markersize=8, label='Tag', zorder=3)
ax.plot(etas, eta_ratio, 's--', color=VIOLET, linewidth=2.5, markersize=8, label='Tag/HV', zorder=3)
ax.plot(etas, eta_hv, '^-', color=BLUE, linewidth=2.5, markersize=8, label='HV', zorder=3)
# Annotate key points
ax.annotate(f'{eta_tag[-1]:.2f}×', (etas[-1], eta_tag[-1]),
            textcoords='offset points', xytext=(8, 5), fontsize=9, color=ORANGE, fontweight='bold')
ax.annotate(f'{eta_ratio[-1]:.2f}', (etas[-1], eta_ratio[-1]),
            textcoords='offset points', xytext=(8, -8), fontsize=9, color=VIOLET, fontweight='bold')
ax.annotate(f'{eta_hv[2]:.3f}×', (etas[2], eta_hv[2]),
            textcoords='offset points', xytext=(8, -15), fontsize=9, color=BLUE, fontweight='bold')
ax.set_xlabel('η')
ax.set_ylabel('Value')
ax.set_title('③ η Scan at 17 MeV (v2.4, 17-band)')
ax.legend(loc='upper left')
ax.grid(alpha=0.5)
ax.set_axisbelow(True)

# ═══════════════════════════════════════════
# (1,1) Coverage: 9-disk vs 17-band
# ═══════════════════════════════════════════
ax = axes[1, 1]
ax.fill_between(nsig, cov9, alpha=0.25, color=BLUE, zorder=2)
ax.fill_between(nsig, cov17, alpha=0.25, color=ORANGE, zorder=2)
ax.plot(nsig, cov9, 'o-', color=BLUE, linewidth=2.5, markersize=7, label='9-disk', zorder=3)
ax.plot(nsig, cov17, 's-', color=ORANGE, linewidth=2.5, markersize=7, label='17-band', zorder=3)
# Annotate reference point
ax.annotate(f'  5.4%', (3.0, 5.4), fontsize=9, color=BLUE, fontweight='bold', va='bottom')
ax.annotate(f'  8.5%', (3.0, 8.5), fontsize=9, color=ORANGE, fontweight='bold', va='bottom')
# Increase annotation
for i in range(len(nsig)):
    inc = (cov17[i] - cov9[i]) / cov9[i] * 100
ax.set_xlabel('n_σ')
ax.set_ylabel('C_veto (%)')
ax.set_title('④ Coverage: 9-disk vs 17-band (σ_z = 1 mm)')
ax.legend(loc='upper left')
ax.grid(alpha=0.5)
ax.set_axisbelow(True)

# ═══════════════════════════════════════════
# (2,0) Coverage-Degradation scatter (log)
# ═══════════════════════════════════════════
ax = axes[2, 0]
colors_scatter = [BLUE, ORANGE, AQUA]
sizes = [150, 150, 150]
for i, (cx, cy, lab) in enumerate(cov_points):
    ax.scatter(cx, cy, c=colors_scatter[i], s=sizes[i], zorder=3, edgecolors='white', linewidth=1.5)
    offset_x = 5 if i < 2 else -5
    ha = 'left' if i < 2 else 'right'
    offset_y = 8
    ax.annotate(f'{lab}\nC={cx}%, d−1={cy}',
                (cx, cy), textcoords='offset points',
                xytext=(offset_x, offset_y), fontsize=9,
                color=colors_scatter[i], fontweight='bold', ha=ha)
# Trend line (approximate power law through endcap points)
cx_line = np.linspace(4, 50, 100)
# log-log interpolation through the two endcap points
slope = np.log(0.094/0.058) / np.log(8.5/5.4)
cy_line = 0.058 * (cx_line / 5.4) ** slope
ax.plot(cx_line, cy_line, '--', color='#999999', linewidth=1, alpha=0.6, zorder=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('C_veto (%)')
ax.set_ylabel('d − 1')
ax.set_title('⑤ Coverage–Degradation (3 Geometry Points)')
ax.set_xlim(3, 60)
ax.set_ylim(0.03, 50)
ax.grid(alpha=0.4, which='both')
ax.set_axisbelow(True)

# ═══════════════════════════════════════════
# (2,1) Barrel vs Endcap (log y)
# ═══════════════════════════════════════════
ax = axes[2, 1]
ax.plot(mass_labels, barrel_hv, 'o-', color=BLUE, linewidth=2.5, markersize=8, label='Barrel C3 HV', zorder=3)
ax.plot(mass_labels, barrel_tag, 's--', color=BLUE, linewidth=2, markersize=8, label='Barrel C3 Tag',
        alpha=0.7, zorder=3)
ax.plot(mass_labels, v24_hv, 'o-', color=ORANGE, linewidth=2.5, markersize=8, label='Endcap 17-band HV', zorder=3)
ax.plot(mass_labels, v24_tag, 's--', color=ORANGE, linewidth=2, markersize=8, label='Endcap 17-band Tag',
        alpha=0.7, zorder=3)
# Annotate extremes
ax.annotate(f'{barrel_hv[0]:.1f}×', (mass_labels[0], barrel_hv[0]),
            textcoords='offset points', xytext=(10, 5), fontsize=9, color=BLUE, fontweight='bold')
ax.annotate(f'{v24_tag[0]:.2f}×', (mass_labels[0], v24_tag[0]),
            textcoords='offset points', xytext=(10, -12), fontsize=9, color=ORANGE, fontweight='bold')
ax.set_yscale('log')
ax.set_xlabel('ALP Mass [MeV]')
ax.set_ylabel('Degradation Factor')
ax.set_title('⑥ Barrel C3 vs Endcap 17-band')
ax.legend(loc='upper right', fontsize=9)
ax.grid(alpha=0.5, which='both')
ax.set_axisbelow(True)

plt.tight_layout(rect=[0, 0.01, 1, 0.95])
plt.savefig('/mnt/user-data/outputs/ALP-ttbar-v24-v25-Dashboard-Charts.png', dpi=180, bbox_inches='tight',
            facecolor='#fafafa')
print('Charts saved.')
