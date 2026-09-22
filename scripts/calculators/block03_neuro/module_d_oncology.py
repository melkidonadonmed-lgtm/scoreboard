"""
Block 03: Neurologia e Neurocirurgia
Módulo D: Neuro-Oncologia e Hidrodinâmica Cerebral
Calculadoras Clínicas Monográficas:
1. Classificação de Knosp (Invasão do Seio Cavernoso em Macroadenomas Hipofisários)
2. Classificação de Samii & Koos (Schwannoma Vestibular / Neurinoma do Acústico)
3. DS-GPA & RPA (Diagnosis-Specific Graded Prognostic Assessment para Metástases Cerebrais)
4. KPS (Karnofsky Performance Status) & ECOG
5. Escala de Kiefer (Graduação Clínica para Hidrocefalia de Pressão Normal - HPN)
6. Índice de Evans & Sinais de DESH (Hidrocefalia de Pressão Normal)
"""

from calculators.block03_neuro.functional_cognitive import get_kps

def get_knosp():
    return {
        "id": "calc_knosp",
        "slug": "knosp",
        "name": "Classificação de Knosp para Invasão do Seio Cavernoso",
        "acronym": "Knosp",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neuro-Oncologia e Base do Crânio",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neuro-Oncologia e Base do Crânio",
        "description": "Graduação tomográfica e por ressonância magnética (RM) coronal para estimativa do risco de invasão verdadeira da artéria carótida interna e dos compartimentos do seio cavernoso em adenomas de hipófise, orientando a viabilidade de ressecção endoscópica endonasal e necessidade de radiocirurgia pós-operatória.",
        "summary": "Graduação radiológica coronal (Graus 0 a 4) para predição de invasão do seio cavernoso e ressecabilidade em macroadenomas hipofisários.",
        "clinicalObjective": "Determinar a probabilidade de invasão verdadeira do seio cavernoso, orientando o planejamento cirúrgico (ressecção endoscópica transesfenoidal curativa vs. descompressão do quiasma e radiocirurgia adjuvante).",
        "targetPopulation": "Pacientes com macroadenomas ou tumores selares/parasselares avaliados por Ressonância Magnética com contraste em cortes coronais ponderados em T1.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_Knosp_Selecionado",
        "evidenceSource": "Knosp E, Steiner E, Kitz K, Matula C. Pituitary adenomas with invasion of the cavernous sinus space: a magnetic resonance imaging classification compared with surgical findings. Neurosurgery. 1993;33(4):610-618.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neuro-oncologia",
        "clinicalWarning": "ATENÇÃO: Os Graus 0 a 2 apresentam probabilidade muito baixa de invasão verdadeira da parede medial do seio cavernoso, possibilitando taxas de ressecção tumoral completa > 85-95%. O Grau 3 divide-se em 3A (extensão acima da carótida horizontal para o compartimento superior) e 3B (extensão abaixo da carótida horizontal para o compartimento inferior). O Grau 4 define envolvimento circunferencial (encasement de 360°) da artéria carótida interna intracavernosa, com invasão dural comprovada e indicação primordial de descompressão quiasmática associada a radiocirurgia adjuvante.",
        "radarAxes": [
            {
                "id": "axis_knosp_invasion",
                "label": "Grau de Invasão Cavernosa",
                "system": "Oncológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 4
            },
            {
                "id": "axis_knosp_resectability",
                "label": "Risco de Remanescente Tumoral",
                "system": "Cirúrgico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 4
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_knosp_grade",
                "name": "Grau da Classificação de Knosp (Corte Coronal T1 com Gadolínio)",
                "slug": "grau-knosp",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_knosp_invasion",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "helpText": "Avalie as linhas tangentes intercarotídeas coronal que unem as artérias carótidas internas intracavernosa e supra-clinoideia.",
                "options": [
                    {
                        "id": "opt_knosp_0",
                        "label": "Grau 0: Medial à linha tangente medial",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "O tumor não ultrapassa a linha medial que une as bordas mediais da ACI intracavernosa e supra-clinoideia. Seio cavernoso completamente livre."
                    },
                    {
                        "id": "opt_knosp_1",
                        "label": "Grau 1: Ultrapassa linha medial, medial à intercarotídea",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "O tumor ultrapassa a linha medial, porém não alcança a linha intercarotídea (linha que conecta os centros das secções da ACI). Risco mínimo de invasão verdadeira."
                    },
                    {
                        "id": "opt_knosp_2",
                        "label": "Grau 2: Ultrapassa linha intercarotídea, medial à linha lateral",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 3,
                        "description": "O tumor ultrapassa a linha intercarotídea, mas não alcança a linha lateral tangent à borda lateral das carótidas. Invasão histológica duvidosa."
                    },
                    {
                        "id": "opt_knosp_3a",
                        "label": "Grau 3A: Ultrapassa linha lateral superiormente (Compartimento Cavernoso Superior)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "O tumor estende-se além da linha lateral no compartimento superior do seio cavernoso. Invasão verdadeira em > 60-80% dos casos; risco elevado de remanescente."
                    },
                    {
                        "id": "opt_knosp_3b",
                        "label": "Grau 3B: Ultrapassa linha lateral inferiormente (Compartimento Cavernoso Inferior)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 5,
                        "description": "O tumor estende-se além da linha lateral no compartimento inferior do seio cavernoso. Invasão confirmada; dissecção complexa."
                    },
                    {
                        "id": "opt_knosp_4",
                        "label": "Grau 4: Encasement carotídeo circunferencial total (360°)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 6,
                        "description": "Envolvimento circunferencial completo da ACI intracavernosa. Invasão dural e do seio cavernoso 100% confirmada; lesão não ressecável radicalmente por via transesfenoidal padrão."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_knosp_low",
                "label": "Knosp Graus 0 e 1: Ausência de Invasão Cavernosa",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Taxa de Ressecção Macroscópica Completa (GTR) de 95% a 100%. Risco de invasão histológica do seio cavernoso < 2%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_knosp_cabergolina",
                        "drugName": "Cabergolina",
                        "dosage": "0,5 mg VO por semana",
                        "route": "Oral",
                        "frequency": "1 a 2 vezes por semana",
                        "contraindications": "Doença valvar cardíaca grave conhecida, hipersensibilidade a derivados do ergot."
                    },
                    {
                        "id": "rx_knosp_hidrocortisona",
                        "drugName": "Acetato de Hidrocortisona",
                        "dosage": "20 mg pela manhã e 10 mg às 14h",
                        "route": "Oral",
                        "frequency": "2 vezes ao dia",
                        "contraindications": "Infecção fúngica sistêmica ativa não tratada."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_knosp_eets",
                        "recommendationTitle": "Cirurgia Endoscópica Transesfenoidal (EETS)",
                        "dispositionTarget": "Enfermaria de Neurocirurgia",
                        "monitoringPlan": "Ressonância magnética de controle em 3 meses de pós-operatório para confirmação de ressecção macroscópica completa.",
                        "interventionalProcedure": "Acesso endonasal binostril guiado por óptica de 0° e 30°, abertura do seio esfenoidal e da fáscia selar, com ressecção curativa e reconstrução selar com enxerto de mucosa/fáscia se fístula liquórica."
                    }
                ]
            },
            {
                "id": "tier_knosp_mod",
                "label": "Knosp Grau 2: Invasão Duvidosa / Caso Limítrofe",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de Ressecção Macroscópica Completa de 75% a 85%. Risco de invasão histológica da parede medial do seio cavernoso de aproximadamente 15% a 25%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_knosp_levotiroxina",
                        "drugName": "Levotiroxina Sódica",
                        "dosage": "50 a 100 mcg/dia",
                        "route": "Oral",
                        "frequency": "1 vez ao dia em jejum",
                        "contraindications": "Tireotoxicose não tratada, infarto agudo do miocárdio recente."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_knosp_doppler",
                        "recommendationTitle": "Microdoppler Vascular e Monitorização Selar",
                        "dispositionTarget": "Enfermaria de Neurocirurgia",
                        "monitoringPlan": "RM de crânio com protocolo selar e dosagem do perfil hormonal hipofisário completo no seguimento precoce.",
                        "interventionalProcedure": "Dissecção cuidadosa da parede medial da carótida interna intracavernosa com auxílio de microdoppler vascular."
                    }
                ]
            },
            {
                "id": "tier_knosp_high",
                "label": "Knosp Grau 3 (3A/3B): Invasão Cavernosa Confirmada",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Taxa de Ressecção Completa de apenas 25% a 45%. Invasão histológica do espaço cavernoso documentada em 60% a 85% dos casos. Alto risco de resíduo tumoral.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_knosp_octreotide",
                        "drugName": "Acetato de Octreotide LAR",
                        "dosage": "20 a 30 mg IM",
                        "route": "Intramuscular",
                        "frequency": "A cada 4 semanas",
                        "contraindications": "Hipersensibilidade conhecida à octreotida."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_knosp_srs",
                        "recommendationTitle": "Ressecção Subtotal + Radiocirurgia Estereotáxica (SRS)",
                        "dispositionTarget": "UTI Neurocirúrgica / Enfermaria",
                        "monitoringPlan": "Mapeamento volumétrico do remanescente tumoral intracavernoso por RM aos 3 meses de PO para planejamento de Radiocirurgia.",
                        "interventionalProcedure": "Ressecção subtotal intencional visando descompressão quiasmática ampla e preservação estrita da integridade carotídea."
                    }
                ]
            },
            {
                "id": "tier_knosp_encased",
                "label": "Knosp Grau 4: Encasement Carotídeo Circunferencial (360°)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Taxa de Ressecção Curativa Radical < 5% a 10%. Invasão dural e intracavernosa de 100%. Lesão irressecável radicalmente por via transesfenoidal padrão.",
                "colorHex": "#7f1d1d",
                "pharmacologicalActions": [
                    {
                        "id": "rx_knosp_dexametasona",
                        "drugName": "Dexametasona",
                        "dosage": "4 mg IV",
                        "route": "Intravenosa",
                        "frequency": "12/12h",
                        "contraindications": "Infecções fúngicas sistêmicas não controladas."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_knosp_decompression",
                        "recommendationTitle": "Descompressão Quiasmática e Radioterapia Fracionada",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Avaliação oftalmológica com campimetria visual computadorizada e acuidade visual seriada.",
                        "interventionalProcedure": "Descompressão do nervo óptico e quiasma óptico por via endonasal com suspensão de dissecção na carótida, encaminhando para radioterapia estereotáxica externa fracionada."
                    }
                ]
            }
        ]
    }

