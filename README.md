# ALP-ttbar Toy MC v2.5 — Preregistration: Resolution Deconflation (SENSOR_DISK_Z Separation) in Displaced Light ALP → e⁺e⁻

**Author:** Won Shik Paik (Independent Researcher, Auckland, New Zealand)
**Date:** 2026-11-18
**Preregistration DOI:** https://doi.org/10.5281/zenodo.24329044
**Builds on:** v2.4 preregistration and results, https://doi.org/10.5281/zenodo.24296796 and https://doi.org/10.5281/zenodo.24302619; v2.3 preregistration and results, https://doi.org/10.5281/zenodo.24244893 and https://doi.org/10.5281/zenodo.24273586; v2.2 preregistration and results, https://doi.org/10.5281/zenodo.24189990 and https://doi.org/10.5281/zenodo.24238224; v2.1 preregistration and results, https://doi.org/10.5281/zenodo.24063091 and https://doi.org/10.5281/zenodo.24136462; v2.0 series overview, https://doi.org/10.5281/zenodo.24056097; toy study motivated by arXiv:2610.38932 [E6]
**GitHub:** https://github.com/wspaik5/ALP-ttbar-Toy-MC-v2.5-Prereg-Resolution-Deconflation
**Status:** preregistration (frozen before computation)

> **Disclaimer.** Independent personal toy study, not affiliated with the authors of arXiv:2610.38932 or arXiv:2306.08686, nor with the CMS, ATLAS, LHCb or ALICE Collaborations or the FCC study. Detector numbers are assumed; only qualitative trends and ratios are meaningful.

---

## 0. Executive Summary

The v2.4 post-registration study discovered a resolution conflation: overriding the `DISK_Z` array with all 17 band positions (9 sensor disks + 8 service bands) caused the simulation to assign pixel-quality z resolution (σ_z = 1.0 mm) near service bands, which represent passive material (cables, cooling, support structures) and should not provide measurement capability. This conflation means the v2.4 degradation and tag performance values reflect the combined effect of increased coverage *and* artificially improved measurement resolution, and cannot be attributed to coverage alone.

The v2.5 study introduces a targeted code fix — a new `SENSOR_DISK_Z` array containing only the 9 sensor disk positions — and uses it exclusively in the `_measure_endcap()` function for z resolution assignment. All other uses of `DISK_Z` (conversion generation, veto placement, tag formula evaluation, nearest-disk Δχ²_L pull) continue to use the full 17-band array. The geometry, random seeds, and all other parameters remain identical to v2.4.

This separation isolates the resolution effect from the material effect, enabling a direct comparison of v2.5 results against the published v2.4 values to quantify the impact of the conflation. The seven original predictions (P1–P7) are retested with updated expectations that account for the corrected resolution model, and three new predictions (P8–P10) are introduced to characterise the deconflation effect itself.

---

## 1. Motivation

### 1.1 The Resolution Conflation Problem

In `endcap_sim.py`, the function `_measure_endcap()` assigns z vertex resolution based on proximity to elements in `DISK_Z`:

```python
# E2, E3 config (lines ~215-220 in endcap_sim.py):
near_any = np.zeros(len(z_true), bool)
for zd in DISK_Z:
    near_any |= (np.abs(z_true - zd) < 50.0)
sz_base = np.where(near_any, VTX_RES_PIXEL, VTX_RES_STRIP)
```

When `DISK_Z` contains all 17 band positions (as in v2.4), vertices near service bands at z = 265, 375, 535, 720, 960, 1300, 1700, 2100 mm receive pixel-quality resolution (σ_z = 1.0 mm) even though these positions represent passive material with no active sensors.

**Physical interpretation:** In a real tracker, z resolution depends on sensor placement. Passive material (cables, cooling pipes, support rings) generates photon conversions but provides no measurement points. A vertex reconstructed near a service band should rely on the nearest *sensor* disk for its z measurement, receiving degraded resolution proportional to the distance from that sensor.

### 1.2 Quantitative Example

Consider the service band at z = 960 mm (band S5, midpoint of the 820–1100 mm gap):

- **v2.4 (conflated):** z = 960 mm is in `DISK_Z`, so |960 − 960| = 0 < 50 mm → σ_z = 1.0 mm (pixel quality).
- **v2.5 (deconflated):** `SENSOR_DISK_Z` = [230, 300, 450, 620, 820, 1100, 1500, 1900, 2300]. Nearest sensors are z = 820 mm and z = 1100 mm, both at distance 140 mm > 50 mm → σ_z = 3.0 mm (strip quality).

