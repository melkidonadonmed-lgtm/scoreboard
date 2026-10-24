#!/usr/bin/env python3
"""
Assemble Blocks 01 through 09 JSONs and Unified Manifest JSON for Scoreboard App.
Outputs:
- src/data/blocks/block_01.json (19 calculators)
- src/data/blocks/block_02.json (12 calculators)
- src/data/blocks/block_03.json (39 calculators)
- src/data/blocks/block_04.json (8 calculators)
- src/data/blocks/block_05.json (11 calculators)
- src/data/blocks/block_06.json (7 calculators)
- src/data/blocks/block_07.json (7 calculators)
- src/data/blocks/block_08.json (8 calculators)
- src/data/blocks/block_09.json (3 calculators)
- src/data/manifest.json (114 lightweight index items)
"""

import json
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculators.common import enrich_and_normalize_calculator
from calculators.mod1_sepsis import get_qsofa, get_sofa, get_apache_ii, get_saps_3
from calculators.mod2_vte import get_wells_tep, get_wells_tvp, get_geneva, get_perc, get_pesi, get_spesi
from calculators.mod3_coma import get_glasgow_p, get_four, get_rass, get_sas, get_cam_icu
from calculators.mod4_pancreatitis import get_ranson, get_bisap, get_balthazar_ctsi, get_marshall_mod
from calculators.mod8_neuro import get_block_03_calculators
from calculators.block02_cardio import get_block_02_calculators, BLOCK_02_SYNONYMS
from calculators.block04_pneumo import get_block_04_calculators, BLOCK_04_SYNONYMS
from calculators.block05_surgery import get_block_05_calculators, BLOCK_05_SYNONYMS
from calculators.block06_nephro import get_block_06_calculators, BLOCK_06_SYNONYMS
from calculators.block07_hepato import get_block_07_calculators, BLOCK_07_SYNONYMS
from calculators.block08_pedia import get_block_08_calculators, BLOCK_08_SYNONYMS
from calculators.block09_hemato import get_block_09_calculators, BLOCK_09_SYNONYMS


def build_manifest_item(calc: dict, search_synonyms: list, starred_default: bool = False) -> dict:
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


def validate_calculator_structure(calc: dict) -> None:
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
    assert len(calc["radarAxes"]) >= 3, f"Calculator {calc['id']} must have at least 3 radarAxes"

    # Validate risk tiers
    for tier in calc["riskTiers"]:
        assert "id" in tier and "label" in tier and "severityLevel" in tier, f"Invalid tier in {calc['id']}: {tier}"
        assert "minScore" in tier and "maxScore" in tier, f"Tier missing minScore/maxScore in {calc['id']}: {tier}"
        assert "statisticalOutcome" in tier and "colorHex" in tier, f"Tier missing outcome/color in {calc['id']}: {tier}"