def get_samii_koos():
    return {
        "id": "calc_samii_koos",
        "slug": "samii-koos",
        "name": "Classificação de Samii & Koos para Schwannoma Vestibular",
        "acronym": "Samii-Koos",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neuro-Oncologia e Base do Crânio",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neuro-Oncologia e Base do Crânio",
        "description": "Sistema de estadiamento anatômico para schwannomas vestibulares (neurinomas do acústico) no meato acústico interno e ângulo pontocerebelar (APC), correlacionando volume tumoral, compressão do tronco encefálico e função do nervo facial (House-Brackmann) para decisão terapêutica entre conduta expectante, radiocirurgia e microcirurgia.",
        "summary": "Estadiamento anatômico de schwannomas vestibulares (Graus I a IV) e correlação com risco de hidrocefalia e preservação do nervo facial.",
        "clinicalObjective": "Estratificar o risco cirúrgico de paralisia facial, compressão de tronco e hidrocefalia obstrutiva, orientando indicação de radiocirurgia (SRS) vs cirurgia via retrosigmoidea/translabiríntica.",
        "targetPopulation": "Pacientes portadores de lesões expansivas no meato acústico interno ou ângulo pontocerebelar compatíveis com schwannoma vestibular na RM.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_Koos_Selecionado",
        "evidenceSource": "Koos WT, Day JD, Matula C, Levy DI. Neurotopographic considerations in the microsurgical resection of small acoustic neurinomas. J Neurosurg. 1998;88(3):506-512; Samii M, Matthies C. Management of 1000 vestibular schwannomas: surgical considerations. Neurosurgery. 1997;40(4):710-728.",
        "minPossibleScore": 1,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neuro-oncologia",
        "clinicalWarning": "ALERTA DE SEGURANÇA MÁXIMA: Lesões Grau IV (Samii T4b / Koos IV) com deformação severa do 4º ventrículo e hidrocefalia obstrutiva aguda apresentam risco iminente de herniação tonsilar ou transtentorial. Se houver hipertensão intracraniana descompensada, deve-se realizar Derivação Ventricular Externa (DVE) de emergência antes da descompressão definitiva de fossa posterior. A monitorização intraoperatória neurofisiológica contínua dos nervos facial (VII) e coclear (VIII) é mandatória.",
        "radarAxes": [
            {
                "id": "axis_koos_size",
                "label": "Extensão Anatômica no APC",
                "system": "Oncológico",
                "unit": "grau",
                "baselineValue": 1,
                "maxAxisValue": 4
            },
            {
                "id": "axis_koos_stem",
                "label": "Compressão de Tronco / 4º Ventrículo",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 1,
                "maxAxisValue": 4
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_koos_grade",
                "name": "Estadiamento Anatômico (Koos / Samii)",
                "slug": "estadiamento-koos-samii",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_koos_size",
                "normalBaselineValue": 1,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "helpText": "Selecione o grau de extensão do schwannoma no meato acústico interno e ângulo pontocerebelar.",
                "options": [
                    {
                        "id": "opt_koos_1",
                        "label": "Grau I (Samii T1): Puramente intrameatal",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 1,
                        "description": "Tumor estritamente confinado ao conduto auditivo interno (CAI); sem extensão cisternal para o ângulo pontocerebelar."
                    },
                    {
                        "id": "opt_koos_2",
                        "label": "Grau II (Samii T2): Pequeno intra-extrameatal (<= 20 mm)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 2,
                        "description": "Extensão para o ângulo pontocerebelar, porém sem atingir o tronco encefálico (diâmetro cisternal máximo <= 20 mm)."
                    },
                    {
                        "id": "opt_koos_3",
                        "label": "Grau III (Samii T3a/b): Contato com tronco sem deformação (<= 30 mm)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 3,
                        "description": "Tumor volumoso no APC em contato direto com a ponte/bulbo, porém sem compressão, deslocamento ou distorção anatômica do tronco."
                    },
                    {
                        "id": "opt_koos_4",
                        "label": "Grau IV (Samii T4a/b): Tumor volumoso (> 30 mm) com compressão de tronco e 4º ventrículo",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Tumor gigante (> 30 mm) causando severa deformação do tronco encefálico, deslocamento do 4º ventrículo e risco crítico de hidrocefalia obstrutiva."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_koos_1",
                "label": "Koos Grau I: Tumor Intrameatal Puro",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Taxa de preservação anatômica do nervo facial de 98% a 100%. Preservação auditiva útil em 60% a 80% dos casos tratados com microcirurgia/SRS.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_koos_prednisona",
                        "drugName": "Prednisona",
                        "dosage": "1 mg/kg/dia",
                        "route": "Oral",
                        "frequency": "1 vez ao dia por 7 dias",
                        "contraindications": "Infecção fúngica ativa."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_koos_scan",
                        "recommendationTitle": "Protocolo Wait-and-Scan com Audiometria Seriada",
                        "dispositionTarget": "Ambulatório de Neurocirurgia",
                        "monitoringPlan": "Protocolo Wait-and-Scan com RM de controle a cada 6 a 12 meses em idosos ou pacientes assintomáticos.",
                        "interventionalProcedure": "Radiocirurgia Estereotáxica (11 a 12 Gy) ou Cirurgia via fossa média em casos de crescimento ativo com audição preservada."
                    }
                ]
            },
            {
                "id": "tier_koos_2",
                "label": "Koos Grau II: Tumor Cisternal Pequeno (<= 20 mm)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de controle tumoral com Radiocirurgia de 92% a 97% aos 5 anos. Preservação da função facial (House-Brackmann I-II) em 95%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_koos_lubrificante",
                        "drugName": "Colírio Lubrificante (Carmelose 0,5%)",
                        "dosage": "1 a 2 gotas no olho ipsilateral",
                        "route": "Ocular",
                        "frequency": "A cada 2 a 4 horas",
                        "contraindications": "Hipersensibilidade ao princípio ativo."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_koos_srs",
                        "recommendationTitle": "Radiocirurgia Estereotáxica (SRS)",
                        "dispositionTarget": "Ambulatório / Hospital-Dia",
                        "monitoringPlan": "RM anual de alta resolução para avaliar taxa de crescimento volumétrico.",
                        "interventionalProcedure": "Radiocirurgia Estereotáxica (Gamma Knife / Linac) como opção primária de preservação neural vs Acesso Retrosigmoideo."
                    }
                ]
            },
            {
                "id": "tier_koos_3",
                "label": "Koos Grau III: Contato com Tronco sem Deformação",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Preservação da mímica facial normal/ótima (HB I-II) de 80% a 90% com monitorização neurofisiológica intraoperatória contínua.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_koos_dexametasona",
                        "drugName": "Dexametasona",
                        "dosage": "4 mg IV",
                        "route": "Intravenosa",
                        "frequency": "8/8h",
                        "contraindications": "Hipersensibilidade conhecida."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_koos_mio",
                        "recommendationTitle": "Microcirurgia Retrosigmoidea com MIO Contínua",
                        "dispositionTarget": "UTI Neurocrítica / Enfermaria",
                        "monitoringPlan": "Potenciais evocados auditivos de tronco encefálico (BAEP) e eletroneuromiografia de face pré e pós-operatória.",
                        "interventionalProcedure": "Microcirurgia eletiva por craniotomia retrosigmoidea suboccipital com descompressão capsular interna e preservação do VII par."
                    }
                ]
            },
            {
                "id": "tier_koos_4",
                "label": "Koos Grau IV: Compressão Grave de Tronco e 4º Ventrículo",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Alto risco de paralisia facial pós-operatória (HB III a VI em 20-35% dos casos). Risco de hidrocefalia aguda descompensada e óbito se não tratado.",
                "colorHex": "#7f1d1d",
                "pharmacologicalActions": [
                    {
                        "id": "rx_koos_dexametasona_crit",
                        "drugName": "Dexametasona",
                        "dosage": "8 mg IV bolus seguido por 4 mg IV",
                        "route": "Intravenosa",
                        "frequency": "6/6h",
                        "contraindications": "Infecção fúngica ativa."
                    },
                    {
                        "id": "rx_koos_pomada_ocular",
                        "drugName": "Pomada Oftálmica de Retinol + Aminoácidos",
                        "dosage": "Aplicar no saco conjuntival ao deitar",
                        "route": "Ocular",
                        "frequency": "1 vez ao dia (noturno)",
                        "contraindications": "Hipersensibilidade conhecida."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_koos_decompression_dve",
                        "recommendationTitle": "Descompressão Microcirúrgica de Fossa Posterior + DVE de Resgate",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Vigilância neurológica intensiva contínua em UTI neurocrítica quanto a sinais de hipertensão intracraniana e paresia de pares baixos (IX, X, XII).",
                        "interventionalProcedure": "Craniotomia retrosigmoidea com aspiração ultrassônica central vigorosa, preservação da interface aracnóidea do tronco e instalação de DVE se ventrículos dilatados pré-operatórios."
                    }
                ]
            }
        ]
    }

