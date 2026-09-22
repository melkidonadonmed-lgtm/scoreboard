"""
Block 03: Module C - Cirurgia de Coluna & Medula
1. TLICS (Thoracolumbar Injury Classification and Severity Score, 1-10 pts)
2. SLICS (Subaxial Cervical Spine Injury Classification, 0-10 pts)
3. Anderson-D'Alonzo (C2 Odontoid Fractures, Types I-III & Grauer)
4. SINS (Spine Instability Neoplastic Score, 0-18 pts)
5. NOMS Framework & Bilsky Scale (Spinal Oncology Decision Matrix)
6. Balanço Sagital e Parâmetros Espinopélvicos (SRS-Schwab)
7. mJOA & Nurick (Cervical Spondylotic Myelopathy & Benzel Diamond)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL


def get_tlics():
    """Thoracolumbar Injury Classification and Severity Score (Vaccaro et al. 2005)."""
    return {
        "id": "calc_tlics",
        "slug": "tlics",
        "name": "Escore TLICS para Trauma da Coluna Toracolombar",
        "acronym": "TLICS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Sistema de classificação baseado em evidências para traumatismo toracolombar (T1 a L5) que avalia morfologia da fratura, integridade do complexo ligamentar posterior (CLP) e estado neurológico, definindo a indicação cirúrgica objetiva.",
        "summary": "Classificação biomecânica e neurológica do trauma toracolombar (corte cirúrgico >= 5 pontos).",
        "clinicalObjective": "Estratificar a estabilidade mecânica e neurológica das fraturas toracolombares para direcionar conduta conservadora (<= 3), limítrofe (4) ou cirúrgica mandatória (>= 5).",
        "targetPopulation": "Pacientes com fratura traumática aguda da coluna toracolombar (T1 a L5).",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Morfologia + Pontos_CLP + Pontos_Neurologico",
        "evidenceSource": "Vaccaro AR, Lehman RA Jr, Hurlbert RJ, et al. A new classification of thoracolumbar injuries: the importance of injury morphology, the integrity of the posterior ligamentous complex, and neurologic status. Spine. 2005;30(20):2325-2333.",
        "minPossibleScore": 1,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "ATENÇÃO BIOMECÂNICA: A lesão medular incompleta pontua 3 pontos (mais do que a completa, que pontua 2), pois há parênquima medular viável em risco de isquemia irreversível, exigindo descompressão cirúrgica de urgência em < 8 a 24 horas. Em casos de escore 4 pontos (zona limítrofe), avaliar cifose focal > 20-30° e perda de altura > 50%.",
        "radarAxes": [
            {"id": "axis_tlics_morph", "label": "Morfologia da Fratura", "system": "Mecânico", "unit": "pts", "baselineValue": 1, "maxAxisValue": 4},
            {"id": "axis_tlics_plc", "label": "Complexo Ligamentar Posterior", "system": "Biomecânico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_tlics_neuro", "label": "Comprometimento Neurológico", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
        ],
        "parameterGroups": [
            {
                "id": "grp_tlics_morphology",
                "name": "1. Morfologia da Fratura",
                "slug": "morfologia-tlics",
                "inputType": "single_choice",
                "radarAxisId": "axis_tlics_morph",
                "normalBaselineValue": 1,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "helpText": "Padrão biomecânico principal de deformação da coluna vertebral na TC/radiografia.",
                "options": [
                    {"id": "opt_tlics_morph_comp", "label": "Fratura por Compressão Simples em Cunha (1 pt)", "pointValue": 1, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Fratura do platô vertebral anterior sem acometimento da parede posterior."},
                    {"id": "opt_tlics_morph_burst", "label": "Fratura em Explosão / Burst (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Cominuição da coluna anterior e média com fragmento ósseo retropulsado no canal vertebral."},
                    {"id": "opt_tlics_morph_trans", "label": "Fratura Translacional ou Rotacional (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3, "description": "Deslocamento horizontal de uma vértebra sobre a outra ou desalinhamento facetário."},
                    {"id": "opt_tlics_morph_distr", "label": "Fratura por Distração / Lesão tipo Chance (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Falência por tração/abertura dos elementos posteriores e/ou anteriores (ex.: cinto de segurança)."},
                ],
            },
            {
                "id": "grp_tlics_plc",
                "name": "2. Integridade do Complexo Ligamentar Posterior (CLP)",
                "slug": "clp-tlics",
                "inputType": "single_choice",
                "radarAxisId": "axis_tlics_plc",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Ligamento supraespinhoso, interespinhoso, ligamento amarelo e cápsulas facetárias.",
                "options": [
                    {"id": "opt_tlics_plc_intact", "label": "Íntegro (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem diástase de processos espinhosos nem edema no plano ligamentar posterior na RM."},
                    {"id": "opt_tlics_plc_suspect", "label": "Suspeito / Indeterminado (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 2, "description": "Hipersinal T2/STIR no ligamento interespinhal sem ruptura ligamentar mecânica franca visível."},
                    {"id": "opt_tlics_plc_disrupt", "label": "Rompido / Desestruturado (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Gap palpável ou radiográfico interespinhal, diástase facetária bilateral ou avulsão óssea."},
                ],
            },
            {
                "id": "grp_tlics_neuro",
                "name": "3. Estado Neurológico",
                "slug": "neurologico-tlics",
                "inputType": "single_choice",
                "radarAxisId": "axis_tlics_neuro",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 3,
                "helpText": "Avaliação motora, sensitiva e esfincteriana distal ao nível da fratura.",
                "options": [
                    {"id": "opt_tlics_neuro_intact", "label": "Neurologicamente Intacto (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Força, sensibilidade e reflexos completamente normais."},
                    {"id": "opt_tlics_neuro_root", "label": "Lesão de Raiz Nervosa Isolada (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Radiculopatia motora ou sensitiva focal unilateral."},
                    {"id": "opt_tlics_neuro_complete", "label": "Lesão Medular Completa - ASIA A (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 3, "description": "Plegia e anestesia completas abaixo do nível motor/sensitivo com ausência de função sacral."},
                    {"id": "opt_tlics_neuro_incomplete", "label": "Lesão Medular Incompleta - ASIA B, C ou D (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Preservação parcial motora ou sensitiva (parênquima viável em risco crítico de necrose isquêmica)."},
                    {"id": "opt_tlics_neuro_cauda", "label": "Síndrome da Cauda Equina (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5, "description": "Anestesia em sela com perda de controle esfincteriano vesical e retal."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_tlics_cons",
                "label": "Tratamento Conservador Seguro (1 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 3,
                "statisticalOutcome": "Coluna mecanicamente estável com CLP preservado e sem déficit neurológico. Alta probabilidade de consolidação óssea com órtese.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_tlics_analgesia",
                        "drugName": "Analgesia Otimizada Multimodal",
                        "dosage": "Dipirona 1g VO 6/6h + Cetoprofeno 100mg VO 12/12h por 5 a 7 dias",
                        "route": "Oral",
                        "frequency": "6/6h e 12/12h",
                        "dilutionInstructions": "Evitar AINE prolongado em idosos ou nefropatas.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_tlics_cons",
                        "recommendationTitle": "Tratamento Conservador Seguro com Órtese Toracolombar",
                        "dispositionTarget": "Enfermaria / Ambulatório",
                        "monitoringPlan": "Imobilização com colete rígido (TLSO bivalve ou órtese de Jewett) por 8 a 12 semanas. Radiografias de controle em perfil com carga em 2, 4 e 8 semanas.",
                        "interventionalProcedure": "Cirurgia não indicada.",
                    }
                ],
            },
            {
                "id": "tier_tlics_lim",
                "label": "Zona Limítrofe / Critério do Cirurgião (4 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Instabilidade mecânica relativa. Decisão individualizada baseada no perfil biomecânico e clínico.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_tlics_pain_mod",
                        "drugName": "Analgesia Escalonada com Opióides Fracos",
                        "dosage": "Tramadol 50 mg VO 8/8h se dor refratária",
                        "route": "Oral",
                        "frequency": "8/8h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_tlics_lim",
                        "recommendationTitle": "Caso Limítrofe / Individualização Cirúrgica vs Conservadora",
                        "dispositionTarget": "Enfermaria Ortopédica / Neurocirúrgica",
                        "monitoringPlan": "Se paciente jovem e ativo com perda de altura vertebral > 50% ou cifose focal > 20-30°: indicar artrodese posterior curta instrumentada para rápida desospitalização e prevenção de cifose tardia; se paciente idoso ou com alto risco anestésico, adotar colete TLSO e TC seriada.",
                        "interventionalProcedure": "Cirurgia eletiva planejada ou órtese sob controle rígido.",
                    }
                ],
            },
            {
                "id": "tier_tlics_surg",
                "label": "Indicação Cirúrgica Mandatória (5 a 10 pontos)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 10,
                "statisticalOutcome": "Instabilidade mecânica grave com falência ligamentar ou déficit neurológico progressivo. Alto risco de colapso vertebral e paraplegia sob manejo conservador.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_tlics_cefazolin",
                        "drugName": "Cefazolina Profilática Perioperatória",
                        "dosage": "2g IV na indução anestésica (3g se peso > 120 kg)",
                        "route": "Intravenosa",
                        "frequency": "Dose única na indução + repetição a cada 4 horas de cirurgia",
                        "dilutionInstructions": "100 mL SF 0,9% em 20 minutos.",
                    },
                    {
                        "id": "rx_tlics_pregabalin",
                        "drugName": "Pregabalina para Dor Neuropática / Radiculopatia",
                        "dosage": "75 mg VO 12/12h",
                        "route": "Oral",
                        "frequency": "12/12h",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_tlics_surg",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: Descompressão e Artrodese Posterior Instrumentada",
                        "dispositionTarget": "Centro Cirúrgico de Emergência",
                        "monitoringPlan": "Monitorização neurofisiológica intraoperatória de potenciais evocados motores (PEM) e somatossensoriais (PESS).",
                        "interventionalProcedure": "Laminectomia descompressiva ampla de urgência em < 8 a 24 horas se déficit incompleto ou cauda equina + Redução anatômica e Artrodese Posterior Instrumentada com Parafusos Pediculares (construção curta de 1 acima e 1 abaixo para fraturas burst simples ou longa de 2 acima e 2 abaixo para translação/distração).",
                    }
                ],
            },
        ],
    }


def get_slics():
    """Subaxial Cervical Spine Injury Classification System (Vaccaro et al. 2007)."""
    return {
        "id": "calc_slics",
        "slug": "slics",
        "name": "Escore SLICS para Trauma Cervical Subaxial",
        "acronym": "SLICS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Sistema de graduação para traumatismos da coluna cervical subaxial (C3 a C7) que avalia a morfologia da lesão, integridade do complexo disco-ligamentar (DLC) e estado neurológico, incluindo modificador aditivo de piora progressiva.",
        "summary": "Escore de decisão cirúrgica para traumatismo cervical C3 a C7 (corte cirúrgico >= 5 pontos).",
        "clinicalObjective": "Orientar o manejo das lesões cervicais subaxiais entre imobilização rígida, tração esquelética imediata e descompressão/artrodese cirúrgica urgente.",
        "targetPopulation": "Pacientes com traumatismo contuso da coluna cervical subaxial (C3 a C7). Contraindicado em fraturas de C1-C2.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Morfologia + Pontos_DLC + Pontos_Neurologico + Modificador_Progressivo (+1)",
        "evidenceSource": "Vaccaro AR, Hulbert RJ, Patel AA, et al. The subaxial cervical spine injury classification system: a novel approach to recognize the importance of morphology, neurology, and integrity of the disco-ligamentous complex. Spine. 2007;32(21):2365-2374.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "ALERTA CRÍTICO: (1) O modificador de piora neurológica progressiva adiciona +1 ponto de urgência, convertendo casos limítrofes (4 pontos) em indicação cirúrgica imediata (5 pontos). (2) Protocolo de perfusão medular: Manter PAM entre 85 e 90 mmHg por 7 dias contínuos no choque neurogênico cervical. Corticoterapia em megadoses (NASCIS) é expressamente desaconselhada.",
        "radarAxes": [
            {"id": "axis_slics_morph", "label": "Morfologia da Lesão", "system": "Mecânico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 4},
            {"id": "axis_slics_dlc", "label": "Complexo Disco-Ligamentar", "system": "Biomecânico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 2},
            {"id": "axis_slics_neuro", "label": "Status Neurológico", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_slics_mod", "label": "Progressão do Déficit", "system": "Evolutivo", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_slics_morphology",
                "name": "1. Morfologia da Lesão Cervical",
                "slug": "morfologia-slics",
                "inputType": "single_choice",
                "radarAxisId": "axis_slics_morph",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 1,
                "helpText": "Padrão de fratura ou luxação observado na TC da coluna cervical.",
                "options": [
                    {"id": "opt_slics_morph_none", "label": "Sem fratura ou fratura sem desalinhamento (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Alinhamento anatômico cervical mantido."},
                    {"id": "opt_slics_morph_comp", "label": "Fratura por Compressão Simples (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.25, "sortOrder": 2, "description": "Colapso do platô anterior sem cominuição posterior."},
                    {"id": "opt_slics_morph_burst", "label": "Fratura por Explosão / Burst (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 3, "description": "Fratura axial com invasão do canal vertebral por fragmento da parede posterior."},
                    {"id": "opt_slics_morph_distr", "label": "Fratura por Distração (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4, "description": "Separação axial anatômica por hiperextensão ou hiperflexão severa."},
                    {"id": "opt_slics_morph_trans", "label": "Fratura por Translação / Rotação (Luxação Facetária) (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5, "description": "Luxação unifacetária ou bifacetária, salto facetário ou espondilolistese traumática."},
                ],
            },
            {
                "id": "grp_slics_dlc",
                "name": "2. Complexo Disco-Ligamentar (DLC)",
                "slug": "dlc-slics",
                "inputType": "single_choice",
                "radarAxisId": "axis_slics_dlc",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 2,
                "helpText": "Disco intervertebral, ligamentos longitudinais anterior e posterior, cápsulas facetárias e ligamento amarelo.",
                "options": [
                    {"id": "opt_slics_dlc_intact", "label": "Íntegro (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem diástase facetária, sem alargamento do espaço discal e sem edema ligamentar na RM."},
                    {"id": "opt_slics_dlc_indet", "label": "Indeterminado (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Hipersinal isolado em partes moles pré-vertebrais ou ligamento interespinhal na RM sem ruptura mecânica evidente."},
                    {"id": "opt_slics_dlc_disrupt", "label": "Rompido / Desestruturado (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Diástase facetária, extrusão traumática discal ou gap interespinhal franco."},
                ],
            },
            {
                "id": "grp_slics_neuro",
                "name": "3. Estado Neurológico Admissional",
                "slug": "neurologico-slics",
                "inputType": "single_choice",
                "radarAxisId": "axis_slics_neuro",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 3,
                "helpText": "Avaliação clínica do nível neurológico motor e sensitivo.",
                "options": [
                    {"id": "opt_slics_neuro_intact", "label": "Neurologicamente Intacto (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Exame neurológico motor e sensitivo dos 4 membros estritamente normal."},
                    {"id": "opt_slics_neuro_rad", "label": "Radiculopatia Isolada (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Dor radicular ou déficit motor/sensitivo exclusivo no miótomo/dermátomo correspondente."},
                    {"id": "opt_slics_neuro_comp", "label": "Lesão Medular Completa - ASIA A (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3, "description": "Tetraplegia completa sem preservação sacral S4-S5."},
                    {"id": "opt_slics_neuro_incomp", "label": "Lesão Medular Incompleta - ASIA B, C ou D (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Função motora ou sensitiva residual preservada abaixo do nível neurológico da lesão."},
                ],
            },
            {
                "id": "grp_slics_modifier",
                "name": "4. Modificador de Piora Neurológica Progressiva",
                "slug": "modificador-progressivo-slics",
                "inputType": "single_choice",
                "radarAxisId": "axis_slics_mod",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Presença de deterioração neurológica documentada nas horas seguintes ao trauma.",
                "options": [
                    {"id": "opt_slics_mod_no", "label": "Ausente: Déficit estável ou paciente intacto (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem evolução progressiva de perda motora."},
                    {"id": "opt_slics_mod_yes", "label": "Presente: Piora motora progressiva ativa (+1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Perda contínua de força em membros superiores ou inferiores; sinal de compressão medular expansiva aguda."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_slics_cons",
                "label": "Tratamento Conservador Seguro (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Coluna cervical biomecanicamente estável. Baixo risco de subluxação tardia sob imobilização rígida.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_slics_analgesia",
                        "drugName": "Analgesia Oral Padrão",
                        "dosage": "Dipirona 1g VO 6/6h",
                        "route": "Oral",
                        "frequency": "6/6h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_slics_cons",
                        "recommendationTitle": "Tratamento Conservador Seguro com Colar Cervical Rígido",
                        "dispositionTarget": "Enfermaria / Ambulatório",
                        "monitoringPlan": "Uso contínuo de colar cervical rígido (Miami-J ou Filadélfia) por 6 a 12 semanas. Radiografias dinâmicas de flexo-extensão após consolidação para atestar estabilidade.",
                        "interventionalProcedure": "Cirurgia contraindicada.",
                    }
                ],
            },
            {
                "id": "tier_slics_lim",
                "label": "Conduta Limítrofe / Individualização (4 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Instabilidade mecânica relativa. Avaliar integridade discal e atividade física do paciente.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_slics_pain_mod",
                        "drugName": "Analgesia e Miorrelaxante",
                        "dosage": "Ciclobenzaprina 5 a 10 mg VO ao deitar + Dipirona",
                        "route": "Oral",
                        "frequency": "24/24h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_slics_lim",
                        "recommendationTitle": "Caso Limítrofe / Decisão Compartilhada",
                        "dispositionTarget": "Enfermaria de Especialidades",
                        "monitoringPlan": "Se falha ligamentar importante (DLC = 2) em paciente jovem: artrodese anterior precoce para prevenir cifose tardia; se paciente idoso com alto risco cirúrgico: manter colar rígido estrito com TC semanal.",
                        "interventionalProcedure": "Cirurgia eletiva de fixação versus haloveste/colar rígido.",
                    }
                ],
            },
            {
                "id": "tier_slics_surg",
                "label": "Indicação Cirúrgica Mandatória (5 a 10 pontos)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 10,
                "statisticalOutcome": "Instabilidade mecânica grave da coluna cervical e/ou compressão medular aguda em evolução. Risco elevado de dano neurológico permanente.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_slics_norepi_shock",
                        "drugName": "Noradrenalina IV Contínua (Protocolo de Perfusão Medular)",
                        "dosage": "Titulada para manter PAM entre 85 e 90 mmHg por 7 dias contínuos",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "16 mg em 234 mL SG 5% (64 mcg/mL). Manter perfusão na lesão medular aguda.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_slics_surg",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: Descompressão e Artrodese Cervical",
                        "dispositionTarget": "Centro Cirúrgico de Urgência",
                        "monitoringPlan": "Monitorização contínua de PAM invasiva (PAI) em UTI.",
                        "interventionalProcedure": "Se luxação facetária fechada em paciente consciente e cooperativo: tração esquelética cervical com halo Gardner-Wells sob controle fluoroscópico contínuo (proibida tração se hérnia discal livre em RM). Cirurgia definitiva: Artrodese Cervical Anterior e Discectomia (ACDF) com placa bloqueada e cage; se lesão posterior severa: Fixação Posterior (massa lateral C3-C6 e pedicular C7) ou via 360° combinada.",
                    }
                ],
            },
        ],
    }


def get_anderson_dalonzo():
    """Classificação de Fraturas de Odontoide de Anderson e D'Alonzo (1974) com Subtipos de Grauer."""
    return {
        "id": "calc_anderson_dalonzo",
        "slug": "anderson-dalonzo",
        "name": "Classificação de Anderson-D'Alonzo para Fraturas de Odontoide C2",
        "acronym": "Anderson-D'Alonzo",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Classificação anatômica padrão-ouro para fraturas do processo odontoide da vértebra C2 (áxis) associada à subestratificação de Grauer para indicação de parafuso anterior de odontoide versus artrodese posterior C1-C2.",
        "summary": "Estadiamento das fraturas de odontoide C2 em Tipos I, II (Grauer IIA/B/C) e III para direcionamento cirúrgico.",
        "clinicalObjective": "Quantificar a estabilidade biomecânica e taxa de pseudoartrose, definindo a indicação entre colar rígido, parafuso anterior de odontoide e artrodese posterior de Harms-Goel.",
        "targetPopulation": "Pacientes com fratura aguda do processo odontoide do áxis (C2) por trauma contuso.",
        "calculationType": "branching_decision",
        "formulaExpression": "Tipo Anatômico Anderson-D'Alonzo (I a III) e Orientação do Traço (Grauer)",
        "evidenceSource": "Anderson LD, D'Alonzo RT. Fractures of the odontoid process of the axis. J Bone Joint Surg Am. 1974;56(8):1663-1674. Grauer JN, Shafi B, Hilibrand AS, et al. Proposal of a modified, treatment-oriented classification of odontoid fractures. Spine J. 2005;5(2):123-129.",
        "minPossibleScore": 1,
        "maxPossibleScore": 3,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "CONTRAINDICAÇÃO FORMAL AO PARAFUSO ANTERIOR DE ODONTOIDE: (1) Traço oblíquo reverso (Grauer Tipo IIC: anteroinferior para posterossuperior) — o aperto do parafuso causa cisalhamento e deslocamento anterior do dente; (2) Cominuição da base; (3) Ruptura do ligamento transverso associada; (4) Osteoporose grave; (5) Hipercifose torácica (impede a trajetória anterior da broca). Nestes casos, a conduta mandatória é a Artrodese Posterior C1-C2 de Harms-Goel.",
        "radarAxes": [
            {"id": "axis_od_type", "label": "Tipo Anatômico da Fratura", "system": "Anatômico", "unit": "grau", "baselineValue": 1, "maxAxisValue": 3},
            {"id": "axis_od_nonunion", "label": "Risco de Pseudoartrose", "system": "Biológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_od_approach", "label": "Complexidade da Abordagem", "system": "Cirúrgico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_anderson_type",
                "name": "Tipo Anatômico da Fratura de Odontoide",
                "slug": "tipo-anderson-dalonzo",
                "inputType": "single_choice",
                "radarAxisId": "axis_od_type",
                "normalBaselineValue": 1,
                "maxAxisValue": 3,
                "sortOrder": 1,
                "helpText": "Nível anatômico do traço de fratura no processo odontoide avaliado na TC em corte sagital e coronal.",
                "options": [
                    {
                        "id": "opt_od_type1",
                        "label": "Tipo I: Fratura no Ápice do Odontoide (Avulsão do Ligamento Alar) (1 pt)",
                        "pointValue": 1,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Avulsão rara da ponta do odontoide. Estável se ligamento alar contralateral íntegro. Taxa de consolidação espontânea > 99%.",
                    },
                    {
                        "id": "opt_od_type2_b",
                        "label": "Tipo II (Grauer IIB): Base do Odontoide com Traço Oblíquo Favorável a Parafuso Anterior (2 pts)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.7,
                        "sortOrder": 2,
                        "description": "Fratura na base/colo do odontoide (zona watershed) com traço de anterossuperior para posteroinferior. Candidato ideal a parafuso anterior.",
                    },
                    {
                        "id": "opt_od_type2_c",
                        "label": "Tipo II (Grauer IIC): Base do Odontoide com Traço Reverso ou Cominuição (2 pts)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Traço oblíquo reverso ou cominuição severa da base. Contraindica parafuso anterior; exige fixação posterior C1-C2 de Harms.",
                    },
                    {
                        "id": "opt_od_type3",
                        "label": "Tipo III: Fratura com Extensão para o Corpo Esponjoso de C2 (3 pts)",
                        "pointValue": 3,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.2,
                        "sortOrder": 4,
                        "description": "Traço que mergulha no osso esponjoso trabecular ricamente vascularizado do corpo de C2. Alta taxa de união consolidada (85-95%).",
                    },
                ],
            }
        ],
        "riskTiers": [
            {
                "id": "tier_od_cons",
                "label": "Tipos I e III: Tratamento Conservador Seguro",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Taxa de consolidação óssea espontânea superior a 85% a 95% sob imobilização externa adequada.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_od_pain",
                        "drugName": "Analgesia Simples com Dipirona",
                        "dosage": "1g VO 6/6h se dor cervical",
                        "route": "Oral",
                        "frequency": "6/6h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_od_cons",
                        "recommendationTitle": "Tratamento Conservador Seguro com Colar Cervical Rígido",
                        "dispositionTarget": "Ambulatório de Cirurgia de Coluna",
                        "monitoringPlan": "Uso estrito de colar cervical rígido (Filadélfia ou Miami-J) ou órtese tipo SOMI por 8 a 12 semanas. Radiografia em perfil aos 30 e 60 dias.",
                        "interventionalProcedure": "Cirurgia contraindicada.",
                    }
                ],
            },
            {
                "id": "tier_od_screw",
                "label": "Tipo IIB: Indicação de Osteossíntese Anterior com Parafuso de Odontoide",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Preservação de 50% da rotação axial cervical fisiológica da articulação C1-C2 e taxa de união anatômica de 85% a 90%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_od_proph",
                        "drugName": "Cefazolina Profilática Perioperatória",
                        "dosage": "2g IV na indução cirúrgica",
                        "route": "Intravenosa",
                        "frequency": "Dose única na indução",
                        "dilutionInstructions": "Diluir em 100 mL de SF 0,9% e infundir em 20 a 30 minutos.",
                        "contraindications": "Hipersensibilidade grave conhecida a cefalosporinas ou betalactâmicos.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_od_screw",
                        "recommendationTitle": "Osteossíntese Anterior com Parafuso Canulado de Odontoide (Técnica de Bohler/Apfelbaum)",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Fluoroscopia biplanar intraoperatória (AP transoral e perfil contínuos).",
                        "interventionalProcedure": "Abordagem cervical ântero-medial na altura de C5-C6, passagem de fio-guia através da borda anteroinferior de C2 até o ápice do odontoide e inserção de 1 ou 2 parafusos canulados de rosca parcial de 3,5 mm para compressão interfragmentar. Preserva 50% da rotação cervical.",
                    }
                ],
            },
            {
                "id": "tier_od_harms",
                "label": "Tipo IIC / Falha de Parafuso: Indicação de Artrodese Posterior C1-C2 de Harms-Goel",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Taxa de consolidação óssea > 98%, sacrificando a rotação axial C1-C2.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_od_harms_abx",
                        "drugName": "Cefazolina 2g IV",
                        "dosage": "2g IV na indução anestésica",
                        "route": "Intravenosa",
                        "frequency": "Indução",
                        "dilutionInstructions": "Diluir em 100 mL de SF 0,9% administrado até 30 minutos antes da incisão.",
                        "contraindications": "Anafilaxia prévia a penicilinas ou cefalosporinas.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_od_harms",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: Artrodese Posterior C1-C2 Instrumentada (Harms-Goel)",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Verificação anatômica pré-operatória da artéria vertebral em angio-TC para descartar trajeto anômalo/deiscente.",
                        "interventionalProcedure": "Artrodese instrumentada via posterior com parafusos em massa lateral de C1 e parafusos pediculares/ístmicos de C2 (Técnica de Harms) ou parafusos intralaminares de Wright em C2 se artéria vertebral aberrante + enxerto ósseo autólogo interlaminal.",
                    }
                ],
            },
        ],
    }


