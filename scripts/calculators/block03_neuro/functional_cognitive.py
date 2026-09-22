"""
Block 03: Neurologia e Neurocirurgia
Módulo: Avaliação Funcional, Cognitiva e Neurodegenerativa
Calculadoras Clínicas Monográficas:
- mRS (Modified Rankin Scale)
- KPS (Karnofsky Performance Status)
- MEEM / MMSE (Mini-Exame do Estado Mental)
- MoCA (Montreal Cognitive Assessment)
- Hoehn & Yahr (Estadiamento Motor na Doença de Parkinson)
- EDSS (Expanded Disability Status Scale de Kurtzke)
"""

def get_mrs():
    return {
        "id": "calc_mrs",
        "slug": "mrs",
        "name": "Escala de Rankin Modificada",
        "acronym": "mRS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Avaliação Funcional e Desfechos Clínicos",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Avaliação Funcional e Desfechos Clínicos",
        "description": "Escala ordinal padronizada para mensuração global do grau de incapacidade, dependência funcional e autonomia nas atividades de vida diária após acidente vascular cerebral ou injúria neurológica aguda.",
        "summary": "Escala ordinal de 0 a 6 para mensuração de incapacidade e dependência funcional pós-AVC.",
        "clinicalObjective": "Quantificar a autonomia e o grau de dependência funcional nas atividades cotidianas, servindo como desfecho primário padrão (primary endpoint) em ensaios clínicos e na prática neurovascular.",
        "targetPopulation": "Pacientes pós-AVC isquêmico ou hemorrágico avaliados no estado pré-mórbido (basal) e no seguimento em 30, 90 e 365 dias.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_mRS_Selecionado",
        "evidenceSource": "van Swieten JC, Koudstaal PJ, Visser MC, et al. Interobserver agreement for the assessment of handicap in stroke patients. Stroke. 1988;19(5):604-607.",
        "minPossibleScore": 0,
        "maxPossibleScore": 6,
        "baseScore": 0,
        "badge": "funcional",
        "clinicalWarning": "ATENÇÃO: A fronteira crucial entre mRS 2 e mRS 3 reside na capacidade de VIVER SOZINHO DE FORMA INDEPENDENTE. Se o paciente deambula sem auxílio, mas requer que terceiros façam suas compras, preparem refeições ou administrem finanças/medicamentos, deve ser pontuado obrigatoriamente como mRS 3 (incapacidade moderada). A pontuação 6 corresponde a óbito.",
        "radarAxes": [
            {
                "id": "axis_mrs_autonomy",
                "label": "Grau de Dependência / AVD",
                "system": "Funcional",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 6
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_mrs_grade",
                "name": "Nível de Incapacidade Funcional (Grau mRS)",
                "slug": "grau-mrs",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_mrs_autonomy",
                "normalBaselineValue": 0,
                "maxAxisValue": 6,
                "sortOrder": 1,
                "helpText": "Selecione o grau que melhor descreve o estado funcional atual do paciente.",
                "options": [
                    {
                        "id": "opt_mrs_0",
                        "label": "Grau 0: Totalmente assintomático",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Nenhum sintoma neurológico residual ou queixa subjetiva. Vida e atividades completamente normais."
                    },
                    {
                        "id": "opt_mrs_1",
                        "label": "Grau 1: Incapacidade não significativa",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.17,
                        "sortOrder": 2,
                        "description": "Apresenta sintomas discretos (parestesia leve, disartria discreta), mas é plenamente capaz de realizar todos os deveres e atividades cotidianas prévias sem assistência."
                    },
                    {
                        "id": "opt_mrs_2",
                        "label": "Grau 2: Incapacidade leve (Independente para AVDs)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 3,
                        "description": "Incapaz de realizar todas as atividades anteriores (ex.: trabalhar ou dirigir), mas plenamente capaz de cuidar dos próprios assuntos pessoais e deambular sem ajuda de outra pessoa."
                    },
                    {
                        "id": "opt_mrs_3",
                        "label": "Grau 3: Incapacidade moderada (Caminha sem ajuda, requer assistência instrumental)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 4,
                        "description": "Requer assistência para atividades instrumentais (compras, preparo de alimentos, finanças, medicações), mas caminha de forma autônoma sem assistência física de terceiros (pode usar bengala/andador)."
                    },
                    {
                        "id": "opt_mrs_4",
                        "label": "Grau 4: Incapacidade moderadamente grave (Incapaz de caminhar sem ajuda)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.67,
                        "sortOrder": 5,
                        "description": "Incapaz de caminhar sem assistência física de outra pessoa e incapaz de atender às próprias necessidades fisiológicas/corporais sem ajuda contínua."
                    },
                    {
                        "id": "opt_mrs_5",
                        "label": "Grau 5: Incapacidade grave (Totalmente dependente e acamado)",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.83,
                        "sortOrder": 6,
                        "description": "Confinado ao leito, incontinente vesical e fecal, necessitando de cuidados de enfermagem integrais e assistência constante 24 horas por dia."
                    },
                    {
                        "id": "opt_mrs_6",
                        "label": "Grau 6: Óbito",
                        "pointValue": 6,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 7,
                        "description": "Morte do paciente decorrente do evento vascular ou de complicações secundárias."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_mrs_good",
                "label": "Independência Funcional / Desfecho Favorável (mRS 0 a 2)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Desfecho funcional favorável (Good Functional Outcome). Paciente capaz de viver de forma independente sem necessidade de cuidador no domicílio. Sobrevida em 1 ano superior a 90-95%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mrs_statin",
                        "drugName": "Atorvastatina (Terapia Hipolipemiante de Alta Potência)",
                        "dosage": "80 mg VO uma vez ao dia (à noite)",
                        "route": "Oral",
                        "frequency": "1x/dia",
                        "dilutionInstructions": "Comprimido via oral; não requer diluição.",
                        "renalAdjustment": "Não requer ajuste para insuficiência renal.",
                        "contraindications": "Hepatopatia ativa ou elevação inexplicada persistente de transaminases > 3x LSN."
                    },
                    {
                        "id": "rx_mrs_antiplatelet",
                        "drugName": "AAS (Ácido Acetilsalicílico) ou Clopidogrel (Prevenção Secundária)",
                        "dosage": "AAS 100 mg VO 1x/dia OU Clopidogrel 75 mg VO 1x/dia",
                        "route": "Oral",
                        "frequency": "1x/dia",
                        "dilutionInstructions": "Via oral com água após as refeições.",
                        "renalAdjustment": "Monitorar toxicidade renal; usar com cautela em DRC estágio 4/5.",
                        "contraindications": "Úlcera péptica ativa sangrante e coagulopatias severas."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_mrs_rehab",
                        "recommendationTitle": "Reabilitação Neurofuncional Ambulatorial e Prevenção Secundária",
                        "dispositionTarget": "Acompanhamento Ambulatorial de Neurologia / Fisioterapia",
                        "monitoringPlan": "Retorno médico em 30, 90 e 180 dias com perfil lipídico, hemoglobina glicada e monitoramento pressórico ambulatorial (MAPA/MRPA).",
                        "interventionalProcedure": "Programa de exercícios físicos aeróbicos moderados (150 min/semana), controle dietético DASH/mediterrânea e cessação completa do tabagismo."
                    }
                ]
            },
            {
                "id": "tier_mrs_mod",
                "label": "Incapacidade Moderada a Moderadamente Grave (mRS 3 a 4)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Perda da independência funcional para viver sozinho. Elevado risco de complicações clínicas secundárias (pneumonia por broncoaspiração, infecções urinárias e trombose venosa profunda).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mrs_vte_proph",
                        "drugName": "Enoxaparina Sódica (Profilaxia de TEV)",
                        "dosage": "40 mg SC uma vez ao dia (ou HNF 5.000 UI SC a cada 8 horas)",
                        "route": "Subcutânea",
                        "frequency": "1x/dia",
                        "dilutionInstructions": "Seringa pré-preenchida; injeção subcutânea na parede abdominal.",
                        "renalAdjustment": "Se ClCr < 30 mL/min: reduzir Enoxaparina para 20 mg SC 1x/dia ou substituir por HNF 5.000 UI SC 12/12h.",
                        "contraindications": "Sangramento ativo clinicamente significativo e plaquetopenia induzida por heparina (HIT)."
                    },
                    {
                        "id": "rx_mrs_spasticity",
                        "drugName": "Baclofeno (Controle de Espasticidade Muscular)",
                        "dosage": "5 mg VO a cada 8 horas, titulando semanalmente até 10 a 20 mg VO a cada 8 horas se tolerado",
                        "route": "Oral / Enteral",
                        "frequency": "8/8h",
                        "dilutionInstructions": "Comprimidos administrados com água ou via sonda enteral triturados.",
                        "renalAdjustment": "Excreção predominantemente renal; reduzir dose e monitorar sedação se ClCr < 50 mL/min.",
                        "contraindications": "Hipersensibilidade ao baclofeno; evitar retirada abrupta (risco de convulsões e hipertermia)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_mrs_swallow",
                        "recommendationTitle": "Avaliação Fonoaudiológica da Deglutição e Treino de Transferência",
                        "dispositionTarget": "Enfermaria de Cuidados Subagudos / Reabilitação Hospitalar",
                        "monitoringPlan": "Vigilância ativa para sinais de microaspiração brônquica e integridade cutânea em áreas de apoio.",
                        "interventionalProcedure": "Avaliação de deglutição à beira do leito (teste de deglutição de água); adaptação de dieta com líquidos espessados; passagem de SNE se disfagia grave; fisioterapia motora para marcha assistida."
                    }
                ]
            },
            {
                "id": "tier_mrs_severe",
                "label": "Dependência Funcional Grave / Acamado (mRS 5)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 5,
                "statisticalOutcome": "Dependência física integral 24 horas por dia. Mortalidade em 1 ano entre 40% e 60%. Elevadíssima incidência de lesões por pressão em estágio avançado e infecções nosocomiais.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mrs_palliative",
                        "drugName": "Racionalização Terapêutica e Terapia Sintomática",
                        "dosage": "Desprescrição de estatinas e medicamentos preventivos secundários se transição para cuidados paliativos exclusivos; manejo de dor e secreções.",
                        "route": "Oral / Enteral / Subcutânea",
                        "frequency": "Individualizada",
                        "dilutionInstructions": "Formas líquidas ou orodispersíveis se aplicável.",
                        "renalAdjustment": "Ajuste individualizado para medicações sintomáticas."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_mrs_comfort",
                        "recommendationTitle": "Cuidados de Conforto, Prevenção de Escaras e Gastrostomia",
                        "dispositionTarget": "Unidade de Cuidados Prolongados / Suporte Domiciliar (Home Care)",
                        "monitoringPlan": "Conferência familiar multidisciplinar sobre metas de cuidado, diretivas antecipadas de vontade e suporte paliativo.",
                        "interventionalProcedure": "Mudança sistemática de decúbito a cada 2 horas, colchão pneumático articulado com pressão alternada, higiene perianal rigorosa, e consideração de gastrostomia endoscópica (GTT) se nutrição enteral de longo prazo."
                    }
                ]
            },
            {
                "id": "tier_mrs_death",
                "label": "Óbito (mRS 6)",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 6,
                "statisticalOutcome": "Óbito confirmado. Desfecho desfavorável extremo.",
                "colorHex": "#1f2937",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_mrs_death_support",
                        "recommendationTitle": "Acolhimento Familiar e Procedimentos Administrativos",
                        "dispositionTarget": "Necrotério / Protocolo de Declaração de Óbito",
                        "monitoringPlan": "Preenchimento criterioso da Declaração de Óbito identificando a cadeia causal (ex.: Broncoaspiração devida a Sequela de AVC Isquêmico).",
                        "interventionalProcedure": "Apoio psicológico e acolhimento aos familiares enlutados."
                    }
                ]
            }
        ]
    }

