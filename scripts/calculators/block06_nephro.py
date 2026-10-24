"""
Block 06: Nefrologia e Meio Interno (7 Calculadoras Monográficas)
1. calc_kdigo_lra (Critérios KDIGO / AKIN para Injúria Renal Aguda — LRA, Estágios 1, 2 e 3 + Urgências Dialíticas)
2. calc_rifle (Classificação RIFLE para Disfunção Renal Aguda: Risk, Injury, Failure, Loss, ESKD)
3. calc_ckd_epi_2021 (Equação CKD-EPI 2021 Sem Variável de Raça — TFGe e Estadiamento KDIGO G1-G5 / A1-A3)
4. calc_cockcroft_gault (Clearance de Creatinina por Cockcroft-Gault e Ajuste Renal de Antimicrobianos e Anticoagulantes)
5. calc_anion_gap (Ânion Gap Plasmático Corrigido pela Albumina & Relação Delta-Delta na Acidose Metabólica)
6. calc_free_water_deficit (Déficit de Água Livre na Hipernatremia e Taxa Segura <= 10 mEq/L em 24h)
7. calc_hyponatremia_adrogue (Correção de Hiponatremia Sintomática / Fórmula de Adrogué-Madias com NaCl 3% e teto <= 8 mEq/L/24h)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL


def _axis(axis_id: str, label: str, system: str, unit: str = "pts") -> dict:
    return {
        "id": axis_id,
        "label": label,
        "system": system,
        "unit": unit,
        "baselineValue": 0,
        "maxAxisValue": 1,
    }


def _opt(
    opt_id: str,
    label: str,
    pts: float,
    baseline: bool,
    radar: float,
    order: int,
    desc: str,
) -> dict:
    return {
        "id": opt_id,
        "label": label,
        "pointValue": pts,
        "isNormalBaseline": baseline,
        "radarNormalizedValue": radar,
        "sortOrder": order,
        "description": desc,
    }


def _grp(
    grp_id: str,
    name: str,
    slug: str,
    axis_id: str,
    order: int,
    help_text: str,
    options: list[dict],
) -> dict:
    return {
        "id": grp_id,
        "name": name,
        "slug": slug,
        "inputType": "single_choice",
        "radarAxisId": axis_id,
        "normalBaselineValue": 0,
        "maxAxisValue": 1,
        "sortOrder": order,
        "helpText": help_text,
        "options": options,
    }


def _rx(
    rx_id: str,
    drug: str,
    dosage: str,
    route: str,
    freq: str,
    dilution: str | None = None,
    renal: str | None = None,
    contra: str | None = None,
    infusion: dict | None = None,
) -> dict:
    d = {
        "id": rx_id,
        "drugName": drug,
        "dosage": dosage,
        "route": route,
        "frequency": freq,
    }
    if dilution:
        d["dilutionInstructions"] = dilution
    if renal:
        d["renalAdjustment"] = renal
    if contra:
        d["contraindications"] = contra
    if infusion:
        d["infusionProtocol"] = infusion
    return d


def _nonrx(
    nrx_id: str,
    title: str,
    disp: str,
    mon: str,
    proc: str | None = None,
    vent: str | None = None,
    vasc: str | None = None,
    lab: str | None = None,
) -> dict:
    d = {
        "id": nrx_id,
        "recommendationTitle": title,
        "dispositionTarget": disp,
        "monitoringPlan": mon,
    }
    if proc:
        d["interventionalProcedure"] = proc
    if vent:
        d["ventilatorySupport"] = vent
    if vasc:
        d["vascularAccess"] = vasc
    if lab:
        d["laboratoryPanel"] = lab
    return d


def _tier(
    tier_id: str,
    label: str,
    sev: str,
    min_s: float,
    max_s: float,
    outcome: str,
    color: str,
    rx_list: list[dict],
    nonrx_list: list[dict],
    infusion: dict | None = None,
) -> dict:
    d = {
        "id": tier_id,
        "label": label,
        "severityLevel": sev,
        "minScore": min_s,
        "maxScore": max_s,
        "statisticalOutcome": outcome,
        "colorHex": color,
        "pharmacologicalActions": rx_list,
        "nonPharmacologicalActions": nonrx_list,
    }
    if infusion:
        d["infusionProtocol"] = infusion
    return d


def get_kdigo_lra() -> dict:
    return {
        "id": "calc_kdigo_lra",
        "slug": "criterios-kdigo-akin-injuria-renal-aguda-lra",
        "name": "Critérios KDIGO / AKIN para Injúria Renal Aguda (LRA — Estágios 1, 2 e 3)",
        "acronym": "KDIGO LRA",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Injúria Renal Aguda e Terapia Renal Substitutiva",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Injúria Renal Aguda e Doença Renal Crônica",
        "description": "Padrão internacional KDIGO (Kidney Disease: Improving Global Outcomes) que unifica os sistemas RIFLE e AKIN para diagnóstico e estadiamento da Injúria Renal Aguda (Estágios 1, 2 e 3) pela cinética da Creatinina Sérica (48h / 7 dias) e Débito Urinário horário (mL/kg/h), integrando a triagem de Urgências Dialíticas imediatas (AEIOU: Acidose refratária, Eletrólitos/Hipercalemia, Intoxicação, Overload/EAP e Uremia).",
        "summary": "Estadiamento KDIGO 1, 2 e 3 de LRA (Creatinina e Diurese mL/kg/h) e indicação de Hemodiálise de Urgência (AEIOU).",
        "clinicalObjective": "Detectar precocemente a LRA, aplicar o pacote nefroprotetor KDIGO e indicar Terapia Renal Substitutiva (Hemodiálise Intermitente ou CRRT) nas urgências dialíticas.",
        "targetPopulation": "Pacientes hospitalizados em enfermaria, pronto-socorro ou UTI com queda da diurese, elevação de escórias nitrogenadas ou sepse/choque.",
        "calculationType": "additive_points",
        "formulaExpression": "Estágio Cinético da Creatinina (0-3) + Estágio de Oligoanúria (0-3) + Urgência Dialítica AEIOU (0 ou +6)",
        "evidenceSource": "KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney Int Suppl. 2012;2(1):1-138. Ensaios STARRT-AKI (NEJM 2020) e AKIKI.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "nefrologia",
        "clinicalWarning": "Prevalece sempre o pior critério atingido (Creatinina OU Débito Urinário). Diuréticos de alça (Furosemida) tratam apenas a sobrecarga hídrica/congestão e NÃO revertem a necrose tubular aguda nem devem postergar a diálise quando houver indicação de urgência (AEIOU).",
        "radarAxes": [
            _axis("axis_kdigo_cr", "Cinética da Creatinina Sérica", "Renal"),
            _axis("axis_kdigo_uo", "Débito Urinário (Oligoanúria)", "Hidroeletrolítico"),
            _axis("axis_kdigo_aeiou", "Urgência Dialítica (AEIOU)", "Metabólico"),
        ],
        "parameterGroups": [
            _grp("grp_kdigo_creat", "1. Critério de Creatinina Sérica (Elevação em 48h ou 7 dias vs Basal)", "creatinina-kdigo-lra", "axis_kdigo_cr", 1, "Definir LRA se aumento >= 0,3 mg/dL em 48h ou >= 1,5x o valor basal conhecido/presumido nos últimos 7 dias.", [
                _opt("opt_kd_cr_0", "Sem elevação aguda (< 0,3 mg/dL em 48h e < 1,5x o basal) (0 pts)", 0, True, 0.0, 1, "Função glomerular estável."),
                _opt("opt_kd_cr_1", "KDIGO Estágio 1 — Aumento >= 0,3 mg/dL em 48h OU 1,5 a 1,9x a creatinina basal (+1 pt)", 1, False, 0.35, 2, "Injúria renal aguda inicial; alta reversibilidade se corrigida hipovolemia e suspensos nefrotóxicos."),
                _opt("opt_kd_cr_2", "KDIGO Estágio 2 — Aumento de 2,0 a 2,9x a creatinina basal (+2 pts)", 2, False, 0.7, 3, "Queda > 50% da TFG basal; ajuste obrigatório de antimicrobianos e anticoagulantes."),
                _opt("opt_kd_cr_3", "KDIGO Estágio 3 — Aumento >= 3,0x o basal, Creatinina >= 4,0 mg/dL ou Início de TRS (+4 pts)", 4, False, 1.0, 4, "Falência renal aguda estabelecida (AKIN 3 / RIFLE-F)."),
            ]),
            _grp("grp_kdigo_urine", "2. Critério de Débito Urinário (Diurese Horária em mL/kg/h)", "diurese-kdigo-lra", "axis_kdigo_uo", 2, "Oligúria documentada (exige exclusão prévia de obstrução pós-renal / bexigoma).", [
                _opt("opt_kd_uo_0", "Diurese preservada (>= 0,5 mL/kg/h) (0 pts)", 0, True, 0.0, 1, "Fluxo urinário adequado."),
                _opt("opt_kd_uo_1", "KDIGO Estágio 1 — Diurese < 0,5 mL/kg/h por 6 a 12 horas (+1 pt)", 1, False, 0.35, 2, "Oligúria inicial (avaliar fluido-responsividade e Teste de Estresse com Furosemida se euvolêmico)."),
                _opt("opt_kd_uo_2", "KDIGO Estágio 2 — Diurese < 0,5 mL/kg/h por >= 12 horas (+2 pts)", 2, False, 0.7, 3, "Oligúria sustentada indicando lesão tubular estabelecida."),
                _opt("opt_kd_uo_3", "KDIGO Estágio 3 — Diurese < 0,3 mL/kg/h por >= 24h OU Anúria por >= 12 horas (+4 pts)", 4, False, 1.0, 4, "Oligoanúria grave (alto risco de sobrecarga hídrica e hipercalemia)."),
            ]),
            _grp("grp_kdigo_aeiou", "3. Critérios de Urgência Dialítica Imediata (Mnemônico AEIOU)", "urgencia-dialitica-aeiou", "axis_kdigo_aeiou", 3, "Presença de complicação ameaçadora à vida refratária a medidas clínicas conservadoras.", [
                _opt("opt_kd_ae_0", "Ausente — Sem urgência dialítica imediata (0 pts)", 0, True, 0.0, 1, "Passível de manejo conservador e vigilância intensiva (estratégia STARRT-AKI)."),
                _opt("opt_kd_ae_6", "Presente — Acidose pH < 7,15 refratária, Hipercalemia K+ > 6,5 mEq/L refratária, Intoxicação dialisável (Lítio/Metanol/Salicilato), EAP/Hipervolemia refratária a diurético ou Uremia franca (Encefalopatia/Pericardite) (+6 pts)", 6, False, 1.0, 2, "Indicação absoluta de Terapia Renal Substitutiva (Hemodiálise) de emergência."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_kd_norm", "Sem LRA Detectada / Risco Basal (0 pontos)", "low", 0, 0, "Função renal preservada. Manter euvolemia e evitar exposição desnecessária a contraste iodado ou AINEs.", "#10b981", [
                _rx("rx_kd_0", "Prevenção Primária de Nefrotoxicidade", "Preferir soluções cristaloides balanceadas (Ringer Lactato / Plasma-Lyte) em vez de SF 0,9% em grandes volumes", "IV", "Manutenção"),
            ], [
                _nonrx("nrx_kd_0", "Monitorização de Balanço Hídrico e Creatinina", "Enfermaria", "Evitar associação tripla nefrotóxica ('Triple Whammy': IECA/BRA + Diurético + AINE)."),
            ]),
            _tier("tier_kd_stg1", "KDIGO Estágio 1 — Injúria Renal Aguda Inicial (1 ponto)", "intermediate", 1, 1, "Aumento de 1,5-1,9x da creatinina ou >= 0,3 mg/dL em 48h, ou oligúria 6-12h. Mortalidade hospitalar ~10-15%.", "#f59e0b", [
                _rx("rx_kd_1", "Suspensão Imediata de Nefrotóxicos + Expansão Guiada se Hipovolemia", "Suspender AINEs, aminoglicosídeos, anfotericina B desoxicolato e IECA/BRA temporariamente; Ringer Lactato 250-500 mL IV se sinais de hipovolemia pré-renal", "IV", "Imediato"),
            ], [
                _nonrx("nrx_kd_1", "Pacote KDIGO Bundle: EAS, Fração de Excreção de Sódio (FENa / FEUreia) e USG de Rins e Vias Urinárias", "Enfermaria / Semi-Intensiva", "Afastar obstrução pós-renal com USG ou bladder scan; monitorar diurese a cada 6h e creatinina/eletrólitos a cada 12-24h."),
            ]),
            _tier("tier_kd_stg2_3", "KDIGO Estágio 2 a 3 Sem Urgência Dialítica Imediata (2 a 5 pontos)", "high", 2, 5, "Queda severa da TFG (Cr >= 2x a >= 3x ou >= 4,0 mg/dL). Alto risco de progressão para TRS e sobrecarga volêmica.", "#f97316", [
                _rx("rx_kd_23_fst", "Teste de Estresse com Furosemida (FST) / Manejo de Hipervolemia", "Em paciente euvolêmico/hipervolêmico: Furosemida 1,0 mg/kg IV em bolus (ou 1,5 mg/kg se uso prévio de diurético). Se diurese < 200 mL em 2 horas, prediz progressão para Estágio 3 e necessidade de diálise", "IV", "Dose teste / Regrada", "Restringir aporte de potássio e fósforo na dieta/soroterapia; ajustar doses de Vancomicina, Meropenem, Cefepime e Enoxaparina."),
            ], [
                _nonrx("nrx_kd_23", "Parecer da Nefrologia e Preparo Preventivo de Acesso Vascular (Evitar Subclávia e PICC)", "UTI / Semi-Intensiva", "Preservar veias periféricas e evitar punção de veia subclávia (risco de estenose central que inviabiliza fístula arteriovenosa futura). Monitorar K+, pH e balanço hídrico rigoroso."),
            ]),
            _tier("tier_kd_dialysis", "KDIGO Estágio 3 com Urgência Dialítica Imediata — AEIOU (>= 6 pontos)", "critical", 6, 12, "Risco iminente de parada cardíaca por hipercalemia, edema agudo de pulmão anúrico ou acidemia refratária.", "#ef4444", [
                _rx("rx_kd_dial_k", "Ponte Farmacológica Anti-Hipercalêmica e Tampão Alcalino (Enquanto Instala Cateter de Shilley)", "Se Hipercalemia com alteração de ECG: Gluconato de Cálcio 10% 10-20 mL IV em 5 min (estabiliza membrana) + Insulina Regular 10 UI em SG 50% 50 mL (ou SG 10% 250 mL) IV em 30 min + Fenoterol/Salbutamol inalatório 10-20 gotas. Se pH < 7,15: Bicarbonato de Sódio 8,4% 100 mL IV", "IV", "Emergência"),
                _rx("rx_kd_dial_dva", "Noradrenalina em BIC se Instabilidade Hemodinâmica (Indica CRRT / SLED)", "Noradrenalina 0,05 a 0,5 mcg/kg/min IV contínua para manter PAM >= 65-70 mmHg durante a terapia dialítica", "IV Central", "Contínua em BIC", None, None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_kd_dial", "Início Imediato de Terapia Renal Substitutiva (Hemodiálise Intermitente vs Contínua CRRT)", "UTI", "Passagem de cateter de duplo lúmen para hemodiálise (Shilley 12F) guiada por ultrassom (1ª escolha: Veia Jugular Interna Direita; 2ª escolha: Femoral; evitar Subclávia). Se paciente hemodinamicamente instável sob vasopressor ou com TCE/edema cerebral, indicar Hemodiálise Contínua (CVVHDF/CRRT) ou Estendida (SLED).", "Passagem de Cateter de Shilley (Jugular Direita) e Hemodiálise de Emergência."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_rifle() -> dict:
    return {
        "id": "calc_rifle",
        "slug": "classificacao-rifle-disfuncao-renal-aguda",
        "name": "Classificação RIFLE para Disfunção Renal Aguda (Risk, Injury, Failure, Loss, ESKD)",
        "acronym": "RIFLE",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Injúria Renal Aguda e Desfechos Renais de Longo Prazo",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Injúria Renal Aguda e Doença Renal Crônica",
        "description": "Classificação histórica e prognóstica do grupo ADQI (Acute Dialysis Quality Initiative) estruturada em 3 níveis crescentes de gravidade aguda — Risk (Risco), Injury (Lesão) e Failure (Falência) baseados na queda percentual da TFG, elevação da Creatinina e duração da oligúria — e 2 desfechos evolutivos temporais: Loss (Perda da função renal com necessidade de diálise > 4 semanas) e ESKD (Doença Renal Terminal > 3 meses).",
        "summary": "Classificação em 5 estágios (Risk, Injury, Failure, Loss > 4 sem, ESKD > 3 meses) por Creatinina/TFG e Diurese.",
        "clinicalObjective": "Correlacionar os estágios agudos (R, I, F) com os desfechos renais crônicos de dependência dialítica (Loss e ESKD).",
        "targetPopulation": "Pacientes críticos e hospitalizados com deterioração aguda ou subaguda da função renal.",
        "calculationType": "additive_points",
        "formulaExpression": "Máximo entre Critério Glomerular (Cr/TFG), Critério de Diurese e Tempo de Dependência de TRS (Loss/ESKD)",
        "evidenceSource": "Bellomo R, Ronco C, Kellum JA, Mehta RL, Palevsky P; Acute Dialysis Quality Initiative workgroup. Acute renal failure - definition, outcome measures, animal models, fluid therapy and information technology needs: the Second International Consensus Conference of the ADQI Group. Crit Care. 2004;8(4):R204-R212.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "nefrologia",
        "clinicalWarning": "Na classificação RIFLE, os estágios Loss (> 4 semanas em TRS) e ESKD (> 3 meses em TRS) definem a transição da Injúria Renal Aguda para Doença Renal Aguda (AKD) e Doença Renal Crônica Dialítica (DRC G5D).",
        "radarAxes": [
            _axis("axis_rifle_gfr", "Queda da TFG / Creatinina (R-I-F)", "Glomerular"),
            _axis("axis_rifle_uo", "Fluxo Urinário Horário", "Tubular"),
            _axis("axis_rifle_time", "Cronicidade / Dependência de TRS (L-E)", "Evolutivo"),
        ],
        "parameterGroups": [
            _grp("grp_rifle_cr", "1. Critério de Creatinina Sérica e Queda da TFG (Estágios R, I, F)", "creatinina-tfg-rifle", "axis_rifle_gfr", 1, "Elevação da creatinina sérica ou redução percentual da Taxa de Filtração Glomerular em até 7 dias.", [
                _opt("opt_rf_cr_0", "Normal — Creatinina < 1,5x o basal e queda da TFG <= 25% (0 pts)", 0, True, 0.0, 1, "Sem critério glomerular RIFLE."),
                _opt("opt_rf_cr_r", "RIFLE-R (Risk / Risco) — Creatinina 1,5x o basal OU queda da TFG > 25% (+1 pt)", 1, False, 0.35, 2, "Sensibilidade máxima para detecção precoce de insulto renal."),
                _opt("opt_rf_cr_i", "RIFLE-I (Injury / Lesão) — Creatinina 2,0x o basal OU queda da TFG > 50% (+2 pts)", 2, False, 0.7, 3, "Lesão parenquimatosa estabelecida."),
                _opt("opt_rf_cr_f", "RIFLE-F (Failure / Falência) — Creatinina 3,0x o basal, queda da TFG > 75% OU Cr >= 4,0 mg/dL (com subida aguda >= 0,5 mg/dL) (+3 pts)", 3, False, 1.0, 4, "Falência renal aguda severa."),
            ]),
            _grp("grp_rifle_uo", "2. Critério de Débito Urinário (Oligúria / Anúria)", "diurese-rifle", "axis_rifle_uo", 2, "Avaliação temporal do débito urinário em mL/kg/h.", [
                _opt("opt_rf_uo_0", "Diurese >= 0,5 mL/kg/h (0 pts)", 0, True, 0.0, 1, "Débito urinário preservado."),
                _opt("opt_rf_uo_r", "RIFLE-R (Risk) — Diurese < 0,5 mL/kg/h por >= 6 horas (+1 pt)", 1, False, 0.35, 2, "Oligúria de 6 horas."),
                _opt("opt_rf_uo_i", "RIFLE-I (Injury) — Diurese < 0,5 mL/kg/h por >= 12 horas (+2 pts)", 2, False, 0.7, 3, "Oligúria persistente por 12 horas."),
                _opt("opt_rf_uo_f", "RIFLE-F (Failure) — Diurese < 0,3 mL/kg/h por >= 24h OU Anúria por >= 12 horas (+3 pts)", 3, False, 1.0, 4, "Oligoanúria crítica."),
            ]),
            _grp("grp_rifle_outcome", "3. Desfecho Temporal de Dependência de Diálise (Loss e ESKD)", "desfecho-loss-eskd-rifle", "axis_rifle_time", 3, "Duração da perda completa da função renal exigindo Terapia Renal Substitutiva (TRS).", [
                _opt("opt_rf_out_0", "Fase Aguda (< 4 semanas de evolução ou sem necessidade de TRS) (0 pts)", 0, True, 0.0, 1, "Estratificado exclusivamente pelos critérios agudos R, I ou F."),
                _opt("opt_rf_out_l", "RIFLE-L (Loss / Perda) — Perda completa da função renal exigindo TRS por > 4 semanas (+4 pts)", 4, False, 0.85, 2, "Persistência de falência renal além de 28 dias; requer planejamento de acesso de longa permanência."),
                _opt("opt_rf_out_e", "RIFLE-E (ESKD / Doença Renal Terminal) — Dependência de TRS por > 3 meses (+5 pts)", 5, False, 1.0, 3, "Transição definitiva para Doença Renal Crônica estágio G5D."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_rifle_r", "RIFLE — Normal a Risk (Risco Renal Agudo — 0 a 1 ponto)", "low", 0, 1, "Alta reversibilidade se restaurada a pressão de perfusão renal (PAM >= 65 mmHg) e suspensos nefrotóxicos.", "#10b981", [
                _rx("rx_rf_r", "Otimização Volêmica com Cristaloide Balanceado e Suspensão de Nefrotóxicos", "Ringer Lactato guiado por parâmetros dinâmicos de fluido-responsividade; suspender AINEs e contrastes", "IV", "Imediato"),
            ], [
                _nonrx("nrx_rf_r", "Vigilância de Diurese 6/6h e Balanço Hídrico", "Enfermaria / Semi-Intensiva", "Repetir creatinina e eletrólitos em 24h."),
            ]),
            _tier("tier_rifle_i", "RIFLE-I — Injury (Lesão Renal Estabelecida — 2 a 3 pontos)", "intermediate", 2, 3, "Queda > 50% da TFG ou oligúria >= 12h. Risco significativo de sobrecarga volêmica e acidose metabólica.", "#f59e0b", [
                _rx("rx_rf_i", "Ajuste Renal de Fármacos e Controle de Congestão com Furosemida IV", "Furosemida 20-80 mg IV se hipervolemia; ajuste estrito de antimicrobianos pelo clearance estimado", "IV", "Regrada"),
            ], [
                _nonrx("nrx_rf_i", "Interconsulta com Nefrologia e Ultrassonografia Renal com Doppler", "Unidade Semi-Intensiva / UTI", "Afastar causas obstrutivas e glomerulares; evitar hiper-hidratação."),
            ]),
            _tier("tier_rifle_f", "RIFLE-F — Failure (Falência Renal Aguda — 4 a 6 pontos)", "high", 4, 6, "Queda > 75% da TFG, Cr >= 4 mg/dL ou anúria >= 12h. Alta mortalidade hospitalar em pacientes sépticos.", "#f97316", [
                _rx("rx_rf_f", "Manejo de Hipercalemia/Acidose e Indicação de Terapia Renal Substitutiva", "Bicarbonato de Sódio 8,4% se pH < 7,15-7,20 + Medidas hipocalemiantes + Preparo para Hemodiálise", "IV", "UTI"),
            ], [
                _nonrx("nrx_rf_f", "Início de Hemodiálise (Intermitente ou CRRT) Conforme Status Hemodinâmico", "UTI", "Implante de cateter de duplo lúmen guiado por USG em jugular interna direita."),
            ]),
            _tier("tier_rifle_le", "RIFLE-L / RIFLE-E — Loss (> 4 sem) ou ESKD (> 3 meses em Diálise — 7 a 10 pontos)", "critical", 7, 10, "Falência renal prolongada (> 4 semanas) ou irreversível (> 90 dias — DRC G5D).", "#ef4444", [
                _rx("rx_rf_le", "Manejo de DRC Dialítica (Quelantes de Fósforo, Alfaepoetina e Reposição de Ferro)", "Sevelâmer 800 mg VO às refeições + Alfaepoetina SC se Hb < 10 g/dL + Sacarato de Hidróxido Férrico IV", "VO / SC / IV", "Programa de Hemodiálise"),
            ], [
                _nonrx("nrx_rf_le", "Transição para Cateter Tunelizado (Permcath) ou Confecção de Fístula Arteriovenosa (FAV)", "Unidade de Diálise / Ambulatório de Nefrologia", "Substituir cateter temporário de Shilley por Permcath e encaminhar ao cirurgião vascular para mapeamento Doppler e confecção de FAV (radiocefálica ou braquiocefálica).", "Confecção de Fístula Arteriovenosa ou Implante de Permcath."),
            ]),
        ],
    }


def get_ckd_epi_2021() -> dict:
    return {
        "id": "calc_ckd_epi_2021",
        "slug": "equacao-ckd-epi-2021-sem-raca-tfge-kdigo",
        "name": "Equação CKD-EPI 2021 (Sem Variável de Raça) — TFGe e Matriz KDIGO G1–G5 / A1–A3",
        "acronym": "CKD-EPI 2021",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Função Glomerular e Estadiamento da Doença Renal Crônica",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Injúria Renal Aguda e Doença Renal Crônica",
        "description": "Equação padrão-ouro recomendada pela National Kidney Foundation (NKF), American Society of Nephrology (ASN), KDIGO 2024 e Sociedade Brasileira de Nefrologia (SBN) para estimativa da Taxa de Filtração Glomerular (TFGe em mL/min/1,73m²) SEM coeficiente de raça/cor (Inker et al., NEJM 2021), acoplada à matriz bidimensional de estadiamento KDIGO por categoria de TFG (G1 a G5) e relação Albumina/Creatinina urinária (A1 a A3).",
        "summary": "Cálculo da TFGe pela equação CKD-EPI 2021 sem variável de raça e estadiamento KDIGO G1-G5 / A1-A3.",
        "clinicalObjective": "Estadiar a Doença Renal Crônica sem viés racial, indicar nefroproteção modificadora de doença (IECA/BRA, iSGLT2 e Finerenona) e definir o momento de encaminhamento ao nefrologista (TFGe < 30 mL/min/1,73m² ou A3).",
        "targetPopulation": "Adultos (>= 18 anos) em avaliação ambulatorial ou hospitalar estável da função renal basal.",
        "calculationType": "additive_points",
        "formulaExpression": "TFGe = 142 × min(Cr/κ, 1)^α × max(Cr/κ, 1)^(-1,200) × 0,9938^Idade × (1,012 se Mulher) [κ=0,7 F / 0,9 M; α=-0,241 F / -0,302 M — SEM variável de raça]",
        "evidenceSource": "Inker LA, Eneanya ND, Coresh J, et al. New Creatinine- and Cystatin C-Based Equations to Estimate GFR without Race. N Engl J Med. 2021;385(19):1737-1749. KDIGO 2024 CKD Guideline.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "nefrologia",
        "clinicalWarning": "DIRETRIZ MANDATÓRIA (CKD-EPI 2021 / KDIGO 2024): A variável de raça negra foi definitivamente abolida do cálculo da TFGe por ser um construto social que atrasava o diagnóstico de DRC, a prescrição de iSGLT2 e a inscrição em lista de transplante renal. Em extremos de massa muscular (sarcopenia, amputados, cirróticos), associar dosagem de Cistatina C (equação CKD-EPI Cr-CysC 2021).",
        "radarAxes": [
            _axis("axis_ckd_gfr", "Estágio de Filtração Glomerular (G1-G5)", "Glomerular", "mL/min/1,73m²"),
            _axis("axis_ckd_acr", "Albuminúria / Lesão Podocitária (A1-A3)", "Endotelial", "mg/g"),
            _axis("axis_ckd_age", "Reserva Etária e Sexo Biológico (κ / α)", "Epidemiológico"),
        ],
        "parameterGroups": [
            _grp("grp_ckd_sex_age", "1. Parâmetros Constantes da Equação CKD-EPI 2021 Sem Raça (Sexo Biológico κ/α e Idade)", "sexo-idade-ckd-epi-2021", "axis_ckd_age", 1, "Mulher: κ = 0,7, α = -0,241, multiplicador = 1,012 | Homem: κ = 0,9, α = -0,302, multiplicador = 1,000 | Fator etário = 0,9938^Idade.", [
                _opt("opt_ckd_sa_yng", "Adulto < 60 anos (Fem κ=0,7/α=-0,241×1,012 | Masc κ=0,9/α=-0,302) — Sem perda senil (0 pts)", 0, True, 0.1, 1, "Aplica a equação CKD-EPI 2021 estritamente livre de variável racial."),
                _opt("opt_ckd_sa_old", "Idoso >= 60 anos (Fator 0,9938^Idade com declínio fisiológico ~0,8 mL/min/ano) (+1 pt)", 1, False, 0.5, 2, "Considerar menor reserva nefrônica diante de insultos hemodinâmicos ou contraste."),
            ]),
            _grp("grp_ckd_g_stage", "2. Categoria de TFGe Calculada pela CKD-EPI 2021 (Estágios KDIGO G1 a G5)", "estagio-tfge-kdigo-g1-g5", "axis_ckd_gfr", 2, "Classificação da Taxa de Filtração Glomerular estimada em mL/min/1,73m².", [
                _opt("opt_ckd_g1", "KDIGO G1 — TFGe >= 90 mL/min/1,73m² (Normal ou Elevada) (0 pts)", 0, True, 0.0, 1, "Sem DRC se ausência de albuminúria ou alteração estrutural renal por > 3 meses."),
                _opt("opt_ckd_g2", "KDIGO G2 — TFGe 60 a 89 mL/min/1,73m² (Redução Discreta) (+1 pt)", 1, False, 0.2, 2, "Investigar albuminúria se hipertenso ou diabético."),
                _opt("opt_ckd_g3a", "KDIGO G3a — TFGe 45 a 59 mL/min/1,73m² (Redução Leve a Moderada) (+2 pts)", 2, False, 0.45, 3, "DRC confirmada se persistente > 3 meses; iniciar iSGLT2 e ajustar metformina/antibióticos."),
                _opt("opt_ckd_g3b", "KDIGO G3b — TFGe 30 a 44 mL/min/1,73m² (Redução Moderada a Grave) (+4 pts)", 4, False, 0.7, 4, "Rastreio obrigatório de distúrbio mineral e ósseo (PTH, Fósforo, Cálcio, Vitamina D) e anemia renal."),
                _opt("opt_ckd_g4", "KDIGO G4 — TFGe 15 a 29 mL/min/1,73m² (Redução Severa — Pré-Diálise) (+6 pts)", 6, False, 0.9, 5, "Encaminhamento mandatório ao nefrologista, preservação de veias do membro não dominante para FAV e preparo para TRS/transplante."),
                _opt("opt_ckd_g5", "KDIGO G5 — TFGe < 15 mL/min/1,73m² (Falência Renal / Uremia) (+8 pts)", 8, False, 1.0, 6, "Estágio terminal: avaliação para início de Terapia Renal Substitutiva ou transplante renal preemptivo."),
            ]),
            _grp("grp_ckd_a_stage", "3. Categoria de Albuminúria Persistente — Relação Albumina/Creatinina em Amostra Isolada (RAC: A1 a A3)", "albuminuria-kdigo-a1-a3", "axis_ckd_acr", 3, "Marcador independente de progressão para falência renal e mortalidade cardiovascular.", [
                _opt("opt_ckd_a1", "KDIGO A1 — Normal a Levemente Aumentada (RAC < 30 mg/g ou < 3 mg/mmol) (0 pts)", 0, True, 0.0, 1, "Barreira de filtração glomerular íntegra."),
                _opt("opt_ckd_a2", "KDIGO A2 — Moderadamente Aumentada /Antiga Microalbuminúria (RAC 30 a 300 mg/g) (+1 pt)", 1, False, 0.5, 2, "Indicação formal de bloqueio do SRAA (IECA ou BRA) + Inibidor de SGLT2 (Dapagliflozina/Empagliflozina)."),
                _opt("opt_ckd_a3", "KDIGO A3 — Gravemente Aumentada / Macroalbuminúria (RAC > 300 mg/g) (+3 pts)", 3, False, 1.0, 3, "Altíssimo risco de perda acelerada de TFG e eventos cardiovasculares; meta pressórica PAS < 120-130 mmHg."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_ckd_green", "Risco Baixo KDIGO (G1–G2 com Albuminúria A1 — 0 a 1 ponto)", "low", 0, 1, "Sem Doença Renal Crônica (salvo lesão estrutural/policística). Baixo risco de progressão.", "#10b981", [
                _rx("rx_ckd_low", "Controle Pressórico (< 130/80 mmHg) e Glicêmico", "Cessação do tabagismo, restrição de sódio (< 2 g Na+ ou < 5 g NaCl/dia) e evitar uso crônico de AINEs", "VO", "Ambulatorial"),
            ], [
                _nonrx("nrx_ckd_low", "Rastreio Anual com Creatinina (CKD-EPI 2021) + RAC Urinária em Diabéticos e Hipertensos", "Atenção Primária / Ambulatório", "Monitoramento anual de grupos de risco."),
            ]),
            _tier("tier_ckd_yellow", "Risco Moderadamente Aumentado KDIGO (G3a-A1 ou G1/G2-A2 — 2 a 3 pontos)", "intermediate", 2, 3, "DRC inicial a moderada. Intervenção farmacológica precoce reduz em 30-40% o declínio da TFG.", "#f59e0b", [
                _rx("rx_ckd_mod_sglt2", "Duplo Pilar Nefroprotetor: IECA/BRA em Dose Máxima Tolerada + Inibidor de SGLT2", "Enalapril 10-20 mg 12/12h ou Losartana 50-100 mg/dia + Dapagliflozina 10 mg VO 1x/dia ou Empagliflozina 10 mg VO 1x/dia (em diabéticos e não diabéticos com RAC >= 200 mg/g ou TFGe >= 20)", "VO", "Uso contínuo", "Uma queda aguda funcional de até 25-30% na TFGe nas primeiras 2-4 semanas após início de IECA/BRA ou iSGLT2 é esperada (redução da hiperfiltração intraglomerular) e NÃO indica suspensão do fármaco."),
            ], [
                _nonrx("nrx_ckd_mod", "Monitoramento Semestral de TFGe, Potássio e Relação Albumina/Creatinina", "Ambulatório de Clínica Médica", "Associar Estatina para prevenção cardiovascular primária em pacientes >= 50 anos com DRC."),
            ]),
            _tier("tier_ckd_orange", "Alto Risco KDIGO (G3b ou G3a-A2/A3 — 4 a 5 pontos)", "high", 4, 5, "Elevado risco de progressão para diálise e eventos cardiovasculares maiores.", "#f97316", [
                _rx("rx_ckd_high", "Otimização Nefroprotetora (IECA/BRA + iSGLT2 + Finerenona se DM2 com Albuminúria Residual) e Ajuste de Metformina", "Reduzir dose máxima de Metformina para 1.000 mg/dia na faixa G3b (TFGe 30-44 mL/min); manter Dapagliflozina/Empagliflozina + Estatina + Finerenona 10-20 mg se DM2 com RAC >= 30 mg/g e K+ <= 4,8 mEq/L", "VO", "Diária"),
            ], [
                _nonrx("nrx_ckd_high", "Acompanhamento Conjunto com Nefrologia e Rastreio de Anemia/DMO-DRC", "Ambulatório de Nefrologia", "Solicitar Hemograma, Ferritina, Saturação de Transferrina, Cálcio, Fósforo, PTH intacto, 25-OH-Vitamina D e Gasometria Venosa (corrigir bicarbonato se < 22 mEq/L com Bicarbonato de Sódio VO)."),
            ]),
            _tier("tier_ckd_red", "Muito Alto Risco KDIGO — DRC Avançada G4–G5 ou Macroalbuminúria Grave (>= 6 pontos)", "critical", 6, 12, "Altíssimo risco de falência renal (G5) necessitando de TRS ou transplante renal em 1 a 2 anos.", "#ef4444", [
                _rx("rx_ckd_crit", "Suspensão de Metformina (se TFGe < 30), Controle de Acidose, Hipercalemia e Anemia Renal", "Suspender Metformina se TFGe < 30 mL/min; Bicarbonato de Sódio 500-1.000 mg VO 8/8h (meta HCO3 >= 22 mEq/L); Ciclossilicato de Zircônio/Patiromer se hipercalemia; Alfaepoetina e Ferro IV se anemia", "VO / SC", "Multidisciplinar", "Nota KDIGO 2024: iSGLT2 iniciados previamente podem ser mantidos mesmo quando a TFGe cair abaixo de 20 mL/min até o início da diálise."),
            ], [
                _nonrx("nrx_ckd_crit", "Cuidado Nefrológico Pré-Diálise, Vacinação para Hepatite B (Esquema Dobrado) e Confecção Precoce de FAV", "Ambulatório Pré-Diálise / Transplante Renal", "PROIBIDO puncionar veias do membro superior não dominante (proteger rede cefálica/basílica para Fístula Arteriovenosa). Encaminhar para confecção de FAV quando TFGe < 15-20 mL/min ou inscrição em transplante preemptivo quando TFGe < 20 mL/min."),
            ]),
        ],
    }


def get_cockcroft_gault() -> dict:
    return {
        "id": "calc_cockcroft_gault",
        "slug": "clearance-creatinina-cockcroft-gault-ajuste-antimicrobianos",
        "name": "Clearance de Creatinina (Cockcroft-Gault) & Ajuste Renal de Fármacos (Enoxaparina, DOACs, Antibióticos)",
        "acronym": "Cockcroft-Gault",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Farmacocinética Clínica e Segurança de Prescrição",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Injúria Renal Aguda e Doença Renal Crônica",
        "description": "Equação clássica de estimativa do Clearance de Creatinina (ClCr em mL/min não indexado por superfície corporal: [(140 - Idade) × Peso] / [72 × Cr] × 0,85 se mulher), que permanece como referência regulatória oficial de bula (FDA / ANVISA / Sanford Guide) para o ajuste posológico de anticoagulantes (Enoxaparina, Rivaroxabana, Apixabana, Dabigatrana, Edoxabana) e antimicrobianos hidrofílicos de eliminação renal (Vancomicina, Meropenem, Cefepime, Piperacilina-Tazobactam, Aciclovir).",
        "summary": "Clearance de Creatinina (mL/min) por Cockcroft-Gault com tabela completa de ajuste renal de anticoagulantes e antibióticos.",
        "clinicalObjective": "Prevenir sangramento maior por acúmulo de Enoxaparina/DOACs e neurotoxicidade/nefrotoxicidade por superdosagem de Cefepime, Meropenem, Vancomicina e Aciclovir.",
        "targetPopulation": "Pacientes adultos recebendo fármacos de índice terapêutico estreito ou excreção predominantemente renal.",
        "calculationType": "additive_points",
        "formulaExpression": "ClCr (mL/min) = [(140 - Idade) × Peso (kg)] / [72 × Creatinina (mg/dL)] × (0,85 se Sexo Feminino)",
        "evidenceSource": "Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. Nephron. 1976;16(1):31-41. Sanford Guide to Antimicrobial Therapy 2024/2025.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "farmacocinetica",
        "clinicalWarning": "ALERTA DE SEGURANÇA (ANVISA / FDA): (1) O ajuste de DOACs nos ensaios ROCKET-AF, ARISTOTLE, RE-LY e ENGAGE AF foi validado exclusivamente pela fórmula de Cockcroft-Gault usando o Peso Corporal Real. (2) Em obesos mórbidos (IMC >= 30-40 kg/m²), utilizar o Peso Corporal Ajustado: P_ajust = P_ideal + 0,4 × (P_real - P_ideal) para evitar superestimar o ClCr. (3) Cefepime sem ajuste renal em ClCr < 30-50 mL/min causa Estado de Mal Epiléptico Não Convulsivo (NCSE) e mioclonias.",
        "radarAxes": [
            _axis("axis_cg_clcr", "Faixa de Clearance (ClCr mL/min)", "Renal", "mL/min"),
            _axis("axis_cg_antithromb", "Risco de Acúmulo de Anticoagulantes", "Hematológico"),
            _axis("axis_cg_abx", "Ajuste de Antimicrobianos (PK/PD)", "Infeccioso"),
        ],
        "parameterGroups": [
            _grp("grp_cg_weight_rule", "1. Critério Antropométrico e Sexo Biológico na Fórmula de Cockcroft-Gault", "peso-sexo-cockcroft-gault", "axis_cg_clcr", 1, "Multiplicador 0,85 no sexo feminino; uso de Peso Ideal ou Ajustado [PI + 0,4×(PR - PI)] em obesos.", [
                _opt("opt_cg_wt_std", "Eutrófico (Peso Real) — Homem (×1,0) ou Mulher (×0,85) (0 pts)", 0, True, 0.1, 1, "Fórmula direta: [(140 - Idade) × Peso] / (72 × Cr) [× 0,85 se mulher]."),
                _opt("opt_cg_wt_adj", "Idoso Sarcopênico / Baixo Peso (< 50 kg) ou Obeso usando Peso Ajustado (+1 pt)", 1, False, 0.5, 2, "Atenção: em idosos com Cr falsamente 'normal' (0,8-1,0 mg/dL) e peso < 50 kg, o ClCr real frequentemente já é < 35-40 mL/min!"),
            ]),
            _grp("grp_cg_clcr_range", "2. Faixa de Clearance de Creatinina Calculado (ClCr em mL/min)", "faixa-clcr-cockcroft-gault", "axis_cg_clcr", 2, "Estrato de depuração renal para ajuste de bulas antimicrobianas e antitrombóticas.", [
                _opt("opt_cg_cl_gt50", "ClCr > 50 mL/min — Depuração Renal Preservada / Redução Discreta (0 pts)", 0, True, 0.0, 1, "Doses plenas habituais da maioria dos antimicrobianos e anticoagulantes."),
                _opt("opt_cg_cl_30_50", "ClCr 30 a 50 mL/min — Insuficiência Renal Moderada (+2 pts)", 2, False, 0.5, 2, "Exige ajuste de Meropenem, Cefepime, Piperacilina-Tazobactam (se < 40), Rivaroxabana e Edoxabana."),
                _opt("opt_cg_cl_15_29", "ClCr 15 a 29 mL/min — Insuficiência Renal Grave (+5 pts)", 5, False, 0.85, 3, "Contraindica Dabigatrana; exige redução de Enoxaparina (1 mg/kg 24/24h na plena; 20-30 mg na profilática) e ajuste severo de beta-lactâmicos."),
                _opt("opt_cg_cl_lt15", "ClCr < 15 mL/min ou Paciente em Hemodiálise (TRS) (+8 pts)", 8, False, 1.0, 4, "Contraindica DOACs (preferir HNF ou Varfarina) e exige administração pós-hemodiálise de antimicrobianos dialisáveis."),
            ]),
            _grp("grp_cg_drug_class", "3. Classe Terapêutica Alvo na Prescrição Atual", "classe-farmaco-cockcroft", "axis_cg_antithromb", 3, "Risco farmacocinético específico da prescrição em curso.", [
                _opt("opt_cg_drg_abx", "Antimicrobianos Beta-Lactâmicos (Meropenem, Cefepime, Pip-Tazo) (0 pts)", 0, True, 0.2, 1, "Manter DOSE DE ATAQUE plena na 1ª dose na sepse (volume de distribuição elevado) e ajustar apenas a manutenção a partir da 2ª dose!"),
                _opt("opt_cg_drg_vanco", "Glicopeptídeos / Polimixinas / Aminoglicosídeos (Vancomicina, Amicacina) (+1 pt)", 1, False, 0.65, 2, "Fármacos diretamente nefrotóxicos: monitorar vancocinemia (AUC/MIC 400-600 ou vale 15-20 mcg/mL)."),
                _opt("opt_cg_drg_anticoag", "Anticoagulantes Plenos ou Profiláticos (Enoxaparina, Rivaroxabana, Apixabana, Dabigatrana) (+1 pt)", 1, False, 0.8, 3, "Alto risco de sangramento maior retroperitoneal ou intracraniano se não ajustados para ClCr < 30 mL/min."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_cg_norm", "ClCr > 50 mL/min — Doses Plenas Padrão (0 a 1 ponto)", "low", 0, 1, "Depuração renal suficiente para posologia habitual sem risco de bioacumulação.", "#10b981", [
                _rx("rx_cg_50_ant", "Posologia Plena de Anticoagulantes (ClCr > 50 mL/min)", "Enoxaparina plena: 1 mg/kg SC 12/12h (profilática: 40 mg SC 24/24h) | Rivaroxabana: 20 mg VO 1x/dia | Apixabana: 5 mg VO 12/12h | Dabigatrana: 150 mg VO 12/12h", "SC / VO", "Dose padrão"),
                _rx("rx_cg_50_abx", "Posologia Plena de Antimicrobianos (ClCr > 50 mL/min)", "Meropenem 1 g IV 8/8h (2 g 8/8h em meningite/choque) | Cefepime 2 g IV 8/8h | Piperacilina-Tazobactam 4,5 g IV 6/6h | Vancomicina ataque 25-30 mg/kg + 15-20 mg/kg 12/12h", "IV", "Dose padrão"),
            ], [
                _nonrx("nrx_cg_50", "Reavaliação Diária do ClCr em Pacientes Críticos", "Enfermaria / UTI", "Atenção à hiperfiltração renal aumentada (ARC: ClCr > 130 mL/min em jovens politraumatizados/queimados), que exige infusão estendida de beta-lactâmicos (3-4h)."),
            ]),
            _tier("tier_cg_mod", "ClCr 30 a 50 mL/min — Ajuste Renal Moderado Obrigatório (2 a 4 pontos)", "intermediate", 2, 4, "Redução moderada da depuração. Necessário ajuste de manutenção de beta-lactâmicos e DOACs.", "#f59e0b", [
                _rx("rx_cg_30_50_abx", "Ajuste de Antimicrobianos para ClCr 30–50 mL/min (Após 1ª Dose de Ataque Plena!)", "Meropenem: 1 g IV de 12/12h (ClCr 26-50) | Cefepime: 2 g IV de 12/12h | Piperacilina-Tazobactam: 4,5 g IV 6/6h (se ClCr 20-40: 2,25 g 6/6h ou 4,5 g 8/8h) | Vancomicina: ataque 25 mg/kg + 15 mg/kg 24/24h guiado por nível sérico", "IV", "Manutenção ajustada"),
                _rx("rx_cg_30_50_ac", "Ajuste de Anticoagulantes para ClCr 30–50 mL/min", "Enoxaparina: sem ajuste (manter 1 mg/kg 12/12h plena e 40 mg/dia profilática) | Rivaroxabana (FA): reduzir para 15 mg VO 1x/dia com alimento | Edoxabana: 30 mg VO 1x/dia | Dabigatrana: considerar 110 mg 12/12h | Apixabana: 5 mg 12/12h (reduzir para 2,5 mg 12/12h apenas se >= 2 critérios ABC: Idade >= 80 anos, Peso <= 60 kg, Cr >= 1,5 mg/dL)", "SC / VO", "Posologia ajustada"),
            ], [
                _nonrx("nrx_cg_30_50", "Monitorar Neurotoxicidade por Cefepime e Nível Sérico de Vancomicina", "Enfermaria / UTI", "Dosar vancocinemia antes da 3ª ou 4ª dose."),
            ]),
            _tier("tier_cg_sev", "ClCr 15 a 29 mL/min — Ajuste Renal Grave e Restrição de Enoxaparina/DOACs (5 a 7 pontos)", "high", 5, 7, "Alto risco de sangramento grave com Enoxaparina em dose padrão e encefalopatia por Cefepime.", "#f97316", [
                _rx("rx_cg_15_29_ac", "Ajuste Crítico de Anticoagulantes (ClCr 15–29 mL/min)", "Enoxaparina TERAPÊUTICA: reduzir para 1 mg/kg SC 1x/dia (24/24h)! Enoxaparina PROFILÁTICA: 20 mg (ou 30 mg) SC 1x/dia (ou substituir por HNF 5.000 UI SC 8/8h ou 12/12h). Dabigatrana: CONTRAINDICADA (ClCr < 30). Apixabana: 2,5 mg VO 12/12h com cautela", "SC / VO", "Dose reduzida de segurança"),
                _rx("rx_cg_15_29_abx", "Ajuste de Antimicrobianos (ClCr 10–25 mL/min)", "Meropenem: 500 mg IV de 12/12h | Cefepime: 1 g IV de 12/12h (ou 2 g 24/24h) | Piperacilina-Tazobactam: 2,25 g IV de 8/8h | Vancomicina: dose de ataque 20-25 mg/kg e redosar apenas conforme vancocinemia", "IV", "Ajuste estrito"),
            ], [
                _nonrx("nrx_cg_15_29", "Dosagem de Fator Anti-Xa se Uso Prolongado de Enoxaparina", "Unidade Semi-Intensiva / UTI", "Preferir Heparina Não Fracionada (HNF) se ClCr < 20 mL/min ou instabilidade renal aguda."),
            ]),
            _tier("tier_cg_esrd", "ClCr < 15 mL/min ou Hemodiálise — Posologia Dialítica e Contraindicação a HBPM/DOACs (8 a 10 pontos)", "critical", 8, 10, "Excreção renal mínima. Fármacos dialisáveis devem ser administrados SEMPRE APÓS a sessão de hemodiálise.", "#ef4444", [
                _rx("rx_cg_hd_ac", "Anticoagulação Segura na Falência Renal / Diálise (ClCr < 15 mL/min)", "Anticoagulação Plena: Heparina Não Fracionada (HNF) IV em BIC guiada por TTPa (1,5-2,5x) com transição para Varfarina (INR 2,0-3,0). Profilaxia de TEV: HNF 5.000 UI SC de 8/8h ou 12/12h (Evitar Enoxaparina e Fondaparinux)", "IV / SC / VO", "Guiado por TTPa / INR"),
                _rx("rx_cg_hd_abx", "Posologia em Hemodiálise Intermitente (Administrar APÓS a Diálise)", "Meropenem: 500 mg IV a cada 24h (após HD nos dias de sessão) | Cefepime: 1 g IV a cada 24h (após HD) | Piperacilina-Tazobactam: 2,25 g IV de 12/12h (+ dose suplementar de 0,75 g após HD) | Vancomicina: ataque 20-25 mg/kg + 500-1.000 mg após cada sessão guiado por nível pré-diálise", "IV", "Pós-Hemodiálise"),
            ], [
                _nonrx("nrx_cg_hd", "Revisão Farmacêutica Diária em UTI (Atenção especial à CRRT: Doses Maiores que na HD Intermitente!)", "UTI / Unidade de Diálise", "ATENÇÃO: Pacientes em Hemodiálise Contínua (CVVHDF/CRRT com efluente 25-35 mL/kg/h) depuram intensamente beta-lactâmicos, exigindo doses equivalentes a ClCr 30-50 mL/min (ex.: Meropenem 1 g 8/8h ou 12/12h) para evitar subdosagem séptica!"),
            ]),
        ],
    }


def get_anion_gap() -> dict:
    return {
        "id": "calc_anion_gap",
        "slug": "anion-gap-corrigido-albumina-relacao-delta-delta",
        "name": "Ânion Gap Corrigido pela Albumina (Figge) & Relação Delta-Delta na Acidose Metabólica",
        "acronym": "Ânion Gap / Δ-Δ",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Distúrbios Ácido-Base e Gasometria Arterial",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Distúrbios Hidroeletrolíticos e Ácido-Base",
        "description": "Sistema diagnóstico integrado para avaliação de acidose metabólica: calcula o Ânion Gap clássico [Na+ - (Cl- + HCO3-)], aplica a Correção de Figge para Hipoalbuminemia [AG_corr = AG + 2,5 × (4,0 - Albumina g/dL)], diferencia acidose normoclorêmica (AG > 12 — GOLD MARK: Glicóis, Oxoprolina, L-lactato, D-lactato, Metanol, Aspirina, Renal/Uremia, Ketoacidosis) de hiperclorêmica (AG 8-12 — perdas digestivas/ATR/SF 0,9%) e avalia distúrbios mistos ocultos pela Relação Delta-Delta [ΔAG / ΔHCO3 = (AG_corr - 12) / (24 - HCO3-)].",
        "summary": "Ânion Gap corrigido pela albumina (Figge) e Relação Delta-Delta (ΔAG/ΔHCO3) para distúrbios ácido-base mistos.",
        "clinicalObjective": "Revelar acidose de ânion gap elevado mascarada por hipoalbuminemia em pacientes críticos e identificar alcalose metabólica ou acidose hiperclorêmica associadas via Delta-Delta.",
        "targetPopulation": "Pacientes em UTI, sala de emergência ou enfermaria com acidose metabólica (pH < 7,35 e HCO3- < 22 mEq/L) ou choque/cetoacidose.",
        "calculationType": "additive_points",
        "formulaExpression": "AG_corr = [Na+ - (Cl- + HCO3-)] + 2,5 × (4,0 - Albumina) | Relação Δ/Δ = (AG_corr - 12) / (24 - HCO3-)",
        "evidenceSource": "Figge J, Jabor A, Kazda A, Fencl V. Anion gap and hypoalbuminemia. Crit Care Med. 1998;26(11):1807-1810; Berend K, de Vries AP, Gans RO. Physiological approach to assessment of acid-base disturbances. N Engl J Med. 2014;371(15):1434-1445.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "gasometria",
        "clinicalWarning": "REGRA DE FIGGE: Cada queda de 1,0 g/dL na Albumina sérica abaixo de 4,0 g/dL reduz o Ânion Gap basal em 2,5 mEq/L. Em pacientes sépticos hipoalbuminêmicos (ex.: Albumina = 1,6 g/dL), um AG 'aparentemente normal' de 10 mEq/L corresponde na verdade a um AG Corrigido = 16 mEq/L (Acidose de AG Elevado oculta!). Verificar sempre a compensação respiratória pela Fórmula de Winter: PaCO2 esperada = (1,5 × HCO3-) + 8 ± 2.",
        "radarAxes": [
            _axis("axis_ag_val", "Ânion Gap Corrigido (Figge)", "Metabólico", "mEq/L"),
            _axis("axis_ag_alb", "Impacto da Hipoalbuminemia", "Bioquímico", "g/dL"),
            _axis("axis_ag_delta", "Relação Delta-Delta (ΔAG / ΔHCO3)", "Gasométrico"),
        ],
        "parameterGroups": [
            _grp("grp_ag_albumin", "1. Correção de Figge pela Albumina Sérica [2,5 × (4,0 - Albumina g/dL)]", "albumina-figge-anion-gap", "axis_ag_alb", 1, "A albumina é o principal ânion não mensurado fisiológico do plasma.", [
                _opt("opt_ag_alb_norm", "Normoalbuminemia (Albumina >= 3,5 a 4,0 g/dL — Correção +0 a +1,2 mEq/L) (0 pts)", 0, True, 0.0, 1, "Ânion Gap medido reflete fielmente os ácidos orgânicos circulantes."),
                _opt("opt_ag_alb_mod", "Hipoalbuminemia Moderada (Albumina 2,5 a 3,4 g/dL — Somar +1,5 a +3,75 mEq/L ao AG) (+1 pt)", 1, False, 0.5, 2, "Sem correção de Figge, subestima o Ânion Gap real em ~3 mEq/L."),
                _opt("opt_ag_alb_sev", "Hipoalbuminemia Grave de UTI/Cirrose/Nefrótico (Albumina < 2,5 g/dL — Somar +4,0 a +6,0 mEq/L ao AG) (+2 pts)", 2, False, 1.0, 3, "Obrigatória a aplicação da fórmula de Figge para não perder acidose lática ou cetoacidose."),
            ]),
            _grp("grp_ag_corrected", "2. Valor do Ânion Gap Corrigido [Na+ - (Cl- + HCO3-) + 2,5×(4 - Alb)]", "valor-anion-gap-corrigido", "axis_ag_val", 2, "Faixa fisiológica de referência: 8 a 12 mEq/L.", [
                _opt("opt_ag_val_norm", "Ânion Gap Normal (8 a 12 mEq/L) — Acidose Metabólica Hiperclorêmica (se HCO3- < 22) (0 pts)", 0, True, 0.2, 1, "Causas: Diarreia aguda, fístula pancreática/biliar, infusão maciça de SF 0,9% ou Acidose Tubular Renal (ATR I, II, IV)."),
                _opt("opt_ag_val_high", "Ânion Gap Moderadamente Elevado (13 a 20 mEq/L) — Acidose Normoclorêmica (+3 pts)", 3, False, 0.65, 2, "Investigar GOLD MARK: Acidose Lática (sepse/hipoperfusão), Cetoacidose (diabética, alcoólica, jejum) ou Uremia (LRA/DRC)."),
                _opt("opt_ag_val_crit", "Ânion Gap Muito Elevado (> 20 mEq/L) — Acidose Orgânica Severa / Intoxicação (+6 pts)", 6, False, 1.0, 3, "VPP > 95% para acidose orgânica grave: Cetoacidose Diabética, Choque Lático ou Intoxicação Exógena (Metanol, Etilenoglicol, Salicilatos)."),
            ]),
            _grp("grp_ag_deltadelta", "3. Relação Delta-Delta [ΔAG / ΔHCO3 = (AG_corr - 12) / (24 - HCO3-)]", "relacao-delta-delta", "axis_ag_delta", 3, "Compara o excesso de ânions (ΔAG) com o consumo de bicarbonato (ΔHCO3).", [
                _opt("opt_ag_dd_pure", "Relação Δ/Δ entre 1,0 e 2,0 — Acidose Metabólica de Ânion Gap Elevado PURA (0 pts)", 0, True, 0.2, 1, "Na acidose lática a relação típica é ~1,6; na cetoacidose pura ~1,0 (devido à perda urinária de cetoânions)."),
                _opt("opt_ag_dd_low", "Relação Δ/Δ < 1,0 (ou < 0,8) — Distúrbio Duplo: Acidose de AG Elevado + Acidose Hiperclorêmica associada (+2 pts)", 2, False, 0.75, 2, "Queda de HCO3- maior que a subida do AG (ex.: Cetoacidose reidratada com muito SF 0,9%, ou Choque Séptico + Diarreia/ATR)."),
                _opt("opt_ag_dd_high", "Relação Δ/Δ > 2,0 — Distúrbio Duplo: Acidose de AG Elevado + Alcalose Metabólica coexistente (ou Retenção Crônica de CO2) (+4 pts)", 4, False, 1.0, 3, "HCO3- está mais alto que o esperado para o AG (ex.: Cetoacidose/Acidose Lática em paciente com vômitos incoercíveis, SNG aberta, uso de furosemida ou DPOC retentor crônico)."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_ag_hyperchl", "Acidose Metabólica de Ânion Gap Normal / Hiperclorêmica (0 a 2 pontos)", "low", 0, 2, "Consumo de bicarbonato compensado estequiometricamente por retenção de Cloreto (Cl-). Calcular Ânion Gap Urinário se causa incerta.", "#10b981", [
                _rx("rx_ag_norm", "Suspensão de SF 0,9% e Reposição de Bicarbonato (na Perda Digestiva ou ATR)", "Substituir SF 0,9% por Ringer Lactato; se diarreia intensa ou ATR com HCO3- < 15-18 mEq/L: Bicarbonato de Sódio VO ou IV isotônico (150 mL de NaHCO3 8,4% em 850 mL de SG 5%)", "IV / VO", "Guiado por gasometria"),
            ], [
                _nonrx("nrx_ag_norm", "Cálculo do Ânion Gap Urinário [AG_u = (Na_u + K_u) - Cl_u]", "Enfermaria / Observação", "Se AG urinário NEGATIVO (-20 a -50 mEq/L): excreção renal de NH4+ preservada -> Perda Gastrointestinal (Diarreia) ou uso de SF 0,9%. Se AG urinário POSITIVO: falha na acidificação renal -> Acidose Tubular Renal (ATR)."),
            ]),
            _tier("tier_ag_hagma_mod", "Acidose de Ânion Gap Elevado Pura ou Mista Moderada (3 a 6 pontos)", "high", 3, 6, "Acúmulo de ácidos fixos não voláteis (Lactato, Cetoácidos ou Escórias Urêmicas). Tratar a causa base!", "#f59e0b", [
                _rx("rx_ag_mod", "Tratamento Dirigido à Etiologia (Insulina Regular na CAD / Ressuscitação na Acidose Lática)", "Na CAD: Hidratação + Insulina Regular 0,1 UI/kg/h IV (após K+ >= 3,3 mEq/L) até fechamento do Ânion Gap (<= 12 mEq/L). Na Acidose Lática: restaurar perfusão tecidual com Ringer Lactato e antibióticos", "IV", "Contínua", "Na Cetoacidose e Acidose Lática com pH >= 7,15, NÃO administrar Bicarbonato de Sódio de rotina (causa acidose paradoxal intracelular/SNC, hipocalemia e desvio da curva da hemoglobina)."),
            ], [
                _nonrx("nrx_ag_mod", "Solicitar Lactato Arterial, Cetonemia (Beta-Hidroxibutirato), Função Renal e Aplicar Fórmula de Winter", "Unidade Semi-Intensiva / Sala Vermelha", "Verificar compensação ventilatória: PaCO2 esperada = (1,5 × HCO3-) + 8 ± 2. Se PaCO2 real > esperada: Acidose Respiratória associada (fadiga muscular iminente!)."),
            ]),
            _tier("tier_ag_hagma_crit", "Acidose de Ânion Gap Muito Elevado (> 20 mEq/L) ou Distúrbio Triplo / Intoxicação por Álcoois Tóxicos (7 a 12 pontos)", "critical", 7, 12, "Risco iminente de colapso cardiovascular (refratariedade a catecolaminas quando pH < 7,10), arritmias ventriculares e coma.", "#ef4444", [
                _rx("rx_ag_crit_bic", "Bicarbonato de Sódio IV (Se pH < 7,15 com LRA KDIGO 2-3 — Ensaio BICAR-ICU, ou pH < 6,90 na CAD)", "Solução Isotônica de Bicarbonato: 150 mL de NaHCO3 8,4% (150 mEq) diluídos em 850 mL de SG 5% ou Água Destilada (infundir 250-500 mL em 1-2h visando pH > 7,20 e HCO3 > 12-15 mEq/L)", "IV", "Titulado por gasometria a cada 2h", "Se suspeita de intoxicação por Metanol ou Etilenoglicol (Gap Osmolar > 10 mOsm/kg): Fomepizol IV (ou Etanol absoluto) + Tiamina/Piridoxina/Ácido Folínico + Hemodiálise de Emergência!"),
            ], [
                _nonrx("nrx_ag_crit", "Cálculo do Gap Osmolar [Osm_medida - (2×Na + Glicose/18 + Ureia/6)] e UTI / Hemodiálise", "UTI", "Se paciente necessitar de Intubação Orotraqueal na acidose metabólica grave, manter hiperventilação compensatória no ventilador mecânico (FR 24-30 irpm) para evitar queda abrupta letal do pH pós-intubação!"),
            ]),
        ],
    }


def get_free_water_deficit() -> dict:
    return {
        "id": "calc_free_water_deficit",
        "slug": "deficit-agua-livre-hipernatremia-correcao-segura",
        "name": "Déficit de Água Livre na Hipernatremia & Taxa Segura de Redução do Sódio (<= 10 mEq/L/24h)",
        "acronym": "Déficit de Água Livre",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Distúrbios do Sódio e Tonicidade Plasmática",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Distúrbios Hidroeletrolíticos e Ácido-Base",
        "description": "Calculadora fisiológica do Déficit Corporal de Água Livre [ACT × ((Na_atual / 140) - 1)] e da variação de sódio por litro de solução hipotônica infundida pela Fórmula de Adrogué-Madias [(Na_infusão - Na_sérico) / (ACT + 1)], estruturando o plano de reposição com Água Potável Enteral, Soro Glicosado 5% (0 mEq/L) ou Salina Hipotônica NaCl 0,45% (77 mEq/L) respeitando a trava de segurança de redução máxima <= 10 mEq/L em 24 horas (<= 0,4 a 0,5 mEq/L/h) para prevenção de edema cerebral iatrogênico.",
        "summary": "Cálculo do Déficit de Água Livre [ACT × ((Na/140) - 1)] e prescrição segura de SG 5% ou NaCl 0,45% (queda <= 10 mEq/L/24h).",
        "clinicalObjective": "Corrigir o estado hiperosmolar da hipernatremia (Na+ > 145 mEq/L) somando o déficit de água livre às perdas insensíveis diárias (~1.000 mL/24h), sem provocar edema cerebral e herniação.",
        "targetPopulation": "Adultos e idosos com hipernatremia (Na+ > 145 mEq/L) por privação hídrica, perdas hipotônicas (diarreia, diurese osmótica) ou Diabetes Insipidus (central ou nefrogênico).",
        "calculationType": "additive_points",
        "formulaExpression": "Déficit de Água Livre (L) = ACT × [(Na_atual / 140) - 1] | ACT = Peso × (0,6 Homem; 0,5 Mulher/Idoso; 0,45 Idosa)",
        "evidenceSource": "Adrogué HJ, Madias NE. Hypernatremia. N Engl J Med. 2000;342(20):1493-1499; Sterns RH. Disorders of plasma sodium. N Engl J Med. 2015;372(1):55-65.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "eletrolitos",
        "clinicalWarning": "TRAVA DE SEGURANÇA NEUROLÓGICA: Na hipernatremia crônica (> 48h ou tempo indeterminado), os neurônios acumulam idiogênicos orgânicos (mio-inositol, taurina, glutamina). A redução rápida do sódio sérico (> 10 mEq/L em 24h ou > 0,5 mEq/L/h) provoca entrada osmótica maciça de água nos neurônios, causando EDEMA CEREBRAL, convulsões e morte. SE houver choque hipovolêmico concomitante, restaurar PRIMEIRO a volemia intravascular com Ringer Lactato ou SF 0,9% antes de iniciar soluções hipotônicas!",
        "radarAxes": [
            _axis("axis_fwd_na", "Gravidade da Hipernatremia (Na+)", "Osmolar", "mEq/L"),
            _axis("axis_fwd_tbw", "Água Corporal Total (ACT) e Volemia", "Hidroeletrolítico", "L"),
            _axis("axis_fwd_time", "Cronicidade e Poliúria (Diabetes Insipidus)", "Neuroendócrino"),
        ],
        "parameterGroups": [
            _grp("grp_fwd_tbw", "1. Fração de Água Corporal Total (ACT = Peso × Fator) e Status Hemodinâmico", "agua-corporal-total-hipernatremia", "axis_fwd_tbw", 1, "Fator de ACT: Homem jovem = 0,6 | Mulher jovem ou Homem idoso = 0,5 | Mulher idosa = 0,45.", [
                _opt("opt_fwd_tbw_euv", "Euvolêmico / Desidratação Intracelular Pura (ACT 0,5 a 0,6 × Peso) — Sem hipotensão (0 pts)", 0, True, 0.2, 1, "Indicado iniciar diretamente reposição de água livre enteral (SNE/VO) ou SG 5% IV."),
                _opt("opt_fwd_tbw_hypo", "Hipovolêmico Moderado (Taquicardia, mucosas secas, idoso ACT 0,45-0,5 × Peso) (+2 pts)", 2, False, 0.6, 2, "Preferir Salina ao Meio (NaCl 0,45% = 77 mEq/L) que repõe simultaneamente volume extracelular e 50% de água livre."),
                _opt("opt_fwd_tbw_shock", "Choque Hipovolêmico Franco (PAS < 90 mmHg, oligúria pré-renal) (+4 pts)", 4, False, 1.0, 3, "PRIORIDADE 1: Ressuscitar primeiro com Ringer Lactato ou SF 0,9% até estabilidade hemodinâmica; só então trocar para SG 5% / NaCl 0,45%."),
            ]),
            _grp("grp_fwd_sodium", "2. Nível de Sódio Sérico Atual e Déficit Estimado (Para Referência de 70 kg, ACT = 35 L)", "sodio-serico-hipernatremia", "axis_fwd_na", 2, "Déficit (L) = ACT × [(Na_atual / 140) - 1]. Acrescentar sempre +1.000 a 1.500 mL/24h de perdas insensíveis obrigatórias.", [
                _opt("opt_fwd_na_mild", "Hipernatremia Leve: Na+ 146 a 150 mEq/L (Déficit ~1,5 a 2,5 L para ACT 35 L) (+1 pt)", 1, True, 0.3, 1, "Correção em 24h com água livre via oral/SNE (200 mL de 4/4h) ou SG 5% ~100-120 mL/h."),
                _opt("opt_fwd_na_mod", "Hipernatremia Moderada: Na+ 151 a 159 mEq/L (Déficit ~2,8 a 4,8 L para ACT 35 L) (+3 pts)", 3, False, 0.65, 2, "Corrigir o déficit em 48 horas (reduzir no máximo 8 a 10 mEq/L a cada 24h) + perdas insensíveis."),
                _opt("opt_fwd_na_sev", "Hipernatremia Grave: Na+ >= 160 mEq/L (Déficit >= 5,0 a 8,5 L para ACT 35 L; Sonolência/Coma) (+5 pts)", 5, False, 1.0, 3, "Emergência hiperosmolar: corrigir ao longo de 48 a 72 horas (meta estrita: queda <= 8 a 10 mEq/L por dia; dosar Na+ a cada 4h)."),
            ]),
            _grp("grp_fwd_etiology", "3. Tempo de Instalação e Etiologia (Perda Extrarrenal vs Diabetes Insipidus / TCE / Lítio)", "etiologia-diabetes-insipidus", "axis_fwd_time", 3, "Diferenciar hipodipsia/perda digestiva (urina concentrada > 600 mOsm/kg) de Diabetes Insipidus (poliúria > 3 L/dia com urina diluída < 300 mOsm/kg).", [
                _opt("opt_fwd_et_chronic", "Hipernatremia Crônica (> 48h ou duração desconhecida) por hipodipsia, febre ou perda digestiva (0 pts)", 0, True, 0.2, 1, "Teto rigoroso de redução: máximo de 8 a 10 mEq/L em 24h (<= 0,4 mEq/L/h)."),
                _opt("opt_fwd_et_acute", "Hipernatremia Hiperaguda (< 24h: intoxicação iatrogênica por NaHCO3 / NaCl 3%) (+1 pt)", 1, False, 0.6, 2, "Permite redução inicial mais rápida (1 mEq/L/h até normalização) pois o cérebro ainda não acumulou osmóis orgânicos."),
                _opt("opt_fwd_et_di", "Diabetes Insipidus Central (TCE, Neurocirurgia, Morte Encefálica) ou Nefrogênico (Lítio) com Poliúria > 4 mL/kg/h (+3 pts)", 3, False, 1.0, 3, "Exige reposição horária mL a mL da diurese + Desmopressina (DDAVP) no Diabetes Insipidus Central."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_fwd_mild", "Hipernatremia Leve a Moderada Sem Choque (Na+ 146–154 mEq/L — 1 a 3 pontos)", "low", 0, 3, "Déficit de água livre moderado (1,5 a 3,5 L). Via enteral (VO ou SNE) é a mais segura e fisiológica.", "#10b981", [
                _rx("rx_fwd_mild", "Água Potável por Via Oral / SNE ou Soro Glicosado 5% IV", "Água filtrada via SNE 150 a 250 mL a cada 3-4h OU Soro Glicosado 5% (SG 5%) IV a 100-150 mL/h (calculando: 50% do déficit nas primeiras 24h + 1.000 mL de perdas insensíveis)", "VO / SNE / IV", "Contínua / Fracionada", "Como Preparar Salina 0,45% (77 mEq/L) na falta de bolsa pronta: diluir 500 mL de SF 0,9% + 500 mL de Água Destilada (ou diluir 20 mL de NaCl 20% em 980 mL de Água Destilada/SG 5%)."),
            ], [
                _nonrx("nrx_fwd_mild", "Controle de Sódio e Glicemia Capilar a cada 6 a 12 horas", "Enfermaria", "Atenção: infusões rápidas de SG 5% (> 250 mL/h) podem causar hiperglicemia com glicosúria e diurese osmótica, agravando paradoxalmente a perda de água livre!"),
            ]),
            _tier("tier_fwd_mod", "Hipernatremia Moderada a Grave Crônica (Na+ 155–165 mEq/L — 4 a 7 pontos)", "high", 4, 7, "Alto risco de encefalopatia hipernatrêmica e risco de edema cerebral se reduzido > 10 mEq/L/24h.", "#f59e0b", [
                _rx("rx_fwd_mod", "Esquema Combinado: Água Livre por SNE + Salina 0,45% ou SG 5% em BIC", "Meta de queda: 8 a 10 mEq/L a cada 24h (~0,4 mEq/L/h). Pela fórmula de Adrogué-Madias, 1 litro de SG 5% reduz o Na+ em [-Na_atual / (ACT + 1)] (~4 mEq/L em adulto de 70 kg). Infundir ~130 a 180 mL/h combinando SNE + IV", "IV em BIC + SNE", "Contínua em BIC"),
            ], [
                _nonrx("nrx_fwd_mod", "Dosagem de Sódio Sérico a cada 4 a 6 horas e Balanço Hídrico Rigoroso", "Unidade Semi-Intensiva / UTI", "Se o sódio cair > 5 mEq/L em 6h (> 0,8 mEq/L/h), reduzir imediatamente a vazão de SG 5% pela metade."),
            ]),
            _tier("tier_fwd_crit", "Hipernatremia Crítica (Na+ > 165 mEq/L), Choque Hipovolêmico ou Diabetes Insipidus (8 a 12 pontos)", "critical", 8, 12, "Mortalidade hospitalar de 40% a 60% (hemorragia subaracnóidea por tração venosa, trombose de seio venoso ou choque).", "#ef4444", [
                _rx("rx_fwd_crit_vol", "1º Passo (Se Choque): Expansão com Ringer Lactato | 2º Passo: SG 5% / NaCl 0,45% Titulado", "Se hipotensão/choque: Ringer Lactato (Na+ 130 mEq/L) 20 mL/kg até restaurar PAM >= 65 mmHg. Após euvolemia: SG 5% + Água via SNE para reduzir Na+ em exatos 8 a 10 mEq/L por 24h (dividir déficit total em 48 a 72 horas)", "IV Central / Periférico", "Contínua em BIC"),
                _rx("rx_fwd_crit_ddavp", "Desmopressina (DDAVP) — Se Diabetes Insipidus Central (TCE / Pós-Hipofisectomia / Morte Encefálica)", "Desmopressina (DDAVP) 1 a 2 mcg IV ou SC a cada 12h (ou 10-20 mcg intranasal 12/12h) + Reposição horária da diurese excedente com SG 5% ou Água livre", "IV / SC / Intranasal", "12/12h se poliúria > 300 mL/h com densidade urinária < 1.005"),
            ], [
                _nonrx("nrx_fwd_crit", "Monitorização Intensiva em UTI com Sódio Sérico de 2/2h a 4/4h e Diurese Horária", "UTI", "No Diabetes Insipidus Nefrogênico por Lítio: suspender Lítio, associar Amilorida 5-10 mg/dia e Hidroclorotiazida + dieta hipossódica."),
            ]),
        ],
    }


def get_hyponatremia_adrogue() -> dict:
    return {
        "id": "calc_hyponatremia_adrogue",
        "slug": "hiponatremia-sintomatica-adrogue-madias-salina-3",
        "name": "Correção de Hiponatremia Sintomática & Fórmula de Adrogué-Madias (Salina Hipertônica NaCl 3%)",
        "acronym": "Adrogué-Madias (NaCl 3%)",
        "version": "1.0.0",
        "category": "Nefrologia e Meio Interno",
        "subcategory": "Distúrbios do Sódio e Emergências Neurológicas",
        "categorySlug": "bloco-06-nefrologia-meio-interno",
        "categoryName": "Nefrologia e Meio Interno",
        "moduleName": "Distúrbios Hidroeletrolíticos e Ácido-Base",
        "description": "Protocolo completo das Diretrizes Europeias (ESICM/ERA-EDTA) e Americanas para manejo da Hiponatremia (Na+ < 135 mEq/L) e cálculo da variação de sódio por litro de solução pela Fórmula de Adrogué-Madias [ΔNa = (Na_infusão - Na_sérico) / (ACT + 1)]. Define o bolus salvador de Salina Hipertônica NaCl 3% (513 mEq/L: 100 a 150 mL IV em 10-20 min) na encefalopatia hiponatrêmica aguda/grave (convulsões, coma) e impõe o teto máximo absoluto de elevação de 8 mEq/L em 24 horas (6 a 8 mEq/L/24h em alto risco) com protocolo de resgate com DDAVP + SG 5% para prevenir a Síndrome de Desmielinização Osmótica (Mielinólise Pontina).",
        "summary": "Bolus de NaCl 3% (100-150 mL) na hiponatremia sintomática grave, Fórmula de Adrogué-Madias e trava <= 8 mEq/L/24h.",
        "clinicalObjective": "Reverter rapidamente o edema cerebral agudo (elevando o Na+ em 4 a 6 mEq/L nas primeiras horas com NaCl 3%) sem jamais ultrapassar o limite de 8 a 10 mEq/L em 24h que desencadeia Mielinólise Pontina.",
        "targetPopulation": "Pacientes adultos com hiponatremia hipotônica verdadeira (Osmolaridade plasmática efetiva < 275 mOsm/kg, excluída pseudo-hiponatremia e hiperglicemia).",
        "calculationType": "additive_points",
        "formulaExpression": "ΔNa por 1L de NaCl 3% (513 mEq/L) = (513 - Na_atual) / (ACT + 1) | Receita Prática NaCl 3%: 850 mL SF 0,9% + 150 mL NaCl 20% (ou 445 mL AD + 55 mL NaCl 20%)",
        "evidenceSource": "Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia (ESICM/ESE/ERA-EDTA). Intensive Care Med. 2014;40(3):320-331; Adrogué HJ, Madias NE. Hyponatremia. N Engl J Med. 2000;342(21):1581-1589.",
        "minPossibleScore": 0,
        "maxPossibleScore": 14,
        "baseScore": 0,
        "badge": "eletrolitos",
        "clinicalWarning": "RECEITA PRÁTICA DE SALINA HIPERTÔNICA NaCl 3% (513 mEq/L = 0,513 mEq/mL): Diluir 150 mL de NaCl 20% (15 ampolas de 10 mL) + 850 mL de SF 0,9% (Total 1.000 mL a 3,1% = ~530 mEq/L) OU diluir 45 mL de NaCl 20% + 255 mL de SF 0,9% (Total 300 mL a 3%). TETO DE SEGURANÇA CONTRA MIELINÓLISE PONTINA: Elevar no MÁXIMO 8 mEq/L em 24 horas (e <= 6 mEq/L em 24h se alcoolismo, desnutrição, hepatopatia, hipocalemia associada ou Na+ inicial <= 105 mEq/L). Nota: Repor Potássio (KCl) eleva o Sódio sérico na mesma proporção osmótica (ΔNa = [(Na_inf + K_inf) - Na_sérico] / [ACT + 1])!",
        "radarAxes": [
            _axis("axis_hypo_neuro", "Sintomas Neurológicos (Edema Cerebral)", "Neurológico"),
            _axis("axis_hypo_na", "Nível de Sódio e Volemia (SIADH vs Hipovolemia)", "Osmolar", "mEq/L"),
            _axis("axis_hypo_ods", "Risco de Desmielinização Osmótica (ODS)", "Segurança"),
        ],
        "parameterGroups": [
            _grp("grp_hypo_symptoms", "1. Gravidade dos Sintomas Neurológicos de Edema Cerebral Hiponatrêmico", "sintomas-neurologicos-hiponatremia", "axis_hypo_neuro", 1, "A clínica neurológica (e não apenas o número isolado do sódio) define a indicação de bolus imediato de Salina 3%.", [
                _opt("opt_hypo_sym_none", "Assintomático ou Sintomas Leves Inespecíficos (Cefaleia leve, déficit de atenção/marcha) (0 pts)", 0, True, 0.1, 1, "Sem indicação de bolus de NaCl 3%; tratar conforme status volêmico e etiologia."),
                _opt("opt_hypo_sym_mod", "Sintomas Moderadamente Graves (Náuseas, vômitos, confusão mental, letargia intensa sem coma) (+3 pts)", 3, False, 0.65, 2, "Indicação de 1 bolus de NaCl 3% (150 mL IV em 20 min) ou infusão contínua controlada em BIC."),
                _opt("opt_hypo_sym_sev", "Sintomas Graves / Encefalopatia Hiponatrêmica Crítica (Convulsões, Coma GCS <= 8, Herniação ou Parada Respiratória) (+7 pts)", 7, False, 1.0, 3, "EMERGÊNCIA MÉDICA IMEDIATA: Bolus de 100 a 150 mL de NaCl 3% em 10-20 min (repetir até 2x se necessário para subir Na+ em 4 a 6 mEq/L na 1ª hora)."),
            ]),
            _grp("grp_hypo_sodium_vol", "2. Nível de Sódio Sérico Corrigido pela Glicemia e Perfil Volêmico", "sodio-volemia-hiponatremia", "axis_hypo_na", 2, "Descontar 1,6 mEq/L de Na+ para cada 100 mg/dL de Glicemia acima de 100 mg/dL (pseudo-hiponatremia translocacional).", [
                _opt("opt_hypo_na_mild", "Hiponatremia Leve a Moderada (Na+ 125 a 134 mEq/L) — Hipovolêmica, Euvolêmica (SIADH) ou Hipervolêmica (ICC/Cirrose) (0 pts)", 0, True, 0.2, 1, "Manejo etiológico: SF 0,9% se hipovolêmico; restrição hídrica < 800-1.000 mL/dia se SIADH ou hipervolêmico."),
                _opt("opt_hypo_na_prof", "Hiponatremia Profunda Bioquímica (Na+ 115 a 124 mEq/L) (+2 pts)", 2, False, 0.6, 2, "Vigilância laboratorial de 4/4h a 6/6h; alto risco de correção rápida inadvertida (aquaresis espontânea) se suspenso estímulo do ADH."),
                _opt("opt_hypo_na_extr", "Hiponatremia Extrema (Na+ < 115 mEq/L ou <= 105 mEq/L) (+4 pts)", 4, False, 1.0, 3, "Zona de altíssimo risco de Síndrome de Desmielinização Osmótica (Mielinólise Pontina) se subir > 6 a 8 mEq/L em 24h."),
            ]),
            _grp("grp_hypo_ods_risk", "3. Fatores de Alto Risco para Síndrome de Desmielinização Osmótica (Mielinólise Pontina)", "risco-mielinolise-pontina", "axis_hypo_ods", 3, "Crônica (> 48h), Etilismo crônico, Desnutrição grave, Hepatopatia/Cirrose, Hipocalemia concomitante ou Na+ <= 105 mEq/L.", [
                _opt("opt_hypo_ods_std", "Hiponatremia Aguda Documentada (< 48h: pós-operatório, polidipsia, maratonista, MDMA) sem fatores de risco (0 pts)", 0, True, 0.2, 1, "Teto de segurança: <= 8 a 10 mEq/L em 24h (e <= 18 mEq/L em 48h)."),
                _opt("opt_hypo_ods_high", "Hiponatremia Crônica (> 48h) OU presença de Alcoolismo, Cirrose, Desnutrição, Hipocalemia ou Na+ <= 105 mEq/L (+3 pts)", 3, False, 1.0, 2, "TETO ESTRITO REDUZIDO: elevar entre 4 e 6 mEq/L em 24h (NUNCA ultrapassar 8 mEq/L em 24h!). Vigiar diurese aquosa súbita (> 100 mL/h)."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_hypo_chronic_mild", "Hiponatremia Assintomática ou Leve Crônica — Manejo Etiológico Sem Salina 3% (0 a 2 pontos)", "low", 0, 2, "Sem edema cerebral agudo sintomático. O tratamento depende estritamente da volemia e osmolalidade/sódio urinário.", "#10b981", [
                _rx("rx_hypo_mild", "Conduta Guiada por Status Volêmico (Sem NaCl 3%)", "1) Hipovolêmica (Na_urinário < 30 mEq/L): SF 0,9% 50-100 mL/h (cuidado: ao restaurar a volemia, o ADH cai subitamente e pode disparar diurese aquosa rápida!). 2) Euvolêmica / SIADH (Na_urinário > 30 mEq/L, Osm_urinária > 100): Restrição hídrica < 800 mL/dia + Furosemida 20 mg VO + NaCl cápsulas 1-2 g 8/8h (ou Ureia oral 15-30 g/dia). 3) Hipervolêmica (ICC/Cirrose): Restrição hídrica + Furosemida IV + Espironolactona", "VO / IV", "Conforme volemia"),
            ], [
                _nonrx("nrx_hypo_mild", "Solicitar Osmolalidade Plasmática/Urinária, Sódio Urinário, TSH e Cortisol Matinal", "Enfermaria / Ambulatório", "Sempre excluir Hipotireoidismo grave e Insuficiência Adrenal (deficiência de cortisol simula SIADH e corrige rapidamente com Hidrocortisona 50-100 mg IV!)."),
            ]),
            _tier("tier_hypo_mod", "Hiponatremia Sintomática Moderada ou Profunda (Na+ < 120 mEq/L) com Alto Risco de ODS (3 a 6 pontos)", "high", 3, 6, "Necessidade de elevação controlada de 4 a 6 mEq/L em 24h (teto absoluto de 8 mEq/L/24h).", "#f59e0b", [
                _rx("rx_hypo_mod_3pct", "Infusão Controlada de Salina Hipertônica NaCl 3% (Adrogué-Madias) ou Bolus Único de 150 mL", "Se náuseas/vômitos/confusão: 1 bolus de 150 mL de NaCl 3% IV em 20 min OU infusão contínua em BIC: Taxa inicial (mL/h) ≈ Peso (kg) × 0,5 a 1,0 mL/h (ex.: 30 a 50 mL/h em adulto de 70 kg, onde 1 L de NaCl 3% sobe o Na+ em ~10 mEq/L). Suspender NaCl 3% assim que atingir subida de 5 mEq/L!", "IV em BIC", "Monitorar Na+ a cada 4h", "Preparo NaCl 3%: 850 mL SF 0,9% + 150 mL NaCl 20%. Se houver Hipocalemia associada, descontar os mEq de KCl infundidos do alvo de subida do sódio."),
            ], [
                _nonrx("nrx_hypo_mod", "Dosagem de Sódio Sérico a cada 4h e Monitorização Rigorosa de Diurese Horária", "Unidade Semi-Intensiva / UTI", "ALERTA DE AQUARESIS: Se a diurese ultrapassar subitamente > 100-150 mL/h com densidade urinária baixa (< 1.005), o paciente entrou em 'autocorreção' rápida por queda do ADH — aplicar protocolo de freio com DDAVP + SG 5%!"),
            ]),
            _tier("tier_hypo_emerg", "Emergência Neurológica Hiponatrêmica (Convulsão / Coma) — Bolus Imediato de NaCl 3% e Prevenção de Mielinólise (>= 7 pontos)", "critical", 7, 14, "Risco imediato de herniação transtentorial por edema cerebral agudo. Meta: subir Na+ em 4 a 6 mEq/L na 1ª hora e parar em <= 8 mEq/L nas 24h!", "#ef4444", [
                _rx("rx_hypo_crit_bolus", "Bolus Salvador de Salina Hipertônica NaCl 3% (Diretriz Europeia ESICM / Americana)", "Infundir IMEDIATAMENTE 150 mL de NaCl 3% IV em 10 a 20 minutos (pode ser feito em acesso venoso periférico!). Checar Na+ após 20 min e repetir 2º bolus de 150 mL em 20 min se persistência de coma/convulsão, até atingir elevação de 5 mEq/L no sódio sérico", "IV (Periférico ou Central)", "Bolus em 10-20 min", "TETO DE 24 HORAS: Após subir 5 mEq/L e cessar a convulsão/coma, SUSPENDER a Salina 3%! O ganho total nas primeiras 24h (incluindo os bolus iniciais) NÃO pode ultrapassar 8 mEq/L (ou 6 mEq/L em etilistas/cirróticos/desnutridos/Na <= 105)."),
                _rx("rx_hypo_crit_rescue", "Protocolo de Resgate (Re-Lowering) se Ultrapassar o Teto (> 8 mEq/L em 24h) ou Diurese > 150 mL/h", "Para travar a subida excessiva e prevenir Mielinólise Pontina: 1) Desmopressina (DDAVP) 2 mcg IV ou SC a cada 8h (trava a perda renal de água livre) + 2) Soro Glicosado 5% (SG 5%) 3 mL/kg/h IV em BIC até reduzir o Na+ de volta para a margem segura (<= 6-8 mEq/L acima do basal)", "IV + SC", "Resgate anti-mielinólise"),
            ], [
                _nonrx("nrx_hypo_crit", "Admissão em UTI, Proteção de Via Aérea (se GCS <= 8) e Sódio Sérico na Hora 1, 2, 4, 6 e a cada 4h", "UTI", "Monitorização neurológica contínua, sonda vesical para diurese horária e controle estrito da natremia."),
            ]),
        ],
    }


BLOCK_06_SYNONYMS: dict[str, list[str]] = {
    "calc_kdigo_lra": [
        "kdigo", "kdigo lra", "injuria renal aguda", "insuficiencia renal aguda", "ira", "lra",
        "criterios de akin", "oliguria", "anuria", "creatinina aguda", "urgencia dialitica",
        "aeiou dialise", "hemodialise de urgencia", "teste de estresse com furosemida", "cid n17",
    ],
    "calc_rifle": [
        "rifle", "classificacao rifle", "risk injury failure loss eskd", "disfuncao renal aguda",
        "adqi", "perda da funcao renal", "queda da tfg", "falencia renal aguda",
        "dependencia de dialise", "nefrologia intensiva", "cid n17.9",
    ],
    "calc_ckd_epi_2021": [
        "ckd-epi", "ckd epi 2021", "ckd-epi sem raca", "taxa de filtracao glomerular", "tfge",
        "egfr", "doenca renal cronica", "drc", "estadiamento kdigo", "g1 g2 g3a g3b g4 g5",
        "albuminuria a1 a2 a3", "relacao albumina creatinina", "isglt2 dapagliflozina", "cid n18",
    ],
    "calc_cockcroft_gault": [
        "cockcroft-gault", "cockcroft gault", "clearance de creatinina", "clcr", "depuracao de creatinina",
        "ajuste renal de antibioticos", "ajuste de dose renal", "enoxaparina ajuste renal", "meropenem ajuste renal",
        "vancomicina ajuste renal", "cefepime neurotoxicidade", "doac ajuste renal", "sanford guide",
    ],
    "calc_anion_gap": [
        "anion gap", "hiato anionico", "anion gap corrigido pela albumina", "formula de figge",
        "relacao delta-delta", "delta gap", "acidose metabolica", "acidose latica", "cetoacidose diabetica",
        "gold mark", "mudpiles", "acidose hipercloremica", "formula de winter", "gasometria arterial",
    ],
    "calc_free_water_deficit": [
        "deficit de agua livre", "hipernatremia", "sodio alto", "desidratacao hipernatremica",
        "soro glicosado 5 hipernatremia", "salina 0,45", "nacl 0,45%", "diabetes insipidus",
        "desmopressina ddavp", "edema cerebral hipernatremia", "agua corporal total", "cid e87.0",
    ],
    "calc_hyponatremia_adrogue": [
        "adrogue-madias", "formula de adrogue madias", "hiponatremia", "hiponatremia sintomatica",
        "salina hipertonica", "nacl 3%", "salina 3%", "sodio baixo", "siadh",
        "mielinolise pontina", "sindrome de desmielinizacao osmotica", "convulsao hiponatremia", "cid e87.1",
    ],
}


def get_block_06_calculators() -> list[dict]:
    calculators = [
        get_kdigo_lra(),
        get_rifle(),
        get_ckd_epi_2021(),
        get_cockcroft_gault(),
        get_anion_gap(),
        get_free_water_deficit(),
        get_hyponatremia_adrogue(),
    ]
    for calc in calculators:
        calc["blockId"] = "block_06"
        calc["blockFile"] = "block_06.json"
        calc["categorySlug"] = "bloco-06-nefrologia-meio-interno"
        calc["categoryName"] = "Nefrologia e Meio Interno"
    return calculators
