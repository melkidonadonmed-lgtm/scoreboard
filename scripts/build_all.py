#!/usr/bin/env python3
"""
Assemble Block 01, Block 03 JSONs and Unified Manifest JSON for Scoreboard App.
Outputs:
- src/data/blocks/block_01.json (19 calculators)
- src/data/blocks/block_03.json (18 calculators)
- src/data/manifest.json (37 lightweight index items)
"""

import json
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculators.mod1_sepsis import get_qsofa, get_sofa, get_apache_ii, get_saps_3
from calculators.mod2_vte import get_wells_tep, get_wells_tvp, get_geneva, get_perc, get_pesi, get_spesi
from calculators.mod3_coma import get_glasgow_p, get_four, get_rass, get_sas, get_cam_icu
from calculators.mod4_pancreatitis import get_ranson, get_bisap, get_balthazar_ctsi, get_marshall_mod
from calculators.mod8_neuro import get_block_03_calculators

def build_manifest_item(calc, search_synonyms, starred_default=False):
    block_id = calc.get("blockId", "block_01")
    block_file = calc.get("blockFile", f"{block_id}.json")
    return {
        "id": calc["id"],
        "slug": calc["slug"],
        "name": calc["name"],
        "acronym": calc["acronym"],
        "category": calc.get("category", calc.get("categoryName", "Medicina Clínica")),
        "subcategory": calc.get("subcategory", calc.get("moduleName", "")),
        "categorySlug": calc["categorySlug"],
        "categoryName": calc["categoryName"],
        "moduleName": calc["moduleName"],
        "description": calc.get("description", calc["summary"]),
        "summary": calc["summary"],
        "synonyms": search_synonyms,
        "searchSynonyms": search_synonyms,
        "calculationType": calc["calculationType"],
        "blockId": block_id,
        "blockFile": block_file,
        "evidenceSource": calc["evidenceSource"],
        "badge": calc.get("badge", "clinica"),
        "hasInfusionProtocol": bool(calc.get("riskTiers", [{}])[-1].get("infusionProtocol") or calc.get("hasInfusionProtocol")),
        "starredDefault": starred_default
    }

def validate_calculator_structure(calc):
    """Verifies that the calculator conforms strictly to schema contracts."""
    required_keys = [
        "id", "slug", "name", "acronym", "categorySlug",
        "summary", "calculationType", "evidenceSource",
        "minPossibleScore", "maxPossibleScore",
        "parameterGroups", "riskTiers", "radarAxes"
    ]
    for key in required_keys:
        assert key in calc, f"Calculator {calc.get('id')} missing required field: {key}"

    assert calc["calculationType"] in ["additive_points", "continuous_formula", "branching_decision"], \
        f"Invalid calculationType in {calc['id']}: {calc['calculationType']}"

    assert len(calc["parameterGroups"]) >= 1, f"Calculator {calc['id']} must have at least 1 parameterGroup"
    assert len(calc["riskTiers"]) >= 1, f"Calculator {calc['id']} must have at least 1 riskTier"
    assert len(calc["radarAxes"]) >= 1, f"Calculator {calc['id']} must have at least 1 radarAxis"

    # Validate risk tiers
    for tier in calc["riskTiers"]:
        assert "id" in tier and "label" in tier and "severityLevel" in tier, f"Invalid tier in {calc['id']}: {tier}"
        assert "minScore" in tier and "maxScore" in tier, f"Tier missing minScore/maxScore in {calc['id']}: {tier}"
        assert "statisticalOutcome" in tier and "colorHex" in tier, f"Tier missing outcome/color in {calc['id']}: {tier}"

