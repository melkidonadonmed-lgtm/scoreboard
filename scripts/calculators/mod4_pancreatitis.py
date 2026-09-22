"""
Module 04: Emergency Gastroenterology - Acute Pancreatitis
- Critérios de Ranson
- Escore BISAP
- Escore de Balthazar e CTSI
- Escore de Marshall Modificado
"""

def get_ranson():
    return {
        "id": "calc_ranson",
        "slug": "ranson-criteria",
        "name": "Critérios de Ranson para Pancreatite Aguda",
        "acronym": "Ranson",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Pancreatite Aguda de Emergência",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Pancreatite Aguda de Emergência",
        "description": "Estratificação bifásica de gravidade e necrose na pancreatite aguda avaliada na admissão (0h) e após 48 horas de internação.",
        "summary": "Estratificação bifásica (admissão e 48 horas) de gravidade e risco de necrose pancreática/mortalidade.",
        "clinicalObjective": "Predição prognóstica precoce de necrose pancreática e mortalidade intra-hospitalar na pancreatite aguda.",
        "targetPopulation": "Adultos com diagnóstico confirmado de pancreatite aguda (dor abdominal + lipase/amilase >= 3x o limite superior).",
        "calculationType": "additive_points",
        "formulaExpression": "Soma de 11 critérios (5 na admissão + 6 em 48 horas)",
        "evidenceSource": "Ranson JH, Rifkind KM, Roses DF, et al. Prognostic signs and the role of operative management in acute pancreatitis. Surg Gynecol Obstet. 1974;139(1):69-81.",
        "minPossibleScore": 0,
        "maxPossibleScore": 11,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_ran_adm", "label": "Admissão (0h)", "system": "Admissão", "baselineValue": 0, "maxAxisValue": 5},
            {"id": "axis_ran_48h", "label": "Evolução (48h)", "system": "48 Horas", "baselineValue": 0, "maxAxisValue": 6}
        ],
        "parameterGroups": [
            {
                "id": "grp_ran_age",
                "name": "1. Idade na Admissão (> 55 anos não biliar ou > 70 anos biliar)",
                "slug": "idade-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_adm",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_ran_age_no", "label": "Não (Abaixo do corte: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_age_yes", "label": "Sim (Acima do corte etário: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_leuko",
                "name": "2. Leucócitos na Admissão (> 16.000 não biliar ou > 18.000 biliar)",
                "slug": "leucocitos-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_adm",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_ran_leu_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_leu_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_glyc",
                "name": "3. Glicemia na Admissão (> 200 mg/dL não biliar ou > 220 mg/dL biliar)",
                "slug": "glicemia-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_adm",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_ran_gly_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_gly_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_ldh",
                "name": "4. LDH Sérico na Admissão (> 350 UI/L não biliar ou > 400 UI/L biliar)",
                "slug": "ldh-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_adm",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_ran_ldh_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_ldh_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_ast",
                "name": "5. AST / TGO na Admissão (> 250 UI/L)",
                "slug": "ast-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_adm",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_ran_ast_no", "label": "Não (AST <= 250 UI/L: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_ast_yes", "label": "Sim (AST > 250 UI/L: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_hct",
                "name": "6. Queda do Hematócrito > 10% nas primeiras 48h",
                "slug": "queda-hematocrito",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "options": [
                    {"id": "opt_ran_hct_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_hct_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_bun",
                "name": "7. Aumento do BUN > 5 mg/dL nas primeiras 48h",
                "slug": "aumento-bun",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "options": [
                    {"id": "opt_ran_bun_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_bun_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_ca",
                "name": "8. Cálcio Sérico < 8,0 mg/dL nas primeiras 48h",
                "slug": "calcio-serico",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "options": [
                    {"id": "opt_ran_ca_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_ca_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_pao2",
                "name": "9. PaO2 Arterial < 60 mmHg nas primeiras 48h",
                "slug": "pao2-ranson",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 9,
                "options": [
                    {"id": "opt_ran_po2_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_po2_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_be",
                "name": "10. Déficit de Base (Base Excess < -4 mEq/L) em 48h",
                "slug": "deficit-base",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 10,
                "options": [
                    {"id": "opt_ran_be_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_be_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_ran_fluid",
                "name": "11. Sequestro Hídrico Estimado > 6.000 mL em 48h",
                "slug": "sequestro-hidrico",
                "inputType": "single_choice",
                "radarAxisId": "axis_ran_48h",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 11,
                "options": [
                    {"id": "opt_ran_fl_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_ran_fl_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ran_mild",
                "label": "Pancreatite Aguda Leve (0 a 2 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade estimada < 1%. Risco muito baixo de necrose pancreática ou falência orgânica.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ran_mild",
                        "drugName": "Hidratação Venosa com Ringer Lactato e Analgesia",
                        "dosage": "Ringer Lactato 150 a 200 mL/h IV + Dipirona 1g IV 6/6h",
                        "route": "IV",
                        "frequency": "Contínua / Regrada",
                        "indication": "Hidratação moderada sem sobrecarga hídrica; realimentação oral precoce assim que cessar dor e náuseas."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ran_1", "recommendationTitle": "Enfermaria e Dieta Precoce", "dispositionTarget": "Enfermaria", "monitoringPlan": "Reavaliação clínica diária e controle hidroeletrolítico."}
                ]
            },
            {
                "id": "tier_ran_mod",
                "label": "Pancreatite Potencialmente Grave (3 a 5 pontos)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Mortalidade estimada em 10% a 20%. Risco considerável de necrose pancreática estéril.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ran_mod",
                        "drugName": "Ressuscitação Guiada por Metas e Analgesia com Opioides",
                        "dosage": "Ringer Lactato 250 a 350 mL/h + Tramadol 100mg IV ou Morfina 2-4mg IV",
                        "route": "IV",
                        "frequency": "Contínua",
                        "indication": "Meta: débito urinário >= 0,5 a 1 mL/kg/h e hematócrito estável."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ran_2", "recommendationTitle": "Internação em Unidade Semi-Intensiva ou UTI", "dispositionTarget": "Semi-Intensiva / UTI", "monitoringPlan": "Programar TC de abdome contrastada para 72 a 96 horas após início da dor."}
                ]
            },
            {
                "id": "tier_ran_severe",
                "label": "Pancreatite Aguda Grave / Fulminante (6 a 11 pontos)",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 11,
                "statisticalOutcome": "Mortalidade hospitalar excede 50% a > 90%. Alta incidência de falência multiorgânica e infecção de necrose.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ran_sev_atb",
                        "drugName": "Meropenem (Apenas se necrose infectada confirmada ou suspeita com deterioração)",
                        "dosage": "1g IV de 8 em 8 horas",
                        "route": "IV",
                        "frequency": "8/8h",
                        "dilutionInstructions": "Infusão estendida em 3 horas.",
                        "renalAdjustment": "Ajustar dose para ClCr < 50 mL/min.",
                        "contraindications": "Antibioticoprofilaxia de rotina desaconselhada pelas diretrizes internacionais (ACG 2024 / IAP)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ran_3",
                        "recommendationTitle": "Suporte Intensivo Pleno e Abordagem 'Step-Up'",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Manejo conservador inicial; se necrose infectada após 2-4 semanas, adotar estratégia 'Step-Up' (drenagem percutânea/endoscópica antes de necrosectomia cirúrgica).",
                        "interventionalProcedure": "Drenagem percutânea guiada por TC ou necrosectomia endoscópica transgástrica."
                    }
                ]
            }
        ]
    }

def get_bisap():
    return {
        "id": "calc_bisap",
        "slug": "bisap-score",
        "name": "Escore BISAP (Bedside Index for Severity in Acute Pancreatitis)",
        "acronym": "BISAP",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Pancreatite Aguda de Emergência",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Pancreatite Aguda de Emergência",
        "description": "Índice de gravidade precoce nas primeiras 24 horas de internação para predição de falência orgânica e mortalidade na pancreatite aguda.",
        "summary": "Índice de gravidade precoce nas primeiras 24h para predição rápida de falência orgânica e morte.",
        "clinicalObjective": "Superar o atraso de 48h de Ranson, permitindo triagem de alto risco já no primeiro dia de internação hospitalar.",
        "targetPopulation": "Pacientes com pancreatite aguda nas primeiras 24 horas do atendimento.",
        "calculationType": "additive_points",
        "formulaExpression": "BUN + Impaired_Mental + SIRS + Age + Pleural_Effusion",
        "evidenceSource": "Wu BU, Johannes RS, Sun X, Tabak Y, Conwell DL, Banks PA. The early prediction of mortality in acute pancreatitis: a large population-based study. Gut. 2008;57(12):1698-1703.",
        "minPossibleScore": 0,
        "maxPossibleScore": 5,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_bisap_bun", "label": "BUN / Ureia", "system": "Renal", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_bisap_gcs", "label": "Estado Mental", "system": "Neurológico", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_bisap_sirs", "label": "SIRS", "system": "Inflamatório", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_bisap_age", "label": "Idade > 60", "system": "Demográfico", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_bisap_pleur", "label": "Derrame Pleural", "system": "Respiratório", "baselineValue": 0, "maxAxisValue": 1}
        ],
        "parameterGroups": [
            {
                "id": "grp_bisap_bun",
                "name": "B - BUN > 25 mg/dL (ou Ureia > 53,5 mg/dL)",
                "slug": "bun-ureia",
                "inputType": "single_choice",
                "radarAxisId": "axis_bisap_bun",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Conversor brasileiro: Ureia = BUN x 2,14. O corte de BUN > 25 mg/dL equivale exatamente a Ureia > 53,5 mg/dL.",
                "options": [
                    {"id": "opt_bisap_bun_no", "label": "BUN <= 25 mg/dL (Ureia <= 53,5 mg/dL: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bisap_bun_yes", "label": "BUN > 25 mg/dL (Ureia > 53,5 mg/dL: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_bisap_mental",
                "name": "I - Impaired Mental Status (Glasgow < 15 ou Desorientação Aguda)",
                "slug": "estado-mental-bisap",
                "inputType": "single_choice",
                "radarAxisId": "axis_bisap_gcs",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_bisap_gcs_no", "label": "Glasgow = 15 (Sem alteração cognitiva: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bisap_gcs_yes", "label": "Glasgow < 15 ou confusão mental aguda (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_bisap_sirs",
                "name": "S - SIRS (Síndrome da Resposta Inflamatória Sistêmica >= 2 critérios)",
                "slug": "sirs-bisap",
                "inputType": "single_choice",
                "radarAxisId": "axis_bisap_sirs",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Critérios: Temp < 36°C ou > 38°C; FC > 90; FR > 20 ou PaCO2 < 32; Leucócitos < 4.000 ou > 12.000 ou > 10% bastonetes.",
                "options": [
                    {"id": "opt_bisap_sirs_no", "label": "< 2 critérios de SIRS (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bisap_sirs_yes", "label": ">= 2 critérios de SIRS (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_bisap_age",
                "name": "A - Age (Idade > 60 anos)",
                "slug": "idade-60",
                "inputType": "single_choice",
                "radarAxisId": "axis_bisap_age",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_bisap_age_no", "label": "Idade <= 60 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bisap_age_yes", "label": "Idade > 60 anos (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_bisap_pleural",
                "name": "P - Pleural Effusion (Derrame Pleural em RX ou TC)",
                "slug": "derrame-pleural",
                "inputType": "single_choice",
                "radarAxisId": "axis_bisap_pleur",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_bisap_pl_no", "label": "Ausente (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bisap_pl_yes", "label": "Presente (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_bisap_low",
                "label": "BISAP 0 a 2 pontos (Baixo Risco)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade hospitalar muito baixa (< 2%). Risco de falência orgânica < 5%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_bisap_low",
                        "drugName": "Ressuscitação Volêmica Moderada com Ringer Lactato",
                        "dosage": "150 a 200 mL/h IV nas primeiras 24 horas",
                        "route": "IV",
                        "frequency": "Contínua",
                        "indication": "Manter débito urinário > 0,5 mL/kg/h e hematócrito estável."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_bisap_1", "recommendationTitle": "Manejo em Enfermaria Geral", "dispositionTarget": "Enfermaria", "monitoringPlan": "Realimentação oral precoce e analgesia escalonada."}
                ]
            },
            {
                "id": "tier_bisap_high",
                "label": "BISAP 3 a 5 pontos (Alto Risco de Gravidade / Falência)",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Mortalidade hospitalar substancialmente elevada (BISAP 3: ~5%; BISAP 4: ~15%; BISAP 5: > 22% a 30%). Risco elevado de falência orgânica persistente.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_bisap_high",
                        "drugName": "Ressuscitação Volêmica Agressiva Guiada por Metas",
                        "dosage": "Ringer Lactato 250 a 350 mL/h em BIC com titulação por débito urinário",
                        "route": "IV em BIC",
                        "frequency": "Contínua",
                        "indication": "Alvo: débito urinário >= 0,5 a 1,0 mL/kg/h, queda do hematócrito e redução do BUN em 24h."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_bisap_2",
                        "recommendationTitle": "Internação Imediata em UTI e Monitorização Invasiva",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Programar TC com contraste para 72-96h do início dos sintomas. Monitorização seriada de hematócrito, ureia e gasometria a cada 12h.",
                        "vascularAccess": "Acesso venoso calibroso ou central e cateter vesical de demora."
                    }
                ]
            }
        ]
    }

def get_balthazar_ctsi():
    return {
        "id": "calc_balthazar_ctsi",
        "slug": "balthazar-ctsi",
        "name": "Escore de Balthazar e Índice de Gravidade por Tomografia (CTSI)",
        "acronym": "Balthazar CTSI",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Pancreatite Aguda de Emergência",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Pancreatite Aguda de Emergência",
        "description": "Quantificação tomográfica da inflamação peripancreática e extensão da necrose tecidual (0 a 10 pontos).",
        "summary": "Índice de severidade tomográfica para necrose e complicações na pancreatite aguda.",
        "clinicalObjective": "Estratificar o risco de complicações locais, infecção e mortalidade com base na TC de abdome contrastada realizada preferencialmente entre 72 e 96 horas.",
        "targetPopulation": "Pacientes com pancreatite aguda submetidos a TC com contraste após 72h de evolução.",
        "calculationType": "additive_points",
        "evidenceSource": "Balthazar EJ, Robinson DL, Megibow AJ, Ranson JH. Acute pancreatitis: value of CT in establishing prognosis. Radiology. 1990;174(2):331-336.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_ctsi", "label": "Índice CTSI", "system": "Radiologia", "baselineValue": 0, "maxAxisValue": 10}
        ],
        "parameterGroups": [
            {
                "id": "grp_ctsi_morph",
                "name": "Grau Morfológico de Balthazar (0 a 4 pontos)",
                "slug": "grau-balthazar",
                "inputType": "single_choice",
                "radarAxisId": "axis_ctsi",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_bal_a", "label": "Grau A: Pâncreas de aspecto normal (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_bal_b", "label": "Grau B: Aumento focal ou difuso do pâncreas (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_bal_c", "label": "Grau C: Inflamação peripancreática / estriação da gordura (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_bal_d", "label": "Grau D: Coleção líquida única mal delimitada (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_bal_e", "label": "Grau E: Duas ou mais coleções líquidas OU presença de gás peripancreático (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_ctsi_necr",
                "name": "Extensão da Necrose Pancreática (0 a 6 pontos)",
                "slug": "necrose-pancreatica",
                "inputType": "single_choice",
                "radarAxisId": "axis_ctsi",
                "normalBaselineValue": 0,
                "maxAxisValue": 6,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_nec_0", "label": "Sem necrose pancreática (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_nec_30", "label": "Necrose de até 30% do parênquima (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_nec_50", "label": "Necrose de 30% a 50% do parênquima (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_nec_high", "label": "Necrose superior a 50% do parênquima (+6 pts)", "pointValue": 6, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ctsi_mild",
                "label": "CTSI 0 a 3 pontos (Baixo Índice de Gravidade)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade estimada em ~3%. Risco de complicações locais < 8%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ctsi_1", "recommendationTitle": "Tratamento Conservador", "dispositionTarget": "Enfermaria", "monitoringPlan": "Evolução clínica favorável; não requer intervenção intervencionista."}
                ]
            },
            {
                "id": "tier_ctsi_mod",
                "label": "CTSI 4 a 6 pontos (Índice de Gravidade Médio)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 6,
                "statisticalOutcome": "Mortalidade estimada em ~6%. Risco de complicações locais de até 35%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ctsi_2", "recommendationTitle": "Vigilância de Coleções", "dispositionTarget": "Semi-Intensiva", "monitoringPlan": "Acompanhamento clínico estrito e repetição de imagem se febre ou leucocitose."}
                ]
            },
            {
                "id": "tier_ctsi_severe",
                "label": "CTSI 7 a 10 pontos (Alto Índice de Gravidade)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 10,
                "statisticalOutcome": "Mortalidade estimada em 17% a > 20%. Risco de complicações graves excede 70% a 80%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_ctsi_3", "recommendationTitle": "UTI e Planejamento 'Step-Up'", "dispositionTarget": "UTI", "monitoringPlan": "Manejo em centro terciário com suporte cirúrgico e endoscópico avançado."}
                ]
            }
        ]
    }

def get_marshall_mod():
    return {
        "id": "calc_marshall_mod",
        "slug": "marshall-score",
        "name": "Escore de Marshall Modificado para Pancreatite Aguda",
        "acronym": "Marshall Modificado",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Pancreatite Aguda de Emergência",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Pancreatite Aguda de Emergência",
        "description": "Critério formal da Classificação de Atlanta Revisada para definição de falência orgânica (respiratória, renal e cardiovascular) na pancreatite aguda.",
        "summary": "Definição formal de falência orgânica na pancreatite aguda pela Classificação de Atlanta.",
        "clinicalObjective": "Diagnosticar e classificar a falência orgânica em transitória (< 48h = moderada) ou persistente (> 48h = pancreatite aguda grave).",
        "targetPopulation": "Pacientes com pancreatite aguda.",
        "calculationType": "additive_points",
        "evidenceSource": "Banks PA, Bollen TL, Dervenis C, et al. Classification of acute pancreatitis--2012: revision of the Atlanta classification and definitions by international consensus. Gut. 2013;62(1):102-111. Marshall 1995.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_marsh_resp", "label": "Respiratório (PaO2/FiO2)", "system": "Respiratório", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_marsh_ren", "label": "Renal (Creatinina)", "system": "Renal", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_marsh_cv", "label": "Cardiovascular (PAS)", "system": "Cardiovascular", "baselineValue": 0, "maxAxisValue": 4}
        ],
        "parameterGroups": [
            {
                "id": "grp_marsh_resp",
                "name": "1. Sistema Respiratório (PaO2 / FiO2)",
                "slug": "respiratorio-marshall",
                "inputType": "single_choice",
                "radarAxisId": "axis_marsh_resp",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_mar_r_0", "label": "PaO2/FiO2 > 400 (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_mar_r_1", "label": "PaO2/FiO2 301 a 400 (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_mar_r_2", "label": "PaO2/FiO2 201 a 300 (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_mar_r_3", "label": "PaO2/FiO2 101 a 200 (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_mar_r_4", "label": "PaO2/FiO2 <= 101 (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_marsh_renal",
                "name": "2. Sistema Renal (Creatinina sérica em mg/dL)",
                "slug": "renal-marshall",
                "inputType": "single_choice",
                "radarAxisId": "axis_marsh_ren",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_mar_k_0", "label": "Creatinina <= 1,4 mg/dL (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_mar_k_1", "label": "Creatinina 1,5 a 1,8 mg/dL (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_mar_k_2", "label": "Creatinina 1,9 a 3,6 mg/dL (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_mar_k_3", "label": "Creatinina 3,7 a 4,9 mg/dL (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_mar_k_4", "label": "Creatinina >= 5,0 mg/dL (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_marsh_cv",
                "name": "3. Sistema Cardiovascular (Pressão Sistólica e Resposta a Volume)",
                "slug": "cv-marshall",
                "inputType": "single_choice",
                "radarAxisId": "axis_marsh_cv",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_mar_c_0", "label": "PAS > 90 mmHg (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_mar_c_1", "label": "PAS < 90 mmHg responsiva a fluidos (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_mar_c_2", "label": "PAS < 90 mmHg não responsiva a fluidos (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_mar_c_3", "label": "PAS < 90 mmHg e pH < 7,3 (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_mar_c_4", "label": "PAS < 90 mmHg e pH < 7,2 (+4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_marsh_no_fail",
                "label": "Sem Falência Orgânica (< 2 pontos em todos os sistemas)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Ausência de falência orgânica pela Classificação de Atlanta.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_mar_1", "recommendationTitle": "Tratamento em Enfermaria Geral", "dispositionTarget": "Enfermaria", "monitoringPlan": "Reavaliação clínica seriada."}
                ]
            },
            {
                "id": "tier_marsh_failure",
                "label": "Falência Orgânica Presente (>= 2 pontos em qualquer sistema)",
                "severityLevel": "critical",
                "minScore": 2,
                "maxScore": 12,
                "statisticalOutcome": "Falência orgânica confirmada. Se durar < 48h: Falência Transitória (Pancreatite Moderadamente Grave). Se durar >= 48h: Falência Persistente (Pancreatite Aguda Grave - mortalidade > 30% a 50%).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_mar_2", "recommendationTitle": "Internação em UTI e Reavaliação em 48h", "dispositionTarget": "UTI", "monitoringPlan": "Reavaliar escore de Marshall exatamente às 48h para diferenciar falência transitória de persistente."}
                ]
            }
        ]
    }
