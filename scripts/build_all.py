#!/usr/bin/env python3
"""
Assemble Block 01 JSON and Manifest JSON for Scoreboard App.
Outputs:
- src/data/blocks/block_01.json
- src/data/manifest.json (~30KB)
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

def build_manifest_item(calc, search_synonyms, starred_default=False):
    return {
        "id": calc["id"],
        "slug": calc["slug"],
        "name": calc["name"],
        "acronym": calc["acronym"],
        "category": calc.get("category", "Emergência, Choque e Terapia Intensiva"),
        "subcategory": calc.get("subcategory", calc["moduleName"]),
        "categorySlug": calc["categorySlug"],
        "categoryName": calc["categoryName"],
        "moduleName": calc["moduleName"],
        "description": calc.get("description", calc["summary"]),
        "summary": calc["summary"],
        "synonyms": search_synonyms,
        "searchSynonyms": search_synonyms,
        "calculationType": calc["calculationType"],
        "blockId": "block_01",
        "blockFile": "block_01.json",
        "evidenceSource": calc["evidenceSource"],
        "badge": calc.get("badge", "emergencia"),
        "hasInfusionProtocol": bool(calc.get("riskTiers", [{}])[-1].get("infusionProtocol") or calc.get("hasInfusionProtocol")),
        "starredDefault": starred_default
    }

def main():
    calculators = [
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

    print(f"Total calculators compiled: {len(calculators)}")
    assert len(calculators) == 19, f"Expected 19 calculators, got {len(calculators)}"

    # Construct Block 01
    block_01_data = {
        "blockId": "block_01",
        "blockName": "Emergência, Choque e Terapia Intensiva",
        "version": "1.0.0",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "description": "Dossiês monográficos completos dos 19 escores de emergência, choque e terapia intensiva com preservação estrita de parâmetros, estratificações de risco, condutas farmacológicas e protocolos de BIC.",
        "calculators": calculators
    }

    # Rich clinical synonyms dictionary for Brazilian physicians
    SYNONYMS_MAP = {
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
            "fotomotor corneano tosse", "cheyne stokes", "apneia", "neurologia uti", "wijdicks"
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
        ]
    }

    STARRED_DEFAULTS = {"calc_qsofa", "calc_sofa", "calc_wells_tep", "calc_glasgow_p", "calc_bisap"}

    # Construct Manifest
    manifest_items = []
    for calc in calculators:
        calc_id = calc["id"]
        synonyms = SYNONYMS_MAP.get(calc_id, [calc["acronym"].lower(), calc["name"].lower()])
        is_starred = calc_id in STARRED_DEFAULTS
        item = build_manifest_item(calc, synonyms, is_starred)
        manifest_items.append(item)

    # Output paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    block_01_path = os.path.join(base_dir, "src", "data", "blocks", "block_01.json")
    manifest_path = os.path.join(base_dir, "src", "data", "manifest.json")

    os.makedirs(os.path.dirname(block_01_path), exist_ok=True)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    # Write block_01.json
    with open(block_01_path, "w", encoding="utf-8") as f:
        json.dump(block_01_data, f, indent=2, ensure_ascii=False)
    block_01_size = os.path.getsize(block_01_path)
    print(f"Generated: {block_01_path} ({block_01_size:,} bytes, {block_01_size / 1024:.1f} KB)")

    # Write manifest.json
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_items, f, indent=2, ensure_ascii=False)
    manifest_size = os.path.getsize(manifest_path)
    print(f"Generated: {manifest_path} ({manifest_size:,} bytes, {manifest_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
