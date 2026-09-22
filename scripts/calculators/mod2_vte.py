"""
Module 02: Venous Thromboembolism (DVT and PE)
- Wells TEP
- Wells TVP
- Geneva Revisado
- PERC
- PESI
- sPESI
"""

def get_wells_tep():
    return {
        "id": "calc_wells_tep",
        "slug": "wells-tep",
        "name": "Escore de Wells para Tromboembolismo Pulmonar",
        "acronym": "Wells TEP",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Estratificação pré-teste de probabilidade clínica de Tromboembolismo Pulmonar (TEP) com direcionamento para D-Dímero ou Angio-TC.",
        "summary": "Estratificação clínica pré-teste de probabilidade de embolia pulmonar com tomada de decisão sobre D-Dímero ou Angio-TC.",
        "clinicalObjective": "Definir a probabilidade pré-teste de TEP em pacientes com dispneia aguda ou dor torácica pleurítica, orientando a propedêutica armada sem exames desnecessários.",
        "targetPopulation": "Adultos com suspeita clínica de TEP hemodinamicamente estáveis (contraindicado em choque obstrutivo com PAS < 90 mmHg).",
        "calculationType": "additive_points",
        "formulaExpression": "Soma de 7 critérios ponderados",
        "evidenceSource": "Wells PS, Anderson DR, Rodger M, et al. Derivation of a simple clinical model to categorize patients probability of pulmonary embolism: increasing the models utility with the SimpliRED D-dimer. Thromb Haemost. 2000;83(3):416-420. ESC Guidelines 2019/2024.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12.5,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_wtep_tvp", "label": "Sinais de TVP", "system": "Vascular Periférico", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_wtep_alt", "label": "Diagnóstico Alternativo Improvável", "system": "Clínico", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_wtep_hr", "label": "Taquicardia (FC > 100)", "system": "Hemodinâmico", "baselineValue": 0, "maxAxisValue": 1.5},
            {"id": "axis_wtep_immob", "label": "Imobilização / Cirurgia", "system": "Fator de Risco", "baselineValue": 0, "maxAxisValue": 1.5},
            {"id": "axis_wtep_prior", "label": "TEV Prévio", "system": "Histórico", "baselineValue": 0, "maxAxisValue": 1.5},
            {"id": "axis_wtep_hemopt", "label": "Hemoptise", "system": "Respiratório", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_wtep_cancer", "label": "Neoplasia Ativa", "system": "Comorbidade", "baselineValue": 0, "maxAxisValue": 1}
        ],
        "parameterGroups": [
            {
                "id": "grp_wtep_tvp",
                "name": "1. Sinais e Sintomas Clínicos de TVP",
                "slug": "sinais-tvp",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_tvp",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 1,
                "helpText": "Edema assimétrico de membro inferior (diferença >= 3 cm) e dor à palpação do trajeto venoso profundo.",
                "options": [
                    {"id": "opt_wtep_tvp_no", "label": "Ausentes (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_tvp_yes", "label": "Presentes (+3,0 pts)", "pointValue": 3.0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_alt",
                "name": "2. Diagnóstico Alternativo Menos Provável que TEP",
                "slug": "diagnostico-alternativo",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_alt",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Julgamento clínico de que o TEP é a principal hipótese diagnóstica frente a pneumopatia, SCA ou dor osteomuscular.",
                "options": [
                    {"id": "opt_wtep_alt_no", "label": "Outro diagnóstico é mais provável (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_alt_yes", "label": "TEP é o diagnóstico mais provável (+3,0 pts)", "pointValue": 3.0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_hr",
                "name": "3. Frequência Cardíaca > 100 bpm",
                "slug": "taquicardia",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_hr",
                "normalBaselineValue": 0,
                "maxAxisValue": 1.5,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_wtep_hr_no", "label": "FC <= 100 bpm (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_hr_yes", "label": "FC > 100 bpm (+1,5 pts)", "pointValue": 1.5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_immob",
                "name": "4. Imobilização ou Cirurgia Recente",
                "slug": "imobilizacao-cirurgia",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_immob",
                "normalBaselineValue": 0,
                "maxAxisValue": 1.5,
                "sortOrder": 4,
                "helpText": "Imobilização no leito por >= 3 dias consecutivos ou cirurgia de grande porte nas últimas 4 semanas.",
                "options": [
                    {"id": "opt_wtep_immob_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_immob_yes", "label": "Sim (+1,5 pts)", "pointValue": 1.5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_prior",
                "name": "5. Histórico Prévio Documentado de TVP ou TEP",
                "slug": "tev-previo",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_prior",
                "normalBaselineValue": 0,
                "maxAxisValue": 1.5,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_wtep_prior_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_prior_yes", "label": "Sim (+1,5 pts)", "pointValue": 1.5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_hemopt",
                "name": "6. Hemoptise",
                "slug": "hemoptise",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_hemopt",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "options": [
                    {"id": "opt_wtep_hemopt_no", "label": "Ausente (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_hemopt_yes", "label": "Presente (+1,0 pt)", "pointValue": 1.0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtep_cancer",
                "name": "7. Neoplasia Maligna Ativa",
                "slug": "cancer-ativo",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtep_cancer",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "helpText": "Tratamento nos últimos 6 meses ou em cuidados paliativos.",
                "options": [
                    {"id": "opt_wtep_cancer_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtep_cancer_yes", "label": "Sim (+1,0 pt)", "pointValue": 1.0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_wtep_unlikely",
                "label": "TEP Improvável (<= 4,0 pontos)",
                "severityLevel": "low",
                "minScore": 0.0,
                "maxScore": 4.0,
                "statisticalOutcome": "Prevalência média de TEP estimada em ~8%. Aplicar critérios de PERC para exclusão sem D-dímero.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wtep_unlikely_1",
                        "drugName": "Anticoagulação plena NÃO indicada no momento",
                        "dosage": "Aguardar resultado de D-Dímero",
                        "route": "Nenhuma",
                        "frequency": "Nenhuma",
                        "contraindications": "Evitar anticoagulação empírica em pacientes de probabilidade improvável."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_wtep_unlikely_1",
                        "recommendationTitle": "Fluxo Diagnóstico: Regra de PERC e D-Dímero Ajustado",
                        "dispositionTarget": "Observação",
                        "monitoringPlan": "1. Aplicar escore PERC: se todos os 8 critérios PERC forem negativos, TEP está EXCLUÍDO clinicamente (sem exames laboratoriais ou radiológicos).\n2. Se PERC positivo (qualquer critério presente): solicitar D-Dímero ultrassensível com ponto de corte ajustado pela idade (Idade x 10 mcg/L se idade > 50 anos).\n3. Se D-Dímero normal: TEP descartado. Se D-Dímero elevado: proceder para Angio-TC de tórax.",
                        "laboratoryPanel": "D-Dímero de alta sensibilidade (ELISA)."
                    }
                ]
            },
            {
                "id": "tier_wtep_likely",
                "label": "TEP Provável (> 4,0 pontos)",
                "severityLevel": "high",
                "minScore": 4.5,
                "maxScore": 12.5,
                "statisticalOutcome": "Prevalência de TEP estimada entre 30% e 40% (Alto risco pré-teste). Encaminhar diretamente para Angio-TC de Tórax.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wtep_likely_enox",
                        "drugName": "Enoxaparina Sódica (ou Heparina Não Fracionada)",
                        "dosage": "1 mg/kg SC de 12 em 12 horas (ou 1,5 mg/kg SC 1x/dia)",
                        "route": "Subcutânea",
                        "frequency": "12/12 horas",
                        "dilutionInstructions": "Solução pronta para injeção subcutânea.",
                        "renalAdjustment": "Se ClCr < 30 mL/min: Reduzir dose para 1 mg/kg SC 1x/dia OU comutar para Heparina Não Fracionada IV contínua (bolus 80 UI/kg seguido de 18 UI/kg/h com alvo de TTPA 1,5 a 2,5x o controle).",
                        "contraindications": "Sangramento ativo maior, plaquetopenia grave (< 50.000), histórico de plaquetopenia induzida por heparina (HIT) ou cirurgia recente do SNC/ocular."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_wtep_likely_1",
                        "recommendationTitle": "Angiotomografia de Tórax Imediata e Anticoagulação Empírica",
                        "dispositionTarget": "Enfermaria / Semi-Intensiva",
                        "monitoringPlan": "Encaminhar diretamente para Angio-TC de Artérias Pulmonares. Contraindicada a solicitação de D-Dímero (falso positivo frequente, não descarta). Se atraso previsto para o exame > 4 horas e sem risco hemorrágico elevado, INICIAR anticoagulação plena empírica antes do laudo tomográfico.",
                        "interventionalProcedure": "Se contraindicação absoluta à anticoagulação com TEP confirmado: avaliar implante de Filtro de Veia Cava Inferior.",
                        "laboratoryPanel": "Coagulograma completo, função renal e hemograma com plaquetas."
                    }
                ]
            }
        ]
    }

def get_wells_tvp():
    return {
        "id": "calc_wells_tvp",
        "slug": "wells-tvp",
        "name": "Escore de Wells para Trombose Venosa Profunda (TVP)",
        "acronym": "Wells TVP",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Estratificação pré-teste de probabilidade clínica de TVP de membros inferiores.",
        "summary": "Estratificação pré-teste de Trombose Venosa Profunda para direcionamento de D-Dímero ou USG Doppler.",
        "clinicalObjective": "Determinar probabilidade pré-teste de TVP em membros inferiores.",
        "targetPopulation": "Pacientes com suspeita de TVP em membros inferiores.",
        "calculationType": "additive_points",
        "evidenceSource": "Wells PS, Anderson DR, Bormanis J, et al. Value of assessment of pretest probability of deep-vein thrombosis in clinical management. Lancet. 1997;350(9094):1795-1798. Wells 2003.",
        "minPossibleScore": -2,
        "maxPossibleScore": 9,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_wtvp_score", "label": "Pontuação Wells TVP", "system": "Vascular", "baselineValue": 0, "maxAxisValue": 9}
        ],
        "parameterGroups": [
            {
                "id": "grp_wtvp_cancer",
                "name": "1. Câncer Ativo",
                "slug": "cancer-ativo",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_wtvp_can_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_can_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_paralysis",
                "name": "2. Paralisia, Paresia ou Imobilização Gessada de MMII",
                "slug": "paralisia-imobilizacao",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_wtvp_par_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_par_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_bedridden",
                "name": "3. Acamado Recentemente >= 3 dias ou Cirurgia Maior em 12 semanas",
                "slug": "acamado-cirurgia",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_wtvp_bed_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_bed_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_tenderness",
                "name": "4. Dor Localizada ao Longo do Sistema Venoso Profundo",
                "slug": "dor-palpacao",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_wtvp_tnd_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_tnd_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_swelling",
                "name": "5. Edema de Todo o Membro Inferior",
                "slug": "edema-todo-membro",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_wtvp_swl_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_swl_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_calf",
                "name": "6. Aumento da Panturrilha > 3 cm comparado ao lado assintomático",
                "slug": "assimetria-panturrilha",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "options": [
                    {"id": "opt_wtvp_calf_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_calf_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_edema",
                "name": "7. Edema com Cacifo (Godet) Confinado à Perna Sintomática",
                "slug": "edema-cacifo",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "options": [
                    {"id": "opt_wtvp_edm_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_edm_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_collateral",
                "name": "8. Veias Superficiais Colaterais Não Varicosas",
                "slug": "veias-colaterais",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "options": [
                    {"id": "opt_wtvp_col_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_col_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_history",
                "name": "9. Histórico Prévio Documentado de TVP",
                "slug": "tvp-previa",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 9,
                "options": [
                    {"id": "opt_wtvp_his_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_his_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_wtvp_alt_diag",
                "name": "10. Diagnóstico Alternativo Tão ou Mais Provável que TVP (Redutor)",
                "slug": "diagnostico-alternativo-tvp",
                "inputType": "single_choice",
                "radarAxisId": "axis_wtvp_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 10,
                "helpText": "Ex.: celulite, erisipela, cisto de Baker roto, hematoma muscular ou insuficiência venosa crônica.",
                "options": [
                    {"id": "opt_wtvp_alt_no", "label": "Não há diagnóstico alternativo tão provável (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_wtvp_alt_yes", "label": "Sim, outro diagnóstico é provável (-2 pts)", "pointValue": -2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_wtvp_unlikely",
                "label": "TVP Improvável (<= 1 ponto)",
                "severityLevel": "low",
                "minScore": -2,
                "maxScore": 1,
                "statisticalOutcome": "Baixa probabilidade clínica pré-teste (~5%). Solicitar D-Dímero de alta sensibilidade.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_wtvp_1", "recommendationTitle": "Triagem com D-Dímero", "dispositionTarget": "Ambulatório / Observação", "monitoringPlan": "Se D-Dímero negativo, TVP descartada sem ultrassom. Se D-Dímero positivo, realizar USG Doppler venoso."}
                ]
            },
            {
                "id": "tier_wtvp_likely",
                "label": "TVP Provável (>= 2 pontos)",
                "severityLevel": "high",
                "minScore": 2,
                "maxScore": 9,
                "statisticalOutcome": "Alta probabilidade pré-teste (~28% a 40%). Realizar Ultrassonografia Doppler venosa de membros inferiores.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wtvp_enox",
                        "drugName": "Anticoagulação Plena com Enoxaparina",
                        "dosage": "1 mg/kg SC 12/12h",
                        "route": "SC",
                        "frequency": "12/12h",
                        "renalAdjustment": "Ajustar dose se ClCr < 30 mL/min."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_wtvp_2", "recommendationTitle": "USG Doppler Venoso e Meias Elásticas", "dispositionTarget": "Observação / Enfermaria", "monitoringPlan": "Confirmar com Doppler venoso de compressão."}
                ]
            }
        ]
    }

def get_geneva():
    return {
        "id": "calc_geneva",
        "slug": "geneva-score",
        "name": "Escore de Geneva Revisado para Tromboembolismo Pulmonar",
        "acronym": "Geneva Revisado",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Estratificação pré-teste de probabilidade clínica de TEP baseada em dados objetivos sem variáveis subjetivas.",
        "summary": "Probabilidade pré-teste de TEP baseada em dados estritamente objetivos.",
        "clinicalObjective": "Alternativa totalmente objetiva ao escore de Wells para determinar necessidade de D-Dímero vs Angio-TC.",
        "targetPopulation": "Adultos com suspeita de TEP em emergência.",
        "calculationType": "additive_points",
        "evidenceSource": "Le Gal G, Righini M, Roy PM, et al. Prediction of pulmonary embolism in the emergency department: the revised Geneva score. Ann Intern Med. 2006;144(3):165-172.",
        "minPossibleScore": 0,
        "maxPossibleScore": 22,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_gen_score", "label": "Pontuação Geneva", "system": "TEV", "baselineValue": 0, "maxAxisValue": 22}
        ],
        "parameterGroups": [
            {
                "id": "grp_gen_age",
                "name": "Idade > 65 anos",
                "slug": "idade-geneva",
                "inputType": "single_choice",
                "radarAxisId": "axis_gen_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_gen_age_no", "label": "<= 65 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gen_age_yes", "label": "> 65 anos (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_gen_prev",
                "name": "Histórico de TVP ou TEP prévio",
                "slug": "tev-previo-geneva",
                "inputType": "single_choice",
                "radarAxisId": "axis_gen_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_gen_prev_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gen_prev_yes", "label": "Sim (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_gen_surg",
                "name": "Cirurgia ou fratura no último mês",
                "slug": "cirurgia-geneva",
                "inputType": "single_choice",
                "radarAxisId": "axis_gen_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_gen_surg_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gen_surg_yes", "label": "Sim (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_gen_canc",
                "name": "Neoplasia maligna ativa",
                "slug": "cancer-geneva",
                "inputType": "single_choice",
                "radarAxisId": "axis_gen_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_gen_canc_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gen_canc_yes", "label": "Sim (+2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_gen_hr",
                "name": "Frequência Cardíaca",
                "slug": "fc-geneva",
                "inputType": "single_choice",
                "radarAxisId": "axis_gen_score",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_gen_hr_normal", "label": "< 75 bpm (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gen_hr_mod", "label": "75 a 94 bpm (+3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 2},
                    {"id": "opt_gen_hr_high", "label": ">= 95 bpm (+5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_gen_low",
                "label": "Baixa Probabilidade (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Prevalência de TEP estimada < 10%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_gen_1", "recommendationTitle": "Dosagem de D-Dímero", "dispositionTarget": "Observação", "monitoringPlan": "Se D-Dímero negativo, excluir TEP."}
                ]
            },
            {
                "id": "tier_gen_mod",
                "label": "Probabilidade Intermediária (4 a 10 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 10,
                "statisticalOutcome": "Prevalência de TEP estimada em ~30%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_gen_2", "recommendationTitle": "D-Dímero ou Angio-TC", "dispositionTarget": "Observação", "monitoringPlan": "D-Dímero ajustado por idade; se positivo proceder à Angio-TC."}
                ]
            },
            {
                "id": "tier_gen_high",
                "label": "Alta Probabilidade (>= 11 pontos)",
                "severityLevel": "high",
                "minScore": 11,
                "maxScore": 22,
                "statisticalOutcome": "Prevalência de TEP excede 65%. Angio-TC direta.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_gen_3", "recommendationTitle": "Angiotomografia de Tórax Direta", "dispositionTarget": "Enfermaria / Semi-Intensiva", "monitoringPlan": "Iniciar anticoagulação se atraso > 4h."}
                ]
            }
        ]
    }

def get_perc():
    return {
        "id": "calc_perc",
        "slug": "perc-rule",
        "name": "Critérios de PERC (Pulmonary Embolism Rule-out Criteria)",
        "acronym": "PERC",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Regra clínica de exclusão rápida de TEP em pacientes com suspeita clínica de baixo risco.",
        "summary": "Critérios de exclusão de TEP sem necessidade de D-Dímero em pacientes de baixo risco.",
        "clinicalObjective": "Dispensar a dosagem de D-Dímero e Angio-TC em pacientes de baixo risco pré-teste que preencham todos os 8 critérios negativos.",
        "targetPopulation": "Pacientes de baixo risco clínico (< 15% de probabilidade pré-teste) com suspeita de TEP.",
        "calculationType": "additive_points",
        "evidenceSource": "Kline JA, Mitchell AM, Kabrhel C, et al. Clinical criteria to prevent unnecessary diagnostic testing in emergency department patients with suspected pulmonary embolism. J Thromb Haemost. 2004;2(8):1247-1267.",
        "minPossibleScore": 0,
        "maxPossibleScore": 8,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_perc", "label": "Critérios Positivos PERC", "system": "PERC", "baselineValue": 0, "maxAxisValue": 8}
        ],
        "parameterGroups": [
            {
                "id": "grp_perc_age",
                "name": "Idade >= 50 anos",
                "slug": "idade-50",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_perc_age_no", "label": "Não (< 50 anos: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_age_yes", "label": "Sim (>= 50 anos: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_hr",
                "name": "Frequência Cardíaca >= 100 bpm",
                "slug": "fc-100",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_perc_hr_no", "label": "Não (< 100 bpm: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_hr_yes", "label": "Sim (>= 100 bpm: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_spo2",
                "name": "Saturação de O2 < 95% em ar ambiente",
                "slug": "spo2-95",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_perc_spo2_no", "label": "Não (SpO2 >= 95%: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_spo2_yes", "label": "Sim (SpO2 < 95%: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_leg",
                "name": "Edema unilateral de membro inferior",
                "slug": "edema-unilateral",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_perc_leg_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_leg_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_hemopt",
                "name": "Hemoptise",
                "slug": "hemoptise-perc",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_perc_hem_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_hem_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_surg",
                "name": "Cirurgia ou trauma recente com internação <= 4 semanas",
                "slug": "cirurgia-trauma-perc",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "options": [
                    {"id": "opt_perc_surg_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_surg_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_prior",
                "name": "Histórico prévio de TVP ou TEP",
                "slug": "tev-previo-perc",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "options": [
                    {"id": "opt_perc_pri_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_pri_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_perc_estrog",
                "name": "Uso exógeno de estrogênio (ACO, TRH)",
                "slug": "estrogenio-perc",
                "inputType": "single_choice",
                "radarAxisId": "axis_perc",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "options": [
                    {"id": "opt_perc_est_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_perc_est_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_perc_neg",
                "label": "PERC Negativo (0 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Probabilidade de TEP residual < 1,5%. TEP descartado com segurança sem exames adicionais.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_perc_1", "recommendationTitle": "Alta Hospitalar / Investigação Alternativa", "dispositionTarget": "Alta Orientada", "monitoringPlan": "Dispensada dosagem de D-Dímero e Angiotomografia. Investigar outras causas de dispneia ou dor."}
                ]
            },
            {
                "id": "tier_perc_pos",
                "label": "PERC Positivo (>= 1 ponto)",
                "severityLevel": "intermediate",
                "minScore": 1,
                "maxScore": 8,
                "statisticalOutcome": "A regra de PERC não exclui o TEP. Requer dosagem de D-Dímero de alta sensibilidade.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_perc_2", "recommendationTitle": "Dosagem de D-Dímero Mandatória", "dispositionTarget": "Observação", "monitoringPlan": "Dosar D-Dímero ajustado por idade (Idade x 10 mcg/L se > 50 anos)."}
                ]
            }
        ]
    }

def get_pesi():
    return {
        "id": "calc_pesi",
        "slug": "pesi-score",
        "name": "PESI (Pulmonary Embolism Severity Index)",
        "acronym": "PESI",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Escore prognóstico de mortalidade em 30 dias para estratificação de risco em pacientes com diagnóstico confirmado de TEP.",
        "summary": "Índice de gravidade e predição de mortalidade em 30 dias no TEP confirmado (Classes I a V).",
        "clinicalObjective": "Identificar pacientes com TEP confirmado que apresentam baixo risco de complicações e são candidatos a alta precoce ou tratamento ambulatorial.",
        "targetPopulation": "Adultos com diagnóstico confirmado de embolia pulmonar.",
        "calculationType": "additive_points",
        "evidenceSource": "Aujesky D, Obrosky DS, Stone RA, et al. Derivation and validation of a prognostic model for pulmonary embolism. Am J Respir Crit Care Med. 2005;172(8):1041-1046.",
        "minPossibleScore": 0,
        "maxPossibleScore": 250,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_pesi", "label": "Pontos PESI", "system": "PESI", "baselineValue": 0, "maxAxisValue": 150}
        ],
        "parameterGroups": [
            {
                "id": "grp_pesi_age",
                "name": "Idade (em anos = pontuação exata)",
                "slug": "idade-pesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_pesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 90,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_pesi_age_40", "label": "Idade <= 40 anos (+40 pts)", "pointValue": 40, "isNormalBaseline": False, "radarNormalizedValue": 0.27, "sortOrder": 1},
                    {"id": "opt_pesi_age_60", "label": "Idade 41 a 60 anos (+60 pts)", "pointValue": 60, "isNormalBaseline": False, "radarNormalizedValue": 0.40, "sortOrder": 2},
                    {"id": "opt_pesi_age_80", "label": "Idade > 60 anos (+80 pts)", "pointValue": 80, "isNormalBaseline": False, "radarNormalizedValue": 0.53, "sortOrder": 3}
                ]
            },
            {
                "id": "grp_pesi_sex",
                "name": "Sexo Masculino",
                "slug": "sexo-pesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_pesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 10,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_pesi_sex_f", "label": "Feminino (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_pesi_sex_m", "label": "Masculino (+10 pts)", "pointValue": 10, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_pesi_cancer",
                "name": "Histórico de Câncer",
                "slug": "cancer-pesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_pesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 30,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_pesi_can_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_pesi_can_yes", "label": "Sim (+30 pts)", "pointValue": 30, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_pesi_hf",
                "name": "Insuficiência Cardíaca Crônica",
                "slug": "icc-pesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_pesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 10,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_pesi_hf_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_pesi_hf_yes", "label": "Sim (+10 pts)", "pointValue": 10, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_pesi_sbp",
                "name": "Pressão Arterial Sistólica < 100 mmHg",
                "slug": "pas-pesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_pesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 30,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_pesi_sbp_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_pesi_sbp_yes", "label": "Sim (+30 pts)", "pointValue": 30, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_pesi_1_2",
                "label": "PESI Classe I e II - Baixo Risco (<= 85 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 85,
                "statisticalOutcome": "Mortalidade em 30 dias muito baixa (0% a 3,5%). Candidato a alta hospitalar precoce e tratamento domiciliar com anticoagulante oral direto (DOAC).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_pesi_doac",
                        "drugName": "Rivaroxabana ou Apixabana",
                        "dosage": "Rivaroxabana 15 mg VO 12/12h por 21 dias seguido de 20 mg 1x/dia",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "renalAdjustment": "Evitar se ClCr < 15 mL/min."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_pesi_1", "recommendationTitle": "Elegibilidade para Tratamento Ambulatorial", "dispositionTarget": "Alta Orientada", "monitoringPlan": "Retorno em 48-72h e suporte social verificado."}
                ]
            },
            {
                "id": "tier_pesi_3_5",
                "label": "PESI Classe III a V - Risco Intermediário a Alto (> 85 pontos)",
                "severityLevel": "high",
                "minScore": 86,
                "maxScore": 250,
                "statisticalOutcome": "Mortalidade em 30 dias estimada de 7% a > 24%. Internação hospitalar mandatória.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_pesi_2", "recommendationTitle": "Internação Hospitalar / Monitorização", "dispositionTarget": "Enfermaria / UTI", "monitoringPlan": "Ecocardiograma e troponina seriados para avaliar disfunção ventricular direita."}
                ]
            }
        ]
    }

def get_spesi():
    return {
        "id": "calc_spesi",
        "slug": "spesi-score",
        "name": "sPESI (Simplified Pulmonary Embolism Severity Index)",
        "acronym": "sPESI",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Tromboembolismo Venoso (TVP e TEP)",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Tromboembolismo Venoso (TVP e TEP)",
        "description": "Versão simplificada dicotômica do PESI para decisão rápida de internação vs desospitalização precoce em TEP.",
        "summary": "Versão rápida de 6 itens para prognóstico de mortalidade em 30 dias em TEP confirmado.",
        "clinicalObjective": "Estratificação prognóstica binária rápida (0 pontos = Baixo Risco vs >= 1 ponto = Alto Risco).",
        "targetPopulation": "Pacientes com TEP confirmado.",
        "calculationType": "additive_points",
        "evidenceSource": "Jiménez D, Aujesky D, Moores L, et al. Simplification of the pulmonary embolism severity index for prognostication in patients with acute symptomatic pulmonary embolism. Arch Intern Med. 2010;170(15):1383-1389.",
        "minPossibleScore": 0,
        "maxPossibleScore": 6,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_spesi", "label": "Critérios sPESI", "system": "sPESI", "baselineValue": 0, "maxAxisValue": 6}
        ],
        "parameterGroups": [
            {
                "id": "grp_spesi_age",
                "name": "1. Idade > 80 anos",
                "slug": "idade-80",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_sp_age_no", "label": "Não (<= 80 anos: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_age_yes", "label": "Sim (> 80 anos: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_spesi_cancer",
                "name": "2. Câncer",
                "slug": "cancer-spesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_sp_can_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_can_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_spesi_cp",
                "name": "3. Doença Cardiopulmonar Crônica (ICC ou DPOC)",
                "slug": "cardiopulmonar-spesi",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_sp_cp_no", "label": "Não (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_cp_yes", "label": "Sim (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_spesi_hr",
                "name": "4. Frequência Cardíaca >= 110 bpm",
                "slug": "fc-110",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_sp_hr_no", "label": "Não (< 110 bpm: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_hr_yes", "label": "Sim (>= 110 bpm: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_spesi_sbp",
                "name": "5. Pressão Arterial Sistólica < 100 mmHg",
                "slug": "pas-100",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "options": [
                    {"id": "opt_sp_sbp_no", "label": "Não (PAS >= 100 mmHg: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_sbp_yes", "label": "Sim (PAS < 100 mmHg: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_spesi_spo2",
                "name": "6. Saturação de O2 < 90%",
                "slug": "spo2-90",
                "inputType": "single_choice",
                "radarAxisId": "axis_spesi",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "options": [
                    {"id": "opt_sp_spo2_no", "label": "Não (SpO2 >= 90%: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_sp_spo2_yes", "label": "Sim (SpO2 < 90%: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_spesi_low",
                "label": "sPESI = 0 pontos (Baixo Risco)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em ~1,0%. Elegível a alta hospitalar precoce e tratamento domiciliar com DOAC se estabilidade psicossocial.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_spesi_doac",
                        "drugName": "Anticoagulação Oral com DOAC (Rivaroxabana ou Apixabana)",
                        "dosage": "Rivaroxabana 15 mg VO 12/12h com alimentos",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "renalAdjustment": "Seguro se ClCr > 15-30 mL/min."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_spesi_1", "recommendationTitle": "Alta Precoce Assistida", "dispositionTarget": "Alta Orientada", "monitoringPlan": "Consulta de retorno em até 72 horas."}
                ]
            },
            {
                "id": "tier_spesi_high",
                "label": "sPESI >= 1 ponto (Alto Risco de Mortalidade)",
                "severityLevel": "high",
                "minScore": 1,
                "maxScore": 6,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em ~10,9%. Internação hospitalar indicada.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_spesi_2", "recommendationTitle": "Internação Hospitalar com Monitorização", "dispositionTarget": "Enfermaria / Semi-Intensiva", "monitoringPlan": "Avaliar ecocardiograma e troponina."}
                ]
            }
        ]
    }
