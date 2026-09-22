"""
Module 01: Sepsis, Septic Shock and Organ Dysfunction
- qSOFA
- SOFA
- APACHE II
- SAPS 3
"""

from .common import NOREPINEPHRINE_PROTOCOL, VASOPRESSIN_PROTOCOL, DOBUTAMINE_PROTOCOL

def get_qsofa():
    return {
        "id": "calc_qsofa",
        "slug": "qsofa",
        "name": "quick SOFA (Quick Sequential Organ Failure Assessment)",
        "acronym": "qSOFA",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Sepse, Choque Séptico e Disfunção Orgânica",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Sepse, Choque Séptico e Disfunção Orgânica",
        "description": "Triagem rápida à beira do leito de disfunção orgânica e risco de deterioração clínica em pacientes adultos com suspeita de infecção fora da UTI.",
        "summary": "Triagem rápida de disfunção orgânica e risco de mortalidade em suspeita de infecção fora da UTI.",
        "clinicalObjective": "Identificação precoce de pacientes infectados fora da UTI com alto risco de deterioração clínica, permanência prolongada em UTI ou óbito intra-hospitalar.",
        "targetPopulation": "Pacientes adultos (>= 18 anos) em pronto-socorro, unidades de pronto atendimento ou enfermarias com suspeita de infecção.",
        "calculationType": "additive_points",
        "formulaExpression": "FR_pontos + Glasgow_pontos + PAS_pontos",
        "evidenceSource": "Seymour CW, Liu VX, Iwashyna TJ, et al. Assessment of Clinical Criteria for Sepsis: For the Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315(8):762-774.",
        "minPossibleScore": 0,
        "maxPossibleScore": 3,
        "ssc2021Warning": True,
        "clinicalWarning": "O Surviving Sepsis Campaign (SSC 2021) desaconselha formalmente o uso isolado do qSOFA como ferramenta única de triagem ou exclusão de sepse, devido à sua sensibilidade insuficiente (< 60%). Pacientes sépticos graves podem apresentar qSOFA de 0 ou 1 ponto. Recomenda-se a triagem multimodal associando critérios de SIRS, NEWS ou MEWS, e o cálculo obrigatório do SOFA completo diante de qualquer suspeita clínica persistente.",
        "badge": "emergencia",
        "radarAxes": [
            {
                "id": "axis_qsofa_resp",
                "label": "Frequência Respiratória",
                "system": "Respiratório",
                "unit": "ipm",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_qsofa_gcs",
                "label": "Nível de Consciência",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_qsofa_sbp",
                "label": "Pressão Arterial Sistólica",
                "system": "Cardiovascular",
                "unit": "mmHg",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_qsofa_resp",
                "name": "Frequência Respiratória (FR)",
                "slug": "frequencia-respiratoria",
                "inputType": "single_choice",
                "unit": "ipm",
                "radarAxisId": "axis_qsofa_resp",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Contagem de incursões respiratórias por minuto em repouso.",
                "options": [
                    {
                        "id": "opt_resp_normal",
                        "label": "FR < 22 ipm (Eupneico / Normal)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Frequência respiratória normal dentro dos limites fisiológicos."
                    },
                    {
                        "id": "opt_resp_high",
                        "label": "FR >= 22 ipm (Taquipneia)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Taquipneia aguda indicando esforço ventilatório ou compensação metabólica."
                    }
                ]
            },
            {
                "id": "grp_qsofa_gcs",
                "name": "Estado Mental / Escala de Glasgow",
                "slug": "nivel-consciencia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_qsofa_gcs",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Avaliação de declínio agudo do estado mental em relação ao basal.",
                "options": [
                    {
                        "id": "opt_gcs_15",
                        "label": "Glasgow = 15 (Alerta e orientado)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem alteração aguda da cognição ou do nível de consciência."
                    },
                    {
                        "id": "opt_gcs_less_15",
                        "label": "Glasgow < 15 (Confusão, sonolência ou rebaixamento agudo)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Qualquer alteração cognitiva aguda ou queda do escore de Glasgow."
                    }
                ]
            },
            {
                "id": "grp_qsofa_sbp",
                "name": "Pressão Arterial Sistólica (PAS)",
                "slug": "pressao-sistolica",
                "inputType": "single_choice",
                "unit": "mmHg",
                "radarAxisId": "axis_qsofa_sbp",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Aferição de PA sistólica no membro superior.",
                "options": [
                    {
                        "id": "opt_sbp_normal",
                        "label": "PAS > 100 mmHg (Normotenso / Estável)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Pressão sistólica acima do limite crítico de hipoperfusão."
                    },
                    {
                        "id": "opt_sbp_low",
                        "label": "PAS <= 100 mmHg (Hipotensão arterial)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipotensão arterial sistólica sugestiva de choque ou vasoplegia séptica."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_qsofa_low",
                "label": "Baixo Risco pelo qSOFA (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada < 3%. Atenção: SSC 2021 alerta para baixa sensibilidade (< 60%); não descarta sepse se houver suspeita clínica fundamentada.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_qsofa_low_1",
                        "drugName": "Investigação Focada e Sintomáticos",
                        "dosage": "Individualizada conforme etiologia suspeita",
                        "route": "VO ou IV",
                        "frequency": "Conforme necessidade",
                        "dilutionInstructions": "Não aplicável",
                        "renalAdjustment": "Ajustar antibióticos orais conforme ClCr se infecção localizada confirmada.",
                        "contraindications": "Evitar anti-inflamatórios não esteroidais (AINEs) se risco de lesão renal aguda."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_qsofa_low_1",
                        "recommendationTitle": "Vigilância Clínica e Triagem Multimodal",
                        "dispositionTarget": "Observação / Enfermaria",
                        "monitoringPlan": "Aferição seriada de sinais vitais a cada 2 a 4 horas. Aplicar escores NEWS/MEWS ou SIRS. Se suspeita clínica de sepse persistir, calcular obrigatoriamente o SOFA completo.",
                        "laboratoryPanel": "Hemograma completo, PCR, urina 1 e cultura de sítio suspeito conforme julgamento clínico."
                    }
                ]
            },
            {
                "id": "tier_qsofa_high",
                "label": "Alto Risco de Sepse / Deterioração Aguda (2 a 3 pontos)",
                "severityLevel": "critical",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Aumento de 3 a 14 vezes na mortalidade hospitalar (risco estimado de 10% a 25%). Acionamento IMEDIATO do Protocolo de Sepse / Pacote de 1 Hora.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_qsofa_high_atb",
                        "drugName": "Piperacilina + Tazobactam (ou Cefepime)",
                        "dosage": "4,5g IV dose de ataque rápida, seguida de 4,5g IV infusão estendida em 3-4h a cada 8h",
                        "route": "Intravenosa",
                        "frequency": "8/8 horas",
                        "dilutionInstructions": "Reconstituir frasco com 20 mL de AD e diluir em 100 mL de SF 0,9% ou SG 5%.",
                        "renalAdjustment": "Se ClCr 20-40 mL/min: 3,375g 6/6h; se ClCr < 20 mL/min: 2,25g 6/6h. Se hemodiálise: 2,25g 8/8h + 0,75g pós-diálise.",
                        "contraindications": "Hipersensibilidade grave a penicilinas / betalactâmicos (considerar Levofloxacino 750mg + Amicacina)."
                    },
                    {
                        "id": "rx_qsofa_high_fluid",
                        "drugName": "Ringer Lactato ou Plasmalyte (Cristaloide Balanceado)",
                        "dosage": "30 mL/kg de peso ideal nas primeiras 3 horas",
                        "route": "Intravenosa rápida",
                        "frequency": "Bolus em 3 horas",
                        "dilutionInstructions": "Solução pronta para infusão em bolsas de 500 mL ou 1.000 mL.",
                        "renalAdjustment": "Avaliar responsividade volêmica (elevação passiva de pernas ou variação da pressão de pulso); cautela em insuficiência cardíaca grave com fração de ejeção reduzida.",
                        "contraindications": "Evitar excesso de volume em edema agudo de pulmão hipertensivo ou insuficiência renal anúrica sem responsividade."
                    },
                    {
                        "id": "rx_qsofa_high_norepi",
                        "drugName": "Noradrenalina (Hemitartarato de Norepinefrina)",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua em BIC",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas (16 mg) em 234 mL SG 5% (Solução Padrão: 64 mcg/mL). Veículo mandatório SG 5%.",
                        "renalAdjustment": "Não requer ajuste de dose para disfunção renal.",
                        "contraindications": "Uso em linha periférica aceitável apenas transitoriamente por no máximo 2-4 horas até acesso central.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_qsofa_high_1",
                        "recommendationTitle": "Pacote de 1 Hora da Sepse e Vaga de Terapia Intensiva",
                        "dispositionTarget": "UTI / Sala Vermelha",
                        "monitoringPlan": "Monitorização contínua com ECG, oximetria e PAI se instável. Manter meta de PAM >= 65 mmHg e débito urinário >= 0,5 mL/kg/h.",
                        "interventionalProcedure": "Cateter Venoso Central (CVC) em veia subclávia ou jugular interna; Pressão Arterial Invasiva (PAI); se rebaixamento persistente com Glasgow <= 8, intubação orotraqueal protetora.",
                        "ventilatorySupport": "Oxigenoterapia sob cateter ou máscara para manter SpO2 92-96%. Ventilação mecânica protetora (6 mL/kg peso predito, Pplatô < 30 cmH2O) se IOT.",
                        "vascularAccess": "Punção de CVC com técnica asséptica e guia ultrassonográfico preferencial.",
                        "laboratoryPanel": "Coleta imediata de 2 pares de hemoculturas de sítios distintos antes do antibiótico; dosagem seriada de lactato sérico na admissão e em 2 a 4h; gasometria arterial; coagulograma; bilirrubinas; creatinina e urina 1 com urocultura."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_sofa():
    return {
        "id": "calc_sofa",
        "slug": "sofa",
        "name": "Sequential Organ Failure Assessment",
        "acronym": "SOFA",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Sepse, Choque Séptico e Disfunção Orgânica",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Sepse, Choque Séptico e Disfunção Orgânica",
        "description": "Estratificação diária e quantificação exaustiva de disfunção orgânica aguda em 6 sistemas fisiológicos independentes (0 a 24 pontos).",
        "summary": "Estratificação formal de disfunção orgânica múltipla (respiratória, hematológica, hepática, cardiovascular, neurológica e renal).",
        "clinicalObjective": "Diagnóstico formal de Sepse (variação Delta SOFA >= 2 pontos decorrente de infecção) e monitorização diária do grau de falência multiorgânica em UTI.",
        "targetPopulation": "Pacientes críticos internados em UTI, semi-intensiva ou sala de emergência.",
        "calculationType": "additive_points",
        "formulaExpression": "Resp + Coag + Hep + Cardiovasc + SNC + Renal",
        "evidenceSource": "Vincent JL, Moreno R, Takala J, et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. Intensive Care Med. 1996;22(7):707-710.",
        "minPossibleScore": 0,
        "maxPossibleScore": 24,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_sofa_resp", "label": "Respiratório", "system": "Respiratório", "unit": "PaO2/FiO2", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_sofa_coag", "label": "Coagulação", "system": "Hematológico", "unit": "x10^3/mm³", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_sofa_liver", "label": "Fígado", "system": "Hepático", "unit": "mg/dL", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_sofa_cv", "label": "Cardiovascular", "system": "Cardiovascular", "unit": "PAM/Drogas", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_sofa_cns", "label": "Neurológico", "system": "Neurológico", "unit": "GCS", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_sofa_renal", "label": "Renal", "system": "Renal", "unit": "Cr/Diurese", "baselineValue": 0, "maxAxisValue": 4}
        ],
        "parameterGroups": [
            {
                "id": "grp_sofa_resp",
                "name": "1. Sistema Respiratório (PaO2 / FiO2)",
                "slug": "sistema-respiratorio",
                "inputType": "single_choice",
                "unit": "mmHg",
                "radarAxisId": "axis_sofa_resp",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "helpText": "Relação PaO2/FiO2 obtida por gasometria arterial e fração inspirada de oxigênio.",
                "options": [
                    {"id": "opt_sofa_resp_0", "label": "PaO2/FiO2 >= 400 mmHg", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_resp_1", "label": "PaO2/FiO2 < 400 mmHg (300 a 399)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_resp_2", "label": "PaO2/FiO2 < 300 mmHg (200 a 299)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_resp_3", "label": "PaO2/FiO2 < 200 mmHg COM suporte ventilatório (VM ou VNI)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_resp_4", "label": "PaO2/FiO2 < 100 mmHg COM suporte ventilatório (SDRA grave)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_sofa_coag",
                "name": "2. Coagulação (Plaquetas)",
                "slug": "sistema-coagulacao",
                "inputType": "single_choice",
                "unit": "x10^3/mm³",
                "radarAxisId": "axis_sofa_coag",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 2,
                "helpText": "Contagem de plaquetas no sangue periférico.",
                "options": [
                    {"id": "opt_sofa_coag_0", "label": "Plaquetas >= 150.000 /mm³", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_coag_1", "label": "Plaquetas < 150.000 /mm³ (100k a 149k)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_coag_2", "label": "Plaquetas < 100.000 /mm³ (50k a 99k)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_coag_3", "label": "Plaquetas < 50.000 /mm³ (20k a 49k)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_coag_4", "label": "Plaquetas < 20.000 /mm³ (Trombocitopenia crítica)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_sofa_liver",
                "name": "3. Sistema Hepático (Bilirrubina Total)",
                "slug": "sistema-hepatico",
                "inputType": "single_choice",
                "unit": "mg/dL",
                "radarAxisId": "axis_sofa_liver",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 3,
                "helpText": "Bilirrubina total sérica.",
                "options": [
                    {"id": "opt_sofa_liver_0", "label": "Bilirrubina < 1,2 mg/dL", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_liver_1", "label": "Bilirrubina 1,2 a 1,9 mg/dL", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_liver_2", "label": "Bilirrubina 2,0 a 5,9 mg/dL", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_liver_3", "label": "Bilirrubina 6,0 a 11,9 mg/dL", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_liver_4", "label": "Bilirrubina >= 12,0 mg/dL", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_sofa_cv",
                "name": "4. Sistema Cardiovascular (Hipotensão e Vasopressores)",
                "slug": "sistema-cardiovascular",
                "inputType": "single_choice",
                "unit": "mcg/kg/min",
                "radarAxisId": "axis_sofa_cv",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 4,
                "helpText": "Pressão arterial média ou taxa de infusão de drogas vasoativas administradas por pelo menos 1 hora.",
                "options": [
                    {"id": "opt_sofa_cv_0", "label": "PAM >= 70 mmHg (Sem drogas vasoativas)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_cv_1", "label": "PAM < 70 mmHg (Sem vasopressores)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_cv_2", "label": "Dopamina <= 5 mcg/kg/min OU Dobutamina em qualquer dose", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_cv_3", "label": "Dopamina > 5 OU Noradrenalina <= 0,1 OU Adrenalina <= 0,1 mcg/kg/min", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_cv_4", "label": "Dopamina > 15 OU Noradrenalina > 0,1 OU Adrenalina > 0,1 mcg/kg/min", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_sofa_cns",
                "name": "5. Sistema Nervoso Central (Escala de Glasgow)",
                "slug": "sistema-nervoso",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_sofa_cns",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 5,
                "helpText": "Escala de Coma de Glasgow (se paciente sedado, estimar pontuação pré-sedação).",
                "options": [
                    {"id": "opt_sofa_cns_0", "label": "Glasgow = 15", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_cns_1", "label": "Glasgow 13 a 14", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_cns_2", "label": "Glasgow 10 a 12", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_cns_3", "label": "Glasgow 6 a 9", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_cns_4", "label": "Glasgow < 6", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_sofa_renal",
                "name": "6. Sistema Renal (Creatinina ou Débito Urinário)",
                "slug": "sistema-renal",
                "inputType": "single_choice",
                "unit": "mg/dL ou mL/dia",
                "radarAxisId": "axis_sofa_renal",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 6,
                "helpText": "Nível de creatinina sérica ou diurese diária.",
                "options": [
                    {"id": "opt_sofa_renal_0", "label": "Creatinina < 1,2 mg/dL", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sofa_renal_1", "label": "Creatinina 1,2 a 1,9 mg/dL", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_sofa_renal_2", "label": "Creatinina 2,0 a 3,4 mg/dL", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_sofa_renal_3", "label": "Creatinina 3,5 a 4,9 mg/dL OU Diurese < 500 mL/dia", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_sofa_renal_4", "label": "Creatinina >= 5,0 mg/dL OU Diurese < 200 mL/dia (Anúria/Oligúria severa)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_sofa_0",
                "label": "Disfunção Orgânica Ausente ou Basal (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Mortalidade em UTI estimada < 5%. Delta SOFA < 2 não preenche critério de sepse pelo Sepsis-3.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sofa_0_1",
                        "drugName": "Conduta Farmacológica: Nenhuma intervenção de suporte avançado indicada nesta faixa",
                        "dosage": "Manutenção habitual",
                        "route": "VO/IV",
                        "frequency": "Rotina",
                        "renalAdjustment": "Avaliar função renal basal."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sofa_0_1",
                        "recommendationTitle": "Monitorização Clínica Regular",
                        "dispositionTarget": "Enfermaria / Observação",
                        "monitoringPlan": "Reavaliação diária de escore SOFA e controle de exames laboratoriais a cada 24-48h."
                    }
                ]
            },
            {
                "id": "tier_sofa_1",
                "label": "Disfunção Orgânica Leve a Moderada / Sepse Inicial (2 a 6 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 6,
                "statisticalOutcome": "Mortalidade em UTI estimada entre 10% e 20%. Presença de Sepse confirmada se infecção associada.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sofa_1_abx",
                        "drugName": "Antibioticoterapia Ampla Empírica",
                        "dosage": "Ajustada por peso e foco infeccioso",
                        "route": "IV",
                        "frequency": "Conforme droga",
                        "dilutionInstructions": "Infusão precoce na primeira hora.",
                        "renalAdjustment": "Ajuste obrigatório para ClCr se disfunção renal presente."
                    },
                    {
                        "id": "rx_sofa_1_fluid",
                        "drugName": "Cristaloides Balanceados",
                        "dosage": "30 mL/kg nas primeiras 3h se sinais de hipoperfusão",
                        "route": "IV",
                        "frequency": "Em bolus",
                        "renalAdjustment": "Avaliar sobrecarga volêmica."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sofa_1_1",
                        "recommendationTitle": "Admissão em Unidade Semi-Intensiva ou UTI",
                        "dispositionTarget": "Semi-Intensiva / UTI",
                        "monitoringPlan": "Monitorização hemodinâmica contínua, balanço hídrico rigoroso de 2 em 2 horas e gasometria com lactato seriada.",
                        "laboratoryPanel": "Hemograma, coagulograma, ureia, creatinina, bilirrubinas, gasometria arterial e lactato 12/12h."
                    }
                ]
            },
            {
                "id": "tier_sofa_2",
                "label": "Disfunção Orgânica Grave (7 a 11 pontos)",
                "severityLevel": "high",
                "minScore": 7,
                "maxScore": 11,
                "statisticalOutcome": "Mortalidade em UTI estimada entre 30% e 50%. Falência de 2 ou mais órgãos.",
                "colorHex": "#ea580c",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sofa_2_norepi",
                        "drugName": "Noradrenalina (Hemitartarato de Norepinefrina)",
                        "dosage": "0,1 a 0,5 mcg/kg/min IV contínua em BIC",
                        "route": "IV contínua em CVC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL).",
                        "renalAdjustment": "Sem ajuste renal necessário.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    },
                    {
                        "id": "rx_sofa_2_vaso",
                        "drugName": "Vasopressina (Arginina Vasopressina)",
                        "dosage": "0,01 a 0,04 UI/min em dose fixa (padrão 0,03 UI/min = 9 mL/h)",
                        "route": "IV contínua em CVC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "1 ampola (20 UI) em 99 mL SF 0,9% ou SG 5% (0,2 UI/mL).",
                        "renalAdjustment": "Sem ajuste renal.",
                        "infusionProtocol": VASOPRESSIN_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sofa_2_1",
                        "recommendationTitle": "Suporte Intensivo Nível 3",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Acesso Venoso Central obrigatório, PAI e sondagem vesical de demora com medição horária de diurese.",
                        "ventilatorySupport": "Se PaO2/FiO2 < 200, considerar IOT com estratégia protetora (Vt 6 mL/kg, Pplatô < 30 cmH2O, PEEP titulada).",
                        "vascularAccess": "CVC duplo lúmen e PAI radial/femoral."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_sofa_3",
                "label": "Falência Multiorgânica Catastrófica (12 a 24 pontos)",
                "severityLevel": "critical",
                "minScore": 12,
                "maxScore": 24,
                "statisticalOutcome": "Mortalidade em UTI excede 60% a 95% (se escore > 15 pontos, mortalidade > 80-90%). Múltiplas disfunções avançadas com choque vasoplégico refratário.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sofa_3_vasopressores",
                        "drugName": "Vasopressores em Associação (Noradrenalina + Vasopressina) +/- Dobutamina",
                        "dosage": "Nora até 2,0 mcg/kg/min + Vasopressina 0,03 UI/min fixa + Dobutamina 2,5-20 mcg/kg/min se disfunção miocárdica",
                        "route": "IV contínua em BIC por CVC exclusivo",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Usar soluções concentradas (Noradrenalina 128 mcg/mL; Dobutamina 2.000 mcg/mL) para restrição hídrica.",
                        "renalAdjustment": "Avaliar terapia de substituição renal contínua (CRRT/CVVHDF).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    },
                    {
                        "id": "rx_sofa_3_corticoide",
                        "drugName": "Hidrocortisona",
                        "dosage": "200 mg/dia (50 mg IV 6/6h ou 200 mg em infusão contínua 24h)",
                        "route": "IV",
                        "frequency": "6/6h ou contínua",
                        "dilutionInstructions": "Diluir em SF 0,9% ou SG 5%.",
                        "indication": "Choque séptico refratário a vasopressores após ressuscitação volêmica adequada."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sofa_3_1",
                        "recommendationTitle": "Suporte Vital Avançado Máximo e Alinhamento de Diretivas",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Monitorização hemodinâmica invasiva avançada (termodiluição transpulmonar PiCCO ou cateter de Swan-Ganz / ecocardiograma seriado).",
                        "interventionalProcedure": "Considerar Posição Prona (>= 16h/dia) se PaO2/FiO2 < 150 em VM protetora; avaliar indicação de Terapia Renal Substitutiva Contínua (CRRT); alinhar metas de proporcionalidade terapêutica com familiares.",
                        "ventilatorySupport": "Ventilação protetora extrema, bloqueio neuromuscular precoce (Cisatracúrio) se assincronia grave nas primeiras 48h.",
                        "vascularAccess": "CVC, PAI e Cateter de Diálise (Shilley ou duplo lúmen calibroso)."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_apache_ii():
    return {
        "id": "calc_apache_ii",
        "slug": "apache-ii",
        "name": "APACHE II (Acute Physiology and Chronic Health Evaluation II)",
        "acronym": "APACHE II",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Sepse, Choque Séptico e Disfunção Orgânica",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Sepse, Choque Séptico e Disfunção Orgânica",
        "description": "Sistema de pontuação prognóstica para estratificação de gravidade e mortalidade intra-hospitalar nas primeiras 24 horas de admissão na UTI.",
        "summary": "Índice prognóstico de gravidade nas primeiras 24h de UTI (12 variáveis fisiológicas + idade + doença crônica).",
        "clinicalObjective": "Calibração de risco de mortalidade hospitalar na admissão da UTI e avaliação comparativa de desempenho assistencial.",
        "targetPopulation": "Pacientes adultos admitidos em UTI geral clínico-cirúrgica (exclui pós-operatório cardíaco eletivo, queimados e estada < 8h).",
        "calculationType": "additive_points",
        "evidenceSource": "Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease classification system. Crit Care Med. 1985;13(10):818-829.",
        "minPossibleScore": 0,
        "maxPossibleScore": 71,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_ap_age", "label": "Idade", "system": "Demográfico", "baselineValue": 0, "maxAxisValue": 6},
            {"id": "axis_ap_physio", "label": "Fisiologia Aguda", "system": "Multissistêmico", "baselineValue": 0, "maxAxisValue": 60},
            {"id": "axis_ap_chronic", "label": "Doença Crônica", "system": "Comorbidade", "baselineValue": 0, "maxAxisValue": 5}
        ],
        "parameterGroups": [
            {
                "id": "grp_ap_age",
                "name": "Faixa Etária (Idade)",
                "slug": "idade",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_age",
                "normalBaselineValue": 0,
                "maxAxisValue": 6,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_ap_age_0", "label": "<= 44 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_age_2", "label": "45 a 54 anos (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_ap_age_3", "label": "55 a 64 anos (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_ap_age_5", "label": "65 a 74 anos (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.83, "sortOrder": 4},
                    {"id": "opt_ap_age_6", "label": ">= 75 anos (+6 pts)", "pointValue": 6, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_ap_chronic",
                "name": "Condição de Saúde Crônica / Falência Prévia de Órgão",
                "slug": "condicao-cronica",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_chronic",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 2,
                "helpText": "Histórico documentado de cirrose com HDA/icterícia, insuficiência cardíaca classe IV NYHA, DPOC severo com hipóxia crônica, diálise crônica ou imunossupressão grave.",
                "options": [
                    {"id": "opt_ap_chr_0", "label": "Sem disfunção crônica de órgãos maiores (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_chr_2", "label": "Cirurgia eletiva com comorbidade crônica grave (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 2},
                    {"id": "opt_ap_chr_5", "label": "Cirurgia de urgência ou paciente clínico com falência crônica/imunossupressão (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3}
                ]
            },
            {
                "id": "grp_ap_temp",
                "name": "Temperatura Central (°C)",
                "slug": "temperatura",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_physio",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_ap_tmp_norm", "label": "36,0°C a 38,4°C (Normal: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_tmp_1", "label": "34,0°C a 35,9°C OU 38,5°C a 38,9°C (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_ap_tmp_2", "label": "32,0°C a 33,9°C (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_ap_tmp_3", "label": "30,0°C a 31,9°C OU 39,0°C a 40,9°C (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_ap_tmp_4", "label": "< 30,0°C OU >= 41,0°C (Hipotermia grave / Hipertermia extrema: +4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_ap_map",
                "name": "Pressão Arterial Média (PAM em mmHg)",
                "slug": "pam",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_physio",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_ap_map_0", "label": "70 a 109 mmHg (Normal: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_map_2", "label": "110 a 129 mmHg OU 50 a 69 mmHg (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2},
                    {"id": "opt_ap_map_3", "label": "130 a 159 mmHg (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 3},
                    {"id": "opt_ap_map_4", "label": "<= 49 mmHg OU >= 160 mmHg (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_ap_hr",
                "name": "Frequência Cardíaca (FC em bpm)",
                "slug": "fc",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_physio",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_ap_hr_0", "label": "70 a 109 bpm (Normal: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_hr_2", "label": "55 a 69 bpm OU 110 a 139 bpm (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2},
                    {"id": "opt_ap_hr_3", "label": "40 a 54 bpm OU 140 a 179 bpm (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 3},
                    {"id": "opt_ap_hr_4", "label": "<= 39 bpm OU >= 180 bpm (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_ap_gcs",
                "name": "Escala de Coma de Glasgow (Déficit em relação a 15)",
                "slug": "glasgow-deficit",
                "inputType": "single_choice",
                "radarAxisId": "axis_ap_physio",
                "normalBaselineValue": 0,
                "maxAxisValue": 12,
                "sortOrder": 6,
                "helpText": "Pontos = 15 menos Glasgow real.",
                "options": [
                    {"id": "opt_ap_gcs_15", "label": "Glasgow 15 (Déficit 0: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ap_gcs_13", "label": "Glasgow 13-14 (Déficit 1-2: +2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.17, "sortOrder": 2},
                    {"id": "opt_ap_gcs_10", "label": "Glasgow 10-12 (Déficit 3-5: +4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3},
                    {"id": "opt_ap_gcs_7", "label": "Glasgow 7-9 (Déficit 6-8: +7 pts)", "pointValue": 7, "isNormalBaseline": False, "radarNormalizedValue": 0.58, "sortOrder": 4},
                    {"id": "opt_ap_gcs_3", "label": "Glasgow 3-6 (Déficit 9-12: +10 pts)", "pointValue": 10, "isNormalBaseline": False, "radarNormalizedValue": 0.83, "sortOrder": 5}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ap_0_9",
                "label": "Baixa Gravidade (0 a 9 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 9,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada < 5% a 8%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ap_1", "recommendationTitle": "Suporte e vigilância em semi-intensiva", "dispositionTarget": "Semi-Intensiva", "monitoringPlan": "Rotina diária de UTI."}
                ]
            },
            {
                "id": "tier_ap_10_19",
                "label": "Gravidade Moderada (10 a 19 pontos)",
                "severityLevel": "intermediate",
                "minScore": 10,
                "maxScore": 19,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada entre 15% e 25%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ap_2", "recommendationTitle": "Cuidados intensivos padrão", "dispositionTarget": "UTI", "monitoringPlan": "Monitorização hemodinâmica contínua e balanço hídrico."}
                ]
            },
            {
                "id": "tier_ap_20_29",
                "label": "Gravidade Alta (20 a 29 pontos)",
                "severityLevel": "high",
                "minScore": 20,
                "maxScore": 29,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada entre 35% e 55%.",
                "colorHex": "#ea580c",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ap_3", "recommendationTitle": "Suporte intensivo avançado", "dispositionTarget": "UTI", "monitoringPlan": "Suporte a falências de múltiplos órgãos e monitorização invasiva."}
                ]
            },
            {
                "id": "tier_ap_30_71",
                "label": "Gravidade Extrema / Crítica (>= 30 pontos)",
                "severityLevel": "critical",
                "minScore": 30,
                "maxScore": 71,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada superior a 70% a > 85%.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ap_4", "recommendationTitle": "Suporte vital máximo / Alinhamento de diretivas", "dispositionTarget": "UTI", "monitoringPlan": "Suporte ventilatório e hemodinâmico máximo; alinhar metas de proporcionalidade."}
                ]
            }
        ]
    }

def get_saps_3():
    return {
        "id": "calc_saps_3",
        "slug": "saps-3",
        "name": "SAPS 3 (Simplified Acute Physiology Score III)",
        "acronym": "SAPS 3",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Sepse, Choque Séptico e Disfunção Orgânica",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Sepse, Choque Séptico e Disfunção Orgânica",
        "description": "Modelo de predição de mortalidade hospitalar na UTI baseado exclusivamente em dados aferidos na primeira hora de admissão (+/- 1h).",
        "summary": "Modelo prognóstico baseado estritamente na 1ª hora de UTI para calibração de mortalidade hospitalar.",
        "clinicalObjective": "Cálculo da probabilidade de óbito hospitalar individualizado calibrado para a América Latina com dados estritamente da admissão.",
        "targetPopulation": "Adultos admitidos em UTI geral.",
        "calculationType": "additive_points",
        "evidenceSource": "Moreno RP, Metnitz PG, Almeida E, et al. SAPS 3--From evaluation of the patient to evaluation of the intensive care unit. Intensive Care Med. 2005;31(10):1336-1344.",
        "minPossibleScore": 0,
        "maxPossibleScore": 217,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_saps_box1", "label": "Caixa 1: Características Prévias", "system": "Demográfico/Crônico", "baselineValue": 0, "maxAxisValue": 50},
            {"id": "axis_saps_box2", "label": "Caixa 2: Circunstâncias da Admissão", "system": "Admissão", "baselineValue": 0, "maxAxisValue": 50},
            {"id": "axis_saps_box3", "label": "Caixa 3: Fisiologia Aguda na 1ªh", "system": "Fisiologia Aguda", "baselineValue": 0, "maxAxisValue": 117}
        ],
        "parameterGroups": [
            {
                "id": "grp_saps_age",
                "name": "Idade na Admissão",
                "slug": "idade-saps",
                "inputType": "single_choice",
                "radarAxisId": "axis_saps_box1",
                "normalBaselineValue": 0,
                "maxAxisValue": 18,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_saps_age_0", "label": "< 40 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_saps_age_1", "label": "40 a 59 anos (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.28, "sortOrder": 2},
                    {"id": "opt_saps_age_2", "label": "60 a 69 anos (+9 pts)", "pointValue": 9, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_saps_age_3", "label": "70 a 74 anos (+13 pts)", "pointValue": 13, "isNormalBaseline": False, "radarNormalizedValue": 0.72, "sortOrder": 4},
                    {"id": "opt_saps_age_4", "label": "75 a 79 anos (+16 pts)", "pointValue": 16, "isNormalBaseline": False, "radarNormalizedValue": 0.89, "sortOrder": 5},
                    {"id": "opt_saps_age_5", "label": ">= 80 anos (+18 pts)", "pointValue": 18, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_saps_location",
                "name": "Origem do Paciente antes da UTI",
                "slug": "origem-paciente",
                "inputType": "single_choice",
                "radarAxisId": "axis_saps_box2",
                "normalBaselineValue": 0,
                "maxAxisValue": 8,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_saps_loc_0", "label": "Centro Cirúrgico / Recuperação Pós-Anestésica (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_saps_loc_1", "label": "Pronto-Socorro / Emergência (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.63, "sortOrder": 2},
                    {"id": "opt_saps_loc_2", "label": "Enfermaria / Outra UTI de outro hospital (+8 pts)", "pointValue": 8, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3}
                ]
            },
            {
                "id": "grp_saps_vaso",
                "name": "Uso de Drogas Vasoativas na 1ª hora",
                "slug": "vasoativos-admissao",
                "inputType": "single_choice",
                "radarAxisId": "axis_saps_box3",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_saps_vaso_no", "label": "Sem drogas vasoativas na 1ª hora (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_saps_vaso_yes", "label": "Em uso de vasopressor ou inotrópico na 1ª hora (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_saps_gcs",
                "name": "Escala de Glasgow na Admissão da UTI",
                "slug": "glasgow-saps",
                "inputType": "single_choice",
                "radarAxisId": "axis_saps_box3",
                "normalBaselineValue": 0,
                "maxAxisValue": 15,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_saps_gcs_15", "label": "Glasgow = 15 (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_saps_gcs_13", "label": "Glasgow 13 a 14 (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.13, "sortOrder": 2},
                    {"id": "opt_saps_gcs_7", "label": "Glasgow 7 a 12 (+7 pts)", "pointValue": 7, "isNormalBaseline": False, "radarNormalizedValue": 0.47, "sortOrder": 3},
                    {"id": "opt_saps_gcs_6", "label": "Glasgow < 7 ou sedado (+15 pts)", "pointValue": 15, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_saps_low",
                "label": "Baixo Risco de Óbito Hospitalar (< 40 pts)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 39,
                "statisticalOutcome": "Probabilidade de óbito hospitalar estimada < 10%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_saps_1", "recommendationTitle": "Cuidados intensivos intermediários", "dispositionTarget": "UTI", "monitoringPlan": "Monitorização de rotina de UTI."}
                ]
            },
            {
                "id": "tier_saps_mod",
                "label": "Risco Intermediário (40 a 59 pts)",
                "severityLevel": "intermediate",
                "minScore": 40,
                "maxScore": 59,
                "statisticalOutcome": "Probabilidade de óbito hospitalar calibrada de 15% a 35%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_saps_2", "recommendationTitle": "Cuidados intensivos com vigilância ativa", "dispositionTarget": "UTI", "monitoringPlan": "Monitorização contínua de sinais vitais e disfunções orgânicas."}
                ]
            },
            {
                "id": "tier_saps_high",
                "label": "Alto Risco de Óbito Hospitalar (60 a 79 pts)",
                "severityLevel": "high",
                "minScore": 60,
                "maxScore": 79,
                "statisticalOutcome": "Probabilidade de óbito hospitalar entre 40% e 70%.",
                "colorHex": "#ea580c",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_saps_3", "recommendationTitle": "Suporte intensivo avançado contínuo", "dispositionTarget": "UTI", "monitoringPlan": "Suporte ventilatório e vasopressor invasivo."}
                ]
            },
            {
                "id": "tier_saps_crit",
                "label": "Risco Crítico / Muito Alto (>= 80 pts)",
                "severityLevel": "critical",
                "minScore": 80,
                "maxScore": 217,
                "statisticalOutcome": "Probabilidade de óbito hospitalar excede 75% a > 90%.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_saps_4", "recommendationTitle": "Suporte vital máximo e conferência familiar", "dispositionTarget": "UTI", "monitoringPlan": "Alinhamento precoce de metas de cuidado e proporcionalidade terapêutica."}
                ]
            }
        ]
    }