def main() -> None:
    # -------------------------------------------------------------------------
    # 1. COMPILE ALL 9 CLINICAL BLOCKS (114 Tools)
    # -------------------------------------------------------------------------
    block_01_calculators = [
        get_qsofa(), get_sofa(), get_apache_ii(), get_saps_3(),
        get_wells_tep(), get_wells_tvp(), get_geneva(), get_perc(), get_pesi(), get_spesi(),
        get_glasgow_p(), get_four(), get_rass(), get_sas(), get_cam_icu(),
        get_ranson(), get_bisap(), get_balthazar_ctsi(), get_marshall_mod()
    ]
    for calc in block_01_calculators:
        calc["blockId"] = "block_01"
        calc["blockFile"] = "block_01.json"

    block_02_calculators = get_block_02_calculators()
    block_03_calculators = get_block_03_calculators()
    block_04_calculators = get_block_04_calculators()
    block_05_calculators = get_block_05_calculators()
    block_06_calculators = get_block_06_calculators()
    block_07_calculators = get_block_07_calculators()
    block_08_calculators = get_block_08_calculators()
    block_09_calculators = get_block_09_calculators()

    blocks_spec = [
        ("block_01", "Emergência, Choque e Terapia Intensiva", "bloco-01-emergencia-choque-uti",
         "Dossiês monográficos completos dos 19 escores de emergência, choque e terapia intensiva com preservação estrita de parâmetros, estratificações de risco, condutas farmacológicas e protocolos de BIC.",
         block_01_calculators, 19),
        ("block_02", "Cardiologia e Hemodinâmica", "bloco-02-cardiologia-hemodinamica",
         "Dossiês monográficos completos dos 12 escores de cardiologia, síndrome coronariana aguda, fibrilação atrial, insuficiência cardíaca e risco cardiovascular perioperatório.",
         block_02_calculators, 12),
        ("block_03", "Neurologia e Neurocirurgia", "bloco-03-neurologia-neurocirurgia",
         "Dossiês monográficos completos dos 39 escores clínicos e cirúrgicos de neurologia, neurocirurgia e neurotrauma com parâmetros exaustivos, estratificações prognósticas, condutas farmacológicas rigorosas e diretrizes de intervenção.",
         block_03_calculators, 39),
        ("block_04", "Pneumologia e Vias Aéreas", "bloco-04-pneumologia-vias-aereas",
         "Dossiês monográficos completos dos 8 escores de pneumologia, pneumonia adquirida na comunidade (CURB-65, PSI/PORT, SMART-COP), DPOC GOLD ABE (BODE, mMRC, CAT) e avaliação de via aérea difícil.",
         block_04_calculators, 8),
        ("block_05", "Cirurgia Geral, Trauma e Queimados", "bloco-05-cirurgia-trauma-queimados",
         "Dossiês monográficos completos dos 11 escores de cirurgia de emergência, apendicite aguda, trauma multissistêmico, transfusão maciça, ressuscitação hídrica em queimados (ABA 2 mL vs Parkland 4 mL) e risco tromboembólico cirúrgico.",
         block_05_calculators, 11),
        ("block_06", "Nefrologia e Distúrbios Hidroeletrolíticos", "bloco-06-nefrologia-dhe",
         "Dossiês monográficos completos dos 7 escores e equações de nefrologia (CKD-EPI 2021 sem raça, Cockcroft-Gault, KDIGO LRA, FENa/FEUreia) e distúrbios hidroeletrolíticos e ácido-básicos (Adrogué-Madias, Anion Gap, Sódio Corrigido).",
         block_06_calculators, 7),
        ("block_07", "Gastroenterologia e Hepatologia", "bloco-07-gastro-hepatologia",
         "Dossiês monográficos completos dos 7 escores de hepatologia (Child-Pugh, MELD-Na / MELD 3.0, Lille, Maddrey, CLIF-C ACLF) e hemorragia digestiva alta (Glasgow-Blatchford, Rockall).",
         block_07_calculators, 7),
        ("block_08", "Pediatria, Neonatologia e Obstetrícia", "bloco-08-pediatria-obstetricia",
         "Dossiês monográficos completos dos 8 escores de neonatologia (Apgar, Silverman-Anderson), emergência pediátrica (PEWS, Taussig, PRISM III, Holliday-Segar) e obstetrícia/ginecologia crítica (Bishop, SOFA Obstétrico / fullPIERS).",
         block_08_calculators, 8),
        ("block_09", "Hematologia, Oncologia e Toxicologia", "bloco-09-hemato-onco-toxico",
         "Dossiês monográficos completos dos 3 escores críticos de hematologia, oncologia e toxicologia (4Ts para Trombocitopenia Induzida por Heparina, MASCC para Neutropenia Febril e Nomograma de Rumack-Matthew / King's College para Intoxicação por Paracetamol).",
         block_09_calculators, 3),
    ]

    all_blocks_data = []
    all_calculators = []
    for block_id, block_name, cat_slug, desc, calcs, expected_len in blocks_spec:
        for calc in calcs:
            calc["blockId"] = block_id
            calc["blockFile"] = f"{block_id}.json"
            enrich_and_normalize_calculator(calc)
            validate_calculator_structure(calc)
        print(f"{block_id} calculators compiled: {len(calcs)}")
        assert len(calcs) == expected_len, f"Expected {expected_len} in {block_id}, got {len(calcs)}"
        all_blocks_data.append({
            "blockId": block_id,
            "blockName": block_name,
            "version": "1.0.0",
            "categorySlug": cat_slug,
            "description": desc,
            "calculators": calcs
        })
        all_calculators.extend(calcs)
    # -------------------------------------------------------------------------
    # 2. CLINICAL BRAZILIAN SYNONYMS MAP
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

        # Block 03 Tools (39 Neuro Tools)
        "calc_rotterdam": ["rotterdam", "escore de rotterdam", "tce", "traumatismo cranioencefalico", "tomografia tce", "neurotrauma", "cisternas da base", "desvio de linha media", "hemorragia epidural", "hsa traumatica", "hiv traumatica", "mortalidade 6 meses", "hic refrataria", "craniectomia", "salina 3", "manitol", "noradrenalina", "cid s06"],
        "calc_marshall": ["marshall", "classificacao de marshall", "marshall tce", "lesao difusa", "lesao em massa", "efeito de massa", "hematoma epidural", "hematoma subdural", "desvio linha media", "cisternas comprimidas", "tce grave", "neurocirurgia trauma", "evacuacao cirurgica", "cid s06.9"],
        "calc_asia_ais": ["asia", "ais", "escala asia", "isncsci", "trm", "trauma raquimedular", "lesao medular", "nivel neurologico", "miotomos", "dermatomos", "chave sacral", "toque retal", "contracao anal voluntaria", "sensibilidade anal profunda", "choque medular", "pam 85 90", "tetraplegia", "paraplegia", "cid s14.1", "cid s24.1", "mielopatia", "mielopatia traumatica", "mielopatia compressiva"],
        "calc_hunt_hess": ["hunt hess", "hunt-hess", "escala de hunt hess", "hsa", "hemorragia subaracnoidea", "aneurisma cerebral", "aneurisma roto", "cefaleia em trovoada", "thunderclap", "rigidez de nuca", "meningismo", "coma aneurismatico", "clipagem", "embolizacao", "nimodipino", "cid i60"],
        "calc_wfns": ["wfns", "world federation of neurosurgical societies", "escala wfns", "hsa aneurismatica", "glasgow hsa", "deficit motor focal", "hemiparesia", "sangramento subaracnoideo", "prognostico neurocirurgico", "espessamento liquorio", "vasoespasmo cerebral"],
        "calc_fisher_classic": ["fisher", "escala de fisher", "fisher classico", "fisher hsa", "vasoespasmo", "isquemia cerebral tardia", "dci", "sangue subaracnoideo tc", "coagulo subaracnoideo", "hemorragia intraventricular", "angiotc cerebral", "doppler transcraniano", "cid i60.9"],
        "calc_fisher_modified": ["fisher modificado", "claassen", "escala de claassen", "escala de fisher modificada", "hsa espessa", "hiv bilateral", "vasoespasmo tardio", "predicao vasoespasmo", "dilatacao ventricular", "dve", "tomografia hsa"],
        "calc_spetzler_martin": ["spetzler martin", "spetzler-martin", "mav", "malformacao arteriovenosa", "cirurgia mav", "ressecabilidade cirurgica", "cortex eloquente", "drenagem venosa profunda", "tamanho da mav", "nidus", "embolizacao mav", "radiocirurgia", "risco cirurgico neuro"],
        "calc_nihss": ["nihss", "nih", "national institutes of health stroke scale", "avc", "avc isquêmico", "avc isquemico", "avci", "stroke", "trombólise", "trombolise", "alteplase", "tenecteplase", "trombectomia mecanica", "oclusao de grande vaso", "lvo", "deficit neurologico", "afasia", "hemiplegia", "paresia facial", "extincao e desatencao", "janela terapeutica 4.5 horas", "cid i63", "cid i64", "tempo porta agulha", "porta agulha", "tempo porta-agulha", "infarto", "infarto cerebral", "infarto isquemico"],
        "calc_aspects": ["aspects", "alberta stroke program early ct score", "tc avc", "tomografia avc", "isquemia precoce", "arteria cerebral media", "acm", "fita insular", "nucleo lenticular", "capsula interna", "caudado", "core isquemico", "grande core", "select2", "trombectomia aspects", "stroke window", "infarto", "infarto cerebral", "infarto de acm", "infarto maligno"],
        "calc_ich_score": ["ich score", "ich", "hemorragia intracerebral", "hic espontanea", "avc hemorragico", "avch", "volume do hematoma", "formula abc 2", "hemorragia intraventricular", "sangramento infratentorial", "mortalidade 30 dias hic", "reversao de anticoagulacao", "complexo protrombinico", "ccp 4 fatores", "metas pressoricas pas 130 140", "cid i61"],
        "calc_abcd2": ["abcd2", "abcd 2", "escore abcd2", "ait", "ataque isquemico transitorio", "tia", "risco de avc", "prevencao secundaria", "dupla antiagregacao", "dapt", "aas clopidogrel", "chance point", "estenose carotidea", "isquemia cerebral transitoria", "cid g45.9"],
        "calc_mrs": ["mrs", "rankin", "rankin modificado", "modified rankin scale", "incapacidade funcional", "desfecho funcional avc", "autonomia avds", "good outcome", "morar sozinho", "dependencia fisica", "reabilitacao neuro", "pos avc", "cid z74"],
        "calc_kps": ["kps", "karnofsky", "performance status", "escala de karnofsky", "neuro oncologia", "glioblastoma", "gbm", "tumor cerebral", "metastase encefalica", "protocolo de stupp", "temozolomida", "radioterapia 60 gy", "ecog", "cuidados paliativos", "cid c71"],
        "calc_meem_mmse": ["meem", "mmse", "mini exame do estado mental", "folstein", "rastreio cognitivo", "demencia", "alzheimer", "perda de memoria", "orientacao temporal", "orientacao espacial", "escolaridade brucki", "bertolucci", "donepezila", "rivastigmina", "memantina", "cid f00", "cid f03", "cid g30"],
        "calc_moca": ["moca", "montreal cognitive assessment", "comprometimento cognitivo leve", "ccl", "mci", "funcao executiva", "visuoespacial", "trilha b", "teste do relogio", "memoria de trabalho", "rastreio sensivel", "corte 26", "ajuste escolaridade 12 anos", "rastreio demencia inicial"],
        "calc_hoehn_yahr": ["hoehn yahr", "hoehn e yahr", "h&y", "parkinson", "doenca de parkinson", "estadiamento parkinson", "pull test", "teste do puxao", "instabilidade postural", "tremor de repouso", "bradicinesia", "rigidez", "dbs", "estimulacao cerebral profunda", "levodopa", "prolopa", "pramipexol", "cid g20"],
        "calc_edss": ["edss", "escala de kurtzke", "kurtzke", "esclerose multipla", "em", "desmielinizante", "surto de esclerose", "distancia de marcha", "metros de deambulação", "bengala", "pulsoterapia", "metilprednisolona", "ocrelizumabe", "natalizumabe", "dmt", "neda", "cid g35", "esclerose em placas", "esclerose de placas"],
        "calc_edema": ["edema", "edema score", "edema cerebral", "avc maligno", "avci extenso", "acm maligno", "craniectomia descompressiva", "midline shift", "desvio de linha media", "cisternas apagadas", "herniacao uncal", "ong 2017", "avc isquemico grave", "infarto maligno", "cid i63"],
        "calc_crash_tbi": ["crash", "crash tbi", "mrc crash", "trauma cranioencefalico", "tce grave", "mortalidade 14 dias", "prognostico tce", "desfecho desfavoravel", "lancet 2008", "contusao hemorragica", "neurotrauma", "salina 3", "contraindicacao corticoide", "cid s06"],
        "calc_impact_tbi": ["impact", "impact tbi", "escore impact", "trauma craniano", "tce moderado grave", "mortalidade 6 meses", "steyerberg", "marshall tc", "hipoxemia", "hipotensao trauma", "glicemia tce", "hemoglobina", "traumatismo encefalico", "cid s06.9"],
        "calc_vasograde": ["vasograde", "escore vasograde", "vasoespasmo hsa", "isquemia cerebral tardia", "dci", "hemorragia subaracnoidea", "wfns fisher", "vasograde verde amarelo vermelho", "nimodipino", "doppler transcraniano", "cid i60"],
        "calc_lawton_young": ["lawton young", "lawton-young", "mav suplementar", "spetzler suplementado", "idade mav", "sangramento previo", "nidus difuso", "malformacao arteriovenosa", "ressecabilidade mav", "microcirurgia vascular", "risco cirurgico mav", "cid q28.2"],
        "calc_zabramski": ["zabramski", "cavernoma", "malformacao cavernosa", "angioma cavernoso", "t1 t2 gradiente eco", "swi ressonancia", "hemossiderina", "hemorragia cavernoma", "epilepsia cavernoma", "tipo 1 tipo 2 tipo 3 tipo 4", "popcorn lesion", "cid d18.0"],
        "calc_phases_score": ["phases", "phases score", "aneurisma incidental", "risco de ruptura aneurisma", "aneurisma nao roto", "populacao hipertensao", "tamanho do aneurisma", "arteria comunicante", "artéria basilar", "sangramento subaracnoideo previo", "greving 2014", "cid i67.1"],
        "calc_uiats": ["uiats", "unruptured intracranial aneurysm", "aneurisma nao roto decisao", "tratamento aneurisma", "conservador vs cirurgia", "clipagem embolizacao", "morbi-mortalidade", "expectativa de vida", "score uiats", "etminan 2015", "aneurisma cerebral", "cid i67.1"],
        "calc_cognard_borden": ["cognard", "borden", "fistula dural", "favd", "fistula arteriovenosa dural", "drenagem venosa cortical", "refluxo venoso cortical", "risco hemorragico favd", "zumbido pulsatil", "trombose de seio dural", "embolizacao transarterial", "cid i67.8"],
        "calc_tlics": ["tlics", "toracolombar", "trauma toracolombar", "fratura de coluna", "fratura toracolombar", "complexo ligamentar posterior", "plc", "burst fratura", "explosao", "deficit neurologico", "artrodese de coluna", "vacarro", "cirurgia de coluna", "cid s32.0"],
        "calc_slics": ["slics", "coluna cervical", "trauma cervical subaxial", "fratura cervical", "c3 c7", "facetas deslocadas", "subluxacao facetaria", "disco ligamentar", "lesao medular cervical", "cirurgia cervical", "descompressao anterior", "vacarro cervical", "cid s12.0", "cid s14.1"],
        "calc_anderson_dalonzo": ["anderson d'alonzo", "anderson dalonzo", "odontoide", "fratura do dente do odontoide", "processo odontoide", "c2 odontoide", "tipo i tipo ii tipo iii", "parafuso de odontoide", "halo veste", "artrodese c1 c2", "pseudoartrose odontoide", "trauma cervical alto", "cid s12.1"],
        "calc_sins": ["sins", "spine instability neoplastic score", "metastase na coluna", "instabilidade na coluna", "fratura patologica", "dor mecanica na coluna", "colapso vertebral", "lise vertebral", "cifoplastia", "artrodese percutanea", "estabilidade espinhal", "fisher 2010", "cid c79.5"],
        "calc_noms_bilsky": ["noms", "noms framework", "bilsky", "compressao medular metastatica", "escc", "neurologico oncologico mecanico sistemico", "escore de bilsky", "cirurgia de separacao", "separation surgery", "sbrt coluna", "metastase espinhal", "cirurgia minimamente invasiva", "cid c79.5"],
        "calc_sagittal_balance": ["balanco sagital", "balanço sagital", "alinhamento sagital", "incidencia pelvica", "inclinacao pelvica", "versao pelvica", "lordose lombar", "eixo vertical sagital", "sva", "pi ll mismatch", "deformidade de coluna", "cifose", "escoliose do adulto", "osteotomia pso", "cid m40.0"],
        "calc_mjoa_nurick": ["mjoa", "nurick", "mielopatia cervical espondilotica", "mielopatia cervical", "cervical spondylotic myelopathy", "compressao medular cervical", "clonus", "babinski", "sinal de hoffmann", "perda de destreza", "marcha espastica", "laminoplastia", "corpectomia", "cid m50.0"],
        "calc_knosp": ["knosp", "classificacao de knosp", "adenoma de hipofise", "macroadenoma", "seio cavernoso", "invasao seio cavernoso", "arteria carotida interna", "cirurgia transesfenoidal", "eets", "radiocirurgia hipofise", "prolactinoma", "apoplexia hipofisaria", "cid d35.2"],
        "calc_samii_koos": ["koos", "samii", "schwannoma vestibular", "neurinoma do acustico", "angulo pontocerebelar", "conduto auditivo interno", "nervo facial", "house-brackmann", "cirurgia retrosigmoidea", "fossa posterior", "hidrocefalia obstrutiva", "gamma knife schwannoma", "cid d33.3"],
        "calc_ds_gpa": ["ds-gpa", "ds gpa", "graded prognostic assessment", "metastase cerebral", "metastases encefalicas", "sobrevida metastase cerebral", "rpa classe", "radiocirurgia srs", "wbrt holocraniana", "kps oncologia", "lung molgpa", "cirurgia metastase", "cid c79.3"],
        "calc_kiefer": ["kiefer", "escala de kiefer", "hpn", "hidrocefalia de pressao normal", "triade de hakim adams", "apraxia de marcha", "incontinencia urinaria", "tap test", "puncao lombar evacuadora", "derivacao ventriculoperitoneal", "dvp valvula regulavel", "valvula programavel", "cid g91.2"],
        "calc_evans_desh": ["evans", "indice de evans", "desh", "sinais de desh", "hidrocefalia comunicante", "ventriculomegalia", "angulo corpo caloso", "colapso do vertex", "edema transependimario", "tap test hpn", "atrofia ex vacuo", "diagnostico hpn", "cid g91.2"],
    }

    for extra_map in (
        BLOCK_02_SYNONYMS, BLOCK_04_SYNONYMS, BLOCK_05_SYNONYMS,
        BLOCK_06_SYNONYMS, BLOCK_07_SYNONYMS, BLOCK_08_SYNONYMS, BLOCK_09_SYNONYMS
    ):
        SYNONYMS_MAP.update(extra_map)

    STARRED_DEFAULTS = {
        "calc_qsofa", "calc_sofa", "calc_wells_tep", "calc_glasgow_p", "calc_bisap",
        "calc_nihss", "calc_rotterdam", "calc_ich_score",
        "calc_heart", "calc_cha2ds2_vasc", "calc_curb65", "calc_ckd_epi_2021", "calc_meld_na", "calc_parkland_aba"
    }

    # -------------------------------------------------------------------------
    # 3. CONSTRUCT UNIFIED MANIFEST (114 Tools)
    # -------------------------------------------------------------------------
    manifest_items = []
    for calc in all_calculators:
        calc_id = calc["id"]
        synonyms = SYNONYMS_MAP.get(calc_id, [calc["acronym"].lower(), calc["name"].lower()])
        is_starred = calc_id in STARRED_DEFAULTS
        item = build_manifest_item(calc, synonyms, is_starred)
        manifest_items.append(item)

    print(f"Total manifest items compiled: {len(manifest_items)}")
    assert len(manifest_items) == 114, f"Expected 114 items in manifest, got {len(manifest_items)}"

    # -------------------------------------------------------------------------
    # 4. WRITE JSON ARTIFACTS
    # -------------------------------------------------------------------------
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    blocks_dir = os.path.join(base_dir, "src", "data", "blocks")
    manifest_path = os.path.join(base_dir, "src", "data", "manifest.json")

    os.makedirs(blocks_dir, exist_ok=True)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    for bdata in all_blocks_data:
        bpath = os.path.join(blocks_dir, f"{bdata['blockId']}.json")
        with open(bpath, "w", encoding="utf-8") as f:
            json.dump(bdata, f, indent=2, ensure_ascii=False)
        bsize = os.path.getsize(bpath)
        print(f"Generated: {bpath} ({bsize:,} bytes, {bsize / 1024:.1f} KB)")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_items, f, indent=2, ensure_ascii=False)
    manifest_size = os.path.getsize(manifest_path)
    print(f"Generated: {manifest_path} ({manifest_size:,} bytes, {manifest_size / 1024:.1f} KB)")

    print("Build completed successfully with 100% schema integrity across all 9 clinical blocks (114 tools).")


if __name__ == "__main__":
    main()