def get_kps():
    return {
        "id": "calc_kps",
        "slug": "kps",
        "name": "Índice de Performance de Karnofsky",
        "acronym": "KPS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neuro-Oncologia e Avaliação Funcional",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neuro-Oncologia e Avaliação Funcional",
        "description": "Escala ordinal percentual de 0% a 100% que quantifica a capacidade funcional global, autonomia física e necessidade de suporte médico/assistencial em pacientes neuro-oncológicos.",
        "summary": "Escala percentual de 0% a 100% em 11 intervalos para estadiamento funcional em neuro-oncologia.",
        "clinicalObjective": "Avaliar a tolerabilidade a tratamentos oncológicos agressivos (Protocolo de Stupp, radiocirurgia e craniotomia com ressecção tumoral) e estratificar prognóstico de sobrevida global.",
        "targetPopulation": "Pacientes portadores de tumores do sistema nervoso central (Glioblastoma, Astrocitomas, Meningiomas, Metástases Encefálicas) e condições neurológicas crônicas graves.",
        "calculationType": "additive_points",
        "formulaExpression": "Percentual_KPS_Selecionado",
        "evidenceSource": "Karnofsky DA, Burchenal JH. The clinical evaluation of chemotherapeutic agents in cancer. In: MacLeod CM, ed. Evaluation of Chemotherapeutic Agents. Columbia Univ Press; 1949:191-205.",
        "minPossibleScore": 0,
        "maxPossibleScore": 100,
        "baseScore": 0,
        "badge": "oncologia",
        "clinicalWarning": "ATENÇÃO: A marca de KPS 70% é o divisor de águas crucial em neuro-oncologia. Pacientes com KPS >= 70% são autossuficientes e toleram radioquimioterapia combinada plena (Protocolo de Stupp com Temozolomida). Abaixo de 70%, o paciente perde autonomia para o autocuidado diário e requer avaliação individualizada quanto a regimes hipofracionados de radioterapia ou transição para cuidados paliativos exclusivos.",
        "radarAxes": [
            {
                "id": "axis_kps_performance",
                "label": "Capacidade Funcional / KPS",
                "system": "Oncológico/Funcional",
                "unit": "%",
                "baselineValue": 100,
                "maxAxisValue": 100
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_kps_level",
                "name": "Nível de Desempenho Funcional Karnofsky",
                "slug": "desempenho-karnofsky",
                "inputType": "single_choice",
                "unit": "%",
                "radarAxisId": "axis_kps_performance",
                "normalBaselineValue": 100,
                "maxAxisValue": 100,
                "sortOrder": 1,
                "helpText": "Selecione o percentual que reflete com maior exatidão a condição clínica e funcional do paciente.",
                "options": [
                    {
                        "id": "opt_kps_100",
                        "label": "100%: Normal, sem queixas",
                        "pointValue": 100,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Capaz de atividade física normal; sem sinais ou sintomas clínicos de doença (Equivalente ECOG 0)."
                    },
                    {
                        "id": "opt_kps_90",
                        "label": "90%: Capaz de atividade normal com sinais mínimos",
                        "pointValue": 90,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.10,
                        "sortOrder": 2,
                        "description": "Capaz de manter atividade habitual normal; sinais ou sintomas clínicos muito discretos (Equivalente ECOG 0)."
                    },
                    {
                        "id": "opt_kps_80",
                        "label": "80%: Atividade normal com esforço",
                        "pointValue": 80,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.20,
                        "sortOrder": 3,
                        "description": "Mantém atividade normal com esforço evidente; apresenta alguns sintomas moderados de doença (Equivalente ECOG 1)."
                    },
                    {
                        "id": "opt_kps_70",
                        "label": "70%: Cuida de si mesmo, mas incapaz de trabalho ativo",
                        "pointValue": 70,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.30,
                        "sortOrder": 4,
                        "description": "Plenamente autossuficiente para o autocuidado diário; totalmente incapaz de realizar trabalho ativo habitual (Equivalente ECOG 1)."
                    },
                    {
                        "id": "opt_kps_60",
                        "label": "60%: Requer assistência ocasional",
                        "pointValue": 60,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.40,
                        "sortOrder": 5,
                        "description": "Cuida da maioria das próprias necessidades, mas necessita de assistência ocasional de terceiros (Equivalente ECOG 2)."
                    },
                    {
                        "id": "opt_kps_50",
                        "label": "50%: Requer assistência considerável e cuidados médicos frequentes",
                        "pointValue": 50,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.50,
                        "sortOrder": 6,
                        "description": "Incapacitado para a maior parte das atividades cotidianas; requer cuidados médicos e de enfermagem constantes (Equivalente ECOG 2)."
                    },
                    {
                        "id": "opt_kps_40",
                        "label": "40%: Incapaz; requer cuidados especiais e assistência contínua",
                        "pointValue": 40,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.60,
                        "sortOrder": 7,
                        "description": "Severamente incapacitado; passa mais de 50% das horas de vigília no leito; requer cuidados de enfermagem especializados (Equivalente ECOG 3)."
                    },
                    {
                        "id": "opt_kps_30",
                        "label": "30%: Severamente incapacitado; indicação de internação",
                        "pointValue": 30,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.70,
                        "sortOrder": 8,
                        "description": "Internação hospitalar formalmente indicada, embora a morte não seja iminente (Equivalente ECOG 3)."
                    },
                    {
                        "id": "opt_kps_20",
                        "label": "20%: Muito doente; suporte ativo de vida necessário",
                        "pointValue": 20,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.80,
                        "sortOrder": 9,
                        "description": "Hospitalização obrigatória para suporte vital ativo e tratamento de suporte intensivo (Equivalente ECOG 4)."
                    },
                    {
                        "id": "opt_kps_10",
                        "label": "10%: Moribundo; processos fatais em progressão rápida",
                        "pointValue": 10,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.90,
                        "sortOrder": 10,
                        "description": "Processo de morte em curso rápido e irreversível (Equivalente ECOG 4)."
                    },
                    {
                        "id": "opt_kps_0",
                        "label": "0%: Óbito",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 11,
                        "description": "Morte confirmada (Equivalente ECOG 5)."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_kps_high",
                "label": "Alto Desempenho Funcional / Autossuficiente (KPS 80% a 100%)",
                "severityLevel": "low",
                "minScore": 80,
                "maxScore": 100,
                "statisticalOutcome": "Excelente tolerabilidade a radioquimioterapia agressiva. Em glioblastoma multiforme recém-diagnosticado, elegibilidade formal ao Protocolo de Stupp completo. Sobrevida mediana significativamente superior.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kps_temozolomide",
                        "drugName": "Temozolomida (Protocolo de Stupp em Glioblastoma)",
                        "dosage": "Fase concomitante: 75 mg/m²/dia VO durante as 6 semanas de radioterapia. Fase adjuvante: 150 mg/m²/dia (ciclo 1) e 200 mg/m²/dia (ciclos 2-6) por 5 dias a cada 28 dias",
                        "route": "Oral",
                        "frequency": "Conforme protocolo Stupp",
                        "dilutionInstructions": "Administrar com estômago vazio (1 hora antes ou 2 horas após refeição); associar antiemético (Ondansetrona 8 mg VO 30 min antes).",
                        "renalAdjustment": "Usar com cautela se ClCr < 30 mL/min; monitorar hemograma semanal (risco de mielossupressão grave).",
                        "contraindications": "Mielossupressão severa preexistente (plaquetas < 100.000/mm³ ou neutrófilos < 1.500/mm³)."
                    },
                    {
                        "id": "rx_kps_dexa",
                        "drugName": "Dexametasona (Controle de Edema Cerebral Vasogênico)",
                        "dosage": "4 a 8 mg/dia VO fracionados a cada 12 horas, associado a Pantoprazol 40 mg/dia VO",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Comprimidos via oral; titular sempre para a menor dose eficaz.",
                        "renalAdjustment": "Não requer ajuste de dose para função renal.",
                        "contraindications": "Infecções fúngicas sistêmicas não controladas; monitorar glicemia e miopatia por corticoide."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kps_stupp_rt",
                        "recommendationTitle": "Ressecção Microcirúrgica Máxima e Radioterapia Fracionada (60 Gy)",
                        "dispositionTarget": "Ambulatório Especializado de Neuro-Oncologia / Radioterapia",
                        "monitoringPlan": "Ressonância magnética de crânio com protocolo de perfusão a cada 2 a 3 meses para diferenciar pseudoprogressão de recidiva tumoral verdadeira.",
                        "interventionalProcedure": "Ressecção microcirúrgica ampla guiada por neuronavegação e fluorescência com 5-ALA, seguida de Radioterapia Conformacional Tridimensional (3D-CRT) ou IMRT: 60 Gy em 30 frações de 2,0 Gy ao longo de 6 semanas."
                    }
                ]
            },
            {
                "id": "tier_kps_int",
                "label": "Desempenho Funcional Intermediário (KPS 60% a 70%)",
                "severityLevel": "intermediate",
                "minScore": 60,
                "maxScore": 70,
                "statisticalOutcome": "Tolerabilidade moderada a tratamentos citotóxicos. Risco aumentado de toxicidade medular e infecções oportunistas. Sobrevida mediana intermediária (6 a 12 meses em neoplasias malignas de alto grau).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kps_dexa_mod",
                        "drugName": "Dexametasona (Manejo Otimizado do Efeito de Massa)",
                        "dosage": "8 a 16 mg/dia IV ou VO divididos a cada 6 a 12 horas com protetor gástrico",
                        "route": "Oral / Intravenosa",
                        "frequency": "8/8h ou 12/12h",
                        "dilutionInstructions": "Ampolas de 4 mg/mL; se IV, administrar em bolus lento.",
                        "renalAdjustment": "Sem necessidade de ajuste renal.",
                        "contraindications": "Hipersensibilidade à dexametasona."
                    },
                    {
                        "id": "rx_kps_levetiracetam",
                        "drugName": "Levetiracetam (Prevenção e Tratamento de Crises Epilépticas Tumorais)",
                        "dosage": "500 mg a 1000 mg VO/IV a cada 12 horas",
                        "route": "Oral / Intravenosa",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Droga de escolha por não ter indução enzimática do citocromo P450, evitando interação com quimioterápicos.",
                        "renalAdjustment": "Ajustar dose se ClCr < 50 mL/min (reduzir para 500 mg 12/12h ou 500 mg 1x/dia se hemodiálise).",
                        "contraindications": "Hipersensibilidade ao levetiracetam; monitorar agitação psicomotora e alterações comportamentais."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kps_hypo_rt",
                        "recommendationTitle": "Radioterapia Hipofracionada e Fisioterapia Motora",
                        "dispositionTarget": "Hospital de Dia Oncológico / Fisioterapia Neurofuncional",
                        "monitoringPlan": "Avaliação semanal de força muscular, fadiga e balanço hídrico.",
                        "interventionalProcedure": "Considerar regime de Radioterapia Hipofracionada (ex.: 40 Gy em 15 frações de 2,67 Gy ou 34 Gy em 10 frações) para minimizar toxicidade e fadiga em pacientes fragilizados."
                    }
                ]
            },
            {
                "id": "tier_kps_low",
                "label": "Baixo Desempenho Funcional / Dependência Grave (KPS 10% a 50%)",
                "severityLevel": "critical",
                "minScore": 10,
                "maxScore": 50,
                "statisticalOutcome": "Altíssimo risco de toxicidade fatal se exposto a esquemas agressivos de quimioterapia ou craniotomia ampla. Sobrevida mediana estimada em semanas a poucos meses. Indicação mandatória de transição para Cuidados Paliativos Exclusivos.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_kps_palliative_pain",
                        "drugName": "Morfina / Fentanil (Controle Paliativo de Dor e Dispneia)",
                        "dosage": "Morfina 5 a 10 mg VO a cada 4 horas ou Fentanil transdérmico 12 a 25 mcg/h a cada 72 horas",
                        "route": "Oral / Transdérmica / Subcutânea",
                        "frequency": "Conforme escala analgésica",
                        "dilutionInstructions": "Via subcutânea ou oral; associar laxativo profilático (Óleo mineral ou Macrogol).",
                        "renalAdjustment": "Morfina acumula metabólitos ativos na insuficiência renal grave; preferir Fentanil ou Metadona se ClCr < 30 mL/min.",
                        "contraindications": "Depressão respiratória grave não monitorada."
                    },
                    {
                        "id": "rx_kps_dexa_palliative",
                        "drugName": "Dexametasona (Alívio Sintomático de Hipertensão Intracraniana)",
                        "dosage": "4 a 8 mg/dia VO/SC pela manhã para manutenção de vigília e alívio de cefaleia",
                        "route": "Oral / Subcutânea",
                        "frequency": "1x/dia pela manhã",
                        "dilutionInstructions": "Administrar pela manhã para mitigar insônia.",
                        "renalAdjustment": "Sem ajuste de dose.",
                        "contraindications": "Desprescrever gradualmente se refratariedade e fase terminal de vida."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kps_hospice",
                        "recommendationTitle": "Plano Terapêutico Singular de Cuidados Paliativos Exclusivos",
                        "dispositionTarget": "Unidade de Cuidados Paliativos (Hospice) ou Domicílio",
                        "monitoringPlan": "Foco integral no controle de sintomas desfavoráveis (dor, náuseas, delírio, estertor pré-morte).",
                        "interventionalProcedure": "Evitar transferências desnecessárias para UTI, procedimentos invasivos fúteis e intubação orotraqueal. Reunião familiar estruturada para pactuação de diretivas antecipadas de vontade."
                    }
                ]
            },
            {
                "id": "tier_kps_death",
                "label": "Óbito (KPS 0%)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Óbito confirmado.",
                "colorHex": "#1f2937",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_kps_death_admin",
                        "recommendationTitle": "Acolhimento Familiar e Declaração de Óbito",
                        "dispositionTarget": "Necrotério / Protocolo de Declaração de Óbito",
                        "monitoringPlan": "Preenchimento criterioso da causa básica tumoral do óbito.",
                        "interventionalProcedure": "Suporte e acolhimento multiprofissional aos familiares enlutados."
                    }
                ]
            }
        ]
    }