The resolution at this position changes by a factor of 3. This affects:
1. The vertex fit quality (Δχ²_T and Δχ²_L), which uses σ_z.
2. The tag formula evaluation, which uses σ_z through the p_conv convolution.
3. The hard-veto zone width at 3σ: ±3 mm (pixel) → ±9 mm (strip).

### 1.3 Service Band Distances to Nearest Sensor

| Service Band | z [mm] | Nearest Sensor z [mm] | Distance [mm] | v2.4 σ_z | v2.5 σ_z |
|-------------|--------|----------------------|---------------|----------|----------|
| S1 (230–300 gap) | 265 | 230 | 35 | 1.0 mm | 1.0 mm* |
| S2 (300–450 gap) | 375 | 300 or 450 | 75 | 1.0 mm | 3.0 mm |
| S3 (450–620 gap) | 535 | 450 or 620 | 85 | 1.0 mm | 3.0 mm |
| S4 (620–820 gap) | 720 | 620 or 820 | 100 | 1.0 mm | 3.0 mm |
| S5 (820–1100 gap) | 960 | 820 or 1100 | 140 | 1.0 mm | 3.0 mm |
| S6 (1100–1500 gap) | 1300 | 1100 or 1500 | 200 | 1.0 mm | 3.0 mm |
| S7 (1500–1900 gap) | 1700 | 1500 or 1900 | 200 | 1.0 mm | 3.0 mm |
| S8 (1900–2300 gap) | 2100 | 1900 or 2300 | 200 | 1.0 mm | 3.0 mm |

*S1 at z = 265 mm is within 50 mm of the sensor disk at z = 230 mm (distance 35 mm), so its resolution is unchanged by the deconflation.

Of the 8 service bands, 7 are further than 50 mm from any sensor disk and will experience a resolution change from 1.0 mm to 3.0 mm. Only S1 (the barrel–endcap transition service band) remains at pixel quality.

---

## 2. Code Change

### 2.1 The Fix

A single new module-level array is introduced in `endcap_sim.py`:

```python
# 9 sensor disk z positions only (identical to v2.2/v2.3 DISK_Z)
SENSOR_DISK_Z = np.array([230., 300., 450., 620., 820., 1100., 1500., 1900., 2300.])
```

The `_measure_endcap()` function is modified to use `SENSOR_DISK_Z` instead of `DISK_Z` for the E2/E3 resolution assignment loop:

```python
# BEFORE (v2.4):
for zd in DISK_Z:          # 17 bands — service bands get pixel resolution
    near_any |= (np.abs(z_true - zd) < 50.0)

# AFTER (v2.5):
for zd in SENSOR_DISK_Z:   # 9 sensor disks only — service bands get strip resolution
    near_any |= (np.abs(z_true - zd) < 50.0)
```

### 2.2 What Does NOT Change

All other uses of `DISK_Z` in `endcap_sim.py` remain with the full 17-band array:

| Function | Use of DISK_Z | Array in v2.5 |
|----------|--------------|---------------|
| `_measure_endcap()` — resolution assignment | Proximity check for σ_z | **SENSOR_DISK_Z** (9 sensors) |
| `endcap_conversions()` — conversion generation | Material positions for photon conversion | DISK_Z (17 bands) |
| `endcap_material_veto()` — hard veto | Band positions for veto window | DISK_Z (17 bands) |
| `compute_dchi2_endcap()` — Δχ²_L nearest-disk pull | Nearest band for longitudinal pull | DISK_Z (17 bands) |
| `mtag_v24.p_conv()` — tag formula | Material map for conversion probability | DISKS (17 bands) |

### 2.3 Runtime Override

The `install_v25_geometry()` function in `run_v25.py` performs the same override as v2.4:

```python
ec.DISK_Z  = np.array([d[0] for d in mtag_v24.DISKS])   # 17 bands
ec.DISK_X0 = np.array([d[1] for d in mtag_v24.DISKS])   # 17 bands
ec.DISK_HW = np.array([d[2] for d in mtag_v24.DISKS])   # 17 bands
```

Additionally, v2.5 introduces:

```python
ec.SENSOR_DISK_Z = np.array([230., 300., 450., 620., 820., 1100., 1500., 1900., 2300.])
```

