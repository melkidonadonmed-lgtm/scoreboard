"""
Block 03: Module A - Neurotrauma & Neurointensivismo
1. Rotterdam Score (TCE, 1-6 pts)
2. Marshall CT Classification (TCE, I-VI)
3. Glasgow-P (ECG-P / GCS-Pupils, 1-15 pts)
4. EDEMA Score (Malignant MCA Stroke, 0-13 pts)
5. CRASH Trial Score (TBI Prognosis & Mortality, 0-10 pts)
6. IMPACT Score (TBI Multidimensional Models, 0-12 pts)
7. Escala ASIA / AIS (Trauma Raquimedular ISNCSCI, A-E)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL

# Import existing implementations
from calculators.block03_neuro.neurotrauma import (
    get_rotterdam,
    get_marshall,
    get_asia_ais,
)
from calculators.mod3_coma import get_glasgow_p


def get_edema():
    """Enhanced Detection of Edema in Malignant Anterior Circulation Stroke Score (Ong 2017)."""
    return {
        "id": "calc_edema",
        "slug": "edema-score",
        "name": "EDEMA Score para Craniectomia no AVCi Maligno",
        "acronym": "EDEMA",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Neurointensivismo",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurotrauma e Neurointensivismo",
        "description": "Escore tomográfico e clínico preditor de edema citotóxico maligno com herniação transtentorial nas primeiras 24h de infarto extenso da artéria cerebral média (ACM), orientando a indicação precoce de craniectomia descompressiva.",
        "summary": "Predição precoce de edema cerebral maligno expansivo após infarto extenso de ACM (0 a 13 pontos).",
        "clinicalObjective": "Identificar nas primeiras 24 horas do ictus isquêmico os pacientes com infarto maligno de ACM que desenvolverão herniação uncal fatal sob manejo conservador, definindo o timing cirúrgico descompressivo ideal.",
        "targetPopulation": "Pacientes com AVC isquêmico extenso de circulação anterior (território de ACM > 50%) admitidos em unidade neurovascular ou UTI neurocrítica.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_MLS + Pontos_Cisternas + Pontos_Glicemia + Pontos_Reperfusao",
        "evidenceSource": "Ong CJ, Gluckstein J, Laurido-Soto O, et al. Enhanced Detection of Edema in Malignant Anterior Circulation Stroke (EDEMA) Score. Stroke. 2017;48(7):1969-1972.",
        "minPossibleScore": 0,
        "maxPossibleScore": 13,
        "baseScore": 0,
        "badge": "neuroemergencia",
        "clinicalWarning": "ALERTA CIRÚRGICO: Pacientes com EDEMA Score >= 7 pontos apresentam probabilidade superior a 70-80% de herniação transtentorial fatal sob tratamento clínico conservador exclusivo. A craniectomia descompressiva hemicraniana precoce (< 24 a 48 horas) reduz a mortalidade de 70-80% para menos de 20-30% (ensaios DECIMAL, DESTINY e HAMLET).",
        "radarAxes": [
            {"id": "axis_edema_mls", "label": "Desvio de Linha Média", "system": "Neurológico", "unit": "mm", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_edema_cisterns", "label": "Cisternas Basais", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_edema_metabolic", "label": "Glicemia e Metabolismo", "system": "Metabólico", "unit": "mg/dL", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_edema_reperfusion", "label": "Status de Reperfusão", "system": "Vascular", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_edema_mls",
                "name": "1. Desvio da Linha Média (MLS na TC)",
                "slug": "desvio-linha-media-edema",
                "inputType": "single_choice",
                "radarAxisId": "axis_edema_mls",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Desvio do septo pelúcido medido no plano axial da TC em 24h ou inicial.",
                "options": [
                    {"id": "opt_edema_mls_0", "label": "Sem desvio de linha média (0 mm)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Estruturas da linha média estritamente centradas."},
                    {"id": "opt_edema_mls_1", "label": "Desvio > 0 a 3 mm (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.2, "sortOrder": 2, "description": "Desvio discreto das estruturas medianas."},
                    {"id": "opt_edema_mls_2", "label": "Desvio > 3 a 6 mm (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.45, "sortOrder": 3, "description": "Desvio moderado com compressão ventricular ipsilateral."},
                    {"id": "opt_edema_mls_4", "label": "Desvio > 6 a 9 mm (4 pts)", "pointValue": 4, "isNormalBaseline": False, "radarNormalizedValue": 0.75, "sortOrder": 4, "description": "Desvio importante com colapso do ventrículo lateral ipsilateral."},
                    {"id": "opt_edema_mls_7", "label": "Desvio > 9 mm (7 pts)", "pointValue": 7, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 5, "description": "Desvio crítico severo com alto risco de herniação subfalcina e uncal."},
                ],
            },
            {
                "id": "grp_edema_cisterns",
                "name": "2. Apagamento das Cisternas Basais",
                "slug": "cisternas-basais-edema",
                "inputType": "single_choice",
                "radarAxisId": "axis_edema_cisterns",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Avaliação das cisternas perimesencefálicas (ambiens, interpeduncular e quadrigeminal).",
                "options": [
                    {"id": "opt_edema_cisterns_open", "label": "Cisternas preservadas e patentes (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Espaço liquórico perimesencefálico amplo e simétrico."},
                    {"id": "opt_edema_cisterns_closed", "label": "Obliteração parcial ou completa das cisternas (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Compressão severa ou apagamento total das cisternas perimesencefálicas."},
                ],
            },
            {
                "id": "grp_edema_glucose",
                "name": "3. Glicemia Admissional",
                "slug": "glicemia-admissional-edema",
                "inputType": "single_choice",
                "radarAxisId": "axis_edema_metabolic",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Glicemia plasmática sérica na admissão na emergência.",
                "options": [
                    {"id": "opt_edema_glu_normal", "label": "Glicemia <= 150 mg/dL (<= 8,3 mmol/L) (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Controle glicêmico fisiológico admissional."},
                    {"id": "opt_edema_glu_high", "label": "Glicemia > 150 mg/dL (> 8,3 mmol/L) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Hiperglicemia aguda: amplifica estresse oxidativo e permeabilidade endotelial."},
                ],
            },
            {
                "id": "grp_edema_reperfusion",
                "name": "4. Terapia de Reperfusão Prévia",
                "slug": "terapia-de-reperfusao-edema",
                "inputType": "single_choice",
                "radarAxisId": "axis_edema_reperfusion",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Realização de trombólise endovenosa (rt-PA/TNK) e/ou trombectomia mecânica.",
                "options": [
                    {"id": "opt_edema_rep_yes", "label": "Reperfusão realizada com sucesso (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Paciente submetido a trombólise química e/ou recanalização endovascular."},
                    {"id": "opt_edema_rep_no", "label": "Nenhuma terapia de reperfusão realizada (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Sem recanalização arterial; persistência de oclusão de grande vaso."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_edema_low",
                "label": "Baixo Risco de Edema Maligno (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Probabilidade de evolução para edema cerebral maligno fatal < 10%. Mortalidade hospitalar global < 10-15%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edema_antiplatelet",
                        "drugName": "Ácido Acetilsalicílico (AAS)",
                        "dosage": "100 a 300 mg VO uma vez ao dia",
                        "route": "Oral / Sonda",
                        "frequency": "24/24h",
                        "dilutionInstructions": "Administrar 24h após trombólise se realizada.",
                        "contraindications": "Transformação hemorrágica sintomática na TC de controle.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_edema_low",
                        "recommendationTitle": "Tratamento Conservador Seguro em Unidade Neurovascular",
                        "dispositionTarget": "Unidade de AVC",
                        "monitoringPlan": "Exame neurológico seriado com NIHSS a cada 4 horas. Cabeceira elevada a 30 graus, alinhamento cervical neutro. TC de crânio de controle em 24h.",
                        "interventionalProcedure": "Tratamento cirúrgico conservador de escolha.",
                    }
                ],
            },
            {
                "id": "tier_edema_mod",
                "label": "Risco Intermediário de Edema Maligno (4 a 6 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 6,
                "statisticalOutcome": "Risco de desenvolvimento de edema expansivo com efeito de massa de 20% a 50%. Mortalidade estimada em ~30-40%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edema_saline3",
                        "drugName": "Solução Salina Hipertônica 3%",
                        "dosage": "Infusão contínua em BIC na vazão de 0,5 a 1,5 mL/kg/h",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Solução pura de NaCl 3%. Meta de natremia sérica: 145 a 155 mEq/L e osmolaridade sérica < 320 mOsm/L.",
                        "contraindications": "Edema agudo de pulmão grave, hipernatremia > 160 mEq/L.",
                    },
                    {
                        "id": "rx_edema_norepi",
                        "drugName": "Noradrenalina (Hemitartarato)",
                        "dosage": "0,05 a 2,0 mcg/kg/min em BIC contínua",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua titulada",
                        "dilutionInstructions": "16 mg em 234 mL SG 5% (64 mcg/mL). Manter PAM >= 85-90 mmHg para assegurar PPC entre 60 e 70 mmHg.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_edema_mod",
                        "recommendationTitle": "Caso Limítrofe / Monitorização Neurocrítica Avançada",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Linha arterial contínua (PAI), avaliação pupilar a cada 1 hora. Notificar equipe neurocirúrgica de sobreaviso para reserva de bloco operatório.",
                        "interventionalProcedure": "Preparo pré-operatório para eventual craniectomia descompressiva de resgate perante deterioração clínica (queda de 2 pts no Glasgow ou sonolência progressiva).",
                    }
                ],
            },
            {
                "id": "tier_edema_high",
                "label": "Alto a Muito Alto Risco de Herniação (7 a 13 pontos)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 13,
                "statisticalOutcome": "Risco de evolução para herniação uncal, parada de tronco e óbito superior a 60% a 80% sob tratamento conservador. Mortalidade cirúrgica pós-craniectomia precoce < 25-30%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_edema_saline_bolus",
                        "drugName": "Salina Hipertônica a 3% (Bolus de Resgate)",
                        "dosage": "Bolus de 150 a 250 mL IV infundidos em 15 a 20 minutos",
                        "route": "Acesso Central ou periférico calibroso",
                        "frequency": "Bolus de resgate",
                        "dilutionInstructions": "Administrar imediatamente perante assimetria pupilar ou bradicardia hipertensiva (reflexo de Cushing) durante a transição para o bloco cirúrgico.",
                    },
                    {
                        "id": "rx_edema_propofol",
                        "drugName": "Propofol 1% Sedoanalgesia",
                        "dosage": "1 a 4 mg/kg/h em infusão contínua em BIC",
                        "route": "Intravenosa",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Propofol puro em bomba de seringa ou frasco exclusivo. Associar a Fentanil (1 a 3 mcg/kg/h).",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_edema_high",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: Craniectomia Descompressiva Hemicraniana Ampla",
                        "dispositionTarget": "Centro Cirúrgico de Emergência",
                        "monitoringPlan": "Monitorização de PIC intraparenquimatosa pós-operatória. Manter meta de PPC >= 60-70 mmHg.",
                        "interventionalProcedure": "Craniectomia Descompressiva Fronto-têmporo-parietal unilateral ampla (incisão em ponto de interrogação invertido, diâmetro anteroposterior >= 12 a 15 cm com ressecção óssea estendida até o assoalho da fossa média e duroplastia de expansão circunferencial com enxerto autólogo de pericrânio ou fáscia lata). Timing ideal: primeiras 24 a 48h.",
                        "ventilatorySupport": "Intubação orotraqueal com ventilação protetora (PaCO2 35-40 mmHg, tolerar 30-35 mmHg transitoriamente durante crise de herniação).",
                    }
                ],
            },
        ],
    }


def get_crash_tbi():
    """MRC CRASH Trial Prognostic Model para TCE (Lancet 2008)."""
    return {
        "id": "calc_crash_tbi",
        "slug": "crash-tbi",
        "name": "CRASH Trial Score para Prognóstico no TCE",
        "acronym": "CRASH TBI",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Neurointensivismo",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurotrauma e Neurointensivismo",
        "description": "Modelo preditivo validado internacionalmente em mais de 10.000 pacientes para estimativa da mortalidade em 14 dias e desfecho funcional desfavorável aos 6 meses no traumatismo cranioencefálico agudo.",
        "summary": "Predição quantitativa de mortalidade aos 14 dias e desfecho funcional aos 6 meses no TCE (0 a 10 pontos).",
        "clinicalObjective": "Quantificar a gravidade global e fornecer estimativas prognósticas calibradas para direcionar suporte intensivo e decisões cirúrgicas em até 8 horas do TCE contuso.",
        "targetPopulation": "Pacientes adultos avaliados em até 8 horas do TCE não-penetrante com Escala de Glasgow total <= 14.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Idade + Pontos_Pais + Pontos_GCS + Pontos_Pupilas + Pontos_Extracraniana + Pontos_Achados_TC",
        "evidenceSource": "MRC CRASH Trial Collaborators. Predicting outcome after head injury: practical prognostic models based on large cohort of international patients. BMJ. 2008;336(7641):425-429. Lancet. 2004;364(9442):1321-1328.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "neurotrauma",
        "clinicalWarning": "ALERTA PRETO DE SEGURANÇA MANDATÓRIO (ENSAIO CRASH): O uso de corticosteroides (Metilprednisolona ou Dexametasona) é TERMINANTEMENTE PROIBIDO no TCE agudo. O ensaio clínico internacional MRC CRASH comprovou de forma inequívoca que a corticoterapia acarreta aumento absoluto significativo da mortalidade intra-hospitalar (OR 1,22; p=0,0001).",
        "radarAxes": [
            {"id": "axis_crash_clinical", "label": "Estado Neurológico / Coma", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_crash_pupil", "label": "Reatividade Pupilar", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_crash_systemic", "label": "Trauma Extracraniano", "system": "Trauma", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_crash_imaging", "label": "Lesões Tomográficas", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_crash_age",
                "name": "1. Faixa Etária do Paciente",
                "slug": "idade-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_clinical",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Idade cronológica do paciente no momento do trauma.",
                "options": [
                    {"id": "opt_crash_age_young", "label": "Idade < 40 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Maior reserva fisiológica neuronal e tolerância tecidual."},
                    {"id": "opt_crash_age_mid", "label": "Idade de 40 a 59 anos (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Reserva intermediária."},
                    {"id": "opt_crash_age_old", "label": "Idade >= 60 anos (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Idoso: maior rigidez cerebral, risco de atrofia e comorbidades sistêmicas."},
                ],
            },
            {
                "id": "grp_crash_country",
                "name": "2. Nível de Recursos do País / Centro",
                "slug": "recursos-pais-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_systemic",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Infraestrutura de atendimento neurointensivo e cirúrgico disponível.",
                "options": [
                    {"id": "opt_crash_country_high", "label": "País de Alta Renda / Centro Terciário Avançado (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Acesso imediato a TC, UTI neurocrítica e neurocirurgia 24h."},
                    {"id": "opt_crash_country_low", "label": "País de Baixa/Média Renda ou Centro Secundário (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Dificuldades de transferência e recursos de neurointensivismo limitados."},
                ],
            },
            {
                "id": "grp_crash_gcs",
                "name": "3. Escala de Coma de Glasgow Admissional",
                "slug": "glasgow-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_clinical",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Escore total de Glasgow avaliado após ressuscitação hemodinâmica.",
                "options": [
                    {"id": "opt_crash_gcs_mild", "label": "Glasgow 13 a 14: TCE Leve a Moderado (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Paciente vigil ou com sonolência discreta."},
                    {"id": "opt_crash_gcs_mod", "label": "Glasgow 9 a 12: TCE Moderado (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Estupor ou confusão mental importante."},
                    {"id": "opt_crash_gcs_severe", "label": "Glasgow 3 a 8: TCE Grave / Coma (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Coma profundo; requer via aérea definitiva imediata."},
                ],
            },
            {
                "id": "grp_crash_pupils",
                "name": "4. Reatividade Pupilar à Luz",
                "slug": "pupilas-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_pupil",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Avaliação do reflexo fotomotor direto e consensual bilateral.",
                "options": [
                    {"id": "opt_crash_pupils_both", "label": "Ambas as pupilas reagem à luz (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Tronco encefálico íntegro; ausência de compressão do III par."},
                    {"id": "opt_crash_pupils_one", "label": "Apenas uma pupila reage (Anisocoria) (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Alerta iminente de herniação uncal unilateral."},
                    {"id": "opt_crash_pupils_none", "label": "Nenhuma pupila reage (Midríase Fixa Bilateral) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Dano grave de mesencéfalo ou herniação transtentorial bilateral."},
                ],
            },
            {
                "id": "grp_crash_extra",
                "name": "5. Grande Lesão Extracraniana Associada",
                "slug": "lesao-extracraniana-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_systemic",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Politrauma: fraturas de ossos longos, trauma torácico ou abdominal com choque.",
                "options": [
                    {"id": "opt_crash_extra_no", "label": "Ausente: Trauma Craniano Isolado (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Sem lesões extracranianas de grande porte."},
                    {"id": "opt_crash_extra_yes", "label": "Presente: Politraumatizado Grave (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Lesão associada grave com choque hipotensivo ou coagulopatia."},
                ],
            },
            {
                "id": "grp_crash_ct",
                "name": "6. Achados Tomográficos Anormais no Crânio",
                "slug": "tc-anormal-crash",
                "inputType": "single_choice",
                "radarAxisId": "axis_crash_imaging",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "helpText": "Presença de petéquias, cisternas obliteradas, tHSA ou desvio > 5 mm na TC.",
                "options": [
                    {"id": "opt_crash_ct_normal", "label": "TC Normal ou Lesões Mínimas sem Efeito de Massa (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Cisternas abertas, sem desvio significativo."},
                    {"id": "opt_crash_ct_abnormal", "label": "TC com Patologia Grave (Cisternas apagadas, tHSA ou DLM > 5 mm) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 2, "description": "Lesão estrutural relevante com risco elevado de HIC."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_crash_low",
                "label": "Baixo Risco Previsto (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade estimada em 14 dias < 10%. Risco de desfecho desfavorável aos 6 meses < 25%. Taxa de recuperação funcional independente > 75%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_crash_keppra_low",
                        "drugName": "Levetiracetam (Profilaxia Anticonvulsivante Precoce)",
                        "dosage": "1.000 mg IV ataque em 15 min, seguido de 500 a 1.000 mg 12/12h por 7 dias",
                        "route": "Intravenosa",
                        "frequency": "12/12h",
                        "dilutionInstructions": "Diluir 1.000 mg em 100 mL de SF 0,9%. Infundir em 15 minutos.",
                        "contraindications": "Hipersensibilidade ao fármaco.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_crash_low",
                        "recommendationTitle": "Tratamento Conservador Seguro / Vigilância Semi-Intensiva",
                        "dispositionTarget": "Semi-Intensiva",
                        "monitoringPlan": "Exame neurológico a cada 2 horas por 24 horas. TC de controle se surgimento de cefaleia persistente ou vômitos.",
                        "interventionalProcedure": "Tratamento cirúrgico não indicado no momento.",
                    }
                ],
            },
            {
                "id": "tier_crash_mod",
                "label": "Risco Intermediário (4 a 6 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 6,
                "statisticalOutcome": "Mortalidade em 14 dias entre 10% e 30%. Probabilidade de desfecho desfavorável aos 6 meses de 25% a 50%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_crash_norepi_mod",
                        "drugName": "Noradrenalina IV Titulada",
                        "dosage": "0,05 a 2,0 mcg/kg/min em BIC contínua",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "16 mg em 234 mL SG 5% (64 mcg/mL). Manter PAM que garanta PPC entre 60 e 70 mmHg.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    },
                    {
                        "id": "rx_crash_saline_mod",
                        "drugName": "Salina Hipertônica a 3%",
                        "dosage": "Bolus de 150 a 250 mL IV se pico agudo de PIC > 22 mmHg",
                        "route": "Acesso Central",
                        "frequency": "Resgate",
                        "dilutionInstructions": "Infundir em 15 a 20 minutos sob monitorização contínua.",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_crash_mod",
                        "recommendationTitle": "Caso Limítrofe / Manejo Neurointensivo em UTI Neurocrítica",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Indicação formal de cateter de PIC intraparenquimatoso ou DVE se Glasgow <= 8. Linha arterial (PAI).",
                        "interventionalProcedure": "Avaliação neurocirúrgica para monitorização invasiva de PIC e preparo cirúrgico de retaguarda.",
                        "ventilatorySupport": "Intubação orotraqueal em sequência rápida se Glasgow <= 8. Ventilação protetora com PaCO2 35-40 mmHg.",
                    }
                ],
            },
            {
                "id": "tier_crash_high",
                "label": "Alto Risco de Mortalidade e Sequelas Graves (7 a 10 pontos)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 10,
                "statisticalOutcome": "Mortalidade em 14 dias > 30% a 50%. Probabilidade acumulada de óbito ou dependência irreversível (GOS 1-3) superior a 60% a 80%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_crash_saline3_high",
                        "drugName": "Osmoterapia Otimizada com Salina Hipertônica 3%",
                        "dosage": "250 mL IV bolus em 15 min + infusão contínua em BIC 1 mL/kg/h",
                        "route": "Acesso Central",
                        "frequency": "Contínua / Resgate",
                        "dilutionInstructions": "Meta de sódio sérico alvo entre 145 e 155 mEq/L. Osmolaridade sérica limite < 320 mOsm/L.",
                    },
                    {
                        "id": "rx_crash_sedation_high",
                        "drugName": "Sedoanalgesia Contínua Profunda",
                        "dosage": "Fentanil 1 a 3 mcg/kg/h + Midazolam 0,05 a 0,2 mg/kg/h ou Propofol",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua",
                        "dilutionInstructions": "Visar sedação profunda (RASS -4 a -5) para evitar picos de PIC associados a tosse e assincronia.",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_crash_high",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória / Escalonamento para Tier 2 e 3 da BTF",
                        "dispositionTarget": "Centro Cirúrgico de Urgência",
                        "monitoringPlan": "Monitorização multimodal de PIC, SjvO2 (55-75%) e PbtO2 (> 20 mmHg).",
                        "interventionalProcedure": "Craniotomia osteoplástica para evacuação de hematomas volumosos (> 25 mL) ou Craniectomia Descompressiva Ampla (frontotemporoparietal unilateral >= 12-15 cm ou bifrontal) com duroplastia de expansão se edema cerebral difuso refratário a medidas clínicas.",
                        "ventilatorySupport": "Ventilação mecânica invasiva obrigatória com metas rigorosas de normocapnia.",
                    }
                ],
            },
        ],
    }


def get_impact_tbi():
    """IMPACT Prognostic Calculator (Steyerberg 2008)."""
    return {
        "id": "calc_impact_tbi",
        "slug": "impact-tbi",
        "name": "IMPACT Score para Prognóstico no TCE",
        "acronym": "IMPACT TBI",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurotrauma e Neurointensivismo",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Neurotrauma e Neurointensivismo",
        "description": "Calculadora prognóstica de alta discriminação internacional baseada em 11 estudos e 8.500 pacientes com TCE moderado a grave, operando em três camadas progressivas (Core, Extended e Lab/CT) para predição de mortalidade aos 6 meses.",
        "summary": "Predição prognóstica multimodal em 3 camadas (Core, Extended, Lab/CT) para TCE moderado a grave (0 a 12 pontos).",
        "clinicalObjective": "Estimar com precisão a probabilidade de mortalidade aos 6 meses e o prognóstico funcional desfavorável (GOS 1-3) no TCE com Glasgow <= 12.",
        "targetPopulation": "Pacientes admitidos com TCE moderado a grave (Glasgow <= 12) avaliados nas primeiras 24 horas pós-trauma.",
        "calculationType": "additive_points",
        "formulaExpression": "Pontos_Idade + Pontos_Motor + Pontos_Pupilas + Pontos_Hipoxia_Hipotensao + Pontos_TC_Lab",
        "evidenceSource": "Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic brain injury: development and international validation of prognostic scores based on admission characteristics. PLoS Med. 2008;5(8):e165.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "neurotrauma",
        "clinicalWarning": "ATENÇÃO: A presença de Hematoma Epidural (HED) no modelo IMPACT apresenta Odds Ratio favorável / efeito protetor relativo no prognóstico de longo prazo, pois constitui lesão focal de descompressão cirúrgica curativa sem o dano axonal difuso das contusões bilaterais. Manter Pressão de Perfusão Cerebral (PPC = PAM - PIC) estritamente entre 60 e 70 mmHg.",
        "radarAxes": [
            {"id": "axis_impact_core", "label": "IMPACT Core (Idade/Motor)", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_impact_pupil", "label": "Reatividade Pupilar", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_impact_secondary", "label": "Insultos Secundários (PA/O2)", "system": "Hemodinâmico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
            {"id": "axis_impact_ct_lab", "label": "TC e Laboratório", "system": "Neurológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
        ],
        "parameterGroups": [
            {
                "id": "grp_impact_age",
                "name": "1. Idade Cronológica (Core)",
                "slug": "idade-impact",
                "inputType": "single_choice",
                "radarAxisId": "axis_impact_core",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Idade do paciente no momento do trauma.",
                "options": [
                    {"id": "opt_impact_age_lt30", "label": "Idade < 30 anos (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Alta plasticidade neuronal e reserva cardiovascular."},
                    {"id": "opt_impact_age_30_49", "label": "Idade 30 a 49 anos (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Reserva fisiológica preservada."},
                    {"id": "opt_impact_age_50_69", "label": "Idade 50 a 69 anos (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3, "description": "Reserva intermediária a diminuída."},
                    {"id": "opt_impact_age_ge70", "label": "Idade >= 70 anos (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Idoso: alta vulnerabilidade a insultos secundários."},
                ],
            },
            {
                "id": "grp_impact_motor",
                "name": "2. Escore Motor da Escala de Glasgow (Core)",
                "slug": "motor-impact",
                "inputType": "single_choice",
                "radarAxisId": "axis_impact_core",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Melhor resposta motora (M) da Escala de Coma de Glasgow.",
                "options": [
                    {"id": "opt_impact_mot_5_6", "label": "Obedece a comandos (M6) ou Localiza dor (M5) (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Função corticoespinhal motora bem preservada."},
                    {"id": "opt_impact_mot_4", "label": "Flexão inespecífica / Retirada à dor (M4) (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.33, "sortOrder": 2, "description": "Disfunção corticossubcortical moderada."},
                    {"id": "opt_impact_mot_3", "label": "Flexão anormal / Decorticação (M3) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 0.67, "sortOrder": 3, "description": "Comprometimento diencefálico / mesencefálico alto."},
                    {"id": "opt_impact_mot_1_2", "label": "Extensão anormal (M2) ou Nenhuma resposta (M1) (3 pts)", "pointValue": 3, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 4, "description": "Comprometimento grave de ponte e mesencéfalo."},
                ],
            },
            {
                "id": "grp_impact_pupils",
                "name": "3. Reatividade Pupilar à Luz (Core)",
                "slug": "pupilas-impact",
                "inputType": "single_choice",
                "radarAxisId": "axis_impact_pupil",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Reflexo fotomotor pupilar bilateral avaliado com lanterna.",
                "options": [
                    {"id": "opt_impact_pup_both", "label": "Ambas as pupilas reativas (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Reflexos de tronco íntegros."},
                    {"id": "opt_impact_pup_one", "label": "Uma pupila reativa / Anisocoria (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Compressão iminente do nervo oculomotor (III par)."},
                    {"id": "opt_impact_pup_none", "label": "Nenhuma pupila reativa / Midríase Fixa Bilateral (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Lesão grave do tronco encefálico."},
                ],
            },
            {
                "id": "grp_impact_secondary",
                "name": "4. Insultos Fisiológicos Secundários (Extended)",
                "slug": "insultos-secundarios-impact",
                "inputType": "single_choice",
                "radarAxisId": "axis_impact_secondary",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Episódio documentado de Hipóxia (SpO2 < 90% ou PaO2 < 60) ou Hipotensão (PAS < 90 mmHg).",
                "options": [
                    {"id": "opt_impact_sec_none", "label": "Ausentes: Sem hipóxia e sem hipotensão (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Estabilidade cardiorrespiratória preservada."},
                    {"id": "opt_impact_sec_one", "label": "Presente UM episódio de hipóxia OU hipotensão (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Insulto secundário precoce com isquemia tecidual cerebral."},
                    {"id": "opt_impact_sec_both", "label": "Presentes AMBOS (Hipóxia E Hipotensão) (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Combinação tóxica: duplica mortalidade e necrose neuronal secundária."},
                ],
            },
            {
                "id": "grp_impact_ct_lab",
                "name": "5. Tomografia e Laboratório Admissional (Lab/CT)",
                "slug": "tomografia-lab-impact",
                "inputType": "single_choice",
                "radarAxisId": "axis_impact_ct_lab",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Classificação tomográfica (Marshall III/IV ou tHSA sem HED) e parâmetros laboratoriais.",
                "options": [
                    {"id": "opt_impact_lab_good", "label": "Marshall I-II ou HED presente isolado (0 pts)", "pointValue": 0, "isNormalBaseline": True, "radarNormalizedValue": 0.0, "sortOrder": 1, "description": "Tomografia favorável ou hematoma epidural focal sem lesão difusa."},
                    {"id": "opt_impact_lab_mod", "label": "Marshall III-IV OU tHSA presente (1 pt)", "pointValue": 1, "isNormalBaseline": False, "radarNormalizedValue": 0.5, "sortOrder": 2, "description": "Edema difuso com cisternas comprimidas ou sangramento subaracnóideo."},
                    {"id": "opt_impact_lab_severe", "label": "Marshall III-IV E tHSA sem HED, ou Glicemia > 180 / Hb < 10 (2 pts)", "pointValue": 2, "isNormalBaseline": False, "radarNormalizedValue": 1.0, "sortOrder": 3, "description": "Lesão axonal difusa severa associada a distúrbios metabólicos críticos."},
                ],
            },
        ],
        "riskTiers": [
            {
                "id": "tier_impact_low",
                "label": "Baixo Risco Previsto (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade estimada em 6 meses < 20%. Risco de desfecho desfavorável (GOS 1-3) < 35%. Independência funcional em 6 meses > 65%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_impact_keppra",
                        "drugName": "Levetiracetam IV",
                        "dosage": "1.000 mg ataque em 15 min, seguido de 500 mg 12/12h por 7 dias",
                        "route": "Intravenosa",
                        "frequency": "12/12h",
                        "dilutionInstructions": "100 mL SF 0,9% em 15 min.",
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_impact_low",
                        "recommendationTitle": "Tratamento Conservador Seguro com Suporte Semi-Intensivo",
                        "dispositionTarget": "Semi-Intensiva",
                        "monitoringPlan": "Monitorização de sinais vitais, Glasgow horário nas primeiras 24 horas. Evitar episódios hipotensivos (PAS < 100 mmHg).",
                        "interventionalProcedure": "Cirurgia não indicada no momento.",
                    }
                ],
            },
            {
                "id": "tier_impact_mod",
                "label": "Risco Intermediário (4 a 7 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 7,
                "statisticalOutcome": "Mortalidade estimada em 6 meses entre 20% e 50%. Risco de desfecho desfavorável de 35% a 60%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_impact_norepi_mod",
                        "drugName": "Noradrenalina em BIC Contínua",
                        "dosage": "0,05 a 2,0 mcg/kg/min",
                        "route": "Acesso Venoso Central",
                        "frequency": "Contínua",
                        "dilutionInstructions": "16 mg em 234 mL SG 5% (64 mcg/mL). Manter PAM que garanta PPC entre 60 e 70 mmHg.",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL,
                    },
                    {
                        "id": "rx_impact_saline_mod",
                        "drugName": "Solução Salina Hipertônica 3%",
                        "dosage": "Bolus de 150 a 250 mL IV em 15-20 min",
                        "route": "Acesso Central",
                        "frequency": "Resgate",
                        "dilutionInstructions": "Infundir se PIC > 22 mmHg sustentada por mais de 5 minutos.",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_impact_mod",
                        "recommendationTitle": "Caso Limítrofe / Manejo Neurocrítico Multimodal em UTI",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Sensor de PIC intraparenquimatoso ou DVE. Manter PAM e PPC entre 60 e 70 mmHg. Saturação venosa jugular SjvO2 entre 55% e 75%.",
                        "interventionalProcedure": "Avaliação neurocirúrgica para monitorização invasiva e planejamento de descompressão se falência clínica.",
                    }
                ],
            },
            {
                "id": "tier_impact_high",
                "label": "Alto Risco de Mortalidade e Sequelas Graves (8 a 12 pontos)",
                "severityLevel": "critical",
                "minScore": 8,
                "maxScore": 12,
                "statisticalOutcome": "Mortalidade em 6 meses > 50%. Probabilidade de dependência funcional grave irreversível ou estado vegetativo (GOS 1-3) superior a 70% a 85%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_impact_osm_high",
                        "drugName": "Osmoterapia Otimizada (Salina 3% ou Manitol 20%)",
                        "dosage": "Salina 3% 250 mL bolus ou Manitol 20% 0,5 a 1,0 g/kg em 20 min",
                        "route": "Acesso Central",
                        "frequency": "Resgate / BIC",
                        "dilutionInstructions": "Manitol contraindicado se hipotensão (PAS < 90) ou osmolaridade > 320 mOsm/L. Manter sódio 145-155 mEq/L.",
                    },
                    {
                        "id": "rx_impact_barb",
                        "drugName": "Coma Barbitúrico com Tiopental Sódico (Tier 3 BTF)",
                        "dosage": "Ataque de 2 a 5 mg/kg IV lento em 30 min, manutenção de 1 a 5 mg/kg/h",
                        "route": "Acesso Central exclusivo",
                        "frequency": "Contínua sob EEG",
                        "dilutionInstructions": "Titulado sob monitorização eletroencefalográfica contínua visando padrão de surto-supressão (1 surto a cada 10-20 segundos). Suporte vasopressor agressivo com Noradrenalina obrigatório pelo risco de colapso miocárdico.",
                    },
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "non_impact_high",
                        "recommendationTitle": "Indicação Cirúrgica Mandatória: Craniectomia Descompressiva de Resgate",
                        "dispositionTarget": "Centro Cirúrgico de Urgência",
                        "monitoringPlan": "Monitorização neurointensiva contínua de PIC, PAI, PbtO2 (> 20 mmHg) e EEG contínuo.",
                        "interventionalProcedure": "Craniectomia Descompressiva Ampla frontotemporoparietal (>= 12-15 cm) com duroplastia de expansão para alívio imediato do edema refratário e prevenção de herniação irreversível de tronco encefálico.",
                        "ventilatorySupport": "Ventilação mecânica protetora invasiva obrigatória.",
                    }
                ],
            },
        ],
    }