def get_ds_gpa():
    return {
        "id": "calc_ds_gpa",
        "slug": "ds-gpa",
        "name": "DS-GPA para Metástases Cerebrais",
        "acronym": "DS-GPA",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neuro-Oncologia e Metástases Cerebrais",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neuro-Oncologia e Metástases Cerebrais",
        "description": "Graded Prognostic Assessment específico por diagnóstico oncológico (DS-GPA) e análise particionada recursiva (RPA) para estimativa da sobrevida global mediana e orientação de conduta terapêutica entre ressecção cirúrgica de cavidade, radiocirurgia estereotáxica (SRS), radioterapia de encéfalo total (WBRT) e cuidados paliativos exclusivos.",
        "summary": "Escore prognóstico multimodal (0 a 4 pontos) preditor de sobrevida global em metástases cerebrais conforme a histologia primária.",
        "clinicalObjective": "Estimar com acurácia a sobrevida em meses e direcionar decisões de ressecção microcirúrgica vs. radiocirurgia (SRS) vs. suporte oncológico exclusivo.",
        "targetPopulation": "Pacientes portadores de metástases encefálicas secundárias a neoplasias sólidas (Pulmão [NSCLC/SCLC], Mama, Melanoma, Renal e Gastrointestinal).",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_KPS + Pontos_Idade + Pontos_Lesoes + Pontos_Sistemica",
        "evidenceSource": "Sperduto PW, Kased N, Roberge D, et al. Summary report on the graded prognostic assessment: an accurate and facile diagnosis-specific tool to estimate survival for patients with brain metastases. J Clin Oncol. 2012;30(4):419-425.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neuro-oncologia",
        "clinicalWarning": "ATENÇÃO: Pacientes com DS-GPA entre 3.0 e 4.0 apresentam sobrevida mediana prolongada (> 12 a 36 meses), justificando plenamente tratamentos locais agressivos (craniotomia com ressecção completa de lesão volumosa única/sintomática e SRS de alta dose). Em contrapartida, pacientes com DS-GPA <= 1.0 (ou RPA Classe III) apresentam sobrevida mediana desfavorável (< 2 a 3 meses), onde a cirurgia aberta não confere benefício de sobrevida e acarreta morbidade injustificada, recomendando-se suporte oncológico exclusivo ou radioterapia paliativa com dexametasona.",
        "radarAxes": [
            {
                "id": "axis_dsgpa_prognosis",
                "label": "Índice Prognóstico Global",
                "system": "Oncológico",
                "unit": "pts",
                "baselineValue": 4,
                "maxAxisValue": 4
            },
            {
                "id": "axis_dsgpa_performance",
                "label": "Status Funcional (KPS)",
                "system": "Funcional",
                "unit": "pts",
                "baselineValue": 1,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_gpa_kps",
                "name": "Desempenho Funcional Karnofsky (KPS)",
                "slug": "desempenho-kps",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_dsgpa_performance",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Capacidade funcional e independência física do paciente.",
                "options": [
                    {
                        "id": "opt_gpa_kps_high",
                        "label": "KPS 90% a 100%: Totalmente autônomo / Quase assintomático",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Atividade física plena, sem sinais clínicos limitantes."
                    },
                    {
                        "id": "opt_gpa_kps_int",
                        "label": "KPS 70% a 80%: Cuida de si, mas incapaz de trabalho ativo",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Independente para AVDs pessoais básicas."
                    },
                    {
                        "id": "opt_gpa_kps_low",
                        "label": "KPS < 70%: Requer assistência diária / Incapaz de autocuidado",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Passa grande parte do dia no leito ou requer cuidados contínuos."
                    }
                ]
            },
            {
                "id": "grp_gpa_age",
                "name": "Faixa Etária do Paciente",
                "slug": "faixa-etaria",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_dsgpa_prognosis",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Idade cronológica à admissão.",
                "options": [
                    {
                        "id": "opt_gpa_age_young",
                        "label": "Idade < 50 anos",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Menor risco cumulativo de comorbidades orgânicas."
                    },
                    {
                        "id": "opt_gpa_age_mid",
                        "label": "Idade de 50 a 59 anos",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Faixa etária intermediária."
                    },
                    {
                        "id": "opt_gpa_age_old",
                        "label": "Idade >= 60 anos",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Idade avançada associada a menor tolerância sistêmica."
                    }
                ]
            },
            {
                "id": "grp_gpa_lesions",
                "name": "Número de Metástases Cerebrais na Ressonância Magnética",
                "slug": "numero-metastases",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_dsgpa_prognosis",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Contagem de focos tumorais encefálicos captantes de contraste.",
                "options": [
                    {
                        "id": "opt_gpa_lesion_single",
                        "label": "Lesão única (1 metástase cerebral)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Metástase isolada passível de controle local cirúrgico ou radiocirúrgico definitivo."
                    },
                    {
                        "id": "opt_gpa_lesion_oligo",
                        "label": "2 a 3 metástases cerebrais (Oligometastático)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Doença oligometastática elegível a radiocirurgia estereotáxica (SRS)."
                    },
                    {
                        "id": "opt_gpa_lesion_multi",
                        "label": ">= 4 metástases cerebrais (Doença disseminada)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Disseminação difusa; indicação clássica de radioterapia de encéfalo total (WBRT) ou SRS de múltiplas lesões."
                    }
                ]
            },
            {
                "id": "grp_gpa_extracranial",
                "name": "Status de Metástases Extracranianas e Controle Sistêmico",
                "slug": "metastases-extracranianas",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_dsgpa_prognosis",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Presença de acometimento tumoral à distância fora do SNC.",
                "options": [
                    {
                        "id": "opt_gpa_extra_none",
                        "label": "Ausência de metástases extracranianas (ou tumor primário controlado)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Doença restrita ao sistema nervoso central."
                    },
                    {
                        "id": "opt_gpa_extra_present",
                        "label": "Metástases extracranianas ativas / Primário descontrolado",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Disseminação sistêmica multiorgânica ativa."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_gpa_low",
                "label": "DS-GPA 0 a 1 Ponto: Prognóstico Desfavorável (RPA Classe III)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Sobrevida global mediana estimada em apenas 2 a 4 meses. Risco de deterioração neurológica rápida.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gpa_dexametasona",
                        "drugName": "Dexametasona",
                        "dosage": "4 a 8 mg/dia",
                        "route": "Oral",
                        "frequency": "1 a 2 vezes ao dia",
                        "contraindications": "Infecção fúngica ativa."
                    },
                    {
                        "id": "rx_gpa_omeprazol",
                        "drugName": "Omeprazol",
                        "dosage": "20 a 40 mg",
                        "route": "Oral",
                        "frequency": "1 vez ao dia em jejum",
                        "contraindications": "Hipersensibilidade ao fármaco."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gpa_paliativo",
                        "recommendationTitle": "Plano de Cuidados Paliativos Exclusivos / WBRT Hipofracionada",
                        "dispositionTarget": "Ambulatório / Cuidados Paliativos",
                        "monitoringPlan": "Acompanhamento conjunto pela equipe de Cuidados Paliativos e Neuro-Oncologia.",
                        "interventionalProcedure": "Discussão de diretivas antecipadas de vontade, conforto domiciliar e radioterapia de encéfalo total (WBRT) hipofracionada (20 Gy em 5 frações) se alívio de sintomas refratários for desejado."
                    }
                ]
            },
            {
                "id": "tier_gpa_int",
                "label": "DS-GPA 2 a 3 Pontos: Prognóstico Intermediário (RPA Classe II)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Sobrevida global mediana estimada entre 6 e 14 meses. Potencial de resposta favorável a terapias locais ablativas.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gpa_memantina",
                        "drugName": "Cloridrato de Memantina",
                        "dosage": "5 mg/dia na semana 1, titulado até 10 mg",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "contraindications": "Insuficiência renal grave (ClCr < 30 mL/min)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gpa_srs",
                        "recommendationTitle": "Radiocirurgia Estereotáxica (SRS) Fracionada ou em Dose Única",
                        "dispositionTarget": "Ambulatório de Radioterapia",
                        "monitoringPlan": "RM de crânio com contraste a cada 2 a 3 meses para detecção precoce de novas lesões ou radionecrose.",
                        "interventionalProcedure": "Prescrição de 18 a 24 Gy em dose única (conforme diâmetro tumoral RTOG 90-05) poupando o parênquima cerebral saudável circundante."
                    }
                ]
            },
            {
                "id": "tier_gpa_high",
                "label": "DS-GPA 4 Pontos: Excelente Prognóstico (RPA Classe I)",
                "severityLevel": "low",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Sobrevida global mediana prolongada de 18 a 36+ meses. Baixa taxa de falência neurológica imediata.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_gpa_levetiracetam",
                        "drugName": "Levetiracetam",
                        "dosage": "500 mg",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "contraindications": "Hipersensibilidade ao fármaco."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_gpa_surgery",
                        "recommendationTitle": "Microcirurgia Ressectiva Guiada por Neuronavigação",
                        "dispositionTarget": "UTI Neurocrítica / Enfermaria",
                        "monitoringPlan": "Ressonância magnética trimestral e seguimento oncológico com terapias-alvo ou imunoterapia moderna.",
                        "interventionalProcedure": "Craniotomia guiada por imagem tridimensional, ressecção en bloc sem violação da cápsula tumoral e hemostasia rigorosa, seguida de radiocirurgia do leito operatório para prevenir recidiva local."
                    }
                ]
            }
        ]
    }

