"""
Block 04: Pneumologia e Vias Aéreas (8 Calculadoras Monográficas Completas)
1. CURB-65 — Gravidade na PAC (calc_curb65)
2. CRB-65 — PAC sem Laboratório / Atenção Primária (calc_crb65)
3. PSI / PORT Score — Pneumonia Severity Index (calc_psi_port)
4. SMART-COP — Suporte Ventilatório/Vasopressor na PAC Grave (calc_smart_cop)
5. Classificação GOLD ABE 2024/2025 para DPOC (calc_gold_abe)
6. Índice BODE — Sobrevida em DPOC (calc_bode)
7. Escala de Dispneia mMRC (calc_mmrc)
8. Escala de Wood-Downes-Ferrés Modificada (calc_wood_downes)
"""

from .common import NOREPINEPHRINE_PROTOCOL


def _axis(axis_id: str, label: str, system: str = "Respiratório", unit: str = "pts") -> dict:
    return {
        "id": axis_id,
        "label": label,
        "system": system,
        "unit": unit,
        "baselineValue": 0,
        "maxAxisValue": 1,
    }


def _opt(opt_id: str, label: str, pts: float, baseline: bool, radar: float, order: int, desc: str) -> dict:
    return {
        "id": opt_id,
        "label": label,
        "pointValue": pts,
        "isNormalBaseline": baseline,
        "radarNormalizedValue": max(0.0, min(1.0, float(radar))),
        "sortOrder": order,
        "description": desc,
    }


def _grp(grp_id: str, name: str, slug: str, axis_id: str, order: int, help_text: str, options: list, unit: str = "pts") -> dict:
    return {
        "id": grp_id,
        "name": name,
        "slug": slug,
        "inputType": "single_choice",
        "unit": unit,
        "radarAxisId": axis_id,
        "normalBaselineValue": 0,
        "maxAxisValue": 1,
        "sortOrder": order,
        "helpText": help_text,
        "options": options,
    }


def _rx(rx_id: str, drug: str, dosage: str, route: str, freq: str, dilution: str, renal: str, contra: str, protocol: dict | None = None) -> dict:
    d = {
        "id": rx_id,
        "drugName": drug,
        "dosage": dosage,
        "route": route,
        "frequency": freq,
        "dilutionInstructions": dilution,
        "renalAdjustment": renal,
        "contraindications": contra,
    }
    if protocol is not None:
        d["infusionProtocol"] = protocol
    return d


def _nonrx(nrx_id: str, title: str, disp: str, mon: str, proc: str = "", vent: str = "", vasc: str = "", lab: str = "") -> dict:
    d = {
        "id": nrx_id,
        "recommendationTitle": title,
        "dispositionTarget": disp,
        "monitoringPlan": mon,
    }
    if proc:
        d["interventionalProcedure"] = proc
    if vent:
        d["ventilatorySupport"] = vent
    if vasc:
        d["vascularAccess"] = vasc
    if lab:
        d["laboratoryPanel"] = lab
    return d


