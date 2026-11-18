"""Generate supplementary charts: Prediction Scorecard + Service Band Resolution + v2.5 Direction."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'figure.facecolor': '#fafafa',
    'axes.facecolor': '#ffffff',
})

BLUE = '#2a78d6'; ORANGE = '#eb6834'; AQUA = '#1baf7a'
VIOLET = '#6250d6'; RED = '#e34948'; GREEN = '#008300'

fig = plt.figure(figsize=(16, 12))

# ═══════════════════════════════════════
# Top: Prediction Scorecard P1–P10
# ═══════════════════════════════════════
ax_pred = fig.add_axes([0.03, 0.58, 0.94, 0.38])
ax_pred.set_xlim(0, 10)
ax_pred.set_ylim(0, 3.5)
ax_pred.axis('off')
ax_pred.set_title('⑦ Prediction Scorecard: P1–P10 (v2.4 Results + v2.5 New)',
                  fontsize=15, fontweight='bold', pad=12)

predictions = [
    ('P1', 'HV ↑ at 17 MeV\n1.07–1.15 범위', 'CONFIRMED\n(1.094×)', 'confirmed'),
    ('P2', 'Coverage–Degrad.\n비례 [1.19, 2.74]', 'CONFIRMED\n(1.56)', 'confirmed'),
    ('P3', 'Tag/HV ↓ ≥ 3%\nat 17 MeV', 'REFUTED\n(+0.55%)', 'refuted'),
    ('P4', 'Tag/HV > 1.0\nall η, 17 MeV', 'CONFIRMED\n(1.26–3.05)', 'confirmed'),
    ('P5', 'Hybrid 최적\nat 17 MeV', 'CONFIRMED\n(4.67×)', 'confirmed'),
    ('P6', 'HV η-독립\n±1% 이내', 'CONFIRMED\n(0.23%)', 'confirmed'),
    ('P7', '200 MeV 수렴\n3% 이내', 'CONFIRMED\n(0.6%)', 'confirmed'),
    ('P8', 'HV v2.5 > v2.4\nat 17 MeV', 'NEW\n미검증', 'new'),
    ('P9', 'Tag v2.5 > v2.4\nat 17 MeV', 'NEW\n미검증', 'new'),
    ('P10', '|Δd_Tag|>|Δd_HV|\nTag 더 민감', 'NEW\n미검증', 'new'),
]

colors_map = {
    'confirmed': (AQUA, '#e6f9f1', '✓'),
    'refuted': (RED, '#fde8e8', '✗'),
    'new': (BLUE, '#e8f0fb', '◆'),
}

for i, (pid, desc, result, status) in enumerate(predictions):
    col = i % 5
    row = 1 - i // 5
    x0 = col * 1.95 + 0.1
    y0 = row * 1.5 + 0.2

    border_color, bg_color, symbol = colors_map[status]

    box = FancyBboxPatch((x0, y0), 1.75, 1.3,
                         boxstyle="round,pad=0.08",
                         facecolor=bg_color, edgecolor=border_color, linewidth=2)
    ax_pred.add_patch(box)

    ax_pred.text(x0 + 0.875, y0 + 1.1, f'{symbol} {pid}',
                ha='center', va='center', fontsize=14, fontweight='bold', color=border_color)
    ax_pred.text(x0 + 0.875, y0 + 0.72, desc,
                ha='center', va='center', fontsize=9, color='#444444', linespacing=1.2)
    ax_pred.text(x0 + 0.875, y0 + 0.22, result,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=border_color,
                linespacing=1.2)

# Legend for scorecard
handles = [
    mpatches.Patch(facecolor='#e6f9f1', edgecolor=AQUA, linewidth=1.5, label='Confirmed (v2.4)'),
    mpatches.Patch(facecolor='#fde8e8', edgecolor=RED, linewidth=1.5, label='Refuted (v2.4)'),
    mpatches.Patch(facecolor='#e8f0fb', edgecolor=BLUE, linewidth=1.5, label='New (v2.5, 미검증)'),
]
ax_pred.legend(handles=handles, loc='lower center', ncol=3, fontsize=10, frameon=True,
              edgecolor='#cccccc', fancybox=True, bbox_to_anchor=(0.5, -0.08))

# ═══════════════════════════════════════
# Bottom-left: Service Band Resolution Change
# ═══════════════════════════════════════
ax_res = fig.add_axes([0.06, 0.06, 0.42, 0.42])
bands = ['S1\n265', 'S2\n375', 'S3\n535', 'S4\n720', 'S5\n960', 'S6\n1300', 'S7\n1700', 'S8\n2100']
v24_sigma = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
v25_sigma = [1.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
distances = [35, 75, 85, 100, 140, 200, 200, 200]

x = np.arange(len(bands))
w = 0.35
bars1 = ax_res.bar(x - w/2, v24_sigma, w, color=ORANGE, label='v2.4 (conflated)', zorder=3,
                   edgecolor='white', linewidth=0.5)
bars2 = ax_res.bar(x + w/2, v25_sigma, w, color=VIOLET, label='v2.5 (deconflated)', zorder=3,
                   edgecolor='white', linewidth=0.5)

# Mark S1 as unchanged
ax_res.annotate('unchanged', (0, 1.0), textcoords='offset points', xytext=(0, 8),
               ha='center', fontsize=8, color='#888888', fontstyle='italic')

# Mark ×3 changes
for i in range(1, 8):
    ax_res.annotate('×3', (x[i] + w/2, 3.0), textcoords='offset points', xytext=(0, 5),
                   ha='center', fontsize=9, fontweight='bold', color=RED)

# Distance annotations at bottom
for i, d in enumerate(distances):
    color = '#888888' if d < 50 else RED
    ax_res.text(i, -0.4, f'{d} mm', ha='center', fontsize=8, color=color, fontstyle='italic')
ax_res.text(len(bands)/2, -0.65, '← distance to nearest sensor →', ha='center', fontsize=9, color='#999999')

ax_res.set_xticks(x)
ax_res.set_xticklabels(bands, fontsize=9)
ax_res.set_ylabel('σ_z [mm]')
ax_res.set_title('⑧ Service Band σ_z: v2.4 → v2.5', fontsize=13, fontweight='bold')
ax_res.set_ylim(-0.8, 4.0)
ax_res.axhline(y=0, color='#cccccc', linewidth=0.5)
ax_res.legend(loc='upper left', fontsize=9)
ax_res.grid(axis='y', alpha=0.4)
ax_res.set_axisbelow(True)

# ═══════════════════════════════════════
# Bottom-right: v2.5 Expected Directions
# ═══════════════════════════════════════
ax_dir = fig.add_axes([0.56, 0.06, 0.40, 0.42])
ax_dir.set_xlim(0, 10)
ax_dir.set_ylim(0, 7)
ax_dir.axis('off')
ax_dir.set_title('⑨ v2.5 예측 방향 (17 MeV, η = 2.0)', fontsize=13, fontweight='bold', pad=10)

# Draw direction cards
items = [
    ('P8: HV Degradation', '1.094×', '↑ 증가 예상', RED,
     '3σ veto zone 확대\n(±3 mm → ±9 mm at service bands)'),
    ('P9: Tag Degradation', '1.682×', '↑ 증가 예상', RED,
     'p_conv 커널 확대 →\n판별력 저하'),
    ('P10: Sensitivity', '—', 'Tag > HV', VIOLET,
     'Tag: 연속 likelihood 사용\nHV: binary cut만 사용'),
]

for i, (title, v24val, direction, color, reason) in enumerate(items):
    y0 = 5.0 - i * 2.1
    # Card background
    box = FancyBboxPatch((0.3, y0 - 0.3), 9.3, 1.8,
                         boxstyle="round,pad=0.1",
                         facecolor='#f8f8f8', edgecolor='#dddddd', linewidth=1)
    ax_dir.add_patch(box)

    # Title
    ax_dir.text(0.6, y0 + 1.15, title, fontsize=12, fontweight='bold', color='#333333')
    # v2.4 value
    ax_dir.text(0.6, y0 + 0.6, f'v2.4: {v24val}', fontsize=11, color='#666666')
    # Direction arrow
    ax_dir.text(4.0, y0 + 0.6, direction, fontsize=14, fontweight='bold', color=color)
    # Reason
    ax_dir.text(5.8, y0 + 0.75, reason, fontsize=9.5, color='#777777',
               va='center', linespacing=1.3)

    # Big arrow
    ax_dir.annotate('', xy=(3.7, y0 + 0.65), xytext=(3.2, y0 + 0.65),
                   arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

plt.savefig('/mnt/user-data/outputs/ALP-ttbar-v24-v25-Dashboard-Predictions.png', dpi=180,
            bbox_inches='tight', facecolor='#fafafa')
print('Predictions chart saved.')