def get_kiefer():
    return {
        "id": "calc_kiefer",
        "slug": "kiefer",
        "name": "Escala de Kiefer para Hidrocefalia de Pressão Normal",
        "acronym": "Kiefer",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hidrodinâmica Cerebral e HPN",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hidrodinâmica Cerebral e HPN",
        "description": "Graduação quantitativa da gravidade clínica da Hidrocefalia de Pressão Normal (HPN) através dos componentes da Tríade de Hakim-Adams (marcha, cognição e incontinência) e sintomas associados, servindo para quantificar a melhora funcional no Tap Test e avaliar o sucesso pós-operatório da Derivação Ventriculoperitoneal (DVP).",
        "summary": "Escala de 0 a 24 pontos para graduação clínica e predição de resposta à DVP na Hidrocefalia de Pressão Normal.",
        "clinicalObjective": "Quantificar objetivamente o comprometimento neurológico na HPN e verificar a resposta terapêutica após punção lombar evacuadora (Tap Test).",
        "targetPopulation": "Pacientes idosos com ventriculomegalia e suspeita clínica da Tríade clássica de Hakim-Adams (apraxia da marcha, declínio cognitivo e urgência/incontinência urinária).",
        "calculationType": "additive_points",
        "formulaExpression": "Marcha_pontos + Cognicao_pontos + Incontinencia_pontos + Cefaleia_pontos + Tontura_pontos",
        "evidenceSource": "Kiefer M, Eymann R, Steudel WI. Outcome predictors for normal-pressure hydrocephalus. Acta Neurochir Suppl. 2006;96:364-367.",
        "minPossibleScore": 0,
        "maxPossibleScore": 24,
        "baseScore": 0,
        "badge": "hidrodinâmica",
        "clinicalWarning": "ATENÇÃO: A melhora de pelo menos 2 pontos na Escala de Kiefer (ou melhora > 20% no teste cronometrado de marcha Timed Up and Go - TUG) após a drenagem liquórica lombar evacuadora de 30 a 50 mL (Tap Test) constitui preditor de excelente resposta à cirurgia de DVP. Recomenda-se a utilização mandatória de válvula regulável com mecanismo gravitacional ou anti-sifão para prevenir complicações decorrentes de hiperdrenagem liquórica e hematoma subdural.",
        "radarAxes": [
            {
                "id": "axis_kiefer_gait",
                "label": "Distúrbio da Marcha",
                "system": "Motor",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 7
            },
            {
                "id": "axis_kiefer_cognitive",
                "label": "Declínio Cognitivo",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 6
            },
            {
                "id": "axis_kiefer_sphincter",
                "label": "Distúrbio Miccional",
                "system": "Esfincteriano",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 4
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_kiefer_gait",
                "name": "1. Distúrbio da Marcha (Hakim-Adams Componente Motor)",
                "slug": "disturbio-marcha",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_kiefer_gait",
                "normalBaselineValue": 0,
                "maxAxisValue": 7,
                "sortOrder": 1,
                "helpText": "Avalie a marcha espontânea e a necessidade de apoio físico.",
                "options": [
                    {
                        "id": "opt_kg_0",
                        "label": "0: Marcha completamente normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem instabilidade, velocidade e cadência normais."
                    },
                    {
                        "id": "opt_kg_1",
                        "label": "1: Instabilidade subjetiva ou insegurança leve",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.14,
                        "sortOrder": 2,
                        "description": "Sem quedas, deambula autonomamente sem apoio."
                    },
                    {
                        "id": "opt_kg_2",
                        "label": "2: Marcha cautelosa, passos curtos evidentes",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.28,
                        "sortOrder": 3,
                        "description": "Lentificação evidente ao girar, base discretamente alargada."
                    },
                    {
                        "id": "opt_kg_3",
                        "label": "3: Instabilidade evidente, requer apoio unilateral (bengala)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.43,
                        "sortOrder": 4,
                        "description": "Marcha magnética, hesitação inicial de marcha; usa bengala."
                    },
                    {
                        "id": "opt_kg_4",
                        "label": "4: Requer apoio bilateral (andador de 4 pontos ou 2 muletas)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.57,
                        "sortOrder": 5,
                        "description": "Incapaz de deambular com segurança sem andador."
                    },
                    {
                        "id": "opt_kg_5",
                        "label": "5: Necessita de auxílio físico direto de outra pessoa",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.71,
                        "sortOrder": 6,
                        "description": "Apoio de terceiros indispensável para deambulação de curta distância."
                    },
                    {
                        "id": "opt_kg_6",
                        "label": "6: Incapaz de deambular mesmo com assistência (Cadeirante)",
                        "pointValue": 6,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.86,
                        "sortOrder": 7,
                        "description": "Permanece em cadeira de rodas; sustenta o tronco com dificuldade."
                    },
                    {
                        "id": "opt_kg_7",
                        "label": "7: Restrito ao leito (Acamado / Imobilidade completa)",
                        "pointValue": 7,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 8,
                        "description": "Incapaz de ficar de pé ou sentar-se sem contenção."
                    }
                ]
            },
            {
                "id": "grp_kiefer_cognitive",
                "name": "2. Declínio Cognitivo / Demência",
                "slug": "declinio-cognitivo",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_kiefer_cognitive",
                "normalBaselineValue": 0,
                "maxAxisValue": 6,
                "sortOrder": 2,
                "helpText": "Avalie orientação, memória e velocidade de processamento mental.",
                "options": [
                    {
                        "id": "opt_kc_0",
                        "label": "0: Função cognitiva normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem queixas de memória ou déficit atencional."
                    },
                    {
                        "id": "opt_kc_1",
                        "label": "1: Bradipsiquismo leve / Lentificação do pensamento",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.17,
                        "sortOrder": 2,
                        "description": "Percebido pelo próprio paciente ou cônjuge; sem impacto nas AVDs."
                    },
                    {
                        "id": "opt_kc_2",
                        "label": "2: Desorientação temporal ou déficits leves de memória recente",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 3,
                        "description": "Esquecimentos frequentes; mantém autonomia pessoal."
                    },
                    {
                        "id": "opt_kc_3",
                        "label": "3: Desorientação espacial/temporal moderada; apatia evidente",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 4,
                        "description": "Incapaz de administrar finanças ou medicações sem supervisão."
                    },
                    {
                        "id": "opt_kc_4",
                        "label": "4: Requer supervisão contínua para autocuidado diário",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.67,
                        "sortOrder": 5,
                        "description": "Dependente de terceiros para banho, vestuário e alimentação."
                    },
                    {
                        "id": "opt_kc_5",
                        "label": "5: Desorientação severa; comunicação verbal fragmentada",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.83,
                        "sortOrder": 6,
                        "description": "Incapacidade de reconhecer familiares próximos de forma consistente."
                    },
                    {
                        "id": "opt_kc_6",
                        "label": "6: Demência avançada / Mutismo acinético",
                        "pointValue": 6,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 7,
                        "description": "Sem interação significativa com o meio ambiente."
                    }
                ]
            },
            {
                "id": "grp_kiefer_sphincter",
                "name": "3. Distúrbio Miccional / Esfincteriano",
                "slug": "disturbio-miccional",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_kiefer_sphincter",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 3,
                "helpText": "Avalie sintomas de urgência miccional e perda involuntária de urina/fezes.",
                "options": [
                    {
                        "id": "opt_ks_0",
                        "label": "0: Continência urinária e fecal normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem urgência miccional patológica ou perdas."
                    },
                    {
                        "id": "opt_ks_1",
                        "label": "1: Polaciúria e urgência miccional sem perdas involuntárias",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Sensação de necessidade imperiosa de urinar, consegue chegar ao toalete."
                    },
                    {
                        "id": "opt_ks_2",
                        "label": "2: Incontinência urinária episódica ou noturna (enurese)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 3,
                        "description": "Perda ocasional durante a noite ou em situações de esforço/pressa."
                    },
                    {
                        "id": "opt_ks_3",
                        "label": "3: Incontinência urinária diária constante (Uso contínuo de fraldas)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Perda frequente durante o dia; incontinência urinária estabelecida."
                    },
                    {
                        "id": "opt_ks_4",
                        "label": "4: Incontinência dupla (urinária e fecal permanente)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Perda total do controle vesical e intestinal."
                    }
                ]
            },
            {
                "id": "grp_kiefer_headache",
                "name": "4. Cefaleia Associada",
                "slug": "cefaleia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_kiefer_gait",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 4,
                "helpText": "Frequência e intensidade de queixas álgicas cranianas.",
                "options": [
                    {
                        "id": "opt_kh_0",
                        "label": "0: Sem cefaleia",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Ausência de queixas álgicas na cabeça."
                    },
                    {
                        "id": "opt_kh_1",
                        "label": "1: Cefaleia leve e infrequente",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Episódios ocasionais, alívio com analgésicos comuns."
                    },
                    {
                        "id": "opt_kh_2",
                        "label": "2: Cefaleia moderada recorrente",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 3,
                        "description": "Presente vários dias por semana."
                    },
                    {
                        "id": "opt_kh_3",
                        "label": "3: Cefaleia intensa diária",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Limita atividades diárias habituais."
                    },
                    {
                        "id": "opt_kh_4",
                        "label": "4: Cefaleia incapacitante contínua com náuseas",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Refratária a analgésicos orais; sugere pico de pressão intracraniana."
                    }
                ]
            },
            {
                "id": "grp_kiefer_dizziness",
                "name": "5. Tontura ou Vertigem",
                "slug": "tontura",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_kiefer_gait",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 5,
                "helpText": "Presença de sintomas vestibulares e vertiginosos.",
                "options": [
                    {
                        "id": "opt_kd_0",
                        "label": "0: Ausente",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem queixas de desequilíbrio vertiginoso."
                    },
                    {
                        "id": "opt_kd_1",
                        "label": "1: Leve, inconstante",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Sensação passageira ao levantar-se ou virar a cabeça rapidamente."
                    },
                    {
                        "id": "opt_kd_2",
                        "label": "2: Moderada, frequente",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.67,
                        "sortOrder": 3,
                        "description": "Contribui para a insegurança de marcha."
                    },
                    {
                        "id": "opt_kd_3",
                        "label": "3: Grave / Incapacitante",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Gera náuseas frequentes e necessidade de repouso no leito."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_kiefer_mild",
                "label": "Kiefer 0 a 4 Pontos: Comprometimento Clínico Leve",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 4,
                "statisticalOutcome": "Fase clínica inicial da HPN. Altíssima probabilidade de reversão completa dos déficits motores se Tap Test positivo.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kiefer_acetazolamida",
                        "drugName": "Acetazolamida",
                        "dosage": "250 mg",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "contraindications": "Hiponatremia, hipocalemia, insuficiência hepática ou renal grave, cirrose."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kiefer_tap_test",
                        "recommendationTitle": "Tap Test Evacuador Diagnóstico (30-50 mL)",
                        "dispositionTarget": "Hospital-Dia / Enfermaria",
                        "monitoringPlan": "Aplicação seriada do teste cronometrado Timed Up and Go (TUG) antes e 2h/24h após punção lombar.",
                        "interventionalProcedure": "Punção lombar no nível L3-L4 ou L4-L5 com mensuração da pressão de abertura (usualmente normal, entre 10 e 18 cmH2O) e drenagem lenta de 40 a 50 mL de líquor límpido."
                    }
                ]
            },
            {
                "id": "tier_kiefer_mod",
                "label": "Kiefer 5 a 11 Pontos: Comprometimento Clínico Moderado",
                "severityLevel": "intermediate",
                "minScore": 5,
                "maxScore": 11,
                "statisticalOutcome": "Quadro clássico consolidado da Tríade de Hakim-Adams. Excelente taxa de sucesso cirúrgico com DVP (melhora funcional sustentada em 75% a 85%).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kiefer_cefazolina",
                        "drugName": "Cefazolina Sódica",
                        "dosage": "2 g IV dose única pré-operatória",
                        "route": "Intravenosa",
                        "frequency": "Dose única 30 min antes da incisão",
                        "contraindications": "Hipersensibilidade grave a cefalosporinas/betalactâmicos."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kiefer_dvp",
                        "recommendationTitle": "Derivação Ventriculoperitoneal (DVP) com Válvula Programável",
                        "dispositionTarget": "UTI Neurocrítica / Enfermaria",
                        "monitoringPlan": "Avaliação neuropsicológica e fisioterapêutica motora pré e pós-operatória.",
                        "interventionalProcedure": "Canulação do corno frontal direito pelo ponto de Kocher, tunelização subcutânea até o abdômen e inserção intraperitoneal do cateter distal sob visão direta ou laparoscopia."
                    }
                ]
            },
            {
                "id": "tier_kiefer_sev",
                "label": "Kiefer 12 a 24 Pontos: Comprometimento Clínico Avançado",
                "severityLevel": "high",
                "minScore": 12,
                "maxScore": 24,
                "statisticalOutcome": "Estágio avançado de HPN. A taxa de melhora motora completa é reduzida (~40-50%), mas o shunt pode aliviar o manejo de enfermagem e estagnar a deterioração.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kiefer_enoxaparina",
                        "drugName": "Enoxaparina Sódica",
                        "dosage": "40 mg SC",
                        "route": "Subcutânea",
                        "frequency": "1 vez ao dia",
                        "contraindications": "Sangramento intracraniano ativo, plaquetopenia < 50.000/mm³."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kiefer_fisioterapia",
                        "recommendationTitle": "Reabilitação Fisioterapêutica Motora Intensiva Pós-DVP",
                        "dispositionTarget": "Enfermaria / Reabilitação",
                        "monitoringPlan": "TC de crânio aos 30 dias de PO para descartar coleções subdurais por hiperdrenagem precoce.",
                        "interventionalProcedure": "Treino intensivo de equilíbrio, transferências posturais e fortalecimento de membros inferiores para reconquista da marcha."
                    }
                ]
            }
        ]
    }