def get_curb65() -> dict:
    return {
        "id": "calc_curb65",
        "slug": "curb-65",
        "name": "CURB-65 para Gravidade da Pneumonia Adquirida na Comunidade (PAC)",
        "acronym": "CURB-65",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Infecções Respiratórias Agudas e PAC",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "Pneumonia Adquirida na Comunidade (PAC)",
        "description": "Escore britânico clássico (British Thoracic Society — Lim et al., 2003) de 0 a 5 pontos para estratificação da mortalidade em 30 dias e decisão do local de tratamento (ambulatorial, enfermaria ou UTI) na Pneumonia Adquirida na Comunidade.",
        "summary": "Estratificação de mortalidade em 30 dias e decisão de internação na PAC (0 a 5 pontos).",
        "clinicalObjective": "Guiar de forma objetiva a alocação do paciente com PAC entre tratamento ambulatorial (0-1 pt), internação hospitalar em enfermaria (2 pts) ou cuidados intensivos em UTI (3-5 pts).",
        "targetPopulation": "Pacientes adultos atendidos no pronto-socorro com diagnóstico clínico-radiológico de Pneumonia Adquirida na Comunidade.",
        "calculationType": "additive_points",
        "formulaExpression": "Confusao + Ureia_50 + FR_30 + PA_Baixa + Idade_65",
        "evidenceSource": "Lim WS, van der Eerden MM, Laing R, et al. Defining community acquired pneumonia severity on presentation to hospital: an international derivation and validation study. Thorax. 2003;58(5):377-382. Diretrizes SBPT / ATS-IDSA.",
        "minPossibleScore": 0,
        "maxPossibleScore": 5,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "ATENÇÃO À OXIGENAÇÃO E FATORES SOCIAIS: Mesmo em pacientes com CURB-65 de 0 ou 1 ponto, a presença de hipoxemia (SpO2 < 90-92% em ar ambiente), derrame pleural complicado/empiema, intolerância à via oral ou vulnerabilidade social indica internação hospitalar.",
        "radarAxes": [
            _axis("axis_curb_resp", "Taquipneia / Esforço Ventilatório (FR)", "Respiratório", "irpm"),
            _axis("axis_curb_hemo", "Instabilidade Pressórica (PAS/PAD)", "Cardiovascular", "mmHg"),
            _axis("axis_curb_neuro", "Encefalopatia Aguda (Confusão)", "Neurológico", "pts"),
            _axis("axis_curb_renal", "Escórias Nitrogenadas (Ureia) e Idade", "Renal", "mg/dL"),
        ],
        "parameterGroups": [
            _grp("grp_curb_c", "1. C — Confusion (Confusão Mental Aguda)", "curb65-confusao", "axis_curb_neuro", 1, "Desorientação aguda em tempo, espaço ou pessoa de início recente (ou escore AMTS <= 8).", [
                _opt("opt_curb_c_0", "Ausente — Lúcido e orientado (0 pts)", 0, True, 0.0, 1, "Cognição basal preservada."),
                _opt("opt_curb_c_1", "Presente — Confusão mental ou desorientação aguda (1 pt)", 1, False, 1.0, 2, "Encefalopatia séptica ou hipóxico-hipercápnica associada à PAC."),
            ]),
            _grp("grp_curb_u", "2. U — Urea (Ureia Sérica > 50 mg/dL ou BUN > 19-20 mg/dL / > 7 mmol/L)", "curb65-ureia", "axis_curb_renal", 2, "No Brasil, utiliza-se o ponto de corte de Ureia plasmática > 50 mg/dL (equivalente a BUN > 19-20 mg/dL).", [
                _opt("opt_curb_u_0", "Ureia <= 50 mg/dL (BUN <= 19 mg/dL) (0 pts)", 0, True, 0.0, 1, "Escórias nitrogenadas dentro da faixa aceitável."),
                _opt("opt_curb_u_1", "Ureia > 50 mg/dL (BUN > 19 mg/dL ou > 7 mmol/L) (1 pt)", 1, False, 1.0, 2, "Azotemia pré-renal por desidratação/hipoperfusão e hipercatabolismo proteico."),
            ], unit="mg/dL"),
            _grp("grp_curb_r", "3. R — Respiratory Rate (Frequência Respiratória >= 30 irpm)", "curb65-fr", "axis_curb_resp", 3, "Contagem de incursões respiratórias por minuto em um minuto completo.", [
                _opt("opt_curb_r_0", "FR < 30 irpm (0 pts)", 0, True, 0.0, 1, "Frequência respiratória abaixo do limiar crítico de exaustão."),
                _opt("opt_curb_r_1", "FR >= 30 irpm (Taquipneia acentuada) (1 pt)", 1, False, 1.0, 2, "Sobrecarga mecânica ventilatória e perda de complacência pulmonar."),
            ], unit="irpm"),
            _grp("grp_curb_b", "4. B — Blood Pressure (PAS < 90 mmHg OU PAD <= 60 mmHg)", "curb65-pa", "axis_curb_hemo", 4, "Basta um dos critérios pressóricos (sistólico < 90 ou diastólico <= 60 mmHg) para pontuar.", [
                _opt("opt_curb_b_0", "PAS >= 90 mmHg E PAD > 60 mmHg (Normotenso) (0 pts)", 0, True, 0.0, 1, "Pressão de perfusão tecidual preservada."),
                _opt("opt_curb_b_1", "PAS < 90 mmHg OU PAD <= 60 mmHg (Hipotensão) (1 pt)", 1, False, 1.0, 2, "Vasoplegia inflamatória sistêmica ou choque séptico incipiente."),
            ], unit="mmHg"),
            _grp("grp_curb_65", "5. 65 — Idade >= 65 anos", "curb65-idade", "axis_curb_renal", 5, "Idade cronológica na admissão.", [
                _opt("opt_curb_65_0", "Idade < 65 anos (0 pts)", 0, True, 0.0, 1, "Adulto com menos de 65 anos."),
                _opt("opt_curb_65_1", "Idade >= 65 anos (1 pt)", 1, False, 1.0, 2, "Imunossenescência e menor reserva fisiológica cardiopulmonar."),
            ], unit="anos"),
        ],
        "riskTiers": [
            {
                "id": "tier_curb_low",
                "label": "Baixo Risco (0 a 1 ponto) — Tratamento Ambulatorial",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Mortalidade em 30 dias de 0,6% (0 pts) a 2,7% (1 pt). Candidato a tratamento antimicrobiano ambulatorial se SpO2 >= 92% e sem complicações pleurais ou sociais.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_curb_low_atb", "Amoxicilina (+/- Clavulanato) + Azitromicina (ou Claritromicina)", "Amoxicilina 1g VO 8/8h (ou Amoxicilina+Clavulanato 875/125mg 12/12h se comorbidades) + Azitromicina 500mg VO 1x/dia por 5 a 7 dias", "Via Oral", "8/8h ou 12/12h + 24/24h", "Alternativa em alérgicos a betalactâmicos: Levofloxacino 750mg VO 1x/dia ou Moxifloxacino 400mg VO 1x/dia por 5 dias.", "Ajustar Amoxicilina e Levofloxacino se ClCr < 30 mL/min.", "Alergia a penicilinas ou intervalo QTc prolongado (macrolídeos/quinolonas).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_curb_low_1", "Alta com Tratamento Domiciliar e Reavaliação em 48-72h", "Alta Orientada / Ambulatório", "Hidratação oral vigorosa, antitérmicos e retorno imediato se surgir dispneia, queda de saturação, sonolência ou persistência de febre após 72h de antibiótico.", lab="Radiografia de tórax PA e perfil; oximetria de pulso.")
                ]
            },
            {
                "id": "tier_curb_mod",
                "label": "Risco Intermediário (2 pontos) — Internação em Enfermaria",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade em 30 dias de 6,8% a 9,2%. Indicação de internação hospitalar em enfermaria clínica (ou hospital-dia sob observação estreita).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_curb_mod_atb", "Ceftriaxona IV + Azitromicina IV/VO (ou Claritromicina)", "Ceftriaxona 1g a 2g IV 24/24h + Azitromicina 500mg IV/VO 24/24h (ou Levofloxacino 750mg IV/VO 24/24h em monoterapia)", "Intravenosa / VO", "24/24 horas", "Ceftriaxona: reconstituir e diluir em 50-100 mL SF 0,9% ou SG 5%. Transicionar para terapia oral assim que afebril por 24-48h e estável.", "Ceftriaxona não exige ajuste renal isolado; Levofloxacino exige ajuste se ClCr < 50 mL/min.", "Não diluir Ceftriaxona em soluções contendo cálcio (Ringer Lactato).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_curb_mod_1", "Internação em Enfermaria e Profilaxia de TEV", "Enfermaria Clínica", "Monitorar sinais vitais e SpO2 de 6/6h; profilaxia farmacológica de TEV com Enoxaparina 40mg SC 1x/dia.", vent="Oxigenoterapia suplementar por cateter nasal para manter SpO2 entre 92% e 96%.", lab="Hemograma, PCR, ureia, creatinina, Na, K, glicemia, RX de tórax (ultrassom torácico se derrame pleural para toracocentese diagnóstica).")
                ]
            },
            {
                "id": "tier_curb_high",
                "label": "Alto Risco / PAC Grave (3 a 5 pontos) — Avaliação de UTI",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Mortalidade em 30 dias de 14,5% (3 pts), 27% a 40% (4 pts) e até 57% (5 pts). Indicação de internação imediata e avaliação de UTI (aplicar SMART-COP / Critérios ATS-IDSA). Em choque séptico ou VM, associar Hidrocortisona (estudo CAPE COD).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_curb_high_atb", "Ceftriaxona 2g IV + Azitromicina 500mg IV (ou Cefepime/Piperacilina-Tazobactam se risco de Pseudomonas)", "Ceftriaxona 2g IV 24/24h + Azitromicina 500mg IV 24/24h (iniciar na 1ª hora se sepse/choque)", "Intravenosa", "24/24h", "Se fatores de risco para MRSA (pneumonia necrosante pós-influenza, colonização prévia), associar Vancomicina (15-20 mg/kg 12/12h) ou Linezolida (600mg 12/12h).", "Ajustar betalactâmicos antipseudomonas e glicopeptídeos conforme ClCr.", "Alergia grave a betalactâmicos."),
                    _rx("rx_curb_high_cort", "Hidrocortisona Endovenosa (na PAC Grave em UTI — Estudo CAPE COD 2023)", "200 mg/dia IV em infusão contínua (ou 50 mg IV de 6/6h) por 4 a 7 dias com desmame gradual", "Intravenosa", "Contínua ou 6/6h", "Diluir em SF 0,9%.", "Sem ajuste renal.", "Pneumonia viral por Influenza confirmada (onde corticoide aumenta mortalidade) ou infecção fúngica invasiva."),
                    _rx("rx_curb_high_norepi", "Noradrenalina em BIC (se Choque Séptico Pulmonar PAM < 65 mmHg)", "0,05 a 2,0 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL).", "Sem ajuste renal.", "Acesso central preferencial.", NOREPINEPHRINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_curb_high_1", "Cuidados Intensivos, Suporte Ventilatório e Pacote de 1 Hora da Sepse", "UTI / Sala Vermelha", "Monitorização multiparamétrica contínua, balanço hídrico e curva de lactato.", vent="Cateter Nasal de Alto Fluxo (CNAF — reduz necessidade de IOT na hipoxemia aguda) ou Ventilação Mecânica Protetora (VC 6 mL/kg peso predito, Pplatô < 30, Driving Pressure < 15 cmH2O).", lab="2 pares de hemoculturas, cultura de secreção traqueal/escarro, antígenos urinários para Pneumococo e Legionella, painel viral respiratório (Influenza/SARS-CoV-2), gasometria arterial e lactato.")
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }


def get_crb65() -> dict:
    return {
        "id": "calc_crb65",
        "slug": "crb-65",
        "name": "CRB-65 para Triagem de PAC sem Laboratório (Atenção Primária e UPA)",
        "acronym": "CRB-65",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Infecções Respiratórias Agudas e PAC",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "Pneumonia Adquirida na Comunidade (PAC)",
        "description": "Versão puramente clínica do CURB-65 (0 a 4 pontos) que dispensa a dosagem sérica de ureia, validada pela British Thoracic Society e OMS para decisão imediata de encaminhamento hospitalar no consultório, UBS ou pronto-atendimento sem laboratório imediato.",
        "summary": "Estratificação clínica imediata de PAC sem necessidade de exames laboratoriais (0 a 4 pontos).",
        "clinicalObjective": "Identificar imediatamente no consultório ou atenção primária pacientes com PAC de baixo risco (0 pts) que podem ser tratados no domicílio versus aqueles (>= 1 pt) que necessitam de avaliação hospitalar.",
        "targetPopulation": "Pacientes adultos com suspeita clínica de Pneumonia Adquirida na Comunidade em ambiente ambulatorial, UBS ou triagem de emergência.",
        "calculationType": "additive_points",
        "formulaExpression": "Confusao + FR_30 + PA_Baixa + Idade_65",
        "evidenceSource": "Bauer TT, Ewig S, Marre R, Suttorp N, Welte T; CAPNETZ Study Group. CRB-65 predicts death from community-acquired pneumonia. J Intern Med. 2006;260(1):93-101.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "Na Atenção Primária, qualquer paciente com CRB-65 >= 1 ponto OU oximetria de pulso < 92% em ar ambiente deve ser referenciado para avaliação hospitalar. Com 0 pontos e SpO2 >= 92%, o tratamento ambulatorial é altamente seguro (mortalidade < 1%).",
        "radarAxes": [
            _axis("axis_crb_resp", "Taquipneia (FR >= 30 irpm)", "Respiratório", "irpm"),
            _axis("axis_crb_hemo", "Pressão Arterial (PAS < 90 ou PAD <= 60)", "Cardiovascular", "mmHg"),
            _axis("axis_crb_neuro_age", "Confusão Mental e Idade >= 65a", "Neurológico", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_crb_c", "1. C — Confusion (Confusão Mental de Início Agudo)", "crb65-confusao", "axis_crb_neuro_age", 1, "Desorientação aguda temporoespacial ou sonolência não habitual.", [
                _opt("opt_crb_c_0", "Ausente — Alerta e orientado (0 pts)", 0, True, 0.0, 1, "Estado mental basal preservado."),
                _opt("opt_crb_c_1", "Presente — Confusão mental aguda (1 pt)", 1, False, 1.0, 2, "Sinal de hipoxemia cerebral ou encefalopatia séptica."),
            ]),
            _grp("grp_crb_r", "2. R — Respiratory Rate (Frequência Respiratória >= 30 irpm)", "crb65-fr", "axis_crb_resp", 2, "Frequência respiratória aferida em repouso.", [
                _opt("opt_crb_r_0", "FR < 30 irpm (0 pts)", 0, True, 0.0, 1, "Sem taquipneia grave."),
                _opt("opt_crb_r_1", "FR >= 30 irpm (1 pt)", 1, False, 1.0, 2, "Taquipneia grave indicando comprometimento parenquimatoso extenso."),
            ], unit="irpm"),
            _grp("grp_crb_b", "3. B — Blood Pressure (PAS < 90 mmHg OU PAD <= 60 mmHg)", "crb65-pa", "axis_crb_hemo", 3, "Pressão arterial aferida no braço.", [
                _opt("opt_crb_b_0", "PAS >= 90 mmHg E PAD > 60 mmHg (0 pts)", 0, True, 0.0, 1, "Estabilidade pressórica."),
                _opt("opt_crb_b_1", "PAS < 90 mmHg OU PAD <= 60 mmHg (1 pt)", 1, False, 1.0, 2, "Hipotensão arterial aguda."),
            ], unit="mmHg"),
            _grp("grp_crb_65", "4. 65 — Idade >= 65 anos", "crb65-idade", "axis_crb_neuro_age", 4, "Idade do paciente.", [
                _opt("opt_crb_65_0", "Idade < 65 anos (0 pts)", 0, True, 0.0, 1, "Menos de 65 anos."),
                _opt("opt_crb_65_1", "Idade >= 65 anos (1 pt)", 1, False, 1.0, 2, "Idoso (>= 65 anos)."),
            ], unit="anos"),
        ],
        "riskTiers": [
            {
                "id": "tier_crb_low",
                "label": "Muito Baixo Risco (0 pontos) — Tratamento Domiciliar",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Mortalidade em 30 dias < 0,9%. Tratamento ambulatorial seguro sem necessidade obrigatória de coleta laboratorial.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_crb_low_1", "Amoxicilina 1g 8/8h (ou Amoxicilina-Clavulanato + Macrolídeo se comorbidades)", "Amoxicilina 1g VO 8/8h por 5-7 dias (associar Azitromicina 500mg/dia se suspeita de germes atípicos)", "Via Oral", "8/8h", "Tomar com água.", "Ajustar se DRC conhecida.", "Alergia a penicilinas (usar Claritromicina 500mg 12/12h ou Levofloxacino 750mg/dia).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_crb_low_1", "Manejo Domiciliar com Revisão em 48 Horas", "Domicílio / UBS", "Aferir SpO2 antes da liberação (deve ser >= 92% em ar ambiente); orientar sinais de alarme.", lab="Dispensável na ausência de comorbidades descompensadas.")
                ]
            },
            {
                "id": "tier_crb_mod",
                "label": "Risco Intermediário (1 a 2 pontos) — Avaliação e Internação Hospitalar",
                "severityLevel": "intermediate",
                "minScore": 1,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade em 30 dias de ~5,2% (1 pt) a ~12,0% (2 pts). Indicação de encaminhamento hospitalar para exames complementares, radiografia e antibioticoterapia parentera/assistida.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_crb_mod_1", "Ceftriaxona 1-2g IV + Azitromicina 500mg IV/VO (ou Levofloxacino 750mg)", "Ceftriaxona 1-2g IV 1x/dia + Azitromicina 500mg 1x/dia", "IV ou VO", "24/24h", "Iniciar primeira dose no pronto-atendimento antes da transferência.", "Ajustar quinolona pela função renal.", "Alergia a cefalosporinas.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_crb_mod_1", "Avaliação Hospitalar e Cálculo do CURB-65 Completo", "Pronto-Socorro / Enfermaria", "Coletar ureia e eletrólitos para converter para CURB-65; manter SpO2 >= 92%.", lab="Hemograma, ureia, creatinina, PCR, glicemia e RX de tórax.")
                ]
            },
            {
                "id": "tier_crb_high",
                "label": "Alto Risco (3 a 4 pontos) — Internação Hospitalar de Urgência / UTI",
                "severityLevel": "critical",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Mortalidade em 30 dias > 31%. Emergência médica exigindo estabilização hemodinâmica e ventilatória imediata e transferência em ambulância avançada para UTI.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_crb_high_1", "Antibioticoterapia Endovenosa na 1ª Hora + Ressuscitação Volêmica / Vasopressor", "Ceftriaxona 2g IV + Azitromicina 500mg IV + Cristaloide 30 mL/kg se hipotensão", "Intravenosa", "Imediato", "Se PAM < 65 mmHg refratária a volume, iniciar Noradrenalina em BIC.", "Sem ajuste na dose de ataque.", "Choque cardiogênico concomitante.", NOREPINEPHRINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_crb_high_1", "Estabilização na Sala Vermelha e Vaga de UTI", "Sala Vermelha / UTI", "Monitorização contínua, oxigenoterapia suplementar / VNI / IOT conforme mecânica respiratória.", vent="CNAF, VNI ou Intubação Orotraqueal se insuficiência respiratória franca.", lab="Gasometria arterial, lactato, hemoculturas, ureia, creatinina, eletrólitos.")
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }


