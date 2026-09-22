"""
Block 03 Subarachnoid Hemorrhage & Vascular Neurosurgery Module:
1. Hunt-Hess Scale (HSA)
2. WFNS Scale (HSA)
3. Fisher Classic Scale (HSA)
4. Modified Fisher / Claassen Scale (HSA)
5. Spetzler-Martin Grade (MAV)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL

def get_hunt_hess():
    return {
        "id": "calc_hunt_hess",
        "slug": "hunt-hess",
        "name": "Escala Clínica de Gravidade de Hunt e Hess na HSA",
        "acronym": "Hunt-Hess",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hemorragia Subaracnóidea e Aneurismas Cerebrais",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hemorragia Subaracnóidea e Aneurismas",
        "description": "Escala clínica de admissão que estratifica em 5 graus clínicos progressivos a gravidade da hemorragia subaracnóidea aneurismática e o risco de mortalidade cirúrgica.",
        "summary": "Escala clínica em 5 graus para avaliação da gravidade e prognóstico cirúrgico na HSA aneurismática.",
        "clinicalObjective": "Estratificar a gravidade clínica na admissão da HSA para estimar mortalidade cirúrgica e guiar o timing de intervenção microcirúrgica ou endovascular.",
        "targetPopulation": "Pacientes com diagnóstico confirmado de hemorragia subaracnóidea espontânea por rotura de aneurisma cerebral.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_Clinico_Base + Modificador_Comorbidade (+1 se doenca grave)",
        "evidenceSource": "Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of intracranial aneurysms. J Neurosurg. 1968;28(1):14-20.",
        "minPossibleScore": 1,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "ALERTA PRETO DE SEGURANÇA: É TERMINANTEMENTE PROIBIDA a administração da formulação de Nimodipino (cápsula ou solução oral) por via parenteral ou intravenosa (risco de colapso cardiovascular maciço fatal por choque vasodilatador refratário). Prescrever estritamente por VIA ORAL ou SONDA ENTERAL (60 mg a cada 4 horas por 21 dias). A indução de hipertensão terapêutica com Noradrenalina é FORMALMENTE CONTRAINDICADA antes da exclusão mecânica do aneurisma pelo risco de ressangramento catastrófico.",
        "radarAxes": [
            {
                "id": "axis_hh_consciousness",
                "label": "Nível de Consciência",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_hh_meningeal",
                "label": "Cefaleia e Sinais Meníngeos",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_hh_deficit",
                "label": "Déficit Neurológico Focal",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_hh_grade",
                "name": "Grau Clínico Admissional de Hunt-Hess",
                "slug": "grau-admissional",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_hh_consciousness",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Selecione o estado clínico neurológico na admissão pré-sedação.",
                "options": [
                    {
                        "id": "opt_hh_1",
                        "label": "Grau 1: Assintomático ou cefaleia leve e discreta rigidez de nuca",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.1,
                        "sortOrder": 1,
                        "description": "Paciente alerta, sem déficit, com cefaleia leve ou rigidez de nuca incipiente."
                    },
                    {
                        "id": "opt_hh_1a",
                        "label": "Grau 1a: Sem reação meníngea aguda, com déficit focal fixo preexistente",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.2,
                        "sortOrder": 2,
                        "description": "Ausência de reação meníngea/cefaleia aguda, portando sequela neurológica antiga fixa."
                    },
                    {
                        "id": "opt_hh_2",
                        "label": "Grau 2: Cefaleia moderada a grave, rigidez de nuca nítida, sem déficit exceto pares cranianos",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.4,
                        "sortOrder": 3,
                        "description": "Cefaleia intensa, rigidez meníngea evidente, sem déficit neurológico exceto paralisia de III ou VI par craniano."
                    },
                    {
                        "id": "opt_hh_3",
                        "label": "Grau 3: Sonolência (letargia), confusão mental ou déficit focal discreto",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.6,
                        "sortOrder": 4,
                        "description": "Sonolência, desorientação cognitiva ou déficit motor/sensitivo leve."
                    },
                    {
                        "id": "opt_hh_4",
                        "label": "Grau 4: Estupor, hemiparesia moderada/grave, descerebração precoce ou disautonomia",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.8,
                        "sortOrder": 5,
                        "description": "Estupor (desperta apenas com dor vigorosa), hemiparesia nítida, rigidez ou distúrbios vegetativos."
                    },
                    {
                        "id": "opt_hh_5",
                        "label": "Grau 5: Coma profundo, postura de descerebração sustentada, aparência moribunda",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 6,
                        "description": "Coma não responsivo, rigidez extensora sustentada ou flacidez terminal."
                    }
                ]
            },
            {
                "id": "grp_hh_modifier",
                "name": "Modificador por Doença Sistêmica Grave ou Vasoespasmo",
                "slug": "modificador-sistemico",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_hh_meningeal",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Adiciona +1 grau à classificação se houver doença grave associada.",
                "options": [
                    {
                        "id": "opt_hh_mod_none",
                        "label": "Ausente (Sem comorbidade descompensada ou vasoespasmo grave)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sem crise hipertensiva refratária, choque, DPOC grave ou vasoespasmo angiográfico documentado."
                    },
                    {
                        "id": "opt_hh_mod_present",
                        "label": "Presente (+1 Grau na Classificação Perioperatória)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Presença de hipertensão grave, choque, coronariopatia descompensada ou vasoespasmo grave."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_hh_good",
                "label": "Bons Graus Clínicos (Hunt-Hess 1 e 2)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade cirúrgica/perioperatória baixa (1% a 11-20%). Prognóstico funcional favorável em 6 meses (mRS 0-2 > 80%).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hh_nimodipine",
                        "drugName": "Nimodipino (Profilaxia de DCI)",
                        "dosage": "60 mg VO ou por SNE rigorosamente a cada 4 horas por 21 dias contínuos",
                        "route": "Via Oral ou Sonda Nasoenteral (PROIBIDO VIA INTRAVENOSA)",
                        "frequency": "4/4 horas",
                        "dilutionInstructions": "Se administrado por sonda enteral, aspirar o conteúdo da cápsula mole com agulha e seringa oral. Lavar a sonda com 20 mL de água destilada. NUNCA UTILIZAR SERINGA PARENTERAL.",
                        "renalAdjustment": "Não requer ajuste renal. Se hipotensão arterial persistente (PAS < 100 mmHg), reduzir para 30 mg a cada 2 horas.",
                        "contraindications": "PROIBIÇÃO FORMAL ABSOLUTA DE ADMINISTRAÇÃO POR VIA PARENTERAL OU INTRAVENOSA."
                    },
                    {
                        "id": "rx_hh_bp_control",
                        "drugName": "Nitroprussiato de Sódio (ou Esmolol) para Controle de PAS Pré-Oclusão",
                        "dosage": "0,25 a 5,0 mcg/kg/min IV contínua titulada para manter PAS < 160 mmHg",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua pré-oclusão",
                        "dilutionInstructions": "1 ampola (50 mg) em 248 mL de SG 5% com equipo fotoprotetor obrigatório.",
                        "contraindications": "Evitar hipotensão com PAS < 100 mmHg para não provocar isquemia cerebral secundária."
                    },
                    {
                        "id": "rx_hh_analgesia",
                        "drugName": "Dipirona 1g IV 6/6h + Morfina 2 a 4 mg IV se dor refratária",
                        "dosage": "Dipirona 1 g IV 6/6h + Morfina 2-4 mg IV resgate",
                        "route": "Intravenosa",
                        "frequency": "6/6 horas e resgate",
                        "dilutionInstructions": "Morfina 1 ampola (10 mg) diluída para 10 mL em SF 0,9% (1 mg/mL).",
                        "contraindications": "Evitar sedação excessiva que mascare deterioração neurológica."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hh_early_clipping",
                        "recommendationTitle": "Tratamento Mecânico Definitivo Urgente do Aneurisma (< 24-72h)",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Repouso absoluto no leito, ambiente escuro e calmo, cabeceira 30°, laxantes osmóticos (Lactulose 15-30 mL/dia) para evitar manobra de Valsalva.",
                        "interventionalProcedure": "Angiografia cerebral digital de urgência e oclusão do aneurisma por microembolização endovascular com molas destacáveis (coils) ou clipagem microcirúrgica em < 24 a 72 horas.",
                        "ventilatorySupport": "Doppler Transcraniano (DTC) de triagem a cada 24-48h a partir do 3º dia pós-sangramento."
                    }
                ]
            },
            {
                "id": "tier_hh_mod",
                "label": "Grau Intermediário (Hunt-Hess 3)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade em torno de 20% a 40%. Risco substancial de deterioração neurológica por hidrocefalia aguda comunicante ou vasoespasmo precoce.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hh3_nimodipine",
                        "drugName": "Nimodipino 60 mg VO/SNE a cada 4 horas",
                        "dosage": "60 mg VO a cada 4 horas por 21 dias",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas",
                        "dilutionInstructions": "PROIBIDO USO INTRAVENOSO."
                    },
                    {
                        "id": "rx_hh3_hydration",
                        "drugName": "Ringer Lactato ou SF 0,9% (Manutenção de Euvolemia Estrita)",
                        "dosage": "2.000 a 3.000 mL/dia de cristaloide isotônico",
                        "route": "Intravenosa",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Solução pronta para infusão.",
                        "contraindications": "A hipervolemia profilática (antiga conduta dos '3 Hs') é PROSCRITA pelas diretrizes AHA/ASA 2023 pelo risco de edema pulmonar e hiponatremia."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hh3_dve",
                        "recommendationTitle": "Vigilância de Hidrocefalia e Derivação Ventricular Externa (DVE)",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "TC de crânio seriada para monitorar dilatação dos cornos temporais ventriculares.",
                        "interventionalProcedure": "Implantação urgente de cateter de Derivação Ventricular Externa (DVE) diante de dilatação ventricular ou hidrocefalia aguda comunicante; oclusão mecânica do aneurisma em < 24-72h."
                    }
                ]
            },
            {
                "id": "tier_hh_poor",
                "label": "Maus Graus Clínicos (Hunt-Hess 4 e 5)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Grau 4: Mortalidade cirúrgica/hospitalar de 40% a 80%. Grau 5: Mortalidade de 70% a 100%. Alto risco de óbito precoce ou incapacidade vegetativa permanente.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hh_crit_nimodipine",
                        "drugName": "Nimodipino por Sonda Enteral Exclusiva",
                        "dosage": "60 mg enteral 4/4h (NUNCA POR VIA PARENTERAL)",
                        "route": "Sonda Nasoenteral",
                        "frequency": "4/4 horas"
                    },
                    {
                        "id": "rx_hh_crit_norepi",
                        "drugName": "Noradrenalina IV para Manutenção de PAM e PPC >= 65 mmHg",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua em BIC",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hh_crit_dve_reval",
                        "recommendationTitle": "Passagem Emergencial de DVE e Regra de Reavaliação Obrigatória",
                        "dispositionTarget": "UTI Neurocrítica / Centro Cirúrgico",
                        "monitoringPlan": "REGRA MANDATÓRIA DE REAVALIAÇÃO PÓS-DVE: A descompressão ventricular emergencial frequentemente alivia a hidrocefalia aguda hipertensiva sobre o diencéfalo, promovendo melhora do nível de consciência e permitindo a reclassificação para Grau 2 ou 3.",
                        "interventionalProcedure": "Implantação imediata de cateter de DVE à beira do leito; se recuperação neurológica pós-drenagem, prosseguir imediatamente para oclusão do aneurisma por via endovascular prioritariamente.",
                        "ventilatorySupport": "Intubação orotraqueal em sequência rápida com proteção de reflexos simpáticos (Lidocaína 1,5 mg/kg IV + Fentanil 3 mcg/kg IV)."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_wfns():
    return {
        "id": "calc_wfns",
        "slug": "wfns",
        "name": "Escala da WFNS para Hemorragia Subaracnóidea",
        "acronym": "WFNS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hemorragia Subaracnóidea e Aneurismas Cerebrais",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hemorragia Subaracnóidea e Aneurismas",
        "description": "Escala universal padronizada pela World Federation of Neurosurgical Societies combinando Glasgow e presença de déficits motores focais maiores na HSA.",
        "summary": "Escala clínica universal (Graus I a V) baseada no Glasgow e déficit motor na HSA aneurismática.",
        "clinicalObjective": "Substituir ambiguidades subjetivas na avaliação da HSA por critérios clínicos objetivos altamente reprodutíveis.",
        "targetPopulation": "Pacientes com hemorragia subaracnóidea espontânea aneurismática confirmada.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_WFNS_Selecionado",
        "evidenceSource": "Drake CG, Hunt WE, Sano K, et al. Report of World Federation of Neurological Surgeons Committee on a Universal Subarachnoid Hemorrhage Grading Scale. J Neurosurg. 1988;68(6):985-986.",
        "minPossibleScore": 1,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "AVALIAÇÃO PRÉ-SEDAÇÃO OBRIGATÓRIA: O escore da WFNS deve ser aferido antes da administração de sedativos ou bloqueadores neuromusculares. A presença de déficit motor focal maior (hemiparesia ou hemiplegia) diferencia o Grau II (GCS 13-14 sem déficit) do Grau III (GCS 13-14 com déficit). Nos Graus IV (GCS 7-12) e V (GCS 3-6), a presença de déficit motor não altera a categoria.",
        "radarAxes": [
            {
                "id": "axis_wfns_gcs",
                "label": "Escala de Glasgow",
                "system": "Neurológico",
                "unit": "GCS",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_wfns_motor",
                "label": "Déficit Motor Focal Maior",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_wfns_class",
                "name": "Classificação Clínica WFNS",
                "slug": "classificacao-wfns",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_wfns_gcs",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Cruze a pontuação da Escala de Glasgow com o déficit motor focal.",
                "options": [
                    {
                        "id": "opt_wfns_1",
                        "label": "Grau I: Glasgow 15, sem déficit motor focal",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Glasgow 15 perfeito, ausência de hemiparesia ou hemiplegia."
                    },
                    {
                        "id": "opt_wfns_2",
                        "label": "Grau II: Glasgow 13 a 14, sem déficit motor focal",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Glasgow 13 ou 14 na ausência de déficit motor focal maior."
                    },
                    {
                        "id": "opt_wfns_3",
                        "label": "Grau III: Glasgow 13 a 14, COM déficit motor focal presente",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.55,
                        "sortOrder": 3,
                        "description": "Glasgow 13 ou 14 associado a hemiparesia ou hemiplegia contralateral."
                    },
                    {
                        "id": "opt_wfns_4",
                        "label": "Grau IV: Glasgow 7 a 12, com ou sem déficit motor",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.8,
                        "sortOrder": 4,
                        "description": "Glasgow entre 7 e 12 pontos, independentemente da presença de déficits motores."
                    },
                    {
                        "id": "opt_wfns_5",
                        "label": "Grau V: Glasgow 3 a 6, com ou sem déficit motor",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Glasgow entre 3 e 6 pontos (coma profundo ou postura patológica)."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_wfns_low",
                "label": "Baixa Gravidade (WFNS Graus I e II)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de bom prognóstico funcional em 6 meses > 80%. Baixa taxa de mortalidade (< 10% a 15%).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wfns_nimodipine",
                        "drugName": "Nimodipino 60 mg VO 4/4h por 21 dias",
                        "dosage": "60 mg VO 4/4h contínuo (PROIBIDO VIA ENDOVENOSA)",
                        "route": "Via Oral ou SNE",
                        "frequency": "4/4 horas"
                    },
                    {
                        "id": "rx_wfns_bp",
                        "drugName": "Controle Pressórico com PAS < 160 mmHg pré-oclusão",
                        "dosage": "Titulação de Nitroprussiato de Sódio ou Esmolol",
                        "route": "Intravenosa",
                        "frequency": "Contínua"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_wfns_early_repair",
                        "recommendationTitle": "Angiografia Cerebral e Oclusão Precoce (< 24-72h)",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Monitorização neurológica contínua e Doppler Transcraniano diário.",
                        "interventionalProcedure": "Embolização endovascular com coils ou clipagem microcirúrgica nas primeiras 24 a 72 horas."
                    }
                ]
            },
            {
                "id": "tier_wfns_mod",
                "label": "Gravidade Intermediária (WFNS Grau III)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Prognóstico intermediário; mortalidade de 25% a 35%. Déficit motor reflete isquemia focal precoce ou hematoma intraparenquimatoso associado.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wfns3_nimo",
                        "drugName": "Nimodipino 60 mg VO/SNE 4/4h",
                        "dosage": "60 mg 4/4h por 21 dias",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_wfns3_angiotc",
                        "recommendationTitle": "Angio-TC Urgente e Avaliação Cirúrgica Aberta",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Descartar hematoma intracerebral com indicação cirúrgica aberta imediata (craniectomia + drenagem + clipagem).",
                        "interventionalProcedure": "Tratamento cirúrgico ou endovascular do aneurisma."
                    }
                ]
            },
            {
                "id": "tier_wfns_high",
                "label": "Alta Gravidade (WFNS Graus IV e V)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Alta taxa de mortalidade hospitalar (50% a 85%). Sobreviventes frequentemente evoluem com incapacidade funcional grave dependente (mRS 4 ou 5).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_wfns_crit_norepi",
                        "drugName": "Noradrenalina IV para Meta de PPC >= 65 mmHg",
                        "dosage": "0,05 a 2,0 mcg/kg/min IV contínua em BIC",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_wfns_crit_dve",
                        "recommendationTitle": "Passagem Imediata de DVE e Reavaliação Pós-Descompressão",
                        "dispositionTarget": "UTI Neurocrítica / Centro Cirúrgico",
                        "monitoringPlan": "Intubação orotraqueal imediata, proteção de via aérea e passagem urgente de cateter de DVE para descompressão de hidrocefalia e monitorização de PIC.",
                        "interventionalProcedure": "Reavaliação neurológica mandatória pós-descompressão liquórica; se resposta, proceder à oclusão endovascular do aneurisma.",
                        "ventilatorySupport": "Ventilação mecânica protetora invasiva."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_fisher_classic():
    return {
        "id": "calc_fisher_classic",
        "slug": "fisher-classic",
        "name": "Escala de Fisher Clássica (1980) para HSA",
        "acronym": "Fisher Clássico",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hemorragia Subaracnóidea e Aneurismas Cerebrais",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hemorragia Subaracnóidea e Aneurismas",
        "description": "Escala tomográfica seminal de 4 graus correlacionando a espessura do sangue subaracnóideo nas cisternas e fissuras cerebrais com o risco de vasoespasmo arterial sintomático.",
        "summary": "Escala tomográfica de 4 graus correlacionando espessura do sangue com risco de vasoespasmo na HSA.",
        "clinicalObjective": "Predição do risco de vasoespasmo arterial sintomático e isquemia cerebral a partir dos achados da TC de crânio inicial sem contraste.",
        "targetPopulation": "Pacientes com HSA aneurismática aguda com TC realizada nas primeiras 24 a 72 horas.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_Fisher_Classico",
        "evidenceSource": "Fisher CM, Kistler JP, Davis JM. Relation of cerebral vasospasm to subarachnoid hemorrhage visualized by computerized tomographic scanning. Neurosurgery. 1980;6(1):1-9.",
        "minPossibleScore": 1,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "PEGADINHA DA NÃO-LINEARIDADE: O Fisher Clássico NÃO é uma escala linear crescente de gravidade de vasoespasmo. O Grau 3 (coágulos espessos >= 1 mm) apresenta o risco mais elevado e crítico de vasoespasmo sintomático (60% a 80%), enquanto o Grau 4 (hemoventrículo ou hematoma com sangue fino) apresenta risco substancialmente menor de vasoespasmo (15% a 20%), embora cause maior incidência de hidrocefalia.",
        "radarAxes": [
            {
                "id": "axis_fisher_cl_thickness",
                "label": "Espessura do Sangue Cisternal",
                "system": "Imagem",
                "unit": "mm",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_fisher_cl_ventricular",
                "label": "Hemoventrículo / Hematoma",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_fisher_classic",
                "name": "Achados Tomográficos de Fisher Clássico",
                "slug": "achados-fisher-classico",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_fisher_cl_thickness",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Avalie a espessura da lâmina de sangue e a presença de hemoventrículo.",
                "options": [
                    {
                        "id": "opt_fc_1",
                        "label": "Grau 1: Sem sangue subaracnóideo detectável na TC inicial",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Nenhum sangramento subaracnóideo visível na tomografia computadorizada."
                    },
                    {
                        "id": "opt_fc_2",
                        "label": "Grau 2: Lâmina fina de sangue subaracnóideo difuso (< 1 mm de espessura)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.3,
                        "sortOrder": 2,
                        "description": "Deposição fina de sangue nos sulcos ou cisternas com espessura vertical inferior a 1 mm."
                    },
                    {
                        "id": "opt_fc_3",
                        "label": "Grau 3: Coágulos espessos ou camada vertical de sangue >= 1 mm",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Coágulos densos ou camada vertical >= 1 mm preenchendo fissuras ou cisternas basais (risco máximo de vasoespasmo)."
                    },
                    {
                        "id": "opt_fc_4",
                        "label": "Grau 4: Hematoma intraparenquimatoso ou hemoventrículo com sangue fino ou ausente",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.7,
                        "sortOrder": 4,
                        "description": "Presença de sangramento intraventricular ou intraparenquimatoso sem coágulo subaracnóideo espesso."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_fc_low",
                "label": "Baixo Risco de Vasoespasmo (Fisher Clássico 1 e 2)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Incidência de vasoespasmo arterial sintomático inferior a 5% a 15%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fc_nimodipine",
                        "drugName": "Nimodipino 60 mg VO 4/4h por 21 dias",
                        "dosage": "60 mg VO 4/4h (PROIBIDO USO ENDOVENOSO)",
                        "route": "Via Oral ou SNE",
                        "frequency": "4/4 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fc_dtc",
                        "recommendationTitle": "Vigilância com Doppler Transcraniano a cada 48h",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "DTC seriado a cada 48 horas e oclusão definitiva precoce do aneurisma."
                    }
                ]
            },
            {
                "id": "tier_fc_crit",
                "label": "Risco Crítico de Vasoespasmo Clínico (Fisher Clássico 3)",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Risco crítico de vasoespasmo angiográfico (> 70%) e clínico sintomático (60% a 80%). Elevada incidência de infarto cerebral isquêmico tardio secundário.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fc3_nimo",
                        "drugName": "Nimodipino 60 mg VO 4/4h por 21 dias contínuos",
                        "dosage": "60 mg VO 4/4h",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas"
                    },
                    {
                        "id": "rx_fc3_htn",
                        "drugName": "Hipertensão Terapêutica Induzida com Noradrenalina IV (Pós-Oclusão)",
                        "dosage": "Titular para manter PAS 160 a 180 mmHg se surgir déficit isquêmico após exclusão mecânica do aneurisma",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua pós-oclusão",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL). CONTRAINDICADA ANTES DA OCLUSÃO DO ANEURISMA.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fc3_interv",
                        "recommendationTitle": "Doppler Transcraniano Diário e Resgate Intervencionista",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "DTC diário seriado a cada 12-24h (velocidade média da ACM > 120 cm/s indica espasmo moderado; > 200 cm/s ou elevação > 50 cm/s/dia atesta espasmo crítico; calcular Índice de Lindegaard > 3).",
                        "interventionalProcedure": "Se refratariedade ao manejo hipertensivo: encaminhar para Angioplastia Transluminal com Balão (vasos proximais M1, A1, carótida terminal) ou infusão superseletiva de Milrinona/Nicardipino intra-arterial em sala de hemodinâmica."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_fc_hydro",
                "label": "Risco Moderado de Espasmo e Alta Hidrocefalia (Fisher Clássico 4)",
                "severityLevel": "high",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Risco de vasoespasmo sintomático moderado (15% a 20%), porém elevado risco de hidrocefalia comunicante ou obstrutiva aguda e hipertensão intracraniana.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fc4_nimo",
                        "drugName": "Nimodipino 60 mg VO 4/4h",
                        "dosage": "60 mg VO 4/4h",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fc4_dve",
                        "recommendationTitle": "Passagem de DVE de Urgência para Lavagem e Descompressão",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Implantação de Derivação Ventricular Externa (DVE) para monitorização de PIC e lavagem liquórica contínua do hemoventrículo.",
                        "interventionalProcedure": "Tratamento cirúrgico ou endovascular do aneurisma."
                    }
                ]
            }
        ]
    }

def get_fisher_modified():
    return {
        "id": "calc_fisher_modified",
        "slug": "fisher-modified",
        "name": "Escala de Fisher Modificada (Claassen 2001)",
        "acronym": "Fisher Modificado",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Hemorragia Subaracnóidea e Aneurismas Cerebrais",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hemorragia Subaracnóidea e Aneurismas",
        "description": "Escala radiológica ordinal de 5 graus (0 a 4) combinando a espessura da HSA cisternal com hemorragia intraventricular (HIV) bilateral para estratificação do risco de DCI e vasoespasmo.",
        "summary": "Escala radiológica ordinal de 5 graus (0 a 4) preditora de vasoespasmo e Isquemia Cerebral Tardia (DCI).",
        "clinicalObjective": "Estratificação de risco de isquemia cerebral tardia e vasoespasmo com relação monotônica crescente, substituindo o Fisher clássico de 1980.",
        "targetPopulation": "Pacientes com HSA aneurismática aguda com TC realizada nas primeiras 24 a 72 horas.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_Fisher_Modificado",
        "evidenceSource": "Claassen J, Bernardini GL, Kreiter K, et al. Effect of cisternal and ventricular blood on risk of delayed cerebral ischemia after subarachnoid hemorrhage: the Fisher scale revisited. Stroke. 2001;32(9):2012-2020.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "DIRETRIZ AHA/ASA 2023: A Escala de Fisher Modificada (Claassen) é recomendada como padrão-ouro radiológico para estratificação de risco de vasoespasmo pós-HSA, superando o Fisher clássico ao corrigir a não-linearidade. A presença de HIV bilateral é um multiplicador de risco crítico de Isquemia Cerebral Tardia.",
        "radarAxes": [
            {
                "id": "axis_fm_cisternal",
                "label": "Carga de Sangue Cisternal",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_fm_ivh",
                "label": "Hemorragia Intraventricular Bilateral",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_fisher_mod",
                "name": "Achados Tomográficos de Fisher Modificado (Claassen)",
                "slug": "achados-fisher-modificado",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_fm_cisternal",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Cruze a espessura da HSA cisternal com a presença de HIV bilateral.",
                "options": [
                    {
                        "id": "opt_fm_0",
                        "label": "Grau 0: Sem HSA cisternal e sem Hemorragia Intraventricular (HIV)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Ausência de sangue subaracnóideo cisternal e ausência de sangue nos ventrículos."
                    },
                    {
                        "id": "opt_fm_1",
                        "label": "Grau 1: Sangue fino (< 1 mm), SEM hemorragia intraventricular bilateral",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "HSA focal ou difusa fina (< 1 mm de espessura) sem sangue em ambos os ventrículos laterais."
                    },
                    {
                        "id": "opt_fm_2",
                        "label": "Grau 2: Sangue fino (< 1 mm), COM hemorragia intraventricular bilateral",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "HSA fina associada a sangramento intraventricular bilateral evidente."
                    },
                    {
                        "id": "opt_fm_3",
                        "label": "Grau 3: Sangue espesso (>= 1 mm), SEM hemorragia intraventricular bilateral",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Coágulos espessos >= 1 mm preenchendo cisternas basais sem sangue em ambos os ventrículos."
                    },
                    {
                        "id": "opt_fm_4",
                        "label": "Grau 4: Sangue espesso (>= 1 mm), COM hemorragia intraventricular bilateral",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Coágulos espessos >= 1 mm associados a hemorragia intraventricular bilateral maciça."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_fm_low",
                "label": "Baixo Risco de DCI (Fisher Modificado 0 e 1)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Grau 0: Vasoespasmo 0%, DCI 0%. Grau 1: Vasoespasmo sintomático ~2%, risco de Isquemia Cerebral Tardia (DCI) / infarto ~12% a 15%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fm_nimo",
                        "drugName": "Nimodipino 60 mg VO 4/4h por 21 dias contínuos",
                        "dosage": "60 mg VO 4/4h (PROIBIDO USO ENDOVENOSO)",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fm_obs",
                        "recommendationTitle": "Vigilância Clínica e Doppler Transcraniano a cada 48h",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "DTC seriado a cada 48 horas e oclusão urgente do aneurisma."
                    }
                ]
            },
            {
                "id": "tier_fm_mod",
                "label": "Risco Moderado a Alto de DCI (Fisher Modificado 2 e 3)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Grau 2: Vasoespasmo sintomático ~12%, risco de DCI ~25-30%. Grau 3: Vasoespasmo sintomático ~13%, risco de DCI ~35-40%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fm_mod_nimo",
                        "drugName": "Nimodipino 60 mg 4/4h",
                        "dosage": "60 mg VO 4/4h",
                        "route": "Via Oral ou Enteral",
                        "frequency": "4/4 horas"
                    },
                    {
                        "id": "rx_fm_mod_norepi",
                        "drugName": "Noradrenalina IV para Indução de Hipertensão se DCI Pós-Oclusão",
                        "dosage": "Titular para PAS 160-180 mmHg se déficit isquêmico",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "4 ampolas em 234 mL SG 5% (64 mcg/mL).",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fm_mod_dtc",
                        "recommendationTitle": "DTC Diário a cada 12-24h e Avaliação de Hidrocefalia",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Vigilância de hidrocefalia no Grau 2. Exclusão do aneurisma em < 24-72h."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_fm_crit",
                "label": "Risco Crítico / Máximo de DCI e Hidrocefalia (Fisher Modificado 4)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Vasoespasmo sintomático de 38% e taxa de infarto por Isquemia Cerebral Tardia (DCI) de 40% a 50%. Altíssima incidência de hidrocefalia hipertensiva obstrutiva.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_fm4_nimo",
                        "drugName": "Nimodipino 60 mg enteral 4/4h",
                        "dosage": "60 mg 4/4h por sonda enteral",
                        "route": "Enteral exclusiva",
                        "frequency": "4/4 horas"
                    },
                    {
                        "id": "rx_fm4_norepi",
                        "drugName": "Noradrenalina IV para Hipertensão Induzida em DCI Pós-Oclusão",
                        "dosage": "Titular PAS 160-180 mmHg em BIC exclusiva",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Solução concentrada 128 mcg/mL.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_fm4_dve",
                        "recommendationTitle": "Implantação Urgente de DVE e Resgate Intervencionista",
                        "dispositionTarget": "UTI Neurocrítica / Hemodinâmica",
                        "monitoringPlan": "DVE de emergência para drenagem liquórica e lavagem hemática intraventricular contínua. DTC a cada 12 horas.",
                        "interventionalProcedure": "Angioplastia transluminal com balão ou infusão superseletiva intra-arterial de Milrinona se vasoespasmo sintomático refratário pós-oclusão do aneurisma."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_spetzler_martin():
    return {
        "id": "calc_spetzler_martin",
        "slug": "spetzler-martin",
        "name": "Escala de Spetzler-Martin para MAV Cerebral",
        "acronym": "Spetzler-Martin",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurocirurgia Vascular e Malformações Vasculares",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Malformações Vasculares e MAV",
        "description": "Sistema morfológico angiográfico e radiológico de 1 a 5 pontos para estimar o risco de morbimortalidade neurológica definitiva na ressecção microcirúrgica de MAVs cerebrais.",
        "summary": "Sistema morfológico (1 a 5 pontos) para estimativa do risco cirúrgico de ressecção de MAV cerebral.",
        "clinicalObjective": "Quantificar o risco cirúrgico de novo déficit neurológico permanente pós-operatório na ressecção microcirúrgica de MAVs cerebrais.",
        "targetPopulation": "Pacientes com diagnóstico angiográfico e por RM de malformação arteriovenosa intra-axial cerebral.",
        "calculationType": "additive_points",
        "formulaExpression": "Tamanho_pontos + Eloquencia_pontos + Drenagem_pontos",
        "evidenceSource": "Spetzler RF, Martin NA. A proposed grading system for arteriovenous malformations. J Neurosurg. 1986;65(4):476-483.",
        "minPossibleScore": 1,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "neurocirurgia",
        "clinicalWarning": "ENSAIO CLÍNICO ARUBA (Lancet 2014): O ensaio clínico randomizado internacional ARUBA estabeleceu com evidência de Classe I que o manejo médico conservador é superior à intervenção cirúrgica ou endovascular na prevenção de morte e AVC em pacientes com MAVs não rotas. Graus IV e V devem ser mantidos prioritariamente em manejo conservador expectante.",
        "radarAxes": [
            {
                "id": "axis_sm_size",
                "label": "Tamanho do Nidus",
                "system": "Imagem",
                "unit": "cm",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_sm_eloquence",
                "label": "Eloquência Cortical/Subcortical",
                "system": "Neurológico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_sm_drainage",
                "label": "Drenagem Venosa Profunda",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_sm_size",
                "name": "Tamanho Máximo do Nidus Vascular",
                "slug": "tamanho-nidus",
                "inputType": "single_choice",
                "unit": "cm",
                "radarAxisId": "axis_sm_size",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Maior diâmetro do nidus na angiografia digital.",
                "options": [
                    {
                        "id": "opt_sm_size_small",
                        "label": "Pequeno (< 3 cm)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 1,
                        "description": "Maior dimensão do nidus vascular < 3 cm."
                    },
                    {
                        "id": "opt_sm_size_medium",
                        "label": "Médio (3 a 6 cm)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.67,
                        "sortOrder": 2,
                        "description": "Maior dimensão do nidus vascular entre 3 e 6 cm."
                    },
                    {
                        "id": "opt_sm_size_large",
                        "label": "Grande (> 6 cm)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Maior dimensão do nidus vascular superior a 6 cm."
                    }
                ]
            },
            {
                "id": "grp_sm_eloquence",
                "name": "Eloquência da Área Cerebral Adjacente",
                "slug": "eloquencia-cortical",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_sm_eloquence",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Definição: córtex sensoriomotor, linguagem, visual primário, tálamo, núcleos da base ou tronco.",
                "options": [
                    {
                        "id": "opt_sm_eloq_no",
                        "label": "Área Não Eloquente",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Córtex frontal anterior, temporal anterior ou áreas sem função primária vital."
                    },
                    {
                        "id": "opt_sm_eloq_yes",
                        "label": "Área Eloquente (Linguagem, motor, visual, tálamo, tronco)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Área cortical ou subcortical primária crítica."
                    }
                ]
            },
            {
                "id": "grp_sm_drainage",
                "name": "Padrão de Drenagem Venosa",
                "slug": "drenagem-venosa",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_sm_drainage",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Presença de veias profundas drenando o nidus.",
                "options": [
                    {
                        "id": "opt_sm_drain_superficial",
                        "label": "Apenas Drenagem Superficial",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Drenagem venosa realizada exclusivamente para seios durais superficiais."
                    },
                    {
                        "id": "opt_sm_drain_deep",
                        "label": "Presença de Drenagem Profunda",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Drenagem venosa por veias cerebrais internas, basal de Rosenthal ou magna de Galeno."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_sm_low",
                "label": "Baixo Risco Cirúrgico - Graus I e II (Spetzler-Ponce Classe A)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Grau I: Risco de déficit neurológico cirúrgico permanente de 0% a < 3%. Grau II: Risco de déficit permanente ~5%. Altíssima taxa de cura cirúrgica completa (> 98%).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sm_postop_bp",
                        "drugName": "Controle Rigoroso de Pressão Arterial Pós-Operatória",
                        "dosage": "Manter PAS estritamente < 120 a 130 mmHg para prevenir a Síndrome de Hiperemia por Ruptura da Pressão Normal de Perfusão (NPPB)",
                        "route": "Intravenosa e Oral",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Titular Nitroprussiato de Sódio ou Esmolol no pós-op imediato.",
                        "contraindications": "Evitar picos pressóricos que sobrecarreguem vasos que perderam autorregulação crônica."
                    },
                    {
                        "id": "rx_sm_epilepsy",
                        "drugName": "Levetiracetam",
                        "dosage": "500 a 1000 mg VO 12/12h se crises epilépticas associadas",
                        "route": "Via Oral ou IV",
                        "frequency": "12/12 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sm_surgery",
                        "recommendationTitle": "Microcirurgia Ressectiva Primária Completa",
                        "dispositionTarget": "Centro Cirúrgico de Neurocirurgia / UTI Pós-Op",
                        "monitoringPlan": "Monitorização de PAM contínua e angiografia digital de controle pós-operatória precoce.",
                        "interventionalProcedure": "Microcirurgia ressectiva completa de escolha; embolização pré-operatória superseletiva opcional para pedículos profundos de difícil acesso."
                    }
                ]
            },
            {
                "id": "tier_sm_mod",
                "label": "Risco Cirúrgico Intermediário - Grau III (Spetzler-Ponce Classe B)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Morbidade cirúrgica permanente de 8% a 15% (podendo atingir 20% em lesões profundas). Grupo altamente heterogêneo.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sm3_anticonv",
                        "drugName": "Levetiracetam ou Oxcarbazepina",
                        "dosage": "Levetiracetam 500-1000 mg 12/12h para controle de epilepsia secundária",
                        "route": "Via Oral",
                        "frequency": "12/12 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sm3_multimodal",
                        "recommendationTitle": "Planejamento Terapêutico Multimodal Individualizado",
                        "dispositionTarget": "Ambulatório Especializado / UTI",
                        "monitoringPlan": "Avaliação por equipe multidisciplinar (Neurocirurgião vascular, Neurorradiologista intervencionista e Radioterapeuta).",
                        "interventionalProcedure": "Se pequena profunda (< 3 cm eloquente profunda): Radiocirurgia Estereotáxica (Gamma Knife 18-24 Gy). Se média superficial (3 a 6 cm não eloquente profunda): Embolização prévia estagiada seguida de microcirurgia aberta."
                    }
                ]
            },
            {
                "id": "tier_sm_high",
                "label": "Alto Risco Cirúrgico - Graus IV e V (Spetzler-Ponce Classe C) e VI",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Grau IV: Risco de morbidade permanente ou morte pós-cirúrgica de 31% a 40%. Grau V: Risco de 69% a 80%. Grau VI: Inoperável (100% de déficit devastador ou morte). O risco do tratamento cirúrgico excede o risco da história natural da MAV não rota.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sm_conservative_bp",
                        "drugName": "Manejo Clínico Medicamentoso Conservador e Otimização Pressórica",
                        "dosage": "Controle rigoroso de PA com anti-hipertensivos orais visando PAS < 130 mmHg",
                        "route": "Via Oral",
                        "frequency": "Diária",
                        "contraindications": "Intervenção microcirúrgica aberta de rotina é FORMALMENTE DESACONSELHADA."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_sm_aruba",
                        "recommendationTitle": "Manejo Médico Conservador de Escolha (Diretriz ARUBA)",
                        "dispositionTarget": "Seguimento Ambulatorial Especializado",
                        "monitoringPlan": "Manejo clínico expectante suportado pelo ensaio clínico randomizado ARUBA.",
                        "interventionalProcedure": "Intervenções cirúrgicas ou embolizações reservadas exclusivamente para: hemorragia aguda com hematoma expansivo com risco de herniação (evacuação pontual do coágulo) ou hidrocefalia obstrutiva progressiva (derivação liquórica DVP)."
                    }
                ]
            }
        ]
    }