def get_evans_desh():
    return {
        "id": "calc_evans_desh",
        "slug": "evans-desh",
        "name": "Índice de Evans & Sinais de DESH para HPN",
        "acronym": "Evans-DESH",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hidrodinâmica Cerebral e HPN",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hidrodinâmica Cerebral e HPN",
        "description": "Avaliação neuro-radiológica tomográfica e por ressonância magnética da hidrocefalia comunicante do adulto (HPN), integrando o Índice de Evans (ventriculomegalia patológica), o padrão DESH (Disproportionately Enlarged Subarachnoid-space Hydrocephalus) e o ângulo do corpo caloso para discriminação precisa entre HPN responsiva a shunt e atrofia cerebral ex-vacuo (Demência de Alzheimer).",
        "summary": "Escore radiológico (0 a 10 pontos) com Índice de Evans, padrão DESH e ângulo caloso para predição de resposta à DVP.",
        "clinicalObjective": "Diferenciar a Hidrocefalia de Pressão Normal idiopática responsiva à DVP da dilatação ventricular ex-vacuo secundária à atrofia cortical neurodegenerativa.",
        "targetPopulation": "Pacientes com suspeita clínica de HPN submetidos a TC de crânio ou RM encefálica com cortes axiais e coronais perpendiculares à linha CA-CP.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Evans + Pontos_DESH + Pontos_Angulo + Pontos_Edema",
        "evidenceSource": "Evans WA. An encephalographic ratio for estimating ventricular enlargement and cerebral atrophy. Arch Neurol Psychiatry. 1942;47(6):931-937; Hashimoto M, Ishikawa M, Mori E, Kuwana N. Diagnosis of idiopathic normal pressure hydrocephalus with disproportionately enlarged subarachnoid-space hydrocephalus (DESH). J Neurol Sci. 2010;290(1-2):111-116.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "hidrodinâmica",
        "clinicalWarning": "ATENÇÃO: O Índice de Evans >= 0.30 é critério obrigatório de triagem para HPN, mas isoladamente é inespecífico (presente também em atrofias cerebrais avançadas). A presença do padrão DESH clássico (estreitamento e apagamento dos sulcos da alta convexidade frontoparietal em nítido contraste com alargamento das cisternas da base e fissuras de Sylvius) associado ao Ângulo do Corpo Caloso < 90° no corte coronal apresenta sensibilidade > 90% e valor preditivo positivo > 85-90% para melhora sustentada após DVP.",
        "radarAxes": [
            {
                "id": "axis_desh_pattern",
                "label": "Morfologia DESH",
                "system": "Radiológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 3
            },
            {
                "id": "axis_desh_ventricle",
                "label": "Ventriculomegalia / Evans",
                "system": "Radiológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 3
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_evans_index",
                "name": "1. Índice de Evans (Relação Cornos Frontais / Diâmetro Biparietal Interno)",
                "slug": "indice-evans",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_desh_ventricle",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 1,
                "helpText": "Maior diâmetro linear entre os cornos frontais dos ventrículos laterais dividido pelo maior diâmetro biparietal interno na mesma lâmina axial.",
                "options": [
                    {
                        "id": "opt_evans_normal",
                        "label": "Índice de Evans < 0.30: Normal / Sem ventriculomegalia",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Dimensões ventriculares proporcionais e normais para a idade."
                    },
                    {
                        "id": "opt_evans_enlarged",
                        "label": "Índice de Evans >= 0.30: Ventriculomegalia patológica confirmada",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Critério anatômico de rastreio obrigatório preenchido para prosseguimento da investigação de HPN."
                    }
                ]
            },
            {
                "id": "grp_desh_pattern",
                "name": "2. Padrão DESH (Disproportionately Enlarged Subarachnoid-space Hydrocephalus)",
                "slug": "padrao-desh",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_desh_pattern",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Distribuição disproporcional do líquor subaracnóideo nos sulcos cerebrais e cisternas.",
                "options": [
                    {
                        "id": "opt_desh_none",
                        "label": "Ausência de DESH / Sulcos corticais de convexidade difusamente alargados",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Atrofia cortical difusa típica de doença neurodegenerativa primária (Alzheimer / Atrofia ex-vacuo)."
                    },
                    {
                        "id": "opt_desh_partial",
                        "label": "Padrão DESH parcial / Incompleto",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Dilatação das fissuras silvianas presente, porém com sulcos do vértex apenas discretamente reduzidos."
                    },
                    {
                        "id": "opt_desh_classic",
                        "label": "Padrão DESH clássico completo (Sinal do Ápice Colabado)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Dilatação acentuada das fissuras silvianas e cisternas basais contrastando com colapso quase total dos sulcos da alta convexidade frontoparietal parassagital."
                    }
                ]
            },
            {
                "id": "grp_callosal_angle",
                "name": "3. Ângulo do Corpo Caloso (Corte Coronal ao Nível da Comissura Posterior)",
                "slug": "angulo-corpo-caloso",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_desh_pattern",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 3,
                "helpText": "Ângulo formado entre as paredes ventrais dos cornos frontais no corte coronal perpendicular ao plano CA-CP.",
                "options": [
                    {
                        "id": "opt_angle_wide",
                        "label": "Ângulo Obtuso >= 100° a 120° (Típico de Atrofia Cortical)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Dilatação ventricular proporcional à perda de volume cerebral; baixa probabilidade de resposta à DVP."
                    },
                    {
                        "id": "opt_angle_intermediate",
                        "label": "Ângulo Intermediário (90° a 99°)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Zona cinzenta / Limítrofe entre HPN e processo atrófico misto."
                    },
                    {
                        "id": "opt_angle_acute",
                        "label": "Ângulo Agudo < 90° (Típico de HPN Verdadeira)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Elevação e estiramento do corpo caloso contra a foice cerebral; alta especificidade para hidrocefalia de pressão normal."
                    }
                ]
            },
            {
                "id": "grp_periventricular_edema",
                "name": "4. Hiperintensidade Periventricular / Edema Transependimário",
                "slug": "edema-transependimario",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_desh_ventricle",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 4,
                "helpText": "Halo de hipodensidade na TC ou hipersinal em T2/FLAIR circundando os cornos ventriculares.",
                "options": [
                    {
                        "id": "opt_edema_absent",
                        "label": "Ausente ou restrito a leucoaraiose vascular pontilhada",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem sinal inequívoco de transudação transependimária ativa de líquor."
                    },
                    {
                        "id": "opt_edema_present",
                        "label": "Halo peri-ventricular confluente típico (Edema transependimário ativo)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Presença de gradiente pressórico transventricular favorecendo a reabsorção transependimária de líquor."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ed_unlikely",
                "label": "Escore 0 a 2: Baixa Probabilidade de HPN Responsiva (Atrofia ex-vacuo)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Padrão tomográfico/RM altamente sugestivo de atrofia cerebral difusa (ex-vacuo). Taxa de resposta à DVP < 15-20%. Elevado risco de complicações sem benefício.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ed_donepezila",
                        "drugName": "Cloridrato de Donepezila",
                        "dosage": "5 mg a 10 mg",
                        "route": "Oral",
                        "frequency": "1 vez ao dia à noite",
                        "contraindications": "Bradicardia sinusal grave, bloqueio atrioventricular."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ed_geriatria",
                        "recommendationTitle": "Investigação com Biomarcadores Liquóricos de Alzheimer",
                        "dispositionTarget": "Ambulatório de Neurologia / Geriatria",
                        "monitoringPlan": "Encaminhamento para avaliação neurológica e geriátrica de demências neurodegenerativas primárias.",
                        "interventionalProcedure": "Dosagem de Beta-amiloide 42, Tau total e Fosfo-Tau no líquor para confirmação diagnóstica de amiloidopatia cortical."
                    }
                ]
            },
            {
                "id": "tier_ed_possible",
                "label": "Escore 3 a 5: HPN Possível / Quadro Limítrofe ou Misto",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Ventriculomegalia confirmada com sinais parciais de HPN. Taxa de melhora funcional após cirurgia entre 45% e 60%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ed_acetazolamida",
                        "drugName": "Acetazolamida",
                        "dosage": "250 mg",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "contraindications": "Acidose metabólica hiperclorêmica, insuficiência renal severa."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ed_rout_test",
                        "recommendationTitle": "Teste de Infusão Lombar (Resistência à Reabsorção Liquórica - Rout)",
                        "dispositionTarget": "Hospital-Dia",
                        "monitoringPlan": "Investigação invasiva complementar com Tap Test quantitativo ou monitorização contínua da pressão intracraniana.",
                        "interventionalProcedure": "Infusão intratecal de soro fisiológico a fluxo constante para cálculo de Rout. Rout > 12 mmHg/mL/min reforça indicação cirúrgica de DVP."
                    }
                ]
            },
            {
                "id": "tier_ed_classic",
                "label": "Escore 6 a 10: Padrão DESH Típico / Altíssima Probabilidade de Resposta à DVP",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 10,
                "statisticalOutcome": "Padrão ouro neuro-radiológico de Hidrocefalia de Pressão Normal idiopática. Taxa de melhora funcional sustentada com DVP > 85% a 92%.",
                "colorHex": "#7f1d1d",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ed_cefazolina",
                        "drugName": "Cefazolina Sódica",
                        "dosage": "2 g IV dose única",
                        "route": "Intravenosa",
                        "frequency": "30 min antes da incisão cirúrgica",
                        "contraindications": "Anafilaxia a betalactâmicos."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ed_dvp_gravitacional",
                        "recommendationTitle": "Cirurgia de DVP com Válvula Programável Anti-Sifão",
                        "dispositionTarget": "UTI Neurocrítica / Enfermaria",
                        "monitoringPlan": "Programação cirúrgica prioritária e agendamento de consultas de controle pós-operatório da válvula.",
                        "interventionalProcedure": "Implante ventricular frontal direito com válvula programável gravitacional ajustada para nível pressórico inicial de 100-120 mmH2O, permitindo titulação não invasiva ambulatorial."
                    }
                ]
            }
        ]
    }
