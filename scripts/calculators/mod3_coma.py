"""
Module 03: Coma, Level of Consciousness and Sedation
- Glasgow-P (ECG-P)
- FOUR Score
- RASS
- SAS (Riker)
- CAM-ICU
"""

def get_glasgow_p():
    return {
        "id": "calc_glasgow_p",
        "slug": "glasgow-p",
        "name": "Escala de Coma de Glasgow com Reatividade Pupilar (ECG-P)",
        "acronym": "Glasgow-P",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Coma, Nível de Consciência e Sedação",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Coma, Nível de Consciência e Sedação",
        "description": "Avaliação neurológica quantitativa integrando a escala tradicional de Glasgow (3-15) à reatividade pupilar à luz (0-2 subtraídos), resultando em pontuação de 1 a 15.",
        "summary": "Escala de coma refinada para TCE e neuroemergências com pontuação pupilar subtrativa (1 a 15 pontos).",
        "clinicalObjective": "Quantificar a profundidade do coma no trauma cranioencefálico (TCE) e neuroemergências, orientando a decisão de via aérea definitiva e neuroproteção intensiva.",
        "targetPopulation": "Pacientes com traumatismo cranioencefálico, AVE, encefalopatias agudas ou rebaixamento do nível de consciência.",
        "calculationType": "branching_decision",
        "formulaExpression": "(Ocular + Verbal + Motor) - Reatividade_Pupilar",
        "evidenceSource": "Brennan PM, Murray GD, Teasdale GM. A practical method for dealing with missing Glasgow Coma Scale components: GCS-Pupils score. Pract Neurol. 2018;18(5):370-377. ATLS 10th Ed; Brain Trauma Foundation 2020.",
        "minPossibleScore": 1,
        "maxPossibleScore": 15,
        "badge": "emergencia",
        "radarAxes": [
            {"id": "axis_gp_eye", "label": "Abertura Ocular", "system": "Neurológico", "baselineValue": 4, "maxAxisValue": 1},
            {"id": "axis_gp_verb", "label": "Resposta Verbal", "system": "Neurológico", "baselineValue": 5, "maxAxisValue": 1},
            {"id": "axis_gp_mot", "label": "Resposta Motora", "system": "Neurológico", "baselineValue": 6, "maxAxisValue": 1},
            {"id": "axis_gp_pup", "label": "Reatividade Pupilar", "system": "Neurológico", "baselineValue": 0, "maxAxisValue": 2}
        ],
        "parameterGroups": [
            {
                "id": "grp_gp_eye",
                "name": "1. Abertura Ocular (O)",
                "slug": "abertura-ocular",
                "inputType": "single_choice",
                "radarAxisId": "axis_gp_eye",
                "normalBaselineValue": 4,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_gp_eye_4", "label": "Espontânea (4 pts)", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gp_eye_3", "label": "Ao chamado verbal / comando sonoro (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_gp_eye_2", "label": "À pressão dolorosa central / estímulo tátil (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_gp_eye_1", "label": "Nenhuma resposta ocular (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_gp_verb",
                "name": "2. Resposta Verbal (V)",
                "slug": "resposta-verbal",
                "inputType": "single_choice",
                "radarAxisId": "axis_gp_verb",
                "normalBaselineValue": 5,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_gp_v_5", "label": "Orientada no tempo, espaço e pessoa (5 pts)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gp_v_4", "label": "Confusa / desorientada (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_gp_v_3", "label": "Palavras inapropriadas e desconexas (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_gp_v_2", "label": "Sons ininteligíveis / gemidos (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_gp_v_1", "label": "Nenhuma resposta verbal (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_gp_mot",
                "name": "3. Melhor Resposta Motora (M)",
                "slug": "resposta-motora",
                "inputType": "single_choice",
                "radarAxisId": "axis_gp_mot",
                "normalBaselineValue": 6,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_gp_m_6", "label": "Obedece a comandos motores verbais (6 pts)", "pointValue": 6, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_gp_m_5", "label": "Localiza estímulo doloroso (5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_gp_m_4", "label": "Flexão normal / retirada à dor (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_gp_m_3", "label": "Flexão anormal / padrão de decorticação (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_gp_m_2", "label": "Extensão anormal / padrão de descerebração (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_gp_m_1", "label": "Nenhuma resposta motora / flacidez (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_gp_pup",
                "name": "4. Reatividade Pupilar à Luz (Escore Pupilar Subtrativo)",
                "slug": "reatividade-pupilar",
                "inputType": "single_choice",
                "radarAxisId": "axis_gp_pup",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 4,
                "helpText": "Subtrair pontos da soma do Glasgow (ECG 3-15) conforme o número de pupilas que NÃO reagem à luz.",
                "options": [
                    {"id": "opt_gp_p_0", "label": "Ambas as pupilas reagem à luz (Subtrair 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Fotomotor bilateral preservado."},
                    {"id": "opt_gp_p_1", "label": "Apenas uma pupila reage à luz (Subtrair 1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Anisocoria com midríase unilateral fixa (alerta de herniação uncal)."},
                    {"id": "opt_gp_p_2", "label": "NENHUMA pupila reage à luz (Subtrair 2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Midríase bilateral fixa ou miose paralítica (lesão de tronco grave)."}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_gp_mild",
                "label": "TCE / Comprometimento Leve (13 a 15 pontos)",
                "severityLevel": "low",
                "minScore": 13,
                "maxScore": 15,
                "statisticalOutcome": "Risco de intervenção neurocirúrgica < 1%. Mortalidade < 1%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gp_mild",
                        "drugName": "Analgesia Simples (Dipirona ou Paracetamol)",
                        "dosage": "Dipirona 1g IV ou Paracetamol 750mg VO",
                        "route": "IV / VO",
                        "frequency": "6/6h se dor",
                        "contraindications": "Evitar sedativos, opioides fortes e anti-inflamatórios."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gp_mild",
                        "recommendationTitle": "Observação Seriada e Regra de Ottawa para TC",
                        "dispositionTarget": "Observação",
                        "monitoringPlan": "Avaliação neurológica seriada a cada 2h. Aplicar regras clínicas canadenses (Canadian CT Head Rule) para definir indicação de TC de crânio."
                    }
                ]
            },
            {
                "id": "tier_gp_mod",
                "label": "TCE / Comprometimento Moderado (9 a 12 pontos)",
                "severityLevel": "intermediate",
                "minScore": 9,
                "maxScore": 12,
                "statisticalOutcome": "Risco de lesão intracraniana tomográfica de 15% a 30%. Risco de deterioração neurológica.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gp_mod_anti",
                        "drugName": "Profilaxia Anticonvulsivante (Levetiracetam ou Fenitoína)",
                        "dosage": "Levetiracetam 1g IV em 100 mL SF 0,9% em 15 min (ou Fenitoína 20 mg/kg IV lenta máx 50 mg/min)",
                        "route": "IV",
                        "frequency": "Dose de ataque",
                        "indication": "TCE moderado com contusão cortical, fratura deprimida ou hematoma intracraniano para prevenção de convulsões precoces (< 7 dias)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gp_mod",
                        "recommendationTitle": "Tomografia de Crânio Urgente e Vaga Monitorizada",
                        "dispositionTarget": "Semi-Intensiva / Sala Vermelha",
                        "monitoringPlan": "TC de crânio sem contraste urgente. Cabeceira elevada a 30 graus, alinhamento cervical neutro, vigilância rigorosa de pupila e motricidade a cada 1h.",
                        "laboratoryPanel": "Coagulograma, hemograma, glicemia capilar e gasometria."
                    }
                ]
            },
            {
                "id": "tier_gp_severe",
                "label": "TCE / Coma Grave (1 a 8 pontos)",
                "severityLevel": "critical",
                "minScore": 1,
                "maxScore": 8,
                "statisticalOutcome": "Mortalidade superior a 30% a 50% (se reatividade pupilar 0 com escore 1-4, mortalidade > 70%). Perda de reflexos protetores de via aérea.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gp_rsi",
                        "drugName": "Sequência Rápida de Intubação (Etomidato + Succinilcolina / Rocurônio)",
                        "dosage": "Etomidato 0,3 mg/kg IV + Succinilcolina 1,0 a 1,5 mg/kg IV (ou Rocurônio 1,2 mg/kg IV)",
                        "route": "IV em bolus rápido",
                        "frequency": "Dose única",
                        "contraindications": "Evitar hipotensão durante indução (manter PAM >= 80 mmHg; iniciar Noradrenalina profilática se necessário)."
                    },
                    {
                        "id": "rx_gp_osm",
                        "drugName": "Terapia Osmolar de Emergência (Solução Salina Hipertônica 3% ou Manitol 20%)",
                        "dosage": "Salina 3% 250 a 300 mL IV em 15-20 min OU Manitol 20% 0,5 a 1,0 g/kg IV",
                        "route": "IV",
                        "frequency": "Se sinais de herniação transtentorial ou anisocoria aguda",
                        "indication": "Descompressão osmolar de urgência para salvar parênquima cerebral em herniação uncal iminente."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gp_severe",
                        "recommendationTitle": "Intubação Orotraqueal Imediata e Metas Rígidas de Neuroproteção",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Metas da Brain Trauma Foundation: PaCO2 rigorosamente entre 35 e 40 mmHg (evitar hiperventilação profilática), PaO2 >= 80 mmHg, PAM >= 80 mmHg (para manter Pressão de Perfusão Cerebral PPC > 60 mmHg), temperatura 36-37°C e glicemia 140-180 mg/dL.",
                        "interventionalProcedure": "Avaliação neurocirúrgica imediata para craniotomia descompressiva / monitorização de Pressão Intracraniana (PIC).",
                        "ventilatorySupport": "Ventilação mecânica protetora controlada a volume, evitando PEEP excessiva (> 10-12 cmH2O) que reduza retorno venoso cerebral."
                    }
                ]
            }
        ]
    }