def get_psi_port() -> dict:
    return {
        "id": "calc_psi_port",
        "slug": "psi-port",
        "name": "PSI / PORT Score (Pneumonia Severity Index)",
        "acronym": "PSI/PORT",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Infecções Respiratórias Agudas e PAC",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "Pneumonia Adquirida na Comunidade (PAC)",
        "description": "Escore prognóstico mais extensamente validado pelas diretrizes ATS/IDSA (Fine et al., 1997) para estratificação da Pneumonia Adquirida na Comunidade em 5 Classes de Risco (Classes I a V), combinando demografia, comorbidades, exame físico, gasometria, bioquímica e radiologia.",
        "summary": "Estratificação detalhada ATS/IDSA da PAC nas Classes de Risco I a V para decisão segura de alta ou internação.",
        "clinicalObjective": "Maximizar a identificação segura de pacientes de baixo risco (Classes I e II, <= 70 pontos) para tratamento ambulatorial, reduzindo internações desnecessárias com maior poder discriminatório que o CURB-65.",
        "targetPopulation": "Pacientes adultos atendidos em serviços de emergência com diagnóstico de Pneumonia Adquirida na Comunidade.",
        "calculationType": "additive_points",
        "formulaExpression": "Demografia + Comorbidades + ExameFisico + GasometriaOxigenacao + BioquimicaHematologia + DerramePleural",
        "evidenceSource": "Fine MJ, Auble TE, Yealy DM, et al. A prediction rule to identify low-risk patients with community-acquired pneumonia. N Engl J Med. 1997;336(4):243-250. ATS/IDSA CAP Guidelines 2019.",
        "minPossibleScore": 0,
        "maxPossibleScore": 290,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "A diretriz ATS/IDSA recomenda preferencialmente o PSI/PORT sobre o CURB-65 para identificar candidatos ao tratamento ambulatorial (Classes I e II), mas ressalta que o PSI pode superestimar a gravidade em idosos saudáveis pelo peso da idade e subestimar a necessidade de UTI em jovens hipoxêmicos (onde o SMART-COP é superior).",
        "radarAxes": [
            _axis("axis_psi_demo_comorb", "Demografia e Comorbidades Crônicas", "Cardiovascular", "pts"),
            _axis("axis_psi_vitals", "Instabilidade de Sinais Vitais e Sensório", "Neurológico", "pts"),
            _axis("axis_psi_gaso", "Acidose (pH < 7,35) e Hipoxemia", "Respiratório", "pts"),
            _axis("axis_psi_lab_rx", "Distúrbios Metabólicos e Derrame Pleural", "Renal", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_psi_1", "1. Demografia, Faixa Etária e Institucionalização", "psi-demografia", "axis_psi_demo_comorb", 1, "No PSI original: Homens pontuam a idade em anos; Mulheres pontuam Idade - 10; Residentes em asilo/ILPI somam +10 pts.", [
                _opt("opt_psi_1_0", "Adulto < 50 anos sem comorbidades e sinais vitais normais (Classe I) (0 pts)", 0, True, 0.0, 1, "Critério de triagem da Etapa 1 de Fine (Classe I direta se sem alterações)."),
                _opt("opt_psi_1_50", "Faixa de 50 a 64 anos (ou mulher de 60 a 74 anos) (50 pts)", 50, False, 0.45, 2, "Pontuação demográfica intermediária."),
                _opt("opt_psi_1_70", "Faixa de 65 a 79 anos (70 pts)", 70, False, 0.75, 3, "Pontuação demográfica elevada."),
                _opt("opt_psi_1_90", "Idade >= 80 anos OU Idoso residente em Instituição de Longa Permanência (+10) (90 pts)", 90, False, 1.0, 4, "Longevidade avançada e/ou fragilidade institucional."),
            ]),
            _grp("grp_psi_2", "2. Doenças Coexistentes (Comorbidades de Base)", "psi-comorbidades", "axis_psi_demo_comorb", 2, "Neoplasia ativa (+30), Doença Hepática (+20), Insuficiência Cardíaca (+10), Doença Cerebrovascular (+10), Doença Renal (+10).", [
                _opt("opt_psi_2_0", "Nenhuma comorbidade maior presente (0 pts)", 0, True, 0.0, 1, "Sem neoplasia, hepatopatia, ICC, AVC ou nefropatia."),
                _opt("opt_psi_2_10", "1 comorbidade moderada: ICC (+10), Doença Cerebrovascular (+10) ou Doença Renal (+10) (10 pts)", 10, False, 0.25, 2, "Presença de uma comorbidade de 10 pontos."),
                _opt("opt_psi_2_20", "Doença Hepática / Cirrose (+20) OU 2 comorbidades de 10 pts (20 pts)", 20, False, 0.5, 3, "Hepatopatia crônica ou associação de duas comorbidades cardiovasculares/renais."),
                _opt("opt_psi_2_30", "Neoplasia ativa (+30) (exceto pele basocelular/espinocelular) (30 pts)", 30, False, 0.75, 4, "Câncer ativo ou diagnosticado no último ano."),
                _opt("opt_psi_2_50", "Múltiplas comorbidades graves (ex: Neoplasia + ICC/DRC ou Hepatopatia) (50 pts)", 50, False, 1.0, 5, "Elevada carga multimórbida basal."),
            ]),
            _grp("grp_psi_3", "3. Achados do Exame Físico na Admissão", "psi-exame-fisico", "axis_psi_vitals", 3, "Confusão mental (+20), FR >= 30 irpm (+20), PAS < 90 mmHg (+20), Temp < 35°C ou >= 40°C (+15), FC >= 125 bpm (+10).", [
                _opt("opt_psi_3_0", "Exame físico sem sinais críticos (Lúcido, FR < 30, PAS >= 90, FC < 125) (0 pts)", 0, True, 0.0, 1, "Sinais vitais e estado mental preservados."),
                _opt("opt_psi_3_20", "1 achado crítico: Confusão (+20) OU FR >= 30 (+20) OU PAS < 90 (+20) OU Temp extrema/FC >= 125 (20 pts)", 20, False, 0.4, 2, "Um marcador clínico de instabilidade aguda."),
                _opt("opt_psi_3_40", "2 achados críticos (ex: Taquipneia FR >= 30 + Confusão ou Hipotensão) (40 pts)", 40, False, 0.75, 3, "Dupla disfunção clínica aguda."),
                _opt("opt_psi_3_60", ">= 3 achados críticos concomitantes no exame físico (60 pts)", 60, False, 1.0, 4, "Instabilidade clínica grave multissistêmica."),
            ]),
            _grp("grp_psi_4", "4. Gasometria Arterial e Oxigenação (pH e PaO2/SpO2)", "psi-gasometria", "axis_psi_gaso", 4, "Acidemia pH arterial < 7,35 (+30 pts) e Hipoxemia PaO2 < 60 mmHg ou SpO2 < 90% em ar ambiente (+10 pts).", [
                _opt("opt_psi_4_0", "pH >= 7,35 E PaO2 >= 60 mmHg (SpO2 >= 90% em AA) (0 pts)", 0, True, 0.0, 1, "Equilíbrio ácido-básico e oxigenação preservados."),
                _opt("opt_psi_4_10", "Hipoxemia isolada: PaO2 < 60 mmHg ou SpO2 < 90% em AA com pH >= 7,35 (10 pts)", 10, False, 0.35, 2, "Insuficiência respiratória hipoxêmica sem acidemia."),
                _opt("opt_psi_4_30", "Acidemia grave: pH arterial < 7,35 isolada (30 pts)", 30, False, 0.8, 3, "Acidose metabólica lática ou respiratória hipercápnica."),
                _opt("opt_psi_4_40", "Ambos: pH arterial < 7,35 E Hipoxemia PaO2 < 60 / SpO2 < 90% (40 pts)", 40, False, 1.0, 4, "Falência ventilatória e/ou choque séptico com acidemia hipoxêmica."),
            ]),
            _grp("grp_psi_5", "5. Painel Bioquímico e Hematológico", "psi-bioquimica", "axis_psi_lab_rx", 5, "BUN >= 30 mg/dL / Ureia >= 65 mg/dL (+20), Sódio < 130 mEq/L (+20), Glicemia >= 250 mg/dL (+10), Hematócrito < 30% (+10).", [
                _opt("opt_psi_5_0", "Exames laboratoriais dentro dos limites (Ureia < 65, Na >= 130, Glic < 250, Ht >= 30%) (0 pts)", 0, True, 0.0, 1, "Homeostase metabólica e hematológica preservada."),
                _opt("opt_psi_5_10", "Glicemia >= 250 mg/dL (+10) OU Hematócrito < 30% (+10) (10 pts)", 10, False, 0.3, 2, "Hiperglicemia de estresse ou anemia moderada."),
                _opt("opt_psi_5_20", "Ureia >= 65 mg/dL (BUN >= 30) (+20) OU Hiponatremia Na < 130 mEq/L (+20) (20 pts)", 20, False, 0.65, 3, "Azotemia importante ou SIADH secundária à pneumonia."),
                _opt("opt_psi_5_40", "Combinação de >= 2 distúrbios laboratoriais maiores (ex: Ureia >= 65 + Na < 130) (40 pts)", 40, False, 1.0, 4, "Desarranjo metabólico e renal grave."),
            ]),
            _grp("grp_psi_6", "6. Derrame Pleural na Radiografia ou Ultrassom de Tórax", "psi-derrame-pleural", "axis_psi_lab_rx", 6, "Presença de líquido livre ou loculado no espaço pleural.", [
                _opt("opt_psi_6_0", "Ausente — Seios costofrênicos livres (0 pts)", 0, True, 0.0, 1, "Sem derrame parapneumônico."),
                _opt("opt_psi_6_10", "Presente — Derrame pleural visível no RX ou US (+10 pts)", 10, False, 1.0, 2, "Derrame parapneumônico (avaliar toracocentese se >= 1 cm no decúbito lateral ou > 2-3 cm no US)."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_psi_12",
                "label": "PSI Classes I e II — Baixo Risco (0 a 70 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 70,
                "statisticalOutcome": "Mortalidade em 30 dias de 0,1% (Classe I) a 0,6% (Classe II). Forte recomendação ATS/IDSA para tratamento antimicrobiano ambulatorial.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_psi_12_1", "Amoxicilina 1g 8/8h (ou Amoxicilina-Clavulanato + Macrolídeo)", "Amoxicilina 1g VO 8/8h (associar Azitromicina 500mg/dia ou Doxiciclina 100mg 12/12h se comorbidades)", "Via Oral", "8/8h a 24/24h", "Curso total de 5 dias se estabilidade clínica alcançada.", "Ajustar se ClCr < 30 mL/min.", "Alergia a betalactâmicos (usar quinolona respiratória).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_psi_12_1", "Tratamento Domiciliar com Retorno Programado", "Alta Orientada / Ambulatório", "Reavaliação clínica em 48-72h; não há necessidade de colher hemoculturas ou cultura de escarro no paciente ambulatorial.", lab="RX de tórax e oximetria de pulso.")
                ]
            },
            {
                "id": "tier_psi_3",
                "label": "PSI Classe III — Risco Baixo-Intermediário (71 a 90 pontos)",
                "severityLevel": "intermediate",
                "minScore": 71,
                "maxScore": 90,
                "statisticalOutcome": "Mortalidade em 30 dias de 0,9% a 2,8%. Indica observação hospitalar curta (24h em unidade de decisão clínica) ou tratamento ambulatorial se suporte domiciliar excelente e SpO2 >= 92%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_psi_3_1", "Ceftriaxona IV (1ª dose na observação) + Azitromicina VO ou Levofloxacino 750mg VO", "Ceftriaxona 1-2g IV + Azitromicina 500mg VO (transicionar para Amoxicilina-Clavulanato VO na alta)", "IV / VO", "24/24h", "Garantir primeira dose supervisionada e hidratação.", "Ajustar conforme função renal.", "Alergias específicas.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_psi_3_1", "Observação Curta (12-24h) e Reavaliação de Estabilidade", "Unidade de Observação / Hospital-Dia", "Vigiar curva térmica, aceitação oral e oximetria antes da definição de alta vs. enfermaria.", lab="Hemograma, ureia, creatinina, eletrólitos, PCR.")
                ]
            },
            {
                "id": "tier_psi_4",
                "label": "PSI Classe IV — Risco Moderado-Alto (91 a 130 pontos)",
                "severityLevel": "high",
                "minScore": 91,
                "maxScore": 130,
                "statisticalOutcome": "Mortalidade em 30 dias de 8,2% a 9,3%. Indicação formal de internação hospitalar em enfermaria clínica com antibioticoterapia endovenosa.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    _rx("rx_psi_4_1", "Ceftriaxona 1-2g IV 24/24h + Azitromicina 500mg IV/VO 24/24h", "Terapia combinada Betalactâmico + Macrolídeo (ou Fluoroquinolona respiratória IV)", "Intravenosa", "24/24h", "Se houver derrame pleural significativo, realizar toracocentese diagnóstica (drenar imediatamente se pH líquido pleural < 7,20, pus franco ou glicose < 40 mg/dL).", "Ajustar conforme ClCr.", "Intervalo QTc > 500 ms.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_psi_4_1", "Internação em Enfermaria Clínica e Toracocentese se Derrame", "Enfermaria Clínica", "Monitorização de sinais vitais 4/4h a 6/6h, oxigenoterapia suplementar e profilaxia de TEV com HBPM.", proc="Toracocentese guiada por ultrassom se derrame parapneumônico >= 10 mm.", lab="Hemoculturas (2 pares), cultura de escarro, bioquímica pleural (se derrame), PCR, painel metabólico.")
                ]
            },
            {
                "id": "tier_psi_5",
                "label": "PSI Classe V — Alto Risco / PAC Grave (131 a 290 pontos)",
                "severityLevel": "critical",
                "minScore": 131,
                "maxScore": 290,
                "statisticalOutcome": "Mortalidade em 30 dias de 27,0% a 31,1%. Indicação de admissão em UTI ou Unidade Semi-Intensiva, suporte ventilatório/hemodinâmico avançado e cobertura antimicrobiana de amplo espectro.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_psi_5_atb", "Ceftriaxona 2g IV + Azitromicina 500mg IV + Hidrocortisona 200mg/dia IV (se PAC grave em UTI)", "Antibiótico IV na 1ª hora; ampliar para Piperacilina-Tazobactam 4,5g 6/6h ou Cefepime 2g 8/8h se risco de Pseudomonas", "Intravenosa", "Horário estrito", "Associar Hidrocortisona 200mg/dia IV se necessidade de VM ou CNAF com FiO2 >= 50% (estudo CAPE COD).", "Ajustar conforme função renal após dose de ataque.", "Descartar Influenza antes de iniciar corticoide."),
                    _rx("rx_psi_5_norepi", "Noradrenalina em BIC (se Choque Séptico Pulmonar)", "0,05 a 2,0 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL).", "Sem ajuste renal.", "Garantir ressuscitação volêmica inicial.", NOREPINEPHRINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_psi_5_1", "Internação em UTI e Suporte Avançado de Vida", "UTI", "Monitorização invasiva, controle de lactato e diurese horária.", vent="CNAF ou Ventilação Mecânica Protetora (VC 6 mL/kg peso predito).", lab="Hemoculturas, cultura traqueal, antígenos urinários para Pneumococo e Legionella, gasometria arterial e lactato.")
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }


def get_smart_cop() -> dict:
    return {
        "id": "calc_smart_cop",
        "slug": "smart-cop",
        "name": "SMART-COP Score para Suporte Ventilatório ou Vasopressor na PAC",
        "acronym": "SMART-COP",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Infecções Respiratórias Agudas e PAC Grave",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "Pneumonia Adquirida na Comunidade (PAC)",
        "description": "Ferramenta clínica australiana (Charles et al., 2008) de 0 a 11 pontos desenhada especificamente para prever a necessidade de Suporte Respiratório Intensivo (Ventilação Mecânica Invasiva ou Não Invasiva) ou Suporte Vasopressor (IRVS) na Pneumonia Adquirida na Comunidade, superando o PSI e o CURB-65 em pacientes jovens graves.",
        "summary": "Predição de necessidade de Ventilação Mecânica ou Vasopressores (UTI) na PAC (0 a 11 pontos).",
        "clinicalObjective": "Identificar precocemente na emergência os pacientes com PAC que exigirão intubação, VNI/CNAF ou infusão de noradrenalina (escore >= 3 moderado; >= 5 alto risco de UTI).",
        "targetPopulation": "Pacientes adultos admitidos no hospital com Pneumonia Adquirida na Comunidade.",
        "calculationType": "additive_points",
        "formulaExpression": "PAS_2 + Multilobar_1 + Albumina_1 + FR_1 + Taquicardia_1 + Confusao_1 + Oxigenacao_2 + pH_2",
        "evidenceSource": "Charles PG, Wolfe R, Whitby M, et al. SMART-COP: a tool for predicting the need for intensive respiratory or vasopressor support in community-acquired pneumonia. Clin Infect Dis. 2008;47(3):375-384.",
        "minPossibleScore": 0,
        "maxPossibleScore": 11,
        "baseScore": 0,
        "badge": "emergencia",
        "clinicalWarning": "VANTAGEM CRÍTICA SOBRE O CURB-65: O SMART-COP atribui peso duplo (2 pts) à Hipotensão (PAS < 90), Hipoxemia (ajustada por idade) e Acidose (pH < 7,35), evitando a falsa segurança do CURB-65 em pacientes jovens (< 65 anos) com pneumonia multilobar hipoxêmica.",
        "radarAxes": [
            _axis("axis_sc_oxy_ph", "Hipoxemia e Acidose Respiratória/Metabólica", "Respiratório", "pts"),
            _axis("axis_sc_hemo", "Choque / Hipotensão (PAS) e Taquicardia", "Cardiovascular", "pts"),
            _axis("axis_sc_lung", "Extensão Multilobar e Taquipneia (FR)", "Respiratório", "pts"),
            _axis("axis_sc_syst", "Hipoalbuminemia e Confusão Mental", "Neurológico", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_sc_s", "1. S — Systolic BP (Pressão Arterial Sistólica < 90 mmHg — Peso 2)", "smartcop-pas", "axis_sc_hemo", 1, "PAS inicial ou pré-ressuscitação na emergência.", [
                _opt("opt_sc_s_0", "PAS >= 90 mmHg (0 pts)", 0, True, 0.0, 1, "Pressão sistólica >= 90 mmHg."),
                _opt("opt_sc_s_2", "PAS < 90 mmHg (2 pts)", 2, False, 1.0, 2, "Hipotensão sistólica preditora direta de necessidade de suporte vasopressor."),
            ], unit="mmHg"),
            _grp("grp_sc_m", "2. M — Multilobar Involvement (Acometimento Multilobar no RX/TC)", "smartcop-multilobar", "axis_sc_lung", 2, "Consolidação alveolar acometendo >= 2 lobos pulmonares (uni ou bilateral).", [
                _opt("opt_sc_m_0", "Unilobar — Restrito a 1 lobo pulmonar (0 pts)", 0, True, 0.0, 1, "Infiltrado pneumônico focal."),
                _opt("opt_sc_m_1", "Multilobar — >= 2 lobos acometidos (1 pt)", 1, False, 1.0, 2, "Extensa área de shunt intrapulmonar por preenchimento alveolar."),
            ]),
            _grp("grp_sc_a", "3. A — Albumin (Albumina Sérica < 3,5 g/dL)", "smartcop-albumina", "axis_sc_syst", 3, "Nível sérico de albumina na admissão.", [
                _opt("opt_sc_a_0", "Albumina >= 3,5 g/dL (ou não aferida sem desnutrição) (0 pts)", 0, True, 0.0, 1, "Pressão coloidosmótica e estado nutricional preservados."),
                _opt("opt_sc_a_1", "Albumina < 3,5 g/dL (1 pt)", 1, False, 1.0, 2, "Proteína negativa de fase aguda indicando inflamação sistêmica intensa e extravasamento capilar."),
            ], unit="g/dL"),
            _grp("grp_sc_r", "4. R — Respiratory Rate (Frequência Respiratória Ajustada por Idade)", "smartcop-fr", "axis_sc_lung", 4, "Corte ajustado: se <= 50 anos: FR >= 25 irpm; se > 50 anos: FR >= 30 irpm.", [
                _opt("opt_sc_r_0", "Normal para a idade (<= 50a: < 25 irpm; > 50a: < 30 irpm) (0 pts)", 0, True, 0.0, 1, "Sem taquipneia crítica para a faixa etária."),
                _opt("opt_sc_r_1", "Taquipneia (<= 50a: FR >= 25 irpm; > 50a: FR >= 30 irpm) (1 pt)", 1, False, 1.0, 2, "Esforço ventilatório elevado ajustado à reserva etária."),
            ], unit="irpm"),
            _grp("grp_sc_t", "5. T — Tachycardia (Frequência Cardíaca >= 125 bpm)", "smartcop-fc", "axis_sc_hemo", 5, "Frequência cardíaca na apresentação.", [
                _opt("opt_sc_t_0", "FC < 125 bpm (0 pts)", 0, True, 0.0, 1, "Frequência cardíaca < 125 bpm."),
                _opt("opt_sc_t_1", "FC >= 125 bpm (1 pt)", 1, False, 1.0, 2, "Taquicardia sinusal hiperdinâmica importante."),
            ], unit="bpm"),
            _grp("grp_sc_c", "6. C — Confusion (Confusão Mental de Início Agudo)", "smartcop-confusao", "axis_sc_syst", 6, "Rebaixamento ou desorientação aguda.", [
                _opt("opt_sc_c_0", "Ausente — Lúcido e orientado (0 pts)", 0, True, 0.0, 1, "Sensório normal."),
                _opt("opt_sc_c_1", "Presente — Confusão mental aguda (1 pt)", 1, False, 1.0, 2, "Encefalopatia aguda."),
            ]),
            _grp("grp_sc_o", "7. O — Oxygen Low (Hipoxemia Ajustada por Idade — Peso 2)", "smartcop-oxigenacao", "axis_sc_oxy_ph", 7, "Se <= 50a: PaO2 < 70 mmHg, SpO2 <= 93% ou PaO2/FiO2 < 333. Se > 50a: PaO2 < 60 mmHg, SpO2 <= 90% ou PaO2/FiO2 < 250.", [
                _opt("opt_sc_o_0", "Oxigenação preservada para a idade (0 pts)", 0, True, 0.0, 1, "Troca gasosa preservada."),
                _opt("opt_sc_o_2", "Hipoxemia crítica (<=50a: SpO2 <=93% / PaO2 <70; >50a: SpO2 <=90% / PaO2 <60) (2 pts)", 2, False, 1.0, 2, "Falência de oxigenação indicando shunt grave e necessidade iminente de suporte ventilatório."),
            ]),
            _grp("grp_sc_p", "8. P — Arterial pH < 7,35 (Acidemia na Gasometria — Peso 2)", "smartcop-ph", "axis_sc_oxy_ph", 8, "pH arterial na gasometria admissional.", [
                _opt("opt_sc_p_0", "pH arterial >= 7,35 (0 pts)", 0, True, 0.0, 1, "Sem acidemia descompensada."),
                _opt("opt_sc_p_2", "pH arterial < 7,35 (2 pts)", 2, False, 1.0, 2, "Acidose respiratória por fadiga diafragmática e/ou acidose lática por hipoperfusão."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_sc_low",
                "label": "Baixo Risco de Suporte Intensivo (0 a 2 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Risco < 4% de necessidade de suporte ventilatório invasivo ou vasopressor. Seguro para manejo fora da UTI (enfermaria ou ambulatório conforme CURB-65/PSI).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_sc_low_1", "Antibioticoterapia Padrão para PAC (Betalactâmico + Macrolídeo)", "Ceftriaxona 1-2g IV/dia + Azitromicina 500mg/dia (se internado) ou Amoxicilina-Clavulanato + Macrolídeo VO", "IV ou VO", "24/24h", "Administrar conforme alocação clínica.", "Ajuste renal se necessário.", "Alergia a betalactâmicos.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_sc_low_1", "Cuidados em Enfermaria ou Ambulatório", "Enfermaria / Ambulatório", "Monitorização clínica de rotina e oximetria.", lab="Hemograma, PCR, função renal e RX de tórax.")
                ]
            },
            {
                "id": "tier_sc_mod",
                "label": "Risco Moderado de Suporte Intensivo (3 a 4 pontos)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Risco de 12,5% (1 em cada 8 pacientes) de evoluir com necessidade de ventilação mecânica ou aminas vasoativas. Internação hospitalar obrigatória com vigilância estreita.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_sc_mod_1", "Ceftriaxona 2g IV + Azitromicina 500mg IV + Cristaloide Criterioso", "Ceftriaxona 2g IV 24/24h + Azitromicina 500mg IV 24/24h", "Intravenosa", "24/24h", "Iniciar imediatamente na emergência.", "Sem ajuste renal para Ceftriaxona.", "Hipersensibilidade grave.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_sc_mod_1", "Internação Hospitalar com Vigilância Oximétrica e Gasométrica", "Enfermaria Monitorizada / Semi-Intensiva", "Reavaliar FR, SpO2, índice de ROX e pressão arterial a cada 2-4 horas nas primeiras 24h.", vent="Oxigenoterapia titulada para SpO2 92-96%.", lab="Gasometria arterial, lactato, albumina, ureia, creatinina, hemoculturas.")
                ]
            },
            {
                "id": "tier_sc_high",
                "label": "Alto / Altíssimo Risco de Suporte Intensivo (5 a 11 pontos)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 11,
                "statisticalOutcome": "Risco de 33% (5-6 pts, 1 em 3) a >= 67% (>= 7 pts, 2 em 3) de exigir Ventilação Mecânica ou Suporte Vasopressor (sensibilidade de 92% para escore >= 3). Transferência IMEDIATA para UTI.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_sc_high_atb", "Terapia Antimicrobiana Dupla Endovenosa Imediata + Hidrocortisona 200mg/dia IV", "Ceftriaxona 2g IV (ou Cefepime/Piperacilina-Tazobactam) + Azitromicina 500mg IV + Hidrocortisona 200mg/dia IV", "Intravenosa", "Contínua / Horário", "Na PAC grave em UTI sem Influenza, a Hidrocortisona 200mg/dia reduziu mortalidade em 28 dias de 11,9% para 6,2% (CAPE COD NEJM 2023).", "Ajustar betalactâmicos pela TFG.", "Excluir pneumonia por Influenza."),
                    _rx("rx_sc_high_norepi", "Noradrenalina em BIC (se PAS < 90 mmHg / PAM < 65 mmHg)", "0,05 a 2,0 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL).", "Sem ajuste renal.", "Acesso central.", NOREPINEPHRINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_sc_high_1", "Admissão Imediata em UTI, CNAF / Ventilação Protetora e Suporte Hemodinâmico", "UTI", "Monitorar Índice de ROX ((SpO2/FiO2)/FR) em 2h, 6h e 12h se em CNAF (ROX < 3,85 indica alto risco de falha e necessidade de IOT imediata para não postergar intubação).", vent="Cateter Nasal de Alto Fluxo (CNAF 40-60 L/min) ou Intubação Orotraqueal sob Ventilação Protetora (VC 6 mL/kg peso predito, PEEP titulada, Pplatô < 30 cmH2O).", vasc="Cateter Venoso Central e PAI se choque séptico.", lab="Gasometria arterial seriada, lactato, hemoculturas, painel molecular respiratório e antígenos urinários.")
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }


def get_gold_abe() -> dict:
    return {
        "id": "calc_gold_abe",
        "slug": "gold-abe-dpoc",
        "name": "Classificação GOLD ABE (2024/2025) para Manejo da DPOC",
        "acronym": "GOLD-ABE",
        "version": "2025.1",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Doença Pulmonar Obstrutiva Crônica (DPOC)",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "DPOC e Doenças Obstrutivas Crônicas",
        "description": "Sistema vigente da Global Initiative for Chronic Obstructive Lung Disease (GOLD 2024/2025) que unificou os antigos grupos C e D no novo Grupo E (Exacerbador), classificando o paciente com DPOC confirmada (VEF1/CVF < 0,70 pós-BD) nos Grupos A, B ou E conforme sintomas (mMRC/CAT), histórico de exacerbações e contagem sérica de eosinófilos.",
        "summary": "Classificação moderna GOLD ABE (2024/2025) da DPOC para escolha de LABA, LAMA e Corticoide Inalatório.",
        "clinicalObjective": "Definir a terapia inalatória farmacológica inicial e de seguimento na DPOC estável, reservando a terapia tripla (LABA + LAMA + CI) para pacientes do Grupo E com eosinófilos sanguíneos >= 300 células/µL.",
        "targetPopulation": "Pacientes adultos com diagnóstico espirométrico confirmado de DPOC (relação VEF1/CVF pós-broncodilatador < 0,70).",
        "calculationType": "branching_decision",
        "formulaExpression": "Sintomas_mMRC_CAT(0_ou_2) + Exacerbacoes_GrupoE(0_ou_4) + Eosinofilos_GOLD(0_ou_1)",
        "evidenceSource": "Global Initiative for Chronic Obstructive Lung Disease (GOLD). Global Strategy for the Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary Disease: 2024/2025 Report.",
        "minPossibleScore": 0,
        "maxPossibleScore": 7,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "DIRETRIZ GOLD 2024/2025: A combinação LABA + CI isolada (sem LAMA) NÃO é mais recomendada na DPOC! Sempre que houver indicação de corticoide inalatório (Grupo E com eosinófilos >= 300 cél/µL ou história concomitante de asma), deve-se prescrever TERAPIA TRIPLA (LABA + LAMA + CI), preferencialmente em inalador único (estudos IMPACT e ETHOS demonstraram redução de mortalidade). Se eosinófilos < 100 cél/µL, evitar CI pelo risco elevado de pneumonia bacteriana.",
        "radarAxes": [
            _axis("axis_gold_symp", "Carga Sintomática (Dispneia mMRC / CAT)", "Respiratório", "pts"),
            _axis("axis_gold_exac", "Frequência e Gravidade de Exacerbações (Grupo E)", "Respiratório", "eventos/ano"),
            _axis("axis_gold_eos", "Inflamação Tipo 2 (Eosinófilos) e Obstrução", "Imunológico", "cél/µL"),
        ],
        "parameterGroups": [
            _grp("grp_gold_symp", "1. Eixo Horizontal: Carga de Sintomas (Escala mMRC e Questionário CAT)", "gold-sintomas", "axis_gold_symp", 1, "Basta um dos dois instrumentos atingir o limiar (mMRC >= 2 ou CAT >= 10) para classificar como muito sintomático.", [
                _opt("opt_gold_symp_0", "Pouco Sintomático: mMRC 0 a 1 E CAT < 10 (0 pts)", 0, True, 0.0, 1, "Dispneia apenas a grandes esforços e baixo impacto na qualidade de vida."),
                _opt("opt_gold_symp_2", "Muito Sintomático: mMRC >= 2 OU CAT >= 10 (2 pts)", 2, False, 1.0, 2, "Dispneia ao caminhar no plano no passo de pessoas da mesma idade ou escore CAT >= 10."),
            ]),
            _grp("grp_gold_exac", "2. Eixo Vertical: Histórico de Exacerbações nos Últimos 12 Meses", "gold-exacerbacoes", "axis_gold_exac", 2, "Exacerbação moderada = exigiu antibiótico e/ou corticoide sistêmico. Grave = exigiu internação hospitalar ou ida ao pronto-socorro.", [
                _opt("opt_gold_exac_0", "Baixo Risco de Exacerbação: 0 ou 1 exacerbação moderada (SEM hospitalização) (0 pts)", 0, True, 0.0, 1, "Define alocação nos Grupos A ou B conforme sintomas."),
                _opt("opt_gold_exac_4", "Alto Risco (Grupo E): >= 2 exacerbações moderadas OU >= 1 hospitalização por DPOC (4 pts)", 4, False, 1.0, 2, "Classifica automaticamente o paciente no Grupo E (Exacerbador) independentemente do mMRC/CAT."),
            ]),
            _grp("grp_gold_eos", "3. Biomarcador Sanguíneo (Eosinófilos Periféricos) e Grau Espirométrico (GOLD 1-4)", "gold-eosinofilos", "axis_gold_eos", 3, "A contagem de eosinófilos no hemograma guia a adição de Corticoide Inalatório (CI) no Grupo E.", [
                _opt("opt_gold_eos_0", "Eosinófilos < 300 células/µL (GOLD 1: VEF1>=80%; GOLD 2: 50-79%; GOLD 3: 30-49%; GOLD 4: <30%) (0 pts)", 0, True, 0.0, 1, "Sem inflamação eosinofílica acentuada (se < 100 cél/µL, CI é ineficaz e aumenta risco de pneumonia)."),
                _opt("opt_gold_eos_1", "Eosinófilos >= 300 células/µL (ou >= 100 cél/µL com exacerbações refratárias a LABA+LAMA) (1 pt)", 1, False, 1.0, 2, "Forte preditor de resposta clínica e redução de exacerbações com adição de Corticoide Inalatório (Terapia Tripla)."),
            ], unit="cél/µL"),
        ],
        "riskTiers": [
            {
                "id": "tier_gold_a",
                "label": "GOLD Grupo A — Poucos Sintomas e Baixo Risco de Exacerbações (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "mMRC 0-1, CAT < 10 e 0-1 exacerbação moderada sem internação. Conduta GOLD 2024/2025: Iniciar 1 Broncodilatador (preferencialmente de longa duração LAMA ou LABA).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_gold_a_1", "Broncodilatador em Monoterapia (LAMA ou LABA de Longa Duração)", "Tiotrópio 5 mcg (2 jatos Respimat 1x/dia) ou Glicopirrônio 50 mcg 1x/dia ou Olodaterol / Indacaterol", "Inalatória", "1x/dia", "Revisar técnica inalatória em todas as consultas.", "Sem ajuste renal.", "Glaucoma de ângulo fechado ou retenção urinária grave prostática (cautela com LAMA).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_gold_a_1", "Cessação do Tabagismo, Vacinação e Atividade Física", "Ambulatório", "Cessação do tabagismo (vareniclina/bupropiona/TRN), vacinação anual contra Influenza, Pneumococo (VPC13/VPC15/VPC20 + VPP23), COVID-19, dTpa e Vírus Sincicial Respiratório (VSR se >= 60 anos).", lab="Espirometria com prova broncodilatadora, hemograma (eosinófilos) e dosagem de Alfa-1 Antitripsina (uma vez na vida em todo paciente com DPOC).")
                ]
            },
            {
                "id": "tier_gold_b",
                "label": "GOLD Grupo B — Muito Sintomático e Baixo Risco de Exacerbações (2 a 3 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "mMRC >= 2 ou CAT >= 10 com 0-1 exacerbação moderada sem hospitalização. Conduta GOLD 2024/2025: Iniciar diretamente Dupla Broncodilatação (LABA + LAMA) em dispositivo único.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_gold_b_1", "Dupla Broncodilatação: LABA + LAMA (Superior à monoterapia no alívio de dispneia)", "Tiotrópio + Olodaterol (2,5/2,5 mcg 2 jatos 1x/dia) OU Umeclidínio + Vilanterol (62,5/25 mcg 1 inalação/dia) OU Indacaterol + Glicopirrônio (110/50 mcg 1x/dia)", "Inalatória", "1x/dia", "Preferir combinação em dispositivo único para maximizar adesão.", "Sem ajuste renal.", "Não associar dois anticolinérgicos (ex: Tiotrópio + Ipratrópio).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_gold_b_1", "Reabilitação Pulmonar Formal e Rastreio de Comorbidades", "Ambulatório de Pneumologia / Reabilitação", "Indicar programa de Reabilitação Pulmonar (obrigatório nos Grupos B e E); investigar insuficiência cardíaca, apneia do sono e câncer de pulmão (TC de baixa dose anual em tabagistas/ex-tabagistas 50-80a com >= 20 anos-maço).", lab="Oximetria, espirometria, TC de tórax e ecocardiograma se dispneia desproporcional.")
                ]
            },
            {
                "id": "tier_gold_e",
                "label": "GOLD Grupo E — Alto Risco de Exacerbação (>= 2 moderadas ou >= 1 internação) (4 a 7 pontos)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 7,
                "statisticalOutcome": "Fenótipo Exacerbador com alto risco de declínio acelerado do VEF1, reinternação e óbito. Conduta GOLD 2024/2025: LABA + LAMA (se Eos < 300) OU Terapia Tripla LABA + LAMA + CI de início se Eosinófilos >= 300 cél/µL (ou >= 100 cél/µL na falha de LABA+LAMA).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_gold_e_triple", "Terapia Tripla em Inalador Único (LABA + LAMA + CI) se Eosinófilos >= 300 cél/µL (ou LABA + LAMA se Eos < 300)", "Fluticasona + Umeclidínio + Vilanterol (100/62,5/25 mcg 1x/dia) OU Beclometasona + Formoterol + Glicopirrônio (2 jatos 12/12h) OU Budesonida + Glicopirrônio + Formoterol", "Inalatória", "1x/dia ou 12/12h", "Se paciente persistir exacerbando sob Terapia Tripla (ou sob LABA+LAMA com Eos < 100): adicionar Roflumilaste 500 mcg/dia (se VEF1 < 50% e bronquite crônica), Azitromicina 250mg/dia ou 500mg 3x/sem (em ex-tabagistas) ou Dupilumabe 300mg SC a cada 2 semanas (se Eos >= 300 e bronquite crônica — estudo BOREAS/NOTUS).", "Roflumilaste não exige ajuste renal.", "Evitar CI se pneumonias de repetição, micobacteriose ou eosinófilos < 100 cél/µL.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_gold_e_1", "Reabilitação Pulmonar, Avaliação de Oxigenoterapia Domiciliar (ODP) e VNI Domiciliar", "Ambulatório de DPOC Avançada", "Avaliar indicação de ODP (>= 15h/dia se PaO2 <= 55 mmHg ou SpO2 <= 88% em repouso; ou PaO2 56-59 mmHg com cor pulmonale/policitemia Ht > 55%) e VNI domiciliar noturna se hipercapnia crônica persistente (PaCO2 >= 52-55 mmHg 2-4 semanas após exacerbação).", proc="Avaliar redução volumétrica pulmonar (válvulas endobrônquicas Zephyr) se enfisema heterogêneo grave sem ventilação colateral.", lab="Gasometria arterial em ar ambiente, hemograma com contagem absoluta de eosinófilos, TC de tórax de alta resolução e teste de caminhada de 6 minutos (calcular Índice BODE).")
                ]
            }
        ]
    }