def get_sins():
    """Spine Instability Neoplastic Score (Fisher et al., Spine Oncology Study Group 2010)."""
    return {
        "id": "calc_sins",
        "slug": "sins",
        "name": "SINS - Escore de Instabilidade Neoplásica da Coluna Vertebral",
        "acronym": "SINS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Escore abrangente de 6 domínios (0 a 18 pontos) que diagnostica e quantifica a instabilidade mecânica em pacientes portadores de metástases da coluna vertebral, definindo a necessidade de estabilização cirúrgica antes da radioterapia.",
        "summary": "Escore de 0 a 18 pontos que diagnostica instabilidade mecânica em metástases espinhais.",
        "clinicalObjective": "Identificar instabilidade neoplásica espinhal para indicar estabilização cirúrgica ou cifoplastia/vertebroplastia previamente a procedimentos radioterápicos.",
        "targetPopulation": "Pacientes oncológicos com metástases vertebrais comprovadas de C0 ao sacro.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Localizacao + Pontos_Dor + Pontos_Lesao + Pontos_Alinhamento + Pontos_Colapso + Pontos_Elementos_Posteriores",
        "evidenceSource": "Fisher CG, DiPaola CP, Ryken TC, et al. A novel classification system for spinal instability in neoplastic disease: an evidence-based approach and expert consensus from the Spine Oncology Study Group. Spine. 2010;35(19):E1221-E1229.",
        "minPossibleScore": 0,
        "maxPossibleScore": 18,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "ALERTA ONCOLÓGICO MANDATÓRIO: A radioterapia convencional ou SBRT é FORMALMENTE CONTRAINDICADA de forma isolada na vigência de instabilidade mecânica comprovada (SINS >= 13 pontos), pois a radiação acelera a necrose óssea e o colapso estrutural catastrófico com compressão medular aguda. A coluna instável exige fixação instrumentada prévia à irradiação.",
        "radarAxes": [
            {"id": "axis_sins_location", "label": "Localização e Alinhamento", "system": "Anatômico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 7},
            {"id": "axis_sins_pain", "label": "Dor Mecânica", "system": "Clínico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_sins_bone", "label": "Destruição Óssea / Lise", "system": "Biológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 2},
            {"id": "axis_sins_collapse", "label": "Colapso e Elementos Posteriores", "system": "Estrutural", "unit": "pts", "baselineValue": 0, "maxAxisValue": 6},
        ],
        "parameterGroups": [
            {
                "id": "grp_sins_location",
                "name": "1. Localização Anatômica da Metástase",
                "slug": "localizacao-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_location",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 1,
                "helpText": "Segmento anatômico acometido da coluna vertebral.",
                "options": [
                    {"id": "opt_sins_loc_junc", "label": "Segmento Juncional: Occipito-C2, C7-T1, T11-L1, L5-S1 (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Zonas de alta transição biomecânica e máxima tensão de cisalhamento."},
                    {"id": "opt_sins_loc_mob", "label": "Segmento Móvel: C3-C6, L2-L4 (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 2, "description": "Segmentos com amplitude de movimento significativa."},
                    {"id": "opt_sins_loc_semirig", "label": "Segmento Semirrígido: T2-T10 (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3, "description": "Estabilizado pelo gradil costal e esterno."},
                    {"id": "opt_sins_loc_rigid", "label": "Segmento Rígido: S2-S5 / Sacro distal (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 4, "description": "Estrutura anelar pélvica estável."},
                ],
            },
            {
                "id": "grp_sins_pain",
                "name": "2. Característica da Dor",
                "slug": "dor-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_pain",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 2,
                "helpText": "Diferenciação entre dor puramente inflamatória e dor mecânica com carga.",
                "options": [
                    {"id": "opt_sins_pain_mech", "label": "Dor Mecânica Franca (Piora com ortostase/movimento, alivia com decúbito) (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Sinal patognomônico de instabilidade estrutural do corpo vertebral."},
                    {"id": "opt_sins_pain_nonmech", "label": "Dor Não Mecânica / Noturna Inflamatória Isolada (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Dor constante decorrente de estiramento do periósteo tumoral."},
                    {"id": "opt_sins_pain_none", "label": "Sem dor / Lesão Assintomática (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 3, "description": "Achado incidental em estadiamento de rotina."},
                ],
            },
            {
                "id": "grp_sins_bone",
                "name": "3. Tipo de Lesão Óssea",
                "slug": "tipo-lesao-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_bone",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 3,
                "helpText": "Padrão de destruição óssea na tomografia computadorizada.",
                "options": [
                    {"id": "opt_sins_bone_lytic", "label": "Estritamente Lítica (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Destruição radiotransparente pura (ex.: rim, tireoide, pulmão, melanoma)."},
                    {"id": "opt_sins_bone_mixed", "label": "Mista: Lítica e Blástica coexistentes (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Componentes líticos e osteoescleróticos simultâneos (ex.: mama)."},
                    {"id": "opt_sins_bone_blastic", "label": "Estritamente Blástica (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 3, "description": "Lesão osteoesclerótica hiperdensa pura (ex.: próstata)."},
                ],
            },
            {
                "id": "grp_sins_alignment",
                "name": "4. Alinhamento Radiográfico da Coluna",
                "slug": "alinhamento-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_location",
                "normalBaselineValue": 0,
                "maxAxisValue": 4,
                "sortOrder": 4,
                "helpText": "Presença de subluxação, espondilolistese ou deformidade progressiva de novo.",
                "options": [
                    {"id": "opt_sins_align_sublux", "label": "Subluxação ou Translação Vertebral Evidente (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Deslocamento de uma vértebra sobre a adjacente."},
                    {"id": "opt_sins_align_denovo", "label": "Deformidade de Novo (Cifose ou escoliose progressiva secundária) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Perda do alinhamento sagital ou coronal prévio."},
                    {"id": "opt_sins_align_norm", "label": "Alinhamento Anatômico Mantido / Normal (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 3, "description": "Sem desvios ou translações vertebrais."},
                ],
            },
            {
                "id": "grp_sins_collapse",
                "name": "5. Grau de Colapso do Corpo Vertebral",
                "slug": "colapso-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_collapse",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 5,
                "helpText": "Perda percentual da altura do corpo vertebral acometido.",
                "options": [
                    {"id": "opt_sins_coll_gt50", "label": "Colapso > 50% da altura do corpo vertebral (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Achatamento marcante com risco de retropulsão para o canal."},
                    {"id": "opt_sins_coll_le50", "label": "Colapso <= 50% da altura do corpo vertebral (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 2, "description": "Colapso parcial do muro anterior ou platô."},
                    {"id": "opt_sins_coll_inv_gt50", "label": "Sem colapso, com envolvimento tumoral > 50% do corpo (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3, "description": "Substituição trabecular sem colapso mecânico."},
                    {"id": "opt_sins_coll_inv_le50", "label": "Sem colapso, com envolvimento tumoral <= 50% do corpo (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 4, "description": "Lesão focal circunscrita sem risco imediato."},
                ],
            },
            {
                "id": "grp_sins_posterior",
                "name": "6. Acometimento dos Elementos Posteriores",
                "slug": "elementos-posteriores-sins",
                "inputType": "single_choice",
                "radarAxisId": "axis_sins_collapse",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 6,
                "helpText": "Infiltração tumoral dos pedículos, lâminas, processos transversos ou facetas.",
                "options": [
                    {"id": "opt_sins_post_bilat", "label": "Acometimento Bilateral dos Elementos Posteriores (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Destruição bilateral de pedículos ou lâminas (perda total da banda de tensão)."},
                    {"id": "opt_sins_post_unilat", "label": "Acometimento Unilateral dos Elementos Posteriores (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Destruição pedicular ou facetária unilateral."},
                    {"id": "opt_sins_post_none", "label": "Nenhum acometimento de elementos posteriores (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 3, "description": "Elementos posteriores anatomicamente íntegros."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_sins_stable",
                "label": "Coluna Estável (0 a 6 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 6,
                "statisticalOutcome": "Coluna estruturalmente estável. Baixíssimo risco de colapso patológico.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sins_biphosphonate",
                        "drugName": "Ácido Zoledrônico ou Denosumabe",
                        "dosage": "Ácido Zoledrônico 4 mg IV a cada 3-4 semanas ou Denosumabe 120 mg SC",
                        "route": "Intravenosa / Subcutânea",
                        "frequency": "Mensal",
                        "dilutionInstructions": "Infundir Zoledrônico em 100 mL de SF 0,9% em 15 minutos com hidratação.",
                        "contraindications": "Clearance de creatinina < 30 mL/min (ajustar ou optar por Denosumabe).",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sins_stable",
                        "recommendationTitle": "Radioterapia Externa Convencional ou SBRT Segura",
                        "dispositionTarget": "Radioterapia / Oncologia",
                        "monitoringPlan": "Acompanhamento radiológico trimestral. Dispensada estabilização cirúrgica prévia.",
                        "interventionalProcedure": "Cirurgia profilática contraindicada.",
                    }
                ],
            },
            {
                "id": "tier_sins_potential",
                "label": "Coluna Potencialmente Instável (7 a 12 pontos)",
                "severityLevel": "intermediate",
                "minScore": 7,
                "maxScore": 12,
                "statisticalOutcome": "Instabilidade mecânica latente. Risco moderado a elevado de fratura e colapso vertebral sob estresse mecânico ou pós-radiação.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sins_analgesia_pot",
                        "drugName": "Otimização Álgica com Opióides",
                        "dosage": "Morfina ou Oxicodona de liberação controlada",
                        "route": "Oral",
                        "frequency": "12/12h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sins_potential",
                        "recommendationTitle": "Caso Limítrofe / Avaliação Neurocirúrgica Especializada Mandatória",
                        "dispositionTarget": "Neurocirurgia / Cirurgia de Coluna",
                        "monitoringPlan": "Se dor estritamente mecânica sem invasão do canal: indicar Cifoplastia com Balão ou Vertebroplastia percutânea para alívio imediato e suporte mecânico antes da SBRT; se envolvimento juncional ou de elementos posteriores: considerar artrodese percutânea instrumentada.",
                        "interventionalProcedure": "Cifoplastia percutânea ou estabilização cirúrgica minimamente invasiva prévia à radioterapia.",
                    }
                ],
            },
            {
                "id": "tier_sins_unstable",
                "label": "Coluna Instável (13 a 18 pontos)",
                "severityLevel": "critical",
                "minScore": 13,
                "maxScore": 18,
                "statisticalOutcome": "Instabilidade mecânica grave inequívoca. Risco iminente de colapso catastrófico e compressão medular aguda.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sins_dexa",
                        "drugName": "Dexametasona IV em Altas Doses",
                        "dosage": "10 mg IV bolus inicial, seguido de 4 mg IV 6/6h com desmame progressivo",
                        "route": "Intravenosa",
                        "frequency": "6/6h",
                        "dilutionInstructions": "Associar a inibidor de bomba de prótons (Omeprazol 40 mg IV/dia).",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sins_unstable",
                        "recommendationTitle": "Estabilização Cirúrgica Mandatória Prévia à Radioterapia",
                        "dispositionTarget": "Centro Cirúrgico de Urgência",
                        "monitoringPlan": "Repouso no leito até a estabilização cirúrgica definitiva. PROIBIDA RADIOTERAPIA ISOLADA SEM FIXAÇÃO.",
                        "interventionalProcedure": "Artrodese Posterior Instrumentada com Parafusos Pediculares (construção de pelo menos 2 níveis acima e 2 níveis abaixo) associada a reconstrução anterior com corpectomia e cage se colapso severo.",
                    }
                ],
            },
        ],
    }


def get_noms_bilsky():
    """NOMS Decision Framework for Spine Metastases & Bilsky ESCC Scale (Bilsky et al. 2013)."""
    return {
        "id": "calc_noms_bilsky",
        "slug": "noms-bilsky",
        "name": "Framework NOMS e Escala de Bilsky (ESCC) para Metástases Espinhais",
        "acronym": "NOMS / Bilsky",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Algoritmo multidimensional padrão-ouro que integra compressão medular epidural (Neurológico - Bilsky 0 a 3), radiossensibilidade tumoral (Oncológico), escore SINS (Mecânico) e tolerância cirúrgica (Sistêmico), estabelecendo o paradigma moderno da Cirurgia de Separação (Separation Surgery) com SBRT.",
        "summary": "Algoritmo multidimensional de decisão cirúrgica e radioterápica para metástases vertebrais.",
        "clinicalObjective": "Definir o plano terapêutico ideal (Cirurgia de Separação + SBRT vs Radioterapia Convencional vs Estabilização isolada vs Paliação) em pacientes com metástases na coluna vertebral.",
        "targetPopulation": "Pacientes oncológicos com metástases vertebrais com ou sem compressão medular epidural.",
        "calculationType": "branching_decision",
        "formulaExpression": "Cruzamento Multidimensional 4D: N (Bilsky 0-3) x O (Radiossensibilidade) x M (SINS) x S (KPS/ECOG)",
        "evidenceSource": "Bilsky MH, Laufer I, Fourney DR, et al. Reliability analysis of the epidural spinal cord compression scale. J Neurosurg Spine. 2010;13(3):324-328. Laufer I, Rubin DG, Lis E, et al. The NOMS framework: approach to the treatment of spinal metastatic tumors. Oncologist. 2013;18(6):744-751.",
        "minPossibleScore": 1,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "CONCEITO FUNDAMENTAL DA CIRURGIA DE SEPARAÇÃO (SEPARATION SURGERY): Em tumores radiorresistentes (ex.: rim, melanoma, cólon) com compressão medular de alto grau (Bilsky 2 ou 3), o objetivo cirúrgico moderno NÃO é a ressecção oncológica completa do corpo vertebral, mas sim a descompressão circunferencial focal da dura-máter para criar uma margem de segurança liquórica de 2 a 3 mm ao redor da medula + artrodese posterior, permitindo a posterior entrega de radiocirurgia estereotática ablativa (SBRT 18 a 24 Gy) sem neurotoxicidade medular.",
        "radarAxes": [
            {"id": "axis_noms_neuro", "label": "Compressão Epidural (Bilsky)", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 3},
            {"id": "axis_noms_onco", "label": "Radiorresistência", "system": "Oncológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_noms_mech", "label": "Instabilidade Mecânica (SINS)", "system": "Mecânico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 2},
            {"id": "axis_noms_syst", "label": "Reserva Sistêmica (KPS)", "system": "Sistêmico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_noms_neuro",
                "name": "1. N - Pilar Neurológico: Escala de Bilsky (ESCC)",
                "slug": "bilsky-noms",
                "inputType": "single_choice",
                "radarAxisId": "axis_noms_neuro",
                "normalBaselineValue": 0,
                "maxAxisValue": 3,
                "sortOrder": 1,
                "helpText": "Grau de compressão medular epidural na ressonância magnética axial ponderada em T2.",
                "options": [
                    {"id": "opt_bilsky_0", "label": "Bilsky 0: Osso puro, sem acometimento epidural (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Doença restrita ao corpo vertebral."},
                    {"id": "opt_bilsky_1a", "label": "Bilsky 1a: Contato dural simples, sem deformar o saco tecal (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2, "description": "Tumor epidural encostando na dura sem deformação."},
                    {"id": "opt_bilsky_1b", "label": "Bilsky 1b: Deformação do saco dural sem contato com a medula (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 3, "description": "Recuo do saco dural com espaço liquórico preservado ao redor da medula."},
                    {"id": "opt_bilsky_1c", "label": "Bilsky 1c: Deformação dural e contato medular sem deslocamento da medula (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 4, "description": "Tumor toca a medula mas sem deslocá-la."},
                    {"id": "opt_bilsky_2", "label": "Bilsky 2: Compressão medular evidente com líquor ainda visível (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 5, "description": "Compressão de alto grau; há uma lâmina delgada de líquor residual."},
                    {"id": "opt_bilsky_3", "label": "Bilsky 3: Compressão medular circunferencial grave com colapso liquórico total (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 6, "description": "Obliteração completa do espaço subaracnóideo com medula deformada (alto risco de necrose)."},
                ],
            },
            {
                "id": "grp_noms_onco",
                "name": "2. O - Pilar Oncológico: Radiossensibilidade Convencional",
                "slug": "radiossensibilidade-noms",
                "inputType": "single_choice",
                "radarAxisId": "axis_noms_onco",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Resposta biológica do tumor primário à radioterapia convencional fracionada.",
                "options": [
                    {"id": "opt_onco_sens", "label": "Tumor Radiossensível (Mieloma, Linfoma, Seminoma, Próstata, CPPC) (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Resposta rápida e volumosa à radioterapia convencional com descompressão medular."},
                    {"id": "opt_onco_resist", "label": "Tumor Radiorresistente (Carcinoma Renal, Melanoma, Cólon, Tireoide, Sarcomas) (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Falha em > 80% sob radiação convencional; exige doses ablativas de SBRT para controle tumoral."},
                ],
            },
            {
                "id": "grp_noms_mech",
                "name": "3. M - Pilar Mecânico: Escore SINS",
                "slug": "sins-noms",
                "inputType": "single_choice",
                "radarAxisId": "axis_noms_mech",
                "normalBaselineValue": 0,
                "maxAxisValue": 2,
                "sortOrder": 3,
                "helpText": "Grau de instabilidade biomecânica da coluna.",
                "options": [
                    {"id": "opt_noms_sins_stable", "label": "Coluna Estável: SINS 0 a 6 pontos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem dor mecânica, alinhamento mantido."},
                    {"id": "opt_noms_sins_pot", "label": "Coluna Potencialmente Instável: SINS 7 a 12 pontos (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Dor mecânica ou fratura parcial; considerar suporte percutâneo."},
                    {"id": "opt_noms_sins_unst", "label": "Coluna Instável: SINS 13 a 18 pontos (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Indicação mandatória de estabilização cirúrgica prévia a qualquer tratamento radiante."},
                ],
            },
            {
                "id": "grp_noms_syst",
                "name": "4. S - Pilar Sistêmico: Status Funcional e Sobrevida",
                "slug": "status-sistemico-noms",
                "inputType": "single_choice",
                "radarAxisId": "axis_noms_syst",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Capacidade de tolerar anestesia geral e expectativa de vida estimada.",
                "options": [
                    {"id": "opt_syst_fit", "label": "Elegível Cirurgicamente: KPS >= 70% e Sobrevida Estimada >= 3 meses (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Paciente com reserva funcional e sobrevida que justifica o procedimento descompressivo/estabilizador."},
                    {"id": "opt_syst_unfit", "label": "Inelegível Cirurgicamente / Cuidados Paliativos: KPS < 50% ou Sobrevida < 2-3 meses (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Terminalidade ou comorbidades cardiopulmonares proibitivas."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_noms_sep_sbrt",
                "label": "Perfil 1: Cirurgia de Separação + SBRT Hipofracionada",
                "severityLevel": "critical",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Controle local oncológico da coluna > 85% a 90% em 1 ano e preservação da função motora com deambulação.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_noms_dexa_high",
                        "drugName": "Dexametasona IV",
                        "dosage": "10 mg IV bolus seguido de 4 mg 6/6h com desmame em 7 a 10 dias",
                        "route": "Intravenosa",
                        "frequency": "6/6h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_noms_sep",
                        "recommendationTitle": "Indicação de Cirurgia de Separação (Separation Surgery) + Artrodese Posterior",
                        "dispositionTarget": "Centro Cirúrgico Eletivo de Urgência",
                        "monitoringPlan": "Ressonância magnética pós-operatória precoce para planejamento conformacional da SBRT.",
                        "interventionalProcedure": "Laminectomia descompressiva associada à facetectomia e curetagem parcial posterior do muro posterior do corpo vertebral para restaurar margem tecal livre de 2 a 3 mm ao redor da medula espinhal + Fixação posterior com parafusos pediculares (2 acima e 2 abaixo), seguida de SBRT (18 a 24 Gy em 1 a 3 frações) após 2 a 4 semanas.",
                    }
                ],
            },
            {
                "id": "tier_noms_ebrt",
                "label": "Perfil 2: Radioterapia Convencional de Urgência (cEBRT)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de resposta tumoral rápida de 80% a 90% com melhora álgica e descompressão medular induzida pela radiação.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_noms_dexa_ebrt",
                        "drugName": "Dexametasona IV em Altas Doses",
                        "dosage": "10 mg IV na emergência + 4 mg 6/6h durante os primeiros dias de radioterapia",
                        "route": "Intravenosa / Oral",
                        "frequency": "6/6h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_noms_ebrt",
                        "recommendationTitle": "Radioterapia Externa Fracionada de Urgência (30 Gy / 10 frações)",
                        "dispositionTarget": "Radioterapia de Urgência",
                        "monitoringPlan": "Avaliação neurológica diária durante as sessões de radiação. Se SINS >= 13, realizar fixação instrumentada percutânea para sustentação mecânica.",
                        "interventionalProcedure": "Cirurgia descompressiva aberta dispensada (tumor altamente radiossensível).",
                    }
                ],
            },
            {
                "id": "tier_noms_sbrt_stab",
                "label": "Perfil 3: SBRT Primária Isolada ou Estabilização Percutânea",
                "severityLevel": "low",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Controle oncológico excelente com toxicidade medular nula (espaço liquórico preservado).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_noms_analg_p3",
                        "drugName": "Analgesia Otimizada e Bifosfonato",
                        "dosage": "Ácido Zoledrônico 4 mg IV mensal",
                        "route": "Intravenosa",
                        "frequency": "A cada 28 dias",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_noms_sbrt",
                        "recommendationTitle": "Radiocirurgia Estereotática Ablativa Primária (SBRT)",
                        "dispositionTarget": "Radiocirurgia Ambulatorial",
                        "monitoringPlan": "Se houver dor mecânica / SINS 7-12: realizar Cifoplastia com Balão percutânea antes da SBRT.",
                        "interventionalProcedure": "Cirurgia aberta não indicada.",
                    }
                ],
            },
            {
                "id": "tier_noms_palliative",
                "label": "Perfil 4: Cuidados Paliativos Exclusivos / Hospice",
                "severityLevel": "low",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Controle de sintomas álgicos e conforto com mínima toxicidade terapêutica.",
                "colorHex": "#64748b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_noms_palliation",
                        "drugName": "Analgesia Potente com Morfina e Corticoide de Conforto",
                        "dosage": "Morfina titulada + Dexametasona 4 a 8 mg/dia",
                        "route": "Subcutânea / Oral",
                        "frequency": "Contínua / Regrada",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_noms_hospice",
                        "recommendationTitle": "Radioterapia Paliativa de Curso Curto (Fração Única 8 Gy)",
                        "dispositionTarget": "Cuidados Paliativos / Hospice",
                        "monitoringPlan": "Foco exclusivo no alívio do sofrimento e suporte familiar. Procedimentos invasivos e cirurgia instrumentada contraindicados.",
                        "interventionalProcedure": "Cirurgia aberta formalmente contraindicada por futilidade terapêutica.",
                    }
                ],
            },
        ],
    }


def get_sagittal_balance():
    """Calculadora de Balanço Sagital, Parâmetros Espinopélvicos e Classificação SRS-Schwab."""
    return {
        "id": "calc_sagittal_balance",
        "slug": "balanco-sagital",
        "name": "Balanço Sagital e Parâmetros Espinopélvicos (SRS-Schwab)",
        "acronym": "Balanço Sagital",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Calculadora morfométrica para aferição dos parâmetros angulares e lineares da bacia e coluna vertebral (Incidência Pélvica PI, Versão Pélvica PT, Inclinação Sacral SS, Lordose Lombar LL e Eixo Vertical Sagital SVA), estratificando descompassos espinopélvicos conforme a classificação SRS-Schwab e direcionando o planejamento de osteotomias (SPO vs PSO vs VCR).",
        "summary": "Cálculo do descompasso espinopélvico (PI - LL), alvos de lordose e osteotomias de Schwab na radiografia panorâmica.",
        "clinicalObjective": "Diagnosticar o desbalanço sagital espinopélvico e guiar o planejamento cirúrgico de restauração de lordose em deformidades vertebrais do adulto.",
        "targetPopulation": "Pacientes com deformidade vertebral do adulto, escoliose degenerativa ou planejamento de artrodese toracolombar longa.",
        "calculationType": "continuous_formula",
        "formulaExpression": "PI = PT + SS | Descompasso = PI - LL (Alvo: PI ± 9°) | Modificadores SRS-Schwab",
        "evidenceSource": "Schwab F, Ungar B, Blondel B, et al. Scoliosis Research Society-Schwab adult spinal deformity classification: a validation study. Spine. 2012;37(12):1077-1082. Duval-Beaupère G, Schmidt C, Cosson P. A Barycentremetric approach to evolution of the spinal curvature. Spine. 1992;17(3):261-267.",
        "minPossibleScore": 0,
        "maxPossibleScore": 3,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "IDENTIDADE GEOMÉTRICA DE DUVAL-BEAUPÈRE: Pela geometria fundamental da pelve, a Incidência Pélvica é rigorosamente a soma algébrica da Versão Pélvica com a Inclinação Sacral: PI = PT + SS. Uma diferença superior a 3° entre PI e (PT + SS) denuncia erro técnico grosseiro de aferição radiográfica (demarcação imprecisa do platô de S1 ou do centro das cabeças femorais na radiografia panorâmica).",
        "radarAxes": [
            {"id": "axis_sb_pi_ll", "label": "Descompasso (PI - LL)", "system": "Geométrico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_sb_pt", "label": "Versão Pélvica (PT)", "system": "Postural", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_sb_sva", "label": "Eixo Sagital (SVA)", "system": "Sagital", "unit": "mm", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_sb_pi",
                "name": "1. Incidência Pélvica (PI - Pelvic Incidence)",
                "slug": "pelvic-incidence",
                "inputType": "numeric_input",
                "unit": "grau",
                "radarAxisId": "axis_sb_pi_ll",
                "normalBaselineValue": 53,
                "maxAxisValue": 100,
                "sortOrder": 1,
                "helpText": "Constante anatômica fixa no adulto. Ângulo entre a perpendicular ao platô de S1 e a linha ao centro das cabeças femorais. Valor médio: 53° ± 10°.",
                "options": [
                    {
                        "id": "opt_sb_pi_val",
                        "label": "Valor medido da Incidência Pélvica (graus)",
                        "pointValue": 53,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Valor angular em graus na radiografia panorâmica"
                    }
                ],
            },
            {
                "id": "grp_sb_pt",
                "name": "2. Versão Pélvica (PT - Pelvic Tilt)",
                "slug": "pelvic-tilt",
                "inputType": "numeric_input",
                "unit": "grau",
                "radarAxisId": "axis_sb_pt",
                "normalBaselineValue": 13,
                "maxAxisValue": 60,
                "sortOrder": 2,
                "helpText": "Medida dinâmica de rotação da pelve (retroversão compensatória). Ângulo entre a linha do centro das cabeças femorais ao ponto médio de S1 e a vertical. Normal: < 20° (médio 13° ± 7°).",
                "options": [
                    {
                        "id": "opt_sb_pt_val",
                        "label": "Valor medido da Versão Pélvica (graus)",
                        "pointValue": 13,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Valor angular em graus na radiografia panorâmica"
                    }
                ],
            },
            {
                "id": "grp_sb_ss",
                "name": "3. Inclinação Sacral (SS - Sacral Slope)",
                "slug": "sacral-slope",
                "inputType": "numeric_input",
                "unit": "grau",
                "radarAxisId": "axis_sb_pi_ll",
                "normalBaselineValue": 40,
                "maxAxisValue": 70,
                "sortOrder": 3,
                "helpText": "Ângulo entre o platô sacral superior de S1 e a horizontal. Normal: 40° ± 8°.",
                "options": [
                    {
                        "id": "opt_sb_ss_val",
                        "label": "Valor medido da Inclinação Sacral (graus)",
                        "pointValue": 40,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Valor angular em graus na radiografia panorâmica"
                    }
                ],
            },
            {
                "id": "grp_sb_ll",
                "name": "4. Lordose Lombar Atual (LL - Lumbar Lordosis Cobb L1-S1)",
                "slug": "lumbar-lordosis",
                "inputType": "numeric_input",
                "unit": "grau",
                "radarAxisId": "axis_sb_pi_ll",
                "normalBaselineValue": 53,
                "maxAxisValue": 90,
                "sortOrder": 4,
                "helpText": "Ângulo de Cobb entre o platô superior de L1 e o platô superior de S1. Normal fisiológico: 40° a 65°.",
                "options": [
                    {
                        "id": "opt_sb_ll_val",
                        "label": "Valor medido da Lordose Lombar Cobb L1-S1 (graus)",
                        "pointValue": 53,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Valor angular em graus na radiografia panorâmica"
                    }
                ],
            },
            {
                "id": "grp_sb_sva",
                "name": "5. Eixo Vertical Sagital (SVA - C7 Plumbline)",
                "slug": "sva-sagittal",
                "inputType": "numeric_input",
                "unit": "mm",
                "radarAxisId": "axis_sb_sva",
                "normalBaselineValue": 20,
                "maxAxisValue": 250,
                "sortOrder": 5,
                "helpText": "Distância horizontal linear da linha de prumo que passa pelo centro do corpo de C7 até o canto posterior-superior de S1 em mm. Normal: < 40 mm.",
                "options": [
                    {
                        "id": "opt_sb_sva_val",
                        "label": "Valor medido do Eixo Vertical Sagital C7-S1 (mm)",
                        "pointValue": 20,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Distância horizontal linear em milímetros"
                    }
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_sb_aligned",
                "label": "Balanço Sagital Preservado (Schwab 0)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Descompasso espinopélvico normal (PI - LL < 10°), versão pélvica normal (PT < 20°) e alinhamento linear preservado (SVA < 40 mm).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sb_standard",
                        "drugName": "Manejo Clínico e Reabilitação Postural",
                        "dosage": "Fisioterapia motora focada em fortalecimento de core e cadeia posterior",
                        "route": "Não farmacológica / Oral",
                        "frequency": "3x por semana",
                        "dilutionInstructions": "Não se aplica (terapia física de alinhamento postural).",
                        "contraindications": "Instabilidade mecânica aguda ou déficit neurológico progressivo.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sb_situ",
                        "recommendationTitle": "Artrodese in situ sem necessidade de osteotomias maiores",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Manutenção da lordose fisiológica prévia.",
                        "interventionalProcedure": "Se indicação de cirurgia por espondilolistese ou estenose: realizar artrodese in situ sem osteotomias de cunha/subtração.",
                    }
                ],
            },
            {
                "id": "tier_sb_mod_deformity",
                "label": "Desbalanço Sagital Moderado (Schwab +)",
                "severityLevel": "intermediate",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Descompasso moderado (PI - LL entre 10° e 20°), retroversão pélvica compensatória (PT 20-30°) ou desbalanço anterior moderado (SVA 40 a 95 mm).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sb_mod_pain",
                        "drugName": "Analgesia Escalonada (Paracetamol / Tramadol)",
                        "dosage": "500 mg Paracetamol + 50 mg Tramadol VO",
                        "route": "Oral",
                        "frequency": "A cada 8 horas se dor",
                        "dilutionInstructions": "Administrar por via oral com água após as refeições.",
                        "contraindications": "Insuficiência hepática severa ou histórico de dependência a opioides.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sb_spo",
                        "recommendationTitle": "Osteotomias de Smith-Petersen (SPO / Schwab Grau II) e Cages Lordóticos",
                        "dispositionTarget": "Centro Cirúrgico Especializado em Deformidade",
                        "monitoringPlan": "Controle fluoroscópico intraoperatório e monitorização neurofisiológica de PEM e PESS.",
                        "interventionalProcedure": "Necessidade de ganho de 10° a 20° de lordose lombar: realizar osteotomias posteriores tipo Smith-Petersen (SPO / Schwab Grau II) em múltiplos níveis (~5° a 10° por nível) e/ou implante de cages anteriores/oblíquos hiperlordóticos (ALIF ou OLIF de 15° a 20°).",
                    }
                ],
            },
            {
                "id": "tier_sb_severe_deformity",
                "label": "Desbalanço Sagital Grave / Rígido (Schwab ++)",
                "severityLevel": "critical",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Descompasso espinopélvico severo (PI - LL > 20°), retroversão pélvica grave (PT > 30°) ou colapso anterior marcante (SVA > 95 mm). Incapacidade funcional grave (ODI > 40-50%).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_sb_severe_abx",
                        "drugName": "Protocolo Antibiótico para Cirurgia Complexa",
                        "dosage": "Cefazolina 2g IV na indução + Vancomicina 1g IV",
                        "route": "Intravenosa",
                        "frequency": "Cirurgia longa de grande porte",
                        "dilutionInstructions": "Vancomicina diluída em 250 mL de SF 0,9% infundida em 60 a 90 min; Cefazolina em 100 mL de SF 0,9%.",
                        "contraindications": "Anafilaxia grave a glicopeptídeos ou betalactâmicos.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_sb_pso",
                        "recommendationTitle": "Indicação de Osteotomia de Subtração Pedicular (PSO / Schwab Grau III)",
                        "dispositionTarget": "Centro Cirúrgico de Alta Complexidade / UTI",
                        "monitoringPlan": "Monitorização contínua de potenciais evocados motores e somatossensoriais; teste de despertar (wake-up test) se perda de sinal.",
                        "interventionalProcedure": "Necessidade de ganho focal > 25° a 35° de lordose: indicação formal de Osteotomia de Subtração Pedicular (PSO / Schwab Grau III) em L3 ou L4 com ressecção em cunha do corpo vertebral e fechamento posterior associada a artrodese sacropélvica com parafusos ilíacos ou S2-Alar-Ilíacos (S2AI) para prevenir falha mecânica distal.",
                    }
                ],
            },
        ],
    }


def get_mjoa_nurick():
    """Escala mJOA e Classificação de Nurick para Mielopatia Cervical Espondilótica."""
    return {
        "id": "calc_mjoa_nurick",
        "slug": "mjoa-nurick",
        "name": "Escala mJOA e Classificação de Nurick para Mielopatia Cervical",
        "acronym": "mJOA / Nurick",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Cirurgia de Coluna e Medula",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Cirurgia de Coluna e Medula",
        "description": "Escalas funcionais padronizadas pela AOSpine para quantificar o comprometimento neurológico motor, sensitivo e esfincteriano na Mielopatia Cervical Espondilótica (CSM), associadas ao algoritmo do Diamante de Benzel para seleção da via cirúrgica (Anterior ACDF vs Posterior Laminoplastia/Artrodese).",
        "summary": "Quantificação funcional da mielopatia cervical (mJOA 0-18) e algoritmo do Diamante de Benzel para via cirúrgica.",
        "clinicalObjective": "Graduar a gravidade funcional da mielopatia cervical e direcionar a via de descompressão (anterior versus posterior).",
        "targetPopulation": "Pacientes com estenose do canal cervical degenerativo e sinais de mielopatia espondilótica (hiperreflexia, sinal de Hoffmann, Babinski, ataxia de marcha).",
        "calculationType": "additive_points",
        "formulaExpression": "mJOA: Pontos_MMSS_Motor + Pontos_MMII_Motor + Pontos_Sensitivo + Pontos_Esfincter (0 a 18) | Grau Nurick (0 a 5)",
        "evidenceSource": "Benzel EC. Spine surgery: techniques, complication avoidance, and management. 4th ed. Elsevier; 2017. Fehlings MG, Tetreault LA, Riew KD, et al. A Clinical Practice Guideline for the Management of Patients With Degenerative Cervical Myelopathy: Recommendations for Patients With Mild, Moderate, and Severe Disease and Nonmyelopathic Patients With Evidence of Cord Compression. Global Spine J. 2017;7(3 Suppl):70S-83S. Nurick S. The natural history and the results of surgical treatment of the spinal cord disorder associated with cervical spondylosis. Brain. 1972;95(1):101-108.",
        "minPossibleScore": 0,
        "maxPossibleScore": 18,
        "baseScore": 0,
        "badge": "coluna",
        "clinicalWarning": "DIRETRIZ DO DIAMANTE DE BENZEL & PROIBIÇÃO DE LAMINECTOMIA ISOLADA: (1) Se houver perda de lordose ou cifose cervical (< 10° de lordose), a via ANTERIOR (ACDF ou Corpectomia) é mandatória, pois a cifose estira a medula contra osteófitos ventrais e a laminectomia posterior falha por ausência de migração dorsal da medula; (2) A laminectomia descompressiva cervical isolada sem fixação instrumentada está FORMALMENTE PROSCRITA devido ao risco de deformidade secundária em pescoço de cisne (swan neck deformity) em mais de 40% dos casos.",
        "radarAxes": [
            {"id": "axis_mjoa_upper", "label": "Função Motora MMSS", "system": "Motor", "unit": "pts", "baselineValue": 5, "maxAxisValue": 5},
            {"id": "axis_mjoa_lower", "label": "Marcha e MMII", "system": "Motor", "unit": "pts", "baselineValue": 7, "maxAxisValue": 7},
            {"id": "axis_mjoa_sensory", "label": "Sensibilidade", "system": "Sensitivo", "unit": "pts", "baselineValue": 3, "maxAxisValue": 3},
            {"id": "axis_mjoa_sphincter", "label": "Controle Esfincteriano", "system": "Autonômico", "unit": "pts", "baselineValue": 3, "maxAxisValue": 3},
        ],
        "parameterGroups": [
            {
                "id": "grp_mjoa_upper",
                "name": "1. Função Motora dos Membros Superiores (mJOA)",
                "slug": "mmss-mjoa",
                "inputType": "single_choice",
                "radarAxisId": "axis_mjoa_upper",
                "normalBaselineValue": 5,
                "maxAxisValue": 5,
                "sortOrder": 1,
                "helpText": "Capacidade de preensão fina, abotoar camisa e alimentar-se com colher.",
                "options": [
                    {"id": "opt_mjoa_u0", "label": "0: Impossibilitado de mover as mãos ou de alimentar-se (0 pts)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Plegia ou paresia severa das mãos."},
                    {"id": "opt_mjoa_u1", "label": "1: Move os membros mas incapaz de alimentar-se com colher (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.8, "sortOrder": 2, "description": "Perda severa da motricidade fina."},
                    {"id": "opt_mjoa_u2", "label": "2: Come com colher com lentidão; incapaz de abotoar camisa (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.6, "sortOrder": 3, "description": "Déficit motor moderado a grave."},
                    {"id": "opt_mjoa_u3", "label": "3: Abotoa a camisa com grande dificuldade e lentidão evidente (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.4, "sortOrder": 4, "description": "Clara incoordenação das mãos (hand clumsiness)."},
                    {"id": "opt_mjoa_u4", "label": "4: Abotoa a camisa com discreta dificuldade motora fina (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 5, "description": "Lentificação mínima."},
                    {"id": "opt_mjoa_u5", "label": "5: Função motora fina e preensão completamente normais (5 pts)", "pointValue": 5, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 6, "description": "Sem déficits motores nos membros superiores."},
                ],
            },
            {
                "id": "grp_mjoa_lower",
                "name": "2. Função Motora dos Membros Inferiores / Marcha (mJOA)",
                "slug": "mmii-mjoa",
                "inputType": "single_choice",
                "radarAxisId": "axis_mjoa_lower",
                "normalBaselineValue": 7,
                "maxAxisValue": 7,
                "sortOrder": 2,
                "helpText": "Capacidade de deambulação e grau de ataxia/espasticidade de marcha.",
                "options": [
                    {"id": "opt_mjoa_l0", "label": "0: Perda motora e sensorial completa dos MMII (Plegia) (0 pts)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Plegia total dos membros inferiores."},
                    {"id": "opt_mjoa_l1", "label": "1: Incapaz de deambular mesmo com apoio / Leito ou cadeira (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.86, "sortOrder": 2, "description": "Incapacitado para ortostase."},
                    {"id": "opt_mjoa_l2", "label": "2: Deambula em piso plano apenas com auxílio (bengala/andador) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.71, "sortOrder": 3, "description": "Dependência de dispositivo ortopédico de apoio."},
                    {"id": "opt_mjoa_l3", "label": "3: Deambula no plano sem apoio, mas necessita de corrimão em escadas (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 0.57, "sortOrder": 4, "description": "Dificuldade para vencer desníveis."},
                    {"id": "opt_mjoa_l4", "label": "4: Deambula sem auxílio, mas com marcha lenta e apraxica (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.43, "sortOrder": 5, "description": "Marcha espástica / instável perceptível."},
                    {"id": "opt_mjoa_l5", "label": "5: Deambula sem auxílio, com marcha rígida ou instabilidade discreta (5 pts)", "pointValue": 5, "isNormalBaseline": False, "radarNormalizedValue": 0.29, "sortOrder": 6, "description": "Espasticidade leve."},
                    {"id": "opt_mjoa_l6", "label": "6: Velocidade normal, mas com fatigabilidade precoce ou hiperreflexia (6 pts)", "pointValue": 6, "isNormalBaseline": False, "radarNormalizedValue": 0.14, "sortOrder": 7, "description": "Clonus ou Babinski presentes sem impacto na velocidade."},
                    {"id": "opt_mjoa_l7", "label": "7: Marcha e função motora dos MMII completamente normais (7 pts)", "pointValue": 7, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 8, "description": "Sem queixas na deambulação."},
                ],
            },
            {
                "id": "grp_mjoa_sensory",
                "name": "3. Sensibilidade dos Membros Superiores (mJOA)",
                "slug": "sensitivo-mjoa",
                "inputType": "single_choice",
                "radarAxisId": "axis_mjoa_sensory",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 3,
                "helpText": "Parestesias, dormência em luva ou perda sensitiva tátil/dolorosa.",
                "options": [
                    {"id": "opt_mjoa_s0", "label": "0: Perda sensitiva completa nas mãos (0 pts)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Anestesia completa das mãos."},
                    {"id": "opt_mjoa_s1", "label": "1: Perda sensitiva severa ou dor incapacitante (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 2, "description": "Hipoestesia severa ou dor neuropática contínua."},
                    {"id": "opt_mjoa_s2", "label": "2: Perda sensitiva leve, parestesias ou dormência (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3, "description": "Dormência distal nos dedos sem perda grosseira."},
                    {"id": "opt_mjoa_s3", "label": "3: Sensibilidade tátil e dolorosa completamente normais (3 pts)", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 4, "description": "Sensibilidade íntegra."},
                ],
            },
            {
                "id": "grp_mjoa_sphincter",
                "name": "4. Função Esfincteriana / Miccional (mJOA)",
                "slug": "esfincter-mjoa",
                "inputType": "single_choice",
                "radarAxisId": "axis_mjoa_sphincter",
                "normalBaselineValue": 3,
                "maxAxisValue": 3,
                "sortOrder": 4,
                "helpText": "Controle esfincteriano vesical e retal.",
                "options": [
                    {"id": "opt_mjoa_m0", "label": "0: Retenção urinária completa ou incontinência total (0 pts)", "pointValue": 0, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 1, "description": "Necessidade de sonda vesical permanente ou perda contínua."},
                    {"id": "opt_mjoa_m1", "label": "1: Distúrbio severo (grande esforço, resíduo elevado, perda) (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 2, "description": "Disfunção autonômica vesical grave."},
                    {"id": "opt_mjoa_m2", "label": "2: Distúrbio leve (hesitação, urgência ou polaciúria sem perda) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 3, "description": "Alteração miccional precoce."},
                    {"id": "opt_mjoa_m3", "label": "3: Função miccional e controle esfincteriano normais (3 pts)", "pointValue": 3, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 4, "description": "Controle continente perfeito."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_mjoa_mild",
                "label": "Mielopatia Cervical Leve (mJOA 15 a 17)",
                "severityLevel": "low",
                "minScore": 15,
                "maxScore": 17,
                "statisticalOutcome": "Comprometimento neurológico leve sem incapacidade funcional importante nas AVDs.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mjoa_mild",
                        "drugName": "Manejo Clínico Conservador e Pregabalina se dor radicular",
                        "dosage": "Pregabalina 75 mg VO à noite se parestesias",
                        "route": "Oral",
                        "frequency": "24/24h",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_mjoa_mild",
                        "recommendationTitle": "Ensaio Conservador Estruturado ou Cirurgia Eletiva Precoce",
                        "dispositionTarget": "Ambulatório de Cirurgia de Coluna",
                        "monitoringPlan": "Reavaliação neurológica a cada 3 a 6 meses. Orientar procura imediata se piora da marcha ou perda de preensão manual.",
                        "interventionalProcedure": "Se progressão documentada de déficits: indicar descompressão cirúrgica eletiva.",
                    }
                ],
            },
            {
                "id": "tier_mjoa_mod",
                "label": "Mielopatia Cervical Moderada (mJOA 12 a 14)",
                "severityLevel": "intermediate",
                "minScore": 12,
                "maxScore": 14,
                "statisticalOutcome": "Disfunção funcional evidente que interfere nas atividades profissionais e cotidianas.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mjoa_mod",
                        "drugName": "Analgesia Otimizada e Cuidados Neuroprotetores",
                        "dosage": "Evitar manipulações cervicais ou quiropraxia",
                        "route": "Precaução clínica",
                        "frequency": "Contínua",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_mjoa_mod",
                        "recommendationTitle": "Indicação Formal de Descompressão Cirúrgica",
                        "dispositionTarget": "Centro Cirúrgico Eletivo",
                        "monitoringPlan": "Planejamento cirúrgico baseado no alinhamento sagital (Diamante de Benzel).",
                        "interventionalProcedure": "Se retificação ou cifose cervical: Via Anterior mandatória (ACDF ou Corpectomia com cage e placa); se lordose preservada (> 10°) e estenose multinível (>= 3 níveis): Via Posterior (Laminoplastia open-door ou Laminectomia com fixação em massa lateral C3-C6).",
                    }
                ],
            },
            {
                "id": "tier_mjoa_severe",
                "label": "Mielopatia Cervical Grave (mJOA 0 a 11)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 11,
                "statisticalOutcome": "Comprometimento neurológico grave com alto risco de perda irreversível da deambulação e tetraplegia.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_mjoa_sev_abx",
                        "drugName": "Cefazolina 2g IV Perioperatória",
                        "dosage": "2g IV na indução cirúrgica",
                        "route": "Intravenosa",
                        "frequency": "Indução",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_mjoa_severe",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória e Prioritária",
                        "dispositionTarget": "Centro Cirúrgico de Urgência Eletiva",
                        "monitoringPlan": "Monitorização neurofisiológica intraoperatória de PEM e PESS contínuos.",
                        "interventionalProcedure": "Descompressão cirúrgica urgente: restauração da lordose e liberação circunferencial medular. ACDF multinível ou Corpectomia associada à fixação posterior se canal estreito severo e OPLL.",
                    }
                ],
            },
        ],
    }