The `_measure_endcap()` function references `SENSOR_DISK_Z` from the module scope, so this override takes effect without further changes.

---

## 3. Geometry and Parameters

### 3.1 17-Band Endcap Geometry (Identical to v2.4)

The combined 17-band geometry is unchanged from v2.4. All bands sorted by z:

| Band | Type | z [mm] | X0 | HW [mm] |
|------|------|--------|-----|---------|
| 1 | Sensor | 230 | 0.006 | 1.5 |
| 2 | Service | 265 | 0.005 | 1.5 |
| 3 | Sensor | 300 | 0.020 | 3.0 |
| 4 | Service | 375 | 0.005 | 1.5 |
| 5 | Sensor | 450 | 0.020 | 3.0 |
| 6 | Service | 535 | 0.005 | 1.5 |
| 7 | Sensor | 620 | 0.020 | 3.0 |
| 8 | Service | 720 | 0.005 | 1.5 |
| 9 | Sensor | 820 | 0.022 | 3.5 |
| 10 | Service | 960 | 0.008 | 1.5 |
| 11 | Sensor | 1100 | 0.030 | 4.5 |
| 12 | Service | 1300 | 0.008 | 1.5 |
| 13 | Sensor | 1500 | 0.030 | 5.0 |
| 14 | Service | 1700 | 0.008 | 1.5 |
| 15 | Sensor | 1900 | 0.035 | 5.5 |
| 16 | Service | 2100 | 0.008 | 1.5 |
| 17 | Sensor | 2300 | 0.035 | 6.0 |

### 3.2 Resolution Model

The distance-based interpolation in `_measure_endcap()` (unchanged logic, changed input):

- For E1 config: resolution is based on proximity to `INNER_PIXEL_Z` (unchanged).
- For E2/E3 config: resolution is based on proximity to `SENSOR_DISK_Z` (v2.5 change).
- Threshold: 50 mm. If `|z_vertex − z_sensor| < 50 mm` for any sensor → σ_z = 1.0 mm (pixel). Otherwise → σ_z = 3.0 mm (strip).

This is the same logic as v2.2/v2.3 (which used the original 9-disk `DISK_Z`). The v2.5 fix restores the v2.2/v2.3 resolution behaviour while keeping the v2.4 material model.

### 3.3 Coverage (Unchanged from v2.4)

Coverage depends on band positions and half-widths, not on measurement resolution. The coverage table is identical to v2.4:

| n_σ | 9-disk C_veto | 17-band C_veto | Increase |
|-----|---------------|----------------|----------|
| 1.0 | 0.0383 (3.8%) | 0.0557 (5.6%) | +45.4% |
| 2.0 | 0.0461 (4.6%) | 0.0704 (7.0%) | +52.8% |
| 3.0 | 0.0539 (5.4%) | 0.0852 (8.5%) | +58.1% |
| 4.0 | 0.0617 (6.2%) | 0.1000 (10.0%) | +62.0% |
| 5.0 | 0.0696 (7.0%) | 0.1148 (11.5%) | +64.9% |

### 3.4 Simulation Parameters (Identical to v2.4)

- Masses: [0.017, 0.05, 0.1, 0.2] GeV
- η scan: [1.5, 1.7, 2.0, 2.3, 2.5]
- Seeds: SEED_CONV = 5, SEED_SIG = 11
- Material fraction f = 0.25
- Endcap config: E3 (unless otherwise stated)
- Fiducial z range: [200, 2500] mm
- Tag formula: mtag_v24 (17-band p_conv, unchanged)

---

## 4. Sanity Gates

| Gate | Description | Expected |
|------|-------------|----------|
| 1 | Code identity: SHA-256 of mtag_v24.py matches v2.4 record (`053a0e6c...f041a34d`) | PASS |
| 2 | Tag formula consistency: mtag_v24.lam() produces λ > 0 far from bands, λ < 0 near bands | PASS |
| 3 | Coverage consistency: 17-band C_veto matches v2.4 §3.1 table values to < 5 × 10⁻⁴ | PASS |
| 4 | Barrel tag formula: mtag_v21.lam() consistent to 10⁻¹² at test points (formula check only) | PASS |
| 5 | v2.4 resolution-corrected baseline: 9-disk E3 at η = 2.0 reproduces v2.3 published values to < 0.5% at all 4 masses | PASS |