def get_bode() -> dict:
    return {
        "id": "calc_bode",
        "slug": "indice-bode",
        "name": "Índice BODE para Sobrevida Multidimensional na DPOC",
        "acronym": "BODE",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Doença Pulmonar Obstrutiva Crônica (DPOC)",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "DPOC e Doenças Obstrutivas Crônicas",
        "description": "Escore prognóstico multidimensional (Celli et al., NEJM 2004) de 0 a 10 pontos que integra 4 domínios fisiológicos na DPOC: Body Mass Index (B), Airflow Obstruction pelo VEF1 (O), Dyspnea pela escala mMRC (D) e Exercise Capacity pelo Teste de Caminhada de 6 Minutos (E), predizendo a sobrevida em 4 anos com acurácia superior ao VEF1 isolado.",
        "summary": "Predição de sobrevida em 4 anos na DPOC integrando IMC, VEF1, mMRC e Teste de Caminhada de 6 Minutos (0 a 10 pontos).",
        "clinicalObjective": "Quantificar o comprometimento sistêmico e pulmonar da DPOC para estimar mortalidade em 4 anos e selecionar candidatos a redução volumétrica pulmonar ou Transplante Pulmonar (BODE >= 7).",
        "targetPopulation": "Pacientes adultos com DPOC estável submetidos a espirometria e teste de caminhada de 6 minutos.",
        "calculationType": "additive_points",
        "formulaExpression": "IMC_B + VEF1_O + mMRC_D + TC6M_E",
        "evidenceSource": "Celli BR, Cote CG, Marin JM, et al. The body-mass index, airflow obstruction, dyspnea, and exercise capacity index in chronic obstructive pulmonary disease. N Engl J Med. 2004;350(10):1005-1012.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "CRITÉRIO DE TRANSPLANTE PULMONAR (ISHLT): Um Índice BODE de 5 a 6 pontos indica encaminhamento para avaliação em centro de transplante pulmonar; um Índice BODE de 7 a 10 pontos (sobrevida em 4 anos de apenas 18%) é critério formal de listagem ativa para Transplante Pulmonar.",
        "radarAxes": [
            _axis("axis_bode_fev1", "Obstrução ao Fluxo Aéreo (VEF1 % predito)", "Respiratório", "%"),
            _axis("axis_bode_dysp", "Percepção de Dispneia (Escala mMRC)", "Respiratório", "grau"),
            _axis("axis_bode_6mwt", "Capacidade de Exercício (TC6M em metros)", "Cardiovascular", "m"),
            _axis("axis_bode_bmi", "Depleção Nutricional / Sarcopenia (IMC)", "Metabólico", "kg/m2"),
        ],
        "parameterGroups": [
            _grp("grp_bode_b", "1. B — Body Mass Index (Índice de Massa Corporal — IMC)", "bode-imc", "axis_bode_bmi", 1, "O ponto de corte de desnutrição/caquexia pulmonar no BODE é IMC <= 21 kg/m².", [
                _opt("opt_bode_b_0", "IMC > 21,0 kg/m² (0 pts)", 0, True, 0.0, 1, "Massa corporal acima do limiar crítico de caquexia respiratória."),
                _opt("opt_bode_b_1", "IMC <= 21,0 kg/m² (1 pt)", 1, False, 1.0, 2, "Depleção muscular diafragmática e periférica associada a maior mortalidade."),
            ], unit="kg/m2"),
            _grp("grp_bode_o", "2. O — Airflow Obstruction (VEF1 Pós-Broncodilatador em % do Predito)", "bode-vef1", "axis_bode_fev1", 2, "Volume Expiratório Forçado no 1º segundo pós-broncodilatador expresso em percentual do predito.", [
                _opt("opt_bode_o_0", "VEF1 >= 65% do predito (0 pts)", 0, True, 0.0, 1, "Obstrução leve a moderada inicial."),
                _opt("opt_bode_o_1", "VEF1 de 50% a 64% do predito (1 pt)", 1, False, 0.33, 2, "Obstrução moderada."),
                _opt("opt_bode_o_2", "VEF1 de 36% a 49% do predito (2 pts)", 2, False, 0.66, 3, "Obstrução grave."),
                _opt("opt_bode_o_3", "VEF1 <= 35% do predito (3 pts)", 3, False, 1.0, 4, "Obstrução muito grave ao fluxo aéreo."),
            ], unit="%"),
            _grp("grp_bode_d", "3. D — Dyspnea (Escala Modificada do Medical Research Council — mMRC)", "bode-mmrc", "axis_bode_dysp", 3, "Grau funcional de dispneia de 0 a 4.", [
                _opt("opt_bode_d_0", "mMRC Grau 0 ou 1 (Dispneia apenas a grandes esforços ou aclive) (0 pts)", 0, True, 0.0, 1, "Limitação funcional mínima."),
                _opt("opt_bode_d_1", "mMRC Grau 2 (Anda mais devagar que pessoas da mesma idade no plano) (1 pt)", 1, False, 0.33, 2, "Limitação funcional moderada."),
                _opt("opt_bode_d_2", "mMRC Grau 3 (Para para respirar após caminhar ~100 metros ou poucos minutos) (2 pts)", 2, False, 0.66, 3, "Limitação funcional importante."),
                _opt("opt_bode_d_3", "mMRC Grau 4 (Muito dispneico para sair de casa ou dispneia ao vestir-se) (3 pts)", 3, False, 1.0, 4, "Incapacidade respiratória grave nas atividades diárias."),
            ]),
            _grp("grp_bode_e", "4. E — Exercise Capacity (Distância no Teste de Caminhada de 6 Minutos — TC6M)", "bode-tc6m", "axis_bode_6mwt", 4, "Distância total percorrida em metros no corredor plano de 30 metros em 6 minutos.", [
                _opt("opt_bode_e_0", "Distância >= 350 metros (0 pts)", 0, True, 0.0, 1, "Capacidade funcional de exercício preservada."),
                _opt("opt_bode_e_1", "Distância de 250 a 349 metros (1 pt)", 1, False, 0.33, 2, "Redução discreta a moderada da tolerância ao exercício."),
                _opt("opt_bode_e_2", "Distância de 150 a 249 metros (2 pts)", 2, False, 0.66, 3, "Comprometimento acentuado da capacidade aeróbica submáxima."),
                _opt("opt_bode_e_3", "Distância <= 149 metros (3 pts)", 3, False, 1.0, 4, "Intolerância extrema ao esforço com alto risco de óbito."),
            ], unit="m"),
        ],
        "riskTiers": [
            {
                "id": "tier_bode_q1",
                "label": "Quartil 1 (0 a 2 pontos) — Sobrevida em 4 Anos de 80%",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Taxa de sobrevida estimada em 4 anos de 80% (mortalidade em 4 anos ~20%). Manter broncodilatação otimizada conforme GOLD ABE e atividade física regular.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_bode_q1_1", "Broncodilatação de Longa Duração (LAMA ou LABA+LAMA)", "Tiotrópio 5 mcg/dia ou Tiotrópio+Olodaterol conforme sintomatologia GOLD", "Inalatória", "1x/dia", "Checar técnica inalatória.", "Sem ajuste renal.", "Hipersensibilidade.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_bode_q1_1", "Cessação Tabágica, Vacinação e Treinamento Físico", "Ambulatório", "Incentivar caminhadas regulares e suporte nutricional se IMC próximo de 21 kg/m².", lab="Espirometria anual e oximetria.")
                ]
            },
            {
                "id": "tier_bode_q2",
                "label": "Quartil 2 (3 a 4 pontos) — Sobrevida em 4 Anos de 67%",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Taxa de sobrevida estimada em 4 anos de 67% (mortalidade em 4 anos ~33%). Indicação formal de Reabilitação Pulmonar estruturada (que reduz o escore BODE em 1-2 pontos e melhora a sobrevida).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_bode_q2_1", "Dupla Broncodilatação (LABA + LAMA) ou Terapia Tripla se Exacerbador Eosinofílico", "Umeclidínio+Vilanterol ou Tiotrópio+Olodaterol (adicionar CI se Grupo E com Eos >= 300)", "Inalatória", "1x/dia", "Uso diário contínuo.", "Sem ajuste renal.", "Glaucoma de ângulo estreito.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_bode_q2_1", "Programa de Reabilitação Pulmonar e Suporte Nutricional Hiperproteico", "Centro de Reabilitação Pulmonar", "Treinamento aeróbico e de força de membros inferiores/superiores por 8-12 semanas; suplementação proteico-calórica se IMC <= 21 kg/m².", lab="TC6M com oximetria contínua (avaliar dessaturação esforço-induzida SpO2 < 88%).")
                ]
            },
            {
                "id": "tier_bode_q3",
                "label": "Quartil 3 (5 a 6 pontos) — Sobrevida em 4 Anos de 57%",
                "severityLevel": "high",
                "minScore": 5,
                "maxScore": 6,
                "statisticalOutcome": "Taxa de sobrevida em 4 anos de 57% (mortalidade em 4 anos ~43%). Critério ISHLT para encaminhamento e avaliação inicial em Centro de Transplante Pulmonar e Cirurgia/Broncoscopia Redutora de Volume.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    _rx("rx_bode_q3_1", "Terapia Inalatória Máxima + Avaliação de ODP e Mucolíticos/Macrolídeo", "LABA + LAMA + CI (se indicado) + N-Acetilcisteína 600mg 12/12h ou Roflumilaste", "Inalatória e VO", "Diário", "Otimizar todas as terapias farmacológicas.", "Ajuste conforme função renal.", "Contraindicações específicas.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_bode_q3_1", "Referenciamento para Centro de Transplante Pulmonar e Avaliação de ODP", "Ambulatório de Pneumologia Avançada", "Avaliar gasometria para Oxigenoterapia Domiciliar Prolongada (>= 15h/dia) e pletismografia para redução volumétrica pulmonar.", proc="Avaliação broncoscópica para válvulas endobrônquicas se aprisionamento aéreo severo (VR > 175-200%).", lab="Gasometria arterial, pletismografia de corpo inteiro, DLCO, TC de tórax quantitativa e ecocardiograma (rastreio de hipertensão pulmonar).")
                ]
            },
            {
                "id": "tier_bode_q4",
                "label": "Quartil 4 (7 a 10 pontos) — Sobrevida em 4 Anos de 18% (Listagem para Transplante)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 10,
                "statisticalOutcome": "Taxa de sobrevida em 4 anos de apenas 18% (mortalidade em 4 anos de 82%). Critério formal ISHLT para listagem ativa de Transplante Pulmonar, ODP, VNI domiciliar e cuidados paliativos respiratórios precoces.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_bode_q4_1", "Terapia Inalatória Plena + Morfina em Baixa Dose para Dispneia Refratária", "LABA+LAMA(+CI) + Sulfato de Morfina oral em baixa dose (2,5 a 5 mg VO de 6/6h ou 8/8h titulada para alívio de dispneia refratária)", "Inalatória e VO", "Contínuo", "Associar laxativo profilático (Lactulose ou PEG 4000) sempre que prescrever opioide em baixa dose para dispneia crônica refratária.", "Evitar morfina se anúria/DRC grave (preferir Fentanil ou Metadona).", "Acidose respiratória aguda descompensada sem suporte ventilatório.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_bode_q4_1", "Listagem para Transplante Pulmonar, ODP + VNI Domiciliar e Cuidados Paliativos", "Centro de Transplante Pulmonar / Assistência Domiciliar", "Oxigenoterapia contínua (>= 15h/dia), VNI noturna domiciliar se PaCO2 >= 52 mmHg e diretivas antecipadas de vontade.", proc="Transplante Pulmonar uni ou bilateral ou Redução Volumétrica Pulmonar.", lab="Gasometria arterial, cateterismo cardíaco direito pré-transplante, painel HLA e sorologias.")
                ]
            }
        ]
    }