def get_four():
    return {
        "id": "calc_four",
        "slug": "four-score",
        "name": "Escala FOUR (Full Outline of UnResponsiveness)",
        "acronym": "FOUR Score",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Coma, Nível de Consciência e Sedação",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Coma, Nível de Consciência e Sedação",
        "description": "Escala de avaliação de coma para pacientes de UTI e intubados com avaliação de tronco e drive respiratório (0 a 16 pontos).",
        "summary": "Escala de coma sem dependência de resposta verbal para pacientes intubados e críticos.",
        "clinicalObjective": "Avaliação neurológica precisa em pacientes sob ventilação mecânica, detecção de estado de Locked-in e triagem de morte encefálica.",
        "targetPopulation": "Pacientes críticos intubados ou em coma na UTI e emergência.",
        "calculationType": "additive_points",
        "formulaExpression": "Olhos + Motor + Tronco + Respiracao",
        "evidenceSource": "Wijdicks EF, Bamlet WR, Maramattom BV, Manno EM, McClelland RL. Validation of a new coma scale: The FOUR score. Ann Neurol. 2005;58(4):585-593.",
        "minPossibleScore": 0,
        "maxPossibleScore": 16,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_four_eye", "label": "Olhos (Eye)", "system": "Neurológico", "baselineValue": 4, "maxAxisValue": 0},
            {"id": "axis_four_mot", "label": "Motor (Motor)", "system": "Neurológico", "baselineValue": 4, "maxAxisValue": 0},
            {"id": "axis_four_stem", "label": "Tronco (Brainstem)", "system": "Neurológico", "baselineValue": 4, "maxAxisValue": 0},
            {"id": "axis_four_resp", "label": "Respiração (Respiration)", "system": "Respiratório", "baselineValue": 4, "maxAxisValue": 0}
        ],
        "parameterGroups": [
            {
                "id": "grp_four_eye",
                "name": "1. Resposta Ocular (Eye: 0 a 4)",
                "slug": "olhos-four",
                "inputType": "single_choice",
                "radarAxisId": "axis_four_eye",
                "normalBaselineValue": 4,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_fe_4", "label": "4 = Pálpebras abertas, rastreia ou pisca ao comando", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_fe_3", "label": "3 = Pálpebras abertas, mas não rastreia estímulo", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_fe_2", "label": "2 = Pálpebras fechadas, abrem à voz alta", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_fe_1", "label": "1 = Pálpebras fechadas, abrem somente à dor", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_fe_0", "label": "0 = Pálpebras permanecem fechadas mesmo à dor", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_four_mot",
                "name": "2. Resposta Motora (Motor: 0 a 4)",
                "slug": "motor-four",
                "inputType": "single_choice",
                "radarAxisId": "axis_four_mot",
                "normalBaselineValue": 4,
                "maxAxisValue": 4,
                "sortOrder": 2,
                "options": [
                    {"id": "opt_fm_4", "label": "4 = Faz sinal de positivo (polegar), punho fechado ou paz", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_fm_3", "label": "3 = Localiza a dor (cruza a linha média)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_fm_2", "label": "2 = Resposta flexora à dor (decorticação)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_fm_1", "label": "1 = Resposta extensora à dor (descerebração)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_fm_0", "label": "0 = Nenhuma resposta à dor ou mioclonias generalizadas", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_four_stem",
                "name": "3. Tronco Encefálico (Brainstem: 0 a 4)",
                "slug": "tronco-four",
                "inputType": "single_choice",
                "radarAxisId": "axis_four_stem",
                "normalBaselineValue": 4,
                "maxAxisValue": 4,
                "sortOrder": 3,
                "options": [
                    {"id": "opt_fs_4", "label": "4 = Reflexos pupilar E corneano presentes bilateralmente", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_fs_3", "label": "3 = Uma pupila dilatada e fixa (anisocoria)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_fs_2", "label": "2 = Reflexo pupilar OU corneano ausente", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_fs_1", "label": "1 = Ambos os reflexos pupilar E corneano ausentes", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_fs_0", "label": "0 = Reflexos pupilar, corneano E de tosse ao aspirar tubo ausentes", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            },
            {
                "id": "grp_four_resp",
                "name": "4. Respiração e Ventilação (Respiration: 0 a 4)",
                "slug": "respiracao-four",
                "inputType": "single_choice",
                "radarAxisId": "axis_four_resp",
                "normalBaselineValue": 4,
                "maxAxisValue": 4,
                "sortOrder": 4,
                "options": [
                    {"id": "opt_fr_4", "label": "4 = Não intubado, padrão respiratório regular", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_fr_3", "label": "3 = Não intubado, respiração de Cheyne-Stokes", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2},
                    {"id": "opt_fr_2", "label": "2 = Não intubado, respiração irregular / atáxica", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3},
                    {"id": "opt_fr_1", "label": "1 = Intubado, respira acima do ventilador mecânico (drive preservado)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4},
                    {"id": "opt_fr_0", "label": "0 = Intubado, respira na frequência mandatória do aparelho (apneia)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_four_high_score",
                "label": "Disfunção Leve a Moderada (13 a 16 pontos)",
                "severityLevel": "low",
                "minScore": 13,
                "maxScore": 16,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada < 5%. Reflexos de tronco e drive respiratório preservados.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_four_1", "recommendationTitle": "Desmame Ventilatório e Vigilância", "dispositionTarget": "UTI", "monitoringPlan": "Avaliar teste de respiração espontânea se estabilização clínica."}
                ]
            },
            {
                "id": "tier_four_mod",
                "label": "Coma Moderado (8 a 12 pontos)",
                "severityLevel": "intermediate",
                "minScore": 8,
                "maxScore": 12,
                "statisticalOutcome": "Risco de deterioração clínica em 48h > 25%. Mortalidade estimada em 15% a 30%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_four_2", "recommendationTitle": "Neuroproteção e Tomografia", "dispositionTarget": "UTI", "monitoringPlan": "Vigilância pupilar e gasométrica contínua."}
                ]
            },
            {
                "id": "tier_four_low_score",
                "label": "Coma Profundo / Alto Risco de Óbito (0 a 7 pontos)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 7,
                "statisticalOutcome": "Mortalidade hospitalar superior a 75% a 90%. Se FOUR = 0 persistente na ausência de sedativos e normotérmico, alerta para protocolo de Morte Encefálica.",
                "colorHex": "#b91c1c",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_four_3",
                        "recommendationTitle": "Investigação de Morte Encefálica ou Suporte Neurointensivo Máximo",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "Se FOUR = 0 persistente, abrir protocolo formal de Morte Encefálica (ME) conforme Resolução CFM nº 2.173/2017.",
                        "ventilatorySupport": "Ventilação mecânica invasiva contínua."
                    }
                ]
            }
        ]
    }

def get_rass():
    return {
        "id": "calc_rass",
        "slug": "rass-score",
        "name": "Escala de Agitação e Sedação de Richmond (RASS)",
        "acronym": "RASS",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Coma, Nível de Consciência e Sedação",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Coma, Nível de Consciência e Sedação",
        "description": "Escala padronizada de 10 níveis (-5 a +4) para titulação diária de sedação e metas em pacientes críticos.",
        "summary": "Escala de 10 pontos (-5 a +4) para monitorização e titulação de sedativos e analgésicos em UTI.",
        "clinicalObjective": "Evitar supersedação iatrogênica e direcionar sedação consciente leve (RASS -1 a 0) conforme diretrizes PADIS.",
        "targetPopulation": "Pacientes internados em UTI recebendo sedativos ou em ventilação mecânica.",
        "calculationType": "additive_points",
        "evidenceSource": "Sessler CN, Gosnell MS, Grap MJ, et al. The Richmond Agitation-Sedation Scale: validity and reliability in adult intensive care unit patients. Am J Respir Crit Care Med. 2002;166(10):1338-1344.",
        "minPossibleScore": -5,
        "maxPossibleScore": 4,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_rass", "label": "Nível RASS", "system": "Sedação", "baselineValue": 0, "maxAxisValue": 5}
        ],
        "parameterGroups": [
            {
                "id": "grp_rass_level",
                "name": "Nível Comportamental RASS",
                "slug": "nivel-rass",
                "inputType": "single_choice",
                "radarAxisId": "axis_rass",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_rass_p4", "label": "+4 = Combativo (Violento, perigo imediato para a equipe)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1},
                    {"id": "opt_rass_p3", "label": "+3 = Muito Agitado (Puxa tubos e cateteres, agressivo)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 2},
                    {"id": "opt_rass_p2", "label": "+2 = Agitado (Movimentos frequentes sem propósito, briga com VM)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 3},
                    {"id": "opt_rass_p1", "label": "+1 = Inquieto (Ansioso, mas movimentos não agressivos)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 4},
                    {"id": "opt_rass_0", "label": "0 = Alerta e Calmo (Meta ideal)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 5},
                    {"id": "opt_rass_m1", "label": "-1 = Sonolento (Abre olhos à voz por > 10 segundos)", "pointValue": -1, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 6},
                    {"id": "opt_rass_m2", "label": "-2 = Sedação Leve (Desperta brevemente à voz < 10 segundos)", "pointValue": -2, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 7},
                    {"id": "opt_rass_m3", "label": "-3 = Sedação Moderada (Movimenta-se à voz sem contato visual)", "pointValue": -3, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 8},
                    {"id": "opt_rass_m4", "label": "-4 = Sedação Profunda (Sem resposta à voz, abre olhos apenas à dor)", "pointValue": -4, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 9},
                    {"id": "opt_rass_m5", "label": "-5 = Não Despertável (Sem resposta a nenhum estímulo verbal ou doloroso)", "pointValue": -5, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 10}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_rass_agitated",
                "label": "Agitação Psicomotora (+1 a +4)",
                "severityLevel": "high",
                "minScore": 1,
                "maxScore": 4,
                "statisticalOutcome": "Risco de auto-extubação acidental, perda de cateteres invasivos e hipertermia.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_rass_agit",
                        "drugName": "Analgesia Inicial seguida de Dexmedetomidina ou Antipsicótico",
                        "dosage": "Fentanil 1 mcg/kg IV bolus ou Dexmedetomidina 0,2 a 1,4 mcg/kg/h",
                        "route": "IV",
                        "frequency": "Contínua",
                        "indication": "Controle de dor como primeiro passo; titulação para RASS 0 a -1."
                    }
                ],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_rass_1", "recommendationTitle": "Revisão de Causas de Agitação", "dispositionTarget": "UTI", "monitoringPlan": "Descartar dor, hipóxia, retenção urinária ou delirium hiperativo."}
                ]
            },
            {
                "id": "tier_rass_target",
                "label": "Meta Terapêutica / Sedação Consciente (-2 a 0)",
                "severityLevel": "low",
                "minScore": -2,
                "maxScore": 0,
                "statisticalOutcome": "Faixa alvo recomendada pelas diretrizes PADIS para menor tempo de ventilação mecânica e menor permanência na UTI.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_rass_2", "recommendationTitle": "Manutenção de Sedação Leve", "dispositionTarget": "UTI", "monitoringPlan": "Despertar diário matinal programado e fisioterapia motora precoce."}
                ]
            },
            {
                "id": "tier_rass_deep",
                "label": "Sedação Profunda / Coma Induzido (-5 a -3)",
                "severityLevel": "intermediate",
                "minScore": -5,
                "maxScore": -3,
                "statisticalOutcome": "Aumento do tempo de VM e risco de polineuropatia do doente crítico. Indicado apenas em SDRA grave com bloqueio neuromuscular, estado de mal epiléptico ou hipertensão intracraniana.",
                "colorHex": "#6366f1",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_rass_3", "recommendationTitle": "Redução Gradual de Sedativos", "dispositionTarget": "UTI", "monitoringPlan": "Se não houver indicação formal de sedação profunda, reduzir vazão de hipnóticos em 20-30%."}
                ]
            }
        ]
    }