def get_meem_mmse():
    return {
        "id": "calc_meem_mmse",
        "slug": "meem-mmse",
        "name": "Mini-Exame do Estado Mental (MEEM / MMSE)",
        "acronym": "MEEM / MMSE",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Avaliação Neurocognitiva e Demências",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Avaliação Neurocognitiva e Demências",
        "description": "Instrumento padronizado de rastreio neurocognitivo quantitativo que avalia 7 domínios em 30 pontos, com pontos de corte rigorosamente ajustados pela escolaridade segundo as normas brasileiras (Brucki / Bertolucci).",
        "summary": "Rastreio cognitivo quantitativo de 0 a 30 pontos com cortes educacionais brasileiros.",
        "clinicalObjective": "Rastrear declínio cognitivo objetivo, monitorar a progressão de demências (Alzheimer, Demência Vascular, Demência com Corpos de Lewy) e guiar a introdução de inibidores da colinesterase e memantina.",
        "targetPopulation": "Indivíduos adultos e idosos com queixa de perda de memória, lentificação cognitiva ou suspeita de síndrome demencial.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma_Pontos_Dominios (0 a 30)",
        "evidenceSource": "Folstein MF, Folstein SE, McHugh PR. 'Mini-mental state'. A practical method for grading the cognitive state of patients for the clinician. J Psychiatr Res. 1975;12(3):189-198. Validação brasileira: Brucki SMD, et al. Arq Neuropsiquiatr. 2003;61(3B):777-781; Bertolucci PH, et al. Arq Neuropsiquiatr. 1994;52(1):1-7.",
        "minPossibleScore": 0,
        "maxPossibleScore": 30,
        "baseScore": 0,
        "badge": "cognitivo",
        "clinicalWarning": "ATENÇÃO: O MEEM apresenta marcado EFEITO TETO em indivíduos com alta escolaridade (>11 anos), nos quais pontuações de 28 a 30 podem ocultar Comprometimento Cognitivo Leve (CCL). Nestes casos, a aplicação do MoCA (Montreal Cognitive Assessment) é mandatória. O teste é inválido na vigência de delirium agudo, afasia densa ou déficit sensorial (cegueira/surdez) não corrigido.",
        "radarAxes": [
            {
                "id": "axis_meem_orient",
                "label": "Orientação e Atenção",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 15,
                "maxAxisValue": 15
            },
            {
                "id": "axis_meem_memory",
                "label": "Memória e Registro",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 6,
                "maxAxisValue": 6
            },
            {
                "id": "axis_meem_language",
                "label": "Linguagem e Praxia",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 9,
                "maxAxisValue": 9
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_meem_time",
                "name": "1. Orientação Temporal (0 a 5 pontos)",
                "slug": "orientacao-temporal",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_orient",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Pergunte: Que ano estamos? Que estação do ano é? Em que mês estamos? Que dia do mês é hoje? Que dia da semana é hoje? (1 ponto por resposta exata)",
                "options": [
                    {"id": "opt_meem_time_5", "label": "5 acertos (Ano, estação, mês, dia do mês e dia da semana corretos)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_time_4", "label": "4 acertos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_meem_time_3", "label": "3 acertos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_meem_time_2", "label": "2 acertos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_meem_time_1", "label": "1 acerto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_meem_time_0", "label": "0 acertos (Erra todas as perguntas de tempo)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_meem_space",
                "name": "2. Orientação Espacial (0 a 5 pontos)",
                "slug": "orientacao-espacial",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_orient",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 2,
                "helpText": "Pergunte: Em que país estamos? Em que estado estamos? Em que cidade estamos? Onde estamos agora (hospital/posto/consultório)? Em que andar/sala estamos? (1 ponto por acerto)",
                "options": [
                    {"id": "opt_meem_space_5", "label": "5 acertos (País, estado, cidade, local e andar corretos)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_space_4", "label": "4 acertos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_meem_space_3", "label": "3 acertos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_meem_space_2", "label": "2 acertos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_meem_space_1", "label": "1 acerto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_meem_space_0", "label": "0 acertos (Desorientação espacial completa)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_meem_reg",
                "name": "3. Memória de Registro Imediato (0 a 3 pontos)",
                "slug": "registro-imediato",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_memory",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 3,
                "helpText": "Diga claramente: 'Carro', 'Vaso', 'Tijolo' (1 segundo por palavra). Peça para repetir imediatamente. Pontue apenas a primeira tentativa (1 ponto por palavra repetida).",
                "options": [
                    {"id": "opt_meem_reg_3", "label": "3 palavras repetidas imediatamente na primeira tentativa", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_reg_2", "label": "2 palavras repetidas", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_meem_reg_1", "label": "1 palavra repetida", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_meem_reg_0", "label": "0 palavras repetidas", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_meem_calc",
                "name": "4. Atenção e Cálculo (0 a 5 pontos)",
                "slug": "atencao-e-calculo",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_orient",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 4,
                "helpText": "Subtração seriada de 7 a partir de 100: 93, 86, 79, 72, 65 (1 pt por cálculo correto). Alternativa se analfabeto ou recusa: Soletrar a palavra 'MUNDO' de trás para frente (O-D-N-U-M).",
                "options": [
                    {"id": "opt_meem_calc_5", "label": "5 acertos (5 subtrações corretas ou soletração inversa perfeita)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_calc_4", "label": "4 acertos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_meem_calc_3", "label": "3 acertos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_meem_calc_2", "label": "2 acertos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_meem_calc_1", "label": "1 acerto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_meem_calc_0", "label": "0 acertos", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_meem_recall",
                "name": "5. Memória de Evocação Tardia (0 a 3 pontos)",
                "slug": "evocacao-tardia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_memory",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 5,
                "helpText": "Peça para lembrar as 3 palavras que foram repetidas anteriormente ('Carro', 'Vaso', 'Tijolo'). 1 ponto por cada palavra evocada espontaneamente sem pistas.",
                "options": [
                    {"id": "opt_meem_recall_3", "label": "3 palavras recordadas espontaneamente", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_recall_2", "label": "2 palavras recordadas", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_meem_recall_1", "label": "1 palavra recordada", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_meem_recall_0", "label": "0 palavras recordadas (Amnésia anterógrada de evocação)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_meem_naming",
                "name": "6. Linguagem: Nomeação (0 a 2 pontos)",
                "slug": "nomeacao",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 2,
                "maxAxisValue": 2,
                "sortOrder": 6,
                "helpText": "Aponte para um relógio de pulso e para uma caneta. Pergunte o que é. 1 ponto por objeto nomeado corretamente.",
                "options": [
                    {"id": "opt_meem_naming_2", "label": "2 objetos nomeados corretamente (Relógio e Caneta)", "pointValue": 2, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_naming_1", "label": "1 objeto nomeado", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2},
                    {"id": "opt_meem_naming_0", "label": "0 objetos nomeados (Anomia)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3}
                ]
            },
            {
                "id": "grp_meem_repeat",
                "name": "7. Linguagem: Repetição de Frase (0 a 1 ponto)",
                "slug": "repeticao-frase",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "helpText": "Peça para o paciente repetir a frase exata: 'Nem aqui, nem ali, nem lá'. Apenas 1 tentativa permitida.",
                "options": [
                    {"id": "opt_meem_rep_1", "label": "Repetição exata e correta da frase (1 ponto)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_rep_0", "label": "Erro ou omissão na repetição da frase (0 pontos)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_meem_command",
                "name": "8. Linguagem: Comando em 3 Estágios (0 a 3 pontos)",
                "slug": "comando-3-estagios",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 8,
                "helpText": "Dê uma folha em branco e diga: 'Pegue este papel com a mão direita (1 pt), dobre-o ao meio (1 pt) e coloque-o no chão (1 pt)'.",
                "options": [
                    {"id": "opt_meem_cmd_3", "label": "Executa os 3 estágios corretamente", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_cmd_2", "label": "Executa 2 estágios", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_meem_cmd_1", "label": "Executa 1 estágio", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_meem_cmd_0", "label": "Não executa nenhum estágio (Apraxia / déficit de compreensão)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_meem_read",
                "name": "9. Linguagem: Leitura e Execução (0 a 1 ponto)",
                "slug": "leitura-execucao",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 9,
                "helpText": "Mostre a frase escrita em letras grandes: 'FECHE OS OLHOS'. Peça para o paciente ler e fazer o que está escrito. Pontue 1 se fechar os olhos.",
                "options": [
                    {"id": "opt_meem_read_1", "label": "Lê e fecha os olhos corretamente (1 ponto)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_read_0", "label": "Não executa ou apenas lê em voz alta sem fechar (0 pontos)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_meem_write",
                "name": "10. Linguagem: Escrita de Frase (0 a 1 ponto)",
                "slug": "escrita-frase",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 10,
                "helpText": "Peça para o paciente escrever uma frase completa espontânea. Deve conter sujeito, verbo e ter sentido compreensível. Erros gramaticais menores são aceitos.",
                "options": [
                    {"id": "opt_meem_write_1", "label": "Escreve frase completa com sujeito, verbo e sentido (1 ponto)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_write_0", "label": "Não escreve, escreve apenas palavras soltas ou sem sentido (0 pontos)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            },
            {
                "id": "grp_meem_praxia",
                "name": "11. Praxia Construtiva: Cópia dos Pentágonos (0 a 1 ponto)",
                "slug": "copia-pentagonos",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_meem_language",
                "normalBaselineValue": 1,
                "maxAxisValue": 1,
                "sortOrder": 11,
                "helpText": "Peça para o paciente copiar o desenho de dois pentágonos regulares que se sobrepõem formando um quadrilátero na interseção. Todos os 10 ângulos devem estar presentes.",
                "options": [
                    {"id": "opt_meem_praxia_1", "label": "Cópia correta com 10 ângulos e interseção em quadrilátero (1 ponto)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_meem_praxia_0", "label": "Cópia incorreta, distorcida ou sem interseção pentagonal (0 pontos)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_meem_severe_decline",
                "label": "Rastreio Positivo / Declínio Cognitivo Significativo (0 a 19 pontos)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 19,
                "statisticalOutcome": "Abaixo da nota de corte brasileira para qualquer nível de escolaridade (inclusive analfabetos <= 20). Forte indicativo de síndrome demencial em fase moderada a grave ou quadro confusional agudo sobreposto.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_meem_donepezil",
                        "drugName": "Donepezila (Inibidor da Acetilcolinesterase)",
                        "dosage": "5 mg VO uma vez ao dia à noite por 4 semanas, escalonando para 10 mg VO 1x/dia se boa tolerância",
                        "route": "Oral",
                        "frequency": "1x/dia à noite",
                        "dilutionInstructions": "Comprimido via oral; tomar à noite para mitigar efeitos colaterais colinérgicos (náuseas/diarreia).",
                        "renalAdjustment": "Não requer ajuste renal. Em insuficiência hepática leve a moderada, utilizar com cautela.",
                        "contraindications": "Bradicardia sinusal sintomática, bloqueio atrioventricular (BAV de 2º ou 3º grau), doença ulcerosa péptica ativa e asma grave."
                    },
                    {
                        "id": "rx_meem_memantine",
                        "drugName": "Memantina (Antagonista Não Competitivo dos Receptores NMDA)",
                        "dosage": "5 mg/dia VO pela manhã, aumentando 5 mg/dia semanalmente até a dose-alvo de 10 mg VO a cada 12 horas (20 mg/dia)",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Comprimidos administrados com ou sem alimentos.",
                        "renalAdjustment": "Se ClCr entre 30 e 49 mL/min: dose máxima 10 mg/dia. Se ClCr entre 15 e 29 mL/min: dose máxima 10 mg/dia. Se ClCr < 15 mL/min: uso não recomendado.",
                        "contraindications": "Hipersensibilidade à memantina e insuficiência renal terminal."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_meem_rev_workup",
                        "recommendationTitle": "Investigação Laboratorial de Demências Reversíveis e RM Encefálica",
                        "dispositionTarget": "Ambulatório de Neurologia Cognitiva / Geriatria",
                        "monitoringPlan": "Painel laboratorial obrigatório: Vitamina B12 sérica, TSH, VDRL/FTA-ABS, sorologia para HIV, função renal, eletrólitos e enzimas hepáticas. Se Vit B12 < 350 pg/mL, repor Cianocobalamina 1000 mcg/dia IM ou VO.",
                        "interventionalProcedure": "Ressonância magnética de crânio com cortes coronais finos em T1 ponderado para mensuração da atrofia do hipocampo (Escala de Scheltens / MTA) e exclusão de hidrocefalia de pressão normal ou lesões vasculares."
                    }
                ]
            },
            {
                "id": "tier_meem_mild_decline",
                "label": "Rastreio Limítrofe / Anormal para Baixa Escolaridade (20 a 25 pontos)",
                "severityLevel": "intermediate",
                "minScore": 20,
                "maxScore": 25,
                "statisticalOutcome": "Abaixo do corte de normalidade para indivíduos com 1 a 4 anos de estudo (corte <= 25) e 5 a 8 anos (corte <= 26). Em analfabetos, situa-se na faixa limítrofe superior. Alta suspeição de demência em fase inicial ou CCL com acometimento funcional inicial.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_meem_rivastigmine",
                        "drugName": "Rivastigmina Transdérmica (Opção Terapêutica em Intolerância Gastrointestinal)",
                        "dosage": "Adesivo transdérmico 4,6 mg/24h por 4 semanas, aumentando para 9,5 mg/24h como dose de manutenção",
                        "route": "Transdérmica",
                        "frequency": "Adesivo trocado a cada 24 horas",
                        "dilutionInstructions": "Aplicar em pele limpa, seca e sem pelos no dorso ou braço superior; alternar o local diariamente.",
                        "renalAdjustment": "Não requer ajuste de dose para disfunção renal.",
                        "contraindications": "Dermatite de contato alérgica prévia à rivastigmina."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_meem_rehab_cogn",
                        "recommendationTitle": "Reabilitação Neuropsicológica e Suporte ao Cuidador",
                        "dispositionTarget": "Ambulatório de Reabilitação Cognitiva",
                        "monitoringPlan": "Reaplicação seriada do MEEM a cada 6 meses e aplicação complementar da escala de Pfeffer (FAQ - Questionário de Atividades Funcionais) para confirmar impacto nas AVDs instrumentais.",
                        "interventionalProcedure": "Treino estruturado de memória e estratégias compensatórias (uso de agenda, alarmes, calendários visuais e rotinas fixas)."
                    }
                ]
            },
            {
                "id": "tier_meem_borderline_high",
                "label": "Rastreio Limítrofe para Média / Alta Escolaridade (26 a 28 pontos)",
                "severityLevel": "intermediate",
                "minScore": 26,
                "maxScore": 28,
                "statisticalOutcome": "Normal para analfabetos e indivíduos com até 4 anos de estudo. Porém, ANORMAL para indivíduos com 9 a 11 anos de escolaridade (corte <= 28) e acima de 11 anos / superior (corte <= 29). Suspeição de Comprometimento Cognitivo Leve (CCL).",
                "colorHex": "#3b82f6",
                "pharmacologicalActions": [
                    {
                        "id": "rx_meem_deprescribe",
                        "drugName": "Revisão e Desprescrição de Fármacos Anticolinérgicos e Sedativos",
                        "dosage": "Suspender gradualmente benzodiazepínicos, antidepressivos tricíclicos (Amitriptilina), antivertiginosos (Cinarizina/Flunarizina) e antiespasmódicos vesicais (Oxibutinina)",
                        "route": "Oral",
                        "frequency": "Individualizada",
                        "dilutionInstructions": "Desmame gradual para evitar abstinência.",
                        "renalAdjustment": "Avaliar função renal para excreção de sedativos."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_meem_moca_req",
                        "recommendationTitle": "Aplicação Mandatória do MoCA para Avaliação Executiva",
                        "dispositionTarget": "Avaliação Neuropsicológica Formal",
                        "monitoringPlan": "Devido ao efeito teto do MEEM nesta faixa de escolaridade, aplicar obrigatoriamente a bateria MoCA (Montreal Cognitive Assessment) e avaliação neuropsicológica extensa.",
                        "interventionalProcedure": "Estímulo à reserva cognitiva, atividade física aeróbica regular (150 min/semana), controle rigoroso de hipertensão e diabetes e dieta mediterrânea/MIND."
                    }
                ]
            },
            {
                "id": "tier_meem_normal",
                "label": "Rastreio Cognitivo Globalmente Normal (29 a 30 pontos)",
                "severityLevel": "low",
                "minScore": 29,
                "maxScore": 30,
                "statisticalOutcome": "Desempenho cognitivo quantitativo dentro da normalidade para todos os estratos educacionais segundo normas de Bertolucci (1994) e Brucki (2003). Se houver queixa subjetiva persistente em indivíduo de alta escolaridade, aplicar MoCA para rastreio de CCL.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_meem_lifestyle",
                        "recommendationTitle": "Promoção de Saúde Cerebral e Reserva Cognitiva",
                        "dispositionTarget": "Atenção Primária à Saúde / Medicina Preventiva",
                        "monitoringPlan": "Reavaliação anual se persistirem queixas subjetivas de memória.",
                        "interventionalProcedure": "Engajamento em atividades intelectualmente estimulantes, convívio social ativo, sono reparador (7-8 horas) e manejo de estresse."
                    }
                ]
            }
        ]
    }

def get_moca():
    return {
        "id": "calc_moca",
        "slug": "moca",
        "name": "Montreal Cognitive Assessment",
        "acronym": "MoCA",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Avaliação Neurocognitiva e Demências",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Avaliação Neurocognitiva e Demências",
        "description": "Instrumento de triagem cognitiva de alta sensibilidade para detecção precoce de Comprometimento Cognitivo Leve (CCL / MCI) e avaliação aprofundada de funções executivas frontais, memória de trabalho e habilidades visuoespaciais.",
        "summary": "Rastreio neurocognitivo sensível para CCL (0 a 30 pontos) com correção de escolaridade.",
        "clinicalObjective": "Identificar disfunções cognitivas sutis e Comprometimento Cognitivo Leve em indivíduos que pontuam falsamente normal no MEEM, com sensibilidade superior a 90%.",
        "targetPopulation": "Adultos e idosos com queixas cognitivas subjetivas, histórico de AVC isquêmico menor, traumatismo craniano ou fatores de risco neurodegenerativos.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma_Dominios (0 a 30) + (1 ponto se Escolaridade <= 12 anos; maximo 30)",
        "evidenceSource": "Nasreddine ZS, Phillips NA, Bédirian V, et al. The Montreal Cognitive Assessment, MoCA: a brief screening tool for mild cognitive impairment. J Am Geriatr Soc. 2005;53(4):695-699.",
        "minPossibleScore": 0,
        "maxPossibleScore": 30,
        "baseScore": 0,
        "badge": "cognitivo",
        "clinicalWarning": "ATENÇÃO: A pontuação de normalidade padrão internacional é >= 26 pontos. O ajuste educacional é obrigatório: SE O PACIENTE TIVER 12 ANOS OU MENOS DE ESCOLARIDADE FORMAL, ADICIONE EXATAMENTE +1 PONTO AO ESCORE FINAL (até o teto máximo de 30 pontos). Sem este ajuste, a taxa de falsos-positivos para CCL eleva-se substancialmente em populações brasileiras.",
        "radarAxes": [
            {
                "id": "axis_moca_executive",
                "label": "Funções Executivas e Visuoespacial",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 7,
                "maxAxisValue": 7
            },
            {
                "id": "axis_moca_attention",
                "label": "Atenção e Memória de Trabalho",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 6,
                "maxAxisValue": 6
            },
            {
                "id": "axis_moca_memory_lang",
                "label": "Memória Tardia e Linguagem",
                "system": "Cognitivo",
                "unit": "pts",
                "baselineValue": 17,
                "maxAxisValue": 17
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_moca_visuo",
                "name": "1. Visuoespacial / Executivo (0 a 5 pontos)",
                "slug": "visuoespacial-executivo",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_executive",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Trilha Alternada B (1 pt), Cópia do Cubo tridimensional (1 pt), Desenho do Relógio (Contorno 1 pt, Números 1 pt, Ponteiros indicando 11h10 1 pt = 3 pts). Total do domínio: 5 pontos.",
                "options": [
                    {"id": "opt_moca_visuo_5", "label": "5 pontos (Trilha, Cubo e Relógio perfeitos)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_visuo_4", "label": "4 pontos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_moca_visuo_3", "label": "3 pontos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_moca_visuo_2", "label": "2 pontos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_moca_visuo_1", "label": "1 ponto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_moca_visuo_0", "label": "0 pontos (Disfunção executiva / visuoespacial grave)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_moca_naming",
                "name": "2. Nomeação de Animais (0 a 3 pontos)",
                "slug": "nomeacao-animais",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_memory_lang",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Identificar as figuras de 3 animais da prancha: Leão, Rinoceronte, Camelo (ou Dromedário). 1 ponto por animal correto.",
                "options": [
                    {"id": "opt_moca_name_3", "label": "3 animais nomeados corretamente", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_name_2", "label": "2 animais nomeados", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_moca_name_1", "label": "1 animal nomeado", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_moca_name_0", "label": "0 animais nomeados", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_moca_attention",
                "name": "3. Atenção e Memória de Trabalho (0 a 6 pontos)",
                "slug": "atencao-memoria-trabalho",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_attention",
                "normalBaselineValue": 6,
                "maxAxisValue": 6,
                "sortOrder": 3,
                "helpText": "Dígitos ordem direta (1 pt) e ordem inversa (1 pt); Vigilância auditiva com palmas na letra 'A' (1 pt se <= 1 erro); Subtração seriada de 7 a partir de 100 (4-5 cálculos = 3 pts, 2-3 = 2 pts, 1 = 1 pt).",
                "options": [
                    {"id": "opt_moca_att_6", "label": "6 pontos (Dígitos direto/inverso, vigilância auditiva e cálculos perfeitos)", "pointValue": 6, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_att_5", "label": "5 pontos", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.17, "sortOrder": 2},
                    {"id": "opt_moca_att_4", "label": "4 pontos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3},
                    {"id": "opt_moca_att_3", "label": "3 pontos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.50, "sortOrder": 4},
                    {"id": "opt_moca_att_2", "label": "2 pontos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 5},
                    {"id": "opt_moca_att_1", "label": "1 ponto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.83, "sortOrder": 6},
                    {"id": "opt_moca_att_0", "label": "0 pontos (Inatenção e déficit severo de memória operacional)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 7}
                ]
            },
            {
                "id": "grp_moca_lang",
                "name": "4. Linguagem: Repetição e Fluência (0 a 3 pontos)",
                "slug": "linguagem-fluencia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_memory_lang",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 4,
                "helpText": "Repetição exata de 2 frases complexas (1 pt por frase correta); Fluência verbal fonêmica com letra 'F' (falar >= 11 palavras em 60 segundos = 1 pt).",
                "options": [
                    {"id": "opt_moca_lang_3", "label": "3 pontos (2 frases repetidas com perfeição + >= 11 palavras com 'F')", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_lang_2", "label": "2 pontos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2},
                    {"id": "opt_moca_lang_1", "label": "1 ponto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3},
                    {"id": "opt_moca_lang_0", "label": "0 pontos", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4}
                ]
            },
            {
                "id": "grp_moca_abstract",
                "name": "5. Abstração e Conceitualização (0 a 2 pontos)",
                "slug": "abstracao",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_executive",
                "normalBaselineValue": 2,
                "maxAxisValue": 2,
                "sortOrder": 5,
                "helpText": "Identificar a semelhança abstrata entre: Trem-Bicicleta (meios de transporte) e Relógio-Régua (instrumentos de medida). 1 ponto por par abstrato correto.",
                "options": [
                    {"id": "opt_moca_abs_2", "label": "2 pares abstratos conceituados corretamente", "pointValue": 2, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_abs_1", "label": "1 par abstrato correto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2},
                    {"id": "opt_moca_abs_0", "label": "0 acertos (Pensamento puramente concreto)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3}
                ]
            },
            {
                "id": "grp_moca_delayed_recall",
                "name": "6. Evocação Tardia sem Pistas (0 a 5 pontos)",
                "slug": "evocacao-tardia-moca",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_memory_lang",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 6,
                "helpText": "Recordação espontânea das 5 palavras aprendidas (Rosto, Veludo, Igreja, Margarida, Vermelho) após 5 minutos. 1 ponto por palavra evocada sem pistas.",
                "options": [
                    {"id": "opt_moca_rec_5", "label": "5 palavras evocadas espontaneamente", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_rec_4", "label": "4 palavras evocadas", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2},
                    {"id": "opt_moca_rec_3", "label": "3 palavras evocadas", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3},
                    {"id": "opt_moca_rec_2", "label": "2 palavras evocadas", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4},
                    {"id": "opt_moca_rec_1", "label": "1 palavra evocada", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5},
                    {"id": "opt_moca_rec_0", "label": "0 palavras evocadas (Amnésia de evocação típica hipocampal)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6}
                ]
            },
            {
                "id": "grp_moca_orient",
                "name": "7. Orientação (0 a 6 pontos)",
                "slug": "orientacao-moca",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_attention",
                "normalBaselineValue": 6,
                "maxAxisValue": 6,
                "sortOrder": 7,
                "helpText": "Pergunte a data exata, mês, ano, dia da semana, local atual e cidade. 1 ponto por acerto exato.",
                "options": [
                    {"id": "opt_moca_ori_6", "label": "6 acertos (Data, mês, ano, dia da semana, local e cidade corretos)", "pointValue": 6, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1},
                    {"id": "opt_moca_ori_5", "label": "5 acertos", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.17, "sortOrder": 2},
                    {"id": "opt_moca_ori_4", "label": "4 acertos", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3},
                    {"id": "opt_moca_ori_3", "label": "3 acertos", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.50, "sortOrder": 4},
                    {"id": "opt_moca_ori_2", "label": "2 acertos", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 5},
                    {"id": "opt_moca_ori_1", "label": "1 acerto", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.83, "sortOrder": 6},
                    {"id": "opt_moca_ori_0", "label": "0 acertos", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 7}
                ]
            },
            {
                "id": "grp_moca_edu_adj",
                "name": "8. Ajuste por Nível de Escolaridade",
                "slug": "ajuste-escolaridade",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_moca_memory_lang",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "helpText": "Adicione +1 ponto se o paciente possui 12 anos ou menos de escolaridade formal (ensino médio incompleto ou fundamental).",
                "options": [
                    {
                        "id": "opt_moca_edu_le12",
                        "label": "Escolaridade <= 12 anos (+1 ponto adicionado ao escore total)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Correção padronizada de Nasreddine para compensar desvantagem educacional."
                    },
                    {
                        "id": "opt_moca_edu_gt12",
                        "label": "Escolaridade > 12 anos de estudo (Ensino superior / sem acréscimo de ponto)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 2,
                        "description": "Nenhum ponto adicional."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_moca_dementia_severe",
                "label": "Demência Grave / Comprometimento Extremo (0 a 9 pontos)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 9,
                "statisticalOutcome": "Perda profunda de múltiplas funções cognitivas com dependência funcional acentuada nas AVDs básicas e instrumentais.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_moca_memantine_combo",
                        "drugName": "Associação de Inibidor da Acetilcolinesterase + Memantina",
                        "dosage": "Donepezila 10 mg/dia VO + Memantina 10 mg VO a cada 12 horas",
                        "route": "Oral",
                        "frequency": "Conforme posologia combinada",
                        "dilutionInstructions": "Donepezila à noite; Memantina 10 mg 12/12h às refeições.",
                        "renalAdjustment": "Ajustar Memantina para dose máxima de 10 mg/dia se ClCr < 30 mL/min.",
                        "contraindications": "Bradicardia sintomática grave, síncope de origem desconhecida."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_moca_safety",
                        "recommendationTitle": "Segurança Domiciliar, Supervisão 24h e Suporte Familiar",
                        "dispositionTarget": "Acompanhamento Domiciliar Estruturado / Centro de Convivência",
                        "monitoringPlan": "Vigilância ativa para risco de fuga, quedas, acidentes com fogão e abuso de medicações.",
                        "interventionalProcedure": "Adaptações estruturais no domicílio (trancas de segurança fora do campo de visão, iluminação noturna, barras de apoio no banheiro) e suporte psicológico aos cuidadores primários."
                    }
                ]
            },
            {
                "id": "tier_moca_dementia_mild_mod",
                "label": "Demência Leve a Moderada (10 a 17 pontos)",
                "severityLevel": "critical",
                "minScore": 10,
                "maxScore": 17,
                "statisticalOutcome": "Comprometimento objetivo significativo em múltiplos domínios cognitivos com declínio funcional documentado nas atividades cotidianas instrumentais.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    {
                        "id": "rx_moca_iache_init",
                        "drugName": "Inibidor da Acetilcolinesterase (IAChE)",
                        "dosage": "Donepezila 5 a 10 mg/dia VO ou Rivastigmina adesivo 4,6 a 9,5 mg/24h",
                        "route": "Oral / Transdérmica",
                        "frequency": "1x/dia",
                        "dilutionInstructions": "Titular dose a cada 4 semanas monitorando queixas digestivas e frequência cardíaca.",
                        "renalAdjustment": "Sem ajuste específico de dose.",
                        "contraindications": "Bloqueios atrioventriculares avançados sem marcapasso e úlcera gastroduodenal ativa."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_moca_neuropsych",
                        "recommendationTitle": "Avaliação Neuropsicológica e Intervenção de Terapia Ocupacional",
                        "dispositionTarget": "Ambulatório Especializado de Demências",
                        "monitoringPlan": "Avaliação funcional periódica das AVDs instrumentais (Escala de Lawton & Brody).",
                        "interventionalProcedure": "Terapia de estimulação cognitiva em grupo e adaptação de atividades de vida diária para manutenção da autonomia residual."
                    }
                ]
            },
            {
                "id": "tier_moca_mci",
                "label": "Comprometimento Cognitivo Leve - CCL / MCI (18 a 25 pontos)",
                "severityLevel": "intermediate",
                "minScore": 18,
                "maxScore": 25,
                "statisticalOutcome": "Declínio cognitivo objetivo documentado (especialmente memória episódica tardia e funções executivas), porém com preservação global da independência para as AVDs básicas. Taxa anual de conversão para demência de 10% a 15% ao ano.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_moca_ccl_rx",
                        "drugName": "Otimização Cardiovascular e Controle Metabólico Rígido",
                        "dosage": "Controle estrito de pressão arterial (alvo PAS 120-130 mmHg com IECA/BRA), Atorvastatina para meta de LDL < 70 mg/dL e controle glicêmico (HbA1c < 7%)",
                        "route": "Oral",
                        "frequency": "Individualizada",
                        "dilutionInstructions": "Fármacos direcionados para os fatores de risco vascular associados ao declínio cognitivo.",
                        "renalAdjustment": "Ajuste individualizado conforme fármaco."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_moca_mci_rehab",
                        "recommendationTitle": "Treinamento Cognitivo Estruturado e Modificação de Estilo de Vida",
                        "dispositionTarget": "Ambulatório de Neurologia Cognitiva e Preventiva",
                        "monitoringPlan": "Reavaliação neuropsicológica a cada 6 a 12 meses para detecção precoce de progressão para demência manifesta.",
                        "interventionalProcedure": "Exercícios aeróbicos regulares de moderada intensidade (mínimo 150 min/semana - comprovadamente promotores de neurogênese e BDNF hipocampal), engajamento cognitivo contínuo e adesão rigorosa à dieta MIND."
                    }
                ]
            },
            {
                "id": "tier_moca_normal",
                "label": "Função Cognitiva Normal (26 a 30 pontos)",
                "severityLevel": "low",
                "minScore": 26,
                "maxScore": 30,
                "statisticalOutcome": "Desempenho cognitivo dentro dos limites normais esperados (ponto de corte padrão >= 26 pontos com inclusão de +1 ponto se escolaridade <= 12 anos).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_moca_preservation",
                        "recommendationTitle": "Preservação da Saúde Cerebral e Reserva Cognitiva",
                        "dispositionTarget": "Atenção Primária / Prevenção de Saúde",
                        "monitoringPlan": "Acompanhamento clínico de rotina com checagem anual de fatores de risco vasculares e sono.",
                        "interventionalProcedure": "Incentivo a atividades culturais, convívio interpessoal, higiene do sono e atividade física regular."
                    }
                ]
            }
        ]
    }

def get_hoehn_yahr():
    return {
        "id": "calc_hoehn_yahr",
        "slug": "hoehn-yahr",
        "name": "Escala de Hoehn e Yahr Modificada",
        "acronym": "Hoehn & Yahr",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Distúrbios do Movimento e Parkinsonismo",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Distúrbios do Movimento e Parkinsonismo",
        "description": "Sistema de estadiamento ordinal de 8 estágios que mensura a progressão motora e o acometimento axial na Doença de Parkinson, identificando o marco prognóstico crítico da instabilidade postural.",
        "summary": "Estadiamento motor em 8 níveis na Doença de Parkinson, do acometimento unilateral à restrição ao leito.",
        "clinicalObjective": "Classificar a severidade motora da Doença de Parkinson, identificar a perda de reflexos posturais e selecionar pacientes para terapias avançadas como a Estimulação Cerebral Profunda (DBS).",
        "targetPopulation": "Pacientes com diagnóstico estabelecido de Doença de Parkinson idiopática.",
        "calculationType": "additive_points",
        "formulaExpression": "Estagio_Hoehn_Yahr_Selecionado",
        "evidenceSource": "Hoehn MM, Yahr MD. Parkinsonism: onset, progression and mortality. Neurology. 1967;17(5):427-442. Versão modificada pela Movement Disorder Society (MDS): Goetz CG, et al. Mov Disord. 2004;19(9):1020-1028.",
        "minPossibleScore": 0,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "parkinson",
        "clinicalWarning": "ATENÇÃO: A transição para o Estágio 3 é o DIVISOR DE ÁGUAS CLÍNICO na Doença de Parkinson, marcado pelo surgimento de INSTABILIDADE POSTURAL identificada através da manobra de retropulsão (Pull Test / teste do puxão). Se o paciente tomba em bloco para trás necessitando de amparo do examinador, é classificado obrigatoriamente no Estágio 3 (e não 2 ou 2.5), elevando exponencialmente o risco de quedas e fraturas.",
        "radarAxes": [
            {
                "id": "axis_hy_stage",
                "label": "Progressão Motora / H&Y",
                "system": "Motor",
                "unit": "estágio",
                "baselineValue": 0,
                "maxAxisValue": 5
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_hy_stage",
                "name": "Estágio Clínico Motor de Hoehn & Yahr",
                "slug": "estagio-hoehn-yahr",
                "inputType": "single_choice",
                "unit": "estágio",
                "radarAxisId": "axis_hy_stage",
                "normalBaselineValue": 0,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Selecione o estágio motor que reflete a extensão do acometimento clínico e o resultado do pull test.",
                "options": [
                    {
                        "id": "opt_hy_0",
                        "label": "Estágio 0: Sem sinais de doença",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Nenhum sinal motor ou alteração parkinsoniana detectável ao exame neurológico."
                    },
                    {
                        "id": "opt_hy_1",
                        "label": "Estágio 1: Doença estritamente unilateral",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.2,
                        "sortOrder": 2,
                        "description": "Sinais e sintomas estritamente em um hemicorpo (tremor de repouso, rigidez em roda denteada e bradicinesia unilateral); incapacidade funcional mínima ou ausente."
                    },
                    {
                        "id": "opt_hy_1_5",
                        "label": "Estágio 1.5: Envolvimento unilateral associado a acometimento axial",
                        "pointValue": 1.5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.3,
                        "sortOrder": 3,
                        "description": "Sinais motores predominantemente unilaterais, mas com evidência de acometimento axial precoce (rigidez de tronco ou pescoço, postura levemente fletida)."
                    },
                    {
                        "id": "opt_hy_2",
                        "label": "Estágio 2: Envolvimento bilateral sem perda do equilíbrio",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.4,
                        "sortOrder": 4,
                        "description": "Sinais e sintomas motores bilaterais evidentes, porém com reflexos posturais e equilíbrio rigorosamente preservados."
                    },
                    {
                        "id": "opt_hy_2_5",
                        "label": "Estágio 2.5: Doença bilateral leve com recuperação no pull test",
                        "pointValue": 2.5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 5,
                        "description": "Envolvimento bilateral com preservação do equilíbrio; à manobra de retropulsão (pull test), o paciente recupera o equilíbrio com 1 ou 2 passos rápidos para trás sem cair."
                    },
                    {
                        "id": "opt_hy_3",
                        "label": "Estágio 3: Comprometimento bilateral com instabilidade postural (Pull Test anormal)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.6,
                        "sortOrder": 6,
                        "description": "Perda de reflexos posturais (falha na manobra de retropulsão / tomba para trás no pull test); incapacidade motora leve a moderada, mas fisicamente autossuficiente para AVDs básicas."
                    },
                    {
                        "id": "opt_hy_4",
                        "label": "Estágio 4: Incapacidade motora grave (Caminha sem ajuda, mas muito dependente)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.8,
                        "sortOrder": 7,
                        "description": "Incapacidade grave; ainda capaz de deambular ou ficar de pé sem assistência humana/mecânica, mas amplamente incapacitado e necessitando de auxílio para a maioria das tarefas."
                    },
                    {
                        "id": "opt_hy_5",
                        "label": "Estágio 5: Confinado à cadeira de rodas ou ao leito",
                        "pointValue": 5,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 8,
                        "description": "Restrito ao leito ou à cadeira de rodas, a menos que auxiliado por outra pessoa para todas as transferências e cuidados de suporte."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_hy_early",
                "label": "Doença de Parkinson Inicial / Pré-Axial (Estágios 0 a 2.5)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2.5,
                "statisticalOutcome": "Preservação da estabilidade postural e dos reflexos de proteção. Baixo risco de quedas traumáticas imediatas. Excelente resposta à terapia dopaminérgica de reposição.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hy_ldopa",
                        "drugName": "Levodopa + Benserazida (ou Carbidopa) 100/25 mg",
                        "dosage": "Iniciar com 1/2 comprimido VO 3x/dia após as refeições, titulando a cada 1-2 semanas para 1 comprimido VO 3x/dia (dose-alvo inicial de 300 mg/dia de Levodopa)",
                        "route": "Oral",
                        "frequency": "8/8h",
                        "dilutionInstructions": "Administrar 30 a 60 minutos antes ou 2 horas após refeições ricas em proteínas para evitar competição de absorção com aminoácidos neutros.",
                        "renalAdjustment": "Não requer ajuste formal de dose na insuficiência renal.",
                        "contraindications": "Glaucoma de ângulo fechado não controlado, uso concomitante de IMAO não seletivos e histórico de melanoma maligno ativo."
                    },
                    {
                        "id": "rx_hy_pramipexole",
                        "drugName": "Pramipexol (Agonista Dopaminérgico - Pacientes Jovens < 60 anos)",
                        "dosage": "Iniciar com 0,125 mg VO 3x/dia, escalonando semanalmente até 0,5 a 1,5 mg VO 3x/dia (1,5 a 4,5 mg/dia)",
                        "route": "Oral",
                        "frequency": "8/8h",
                        "dilutionInstructions": "Comprimidos de liberação imediata ou liberação prolongada 1x/dia.",
                        "renalAdjustment": "Eliminação renal mandatória: se ClCr entre 30 e 50 mL/min, dose inicial 0,125 mg 12/12h; se ClCr < 30 mL/min, dose máxima 1,5 mg/dia em tomada única.",
                        "contraindications": "Transtorno de controle de impulsos prévio (jogo patológico, hipersexualidade, compras compulsivas) e sonolência diurna excessiva."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hy_physio_early",
                        "recommendationTitle": "Fisioterapia Motora Preventiva e Exercício Aeróbico de Alta Intensidade",
                        "dispositionTarget": "Ambulatório de Distúrbios do Movimento / Fisioterapia",
                        "monitoringPlan": "Retornos semestrais com aplicação seriada da escala UPDRS Parte III (motora) em estados ON e OFF.",
                        "interventionalProcedure": "Engajamento em exercícios aeróbicos moderados a intensos (esteira, natação, ciclismo, dança) por pelo menos 150 a 180 minutos semanais para estímulo de neuroplasticidade estriatal."
                    }
                ]
            },
            {
                "id": "tier_hy_mod",
                "label": "Doença Moderada com Instabilidade Postural (Estágio 3)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "O DIVISOR DE ÁGUAS CLÍNICO. Perda comprovada dos reflexos posturais protetores. Risco exponencial de quedas recorrentes e fraturas de fêmur. Perda progressiva da independência comunitária.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hy_entacapone",
                        "drugName": "Entacapona (Inibidor Periférico da COMT)",
                        "dosage": "200 mg VO administrado concomitantemente a cada dose de Levodopa (máximo de 1600 a 2000 mg/dia)",
                        "route": "Oral",
                        "frequency": "Com cada dose de Levodopa",
                        "dilutionInstructions": "Tomar junto com o comprimido de levodopa para prolongar a meia-vida plasmática e reduzir flutuações motoras (wearing-off).",
                        "renalAdjustment": "Não requer ajuste de dose para função renal.",
                        "contraindications": "Histórico prévio de Síndrome Neuroléptica Maligna ou rabdomiólise não traumática."
                    },
                    {
                        "id": "rx_hy_amantadine",
                        "drugName": "Amantadina (Controle de Discinesias de Pico de Dose)",
                        "dosage": "100 mg VO 1x/dia pela manhã, podendo aumentar para 100 mg VO 2x/dia (manhã e almoço)",
                        "route": "Oral",
                        "frequency": "12/12h (evitar à noite)",
                        "dilutionInstructions": "Evitar administração no período noturno devido ao risco de insônia vívida e pesadelos.",
                        "renalAdjustment": "Excreção estritamente renal: se ClCr < 50 mL/min, reduzir dose para 100 mg/dia; se ClCr < 15 mL/min, 100 mg a cada 72 horas.",
                        "contraindications": "Insuficiência cardíaca congestiva descompensada e glaucoma de ângulo fechado; monitorar livedo reticular e edema de tornozelo."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hy_dbs_eval",
                        "recommendationTitle": "Avaliação de Elegibilidade para Estimulação Cerebral Profunda (DBS) e Treino de Quedas",
                        "dispositionTarget": "Centro Terciário de Cirurgia de Distúrbios do Movimento",
                        "monitoringPlan": "Teste formal de desafio com levodopa (Levodopa Challenge Test) para quantificar melhora motora percentual (> 33% na UPDRS motora necessária para indicação de DBS).",
                        "interventionalProcedure": "Avaliação neurocirúrgica e neuropsicológica formal para implante de eletrodos de DBS no Núcleo Subtalâmico (STN) ou Globo Pálido Interno (GPi); fisioterapia voltada para estratégias de pista visual/auditiva para congelamento de marcha (freezing)."
                    }
                ]
            },
            {
                "id": "tier_hy_advanced",
                "label": "Doença de Parkinson Avançada / Fase de Dependência (Estágios 4 a 5)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Dependência física severa para deambulação e transferências. Elevada morbimortalidade por complicações secundárias (pneumonia por broncoaspiração, desnutrição e úlceras por pressão). Alta prevalência de demência associada à Doença de Parkinson e psicose dopaminérgica.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_hy_quetiapine",
                        "drugName": "Quetiapina (Manejo de Sintomas Psicóticos e Alucinações)",
                        "dosage": "Iniciar com 12,5 a 25 mg VO à noite, podendo titular até 50 a 100 mg VO à noite",
                        "route": "Oral",
                        "frequency": "1x/dia à noite",
                        "dilutionInstructions": "Droga de escolha para alucinações visuais e delírios associados à terapia dopaminérgica sem piorar o parkinsonismo motor.",
                        "renalAdjustment": "Não requer ajuste na insuficiência renal.",
                        "contraindications": "PROIBIÇÃO ABSOLUTA DE ANTIPSICÓTICOS TÍPICOS (Haloperidol, Clorpromazina) E METOCLOPRAMIDA: bloqueiam receptores D2 estriatais induzindo crise acinética maligna irreversível e rigidez extrema."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_hy_comfort_dysphagia",
                        "recommendationTitle": "Gerenciamento de Disfagia, Prevenção de Broncoaspiração e Suporte ao Leito",
                        "dispositionTarget": "Home Care / Unidade de Cuidados Prolongados",
                        "monitoringPlan": "Avaliação fonoaudiológica seriada para detecção de aspiração silente.",
                        "interventionalProcedure": "Espessamento de líquidos, adaptação para dieta pastosa, fornecimento de cadeira de rodas ergonômica com suporte postural e treinamento dos cuidadores para prevenção de úlceras por pressão."
                    }
                ]
            }
        ]
    }

def get_edss():
    return {
        "id": "calc_edss",
        "slug": "edss",
        "name": "Escala Expandida do Estado de Incapacidade de Kurtzke",
        "acronym": "EDSS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Doenças Desmielinizantes e Neuroimunologia",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Doenças Desmielinizantes e Neuroimunologia",
        "description": "Escala ordinal padronizada de 0,0 a 10,0 pontos em incrementos de 0,5 que quantifica o acúmulo de incapacidade neurológica na Esclerose Múltipla a partir da avaliação dos 7 Sistemas Funcionais e da distância métrica de marcha.",
        "summary": "Escala universal de progressão de incapacidade (0,0 a 10,0) na Esclerose Múltipla.",
        "clinicalObjective": "Mensurar o acúmulo longitudinal de incapacidade, definir progressão confirmada de incapacidade (CDP), guiar a escalada para Terapias Modificadoras da Doença (DMTs) de alta eficácia e avaliar critérios NEDA.",
        "targetPopulation": "Pacientes com diagnóstico confirmado de Esclerose Múltipla (fenótipos EMRR, EMSP ou EMPP) avaliados fora da fase aguda de surto.",
        "calculationType": "additive_points",
        "formulaExpression": "Nivel_EDSS_Selecionado (0.0 a 10.0)",
        "evidenceSource": "Kurtzke JF. Rating neurologic impairment in multiple sclerosis: an expanded disability status scale (EDSS). Neurology. 1983;33(11):1444-1452.",
        "minPossibleScore": 0.0,
        "maxPossibleScore": 10.0,
        "baseScore": 0.0,
        "badge": "desmielinizante",
        "clinicalWarning": "ATENÇÃO: A escala sofre uma DESCONTINUIDADE ESTRUTURAL NO EDSS 4,0. De 0,0 a 3,5, o escore é governado estritamente pelas pontuações dos 7 Sistemas Funcionais (Piramidal, Cerebelar, Tronco, Sensitivo, Esfincteriano, Visual e Mental). A PARTIR DE 4,0, A ESCALA PASSA A SER DETERMINADA QUASE EXCLUSIVAMENTE PELA DISTÂNCIA MÉTRICA EXATA DE DEAMBULAÇÃO SEM APOIO (medida no corredor e não autorrelatada) e pela necessidade de órtese unilateral (6,0) ou bilateral (6,5).",
        "radarAxes": [
            {
                "id": "axis_edss_disability",
                "label": "Incapacidade Global / EDSS",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0.0,
                "maxAxisValue": 10.0
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_edss_level",
                "name": "Degrau Clínico de Incapacidade EDSS (Kurtzke)",
                "slug": "degrau-edss",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_edss_disability",
                "normalBaselineValue": 0.0,
                "maxAxisValue": 10.0,
                "sortOrder": 1,
                "helpText": "Selecione o degrau exato de incapacidade e deambulação aferido.",
                "options": [
                    {"id": "opt_edss_0_0", "label": "0,0: Exame neurológico rigorosamente normal", "pointValue": 0.0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Todos os sistemas funcionais normais (grau 0 em todos os SF)."},
                    {"id": "opt_edss_1_0", "label": "1,0: Sem incapacidade; sinais mínimos em 1 SF", "pointValue": 1.0, "isNormalBaseline": False, "radarNormalizedValue": 0.10, "sortOrder": 2, "description": "Sinais mínimos em 1 Sistema Funcional (grau 1 em 1 SF; outros grau 0)."},
                    {"id": "opt_edss_1_5", "label": "1,5: Sem incapacidade; sinais mínimos em mais de 1 SF", "pointValue": 1.5, "isNormalBaseline": False, "radarNormalizedValue": 0.15, "sortOrder": 3, "description": "Sinais mínimos em mais de um Sistema Funcional (grau 1 em >1 SF)."},
                    {"id": "opt_edss_2_0", "label": "2,0: Incapacidade mínima em 1 SF", "pointValue": 2.0, "isNormalBaseline": False, "radarNormalizedValue": 0.20, "sortOrder": 4, "description": "Incapacidade mínima em 1 SF (grau 2 em 1 SF; outros grau 0 ou 1)."},
                    {"id": "opt_edss_2_5", "label": "2,5: Incapacidade mínima em 2 SF", "pointValue": 2.5, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 5, "description": "Incapacidade mínima em 2 SF (grau 2 em 2 SF; outros grau 0 ou 1)."},
                    {"id": "opt_edss_3_0", "label": "3,0: Incapacidade moderada em 1 SF; totalmente ambulatorial", "pointValue": 3.0, "isNormalBaseline": False, "radarNormalizedValue": 0.30, "sortOrder": 6, "description": "Incapacidade moderada em 1 SF (grau 3 em 1 SF) ou grau 2 em 3-4 SF; deambulação livre e normal."},
                    {"id": "opt_edss_3_5", "label": "3,5: Totalmente ambulatorial com limitação moderada em múltiplos SF", "pointValue": 3.5, "isNormalBaseline": False, "radarNormalizedValue": 0.35, "sortOrder": 7, "description": "Totalmente ambulatorial, mas com incapacidade moderada em 1 SF (grau 3) e grau 2 em 1-2 SF."},
                    {"id": "opt_edss_4_0", "label": "4,0: Deambula sem auxílio >= 500 metros", "pointValue": 4.0, "isNormalBaseline": False, "radarNormalizedValue": 0.40, "sortOrder": 8, "description": "Autossuficiente, deambula sem auxílio ou repouso por pelo menos 500 metros. Incapacidade relativamente grave em 1 SF (grau 4)."},
                    {"id": "opt_edss_4_5", "label": "4,5: Deambula sem auxílio >= 300 metros", "pointValue": 4.5, "isNormalBaseline": False, "radarNormalizedValue": 0.45, "sortOrder": 9, "description": "Deambula sem auxílio ou descanso por pelo menos 300 metros; autossuficiente a maior parte do dia."},
                    {"id": "opt_edss_5_0", "label": "5,0: Deambula sem auxílio cerca de 200 metros", "pointValue": 5.0, "isNormalBaseline": False, "radarNormalizedValue": 0.50, "sortOrder": 10, "description": "Deambula sem assistência por cerca de 200 metros; incapacidade restringe atividade diária completa."},
                    {"id": "opt_edss_5_5", "label": "5,5: Deambula sem auxílio cerca de 100 metros", "pointValue": 5.5, "isNormalBaseline": False, "radarNormalizedValue": 0.55, "sortOrder": 11, "description": "Deambula sem auxílio ou repouso por cerca de 100 metros; incapaz de manter trabalho em tempo integral."},
                    {"id": "opt_edss_6_0", "label": "6,0: Necessita de auxílio unilateral intermitente ou constante (Bengala)", "pointValue": 6.0, "isNormalBaseline": False, "radarNormalizedValue": 0.60, "sortOrder": 12, "description": "Necessita de assistência unilateral constante ou intermitente (bengala, muleta canadense) para caminhar cerca de 100 metros com ou sem descanso."},
                    {"id": "opt_edss_6_5", "label": "6,5: Necessita de auxílio bilateral constante (Duas bengalas / Andador)", "pointValue": 6.5, "isNormalBaseline": False, "radarNormalizedValue": 0.65, "sortOrder": 13, "description": "Necessita de assistência bilateral constante (duas bengalas, muletas ou andador) para caminhar cerca de 20 metros sem parar."},
                    {"id": "opt_edss_7_0", "label": "7,0: Incapaz de caminhar mais de 5 metros; restrito à cadeira de rodas", "pointValue": 7.0, "isNormalBaseline": False, "radarNormalizedValue": 0.70, "sortOrder": 14, "description": "Incapaz de caminhar mais de 5 metros mesmo com auxílio; restrito à cadeira de rodas, mas propulsiona a cadeira e realiza transferências sozinho."},
                    {"id": "opt_edss_7_5", "label": "7,5: Incapaz de dar mais de alguns passos; requer ajuda para transferências", "pointValue": 7.5, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 15, "description": "Restrito à cadeira de rodas; incapaz de propulsionar a cadeira de rodas por todo o dia; necessita de assistência de terceiros para transferências."},
                    {"id": "opt_edss_8_0", "label": "8,0: Restrito ao leito ou cadeira de rodas a maior parte do dia", "pointValue": 8.0, "isNormalBaseline": False, "radarNormalizedValue": 0.80, "sortOrder": 16, "description": "Essencialmente confinado ao leito ou cadeira de rodas empurrada por terceiros; retém a maior parte das funções de autocuidado dos braços."},
                    {"id": "opt_edss_8_5", "label": "8,5: Restrito ao leito a maior parte do dia; perdeu uso funcional dos braços", "pointValue": 8.5, "isNormalBaseline": False, "radarNormalizedValue": 0.85, "sortOrder": 17, "description": "Confinado ao leito a maior parte do dia; perdeu a maior parte do uso funcional dos braços; retém algumas funções elementares de autocuidado."},
                    {"id": "opt_edss_9_0", "label": "9,0: Paciente acamado desamparado", "pointValue": 9.0, "isNormalBaseline": False, "radarNormalizedValue": 0.90, "sortOrder": 18, "description": "Totalmente acamado; capaz de comunicar-se e alimentar-se com dificuldade."},
                    {"id": "opt_edss_9_5", "label": "9,5: Paciente totalmente acamado, mudo e com disfagia grave", "pointValue": 9.5, "isNormalBaseline": False, "radarNormalizedValue": 0.95, "sortOrder": 19, "description": "Totalmente acamado e indefeso; incapaz de comunicar-se ou engolir de forma eficaz."},
                    {"id": "opt_edss_10_0", "label": "10,0: Óbito decorrente de complicações diretas da Esclerose Múltipla", "pointValue": 10.0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 20, "description": "Morte devida à progressão da doença ou complicações respiratórias/infecciosas associadas."}
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_edss_ambulatory",
                "label": "Deambulação Livre / Incapacidade Leve a Moderada (EDSS 0,0 a 4,5)",
                "severityLevel": "low",
                "minScore": 0.0,
                "maxScore": 4.5,
                "statisticalOutcome": "Marcha autônoma preservada sem necessidade de apoio ou órtese. Janela de oportunidade terapêutica crítica para controle precoce da inflamação do SNC e prevenção do acúmulo irreversível de lesões axonais.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edss_methylpred",
                        "drugName": "Metilprednisolona (Pulsoterapia para Tratamento de Surto Agudo)",
                        "dosage": "1.000 mg/dia IV diluída em 250 mL de SF 0,9% infundida ao longo de 2 horas por 3 a 5 dias consecutivos",
                        "route": "Intravenosa",
                        "frequency": "1x/dia por 3-5 dias",
                        "dilutionInstructions": "Infundir em 2 horas; associar proteção gástrica com Pantoprazol 40 mg IV/dia.",
                        "renalAdjustment": "Não requer ajuste de dose para insuficiência renal.",
                        "contraindications": "Infecção fúngica sistêmica ativa e bacteremia não controlada; monitorar glicemia e hipertensão."
                    },
                    {
                        "id": "rx_edss_dmt_high_efficacy",
                        "drugName": "Terapias Modificadoras da Doença (DMTs) de Alta Eficácia",
                        "dosage": "Ocrelizumabe 300 mg IV nos Dias 1 e 15, seguido de 600 mg IV a cada 6 meses; OU Natalizumabe 300 mg IV a cada 4 semanas (se anti-JCV negativo); OU Fingolimode 0,5 mg/dia VO",
                        "route": "Intravenosa / Oral",
                        "frequency": "Conforme protocolo da DMT",
                        "dilutionInstructions": "Ocrelizumabe em SF 0,9% com pré-medicação (Metilprednisolona 100 mg IV + Anti-histamínico).",
                        "renalAdjustment": "Avaliar função hepática e renal antes da prescrição.",
                        "contraindications": "Infecção por vírus JC com alto título de anticorpos (risco de Leucoencefalopatia Multifocal Progressiva - LMP) contraindica Natalizumabe."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_edss_neda",
                        "recommendationTitle": "Monitoramento com Protocolo NEDA (No Evidence of Disease Activity) e RM Seriada",
                        "dispositionTarget": "Centro Especializado de Esclerose Múltipla",
                        "monitoringPlan": "Ressonância magnética de crânio e coluna cervical com contraste a cada 6 a 12 meses para avaliar critérios NEDA-3 (ausência de surtos clínicos, ausência de novas lesões em T2/lesões contrastadas e ausência de progressão de incapacidade confirmada no EDSS).",
                        "interventionalProcedure": "Programa estruturado de fisioterapia neurofuncional, exercícios aeróbicos regulares, e orientações rigorosas para evitar aumento excessivo de temperatura corporal (prevenção do Fenômeno de Uhthoff)."
                    }
                ]
            },
            {
                "id": "tier_edss_gait_aid",
                "label": "Dependência de Suporte para Marcha (EDSS 5,0 a 6,5)",
                "severityLevel": "intermediate",
                "minScore": 5.0,
                "maxScore": 6.5,
                "statisticalOutcome": "Restrição progressiva da distância de marcha e necessidade de apoio unilateral (bengala no 6,0) ou bilateral (andador no 6,5). Frequente transição para fase Secundariamente Progressiva (EMSP), onde predomina neurodegeneração.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edss_baclofen",
                        "drugName": "Baclofeno (Manejo de Espasticidade Espinhal Severa)",
                        "dosage": "Iniciar com 10 mg VO a cada 8 horas, titulando semanalmente até 60 a 80 mg/dia divididos em 3 a 4 tomadas",
                        "route": "Oral",
                        "frequency": "8/8h",
                        "dilutionInstructions": "Comprimidos via oral; evitar retirada abrupta sob risco de hipertermia e convulsões.",
                        "renalAdjustment": "Eliminação renal; reduzir dose se ClCr < 50 mL/min.",
                        "contraindications": "Hipersensibilidade ao baclofeno; monitorar sedação excessiva que comprometa a marcha."
                    },
                    {
                        "id": "rx_edss_fatigue",
                        "drugName": "Amantadina (Tratamento Sintomático da Fadiga Central)",
                        "dosage": "100 mg VO duas vezes ao dia (ao café da manhã e ao almoço)",
                        "route": "Oral",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Administrar até o almoço para prevenir insônia noturna.",
                        "renalAdjustment": "Reduzir dose se insuficiência renal (excreção estritamente renal).",
                        "contraindications": "Insuficiência cardíaca descompensada e glaucoma não tratado."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_edss_gait_training",
                        "recommendationTitle": "Prescrição de Órteses, Treino Postural de Marcha e Fisioterapia",
                        "dispositionTarget": "Centro de Reabilitação Física",
                        "monitoringPlan": "Avaliação semestral de risco de quedas e adequação de dispositivos de assistência à locomoção.",
                        "interventionalProcedure": "Prescrição de bengalas canadenses, andadores com rodas e freios, órteses tornozelo-pé (AFO) para pé caído e fisioterapia neurofuncional diária."
                    }
                ]
            },
            {
                "id": "tier_edss_wheelchair_bed",
                "label": "Restrição à Cadeira de Rodas ou Leito (EDSS 7,0 a 9,5)",
                "severityLevel": "critical",
                "minScore": 7.0,
                "maxScore": 9.5,
                "statisticalOutcome": "Perda da marcha comunitária e domiciliar. Alta incidência de complicações infecciosas (sepse de foco urinário ou pulmonar), úlceras por pressão e atrofia muscular por desuso.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edss_bladder",
                        "drugName": "Oxibutinina (Controle de Hiperatividade Detrusora Neurogênica)",
                        "dosage": "5 mg VO duas a três vezes ao dia (ou Toxina Botulínica intravesical 100 a 200 UI)",
                        "route": "Oral",
                        "frequency": "8/8h ou 12/12h",
                        "dilutionInstructions": "Comprimidos via oral; monitorar resíduo pós-miccional para evitar retenção urinária bacteriana.",
                        "renalAdjustment": "Usar com precaução na insuficiência renal e hepática.",
                        "contraindications": "Glaucoma de ângulo fechado não controlado e obstrução gastrointestinal mecânica."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_edss_icp",
                        "recommendationTitle": "Programa de Cateterismo Vesical Intermitente Limpo (CVI) e Prevenção de Escaras",
                        "dispositionTarget": "Cuidados Domiciliares Especializados / Home Care",
                        "monitoringPlan": "Urocultura seriada e vigilância tegumentar em proeminências ósseas.",
                        "interventionalProcedure": "Treinamento do paciente e cuidadores para Cateterismo Vesical Intermitente Limpo (CVI) a cada 4 a 6 horas; colchão pneumático articulado com pressão alternada; cadeira de rodas motorizada ou adaptada."
                    }
                ]
            },
            {
                "id": "tier_edss_death",
                "label": "Óbito por Complicações da Esclerose Múltipla (EDSS 10,0)",
                "severityLevel": "critical",
                "minScore": 10.0,
                "maxScore": 10.0,
                "statisticalOutcome": "Óbito decorrente de complicações diretas ou indiretas da doença desmielinizante avançada (sepse respiratória ou urinária).",
                "colorHex": "#1f2937",
                "pharmacologicalActions": [],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_edss_death_protocol",
                        "recommendationTitle": "Acolhimento Familiar e Registro de Óbito",
                        "dispositionTarget": "Protocolo Administrativo de Óbito",
                        "monitoringPlan": "Preenchimento correto da cadeia causal do óbito.",
                        "interventionalProcedure": "Apoio e acolhimento multiprofissional aos familiares enlutados."
                    }
                ]
            }
        ]
    }
