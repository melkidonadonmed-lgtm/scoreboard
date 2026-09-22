"""
Module 08: Neurology, Neurosurgery & Neurotrauma (Block 03)
Monographically exhaustive clinical tools with zero truncation:
1. Rotterdam Score (TCE)
2. Marshall CT Classification (TCE)
3. ASIA / AIS Impairment Scale (TRM)
4. Hunt-Hess Scale (HSA)
5. WFNS Scale (HSA)
6. Fisher Classic Scale (HSA)
7. Modified Fisher / Claassen Scale (HSA)
8. Spetzler-Martin Grade (MAV)
9. NIHSS (Full 11 domains / 15 operational items)
10. ASPECTS (10 zones MCA, baseScore 10, subtractive)
11. ICH Score (GCS, Volume cm3, IVH, Infratentorial, Age >= 80)
12. ABCD2 Score (Age, BP, Clinical, Duration, Diabetes)
13. mRS (Modified Rankin Scale 0 to 6)
14. KPS (Karnofsky Performance Status 0-100%)
15. MEEM / MMSE (Folstein with Brazilian schooling tiers)
16. MoCA (Montreal Cognitive Assessment)
17. Hoehn & Yahr (Parkinson staging 0 to 5 including 1.5, 2.5)
18. EDSS (Kurtzke Disability Scale 0.0 to 10.0 in 0.5 increments)
"""

from calculators.block03_neuro.neurotrauma import (
    get_rotterdam,
    get_marshall,
    get_asia_ais,
)
from calculators.block03_neuro.hsa_mav import (
    get_hunt_hess,
    get_wfns,
    get_fisher_classic,
    get_fisher_modified,
    get_spetzler_martin,
)
from calculators.block03_neuro.stroke import (
    get_nihss,
    get_aspects,
    get_ich_score,
    get_abcd2,
)
from calculators.block03_neuro.functional_cognitive import (
    get_mrs,
    get_kps,
    get_meem_mmse,
    get_moca,
    get_hoehn_yahr,
    get_edss,
)

def get_block_03_calculators():
    """Returns all 18 clinical calculators for Block 03 with block metadata attached."""
    calculators = [
        get_rotterdam(),
        get_marshall(),
        get_asia_ais(),
        get_hunt_hess(),
        get_wfns(),
        get_fisher_classic(),
        get_fisher_modified(),
        get_spetzler_martin(),
        get_nihss(),
        get_aspects(),
        get_ich_score(),
        get_abcd2(),
        get_mrs(),
        get_kps(),
        get_meem_mmse(),
        get_moca(),
        get_hoehn_yahr(),
        get_edss(),
    ]
    for calc in calculators:
        calc["blockId"] = "block_03"
        calc["blockFile"] = "block_03.json"
    return calculators