def get_sas():
    return {
        "id": "calc_sas",
        "slug": "sas-score",
        "name": "Escala de Sedação e Agitação de Riker (SAS)",
        "acronym": "SAS",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Coma, Nível de Consciência e Sedação",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Coma, Nível de Consciência e Sedação",
        "description": "Escala comportamental alternativa de 7 níveis (1 a 7) para pacientes críticos em UTI.",
        "summary": "Escala de sedação e agitação de Riker (1 a 7) para monitorização em terapia intensiva.",
        "clinicalObjective": "Classificação da profundidade da sedação e agitação motora em pacientes sob terapia intensiva.",
        "targetPopulation": "Pacientes internados em UTI.",
        "calculationType": "additive_points",
        "evidenceSource": "Riker RR, Picard JT, Fraser GL. Prospective evaluation of the Sedation-Agitation Scale for adult critically ill patients. Crit Care Med. 1999;27(7):1325-1329.",
        "minPossibleScore": 1,
        "maxPossibleScore": 7,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_sas", "label": "Escore SAS", "system": "Sedação", "baselineValue": 4, "maxAxisValue": 7}
        ],
        "parameterGroups": [
            {
                "id": "grp_sas_level",
                "name": "Classificação SAS (1 a 7)",
                "slug": "nivel-sas",
                "inputType": "single_choice",
                "radarAxisId": "axis_sas",
                "normalBaselineValue": 4,
                "maxAxisValue": 7,
                "sortOrder": 1,
                "options": [
                    {"id": "opt_sas_7", "label": "7 = Agitação Perigosa (Puxa tubo endotraqueal, tenta sair do leito)", "pointValue": 7, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1},
                    {"id": "opt_sas_6", "label": "6 = Muito Agitado (Não se acalma apesar de explicação verbal)", "pointValue": 6, "isNormalBaseline": False, "radarNormalizedValue": 0.83, "sortOrder": 2},
                    {"id": "opt_sas_5", "label": "5 = Agitado (Ansioso ou levemente agitado, tenta sentar)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_sas_4", "label": "4 = Calmo e Cooperativo (Meta ideal)", "pointValue": 4, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 4},
                    {"id": "opt_sas_3", "label": "3 = Sedado (Desperta ao chamado ou estímulo leve, mas volta a dormir)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 5},
                    {"id": "opt_sas_2", "label": "2 = Muito Sedado (Desperta apenas ao estímulo doloroso central)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 6},
                    {"id": "opt_sas_1", "label": "1 = Não Despertável (Sem resposta ou resposta mínima à dor)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 7}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_sas_agit",
                "label": "Agitação (SAS 5 a 7)",
                "severityLevel": "high",
                "minScore": 5,
                "maxScore": 7,
                "statisticalOutcome": "Risco de perda acidental de dispositivos e exaustão metabólica.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_sas_1", "recommendationTitle": "Controle de Agitação e Dor", "dispositionTarget": "UTI", "monitoringPlan": "Avaliar analgesia e sedação leve."}
                ]
            },
            {
                "id": "tier_sas_opt",
                "label": "Calmo / Meta Adequada (SAS 3 a 4)",
                "severityLevel": "low",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Faixa alvo ideal para ventilação mecânica confortável e desmame.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_sas_2", "recommendationTitle": "Manutenção de Sedação Adequada", "dispositionTarget": "UTI", "monitoringPlan": "Vigilância rotineira de UTI."}
                ]
            },
            {
                "id": "tier_sas_deep",
                "label": "Sedação Profunda / Coma (SAS 1 a 2)",
                "severityLevel": "intermediate",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Risco de complicações de imobilidade e ventilação prolongada.",
                "colorHex": "#6366f1",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_sas_3", "recommendationTitle": "Reavaliação de Necessidade de Sedação", "dispositionTarget": "UTI", "monitoringPlan": "Reduzir drogas sedativas salvo indicação formal."}
                ]
            }
        ]
    }