def get_mmrc() -> dict:
    return {
        "id": "calc_mmrc",
        "slug": "escala-mmrc",
        "name": "Escala de Dispneia mMRC (Modified Medical Research Council)",
        "acronym": "mMRC",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Avaliação Funcional Respiratória e DPOC",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "DPOC e Doenças Intersticiais Pulmonares",
        "description": "Escala padronizada internacionalmente (Graus 0 a 4) para graduar a limitação funcional imposta pela dispneia nas atividades de vida diária, sendo componente central da classificação GOLD ABE (corte >= 2) e do Índice BODE.",
        "summary": "Graduação funcional da dispneia de Grau 0 a Grau 4 nas atividades diárias (corte sintomático GOLD >= 2).",
        "clinicalObjective": "Quantificar de forma reprodutível a incapacidade funcional por dispneia em pacientes com DPOC, doença pulmonar intersticial, hipertensão pulmonar e insuficiência cardíaca.",
        "targetPopulation": "Pacientes adultos com pneumopatias crônicas (DPOC, fibrose pulmonar, bronquiectasias) ou dispneia crônica em investigação.",
        "calculationType": "additive_points",
        "formulaExpression": "Grau_mMRC_0_a_4",
        "evidenceSource": "Fletcher CM, Elmes PC, Fairbairn AS, Wood CH. The significance of respiratory symptoms and the diagnosis of chronic bronchitis in a working population. Br Med J. 1959;2(5147):257-266. GOLD 2024/2025.",
        "minPossibleScore": 0,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "pneumologia",
        "clinicalWarning": "Na diretriz GOLD 2024/2025, um escore mMRC >= 2 pontos define o paciente como 'Muito Sintomático' (alocando-o no Grupo B ou E) e indica dupla broncodilatação (LABA + LAMA) e encaminhamento para Reabilitação Pulmonar.",
        "radarAxes": [
            _axis("axis_mmrc_grade", "Grau de Dispneia aos Esforços (mMRC 0-4)", "Respiratório", "grau"),
            _axis("axis_mmrc_desat", "Comportamento Oximétrico ao Esforço", "Respiratório", "%"),
            _axis("axis_mmrc_adl", "Comprometimento de Autonomia / AVDs", "Neurológico", "grau"),
        ],
        "parameterGroups": [
            _grp("grp_mmrc_1", "1. Grau de Dispneia na Escala mMRC (0 a 4 pontos)", "mmrc-grau", "axis_mmrc_grade", 1, "Selecione a afirmação que melhor descreve a limitação respiratória atual do paciente.", [
                _opt("opt_mmrc_0", "Grau 0 (0 pts) — Tenho falta de ar apenas quando faço exercício físico intenso (correr, nadar, subir ladeira íngreme)", 0, True, 0.0, 1, "Tolerância fisiológica preservada aos esforços habituais."),
                _opt("opt_mmrc_1", "Grau 1 (1 pt) — Tenho falta de ar quando aperto o passo no plano ou quando subo uma ladeira leve / 1 lance de escada", 1, False, 0.25, 2, "Limitação leve: considerado 'pouco sintomático' pelo corte GOLD (< 2)."),
                _opt("opt_mmrc_2", "Grau 2 (2 pts) — Ando mais devagar que pessoas da mesma idade no plano por falta de ar, ou preciso parar quando ando no meu próprio passo", 2, False, 0.5, 3, "Limiar GOLD de paciente 'Muito Sintomático' (mMRC >= 2): compromete a velocidade da marcha no plano."),
                _opt("opt_mmrc_3", "Grau 3 (3 pts) — Preciso parar para respirar após caminhar cerca de 100 metros (1 quadra) ou após poucos minutos no plano", 3, False, 0.75, 4, "Limitação funcional grave: autonomia restrita a curtas distâncias."),
                _opt("opt_mmrc_4", "Grau 4 (4 pts) — Sinto tanta falta de ar que não consigo sair de casa, ou sinto falta de ar ao vestir-me ou tomar banho", 4, False, 1.0, 5, "Incapacidade respiratória extrema com dispneia aos mínimos esforços de autocuidado."),
            ]),
            _grp("grp_mmrc_2", "2. Comportamento da Oximetria de Pulso (Repouso e Caminhada)", "mmrc-oximetria", "axis_mmrc_desat", 2, "Avaliação complementar da troca gasosa associada à queixa de dispneia (modificador do radar fisiológico).", [
                _opt("opt_mmrc_ox_0", "Normoxemia em repouso e esforço (SpO2 >= 92% sem queda >= 4% na caminhada) (0 pts)", 0, True, 0.0, 1, "Sem dessaturação induzida pelo exercício."),
                _opt("opt_mmrc_ox_1", "Dessaturação ao esforço (queda >= 4% ou SpO2 < 90% na caminhada, porém >= 89% em repouso) (0 pts)", 0, False, 0.5, 2, "Hipoxemia esforço-induzida sugerindo perda de leito capilar alveolar (DLCO reduzida)."),
                _opt("opt_mmrc_ox_2", "Hipoxemia crônica em repouso (SpO2 <= 88% em ar ambiente) (0 pts)", 0, False, 1.0, 3, "Insuficiência respiratória crônica hipoxêmica com indicação de investigar ODP."),
            ]),
            _grp("grp_mmrc_3", "3. Repercussão nas Atividades Básicas e Instrumentais de Vida Diária", "mmrc-avds", "axis_mmrc_adl", 3, "Impacto funcional da dispneia na independência domiciliar e laboral (modificador do radar).", [
                _opt("opt_mmrc_adl_0", "Independente para atividades laborais, domésticas e sociais (0 pts)", 0, True, 0.0, 1, "Autonomia global preservada."),
                _opt("opt_mmrc_adl_1", "Restrição em atividades instrumentais (compras, limpeza pesada, escadas) (0 pts)", 0, False, 0.5, 2, "Necessita pausas frequentes nas tarefas fora do domicílio."),
                _opt("opt_mmrc_adl_2", "Dependência parcial ou total em AVDs básicas (banho, troca de roupa, alimentação) (0 pts)", 0, False, 1.0, 3, "Confinamento domiciliar secundário ao custo energético ventilatório."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_mmrc_low",
                "label": "Dispneia Leve / Pouco Sintomático (mMRC Grau 0 a 1)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Pontuação no Índice BODE = 0 pts para dispneia; classifica como 'Pouco Sintomático' no eixo horizontal do GOLD ABE. Baixa mortalidade atribuível à dispneia isolada.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_mmrc_low_1", "Monoterapia Broncodilatadora (LAMA ou LABA) se DPOC Grupo A", "Tiotrópio 5 mcg/dia (2 jatos Respimat) ou Glicopirrônio 50 mcg/dia", "Inalatória", "1x/dia", "Manter atividade física regular.", "Sem ajuste renal.", "Hipersensibilidade.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_mmrc_low_1", "Estímulo à Atividade Física Regular e Cessação do Tabagismo", "Ambulatório", "Manter condicionamento aeróbico e calendário vacinal em dia.", lab="Espirometria com prova broncodilatadora.")
                ]
            },
            {
                "id": "tier_mmrc_mod",
                "label": "Dispneia Moderada a Importante / Muito Sintomático (mMRC Grau 2 a 3)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "mMRC >= 2 ultrapassa o limiar sintomático da diretriz GOLD (alocando em Grupo B ou E) e soma 1 pt (Grau 2) ou 2 pts (Grau 3) no Índice BODE.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_mmrc_mod_1", "Dupla Broncodilatação (LABA + LAMA) para Desinsuflação Farmacológica", "Tiotrópio + Olodaterol (2,5/2,5 mcg 2 jatos 1x/dia) ou Umeclidínio + Vilanterol (62,5/25 mcg 1x/dia)", "Inalatória", "1x/dia", "A dupla broncodilatação reduz a hiperinsuflação dinâmica no exercício e melhora o mMRC.", "Sem ajuste renal.", "Não associar dois LAMAs.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_mmrc_mod_1", "Encaminhamento Obrigatório para Reabilitação Pulmonar e TC6M", "Ambulatório / Centro de Reabilitação", "Solicitar Teste de Caminhada de 6 Minutos para calcular o Índice BODE completo e descartar causas cardíacas concomitantes.", lab="Espirometria, TC6M, hemograma, BNP e ecocardiograma se necessário.")
                ]
            },
            {
                "id": "tier_mmrc_high",
                "label": "Dispneia Incapacitante / Extrema (mMRC Grau 4)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Soma a pontuação máxima (3 pts) de dispneia no Índice BODE. Alta probabilidade de hiperinsuflação grave, hipoxemia crônica, cor pulmonale e mortalidade elevada em 4 anos.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_mmrc_high_1", "Terapia Inalatória Otimizada (LABA+LAMA ou Tripla) + Manejo de Dispneia Refratária", "LABA + LAMA (+ CI se Grupo E eosinofílico) + considerar Morfina oral em baixa dose (2,5mg VO 6/6h-8/8h) se dispneia refratária", "Inalatória e VO", "Diário", "Avaliar troca de inalador de pó seco (DPI) por névoa suave (Respimat) ou spray com espaçador caso o fluxo inspiratório de pico do paciente seja < 30-40 L/min.", "Ajustar opioide pela função renal.", "Retenção hipercápnica aguda não ventilada.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_mmrc_high_1", "Gasometria Arterial para Oxigenoterapia Domiciliar (ODP) e Conservação de Energia", "Ambulatório de Pneumologia Avançada / Domiciliar", "Prescrever Oxigenoterapia Domiciliar Prolongada (>= 15h/dia) se PaO2 <= 55 mmHg (ou SpO2 <= 88%); técnicas de conservação de energia no banho/vestuário e uso de ventilador portátil facial.", lab="Gasometria arterial em ar ambiente, TC de tórax, ecocardiograma transtorácico e cálculo do Índice BODE.")
                ]
            }
        ]
    }


