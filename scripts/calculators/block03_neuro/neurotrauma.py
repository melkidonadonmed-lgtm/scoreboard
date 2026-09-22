"""
Block 03 Neurotrauma Module:
1. Rotterdam Score (TCE)
2. Marshall CT Classification (TCE)
3. ASIA / AIS Impairment Scale (Trauma Raquimedular)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL

def get_rotterdam():
    return {
        "id": "calc_rotterdam",
        "slug": "rotterdam",
        "name": "Escore Tomográfico de Rotterdam para TCE",
        "acronym": "Rotterdam",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Hipertensão Intracraniana (TCE)",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurotrauma e Hipertensão Intracraniana",
        "description": "Escore tomográfico preditor de mortalidade em 6 meses e prognóstico funcional desfavorável no traumatismo cranioencefálico moderado a grave.",
        "summary": "Escore tomográfico ordinal (1 a 6 pontos) preditor de mortalidade em 6 meses no TCE moderado a grave.",
        "clinicalObjective": "Predição objetiva de mortalidade em 6 meses e risco de HIC refratária no TCE fechado, superando vieses da classificação de Marshall.",
        "targetPopulation": "Pacientes adultos (>= 18 anos) admitidos com TCE moderado ou grave (GCS <= 12 ou trauma de alta energia) com TC de crânio inicial sem contraste.",
        "calculationType": "additive_points",
        "formulaExpression": "1 (constante basal) + Cisternas_pontos + Desvio_pontos + HED_pontos + HSA_HIV_pontos",
        "evidenceSource": "Maas AI, Hukkelhoven CW, Marshall LF, Steyerberg EW. Prediction of outcome in traumatic brain injury with computed tomographic characteristics. Neurosurgery. 2005;57(6):1173-1182.",
        "minPossibleScore": 1,
        "maxPossibleScore": 6,
        "baseScore": 1,
        "badge": "neurotrauma",
        "clinicalWarning": "ATENÇÃO: O cálculo do Escore de Rotterdam inicia-se obrigatoriamente na pontuação basal de +1 ponto. O hematoma epidural pontua 0 quando presente (fator protetor relativo: passível de evacuação cirúrgica descompressiva curativa) e +1 quando ausente (maior associação com dano axonal e contusional difuso). Corticosteroides (Metilprednisolona/Dexametasona) são expressamente contraindicados no TCE (ensaio clínico CRASH demonstrou aumento de mortalidade).",
        "radarAxes": [
            {
                "id": "axis_rotterdam_cisterns",
                "label": "Cisternas da Base",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_rotterdam_shift",
                "label": "Desvio de Linha Média",
                "system": "Neurológico",
                "unit": "mm",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_rotterdam_axial",
                "label": "Lesão Intraparenquimatosa",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_rotterdam_sah",
                "label": "Sangue Subaracnóideo / HIV",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_rotterdam_cisterns",
                "name": "Cisternas da Base (Perimesencefálicas)",
                "slug": "cisternas-da-base",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_rotterdam_cisterns",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Avaliação tomográfica do espaço liquórico perimesencefálico.",
                "options": [
                    {
                        "id": "opt_cisterns_normal",
                        "label": "Normais e patentes",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Cisternas perimesencefálicas amplas, simétricas e sem compressão."
                    },
                    {
                        "id": "opt_cisterns_compressed",
                        "label": "Comprimidas (parcialmente apagadas)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Redução simétrica ou assimétrica do calibre das cisternas da base."
                    },
                    {
                        "id": "opt_cisterns_absent",
                        "label": "Ausentes / Totalmente apagadas",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Obliteração completa do espaço liquórico perimesencefálico (sinal iminente de herniação)."
                    }
                ]
            },
            {
                "id": "grp_rotterdam_shift",
                "name": "Desvio de Linha Média (DLM)",
                "slug": "desvio-linha-media",
                "inputType": "single_choice",
                "unit": "mm",
                "radarAxisId": "axis_rotterdam_shift",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Desvio das estruturas medianas ao nível do forame de Monro.",
                "options": [
                    {
                        "id": "opt_shift_le5",
                        "label": "Desvio <= 5 mm (ou ausente)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Septo pelúcido e terceiro ventrículo centrados ou com desvio <= 5 mm."
                    },
                    {
                        "id": "opt_shift_gt5",
                        "label": "Desvio > 5 mm",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Desvio evidente das estruturas medianas superior a 5 mm no plano axial."
                    }
                ]
            },
            {
                "id": "grp_rotterdam_hed",
                "name": "Hematoma Epidural (HED)",
                "slug": "hematoma-epidural",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_rotterdam_axial",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Presença de sangramento extradural biconvexo.",
                "options": [
                    {
                        "id": "opt_hed_present",
                        "label": "Hematoma Epidural Presente",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Presença de hematoma extradural (fator protetor relativo: lesão focal tratável cirurgicamente sem dano axonal difuso)."
                    },
                    {
                        "id": "opt_hed_absent",
                        "label": "Hematoma Epidural Ausente",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Ausência de hematoma epidural (maior frequência de lesão axonal difusa e contusões intraparenquimatosas múltiplas)."
                    }
                ]
            },
            {
                "id": "grp_rotterdam_sah_ivh",
                "name": "HSA Traumática (tHSA) ou Hemorragia Intraventricular (HIV)",
                "slug": "hsa-ou-hiv",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_rotterdam_sah",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Detecção de sangue nos sulcos corticais ou sistema ventricular.",
                "options": [
                    {
                        "id": "opt_sah_ivh_absent",
                        "label": "Ambas Ausentes na TC",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem sangue hiperdenso subaracnóideo nos sulcos nem nível líquido hemático nos ventrículos."
                    },
                    {
                        "id": "opt_sah_ivh_present",
                        "label": "HSA Traumática OU HIV Presentes",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Presença de sangramento nos sulcos corticais subaracnóideos ou nível de sangue nos ventrículos laterais."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_rotterdam_low",
                "label": "Baixo Risco de Mortalidade (Rotterdam 1 a 2)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Rotterdam 1: Mortalidade em 6 meses de 0% (desfecho desfavorável ~15%). Rotterdam 2: Mortalidade em 6 meses de ~7% (desfecho desfavorável ~26%). Alta taxa de recuperação funcional independente.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_rotterdam_epi_prev",
                        "drugName": "Levetiracetam (ou Fenitoína Sódica)",
                        "dosage": "Levetiracetam 500 a 1000 mg IV 12/12h (ou Fenitoína ataque 18-20 mg/kg em SF 0,9% máx 50 mg/min, manutenção 100 mg IV 8/8h)",
                        "route": "Intravenosa",
                        "frequency": "12/12h ou 8/8h",
                        "dilutionInstructions": "Fenitoína deve ser diluída estritamente em SF 0,9% com filtro de linha. Proibido SG 5% (precipitação).",
                        "renalAdjustment": "Ajustar Levetiracetam conforme clearance de creatinina. Fenitoína não requer ajuste renal.",
                        "contraindications": "Fenitoína contraindicada em bloqueio atrioventricular de 2º/3º grau e bradicardia sinusal grave."
                    },
                    {
                        "id": "rx_rotterdam_analgesia",
                        "drugName": "Dipirona Monoidratada",
                        "dosage": "1 g IV a cada 6 horas",
                        "route": "Intravenosa",
                        "frequency": "6/6 horas",
                        "dilutionInstructions": "Diluir em 100 mL de SF 0,9% e infundir em 15 a 20 minutos.",
                        "renalAdjustment": "Sem ajuste necessário para doses habituais.",
                        "contraindications": "Hipersensibilidade a pirazolonas ou agranulocitose prévia."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_rotterdam_low_obs",
                        "recommendationTitle": "Vigilância Neurointensiva e Repouso Leito",
                        "dispositionTarget": "Unidade de Terapia Semi-Intensiva ou UTI",
                        "monitoringPlan": "Avaliação horária da Escala de Coma de Glasgow, diâmetro e fotoreatividade pupilar e força motora nos 4 membros.",
                        "interventionalProcedure": "TC de crânio de controle em 12 a 24 horas (ou imediata se queda >= 2 pontos no Glasgow).",
                        "ventilatorySupport": "Manter oxigenação com SpO2 >= 94% e PaO2 80-120 mmHg."
                    }
                ]
            },
            {
                "id": "tier_rotterdam_mod",
                "label": "Risco Moderado a Alto (Rotterdam 3 a 4)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Rotterdam 3: Mortalidade em 6 meses de 16% (desfecho desfavorável ~35-40%). Rotterdam 4: Mortalidade em 6 meses de 26% (desfecho desfavorável ~50-55%). Risco substancial de hipertensão intracraniana descompensada.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_rotterdam_sedation",
                        "drugName": "Fentanil + Propofol (Sedoanalgesia Contínua)",
                        "dosage": "Fentanil 1 a 3 mcg/kg/h associado a Propofol 1 a 4 mg/kg/h em BIC",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua em BIC",
                        "dilutionInstructions": "Propofol em frasco puro (10 mg/mL ou 20 mg/mL). Fentanil sem diluição em BIC exclusiva.",
                        "renalAdjustment": "Sem ajuste renal; monitorar triglicerídeos e síndrome da infusão do propofol (PRIS) se > 48h.",
                        "contraindications": "Propofol contraindicado em alergia a ovo/soja e choque cardiogênico descompensado."
                    },
                    {
                        "id": "rx_rotterdam_saline3",
                        "drugName": "Solução Salina Hipertônica 3% (ou Manitol 20%)",
                        "dosage": "150 a 250 mL IV em bolus ao longo de 15 a 20 minutos para picos de PIC > 22 mmHg",
                        "route": "Intravenosa",
                        "frequency": "Sob demanda para picos de PIC",
                        "dilutionInstructions": "Preparo 3%: 445 mL de SF 0,9% + 55 mL de NaCl 20%. Infundir em acesso venoso calibroso ou central.",
                        "renalAdjustment": "Monitorar sódio sérico a cada 4 a 6 horas (alvo máximo de natremia 155 mEq/L e osmolaridade sérica < 320 mOsm/L).",
                        "contraindications": "Hipernatremia extrema (> 160 mEq/L). Manitol contraindicado se osmolaridade > 320 mOsm/L ou choque hipotensivo."
                    },
                    {
                        "id": "rx_rotterdam_norepi",
                        "drugName": "Noradrenalina (Hemitartarato de Norepinefrina)",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua titulada para PPC entre 60 e 70 mmHg",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas (16 mg) em 234 mL de SG 5% (Solução Padrão: 64 mcg/mL). Veículo mandatório SG 5%.",
                        "renalAdjustment": "Não requer ajuste de dose para função renal.",
                        "contraindications": "Uso em linha periférica aceitável apenas transitoriamente por no máximo 2-4 horas até acesso central.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_rotterdam_mod_icu",
                        "recommendationTitle": "Internação em UTI Neurocrítica e Monitorização de PIC",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Indicação formal de monitorização invasiva de Pressão Intracraniana (cateter intraparenquimatoso ou DVE) se Glasgow <= 8 pós-ressuscitação inicial com TC anormal. Meta de PIC < 22 mmHg.",
                        "interventionalProcedure": "Passagem de cateter de PIC ou DVE à beira do leito; avaliação neurocirúrgica imediata se DLM > 5 mm ou lesões expansivas.",
                        "ventilatorySupport": "Ventilação mecânica invasiva protetora: volume corrente 6-8 mL/kg, PEEP 5-8 cmH2O, PaCO2 estritamente entre 35 e 40 mmHg (evitar hiperventilação profilática).",
                        "vascularAccess": "Acesso venoso central e linha arterial invasiva (PAI) para cálculo contínuo de PPC (PAM - PIC)."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_rotterdam_crit",
                "label": "Risco Crítico / Extremo de HIC e Óbito (Rotterdam 5 a 6)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 6,
                "statisticalOutcome": "Rotterdam 5: Mortalidade em 6 meses de 53% (incapacidade grave/vegetativo > 70%). Rotterdam 6: Mortalidade em 6 meses de 61% a 70% (desfecho desfavorável > 85-90%). Altíssimo risco de herniação cerebral transtentorial.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_rotterdam_paralysis",
                        "drugName": "Cisatracúrio (Bloqueio Neuromuscular Contínuo)",
                        "dosage": "Ataque 0,15 mg/kg IV bolus, seguido de infusão contínua de 1 a 3 mcg/kg/min em BIC",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Diluir em SF 0,9% ou SG 5% para concentração de 2 mg/mL.",
                        "renalAdjustment": "Eliminação de Hofmann (independente de função renal ou hepática).",
                        "contraindications": "Ausência de sedação profunda prévia mandatória (RASS -5 obrigatório)."
                    },
                    {
                        "id": "rx_rotterdam_barbiturate",
                        "drugName": "Tiopental Sódico (Coma Barbitúrico de Resgate - Nível 3)",
                        "dosage": "Ataque 2 a 5 mg/kg IV lento em 20-30 min, seguido de 1 a 5 mg/kg/h titulado por EEG até surto-supressão",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua sob EEG",
                        "dilutionInstructions": "Reconstituir 1g em 20 mL de AD e diluir em 500 mL de SF 0,9%.",
                        "renalAdjustment": "Monitorar acúmulo e meia-vida prolongada.",
                        "contraindications": "Hipotensão refratária não corrigida com vasopressores e porfiria aguda intermitente."
                    },
                    {
                        "id": "rx_rotterdam_norepi_crit",
                        "drugName": "Noradrenalina (Suporte Vasoativo Agressivo)",
                        "dosage": "Titular até 2,0 mcg/kg/min para assegurar PAM e PPC >= 60-70 mmHg",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Solução concentrada: 8 ampolas (32 mg) em 218 mL SG 5% (128 mcg/mL).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_rotterdam_surg_decomp",
                        "recommendationTitle": "Craniectomia Descompressiva de Urgência (Código Vermelho)",
                        "dispositionTarget": "Centro Cirúrgico de Emergência / UTI Neurocrítica",
                        "monitoringPlan": "Monitorização multimodal neurocrítica: PIC, PAI, PbtO2 (oxigenação tecidual cerebral com alvo > 20 mmHg) e temperatura central contínua.",
                        "interventionalProcedure": "Craniectomia Hemidescompressiva Fronto-têmporo-parietal unilateral ampla (diâmetro >= 12 a 15 cm com duroplastia de ampliação) se assimetria hemisférica; ou Craniectomia Bifrontal se edema difuso bilateral refratário.",
                        "ventilatorySupport": "Ventilação mecânica protetora rigorosa. Normotermia induzida (36,0 a 37,0°C) com dispositivo de resfriamento intravascular ou mantas térmicas ativas."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_marshall():
    return {
        "id": "calc_marshall",
        "slug": "marshall",
        "name": "Classificação Tomográfica de Marshall no TCE",
        "acronym": "Marshall TCE",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Hipertensão Intracraniana (TCE)",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurotrauma e Hipertensão Intracraniana",
        "description": "Classificação tomográfica categorizando lesões encefálicas difusas (Graus I a IV) e lesões focais com efeito de massa (Graus V e VI) para estratificar risco de HIC precoce e óbito.",
        "summary": "Classificação tomográfica em 6 categorias (Difusa I-IV e Massa V-VI) no TCE moderado a grave.",
        "clinicalObjective": "Categorização das lesões cerebrais agudas pós-trauma para predizer risco de hipertensão intracraniana refratária e direcionar cirurgia descompressiva.",
        "targetPopulation": "Pacientes admitidos com TCE moderado ou grave (Glasgow <= 12) submetidos à TC inicial de crânio.",
        "calculationType": "branching_decision",
        "formulaExpression": "Categoria_Marshall_Selecionada",
        "evidenceSource": "Marshall LF, Marshall SB, Klauber MR, et al. The diagnosis of head injury requires a classification based on computed axial tomography. J Neurotrauma. 1991;8(Suppl 1):S48-S51.",
        "minPossibleScore": 1,
        "maxPossibleScore": 6,
        "baseScore": 0,
        "badge": "neurotrauma",
        "clinicalWarning": "ATENÇÃO: A Classificação de Marshall opera através de árvore diagnóstica categórica mútua e excludente. Lesões focais hiperdensas ou mistas com volume > 25 mL (calculadas pela fórmula ABC/2) são classificadas obrigatoriamente como Grau V (se submetidas à evacuação cirúrgica) ou Grau VI (se não evacuadas). A evacuação cirúrgica de urgência converte o Grau VI em Grau V.",
        "radarAxes": [
            {
                "id": "axis_marshall_edema",
                "label": "Edema e Cisternas",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_marshall_shift",
                "label": "Desvio de Linha Média",
                "system": "Neurológico",
                "unit": "mm",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_marshall_mass",
                "label": "Efeito de Massa / Volume",
                "system": "Imagem",
                "unit": "mL",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_marshall_cat",
                "name": "Categoria Tomográfica de Marshall",
                "slug": "categoria-marshall",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_marshall_edema",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Selecione o achado tomográfico de crânio predominante.",
                "options": [
                    {
                        "id": "opt_marshall_1",
                        "label": "Grau I: Lesão Difusa I (Sem patologia visível)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Nenhuma anormalidade patológica intracraniana visível na TC de crânio."
                    },
                    {
                        "id": "opt_marshall_2",
                        "label": "Grau II: Lesão Difusa II (Cisternas presentes, DLM <= 5 mm)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.2,
                        "sortOrder": 2,
                        "description": "Cisternas perimesencefálicas preservadas; desvio de linha média <= 5 mm; nenhuma lesão hiperdensa ou mista > 25 mL."
                    },
                    {
                        "id": "opt_marshall_3",
                        "label": "Grau III: Lesão Difusa III - Swelling (Cisternas comprimidas/apagadas)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.6,
                        "sortOrder": 3,
                        "description": "Cisternas perimesencefálicas comprimidas ou ausentes; desvio de linha média <= 5 mm; sem lesões focais > 25 mL."
                    },
                    {
                        "id": "opt_marshall_4",
                        "label": "Grau IV: Lesão Difusa IV - Shift (Desvio de linha média > 5 mm)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.8,
                        "sortOrder": 4,
                        "description": "Desvio de linha média > 5 mm decorrente de tumefação hemisférica difusa; sem lesões focais > 25 mL."
                    },
                    {
                        "id": "opt_marshall_5",
                        "label": "Grau V: Massa Evacuada Cirurgicamente",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.7,
                        "sortOrder": 5,
                        "description": "Qualquer lesão intracraniana de alta densidade ou mista submetida à evacuação neurocirúrgica prévia."
                    },
                    {
                        "id": "opt_marshall_6",
                        "label": "Grau VI: Massa Não Evacuada (> 25 mL)",
                        "pointValue": 6,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 6,
                        "description": "Lesão focal hiperdensa ou de densidade mista com volume > 25 mL não submetida à evacuação cirúrgica."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_marshall_low",
                "label": "Baixo Risco de Hipertensão Intracraniana (Marshall Difusa I e II)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Difusa I: Mortalidade hospitalar ~9-10%, risco de HIC < 5%. Difusa II: Mortalidade ~13,5-15%, risco de HIC < 15%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_marshall_low_prev",
                        "drugName": "Levetiracetam (ou Fenitoína)",
                        "dosage": "Levetiracetam 500 a 1000 mg IV 12/12h por 7 dias",
                        "route": "Intravenosa",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Infundir em 100 mL de SF 0,9% em 15 minutos.",
                        "contraindications": "Evitar sedativos de ação prolongada que mascarem rebaixamento de consciência."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_marshall_low_obs",
                        "recommendationTitle": "Vigilância Clínica Neurológica Semi-Intensiva",
                        "dispositionTarget": "Unidade Semi-Intensiva ou UTI",
                        "monitoringPlan": "Avaliação clínica seriada e TC de controle em 12 a 24 horas.",
                        "ventilatorySupport": "Oxigenioterapia para manter SpO2 >= 94%."
                    }
                ]
            },
            {
                "id": "tier_marshall_mod",
                "label": "Risco Moderado a Alto / Massa Evacuada (Marshall III e V)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Difusa III: Mortalidade ~34-35%, risco de HIC > 50-60%. Massa Evacuada V: Mortalidade pós-operatória ~30-40% dependendo do tempo cirúrgico porta-craniotomia.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_marshall_mod_saline",
                        "drugName": "Solução Salina Hipertônica 3% (ou Manitol 20%)",
                        "dosage": "150 a 250 mL IV bolus em 15 minutos para elevação de PIC > 22 mmHg",
                        "route": "Intravenosa",
                        "frequency": "Sob demanda",
                        "dilutionInstructions": "Acesso central ou periférico calibroso. Manter sódio < 155 mEq/L.",
                        "contraindications": "Manitol contraindicado se osmolaridade > 320 mOsm/L."
                    },
                    {
                        "id": "rx_marshall_mod_norepi",
                        "drugName": "Noradrenalina IV para Manutenção de PPC 60-70 mmHg",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua em BIC",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_marshall_mod_pic",
                        "recommendationTitle": "Internação em UTI Neurocrítica com Monitorização de PIC",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Cateter de PIC intraparenquimatoso ou DVE obrigatório para GCS <= 8. Alvo de PIC < 22 mmHg e PPC 60-70 mmHg.",
                        "interventionalProcedure": "Se Marshall III refratário a medidas clínicas: avaliar Craniectomia Descompressiva Bifrontal.",
                        "ventilatorySupport": "IOT e ventilação mecânica protetora com PaCO2 35-40 mmHg."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_marshall_crit",
                "label": "Risco Extremo de Herniação Cerebral (Marshall Difusa IV e VI)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 6,
                "statisticalOutcome": "Difusa IV: Mortalidade de 56% a 60%, risco de HIC > 70-80%. Massa Não Evacuada VI: Mortalidade > 50-70%, risco iminente de herniação uncal com colapso de tronco encefálico (> 85%).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_marshall_crit_rescue",
                        "drugName": "Osmoterapia de Emergência em Bolus",
                        "dosage": "Salina Hipertônica 3% (250 mL IV bolus) ou Manitol 20% (1,0 g/kg IV rápido)",
                        "route": "Intravenosa",
                        "frequency": "Imediata pré-operatória",
                        "dilutionInstructions": "Infundir imediatamente durante transporte para o centro cirúrgico.",
                        "contraindications": "Evitar atraso no transporte para intervenção cirúrgica."
                    },
                    {
                        "id": "rx_marshall_crit_norepi",
                        "drugName": "Noradrenalina em BIC",
                        "dosage": "Titular para manter PAM invasiva garantindo PPC >= 65 mmHg",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Solução concentrada 128 mcg/mL.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_marshall_crit_surg",
                        "recommendationTitle": "Craniotomia / Craniectomia Descompressiva de Emergência",
                        "dispositionTarget": "Centro Cirúrgico de Emergência",
                        "monitoringPlan": "Monitorização invasiva multimodal contínua (PAI, PIC, saturação venosa de jugular ou PbtO2).",
                        "interventionalProcedure": "Para Massa VI: Craniotomia descompressiva de urgência com evacuação cirúrgica do hematoma. Para Difusa IV: Craniectomia hemidescompressiva frontotêmporo-parietal unilateral ampla (>= 12-15 cm) com plastia dural.",
                        "ventilatorySupport": "Intubação orotraqueal imediata com proteção cervical em sequência rápida."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_asia_ais():
    return {
        "id": "calc_asia_ais",
        "slug": "asia-ais",
        "name": "Escala de Deficiência ASIA / AIS (ISNCSCI)",
        "acronym": "ASIA / AIS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Coluna / Trauma Raquimedular",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Trauma Raquimedular e Coluna",
        "description": "Classificação padronizada universal do comitê ISNCSCI para quantificação de nível e completude da lesão medular após traumatismo raquimedular, ancorada na chave sacral S4-S5.",
        "summary": "Classificação padronizada ISNCSCI de déficit motor/sensitivo e preservação sacral S4-S5 (Graus A a E).",
        "clinicalObjective": "Padronização diagnóstica universal da extensão e completude da lesão medular após TRM, definindo Nível Neurológico da Lesão e potencial de recuperação funcional.",
        "targetPopulation": "Pacientes com traumatismo raquimedular agudo ou lesão medular compressiva traumática.",
        "calculationType": "branching_decision",
        "formulaExpression": "Grau_AIS_Selecionado",
        "evidenceSource": "Kirshblum SC, Biering-Sorensen F, Betz R, et al. International standards for neurological classification of spinal cord injury: revised 2011. J Spinal Cord Med. 2011;34(6):547-554.",
        "minPossibleScore": 1,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "neurotrauma",
        "clinicalWarning": "AVALIAÇÃO OBRIGATÓRIA DA CHAVE SACRAL (S4-S5): O exame anal digital com pesquisa de Contração Anal Voluntária (CAV), Sensibilidade Anal Profunda (SAP) e sensibilidade perianal é MANDATÓRIO para diferenciar a lesão completa (Grau A) da incompleta (Grau B). Durante a fase de Choque Medular (arreflexia flácida e ausência do reflexo bulbocavernoso), o diagnóstico de Grau A não pode ser firmado como definitivo. CORTICOSTEROIDES EM MEGADOSES (NASCIS) SÃO FORMALMENTE CONTRAINDICADOS pelas diretrizes AANS/CNS e AO Spine.",
        "radarAxes": [
            {
                "id": "axis_asia_motor",
                "label": "Déficit Motor",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_asia_sensory",
                "label": "Déficit Sensitivo",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_asia_sacral",
                "label": "Preservação Sacral S4-S5",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_asia_grade",
                "name": "Classificação da Lesão Medular (Graus AIS)",
                "slug": "grau-ais",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_asia_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Selecione o grau de completude da lesão conforme padrões ISNCSCI.",
                "options": [
                    {
                        "id": "opt_ais_a",
                        "label": "Grau A: Completa (Sem função motora ou sensitiva em S4-S5)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 1,
                        "description": "Nenhuma função motora ou sensitiva preservada nos segmentos sacrais S4-S5 (CAV ausente, SAP ausente e sensibilidade perianal ausente)."
                    },
                    {
                        "id": "opt_ais_b",
                        "label": "Grau B: Incompleta Sensitiva (Sensibilidade em S4-S5 preservada, sem função motora)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 2,
                        "description": "Sensibilidade preservada abaixo do nível neurológico estendendo-se até S4-S5, porém nenhuma função motora preservada mais de 3 níveis abaixo do nível motor."
                    },
                    {
                        "id": "opt_ais_c",
                        "label": "Grau C: Incompleta Motora (Mais de 50% dos músculos-chave com força < 3)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "Função motora preservada abaixo do nível neurológico, com mais da metade dos músculos-chave abaixo do nível apresentando força menor que grau 3 (MRC 0-2)."
                    },
                    {
                        "id": "opt_ais_d",
                        "label": "Grau D: Incompleta Motora (Pelo menos 50% dos músculos-chave com força >= 3)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 4,
                        "description": "Função motora preservada abaixo do nível neurológico, com pelo menos metade dos músculos-chave apresentando força igual ou superior a grau 3 (MRC 3-5)."
                    },
                    {
                        "id": "opt_ais_e",
                        "label": "Grau E: Normal (Funções motoras e sensitivas normais)",
                        "pointValue": 5,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 5,
                        "description": "Funções motoras e sensitivas rigorosamente normais em todos os segmentos testados em paciente com história documentada de lesão medular prévia."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ais_a",
                "label": "AIS Grau A - Lesão Medular Completa",
                "severityLevel": "critical",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Menos de 3% a 5% recuperam deambulação funcional comunitária a longo prazo. Risco severo de choque neurogênico (hipotensão + bradicardia relativa) em lesões acima de T6.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_asia_pam_target",
                        "drugName": "Noradrenalina IV para Meta de PAM 85 a 90 mmHg",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua em BIC por 7 dias contínuos",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua por 7 dias",
                        "dilutionInstructions": "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL). Associar Dobutamina se bradicardia reflexa concomitante.",
                        "contraindications": "Evitar hipotensão permissiva; hipoperfusão medular agrava dano isquêmico secundário irreversível.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    },
                    {
                        "id": "rx_asia_tev_prev",
                        "drugName": "Enoxaparina Sódica",
                        "dosage": "40 mg SC uma vez ao dia iniciada entre 24 e 72 horas pós-trauma",
                        "route": "Subcutânea",
                        "frequency": "24/24 horas",
                        "dilutionInstructions": "Solução injetável pronta para uso em seringa preenchida.",
                        "renalAdjustment": "Se ClCr < 30 mL/min: reduzir para 20 mg SC uma vez ao dia.",
                        "contraindications": "Presença de sangramento ativo intraespinhal ou hematoma epidural não evacuado."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_asia_crit_decomp",
                        "recommendationTitle": "Descompressão e Fixação Cirúrgica Precoce (< 24h)",
                        "dispositionTarget": "Centro Cirúrgico de Coluna / UTI Neurocrítica",
                        "monitoringPlan": "Manutenção mandatória de PAM entre 85 e 90 mmHg por 7 dias contínuos em UTI com linha arterial.",
                        "interventionalProcedure": "Descompressão cirúrgica urgente e estabilização de fratura/luxação em menos de 24 horas (ensaio STASCIS comprovou superioridade de descompressão precoce).",
                        "ventilatorySupport": "Se lesão cervical alta (C1 a C5): intubação orotraqueal imediata com videolaringoscópio ou fibrobroncoscopia sem hiperextensão cervical; suporte ventilatório invasivo por insuficiência diafragmática (nervo frênico C3-C5). Cateterismo vesical intermitente (CVI) a cada 4 a 6 horas."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_ais_b",
                "label": "AIS Grau B - Lesão Incompleta Sensitiva",
                "severityLevel": "high",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Sensibilidade preservada nos segmentos sacrais S4-S5 sem função motora abaixo do nível da lesão. Recuperação de deambulação funcional em menos de 10% a 15% dos casos.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    {
                        "id": "rx_asia_b_spasticity",
                        "drugName": "Baclofeno (ou Tizanidina)",
                        "dosage": "Baclofeno 5 mg VO 3x/dia, titulando até 20 mg 3x/dia (ou Tizanidina 2 a 4 mg ao deitar)",
                        "route": "Via Oral",
                        "frequency": "8/8 horas",
                        "dilutionInstructions": "Comprimidos administrados com água.",
                        "contraindications": "Evitar suspensão abrupta de baclofeno (risco de crise de abstinência com hipertermia e convulsões)."
                    },
                    {
                        "id": "rx_asia_b_pain",
                        "drugName": "Pregabalina",
                        "dosage": "75 mg VO 12/12h, podendo titular até 150 a 300 mg 12/12h",
                        "route": "Via Oral",
                        "frequency": "12/12 horas",
                        "dilutionInstructions": "Cápsulas por via oral.",
                        "renalAdjustment": "Ajustar dose conforme clearance de creatinina.",
                        "contraindications": "Hipersensibilidade à pregabalina."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_asia_b_rehab",
                        "recommendationTitle": "Descompressão Cirúrgica Precoce e Suporte Hemodinâmico",
                        "dispositionTarget": "UTI Neurocrítica / Enfermaria de Reabilitação",
                        "monitoringPlan": "PAM alvo 85-90 mmHg por 7 dias; profilaxia de TEV com meias elásticas e compressão pneumática.",
                        "interventionalProcedure": "Cirurgia descompressiva precoce (<24h) se compressão medular mecânica persistente.",
                        "ventilatorySupport": "Fisioterapia respiratória e treino motor precoce no leito."
                    }
                ]
            },
            {
                "id": "tier_ais_c",
                "label": "AIS Grau C - Lesão Incompleta Motora (Músculos < grau 3)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Função motora preservada abaixo do nível neurológico com mais da metade dos músculos chave < 3. Até 50% a 70% dos pacientes jovens recuperam marcha comunitária funcional com reabilitação intensa.",
                "colorHex": "#eab308",
                "pharmacologicalActions": [
                    {
                        "id": "rx_asia_c_spasticity",
                        "drugName": "Baclofeno (ou Tizanidina)",
                        "dosage": "Baclofeno 5 mg VO 3x/dia, titulando até 20 mg 3x/dia (ou Tizanidina 2 a 4 mg ao deitar)",
                        "route": "Via Oral",
                        "frequency": "8/8 horas",
                        "dilutionInstructions": "Comprimidos administrados com água.",
                        "contraindications": "Evitar suspensão abrupta de baclofeno."
                    },
                    {
                        "id": "rx_asia_c_pain",
                        "drugName": "Pregabalina",
                        "dosage": "75 mg VO 12/12h, podendo titular até 150 a 300 mg 12/12h",
                        "route": "Via Oral",
                        "frequency": "12/12 horas",
                        "dilutionInstructions": "Cápsulas por via oral.",
                        "renalAdjustment": "Ajustar dose conforme clearance de creatinina.",
                        "contraindications": "Hipersensibilidade à pregabalina."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_asia_c_rehab",
                        "recommendationTitle": "Reabilitação Neurofuncional Intensiva e Treino Motor",
                        "dispositionTarget": "Centro de Reabilitação Hospitalar",
                        "monitoringPlan": "Avaliação semanal de força motora (MRC) e ganho funcional.",
                        "interventionalProcedure": "Fisioterapia motora intensiva diária com treino de transferências e fortalecimento muscular."
                    }
                ]
            },
            {
                "id": "tier_ais_d",
                "label": "AIS Grau D - Lesão Incompleta Avançada / Deambulador",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Excelente prognóstico motor: mais de 85% a 95% recuperam marcha independente e controle funcional esfincteriano.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_asia_d_symptom",
                        "drugName": "Analgesia Multimodal e Relaxante Muscular",
                        "dosage": "Dipirona 1 g VO 6/6h se dor lombar/cervical mecânica",
                        "route": "Via Oral",
                        "frequency": "6/6 horas",
                        "dilutionInstructions": "Não aplicável."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_asia_d_gait",
                        "recommendationTitle": "Treinamento de Marcha e Fisioterapia Neurofuncional",
                        "dispositionTarget": "Enfermaria / Ambulatório de Reabilitação",
                        "monitoringPlan": "Avaliação de equilíbrio, força dos músculos-chave e adaptação de órteses tipo AFO se pé caído.",
                        "ventilatorySupport": "Exercícios ativos e treino de transferências."
                    }
                ]
            },
            {
                "id": "tier_ais_e",
                "label": "AIS Grau E - Normal / Recuperação Completa",
                "severityLevel": "low",
                "minScore": 5,
                "maxScore": 5,
                "statisticalOutcome": "Função neurológica motora e sensitiva integralmente normal em todos os dermátomos e miótomos.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_asia_e_none",
                        "drugName": "Sem Medicamentos Neurotróficos Específicos",
                        "dosage": "Não aplicável",
                        "route": "Não aplicável",
                        "frequency": "Não aplicável"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_asia_e_fup",
                        "recommendationTitle": "Seguimento Biomecânico Ambulatorial da Coluna",
                        "dispositionTarget": "Alta Orientada com Retorno Ambulatorial",
                        "monitoringPlan": "Controle radiológico de consolidação óssea e estabilidade ligamentar em 30, 60 e 90 dias."
                    }
                ]
            }
        ]
    }
