#!/usr/bin/env python3
"""Generate the v2.5 preregistration PDF from README.md content."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib import colors
import datetime

# ── Configuration ──
OUTPUT_FILE = (
    "ALP-ttbar-Toy-MC-v2.5-Preregistration-Resolution-Deconflation-"
    "SENSOR_DISK_Z-Separation-2026-11-18.pdf"
)
SHA256_README = "e3d17539f43b9634a826239a2f5aef55e304197a8df618abbd82292d7ab644f5"
FINAL_SHA256 = "4f7b5160cf7a5f12b6aa6db8b8be5c22bffdd8b5cba023fa17b6a58cf36edeeb"
DOI = "10.5281/zenodo.24329044"
GITHUB_URL = "https://github.com/wspaik5/ALP-ttbar-Toy-MC-v2.5-Prereg-Resolution-Deconflation"

# ── Styles ──
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontSize=14, leading=18, spaceAfter=6, alignment=TA_CENTER
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=9, leading=12, spaceAfter=3, alignment=TA_CENTER,
    textColor=HexColor('#333333')
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=13, leading=16, spaceBefore=14, spaceAfter=6,
    textColor=HexColor('#1a1a1a')
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
    textColor=HexColor('#2a2a2a')
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=9, leading=12, spaceAfter=4, alignment=TA_JUSTIFY
)
code_style = ParagraphStyle(
    'Code', parent=styles['Code'],
    fontSize=7.5, leading=10, spaceAfter=4,
    backColor=HexColor('#f5f5f5'), borderPadding=4,
    fontName='Courier'
)
bullet_style = ParagraphStyle(
    'Bullet', parent=body_style,
    leftIndent=18, bulletIndent=6, spaceAfter=2
)
disclaimer_style = ParagraphStyle(
    'Disclaimer', parent=styles['Normal'],
    fontSize=8, leading=10, spaceAfter=6, alignment=TA_JUSTIFY,
    textColor=HexColor('#555555'), leftIndent=18, rightIndent=18,
    borderPadding=4, backColor=HexColor('#fafafa')
)
footnote_style = ParagraphStyle(
    'Footnote', parent=styles['Normal'],
    fontSize=7.5, leading=9, spaceAfter=2, textColor=HexColor('#666666')
)
ref_style = ParagraphStyle(
    'Ref', parent=styles['Normal'],
    fontSize=8, leading=10, spaceAfter=2, leftIndent=18, firstLineIndent=-18
)

TABLE_STYLE_BASE = TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 7.5),
    ('LEADING', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e8e8e8')),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
])


def make_table(headers, rows, col_widths=None):
    """Create a formatted table."""
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = TableStyle(TABLE_STYLE_BASE.getCommands())
    # Alternate row shading
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.add('BACKGROUND', (0, i), (-1, i), HexColor('#f5f5f5'))
    t.setStyle(style)
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc'),
                       spaceBefore=6, spaceAfter=6)


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch
    )
    story = []

    # ── Title Block ──
    story.append(Paragraph(
        "ALP-ttbar Toy MC v2.5 — Preregistration:<br/>"
        "Resolution Deconflation (SENSOR_DISK_Z Separation)<br/>"
        "in Displaced Light ALP → e<super>+</super>e<super>−</super>",
        title_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Author:</b> Won Shik Paik (Independent Researcher, Auckland, New Zealand)",
        subtitle_style
    ))
    story.append(Paragraph(
        f"<b>Date:</b> 2026-11-18 &nbsp; | &nbsp; "
        f"<b>DOI:</b> https://doi.org/{DOI}",
        subtitle_style
    ))
    story.append(Paragraph(
        f"<b>GitHub:</b> {GITHUB_URL}",
        subtitle_style
    ))
    story.append(Paragraph(
        "<b>Builds on:</b> v2.4 (10.5281/zenodo.24296796 &amp; 10.5281/zenodo.24302619), "
        "v2.3 (10.5281/zenodo.24244893 &amp; 10.5281/zenodo.24273586), "
        "v2.2 (10.5281/zenodo.24189990 &amp; 10.5281/zenodo.24238224), "
        "v2.1 (10.5281/zenodo.24063091 &amp; 10.5281/zenodo.24136462), "
        "v2.0 overview (10.5281/zenodo.24056097); motivated by arXiv:2610.38932",
        subtitle_style
    ))
    story.append(Paragraph(
        "<b>Status:</b> preregistration (frozen before computation)",
        subtitle_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f"<b>SHA-256 of README.md (before hash insertion):</b> "
        f"<font face='Courier' size='7'>{SHA256_README}</font>",
        subtitle_style
    ))
    story.append(Paragraph(
        f"<b>SHA-256 of README.md (final, with hash):</b> "
        f"<font face='Courier' size='7'>{FINAL_SHA256}</font>",
        subtitle_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Disclaimer.</b> Independent personal toy study, not affiliated with the authors "
        "of arXiv:2610.38932 or arXiv:2306.08686, nor with the CMS, ATLAS, LHCb or ALICE "
        "Collaborations or the FCC study. Detector numbers are assumed; only qualitative "
        "trends and ratios are meaningful.",
        disclaimer_style
    ))
    story.append(hr())

    # ── §0 Executive Summary ──
    story.append(Paragraph("0. Executive Summary", h1_style))
    story.append(Paragraph(
        "The v2.4 post-registration study discovered a resolution conflation: overriding the "
        "<font face='Courier'>DISK_Z</font> array with all 17 band positions (9 sensor disks "
        "+ 8 service bands) caused the simulation to assign pixel-quality z resolution "
        "(σ<sub>z</sub> = 1.0 mm) near service bands, which represent passive material "
        "(cables, cooling, support structures) and should not provide measurement capability. "
        "This conflation means the v2.4 degradation and tag performance values reflect the "
        "combined effect of increased coverage <i>and</i> artificially improved measurement "
        "resolution, and cannot be attributed to coverage alone.",
        body_style
    ))
    story.append(Paragraph(
        "The v2.5 study introduces a targeted code fix — a new "
        "<font face='Courier'>SENSOR_DISK_Z</font> array containing only the 9 sensor disk "
        "positions — and uses it exclusively in the "
        "<font face='Courier'>_measure_endcap()</font> function for z resolution assignment. "
        "All other uses of <font face='Courier'>DISK_Z</font> (conversion generation, veto "
        "placement, tag formula evaluation, nearest-disk Δχ<super>2</super><sub>L</sub> pull) "
        "continue to use the full 17-band array. The geometry, random seeds, and all other "
        "parameters remain identical to v2.4.",
        body_style
    ))
    story.append(Paragraph(
        "This separation isolates the resolution effect from the material effect, enabling a "
        "direct comparison of v2.5 results against the published v2.4 values to quantify the "
        "impact of the conflation. The seven original predictions (P1–P7) are retested with "
        "updated expectations that account for the corrected resolution model, and three new "
        "predictions (P8–P10) are introduced to characterise the deconflation effect itself.",
        body_style
    ))
    story.append(hr())

    # ── §1 Motivation ──
    story.append(Paragraph("1. Motivation", h1_style))
    story.append(Paragraph("1.1 The Resolution Conflation Problem", h2_style))
    story.append(Paragraph(
        "In <font face='Courier'>endcap_sim.py</font>, the function "
        "<font face='Courier'>_measure_endcap()</font> assigns z vertex resolution based on "
        "proximity to elements in <font face='Courier'>DISK_Z</font>:",
        body_style
    ))
    story.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "# E2, E3 config (lines ~215-220 in endcap_sim.py):<br/>"
        "near_any = np.zeros(len(z_true), bool)<br/>"
        "for zd in DISK_Z:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;near_any |= (np.abs(z_true - zd) &lt; 50.0)<br/>"
        "sz_base = np.where(near_any, VTX_RES_PIXEL, VTX_RES_STRIP)"
        "</font>",
        code_style
    ))
    story.append(Paragraph(
        "When <font face='Courier'>DISK_Z</font> contains all 17 band positions (as in v2.4), "
        "vertices near service bands at z = 265, 375, 535, 720, 960, 1300, 1700, 2100 mm "
        "receive pixel-quality resolution (σ<sub>z</sub> = 1.0 mm) even though these positions "
        "represent passive material with no active sensors.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Physical interpretation:</b> In a real tracker, z resolution depends on sensor "
        "placement. Passive material (cables, cooling pipes, support rings) generates photon "
        "conversions but provides no measurement points. A vertex reconstructed near a service "
        "band should rely on the nearest <i>sensor</i> disk for its z measurement, receiving "
        "degraded resolution proportional to the distance from that sensor.",
        body_style
    ))

    story.append(Paragraph("1.2 Quantitative Example", h2_style))
    story.append(Paragraph(
        "Consider the service band at z = 960 mm (band S5, midpoint of the 820–1100 mm gap):",
        body_style
    ))
    story.append(Paragraph(
        "• <b>v2.4 (conflated):</b> z = 960 mm is in <font face='Courier'>DISK_Z</font>, "
        "so |960 − 960| = 0 &lt; 50 mm → σ<sub>z</sub> = 1.0 mm (pixel quality).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>v2.5 (deconflated):</b> <font face='Courier'>SENSOR_DISK_Z</font> = "
        "[230, 300, 450, 620, 820, 1100, 1500, 1900, 2300]. Nearest sensors are z = 820 mm "
        "and z = 1100 mm, both at distance 140 mm &gt; 50 mm → σ<sub>z</sub> = 3.0 mm "
        "(strip quality).",
        bullet_style
    ))
    story.append(Paragraph(
        "The resolution at this position changes by a factor of 3. This affects: "
        "(1) the vertex fit quality (Δχ<super>2</super><sub>T</sub> and "
        "Δχ<super>2</super><sub>L</sub>), which uses σ<sub>z</sub>; "
        "(2) the tag formula evaluation, which uses σ<sub>z</sub> through the p<sub>conv</sub> "
        "convolution; (3) the hard-veto zone width at 3σ: ±3 mm (pixel) → ±9 mm (strip).",
        body_style
    ))

    story.append(Paragraph("1.3 Service Band Distances to Nearest Sensor", h2_style))
    story.append(make_table(
        ['Service Band', 'z [mm]', 'Nearest Sensor z [mm]', 'Distance [mm]',
         'v2.4 σ_z', 'v2.5 σ_z'],
        [
            ['S1 (230–300)', '265', '230', '35', '1.0 mm', '1.0 mm*'],
            ['S2 (300–450)', '375', '300 or 450', '75', '1.0 mm', '3.0 mm'],
            ['S3 (450–620)', '535', '450 or 620', '85', '1.0 mm', '3.0 mm'],
            ['S4 (620–820)', '720', '620 or 820', '100', '1.0 mm', '3.0 mm'],
            ['S5 (820–1100)', '960', '820 or 1100', '140', '1.0 mm', '3.0 mm'],
            ['S6 (1100–1500)', '1300', '1100 or 1500', '200', '1.0 mm', '3.0 mm'],
            ['S7 (1500–1900)', '1700', '1500 or 1900', '200', '1.0 mm', '3.0 mm'],
            ['S8 (1900–2300)', '2100', '1900 or 2300', '200', '1.0 mm', '3.0 mm'],
        ],
        col_widths=[85, 45, 95, 55, 50, 50]
    ))
    story.append(Paragraph(
        "*S1 at z = 265 mm is within 50 mm of the sensor disk at z = 230 mm (distance 35 mm), "
        "so its resolution is unchanged. Of the 8 service bands, 7 experience a resolution "
        "change from 1.0 mm to 3.0 mm.",
        footnote_style
    ))
    story.append(hr())

    # ── §2 Code Change ──
    story.append(Paragraph("2. Code Change", h1_style))
    story.append(Paragraph("2.1 The Fix", h2_style))
    story.append(Paragraph(
        "A single new module-level array is introduced in "
        "<font face='Courier'>endcap_sim.py</font>:",
        body_style
    ))
    story.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "# 9 sensor disk z positions only (identical to v2.2/v2.3 DISK_Z)<br/>"
        "SENSOR_DISK_Z = np.array([230., 300., 450., 620., 820., 1100., 1500., 1900., 2300.])"
        "</font>",
        code_style
    ))
    story.append(Paragraph(
        "The <font face='Courier'>_measure_endcap()</font> function is modified to use "
        "<font face='Courier'>SENSOR_DISK_Z</font> instead of "
        "<font face='Courier'>DISK_Z</font> for the E2/E3 resolution assignment loop:",
        body_style
    ))
    story.append(Paragraph(
        "<font face='Courier' size='7.5'>"
        "# BEFORE (v2.4):<br/>"
        "for zd in DISK_Z: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "# 17 bands — service bands get pixel resolution<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;near_any |= (np.abs(z_true - zd) &lt; 50.0)<br/><br/>"
        "# AFTER (v2.5):<br/>"
        "for zd in SENSOR_DISK_Z: &nbsp;# 9 sensor disks only<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;near_any |= (np.abs(z_true - zd) &lt; 50.0)"
        "</font>",
        code_style
    ))

    story.append(Paragraph("2.2 What Does NOT Change", h2_style))
    story.append(make_table(
        ['Function', 'Use of DISK_Z', 'Array in v2.5'],
        [
            ['_measure_endcap() — resolution', 'Proximity check for σ_z',
             'SENSOR_DISK_Z (9)'],
            ['endcap_conversions() — generation', 'Material positions', 'DISK_Z (17)'],
            ['endcap_material_veto() — HV', 'Band positions for veto', 'DISK_Z (17)'],
            ['compute_dchi2_endcap() — Δχ²_L', 'Nearest band for pull', 'DISK_Z (17)'],
            ['mtag_v24.p_conv() — tag', 'Material map for p_conv', 'DISKS (17)'],
        ],
        col_widths=[170, 140, 120]
    ))

    story.append(Paragraph("2.3 Runtime Override", h2_style))
    story.append(Paragraph(
        "The <font face='Courier'>install_v25_geometry()</font> function performs the same "
        "<font face='Courier'>DISK_Z</font>, <font face='Courier'>DISK_X0</font>, "
        "<font face='Courier'>DISK_HW</font> override as v2.4 (17 bands), and additionally "
        "sets <font face='Courier'>ec.SENSOR_DISK_Z</font> to the 9 sensor disk positions. "
        "The <font face='Courier'>_measure_endcap()</font> function references "
        "<font face='Courier'>SENSOR_DISK_Z</font> from the module scope.",
        body_style
    ))
    story.append(hr())

    # ── §3 Geometry and Parameters ──
    story.append(Paragraph("3. Geometry and Parameters", h1_style))
    story.append(Paragraph("3.1 17-Band Endcap Geometry (Identical to v2.4)", h2_style))
    story.append(make_table(
        ['Band', 'Type', 'z [mm]', 'X0', 'HW [mm]'],
        [
            ['1', 'Sensor', '230', '0.006', '1.5'],
            ['2', 'Service', '265', '0.005', '1.5'],
            ['3', 'Sensor', '300', '0.020', '3.0'],
            ['4', 'Service', '375', '0.005', '1.5'],
            ['5', 'Sensor', '450', '0.020', '3.0'],
            ['6', 'Service', '535', '0.005', '1.5'],
            ['7', 'Sensor', '620', '0.020', '3.0'],
            ['8', 'Service', '720', '0.005', '1.5'],
            ['9', 'Sensor', '820', '0.022', '3.5'],
            ['10', 'Service', '960', '0.008', '1.5'],
            ['11', 'Sensor', '1100', '0.030', '4.5'],
            ['12', 'Service', '1300', '0.008', '1.5'],
            ['13', 'Sensor', '1500', '0.030', '5.0'],
            ['14', 'Service', '1700', '0.008', '1.5'],
            ['15', 'Sensor', '1900', '0.035', '5.5'],
            ['16', 'Service', '2100', '0.008', '1.5'],
            ['17', 'Sensor', '2300', '0.035', '6.0'],
        ],
        col_widths=[40, 55, 55, 50, 55]
    ))

    story.append(Paragraph("3.2 Resolution Model", h2_style))
    story.append(Paragraph(
        "Distance-based interpolation in <font face='Courier'>_measure_endcap()</font> "
        "(unchanged logic, changed input): E1 config uses "
        "<font face='Courier'>INNER_PIXEL_Z</font> (unchanged). E2/E3 config uses "
        "<font face='Courier'>SENSOR_DISK_Z</font> (v2.5 change). Threshold: 50 mm — "
        "if |z<sub>vertex</sub> − z<sub>sensor</sub>| &lt; 50 mm for any sensor → "
        "σ<sub>z</sub> = 1.0 mm (pixel), otherwise → σ<sub>z</sub> = 3.0 mm (strip). "
        "This restores the v2.2/v2.3 resolution behaviour while keeping the v2.4 material model.",
        body_style
    ))

    story.append(Paragraph("3.3 Coverage (Unchanged from v2.4)", h2_style))
    story.append(make_table(
        ['n_σ', '9-disk C_veto', '17-band C_veto', 'Increase'],
        [
            ['1.0', '0.0383 (3.8%)', '0.0557 (5.6%)', '+45.4%'],
            ['2.0', '0.0461 (4.6%)', '0.0704 (7.0%)', '+52.8%'],
            ['3.0', '0.0539 (5.4%)', '0.0852 (8.5%)', '+58.1%'],
            ['4.0', '0.0617 (6.2%)', '0.1000 (10.0%)', '+62.0%'],
            ['5.0', '0.0696 (7.0%)', '0.1148 (11.5%)', '+64.9%'],
        ],
        col_widths=[50, 100, 110, 70]
    ))

    story.append(Paragraph("3.4 Simulation Parameters (Identical to v2.4)", h2_style))
    story.append(Paragraph(
        "Masses: [0.017, 0.05, 0.1, 0.2] GeV. η scan: [1.5, 1.7, 2.0, 2.3, 2.5]. "
        "Seeds: SEED_CONV = 5, SEED_SIG = 11. Material fraction f = 0.25. "
        "Endcap config: E3. Fiducial z range: [200, 2500] mm. "
        "Tag formula: mtag_v24 (17-band p<sub>conv</sub>, unchanged).",
        body_style
    ))
    story.append(hr())

    # ── §4 Sanity Gates ──
    story.append(Paragraph("4. Sanity Gates", h1_style))
    story.append(make_table(
        ['Gate', 'Description', 'Expected'],
        [
            ['1', 'Code identity: SHA-256 of mtag_v24.py matches v2.4 record', 'PASS'],
            ['2', 'Tag formula consistency: λ > 0 far from bands, λ < 0 near bands', 'PASS'],
            ['3', 'Coverage consistency: 17-band C_veto matches v2.4 table', 'PASS'],
            ['4', 'Barrel tag formula: mtag_v21.lam() consistent (formula check)', 'PASS'],
            ['5', '9-disk E3 at η = 2.0 reproduces v2.3 values to < 0.5%', 'PASS'],
        ],
        col_widths=[35, 340, 45]
    ))
    story.append(Paragraph(
        "Gates 1–4 are identical to v2.4. Gate 5 verifies that the 9-disk baseline (which "
        "uses <font face='Courier'>SENSOR_DISK_Z</font> = original "
        "<font face='Courier'>DISK_Z</font>) is unchanged by the v2.5 code modification.",
        body_style
    ))
    story.append(hr())

    # ── §5 Validations ──
    story.append(Paragraph("5. Validations", h1_style))
    story.append(make_table(
        ['ID', 'Description', 'Criterion'],
        [
            ['V1', 'HV degradation ≥ 1.0 at all masses and η', 'No HV < 1.0'],
            ['V2', 'Tag degradation ≥ 1.0 at 17 MeV, all η', 'Tag ≥ 1.0'],
            ['V3', '200 MeV convergence', 'd(200 MeV) < 1.05'],
            ['V4', 'η symmetry: HV varies < 2% across η at 17 MeV', 'max/min < 1.02'],
            ['V5', 'Barrel results unchanged', 'v2.1 C3 match < 0.1%'],
            ['V6', 'Random seed reproducibility', 'Bitwise identical'],
        ],
        col_widths=[30, 250, 140]
    ))
    story.append(Paragraph(
        "V1–V6 are identical to v2.4. The barrel (V5) is completely unaffected by the "
        "endcap resolution change.",
        body_style
    ))
    story.append(hr())

    # ── §6 Predictions ──
    story.append(PageBreak())
    story.append(Paragraph("6. Predictions", h1_style))
    story.append(Paragraph("6.1 Retested Predictions (P1–P7)", h2_style))
    story.append(Paragraph(
        "These predictions are carried forward from v2.4 with updated expectations that "
        "account for the resolution correction.",
        body_style
    ))

    # P1-P7 table - split into description + expectation for readability
    pred_data = [
        ['P1', 'HV degradation at 17 MeV: 17-band > 9-disk (1.06×), range 1.07–1.15',
         'CONFIRMED (1.094×)', 'Likely confirmed; HV may increase slightly'],
        ['P2', 'Coverage–degradation proportionality: (d_new−1)/(d_old−1) ∈ [1.19, 2.74]',
         'CONFIRMED (1.56)', 'Uncertain; ratio may change'],
        ['P3', 'Tag/HV ratio decreases ≥ 3% at 17 MeV, η = 2.0',
         'REFUTED (+0.55%)', 'Could pass or remain refuted'],
        ['P4', 'Tag/HV > 1.0 at all η at 17 MeV',
         'CONFIRMED (1.26–3.05)', 'Likely confirmed'],
        ['P5', 'Hybrid optimal at 17 MeV',
         'CONFIRMED', 'Likely confirmed'],
        ['P6', 'HV η-independence: within ±1% of mean at 17 MeV',
         'CONFIRMED (0.23%)', 'Likely confirmed'],
        ['P7', 'High-mass convergence: 17-band HV within 3% of 9-disk at 200 MeV',
         'CONFIRMED (0.6%)', 'Likely confirmed'],
    ]
    story.append(make_table(
        ['ID', 'Description', 'v2.4 Result', 'v2.5 Expectation'],
        pred_data,
        col_widths=[25, 185, 100, 120]
    ))
    story.append(Spacer(1, 6))

    # Rationale for key predictions
    story.append(Paragraph(
        "<b>P1 rationale:</b> Wider effective veto zone at service bands "
        "(σ<sub>z</sub> = 3.0 mm → 3σ = ±9 mm vs ±3 mm with pixel) could increase "
        "HV degradation.",
        footnote_style
    ))
    story.append(Paragraph(
        "<b>P2 rationale:</b> The proportionality was measured under conflated resolution; "
        "deconflation changes d<sub>new</sub> but not d<sub>old</sub>.",
        footnote_style
    ))
    story.append(Paragraph(
        "<b>P3 rationale:</b> With strip-quality σ<sub>z</sub> at service bands, tag "
        "discrimination may degrade more than HV. However, at 17 MeV the dominant effect "
        "is conversion probability, not vertex resolution.",
        footnote_style
    ))

    story.append(Paragraph("6.2 New Predictions (P8–P10)", h2_style))
    story.append(make_table(
        ['ID', 'Description', 'Rationale'],
        [
            ['P8',
             'HV degradation at 17 MeV (η = 2.0) increases: v2.5 > v2.4 (1.094×)',
             'Wider veto zone at 7/8 service bands (3σ: ±9 mm vs ±3 mm). '
             'Modest increase expected (< 2 pp) as service bands are ~19% of total X0.'],
            ['P9',
             'Tag degradation at 17 MeV (η = 2.0) increases: v2.5 > v2.4 (1.682×)',
             'Larger σ_z broadens p_conv peaks near service bands, reducing tag '
             'discrimination at those positions.'],
            ['P10',
             '|Δd_Tag| > |Δd_HV| at 17 MeV, η = 2.0',
             'HV affected only through veto window width (binary cut). '
             'Tag uses σ_z in continuous p_conv likelihood — more sensitive to resolution.'],
        ],
        col_widths=[28, 180, 222]
    ))
    story.append(hr())

    # ── §7 Reference Values ──
    story.append(Paragraph("7. v2.4 Reference Values for Post-Registration Comparison", h1_style))
    story.append(Paragraph("7.1 Endcap E3 at η = 2.0 (f = 0.25, 17-band)", h2_style))
    story.append(make_table(
        ['Mass [MeV]', 'v2.4 HV', 'v2.4 Tag', 'v2.4 Tag/HV'],
        [
            ['17', '1.094×', '1.682×', '1.538'],
            ['50', '1.099×', '1.170×', '1.065'],
            ['100', '1.093×', '1.068×', '0.977'],
            ['200', '1.036×', '1.038×', '1.001'],
        ],
        col_widths=[70, 90, 90, 90]
    ))

    story.append(Paragraph("7.2 η Scan (17 MeV, 17-band)", h2_style))
    story.append(make_table(
        ['η', 'v2.4 HV', 'v2.4 Tag', 'v2.4 Tag/HV'],
        [
            ['1.5', '1.097×', '1.380×', '1.258'],
            ['1.7', '1.097×', '1.397×', '1.274'],
            ['2.0', '1.094×', '1.682×', '1.538'],
            ['2.3', '1.098×', '2.654×', '2.416'],
            ['2.5', '1.094×', '3.334×', '3.048'],
        ],
        col_widths=[50, 100, 100, 100]
    ))

    story.append(Paragraph("7.3 9-disk Baseline (v2.3 published)", h2_style))
    story.append(make_table(
        ['Mass [MeV]', 'v2.3 HV', 'v2.3 Tag'],
        [
            ['17', '1.06×', '1.62×'],
            ['50', '1.06×', '1.14×'],
            ['100', '1.06×', '1.05×'],
            ['200', '1.03×', '1.03×'],
        ],
        col_widths=[80, 120, 120]
    ))

    story.append(Paragraph("7.4 Barrel C3 (v2.1 published)", h2_style))
    story.append(make_table(
        ['Mass [MeV]', 'Barrel C3 HV', 'Barrel C3 Tag'],
        [
            ['17', '26.74×', '25.63×'],
            ['50', '8.83×', '8.73×'],
            ['100', '3.28×', '2.71×'],
            ['200', '1.09×', '1.09×'],
        ],
        col_widths=[80, 120, 120]
    ))
    story.append(hr())

    # ── §8 Analysis Plan ──
    story.append(Paragraph("8. Analysis Plan", h1_style))
    story.append(Paragraph("8.1 Components (Same 3 as v2.4)", h2_style))
    story.append(Paragraph(
        "(1) <b>Coverage computation</b> — confirm C<sub>veto</sub> is unchanged from v2.4. "
        "(2) <b>Hybrid strategy</b> — recompute endcap E3 degradation at η = 2.0 for all "
        "4 masses, combine with barrel C3. "
        "(3) <b>η scan</b> — recompute endcap E3 degradation at 5 η points for all 4 masses.",
        body_style
    ))

    story.append(Paragraph("8.2 Post-Registration Comparison", h2_style))
    story.append(Paragraph(
        "After computation: (1) v2.5 vs v2.4 at η = 2.0 — direct comparison to quantify "
        "the resolution conflation effect. (2) v2.5 vs v2.3 (9-disk) — assess the pure "
        "material effect without resolution conflation. (3) P1–P7 retest under corrected "
        "resolution. (4) P8–P10 evaluation. (5) Update the three-point coverage–degradation "
        "summary with resolution-corrected values.",
        body_style
    ))

    story.append(Paragraph("8.3 Key Diagnostic: Resolution Conflation Magnitude", h2_style))
    story.append(Paragraph(
        "The difference between v2.5 and v2.4 results directly measures the conflation effect: "
        "Δd<sub>HV</sub> = d<sub>HV,v2.5</sub> − d<sub>HV,v2.4</sub>, "
        "Δd<sub>Tag</sub> = d<sub>Tag,v2.5</sub> − d<sub>Tag,v2.4</sub>, "
        "ΔR = (Tag/HV)<sub>v2.5</sub> − (Tag/HV)<sub>v2.4</sub>. "
        "If the conflation had negligible impact, all Δ values should be near zero.",
        body_style
    ))
    story.append(hr())

    # ── §9 Limitations ──
    story.append(Paragraph("9. Limitations", h1_style))
    limitations = [
        "<b>Toy geometry.</b> Band positions are inspired by the CMS Phase-2 Inner Tracker "
        "but do not reproduce any real detector layout. Only qualitative trends and ratios "
        "are meaningful.",
        "<b>Single seed.</b> Results use a single random seed pair (SEED_CONV = 5, "
        "SEED_SIG = 11). Statistical fluctuations at the sub-percent level cannot be "
        "distinguished from systematic effects.",
        "<b>Simplified tracking.</b> Highland multiple scattering + Bethe–Heitler "
        "bremsstrahlung in a uniform solenoidal field; no dead zones, misalignment, or pile-up.",
        "<b>Binary resolution model.</b> The 50 mm proximity threshold for pixel vs strip "
        "quality is a simplified model. The v2.5 fix improves physical realism (service bands "
        "no longer act as sensors) but the binary threshold remains an approximation.",
        "<b>σ<sub>z</sub> does not interpolate smoothly.</b> The resolution jumps from "
        "1.0 mm to 3.0 mm at the 50 mm boundary. A more realistic model would interpolate "
        "based on distance to the nearest sensor.",
        "<b>Tag formula uses σ<sub>z</sub>.</b> The tag formula p<sub>conv</sub>(z, s) "
        "convolves the material map with a Gaussian of width σ<sub>z</sub>. With the v2.5 "
        "fix, conversions near service bands are evaluated with σ<sub>z</sub> = 3.0 mm, "
        "broadening the convolution kernel.",
        "<b>Material fraction assumptions.</b> Service band X0 values (0.005 for inner, "
        "0.008 for outer) are estimates.",
        "<b>No t-quark kinematic correlations.</b> ALP production kinematics are simplified.",
    ]
    for i, lim in enumerate(limitations, 1):
        story.append(Paragraph(f"{i}. {lim}", bullet_style))
    story.append(hr())

    # ── §10 Future Directions ──
    story.append(Paragraph("10. Future Directions", h1_style))
    story.append(Paragraph(
        "The following refinements could improve physical realism in subsequent versions, "
        "should the v2.5 results warrant further investigation:",
        body_style
    ))
    future_items = [
        "<b>Smooth resolution interpolation.</b> Replace the binary 50 mm proximity threshold "
        "with a continuous σ<sub>z</sub>(z) function that interpolates between pixel-quality "
        "(1.0 mm) and strip-quality (3.0 mm) based on distance to the nearest sensor disk, "
        "track angle, and the number of associated hits.",
        "<b>η-dependent material map.</b> Replace the uniform X<sub>0</sub> values per band "
        "with an η- and φ-dependent material budget derived from published CMS Phase-2 "
        "material scans, allowing more realistic conversion-rate gradients across the endcap.",
        "<b>Multi-seed ensemble.</b> Run multiple seed pairs to quantify statistical "
        "uncertainties on the coverage ratio and tag performance, distinguishing genuine "
        "systematic shifts from single-seed fluctuations.",
        "<b>t-quark kinematic correlations.</b> Couple the ALP η distribution to the top-quark "
        "decay kinematics and boost, introducing mass-dependent angular distributions that "
        "could shift the endcap-vs-barrel yield balance.",
        "<b>Pile-up and dead-zone effects.</b> Introduce vertex pile-up contamination and sensor "
        "dead zones to assess robustness of the displaced-vertex fit and material veto under "
        "more realistic operating conditions.",
    ]
    for i, item in enumerate(future_items, 1):
        story.append(Paragraph(f"{i}. {item}", bullet_style))
    story.append(Paragraph(
        "These directions are recorded here for transparency; they do not constitute "
        "commitments and will be evaluated based on v2.5 outcomes.",
        body_style
    ))
    story.append(hr())

    # ── §11 References ──
    story.append(Paragraph("11. References", h1_style))
    refs = [
        "[E1] L. Rygaard, J. Niedziela, R. Schäfer, S. Bruggisser, J. Alimena, S. Westhoff, "
        "F. Blekman, \"Top Secrets: Long-Lived ALPs in Top Production,\" arXiv:2306.08686.",
        "[E2] CMS Collaboration, \"The Phase-2 Upgrade of the CMS Tracker,\" "
        "CERN-LHCC-2017-009.",
        "[E3] Highland, \"Some practical remarks on multiple scattering,\" "
        "Nucl. Instrum. Meth. 129 (1975) 497–499.",
        "[E4] Bethe &amp; Heitler, \"On the stopping of fast particles and on the creation "
        "of positive electrons,\" Proc. R. Soc. Lond. A 146 (1934) 83–112.",
        "[E5] Particle Data Group, \"Review of Particle Physics,\" "
        "Prog. Theor. Exp. Phys. 2022, 083C01.",
        "[E6] J. Alimena, F. Blekman, C. Cazzaniga, X. Cid Vidal, J. Niedziela, L. Rygaard, "
        "R. Soto Rey, \"Hunting for Long-Lived ALPs in Top Events via Displaced Dielectron "
        "Pairs at the LHC,\" arXiv:2610.38932.",
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))
    story.append(hr())

    # ── §12 Reproducibility ──
    story.append(Paragraph("12. Reproducibility", h1_style))
    story.append(Paragraph("<b>Code files for v2.5:</b>", body_style))
    code_files = [
        "<font face='Courier'>run_v25.py</font> — v2.5 orchestrator (modified from v2.4 "
        "with SENSOR_DISK_Z introduction)",
        "<font face='Courier'>endcap_sim.py</font> — endcap simulation with SENSOR_DISK_Z "
        "fix (modified from v2.4)",
        "<font face='Courier'>mtag_v24.py</font> — 17-band endcap tag (unchanged from v2.4; "
        "SHA-256: <font face='Courier' size='6.5'>053a0e6c8fa70130f78a2b5970c98762"
        "396a701e8fbdd6dc695c7293f041a34d</font>)",
        "<font face='Courier'>mtag_v22.py</font> — 9-disk endcap tag (unchanged)",
        "<font face='Courier'>mtag_v21.py</font> — barrel tag (unchanged)",
        "<font face='Courier'>coverage.py</font> — coverage ratio computation (unchanged)",
    ]
    for cf in code_files:
        story.append(Paragraph(f"• {cf}", bullet_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"<b>SHA-256 of README.md (before hash insertion):</b> "
        f"<font face='Courier' size='7'>{SHA256_README}</font>",
        body_style
    ))
    story.append(Paragraph(
        f"<b>SHA-256 of README.md (final, with hash):</b> "
        f"<font face='Courier' size='7'>{FINAL_SHA256}</font>",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Seeds: SEED_CONV = 5, SEED_SIG = 11. All results reproducible from "
        "<font face='Courier'>python3 run_v25.py</font>.",
        body_style
    ))

    # ── Appendix: Comparison Charts ──
    import os
    chart_dir = os.path.dirname(os.path.abspath(__file__))
    charts_png = os.path.join(chart_dir, "dashboard_charts.png")
    preds_png = os.path.join(chart_dir, "dashboard_predictions.png")

    if os.path.exists(charts_png) and os.path.exists(preds_png):
        story.append(PageBreak())
        story.append(Paragraph("Appendix A: Comparison Charts (v2.3 / v2.4 / v2.5)", h1_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "The following charts visualise v2.4 post-registration results alongside "
            "v2.3 baselines and v2.5 predictions.  Chart data are drawn from the "
            "v2.4 post-registration README (DOI: 10.5281/zenodo.24302619).",
            body_style
        ))
        story.append(Spacer(1, 8))

        # Chart image 1 — 6-panel dashboard (scale to fit page width)
        page_w = letter[0] - 2 * 0.75 * inch  # usable width
        story.append(Paragraph("<b>Figure A-1.</b> Six-panel comparison dashboard: "
                               "HV &amp; Tag degradation mass scans, η scan, "
                               "coverage, coverage–degradation, barrel vs endcap.", body_style))
        story.append(Spacer(1, 4))
        img1 = Image(charts_png, width=page_w, height=page_w * 1.125)
        story.append(img1)

        story.append(PageBreak())
        story.append(Paragraph("Appendix A (continued): Predictions &amp; v2.5 Direction", h1_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure A-2.</b> Prediction scorecard (P1–P10), "
                               "service-band σ<sub>z</sub> change v2.4→v2.5, "
                               "and v2.5 expected directions.", body_style))
        story.append(Spacer(1, 4))
        img2 = Image(preds_png, width=page_w, height=page_w * 0.75)
        story.append(img2)

    # ── Build ──
    doc.build(story)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == '__main__':
    build_pdf()