def get_wood_downes() -> dict:
    return {
        "id": "calc_wood_downes",
        "slug": "wood-downes-ferres",
        "name": "Escala de Wood-Downes-Ferrés Modificada para Crise Asmática e Bronquiolite",
        "acronym": "Wood-Downes",
        "version": "1.0.0",
        "blockId": "block_04",
        "blockFile": "block_04.json",
        "category": "Pneumologia e Vias Aéreas",
        "subcategory": "Asma Aguda, Broncoespasmo e Bronquiolite",
        "categorySlug": "bloco-04-pneumologia",
        "categoryName": "Pneumologia e Vias Aéreas",
        "moduleName": "Crise Asmática e Obstrução Aguda das Vias Aéreas",
        "description": "Escala clínica à beira do leito (Wood-Downes-Ferrés Modificada, 0 a 14 pontos) que integra 6 parâmetros cardiorrespiratórios (Sibilos, Tiragem, Entrada de Ar, Cianose, Frequência Respiratória e Frequência Cardíaca) para quantificar a gravidade da crise de broncoespasmo agudo / bronquiolite e indicar suporte intensivo.",
        "summary": "Estratificação clínica da gravidade de crise asmática e bronquiolite aguda (0 a 14 pontos).",
        "clinicalObjective": "Monitorar de forma seriada a resposta ao tratamento broncodilatador na sala de emergência e detectar precocemente o 'tórax silencioso' e a fadiga muscular respiratória (escore >= 8 pontos).",
        "targetPopulation": "Pacientes pediátricos e adultos jovens em crise aguda de asma, sibilância aguda ou bronquiolite viral aguda.",
        "calculationType": "additive_points",
        "formulaExpression": "Sibilos(0_3) + Tiragem(0_3) + EntradaAr(0_3) + Cianose(0_2) + FR(0_2) + FC(0_1)",
        "evidenceSource": "Wood DW, Downes JJ, Lecks HI. A clinical scoring system for the diagnosis of respiratory failure. Preliminary report on childhood status asthmaticus. Am J Dis Child. 1972;123(3):227-228. Ferrés J et al., 1988.",
        "minPossibleScore": 0,
        "maxPossibleScore": 14,
        "baseScore": 0,
        "badge": "emergencia",
        "clinicalWarning": "SINAL DE ALERTA MÁXIMO — TÓRAX SILENCIOSO: O desaparecimento dos sibilos acompanhado de entrada de ar muito reduzida ou abolida (3 pts em Sibilos e 3 pts em Entrada de Ar), cianose e bradicardia/sonolência indica obstrução brônquica quase total e parada respiratória iminente, exigindo Sulfato de Magnésio IV imediato, adrenalina/beta-2 contínuo e preparo para sequência rápida de intubação com Quetamina.",
        "radarAxes": [
            _axis("axis_wd_airflow", "Obstrução Brônquica (Sibilos e Entrada de Ar)", "Respiratório", "pts"),
            _axis("axis_wd_work", "Trabalho Muscular (Tiragem e Taquipneia)", "Respiratório", "pts"),
            _axis("axis_wd_oxy_hr", "Hipoxemia (Cianose) e Resposta Taquicárdica", "Cardiovascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_wd_1", "1. Sibilos à Ausculta Pulmonar (0 a 3 pontos)", "wd-sibilos", "axis_wd_airflow", 1, "Avaliação acústica do broncoespasmo nas fases do ciclo respiratório.", [
                _opt("opt_wd_1_0", "0 pts — Ausentes (Fluxo aéreo normal sem broncoespasmo)", 0, True, 0.0, 1, "Respiração tranquila sem ruídos adventícios."),
                _opt("opt_wd_1_1", "1 pt — Sibilos apenas no final da expiração (teleexpiratórios)", 1, False, 0.33, 2, "Obstrução brônquica leve."),
                _opt("opt_wd_1_2", "2 pts — Sibilos audíveis durante toda a expiração", 2, False, 0.66, 3, "Broncoespasmo moderado com prolongamento do tempo expiratório."),
                _opt("opt_wd_1_3", "3 pts — Sibilos inspiratórios e expiratórios (bifásicos) OU Tórax Silencioso na crise grave", 3, False, 1.0, 4, "Obstrução crítica de pequenas e médias vias aéreas."),
            ]),
            _grp("grp_wd_2", "2. Tiragem / Retrações da Musculatura Acessória (0 a 3 pontos)", "wd-tiragem", "axis_wd_work", 2, "Grau de recrutamento muscular acessório para vencer a resistência das vias aéreas.", [
                _opt("opt_wd_2_0", "0 pts — Ausente (Sem retrações)", 0, True, 0.0, 1, "Mecânica ventilatória basal preservada."),
                _opt("opt_wd_2_1", "1 pt — Tiragem subcostal ou intercostal inferior leve (+1)", 1, False, 0.33, 2, "Recrutamento inicial intercostal/subcostal."),
                _opt("opt_wd_2_2", "2 pts — Tiragem intercostal + supraclavicular + batimento de asa de nariz (+2)", 2, False, 0.66, 3, "Recrutamento acentuado de escalenos, esternocleidomastóideo e aletas nasais."),
                _opt("opt_wd_2_3", "3 pts — Tiragem generalizada supraesternal, intercostal e balanço/dissociação toracoabdominal (+3)", 3, False, 1.0, 4, "Fadiga diafragmática iminente com respiração paradoxal."),
            ]),
            _grp("grp_wd_3", "3. Entrada de Ar / Murmúrio Vesicular (0 a 3 pontos)", "wd-entrada-ar", "axis_wd_airflow", 3, "Intensidade e simetria do murmúrio vesicular nos campos pulmonares.", [
                _opt("opt_wd_3_0", "0 pts — Boa, ampla e simétrica bilateralmente", 0, True, 0.0, 1, "Ventilação alveolar preservada."),
                _opt("opt_wd_3_1", "1 pt — Regular / Levemente diminuída ou assimétrica em bases", 1, False, 0.33, 2, "Redução discreta da ventilação regional."),
                _opt("opt_wd_3_2", "2 pts — Muito diminuída difusamente", 2, False, 0.66, 3, "Hipoventilação alveolar importante por aprisionamento aéreo."),
                _opt("opt_wd_3_3", "3 pts — Abolida / Tórax Silencioso", 3, False, 1.0, 4, "Ausência de fluxo aéreo eficaz — emergência absoluta."),
            ]),
            _grp("grp_wd_4", "4. Cianose / Hipoxemia (0 a 2 pontos)", "wd-cianose", "axis_wd_oxy_hr", 4, "Presença de cianose central/perioral ou queda crítica da SpO2.", [
                _opt("opt_wd_4_0", "0 pts — Ausente em ar ambiente (SpO2 >= 94-95% em AA)", 0, True, 0.0, 1, "Oxigenação arterial preservada."),
                _opt("opt_wd_4_1", "1 pt — Cianose presente em ar ambiente (SpO2 < 92% em AA), revertida com O2 suplementar", 1, False, 0.5, 2, "Hipoxemia por distúrbio V/Q responsivo à suplementação de O2."),
                _opt("opt_wd_4_2", "2 pts — Cianose persistente mesmo sob FiO2 >= 40% (SpO2 < 90% com O2)", 2, False, 1.0, 3, "Hipoxemia refratária por shunt intrapulmonar / atelectasias / hipoventilação grave."),
            ]),
            _grp("grp_wd_5", "5. Frequência Respiratória (FR) (0 a 2 pontos)", "wd-fr", "axis_wd_work", 5, "Frequência respiratória de acordo com a faixa etária.", [
                _opt("opt_wd_5_0", "0 pts — FR < 30 irpm (Normal para a idade)", 0, True, 0.0, 1, "Eupneico ou taquipneia mínima."),
                _opt("opt_wd_5_1", "1 pt — FR de 31 a 45 irpm (Taquipneia moderada)", 1, False, 0.5, 2, "Taquipneia compensatória moderada."),
                _opt("opt_wd_5_2", "2 pts — FR > 45 a 60 irpm OU Bradipneia pré-parada por exaustão", 2, False, 1.0, 3, "Taquipneia extrema ou falência do drive respiratório."),
            ], unit="irpm"),
            _grp("grp_wd_6", "6. Frequência Cardíaca (FC) (0 a 1 ponto)", "wd-fc", "axis_wd_oxy_hr", 6, "Resposta cronotrópica ao esforço respiratório e à hipóxia.", [
                _opt("opt_wd_6_0", "0 pts — FC < 120 bpm (Normal)", 0, True, 0.0, 1, "Frequência cardíaca abaixo de 120 bpm."),
                _opt("opt_wd_6_1", "1 pt — FC >= 120 bpm (Taquicardia importante) OU Bradicardia hipóxica (< 60 bpm)", 1, False, 1.0, 2, "Descarga adrenérgica intensa ou bradicardia hipóxico-acidótica."),
            ], unit="bpm"),
        ],
        "riskTiers": [
            {
                "id": "tier_wd_mild",
                "label": "Crise Leve (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Crise obstrutiva leve com SpO2 >= 95% e boa entrada de ar. Excelente resposta ao broncodilatador de curta ação por aerossol dosimetrado com espaçador.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_wd_mild_saba", "Salbutamol Spray (100 mcg/jato) com Espaçador (ou Formoterol+Budesonida na asma GINA)", "4 a 8 jatos de Salbutamol com espaçador a cada 20 min na 1ª hora (se asma persistente, associar Prednisolona/Prednisona 1-2 mg/kg máx 40-50mg VO)", "Inalatória / VO", "A cada 20 min na 1ª hora", "Em bronquiolite viral aguda (< 2 anos), diretrizes AAP não recomendam broncodilatador ou corticoide de rotina; priorizar aspiração nasal com SF 0,9% e suporte.", "Sem ajuste renal.", "Taquiarritmia grave.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_wd_mild_1", "Reavaliação em 1 Hora e Revisão do Plano de Ação de Asma", "Observação Breve -> Alta Orientada", "Se Wood-Downes mantiver <= 3 pts e SpO2 >= 94% após 1h da última inalação, liberar com plano de ação escrito e corticoide inalatório de manutenção (nunca prescrever SABA isolado na asma — GINA 2024).", lab="Oximetria de pulso (e Pico de Fluxo Expiratório / Peak Flow se >= 6 anos).")
                ]
            },
            {
                "id": "tier_wd_mod",
                "label": "Crise Moderada (4 a 7 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 7,
                "statisticalOutcome": "Crise moderada com esforço respiratório evidente e/ou hipoxemia leve (SpO2 91-94%). Requer terapia inalatória combinada (SABA + SAMA), corticoide sistêmico precoce na 1ª hora e oxigenoterapia.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_wd_mod_1", "Salbutamol + Brometo de Ipratrópio Inalatórios + Corticoide Sistêmico Precoce", "Salbutamol 4-10 jatos + Ipratrópio 4-8 jatos no espaçador a cada 20 min por 1h + Prednisona/Prednisolona 1-2 mg/kg VO (máx 40-60mg) ou Metilprednisolona 1-2 mg/kg IV", "Inalatória + VO/IV", "Ciclo de 1ª hora", "A adição de Brometo de Ipratrópio na 1ª hora reduz significativamente a taxa de internação hospitalar em crises moderadas a graves.", "Sem ajuste renal.", "Hipersensibilidade à atropina/ipratrópio.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_wd_mod_1", "Observação na Sala de Emergência e Oxigenoterapia Titulada", "Sala de Observação / Pronto-Socorro", "Recalcular o escore de Wood-Downes a cada 30-60 minutos; se sem melhora após 3-4h na emergência, internar em enfermaria.", vent="Oxigenoterapia sob cateter nasal ou máscara para manter SpO2 93-95% (em adultos) ou 94-98% (em crianças).", lab="Oximetria contínua; RX de tórax apenas se suspeita de pneumotórax, pneumonia associada ou corpo estranho.")
                ]
            },
            {
                "id": "tier_wd_sev",
                "label": "Crise Grave / Insuficiência Respiratória Iminente (8 a 14 pontos)",
                "severityLevel": "critical",
                "minScore": 8,
                "maxScore": 14,
                "statisticalOutcome": "Crise grave ameaçadora à vida (>= 8 pontos). Altíssimo risco de fadiga muscular respiratória, hipercapnia progressiva e parada cardiorrespiratória hipóxica. Indicação imediata de Sulfato de Magnésio IV, CNAF/VNI ou Intubação em UTI.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_wd_sev_mg", "Sulfato de Magnésio Endovenoso (Broncodilatador de Resgate na Crise Grave)", "Adultos: 2 g IV correr em 20 min; Crianças: 25 a 50 mg/kg IV (máx 2 g) correr em 20 a 30 min", "Intravenosa em infusão de 20-30 min", "Dose única (ou seguida de infusão em UTI)", "Diluir 2g (4 mL de MgSO4 50% ou 20 mL de MgSO4 10%) em 100 mL de SF 0,9% ou SG 5%; infundir em 20-30 minutos monitorando PA e reflexos.", "Cautela extrema e redução de 50% se insuficiência renal grave.", "Bloqueio atrioventricular ou hipotensão grave."),
                    _rx("rx_wd_sev_cort_saba", "Beta-2 Agonista + Ipratrópio Contínuos + Metilprednisolona IV + Quetamina (se IOT)", "Metilprednisolona 1-2 mg/kg IV (máx 60-125mg) 6/6h + Salbutamol contínuo; se Intubação Orotraqueal: usar Quetamina 1,5-2 mg/kg IV como indutor (efeito broncodilatador direto)", "Intravenosa / Inalatória", "Contínuo / 6/6h", "Evitar morfina ou bloqueadores neuromusculares liberadores de histamina (como atracúrio) na crise asmática.", "Ajuste se DRC.", "Hipertensão intracraniana não controlada.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_wd_sev_1", "Transferência para UTI, CNAF/VNI e Estratégia de Ventilação Mecânica Obstrutiva", "UTI / Sala Vermelha", "Monitorização contínua de ECG, capnografia (EtCO2) e linha arterial (avaliar pulso paradoxal > 15-20 mmHg).", proc="Se submetido à Ventilação Mecânica Invasiva: usar tubo de maior calibre possível, FR baixa (10-14 irpm), relação I:E prolongada (1:4 a 1:5), fluxo inspiratório alto (60-80 L/min), VC 6-8 mL/kg e hipercapnia permissiva para evitar Auto-PEEP (aprisionamento dinâmico) e barotrauma/pneumotórax hipertensivo.", vent="CNAF / VNI em tentativa curta sob vigilância médica direta; Intubação Orotraqueal imediata se sonolência, tórax silencioso, bradicardia ou acidose respiratória progressiva.", lab="Gasometria arterial, lactato, potássio sérico (beta-2 em altas doses causa hipocalemia intracelular), magnésio e RX de tórax no leito.")
                ]
            }
        ]
    }


def get_block_04_calculators() -> list[dict]:
    return [
        get_curb65(),
        get_crb65(),
        get_psi_port(),
        get_smart_cop(),
        get_gold_abe(),
        get_bode(),
        get_mmrc(),
        get_wood_downes(),
    ]


BLOCK_04_SYNONYMS: dict[str, list[str]] = {
    "calc_curb65": [
        "curb 65", "curb-65", "curb65", "escore curb 65", "pneumonia",
        "pneumonia adquirida na comunidade", "pac", "gravidade pneumonia",
        "internacao pneumonia", "ureia 50", "confusao mental pneumonia", "lim 2003", "cid j18",
    ],
    "calc_crb65": [
        "crb 65", "crb-65", "crb65", "escore crb 65", "pneumonia sem laboratorio",
        "pneumonia atencao primaria", "pneumonia ubs", "pneumonia consultorio",
        "pac ambulatorial", "triagem pneumonia", "bauer 2006", "cid j18",
    ],
    "calc_psi_port": [
        "psi", "port", "psi port", "escore psi", "escore port",
        "pneumonia severity index", "fine score", "escore de fine", "classes de fine",
        "classe i a v pneumonia", "ats idsa pneumonia", "derrame parapneumonico",
    ],
    "calc_smart_cop": [
        "smart cop", "smart-cop", "smartcop", "escore smart-cop", "pneumonia grave",
        "pac grave uti", "suporte ventilatorio pneumonia", "vasopressor pneumonia",
        "pneumonia multilobar", "charles 2008", "intubacao pneumonia",
    ],
    "calc_gold_abe": [
        "gold", "gold abe", "gold 2024", "gold 2025", "classificacao gold",
        "classificação gold", "dpoc", "doenca pulmonar obstrutiva cronica", "enfisema",
        "bronquite cronica", "grupo a grupo b grupo e", "laba lama", "terapia tripla dpoc",
        "eosinofilos dpoc", "exacerbacao dpoc",
    ],
    "calc_bode": [
        "bode", "indice bode", "índice bode", "bode index", "sobrevida dpoc",
        "mortalidade dpoc", "transplante pulmonar dpoc", "vef1 dpoc",
        "teste de caminhada 6 minutos", "tc6m", "celli 2004", "caquexia pulmonar",
    ],
    "calc_mmrc": [
        "mmrc", "escala mmrc", "dispneia mmrc", "modified medical research council",
        "falta de ar", "grau de dispneia", "dispneia aos esforcos",
        "avaliacao funcional dispneia", "cat dpoc", "fletcher",
    ],
    "calc_wood_downes": [
        "wood downes", "wood-downes", "wood downes ferres", "escala de wood downes",
        "crise asmatica", "crise de asma", "asma grave", "bronquiolite",
        "broncoespasmo", "sibilancia", "torax silencioso", "tiragem subcostal", "sulfato de magnesio",
    ],
}