**Gate 1–4** are identical to v2.4. **Gate 5** verifies that the 9-disk baseline (which uses `SENSOR_DISK_Z` = original `DISK_Z`) is unchanged by the v2.5 code modification. Since v2.3 used the original 9-disk `DISK_Z` for resolution (which is now `SENSOR_DISK_Z`), the 9-disk results should be identical to v2.3.

---

## 5. Validations

| ID | Description | Criterion |
|----|-------------|-----------|
| V1 | HV degradation ≥ 1.0 at all masses and η | No mass point shows HV < 1.0 |
| V2 | Tag degradation ≥ 1.0 at 17 MeV, all η | Tag at 17 MeV never below 1.0 |
| V3 | 200 MeV convergence: HV and tag within 5% of 1.0 | d(200 MeV) < 1.05 for both strategies |
| V4 | η symmetry: HV degradation varies by < 2% across η at 17 MeV | max/min < 1.02 |
| V5 | Barrel results unchanged (identical to v2.1 published) | v2.1 C3 barrel values match to < 0.1% |
| V6 | Random seed reproducibility: same seeds produce same results | Bitwise identical on rerun |

V1–V6 are identical to v2.4. The barrel (V5) is completely unaffected by the endcap resolution change.

---

## 6. Predictions

### 6.1 Retested Predictions (P1–P7)

These predictions are carried forward from v2.4 with updated expectations that account for the resolution correction.

| ID | Description | v2.4 Result | v2.5 Expectation | Rationale |
|----|-------------|-------------|------------------|-----------|
| P1 | HV degradation at 17 MeV: 17-band > 9-disk (1.06×), range 1.07–1.15 | CONFIRMED (1.094×) | Likely confirmed; HV may increase slightly | Wider effective veto zone at service bands (σ_z = 3.0 mm → 3σ = ±9 mm vs ±3 mm with pixel) could increase HV degradation |
| P2 | Coverage–degradation proportionality: (d_new−1)/(d_old−1) ∈ [1.19, 2.74] | CONFIRMED (1.56) | Uncertain; ratio may change | The proportionality was measured under conflated resolution; deconflation changes the numerator d_new but not d_old |
| P3 | Tag/HV ratio decreases ≥ 3% at 17 MeV, η = 2.0 | REFUTED (+0.55%) | Could pass or remain refuted | With strip-quality σ_z at service bands, tag discrimination may degrade more than HV. However, at 17 MeV the dominant effect is conversion probability, not vertex resolution |
| P4 | Tag/HV > 1.0 at all η at 17 MeV | CONFIRMED (1.26–3.05) | Likely confirmed | Tag still uses the full 17-band material map; large margin in v2.4 suggests robustness |
| P5 | Hybrid optimal at 17 MeV | CONFIRMED | Likely confirmed | Barrel unaffected; endcap HV may increase; strategy rankings unlikely to invert |
| P6 | HV η-independence: all within ±1% of mean at 17 MeV | CONFIRMED (0.23%) | Likely confirmed | The z-based veto coverage is structurally η-independent |
| P7 | High-mass convergence: 17-band HV within 3% of 9-disk at 200 MeV | CONFIRMED (0.6%) | Likely confirmed | At 200 MeV, long-lived ALPs decay far from material; resolution near bands has minimal impact |

### 6.2 New Predictions (P8–P10)

| ID | Description | Rationale |
|----|-------------|-----------|
| P8 | HV degradation at 17 MeV (η = 2.0) increases: v2.5 > v2.4 (1.094×) | With strip-quality resolution at 7 of 8 service bands, the effective veto zone widens (3σ: ±9 mm vs ±3 mm). This wider zone captures more signal vertices near service bands, increasing background rejection loss. The increase is expected to be modest (< 2 percentage points) because service bands contribute only ~19% of total X0. |
| P9 | Tag degradation at 17 MeV (η = 2.0) increases: v2.5 > v2.4 (1.682×) | The tag formula evaluates p_conv using σ_z. With larger σ_z near service bands, the convolved conversion peaks become broader and lower, reducing the tag's ability to distinguish signal from conversion at those positions. This should increase the tag's false-negative rate. |
| P10 | The absolute change in HV degradation (|d_HV,v2.5 − d_HV,v2.4|) is smaller than the absolute change in tag degradation (|d_Tag,v2.5 − d_Tag,v2.4|) at 17 MeV, η = 2.0 | The hard veto is a binary cut on z proximity, so it is affected by σ_z only through the veto window width (3σ). The tag uses σ_z in the continuous p_conv likelihood, so its discrimination is more sensitive to resolution changes. The tag should therefore show a larger absolute shift than the HV. |