def main():
    # -------------------------------------------------------------------------
    # 1. COMPILE BLOCK 01 CALCULATORS (19 Tools)
    # -------------------------------------------------------------------------
    block_01_calculators = [
        # Module 01: Sepsis & Organ Dysfunction
        get_qsofa(),
        get_sofa(),
        get_apache_ii(),
        get_saps_3(),

        # Module 02: VTE (DVT & PE)
        get_wells_tep(),
        get_wells_tvp(),
        get_geneva(),
        get_perc(),
        get_pesi(),
        get_spesi(),

        # Module 03: Coma, Level of Consciousness & Sedation
        get_glasgow_p(),
        get_four(),
        get_rass(),
        get_sas(),
        get_cam_icu(),

        # Module 04: Emergency Gastroenterology - Acute Pancreatitis
        get_ranson(),
        get_bisap(),
        get_balthazar_ctsi(),
        get_marshall_mod()
    ]

    for calc in block_01_calculators:
        calc["blockId"] = "block_01"
        calc["blockFile"] = "block_01.json"
        validate_calculator_structure(calc)

    print(f"Block 01 calculators compiled: {len(block_01_calculators)}")
    assert len(block_01_calculators) == 19, f"Expected 19 calculators in Block 01, got {len(block_01_calculators)}"

    block_01_data = {
        "blockId": "block_01",
        "blockName": "Emergência, Choque e Terapia Intensiva",
        "version": "1.0.0",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "description": "Dossiês monográficos completos dos 19 escores de emergência, choque e terapia intensiva com preservação estrita de parâmetros, estratificações de risco, condutas farmacológicas e protocolos de BIC.",
        "calculators": block_01_calculators
    }

    # -------------------------------------------------------------------------
    # 2. COMPILE BLOCK 03 CALCULATORS (18 Tools)
    # -------------------------------------------------------------------------
    block_03_calculators = get_block_03_calculators()
    for calc in block_03_calculators:
        validate_calculator_structure(calc)

    print(f"Block 03 calculators compiled: {len(block_03_calculators)}")
    assert len(block_03_calculators) == 18, f"Expected 18 calculators in Block 03, got {len(block_03_calculators)}"

    block_03_data = {
        "blockId": "block_03",
        "blockName": "Neurologia e Neurocirurgia",
        "version": "1.0.0",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "description": "Dossiês monográficos completos dos 18 escores clínicos e cirúrgicos de neurologia, neurocirurgia e neurotrauma com parâmetros exaustivos, estratificações prognósticas, condutas farmacológicas rigorosas e diretrizes de intervenção.",
        "calculators": block_03_calculators
    }

    # -------------------------------------------------------------------------
    # 3. CLINICAL BRAZILIAN SYNONYMS MAP
    # -------------------------------------------------------------------------
    SYNONYMS_MAP = {
        # Block 01 Tools
        "calc_qsofa": [
            "sepse", "triagem de sepse", "quick sofa", "qsofa", "choque septico", "choque séptico",
            "infeccao", "infecção", "infeccao grave", "leito de enfermaria", "triagem clinica",
            "taquipneia", "hipotensao", "hipotensão", "rebaixamento", "alteracao mental",
            "escala de sepse rapida", "sepsis 3", "ssc 2021", "surviving sepsis", "glasgow",
            "lactato", "sala vermelha", "rastreio infeccioso", "bacteremia", "foco septico",
            "noradrenalina", "vasopressor", "pacote 1 hora", "cid a41", "cid a41.9"
        ],
        "calc_sofa": [
            "sofa", "sofa completo", "sequential organ failure assessment", "disfuncao organica",
            "disfunção orgânica", "falencia multiorganica", "falência múltipla de órgãos", "uti",
            "terapia intensiva", "sepse", "choque septico", "paafi", "relacao pao2 fio2",
            "plaquetopenia", "coagulopatia", "bilirrubina", "ictericia", "hepatite",
            "noradrenalina", "vasopressina", "dobutamina", "adrenalina", "dopamina",
            "creatinina", "oliguria", "insuficiencia renal", "lra", "glasgow",
            "delta sofa", "sepsis 3", "vincent 1996", "cid a41"
        ],
        "calc_apache_ii": [
            "apache", "apache 2", "apache ii", "acute physiology and chronic health",
            "prognostico uti", "prognóstico uti", "mortalidade hospitalar", "escore prognostico",
            "gravidade uti", "primeiras 24 horas", "doenca cronica", "cirurgia de urgencia",
            "temperatura central", "pam", "fc", "leucocitos", "gasometria", "sodio", "potassio",
            "creatinina", "insuficiencia renal aguda", "fisiologia aguda", "calibracao uti"
        ],
        "calc_saps_3": [
            "saps", "saps 3", "saps iii", "simplified acute physiology score",
            "admissao uti", "admissão uti", "primeira hora uti", "prognostico uti",
            "probabilidade de obito", "mortalidade calibrada", "america latina",
            "caixa 1 caixa 2 caixa 3", "origem do paciente", "drogas vasoativas",
            "ventilacao mecanica", "glasgow admissao", "indice de gravidade uti"
        ],
        "calc_wells_tep": [
            "wells tep", "escore de wells", "tromboembolismo pulmonar", "tep", "embolia pulmonar",
            "embolia", "dor pleuritica", "dispneia subita", "falta de ar aguda", "hemoptise",
            "taquicardia", "tvp associada", "cancer ativo", "imobilizacao leito", "cirurgia recente",
            "anticoagulacao", "enoxaparina", "clexane", "heparina", "angio tc", "angiotomografia",
            "d-dimero", "ddimero", "probabilidade pre-teste", "esc guidelines", "cid i26"
        ],
        "calc_wells_tvp": [
            "wells tvp", "trombose venosa profunda", "tvp", "tromboflebite", "edema de perna",
            "dor na panturrilha", "assimetria de membros", "cacifo godet", "veias colaterais",
            "cirurgia ortopedica", "artroplastia", "anticoagulacao plena", "doppler venoso",
            "ultrassom vascular", "d-dimero", "cisto de baker", "celulite erisipela", "cid i80"
        ],
        "calc_geneva": [
            "geneva", "geneva revisado", "escore de genebra", "tep objetivo", "embolia pulmonar",
            "tromboembolismo", "dor toracica", "dispneia", "idade 65", "fc 75 95",
            "cirurgia recente", "fratura", "hemoptise", "d-dimero", "angiotomografia torax"
        ],
        "calc_perc": [
            "perc", "criterios de perc", "pulmonary embolism rule out", "exclusao de tep",
            "regra de perc", "baixo risco tep", "dispensar d-dimero", "evitar angio tc",
            "saturacao 95", "fc 100", "idade 50", "estrogenio aco", "anticoncepcional"
        ],
        "calc_pesi": [
            "pesi", "pulmonary embolism severity index", "gravidade do tep", "mortalidade 30 dias",
            "estratificacao tep", "classes pesi", "classe i classe ii", "classe v",
            "alta hospitalar tep", "tratamento ambulatorial", "doac", "rivaroxabana",
            "apixabana", "insuficiencia cardiaca", "dpoc", "hipotensao tep", "cid i26"
        ],
        "calc_spesi": [
            "spesi", "pesi simplificado", "simplified pesi", "tep ambulatorial", "alta precoce",
            "baixo risco tep", "mortalidade 30 dias", "idade 80", "cancer", "icc dpoc",
            "fc 110", "pas 100", "spo2 90", "anticoagulante oral", "desospitalizacao"
        ],
        "calc_glasgow_p": [
            "glasgow", "glasgow-p", "glasgow p", "ecg-p", "ecgp", "escala de coma de glasgow",
            "reatividade pupilar", "pupilas", "fotomotor", "anisocoria", "midriase", "trauma",
            "tce", "traumatismo cranioencefalico", "neurotrauma", "rebaixamento do nivel de consciencia",
            "coma", "intubacao orotraqueal", "iot", "sequencia rapida", "etomidato", "succinilcolina",
            "rocuronio", "neuroprotecao", "hipertensao intracraniana", "pic", "atls", "cid r40.2"
        ],
        "calc_four": [
            "four", "four score", "escala four", "full outline of unresponsiveness", "coma uti",
            "coma intubado", "paciente intubado", "reflexos de tronco", "drive respiratorio",
            "locked in", "sindrome do cativeiro", "morte encefalica", "triagem de morte encefalica",
            "fotomotor corneano tosse", "cheyne stokes", "apneia", "neurologia uti", "wijdicks",
            "tronco encefalico", "reflexos de tronco encefalico"
        ],
        "calc_rass": [
            "rass", "richmond agitation sedation scale", "escala de rass", "sedacao uti",
            "sedacao consciente", "agitacao psicomotora", "delirium hiperativo", "combativo",
            "fentanil", "midazolam", "propofol", "dexmedetomidina", "precedex", "metas de sedacao",
            "despertar diario", "ventilacao mecanica", "padis guidelines", "amib"
        ],
        "calc_sas": [
            "sas", "riker", "escala de riker", "sedation agitation scale", "sedacao riker",
            "agitacao perigosa", "calmo e cooperativo", "muito sedado", "nao despertavel",
            "avaliacao comportamental", "enfermagem uti", "titulacao de sedativo"
        ],
        "calc_cam_icu": [
            "cam icu", "cam-icu", "confusion assessment method", "delirium uti", "delirium",
            "confusao mental aguda", "desorientacao", "inatencao", "teste das letras",
            "saveahaart", "pensamento desorganizado", "curso flutuante", "alucinacao",
            "haloperidol", "quetiapina", "haldol", "prevencao delirium", "pacote abcdef"
        ],
        "calc_ranson": [
            "ranson", "criterios de ranson", "pancreatite aguda", "pancreatite", "dor abdominal",
            "amilase lipase", "admissao 48 horas", "pancreatite biliar", "pancreatite alcoolica",
            "leucocitose", "glicemia", "ldh", "ast tgo", "queda de hematocrito", "deficit de base",
            "sequestro hidrico", "calcio serico", "hipocalcemia", "necrose pancreatica", "cid k85"
        ],
        "calc_bisap": [
            "bisap", "escore bisap", "pancreatite", "pancreatite aguda", "triagem precoce pancreatite",
            "primeiras 24 horas", "bun", "ureia", "ureia 53", "sirs pancreatite",
            "derrame pleural", "glasgow pancreatite", "idade 60", "falencia organica",
            "mortalidade pancreatite", "ringer lactato", "hidratacao venosa", "cid k85"
        ],
        "calc_balthazar_ctsi": [
            "balthazar", "escore de balthazar", "ctsi", "computed tomography severity index",
            "indice de gravidade por tomografia", "tomografia pancreatite", "necrose pancreatica",
            "colecao peripancreatica", "gas peripancreatico", "balthazar e", "necrose 30 50",
            "pancreatite necrotizante", "step up approach", "drenagem percutanea", "necrosectomia"
        ],
        "calc_marshall_mod": [
            "marshall", "marshall modificado", "falencia organica pancreatite", "classificacao de atlanta",
            "atlanta revisada", "falencia transitoria", "falencia persistente", "pancreatite grave",
            "respiratorio paafi", "renal creatinina", "cardiovascular hipotensao", "choque pancreatite"
        ],

        # Block 03 Tools (18 Neuro Tools)
        "calc_rotterdam": [
            "rotterdam", "escore de rotterdam", "tce", "traumatismo cranioencefalico", "tomografia tce",
            "neurotrauma", "cisternas da base", "desvio de linha media", "hemorragia epidural",
            "hsa traumatica", "hiv traumatica", "mortalidade 6 meses", "hic refrataria", "craniectomia",
            "salina 3", "manitol", "noradrenalina", "cid s06"
        ],
        "calc_marshall": [
            "marshall", "classificacao de marshall", "marshall tce", "lesao difusa", "lesao em massa",
            "efeito de massa", "hematoma epidural", "hematoma subdural", "desvio linha media",
            "cisternas comprimidas", "tce grave", "neurocirurgia trauma", "evacuacao cirurgica", "cid s06.9"
        ],
        "calc_asia_ais": [
            "asia", "ais", "escala asia", "isncsci", "trm", "trauma raquimedular", "lesao medular",
            "nivel neurologico", "miotomos", "dermatomos", "chave sacral", "toque retal",
            "contracao anal voluntaria", "sensibilidade anal profunda", "choque medular", "pam 85 90",
            "tetraplegia", "paraplegia", "cid s14.1", "cid s24.1",
            "mielopatia", "mielopatia traumatica", "mielopatia compressiva"
        ],
        "calc_hunt_hess": [
            "hunt hess", "hunt-hess", "escala de hunt hess", "hsa", "hemorragia subaracnoidea",
            "aneurisma cerebral", "aneurisma roto", "cefaleia em trovoada", "thunderclap",
            "rigidez de nuca", "meningismo", "coma aneurismatico", "clipagem", "embolizacao",
            "nimodipino", "cid i60"
        ],
        "calc_wfns": [
            "wfns", "world federation of neurosurgical societies", "escala wfns", "hsa aneurismatica",
            "glasgow hsa", "deficit motor focal", "hemiparesia", "sangramento subaracnoideo",
            "prognostico neurocirurgico", "espessamento liquorio", "vasoespasmo cerebral"
        ],
        "calc_fisher_classic": [
            "fisher", "escala de fisher", "fisher classico", "fisher hsa", "vasoespasmo",
            "isquemia cerebral tardia", "dci", "sangue subaracnoideo tc", "coagulo subaracnoideo",
            "hemorragia intraventricular", "angiotc cerebral", "doppler transcraniano", "cid i60.9"
        ],
        "calc_fisher_modified": [
            "fisher modificado", "claassen", "escala de claassen", "escala de fisher modificada",
            "hsa espessa", "hiv bilateral", "vasoespasmo tardio", "predicao vasoespasmo",
            "dilatacao ventricular", "dve", "tomografia hsa"
        ],
        "calc_spetzler_martin": [
            "spetzler martin", "spetzler-martin", "mav", "malformacao arteriovenosa", "cirurgia mav",
            "ressecabilidade cirurgica", "cortex eloquente", "drenagem venosa profunda",
            "tamanho da mav", "nidus", "embolizacao mav", "radiocirurgia", "risco cirurgico neuro"
        ],
        "calc_nihss": [
            "nihss", "nih", "national institutes of health stroke scale", "avc", "avc isquêmico",
            "avc isquemico", "avci", "stroke", "trombólise", "trombolise", "alteplase", "tenecteplase",
            "trombectomia mecanica", "oclusao de grande vaso", "lvo", "deficit neurologico", "afasia",
            "hemiplegia", "paresia facial", "extincao e desatencao", "janela terapeutica 4.5 horas",
            "cid i63", "cid i64",
            "tempo porta agulha", "porta agulha", "tempo porta-agulha",
            "infarto", "infarto cerebral", "infarto isquemico"
        ],
        "calc_aspects": [
            "aspects", "alberta stroke program early ct score", "tc avc", "tomografia avc",
            "isquemia precoce", "arteria cerebral media", "acm", "fita insular", "nucleo lenticular",
            "capsula interna", "caudado", "core isquemico", "grande core", "select2",
            "trombectomia aspects", "stroke window",
            "infarto", "infarto cerebral", "infarto de acm", "infarto maligno"
        ],
        "calc_ich_score": [
            "ich score", "ich", "hemorragia intracerebral", "hic espontanea", "avc hemorragico",
            "avch", "volume do hematoma", "formula abc 2", "hemorragia intraventricular",
            "sangramento infratentorial", "mortalidade 30 dias hic", "reversao de anticoagulacao",
            "complexo protrombinico", "ccp 4 fatores", "metas pressoricas pas 130 140", "cid i61"
        ],
        "calc_abcd2": [
            "abcd2", "abcd 2", "escore abcd2", "ait", "ataque isquemico transitorio", "tia",
            "risco de avc", "prevencao secundaria", "dupla antiagregacao", "dapt",
            "aas clopidogrel", "chance point", "estenose carotidea", "isquemia cerebral transitoria",
            "cid g45.9"
        ],
        "calc_mrs": [
            "mrs", "rankin", "rankin modificado", "modified rankin scale", "incapacidade funcional",
            "desfecho funcional avc", "autonomia avds", "good outcome", "morar sozinho",
            "dependencia fisica", "reabilitacao neuro", "pos avc", "cid z74"
        ],
        "calc_kps": [
            "kps", "karnofsky", "performance status", "escala de karnofsky", "neuro oncologia",
            "glioblastoma", "gbm", "tumor cerebral", "metastase encefalica", "protocolo de stupp",
            "temozolomida", "radioterapia 60 gy", "ecog", "cuidados paliativos", "cid c71"
        ],
        "calc_meem_mmse": [
            "meem", "mmse", "mini exame do estado mental", "folstein", "rastreio cognitivo",
            "demencia", "alzheimer", "perda de memoria", "orientacao temporal", "orientacao espacial",
            "escolaridade brucki", "bertolucci", "donepezila", "rivastigmina", "memantina",
            "cid f00", "cid f03", "cid g30"
        ],
        "calc_moca": [
            "moca", "montreal cognitive assessment", "comprometimento cognitivo leve", "ccl",
            "mci", "funcao executiva", "visuoespacial", "trilha b", "teste do relogio",
            "memoria de trabalho", "rastreio sensivel", "corte 26", "ajuste escolaridade 12 anos",
            "rastreio demencia inicial"
        ],
        "calc_hoehn_yahr": [
            "hoehn yahr", "hoehn e yahr", "h&y", "parkinson", "doenca de parkinson",
            "estadiamento parkinson", "pull test", "teste do puxao", "instabilidade postural",
            "tremor de repouso", "bradicinesia", "rigidez", "dbs", "estimulacao cerebral profunda",
            "levodopa", "prolopa", "pramipexol", "cid g20"
        ],
        "calc_edss": [
            "edss", "escala de kurtzke", "kurtzke", "esclerose multipla", "em", "desmielinizante",
            "surto de esclerose", "distancia de marcha", "metros de deambulação", "bengala",
            "pulsoterapia", "metilprednisolona", "ocrelizumabe", "natalizumabe", "dmt", "neda",
            "cid g35",
            "esclerose em placas", "esclerose de placas"
        ]
    }

    STARRED_DEFAULTS = {
        "calc_qsofa", "calc_sofa", "calc_wells_tep", "calc_glasgow_p", "calc_bisap",
        "calc_nihss", "calc_rotterdam", "calc_ich_score"
    }

    # -------------------------------------------------------------------------
    # 4. CONSTRUCT UNIFIED MANIFEST (37 Tools)
    # -------------------------------------------------------------------------
    all_calculators = block_01_calculators + block_03_calculators
    manifest_items = []
    for calc in all_calculators:
        calc_id = calc["id"]
        synonyms = SYNONYMS_MAP.get(calc_id, [calc["acronym"].lower(), calc["name"].lower()])
        is_starred = calc_id in STARRED_DEFAULTS
        item = build_manifest_item(calc, synonyms, is_starred)
        manifest_items.append(item)

    print(f"Total manifest items compiled: {len(manifest_items)}")
    assert len(manifest_items) == 37, f"Expected 37 items in manifest, got {len(manifest_items)}"

    # -------------------------------------------------------------------------
    # 5. WRITE JSON ARTIFACTS
    # -------------------------------------------------------------------------
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    block_01_path = os.path.join(base_dir, "src", "data", "blocks", "block_01.json")
    block_03_path = os.path.join(base_dir, "src", "data", "blocks", "block_03.json")
    manifest_path = os.path.join(base_dir, "src", "data", "manifest.json")

    os.makedirs(os.path.dirname(block_01_path), exist_ok=True)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    # Write block_01.json
    with open(block_01_path, "w", encoding="utf-8") as f:
        json.dump(block_01_data, f, indent=2, ensure_ascii=False)
    block_01_size = os.path.getsize(block_01_path)
    print(f"Generated: {block_01_path} ({block_01_size:,} bytes, {block_01_size / 1024:.1f} KB)")

    # Write block_03.json
    with open(block_03_path, "w", encoding="utf-8") as f:
        json.dump(block_03_data, f, indent=2, ensure_ascii=False)
    block_03_size = os.path.getsize(block_03_path)
    print(f"Generated: {block_03_path} ({block_03_size:,} bytes, {block_03_size / 1024:.1f} KB)")

    # Write manifest.json
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_items, f, indent=2, ensure_ascii=False)
    manifest_size = os.path.getsize(manifest_path)
    print(f"Generated: {manifest_path} ({manifest_size:,} bytes, {manifest_size / 1024:.1f} KB)")

    print("Build completed successfully with 100% schema integrity.")

if __name__ == "__main__":
    main()