def get_cam_icu():
    return {
        "id": "calc_cam_icu",
        "slug": "cam-icu",
        "name": "CAM-ICU (Confusion Assessment Method for the ICU)",
        "acronym": "CAM-ICU",
        "version": "1.0.0",
        "category": "Emergência, Choque e Terapia Intensiva",
        "subcategory": "Coma, Nível de Consciência e Sedação",
        "categorySlug": "bloco-01-emergencia-choque-uti",
        "categoryName": "Emergência, Choque e Terapia Intensiva",
        "moduleName": "Coma, Nível de Consciência e Sedação",
        "description": "Algoritmo padronizado de triagem de Delirium à beira do leito em pacientes críticos sob ventilação mecânica ou fora dela.",
        "summary": "Diagnóstico rápido de Delirium em terapia intensiva baseado em 4 características objetivas.",
        "clinicalObjective": "Detecção precoce de delirium em pacientes de UTI para intervenção não farmacológica imediata e redução da mortalidade hospitalar.",
        "targetPopulation": "Pacientes de UTI com RASS >= -3 (inaplicável em sedação profunda RASS -4 ou -5).",
        "calculationType": "branching_decision",
        "evidenceSource": "Ely EW, Inouye SK, Bernard GR, et al. Delirium in mechanically ventilated patients: validity and reliability of the confusion assessment method for the intensive care unit (CAM-ICU). JAMA. 2001;286(21):2703-2710.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "badge": "uti",
        "radarAxes": [
            {"id": "axis_cam", "label": "Features CAM-ICU", "system": "Delirium", "baselineValue": 0, "maxAxisValue": 4}
        ],
        "parameterGroups": [
            {
                "id": "grp_cam_feat1",
                "name": "Característica 1: Início Agudo ou Curso Flutuante",
                "slug": "inicio-agudo",
                "inputType": "single_choice",
                "radarAxisId": "axis_cam",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Há evidência de alteração aguda no estado mental em relação ao basal ou o comportamento flutuou nas últimas 24 horas?",
                "options": [
                    {"id": "opt_cam_f1_no", "label": "Não (Ausente: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_cam_f1_yes", "label": "Sim (Presente: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_cam_feat2",
                "name": "Característica 2: Inatenção (Teste das Letras S-A-V-E-A-H-A-A-R-T)",
                "slug": "inatencao",
                "inputType": "single_choice",
                "radarAxisId": "axis_cam",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Aperte a mão na letra 'A'. Erros = não apertar no 'A' ou apertar em outra letra. Mais de 2 erros = inatenção presente.",
                "options": [
                    {"id": "opt_cam_f2_no", "label": "0 a 2 erros (Atenção normal: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_cam_f2_yes", "label": "> 2 erros (Inatenção confirmada: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_cam_feat3",
                "name": "Característica 3: Nível de Consciência Alterado (RASS Atual)",
                "slug": "nivel-consciencia-rass",
                "inputType": "single_choice",
                "radarAxisId": "axis_cam",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "O RASS atual do paciente é diferente de ZERO?",
                "options": [
                    {"id": "opt_cam_f3_no", "label": "RASS = 0 (Alerta e calmo: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_cam_f3_yes", "label": "RASS diferente de 0 (+1 a +4 ou -1 a -3: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_cam_feat4",
                "name": "Característica 4: Pensamento Desorganizado",
                "slug": "pensamento-desorganizado",
                "inputType": "single_choice",
                "radarAxisId": "axis_cam",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Perguntas de lógica simples (ex.: 'Uma pedra flutua na água?') e comando motor. Mais de 1 erro = pensamento desorganizado.",
                "options": [
                    {"id": "opt_cam_f4_no", "label": "0 a 1 erro (Normal: 0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_cam_f4_yes", "label": "> 1 erro (Pensamento desorganizado: +1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_cam_neg",
                "label": "CAM-ICU Negativo (Sem Delirium)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Critérios para Delirium não preenchidos. Manter medidas de prevenção não farmacológicas.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {"id": "nonrx_cam_1", "recommendationTitle": "Prevenção de Delirium (Pacote ABCDEF)", "dispositionTarget": "UTI", "monitoringPlan": "Mobilização precoce, preservação do ciclo circadiano sono-vigília e uso de óculos/aparelhos auditivos."}
                ]
            },
            {
                "id": "tier_cam_pos",
                "label": "CAM-ICU Positivo (Delirium Confirmado)",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Diagnóstico de Delirium confirmado (presença obrigatória de Característica 1 E 2 + Característica 3 OU 4). Aumento de 3x na mortalidade hospitalar e tempo de permanência prolongado.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_cam_pos",
                        "drugName": "Haloperidol ou Quetiapina (Apenas se agitação refratária com risco físico)",
                        "dosage": "Haloperidol 1 a 2,5 mg IV ou Quetiapina 25 a 50 mg VO",
                        "route": "IV / VO",
                        "frequency": "Se necessário",
                        "contraindications": "Evitar uso profilático de antipsicóticos; monitorar intervalo QTc no ECG (suspender se QTc > 500 ms)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_cam_2",
                        "recommendationTitle": "Intervenção Multimodal Imediata para Delirium",
                        "dispositionTarget": "UTI",
                        "monitoringPlan": "1. Investigar causas reversíveis (Mnemonic D-E-L-I-R-I-U-M: Drogas, Eletrólitos, Low O2/hipóxia, Infecção, Retenção urinária/fecal, Isquemia, UTI ambiente).\n2. Suspender benzodiazepínicos se presentes.\n3. Presença de familiares e reorientação temporal/espacial contínua."
                    }
                ]
            }
        ]
    }
