"""
Block 03: Module B - Neurocirurgia Vascular & Aneurismas
1. Hunt-Hess (HSA, 1-5 + 1a + comorbidity modifier)
2. WFNS (HSA, I-V)
3. Fisher Clássica (HSA, 1-4)
4. Fisher Modificada / Claassen 2001 (HSA, 0-4)
5. Vasograde (HSA / DCI Risk Matrix, Green / Yellow / Red)
6. Spetzler-Martin (MAVs, I-V + VI inoperável)
7. Spetzler-Martin Suplementar / Lawton-Young (MAVs, 2-10 pts)
8. Zabramski (Cavernomas, I-IV)
9. PHASES Score (Aneurismas não rotos, 0-22 pts)
10. UIATS (Aneurismas não rotos, indicação ativa vs conservadora)
11. Cognard & Borden (FAVDs / Fístulas Durais, I-V)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL

# Import existing implementations
from calculators.block03_neuro.hsa_mav import (
    get_hunt_hess,
    get_wfns,
    get_fisher_classic,
    get_fisher_modified,
    get_spetzler_martin,
)


def get_vasograde():
    """Vasograde Risk Stratification Score for DCI in aSAH (de Oliveira Manoel et al., Stroke 2014)."""
    return {
        "id": "calc_vasograde",
        "slug": "vasograde",
        "name": "Vasograde para Estratificação de Risco de DCI e Vasoespasmo",
        "acronym": "Vasograde",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Escore de decisão visual à beira do leito que cruza a escala clínica WFNS (1 a 5) com a escala tomográfica de Fisher Modificado / Claassen (0 a 4), categorizando os pacientes em 3 estratos de risco de Isquemia Cerebral Tardia (DCI).",
        "summary": "Cruzamento bidimensional de WFNS e Fisher Modificado para predição de DCI e vasoespasmo na HSA.",
        "clinicalObjective": "Identificar pacientes de alto risco para desenvolvimento de Isquemia Cerebral Tardia (DCI) e vasoespasmo arterial sintomático para escalonamento neurointensivo.",
        "targetPopulation": "Pacientes com diagnóstico confirmado de HSA aneurismática admitidos em UTI neurocrítica nas primeiras 72 horas.",
        "calculationType": "branching_decision",
        "formulaExpression": "Cruzamento Matricial: WFNS x Fisher Modificado (Claassen)",
        "evidenceSource": "de Oliveira Manoel AL, Jaja BN, Germans MR, et al. The VASOGRADE: a simple clinical metric for delayed cerebral ischemia after subarachnoid hemorrhage. Stroke. 2014;45(1):294-298.",
        "minPossibleScore": 1,
        "maxPossibleScore": 3,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ALERTA PRETO DE SEGURANÇA MANDATÓRIO: O Nimodipino deve ser administrado estritamente por VIA ORAL ou SONDA NASOENTERAL (60 mg 4/4h por 21 dias). A infusão intravenosa ou parenteral é TERMINANTEMENTE PROIBIDA pelo risco de colapso cardiovascular maciço e choque refratário fatal. A indução de hipertensão com Noradrenalina está proscrita antes da oclusão definitiva do aneurisma.",
        "radarAxes": [
            {"id": "axis_vaso_clinical", "label": "Status Clínico (WFNS)", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_vaso_imaging", "label": "Sangue Tomográfico (Fisher)", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_vaso_dci", "label": "Risco de DCI / Vasoespasmo", "system": "Vascular", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_vasograde_category",
                "name": "Estrato Matricial Vasograde",
                "slug": "estrato-vasograde",
                "inputType": "single_choice",
                "radarAxisId": "axis_vaso_dci",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Selecione a combinação de WFNS e Fisher Modificado avaliados na admissão.",
                "options": [
                    {
                        "id": "opt_vaso_green",
                        "label": "Vasograde-Green (Verde): WFNS 1 ou 2 E Fisher Modificado 0, 1 ou 2",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Bom estado clínico (Glasgow 13-15 sem déficit) e sangramento subaracnóideo fino sem coágulos espessos.",
                    },
                    {
                        "id": "opt_vaso_yellow",
                        "label": "Vasograde-Yellow (Amarelo): WFNS 1, 2 ou 3 E Fisher Modificado 3 ou 4",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Bom ou moderado estado neurológico, porém com coágulos cisternais espessos (>= 1 mm) e/ou hemorragia intraventricular bilateral.",
                    },
                    {
                        "id": "opt_vaso_red",
                        "label": "Vasograde-Red (Vermelho): WFNS 4 ou 5 (qualquer grau de Fisher)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Mau grau clínico (Glasgow 3 a 12) independente da espessura do sangue na tomografia.",
                    },
                ],
            }
        ],
        "riskTiers": [
            {
                "id": "tier_vaso_green",
                "label": "Vasograde-Green: Baixo Risco de DCI",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Incidência estimada de Isquemia Cerebral Tardia (DCI) de aproximadamente 15% a 20%. Mortalidade intra-hospitalar baixa (< 10%).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_vaso_nimo",
                        "drugName": "Nimodipino Oral / Enteral",
                        "dosage": "60 mg VO ou SNE a cada 4 horas por 21 dias contínuos",
                        "route": "Oral / SNE exclusiva",
                        "frequency": "4/4h",
                        "dilutionInstructions": "PROIBIDO USO INTRAVENOSO. Se por sonda, aspirar cápsula com seringa oral e lavar com 20 mL de água.",
                        "contraindications": "Choque hipotensivo grave refratário.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_vaso_green",
                        "recommendationTitle": "Tratamento Intervencionista / Cirúrgico Precoce do Aneurisma",
                        "dispositionTarget": "UTI Neurocrítica / Semi-Intensiva",
                        "monitoringPlan": "Doppler Transcraniano (DTC) a cada 48 horas. Manter euvolemia estrita com cristaloide isotônico (SF 0,9% ou Ringer Lactato 2 a 3 L/dia).",
                        "interventionalProcedure": "Oclusão precoce do aneurisma (< 24 a 72 horas) por Microembolização Endovascular ou Clipagem Microcirúrgica.",
                    }
                ],
            },
            {
                "id": "tier_vaso_yellow",
                "label": "Vasograde-Yellow: Risco Intermediário de DCI",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Incidência estimada de Isquemia Cerebral Tardia (DCI) de aproximadamente 30% a 35%. Alta taxa de vasoespasmo angiográfico.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_vaso_norepi_yellow",
                        "drugName": "Noradrenalina IV (Preparo para Hipertensão Induzida)",
                        "dosage": "Titulada para PAS 160-180 mmHg se surgir novo déficit focal isquêmico PÓS-exclusão mecânica do aneurisma",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "16 mg em 234 mL SG 5% (64 mcg/mL). CONTRAINDICADA ANTES da clipagem/embolização do aneurisma.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_vaso_yellow",
                        "recommendationTitle": "Caso Limítrofe / Vigilância Intensiva de Vasoespasmo com DTC Diário",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Doppler Transcraniano diário (a cada 12-24h). Velocidade média na ACM > 120 cm/s ou elevação > 50 cm/s/dia alerta para espasmo acelerado. Linha arterial invasiva (PAI).",
                        "interventionalProcedure": "Oclusão precoce do aneurisma em < 24h. Preparo de retaguarda para sala de hemodinâmica para angioplastia química superseletiva (Milrinona / Nicardipino) se refratariedade clínica.",
                    }
                ],
            },
            {
                "id": "tier_vaso_red",
                "label": "Vasograde-Red: Alto Risco de DCI e Mau Prognóstico",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Incidência de Isquemia Cerebral Tardia (DCI) de 40% a 50% e elevada mortalidade hospitalar (> 50-70%).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_vaso_norepi_red",
                        "drugName": "Noradrenalina IV para Manutenção de PAM e PPC",
                        "dosage": "0,05 a 2,0 mcg/kg/min",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "SG 5% 234 mL + 16 mg Noradrenalina. Meta pré-oclusão: PAS < 160 mmHg; Meta pós-oclusão perante DCI: PAS 160 a 180 mmHg.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_vaso_red",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: DVE Emergencial + Oclusão Mecânica do Aneurisma",
                        "dispositionTarget": "Centro Cirúrgico / Hemodinâmica",
                        "monitoringPlan": "Monitorização contínua de PIC e débito liquórico pela DVE (zeragem no tragus / forame de Monro).",
                        "interventionalProcedure": "Implantação emergencial de Derivação Ventricular Externa (DVE) à beira do leito para alívio de hidrocefalia aguda hipertensiva e lavagem liquórica, seguida de reavaliação clínica e oclusão urgente do aneurisma (prioritariamente endovascular).",
                        "ventilatorySupport": "Intubação orotraqueal em sequência rápida com proteção cervical e neuroproteção.",
                    }
                ],
            },
        ],
    }


def get_lawton_young():
    """Supplementary Spetzler-Martin System / Lawton-Young (Lawton et al. 2010)."""
    return {
        "id": "calc_lawton_young",
        "slug": "lawton-young",
        "name": "Sistema Lawton-Young / Spetzler-Martin Suplementar para MAVs",
        "acronym": "Lawton-Young",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Sistema de graduação cirúrgico que refina a escala de Spetzler-Martin através da adição de 3 variáveis independentes (idade, história de sangramento e compacidade do nidus), somando 2 a 10 pontos para determinar a segurança da ressecção microcirúrgica.",
        "summary": "Escore combinado de 2 a 10 pontos integrando Spetzler-Martin, idade, ruptura e compacidade do nidus de MAV.",
        "clinicalObjective": "Resolver a heterogeneidade da Classe B (Grau III) de Spetzler-Martin e predizer a morbimortalidade cirúrgica permanente com maior acurácia.",
        "targetPopulation": "Pacientes portadores de Malformações Arteriovenosas (MAVs) cerebrais parenquimatosas avaliadas por angiografia digital e ressonância magnética.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Spetzler_Martin (1-5) + Pontos_Idade (1-3) + Pontos_Ruptura (0-1) + Pontos_Compacidade (0-1)",
        "evidenceSource": "Lawton MT, Kim H, McCulloch CE, et al. A supplementary grading scale for selecting patients with brain arteriovenous malformations for surgery. Neurosurgery. 2010;66(4):702-713.",
        "minPossibleScore": 2,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "DIRETRIZ DO ENSAIO CLÍNICO ARUBA (Lancet 2014): Em MAVs não rotas com escore combinado elevado (Lawton-Young >= 7 pontos), o tratamento médico conservador é categoricamente superior à intervenção ativa, reduzindo em mais de 3 vezes o risco combinado de óbito ou novo AVC incapacitante. A microcirurgia aberta está formalmente contraindicada neste subgrupo.",
        "radarAxes": [
            {"id": "axis_ly_sm", "label": "Escore Spetzler-Martin Base", "system": "Anatômico", "unit": "grau", "baselineValue": 1, "maxAxisValue": 5},
            {"id": "axis_ly_age", "label": "Idade e Reserva Biológica", "system": "Biológico", "unit": "pts", "baselineValue": 1, "maxAxisValue": 3},
            {"id": "axis_ly_rupture", "label": "Status de Ruptura / Gliose", "system": "Clínico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_ly_compact", "label": "Arquitetura do Nidus", "system": "Anatômico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_ly_sm",
                "name": "1. Escore de Spetzler-Martin Clássico Base",
                "slug": "escore-sm-base",
                "inputType": "single_choice",
                "radarAxisId": "axis_ly_sm",
                "normalBaselineValue": 1,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Pontuação somada de Spetzler-Martin (Tamanho + Eloquência + Drenagem Profunda: 1 a 5).",
                "options": [
                    {"id": "opt_ly_sm_1", "label": "Spetzler-Martin Grau I (1 pt)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Pequena (<3 cm), não eloquente, drenagem superficial."},
                    {"id": "opt_ly_sm_2", "label": "Spetzler-Martin Grau II (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2, "description": "Pequena eloquente/profunda ou média não eloquente superficial."},
                    {"id": "opt_ly_sm_3", "label": "Spetzler-Martin Grau III (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3, "description": "Heterogênea: média eloquente/profunda ou grande não eloquente."},
                    {"id": "opt_ly_sm_4", "label": "Spetzler-Martin Grau IV (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4, "description": "Média/grande, eloquente com drenagem profunda."},
                    {"id": "opt_ly_sm_5", "label": "Spetzler-Martin Grau V (5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5, "description": "Grande (>6 cm), eloquente e com drenagem venosa profunda."},
                ],
            },
            {
                "id": "grp_ly_age",
                "name": "2. Idade Cronológica do Paciente",
                "slug": "idade-lawton",
                "inputType": "single_choice",
                "radarAxisId": "axis_ly_age",
                "normalBaselineValue": 1,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Idade cronológica (fator biológico independente de complacência cerebral).",
                "options": [
                    {"id": "opt_ly_age_lt20", "label": "Idade < 20 anos (1 pt)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Alta plasticidade neuronal e excelente tolerância tecidual cerebral."},
                    {"id": "opt_ly_age_20_40", "label": "Idade de 20 a 40 anos (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Reserva intermediária."},
                    {"id": "opt_ly_age_gt40", "label": "Idade > 40 anos (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Menor complacência tecidual, maior rigidez arterial e risco aumentado de déficits pós-operatórios."},
                ],
            },
            {
                "id": "grp_ly_bleed",
                "name": "3. História Prévia de Sangramento / Ruptura",
                "slug": "sangramento-previo-lawton",
                "inputType": "single_choice",
                "radarAxisId": "axis_ly_rupture",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Status de ruptura: sangramento prévio cria cavidade de hematoma facilitadora de clivagem.",
                "options": [
                    {"id": "opt_ly_bleed_yes", "label": "Nidus Roto: Hemorragia prévia documentada (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "O sangramento prévio forma cavidade cística gliótica que facilita a dissecção microcirúrgica perilesional."},
                    {"id": "opt_ly_bleed_no", "label": "Nidus Não-Roto: Descoberta incidental ou convulsão (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Cérebro viável normal intimamente aderido aos vasos do nidus, elevando o risco de infarto tecidual ressectivo."},
                ],
            },
            {
                "id": "grp_ly_compactness",
                "name": "4. Arquitetura e Compacidade do Nidus",
                "slug": "compacidade-nidus-lawton",
                "inputType": "single_choice",
                "radarAxisId": "axis_ly_compact",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Padrão de delimitação do enovelado vascular na angiografia e RM.",
                "options": [
                    {"id": "opt_ly_compact_yes", "label": "Nidus Compacto (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Nidus circunscrito e delimitado sem parênquima cerebral funcionante interposto."},
                    {"id": "opt_ly_compact_no", "label": "Nidus Difuso / Infiltrativo (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Vasos patológicos entremeados por parênquima cerebral normal funcionante; alto risco de déficit definitivo."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_ly_low",
                "label": "Baixa Complexidade Cirúrgica (2 a 4 pontos)",
                "severityLevel": "low",
                "minScore": 2,
                "maxScore": 4,
                "statisticalOutcome": "Morbidade cirúrgica permanente < 3% a 5%. Taxa de obliteração cirúrgica completa imediata > 95% a 98%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ly_keppra",
                        "drugName": "Levetiracetam (Profilaxia Anticonvulsivante Perioperatória)",
                        "dosage": "500 a 1.000 mg VO ou IV 12/12h",
                        "route": "Oral / Intravenosa",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Infundir em 15 min se IV.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ly_low",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Eletiva de Microcirurgia Ressectiva Primária",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Angiografia digital pós-operatória imediata para confirmar exclusão anatômica completa do nidus. Controle estrito de PAS < 120-130 mmHg no pós-operatório (prevenção de NPPB).",
                        "interventionalProcedure": "Craniotomia guiada por neuronavegação com dissecção microcirúrgica circunferencial pial, ligadura progressiva dos pedículos arteriais nutridores e sacrifício final da veia de drenagem.",
                    }
                ],
            },
            {
                "id": "tier_ly_mod",
                "label": "Complexidade Intermediária (5 a 6 pontos)",
                "severityLevel": "intermediate",
                "minScore": 5,
                "maxScore": 6,
                "statisticalOutcome": "Taxa de novos déficits permanentes pós-operatórios de 10% a 25%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ly_nipride",
                        "drugName": "Nitroprussiato de Sódio em BIC (Protocolo Anti-Hiperemia NPPB)",
                        "dosage": "0,25 a 5,0 mcg/kg/min",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua pós-operatória",
                        "dilutionInstructions": "SG 5% 248 mL + 50 mg Nipride com equipo fotoprotetor. Manter PAS < 120 mmHg por 48-72h para evitar sangramento por quebra da pressão de perfusão normal.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ly_mod",
                        "recommendationTitle": "Caso Limítrofe / Planejamento Terapêutico Multimodal Individualizado",
                        "dispositionTarget": "UTI Neurocrítica / Hemodinâmica",
                        "monitoringPlan": "Discussão multidisciplinar (neurocirurgião vascular, intervencionista e radioterapeuta).",
                        "interventionalProcedure": "Embolização endovascular superseletiva prévia estagiada com Onyx/Squid para oclusão de pedículos profundos perigosos seguida de microcirurgia OU Radiocirurgia Estereotática (SRS: 18 a 22 Gy) se nidus < 3 cm.",
                    }
                ],
            },
            {
                "id": "tier_ly_high",
                "label": "Alta Complexidade / Risco Proibitivo (7 a 10 pontos)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 10,
                "statisticalOutcome": "Risco de morbidade cirúrgica permanente grave ou óbito superior a 35% a 50%. O risco da intervenção cirúrgica supera expressivamente a história natural de rotura.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ly_anticonv",
                        "drugName": "Controle Farmacológico Clínico Rigoroso",
                        "dosage": "Levetiracetam ou Lamotrigina para controle de crises epilépticas",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Controle pressórico estrito com anti-hipertensivos orais visando PAS < 130 mmHg.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ly_high",
                        "recommendationTitle": "Tratamento Conservador Seguro / Manejo Clínico Expectante (Ensaio ARUBA)",
                        "dispositionTarget": "Ambulatório Neurovascular",
                        "monitoringPlan": "Acompanhamento clínico regular, cessação de tabagismo e controle rigoroso de PA. RM e angio-RM a cada 2 a 3 anos.",
                        "interventionalProcedure": "Microcirurgia aberta formalmente contraindicada. Intervenção cirúrgica reservada estritamente para evacuação emergencial de hematoma com risco iminente de morte.",
                    }
                ],
            },
        ],
    }


def get_zabramski():
    """Classificação de Zabramski para Malformações Cavernosas Cerebrais (Zabramski et al. 1994)."""
    return {
        "id": "calc_zabramski",
        "slug": "zabramski",
        "name": "Classificação de Zabramski para Cavernomas Cerebrais",
        "acronym": "Zabramski",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Classificação morfológica e evolutiva das malformações cavernosas (cavernomas) cerebrais baseada no padrão de sinal da Ressonância Magnética (T1, T2 e SWI/gradiente-eco), determinando o risco de ressangramento e a indicação de ressecção microcirúrgica.",
        "summary": "Estadiamento morfológico por ressonância magnética dos cavernomas encefálicos em 4 tipos.",
        "clinicalObjective": "Identificar lesões ativas com alto risco de ressangramento, alertar para formas familiares múltiplas e guiar a decisão entre microcirurgia, ressecção do anel de hemossiderina e conduta expectante.",
        "targetPopulation": "Pacientes portadores de angiomas cavernosos intracranianos supratentoriais, infratentoriais ou de tronco encefálico.",
        "calculationType": "branching_decision",
        "formulaExpression": "Tipo Morfológico Zabramski (I a IV) determinado por RM",
        "evidenceSource": "Zabramski JM, Wascher TM, Spetzler RF, et al. The natural history of familial cavernous malformations: results of an ongoing study. J Neurosurg. 1994;80(3):422-432.",
        "minPossibleScore": 1,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ALERTA DE SEGURANÇA MÁXIMA: (1) Preservação da Anomalia de Desenvolvimento Venoso (DVA): É terminantemente proibida a coagulação ou sacrifício da veia de drenagem anômala associada ao cavernoma pelo risco crítico de infarto venoso hemorrágico catastrófico. (2) Contraindicação a Radiocirurgia no Tipo IV familiar: A radiocirurgia é formalmente contraindicada pela indução acelerada de lesões cavernosas de novo.",
        "radarAxes": [
            {"id": "axis_zab_bleed", "label": "Atividade Hemorrágica", "system": "Vascular", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_zab_epilepsy", "label": "Epileptogenicidade (Anel Hemossiderina)", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_zab_familiar", "label": "Carga de Lesões / Genética", "system": "Genético", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_zabramski_type",
                "name": "Tipo Morfológico Zabramski (Padrão de Sinal na RM)",
                "slug": "tipo-zabramski",
                "inputType": "single_choice",
                "radarAxisId": "axis_zab_bleed",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Padrão das sequências T1, T2 e T2* / SWI na ressonância magnética.",
                "options": [
                    {
                        "id": "opt_zab_1",
                        "label": "Tipo I: Hemorragia Subaguda Recente",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 1,
                        "description": "T1 hiperintenso central, T2 hiperintenso com halo hipointenso (metemoglobina subaguda recente intra-lesional). Alto risco de ressangramento iminente.",
                    },
                    {
                        "id": "opt_zab_2",
                        "label": "Tipo II: Lesão Clássica em Pipoca (Popcorn Lesion)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.8,
                        "sortOrder": 2,
                        "description": "T1 e T2 mistos reticulados ('aspecto em pipoca') com espesso halo periférico de hemossiderina. Tromboses e neovasos em diferentes estágios.",
                    },
                    {
                        "id": "opt_zab_3",
                        "label": "Tipo III: Depósito Crônico Inativo de Hemossiderina",
                        "pointValue": 3,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.2,
                        "sortOrder": 3,
                        "description": "T1 e T2 marcadamente hipointensos homogêneos. Lesão trombosada antiga cicatrizada, sem atividade hemorrágica recente.",
                    },
                    {
                        "id": "opt_zab_4",
                        "label": "Tipo IV: Micro-hemorragias Múltiplas / Forma Familiar",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 4,
                        "description": "Lesões puntiformes minúsculas 'em cabeça de alfinete' visíveis apenas em gradiente-eco/SWI (marcador patognomônico de mutações CCM1, CCM2 ou CCM3).",
                    },
                ],
            }
        ],
        "riskTiers": [
            {
                "id": "tier_zab_active",
                "label": "Tipos I e II: Lesões Ativas Sintomáticas",
                "severityLevel": "high",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de ressangramento espontâneo de 4% a 10% ao ano (em lesões de tronco encefálico que já sangraram, o risco pode atingir 15% a 30% ao ano).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_zab_keppra",
                        "drugName": "Levetiracetam Oral",
                        "dosage": "500 a 1.000 mg VO 12/12h",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Droga de primeira linha para controle de crises epilépticas associadas ao anel de hemossiderina.",
                        "contraindications": "Evitar uso não essencial de anticoagulantes plenos.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_zab_surgery",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Eletiva de Ressecção Microcirúrgica Completa",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Monitorização neurofisiológica intraoperatória contínua (potenciais evocados motores/somatossensoriais e pares cranianos se tronco).",
                        "interventionalProcedure": "Ressecção microscópica completa do nidus cavernoso associada à remoção circunferencial do anel gliótico de hemossiderina (hemosiderin rim resection) para controle de epilepsia. Preservar estritamente qualquer DVA associada.",
                    }
                ],
            },
            {
                "id": "tier_zab_inactive",
                "label": "Tipo III: Lesão Inativa Estável",
                "severityLevel": "low",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Risco de sangramento espontâneo muito baixo (< 0,5% a 1% ao ano).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_zab_obs",
                        "drugName": "Manejo Sintomático Conservador",
                        "dosage": "Analgesia simples para cefaleia eventual",
                        "route": "Oral",
                        "frequency": "Se necessário",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_zab_conservative",
                        "recommendationTitle": "Tratamento Conservador Seguro / Seguimento por Imagem",
                        "dispositionTarget": "Ambulatório de Neurocirurgia",
                        "monitoringPlan": "Ressonância magnética de encéfalo a cada 12 a 24 meses. Orientar procura imediata perante novo déficit neurológico focal.",
                        "interventionalProcedure": "Cirurgia não indicada.",
                    }
                ],
            },
            {
                "id": "tier_zab_familiar",
                "label": "Tipo IV: Cavernomatose Múltipla Familiar",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Desenvolvimento dinâmico de novas lesões de novo ao longo da vida com padrão de herança autossômica dominante.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_zab_fam_aed",
                        "drugName": "Antiepilépticos de Manutenção (Levetiracetam / Lacosamida)",
                        "dosage": "Titulado conforme controle clínico e EEG",
                        "route": "Oral",
                        "frequency": "12/12h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_zab_familiar",
                        "recommendationTitle": "Caso Limítrofe / Aconselhamento Genético e Cirurgia Estritamente Seletiva",
                        "dispositionTarget": "Ambulatório Especializado de Neurogenética",
                        "monitoringPlan": "Rastreio genético molecular (painel CCM1/KRIT1, CCM2, CCM3/PDCD10) e triagem de familiares de primeiro grau. RM com SWI seriada a cada 1 a 2 anos.",
                        "interventionalProcedure": "Cirurgia aberta reservada exclusivamente para a lesão índice que sangrou de forma sintomática com efeito de massa ou causou déficit focal progressivo. PROIBIDA RADIOCIRURGIA.",
                    }
                ],
            },
        ],
    }


def get_phases_score():
    """PHASES Aneurysm Rupture Risk Score (Greving et al., Lancet Neurol 2014)."""
    return {
        "id": "calc_phases_score",
        "slug": "phases-score",
        "name": "PHASES Score para Predição de Ruptura de Aneurisma Cerebral",
        "acronym": "PHASES",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Calculadora prognóstica de risco absoluto de ruptura em 5 anos para aneurismas saculares intracranianos não rotos incidentais, baseada em meta-análise com mais de 8.300 pacientes e 6 variáveis clínicas e anatômicas.",
        "summary": "Predição da probabilidade percentual de ruptura em 5 anos de aneurismas cerebrais não rotos (0 a 22 pontos).",
        "clinicalObjective": "Quantificar a probabilidade da história natural de ruptura espontânea do aneurisma para orientar a indicação de intervenção profilática (clipagem ou embolização) versus conduta expectante.",
        "targetPopulation": "Pacientes portadores de aneurismas intracranianos saculares não rotos descobertos incidentalmente ou durante investigação de cefaleia.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Populacao + Pontos_Hipertensao + Pontos_Idade + Pontos_Tamanho + Pontos_HSA_Previa + Pontos_Localizacao",
        "evidenceSource": "Greving JP, Wermer MJ, Brown RD Jr, et al. Development of the PHASES score for prediction of risk of rupture of intracranial aneurysms: a pooled analysis of six prospective cohort studies. Lancet Neurol. 2014;13(1):59-66.",
        "minPossibleScore": 0,
        "maxPossibleScore": 22,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ATENÇÃO: Aneurismas localizados na artéria comunicante anterior (ACoA), comunicante posterior (PCoA) e na circulação vértebro-basilar apresentam pontuação máxima de sítio vascular (+4 pontos) devido ao estresse hemodinâmico crítico de cisalhamento. Aneurismas >= 10 mm ou de rápido crescimento (> 1 mm/ano) possuem risco anual desproporcionalmente elevado.",
        "radarAxes": [
            {"id": "axis_ph_morphology", "label": "Tamanho do Aneurisma", "system": "Anatômico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 10},
            {"id": "axis_ph_site", "label": "Localização Vascular", "system": "Anatômico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_ph_demographic", "label": "Idade e População", "system": "Demográfico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 5},
            {"id": "axis_ph_clinical", "label": "Hipertensão e HSA Prévia", "system": "Clínico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 2},
        ],
        "parameterGroups": [
            {
                "id": "grp_phases_pop",
                "name": "1. P - População / Origem Geográfica",
                "slug": "populacao-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_demographic",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "País ou grupo étnico de origem do paciente.",
                "options": [
                    {"id": "opt_ph_pop_west", "label": "Brasil, América do Norte, Europa Central ou outros países ocidentais (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "População ocidental de risco basal padrão."},
                    {"id": "opt_ph_pop_japan", "label": "Japão (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 2, "description": "Incidência elevada de rotura aneurismática documentada."},
                    {"id": "opt_ph_pop_finland", "label": "Finlândia (5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Maior taxa populacional de HSA por aneurisma do mundo."},
                ],
            },
            {
                "id": "grp_phases_htn",
                "name": "2. H - Hipertensão Arterial Sistêmica",
                "slug": "hipertensao-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_clinical",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Diagnóstico documentado de hipertensão arterial sistêmica.",
                "options": [
                    {"id": "opt_ph_htn_no", "label": "Normotenso / Sem diagnóstico de HAS (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "PA normal sem uso de medicação anti-hipertensiva."},
                    {"id": "opt_ph_htn_yes", "label": "Hipertenso diagnosticado / Em tratamento (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Hipertensão aumenta tensão de cisalhamento sobre a parede aneurismática."},
                ],
            },
            {
                "id": "grp_phases_age",
                "name": "3. A - Idade Cronológica (Age)",
                "slug": "idade-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_demographic",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Idade cronológica no momento da avaliação.",
                "options": [
                    {"id": "opt_ph_age_lt70", "label": "Idade < 70 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Expectativa de vida longa, menor fragilidade vascular."},
                    {"id": "opt_ph_age_ge70", "label": "Idade >= 70 anos (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Aterosclerose e fragilidade da túnica média."},
                ],
            },
            {
                "id": "grp_phases_size",
                "name": "4. S - Tamanho Máximo do Aneurisma (Size)",
                "slug": "tamanho-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_morphology",
                "normalBaselineValue": 0,
                "maxAxisValue": 10,
                "sortOrder": 4,
                "helpText": "Maior diâmetro linear da cúpula aneurismática na angiotomografia ou RM.",
                "options": [
                    {"id": "opt_ph_size_lt7", "label": "Tamanho < 7,0 mm (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Aneurisma pequeno; baixo risco anual de sangramento."},
                    {"id": "opt_ph_size_7_9", "label": "Tamanho de 7,0 a 9,9 mm (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.3, "sortOrder": 2, "description": "Aneurisma de médio porte; risco moderado."},
                    {"id": "opt_ph_size_10_19", "label": "Tamanho de 10,0 a 19,9 mm (6 pts)", "pointValue": 6, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 3, "description": "Aneurisma volumoso; taxa acelerada de rotura espontânea."},
                    {"id": "opt_ph_size_ge20", "label": "Tamanho >= 20,0 mm (Aneurisma Gigante) (10 pts)", "pointValue": 10, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Aneurisma gigante; risco crítico cumulativo de sangramento e efeito de massa."},
                ],
            },
            {
                "id": "grp_phases_earlier_sah",
                "name": "5. E - História Prévia de HSA (Earlier SAH)",
                "slug": "hsa-previa-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_clinical",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Hemorragia subaracnóidea prévia comprovada decorrente de outro aneurisma tratado.",
                "options": [
                    {"id": "opt_ph_earlier_no", "label": "Sem história prévia de HSA aneurismática (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem evento hemorrágico prévio no SNC."},
                    {"id": "opt_ph_earlier_yes", "label": "História prévia de HSA por outro aneurisma tratado (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Evidência biológica de fragilidade congênita da lâmina elástica arterial."},
                ],
            },
            {
                "id": "grp_phases_site",
                "name": "6. S - Sítio Anatômico / Localização Vascular (Site)",
                "slug": "localizacao-phases",
                "inputType": "single_choice",
                "radarAxisId": "axis_ph_site",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 6,
                "helpText": "Artéria de origem e segmento vascular em que o aneurisma se desenvolve.",
                "options": [
                    {"id": "opt_ph_site_ica", "label": "Artéria Carótida Interna (segmento cavernoso/oftálmico) (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Menor tensão de ruptura na circulação anterior proximal."},
                    {"id": "opt_ph_site_mca", "label": "Artéria Cerebral Média (ACM) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Bifurcação ou trifurcação da ACM."},
                    {"id": "opt_ph_site_post", "label": "ACoA, PCoA ou Circulação Posterior (Basilar, Vertebral, PICA) (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Sítios de altíssimo estresse hemodinâmico com máxima taxa de rotura."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_phases_low",
                "label": "Baixo Risco de Ruptura (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Probabilidade estimada de ruptura em 5 anos de 0,4% a 0,7% (risco anual < 0,1% a 0,15%/ano).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ph_bp_control",
                        "drugName": "Controle Pressórico com IECA / BRA",
                        "dosage": "Enalapril 10-20 mg/dia ou Losartana 50-100 mg/dia",
                        "route": "Oral",
                        "frequency": "12/12h ou 24/24h",
                        "dilutionInstructions": "Manter meta pressórica ambulatorial estrita de PAS < 130 mmHg e PAD < 80 mmHg.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ph_conservative",
                        "recommendationTitle": "Tratamento Conservador Seguro / Seguimento por Imagem",
                        "dispositionTarget": "Ambulatório Neurovascular",
                        "monitoringPlan": "Cessação mandatória do tabagismo. Angio-TC ou Angio-RM sem contraste anual; se estabilidade dimensional após 2 anos, espaçar para a cada 2 a 3 anos.",
                        "interventionalProcedure": "Tratamento cirúrgico ou endovascular contraindicado no momento (risco procedimental supera a história natural).",
                    }
                ],
            },
            {
                "id": "tier_phases_mod",
                "label": "Risco Intermediário (4 a 7 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 7,
                "statisticalOutcome": "Probabilidade estimada de ruptura em 5 anos de 0,9% (pontuação 4) a 4,3% (pontuação 7).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ph_smoking",
                        "drugName": "Apoio Farmacológico à Cessação Tabágica",
                        "dosage": "Adesivo de Nicotina transdérmico 14-21 mg/dia ou Bupropiona 150 mg 12/12h",
                        "route": "Transdérmica / Oral",
                        "frequency": "24/24h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ph_shared",
                        "recommendationTitle": "Caso Limítrofe / Tomada de Decisão Compartilhada",
                        "dispositionTarget": "Ambulatório Especializado",
                        "monitoringPlan": "Avaliar fatores adicionais: multilobulação da cúpula, presença de daughter sacs, proporção de aspecto Aspect Ratio > 1,6, idade e expectativa de vida do paciente.",
                        "interventionalProcedure": "Se paciente jovem com expectativa > 25 anos, cúpula irregular ou crescimento documentado na imagem: indicar tratamento ativo profilático.",
                    }
                ],
            },
            {
                "id": "tier_phases_high",
                "label": "Alto a Muito Alto Risco de Ruptura (8 a 22 pontos)",
                "severityLevel": "critical",
                "minScore": 8,
                "maxScore": 22,
                "statisticalOutcome": "Probabilidade de ruptura em 5 anos de 5,3% (pontuação 8) até > 17,8% (pontuação >= 12); em aneurismas gigantes de circulação posterior pode exceder 30% a 40%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ph_dapt",
                        "drugName": "Dupla Antiagregação Plaquetária (Se Indicação de Stent / Diversor de Fluxo)",
                        "dosage": "AAS 100 mg/dia + Clopidogrel 75 mg/dia ou Ticagrelor 90 mg 12/12h",
                        "route": "Oral",
                        "frequency": "24/24h",
                        "dilutionInstructions": "Iniciar 7 a 10 dias antes do procedimento endovascular programado.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_ph_active",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Tratamento Intervencionista Eletivo Ativo",
                        "dispositionTarget": "Centro Cirúrgico / Hemodinâmica Eletiva",
                        "monitoringPlan": "Preparo pré-operatório eletivo programado.",
                        "interventionalProcedure": "Exclusão mecânica ativa: (1) Clipagem Microcirúrgica Eletiva de escolha para bifurcação da ACM e aneurismas de colo largo com ramos arteriais emergentes do colo; (2) Embolização Endovascular com micromolas ou implante de Stent Diversor de Fluxo (Flow Diverter) para carótida paraclinoideia e topo de basilar.",
                    }
                ],
            },
        ],
    }


def get_uiats():
    """Unruptured Intracranial Aneurysm Treatment Score (Etminan et al. 2015)."""
    return {
        "id": "calc_uiats",
        "slug": "uiats",
        "name": "UIATS - Escore de Decisão Terapêutica em Aneurismas Não Rotos",
        "acronym": "UIATS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Algoritmo internacional multidisciplinar ponderado de 29 variáveis que calcula a diferença líquida de pontos entre tratamento intervencionista ativo e manejo conservador expectante em aneurismas intracranianos saculares não rotos.",
        "summary": "Algoritmo quantitativo diferencial que direciona tratamento ativo vs conduta expectante em aneurismas não rotos.",
        "clinicalObjective": "Orientar a decisão clínica multidisciplinar em aneurismas incidentais não rotos ponderando riscos do tratamento versus história natural de ruptura.",
        "targetPopulation": "Pacientes com diagnóstico angiográfico ou tomográfico de aneurisma cerebral sacular não roto.",
        "calculationType": "additive_points",
        "formulaExpression": "Diferença Líquida = Pontos a Favor do Tratamento Ativo - Pontos a Favor do Manejo Conservador",
        "evidenceSource": "Etminan N, Brown RD Jr, Beseoglu K, et al. The unruptured intracranial aneurysm treatment score: a multidisciplinary consensus. Neurology. 2015;85(10):881-889.",
        "minPossibleScore": -10,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ATENÇÃO: Quando a diferença líquida de pontos do UIATS situa-se na zona neutra (entre -2 e +2 pontos), há equilíbrio clínico estrito (equipoise) entre o risco do procedimento e o risco da história natural. Recomenda-se controle rigoroso de PA, cessação de tabagismo e reavaliação tomográfica seriada em 6 meses.",
        "radarAxes": [
            {"id": "axis_uiats_balance", "label": "Balanço Diferencial de Pontos", "system": "Decisão", "unit": "pts", "baselineValue": 0, "maxAxisValue": 5},
            {"id": "axis_uiats_patient", "label": "Fatores do Paciente", "system": "Clínico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_uiats_aneurysm", "label": "Morfologia e Sítio", "system": "Anatômico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_uiats_diff",
                "name": "Balanço Diferencial Líquido do UIATS",
                "slug": "balanco-diferencial-uiats",
                "inputType": "single_choice",
                "radarAxisId": "axis_uiats_balance",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Diferença calculada: Pontos a favor da intervenção MENOS Pontos a favor do conservador.",
                "options": [
                    {
                        "id": "opt_uiats_diff_le_minus3",
                        "label": "Diferença Líquida <= -3 pontos (Favorece Manejo Conservador)",
                        "pointValue": -3,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "O risco da intervenção cirúrgica ou endovascular supera expressivamente o risco cumulativo de sangramento natural ao longo da vida do paciente.",
                    },
                    {
                        "id": "opt_uiats_diff_neutral",
                        "label": "Diferença Líquida entre -2 e +2 pontos (Zona Neutra / Indeterminada)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Equilíbrio clínico entre riscos e benefícios. Decisão compartilhada e vigilância radiológica em 6 meses.",
                    },
                    {
                        "id": "opt_uiats_diff_ge_plus3",
                        "label": "Diferença Líquida >= +3 pontos (Favorece Tratamento Ativo)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "O risco acumulado de rotura do aneurisma excede claramente a morbimortalidade do tratamento cirúrgico ou endovascular.",
                    },
                ],
            }
        ],
        "riskTiers": [
            {
                "id": "tier_uiats_conservative",
                "label": "Favorece Tratamento Conservador Seguro (Diferença <= -3)",
                "severityLevel": "low",
                "minScore": -10,
                "maxScore": -3,
                "statisticalOutcome": "O risco associado à clipagem microcirúrgica ou à embolização excede o risco cumulativo de ruptura natural. Sobrevida livre de morbidade favorável sob manejo conservador.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_uiats_conservative",
                        "drugName": "Manejo Clínico de Fatores de Risco Modificáveis",
                        "dosage": "Anti-hipertensivo oral para PAS < 130 mmHg",
                        "route": "Oral",
                        "frequency": "24/24h",
                        "dilutionInstructions": "Cessação absoluta de tabagismo.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_uiats_conservative",
                        "recommendationTitle": "Tratamento Conservador Seguro de Escolha",
                        "dispositionTarget": "Ambulatório Neurovascular",
                        "monitoringPlan": "Angio-TC ou Angio-RM seriada a cada 12 meses nos primeiros 2 a 3 anos; se estável, a cada 2 a 5 anos.",
                        "interventionalProcedure": "Cirurgia ou embolização contraindicada.",
                    }
                ],
            },
            {
                "id": "tier_uiats_neutral",
                "label": "Zona Indeterminada / Decisão Compartilhada (Diferença -2 a +2)",
                "severityLevel": "intermediate",
                "minScore": -2,
                "maxScore": 2,
                "statisticalOutcome": "Equipoise clínico estrito entre tratamento ativo e manejo conservador expectante.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_uiats_neutral",
                        "drugName": "Otimização Hemodinâmica Ambulatorial",
                        "dosage": "Controle rigoroso de pressão arterial e dislipidemia",
                        "route": "Oral",
                        "frequency": "24/24h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_uiats_neutral",
                        "recommendationTitle": "Caso Limítrofe / Tomada de Decisão Compartilhada e Imagem em Curto Prazo",
                        "dispositionTarget": "Ambulatório Especializado",
                        "monitoringPlan": "Avaliar ansiedade do paciente, sintomas compressivos locais e presença de histórico familiar de rotura. Repetir angio-TC em intervalo curto (6 meses).",
                        "interventionalProcedure": "Se crescimento >= 1 mm documentado em neuroimagem: indicar tratamento ativo imediato.",
                    }
                ],
            },
            {
                "id": "tier_uiats_active",
                "label": "Favorece Tratamento Ativo: Clipagem ou Embolização (Diferença >= +3)",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 10,
                "statisticalOutcome": "O risco cumulativo de ruptura espontânea do aneurisma supera expressivamente os riscos procedimentais de morbimortalidade.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_uiats_dapt",
                        "drugName": "Dupla Antiagregação Plaquetária (Se indicação de Stent / Diversor)",
                        "dosage": "AAS 100 mg + Clopidogrel 75 mg/dia por 7 a 10 dias pré-procedimento",
                        "route": "Oral",
                        "frequency": "24/24h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_uiats_active",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Tratamento Ativo Programado",
                        "dispositionTarget": "Centro Cirúrgico / Hemodinâmica Eletiva",
                        "monitoringPlan": "Preparo pré-operatório eletivo neurovascular.",
                        "interventionalProcedure": "Exclusão mecânica definitiva: Clipagem Microcirúrgica Aberta de escolha para aneurismas com colo largo e bifurcação de ACM; Oclusão Endovascular com micromolas ou stent diversor de fluxo para carótida interna e circulação posterior.",
                    }
                ],
            },
        ],
    }


def get_cognard_borden():
    """Classificação Angiográfica de Cognard e Borden para FAVDs (Borden 1995; Cognard 1995)."""
    return {
        "id": "calc_cognard_borden",
        "slug": "cognard-borden",
        "name": "Classificação de Cognard e Borden para Fístulas Arteriovenosas Durais",
        "acronym": "Cognard-Borden",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular & Aneurismas",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurocirurgia Vascular e Aneurismas",
        "description": "Dupla classificação angiográfica padrão-ouro para fístulas arteriovenosas durais (FAVDs) encefálicas que correlaciona a drenagem venosa cortical retrógrada (Cortical Venous Drainage - CVD) com o risco anual de hemorragia intracraniana catastrófica e déficit neurológico focal.",
        "summary": "Estratificação angiográfica combinada de Borden (I a III) e Cognard (I a V) para FAVDs cerebrais.",
        "clinicalObjective": "Identificar refluxo venoso cortical retrógrado (CVD) para indicar oclusão cirúrgica ou endovascular emergencial e prevenir hemorragia intracraniana.",
        "targetPopulation": "Pacientes com diagnóstico angiográfico de fístula arteriovenosa dural intracraniana.",
        "calculationType": "branching_decision",
        "formulaExpression": "Tipo Combinado Borden e Cognard avaliado em Angiografia Cerebral de 6 Vasos",
        "evidenceSource": "Borden JA, Wu JK, Shucart WA. A proposed classification for spinal and cranial dural arteriovenous fistulous malformations and radicular dural arteriovenous fistulas. J Neurosurg. 1995;82(2):166-179. Cognard C, Gobin YP, Pierot L, et al. Cerebral dural arteriovenous fistulas: clinical and angiographic correlation with a revision of the Borden classification. Radiology. 1995;194(3):671-680.",
        "minPossibleScore": 1,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ALERTA PRETO DE EMERGÊNCIA NEUROVASCULAR: A presença de Drenagem Venosa Cortical Retrógrada (CVD / Cortical Venous Reflux presente em Borden II-III e Cognard IIb a V) transforma a fístula em lesão maligna/agressiva com risco anual de sangramento de até 65%, impondo tratamento cirúrgico ou endovascular de urgência. Em contraste, lesões sem CVD (Borden I / Cognard I) possuem curso benigno e não sangram.",
        "radarAxes": [
            {"id": "axis_cb_cvd", "label": "Refluxo Venoso Cortical (CVD)", "system": "Vascular", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_cb_hemorrhage", "label": "Risco Hemorrágico Anual", "system": "Vascular", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_cb_ectasia", "label": "Ectasia Venosa Varicosa", "system": "Anatômico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_cognard_borden_type",
                "name": "Padrão de Drenagem Venosa na Angiografia",
                "slug": "padrao-drenagem-favd",
                "inputType": "single_choice",
                "radarAxisId": "axis_cb_cvd",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Padrão anatômico e direcional do fluxo venoso da FAVD em angiografia digital de 6 vasos.",
                "options": [
                    {
                        "id": "opt_cb_type1",
                        "label": "Borden Tipo I / Cognard Tipo I e IIa: Drenagem Sinusal Anterógrada SEM Refluxo Cortical (CVD ausente)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Drenagem direta para seio venoso dural sem refluxo para veias corticais piais. Risco de sangramento < 1-2% ao ano (comportamento benigno).",
                    },
                    {
                        "id": "opt_cb_type2",
                        "label": "Borden Tipo II / Cognard Tipo IIb e IIa+b: Drenagem para Seio Dural COM Refluxo Cortical Retrógrado (CVD presente)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.4,
                        "sortOrder": 2,
                        "description": "Estenose ou trombose do seio forçando o refluxo venoso retrógrado para veias corticais. Risco de sangramento anual de 10% a 24%.",
                    },
                    {
                        "id": "opt_cb_type3",
                        "label": "Borden Tipo III / Cognard Tipo III: Drenagem Cortical Direta Pura (Sem drenagem sinusal)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.7,
                        "sortOrder": 3,
                        "description": "Drenagem exclusiva para veias corticais sem ectasia varicosa. Risco de hemorragia intracraniana anual de aproximadamente 40%.",
                    },
                    {
                        "id": "opt_cb_type4",
                        "label": "Cognard Tipo IV: Drenagem Cortical Direta COM Ectasia Venosa Varicosa (> 5 mm)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Presença de variz venosa dilatada (> 5 mm ou > 3x o calibre da veia). Risco crítico de hemorragia maciça de aproximadamente 65% a 66%.",
                    },
                    {
                        "id": "opt_cb_type5",
                        "label": "Cognard Tipo V: Drenagem Venosa Perimedular Espinhal Descendente",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.9,
                        "sortOrder": 5,
                        "description": "Refluxo para as veias perimedulares espinhais cervicais ou torácicas com risco de mielopatia congestiva progressiva (Síndrome de Foix-Alajouanine).",
                    },
                ],
            }
        ],
        "riskTiers": [
            {
                "id": "tier_cb_benign",
                "label": "Lesão Benigna sem Refluxo Cortical (Borden I / Cognard I e IIa)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Risco anual de hemorragia intracraniana de 0% a 1%. Curso clínico benigno.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_cb_symptom",
                        "drugName": "Dipirona Monoidratada (Analgesia)",
                        "dosage": "1 g VO/IV a cada 6h se cefaleia",
                        "route": "Oral / Intravenosa",
                        "frequency": "6/6 horas se necessário",
                        "dilutionInstructions": "Diluir em 100 mL de SF 0,9% se administrado por via intravenosa lenta.",
                        "contraindications": "Hipersensibilidade conhecida a pirazolonas ou histórico de agranulocitose.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_cb_conservative",
                        "recommendationTitle": "Tratamento Conservador Seguro Inicial",
                        "dispositionTarget": "Ambulatório Neurovascular",
                        "monitoringPlan": "Acompanhamento clínico e angiográfico anual. Compressão carotídea externa manual orientada em casos de tinnitus pulsátil.",
                        "interventionalProcedure": "Intervenção invasiva reservada estritamente para pacientes com sintomas incapacitantes graves (tinnitus audível intolerável ou proptose/quemose em FAVD carotídeo-cavernosa).",
                    }
                ],
            },
            {
                "id": "tier_cb_intermediate",
                "label": "Risco Moderado a Alto: Refluxo Cortical Misto (Borden II / Cognard IIb)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Drenagem em seio dural associada a refluxo cortical retrógrado. Risco hemorrágico anual de aproximadamente 10% a 20%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_cb_int_control",
                        "drugName": "Controle Pressórico com Anti-hipertensivo Oral",
                        "dosage": "Anlodipino 5 mg ou Enalapril 10 mg VO 1x/dia",
                        "route": "Oral",
                        "frequency": "1 vez ao dia",
                        "dilutionInstructions": "Administrar por via oral com água.",
                        "contraindications": "Hipotensão arterial sintomática (PAS < 100 mmHg).",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_cb_int_eval",
                        "recommendationTitle": "Avaliação Endovascular Prioritária",
                        "dispositionTarget": "Enfermaria de Neurocirurgia / Angiografia",
                        "monitoringPlan": "Angiografia cerebral diagnóstica superseletiva por cateterismo transfemoral/transradial.",
                        "interventionalProcedure": "Programação de embolização transarterial ou transvenosa eletiva rápida.",
                    }
                ],
            },
            {
                "id": "tier_cb_aggressive",
                "label": "Lesão Maligna com Drenagem Cortical Direta / Ectasia / Medular (Borden III / Cognard III a V)",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Risco de hemorragia intracraniana de 30% a 66% ao ano e risco severo de déficit neurológico permanente ou hipertensão venosa medular.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_cb_urgent",
                        "drugName": "Nitroprussiato de Sódio / Esmolol",
                        "dosage": "Titulação contínua em BIC para PAS < 120 mmHg e PAM 65-80 mmHg",
                        "route": "Intravenosa",
                        "frequency": "Infusão contínua em BIC",
                        "dilutionInstructions": "Proteger equipo com capa fotoprotetora; diluir estritamente em SG 5%.",
                        "contraindications": "Insuficiência renal grave (risco de intoxicação por tiocianato) ou hipotensão basal.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_cb_urgent",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Tratamento Intervencionista de Urgência",
                        "dispositionTarget": "Centro Cirúrgico / Hemodinâmica de Urgência",
                        "monitoringPlan": "Internação em leito de monitorização intensiva e angiografia terapêutica urgente.",
                        "interventionalProcedure": "Oclusão completa do pé da veia de drenagem cortical: (1) Embolização transarterial superseletiva com polímero precipitante não absorvível (Onyx, Squid ou Phil) ou embolização transvenosa do seio; (2) Desconexão Microcirúrgica Aberta simples através de craniotomia focada e coagulação/clipagem bipolar do pé da veia na sua emergência dural se embolização for incompleta ou inviável.",
                    }
                ],
            },
        ],
    }