---

## 7. v2.4 Reference Values for Post-Registration Comparison

### 7.1 Endcap E3 at η = 2.0 (f = 0.25, 17-band)

| Mass [MeV] | v2.4 HV | v2.4 Tag | v2.4 Tag/HV |
|------------|---------|----------|-------------|
| 17 | 1.094× | 1.682× | 1.538 |
| 50 | 1.099× | 1.170× | 1.065 |
| 100 | 1.093× | 1.068× | 0.977 |
| 200 | 1.036× | 1.038× | 1.001 |

### 7.2 η Scan (17 MeV, 17-band)

| η | v2.4 HV | v2.4 Tag | v2.4 Tag/HV |
|-----|---------|----------|-------------|
| 1.5 | 1.097× | 1.380× | 1.258 |
| 1.7 | 1.097× | 1.397× | 1.274 |
| 2.0 | 1.094× | 1.682× | 1.538 |
| 2.3 | 1.098× | 2.654× | 2.416 |
| 2.5 | 1.094× | 3.334× | 3.048 |

### 7.3 9-disk Baseline (v2.3 published, for P2 calculation)

| Mass [MeV] | v2.3 published HV | v2.3 published Tag |
|------------|-------------------|-------------------|
| 17 | 1.06× | 1.62× |
| 50 | 1.06× | 1.14× |
| 100 | 1.06× | 1.05× |
| 200 | 1.03× | 1.03× |

### 7.4 Barrel C3 (v2.1 published, for hybrid strategy)

| Mass [MeV] | Barrel C3 HV | Barrel C3 Tag |
|------------|-------------|---------------|
| 17 | 26.74× | 25.63× |
| 50 | 8.83× | 8.73× |
| 100 | 3.28× | 2.71× |
| 200 | 1.09× | 1.09× |

---

## 8. Analysis Plan

### 8.1 Components (Same 3 as v2.4)

1. **Coverage computation** — confirm C_veto is unchanged from v2.4 (pure geometry, no resolution dependence).
2. **Hybrid strategy** — recompute endcap E3 degradation at η = 2.0 for all 4 masses, combine with barrel C3 for uniform/hybrid/reverse-hybrid comparison.
3. **η scan** — recompute endcap E3 degradation at 5 η points for all 4 masses.

### 8.2 Post-Registration Comparison

After computation, the following comparisons will be made:

1. **v2.5 vs v2.4 at η = 2.0:** Direct comparison of HV and tag degradation at all 4 masses to quantify the resolution conflation effect.
2. **v2.5 vs v2.3 (9-disk):** To assess the pure material effect (without resolution conflation) of adding service bands.
3. **P1–P7 retest:** Evaluate all 7 original predictions under the corrected resolution model.
4. **P8–P10 evaluation:** Test the new deconflation-specific predictions.
5. **Coverage–degradation relationship:** Update the three-point (barrel, 9-disk, 17-band) summary with resolution-corrected endcap values.

### 8.3 Key Diagnostic: Resolution Conflation Magnitude

The difference between v2.5 and v2.4 results at each mass and η point directly measures the resolution conflation effect:

- Δd_HV = d_HV,v2.5 − d_HV,v2.4
- Δd_Tag = d_Tag,v2.5 − d_Tag,v2.4
- ΔR = (Tag/HV)_v2.5 − (Tag/HV)_v2.4

If the resolution conflation had negligible impact, all Δ values should be near zero. If the conflation materially affected the v2.4 results, the Δ values will indicate both the direction and magnitude of the bias.

---

## 9. Limitations (Carried from v2.4 §8, with modifications)

1. **Toy geometry.** Band positions are inspired by the CMS Phase-2 Inner Tracker but do not reproduce any real detector layout. Only qualitative trends and ratios are meaningful.
2. **Single seed.** Results use a single random seed pair (SEED_CONV = 5, SEED_SIG = 11). Statistical fluctuations at the sub-percent level cannot be distinguished from systematic effects.
3. **Simplified tracking.** Highland multiple scattering + Bethe–Heitler bremsstrahlung in a uniform solenoidal field; no dead zones, misalignment, or pile-up.
4. **Binary resolution model.** The 50 mm proximity threshold for pixel vs strip quality is a simplified model. A real tracker would have a more gradual resolution transition based on track propagation and hit association. The v2.5 fix improves the model's physical realism (service bands no longer act as sensors) but the binary threshold remains an approximation.
5. **σ_z does not interpolate smoothly.** The resolution jumps from 1.0 mm to 3.0 mm at the 50 mm boundary. A more realistic model would interpolate based on distance to the nearest sensor, track angle, and number of associated hits. This is noted as a potential refinement for future versions.
6. **Tag formula uses σ_z.** The tag formula `p_conv(z, s)` convolves the material map with a Gaussian of width σ_z. With the v2.5 fix, conversions near service bands are evaluated with σ_z = 3.0 mm, broadening the convolution kernel. This is physically more appropriate (the measurement is less precise) but changes both the tag's numerator and its discrimination power simultaneously.
7. **Material fraction assumptions.** Service band X0 values (0.005 for inner, 0.008 for outer) are estimates; real service material varies with η and azimuthal position.
8. **No t-quark kinematic correlations.** ALP production kinematics are simplified; the η distribution is independent of the ALP mass and production mechanism.

---

## 10. Future Directions

The following refinements could improve physical realism in subsequent versions, should the v2.5 results warrant further investigation:

1. **Smooth resolution interpolation.** Replace the binary 50 mm proximity threshold with a continuous σ_z(z) function that interpolates between pixel-quality (1.0 mm) and strip-quality (3.0 mm) based on distance to the nearest sensor disk, track angle, and the number of associated hits.
2. **η-dependent material map.** Replace the uniform X0 values per band with an η- and φ-dependent material budget derived from published CMS Phase-2 material scans, allowing more realistic conversion-rate gradients across the endcap.
3. **Multi-seed ensemble.** Run multiple seed pairs to quantify statistical uncertainties on the coverage ratio and tag performance, distinguishing genuine systematic shifts from single-seed fluctuations.
4. **t-quark kinematic correlations.** Couple the ALP η distribution to the top-quark decay kinematics and boost, introducing mass-dependent angular distributions that could shift the endcap-vs-barrel yield balance.
5. **Pile-up and dead-zone effects.** Introduce vertex pile-up contamination and sensor dead zones to assess robustness of the displaced-vertex fit and material veto under more realistic operating conditions.

These directions are recorded here for transparency; they do not constitute commitments and will be evaluated based on v2.5 outcomes.

---

## 11. References

[E1] L. Rygaard, J. Niedziela, R. Schäfer, S. Bruggisser, J. Alimena, S. Westhoff, F. Blekman, "Top Secrets: Long-Lived ALPs in Top Production," arXiv:2306.08686.
[E2] CMS Collaboration, "The Phase-2 Upgrade of the CMS Tracker," CERN-LHCC-2017-009.
[E3] Highland, "Some practical remarks on multiple scattering," Nucl. Instrum. Meth. 129 (1975) 497–499.
[E4] Bethe & Heitler, "On the stopping of fast particles and on the creation of positive electrons," Proc. R. Soc. Lond. A 146 (1934) 83–112.
[E5] Particle Data Group, "Review of Particle Physics," Prog. Theor. Exp. Phys. 2022, 083C01.
[E6] J. Alimena, F. Blekman, C. Cazzaniga, X. Cid Vidal, J. Niedziela, L. Rygaard, R. Soto Rey, "Hunting for Long-Lived ALPs in Top Events via Displaced Dielectron Pairs at the LHC," arXiv:2610.38932.

---

## 12. Reproducibility

**Code files for v2.5 (to be distributed with this preregistration):**
- `run_v25.py` — v2.5 orchestrator (modified from v2.4 `run_v24.py` with SENSOR_DISK_Z introduction)
- `endcap_sim.py` — endcap simulation with SENSOR_DISK_Z fix (modified from v2.4)
- `mtag_v24.py` — 17-band endcap tag (unchanged from v2.4; SHA-256: `053a0e6c8fa70130f78a2b5970c98762396a701e8fbdd6dc695c7293f041a34d`)
- `mtag_v22.py` — 9-disk endcap tag (unchanged)
- `mtag_v21.py` — barrel tag (unchanged)
- `coverage.py` — coverage ratio computation (unchanged)

**SHA-256 of this README:** `e3d17539f43b9634a826239a2f5aef55e304197a8df618abbd82292d7ab644f5`

Seeds: SEED_CONV = 5, SEED_SIG = 11. All results reproducible from `python3 run_v25.py`.
