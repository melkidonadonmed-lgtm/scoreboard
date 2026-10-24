"""
Block 02: Cardiologia e Hemodinâmica (12 Calculadoras Monográficas Completas)
1. HEART Score (calc_heart)
2. TIMI Risk Score — IAMSSST / AI (calc_timi_scasst)
3. TIMI Risk Score — IAMCSST / STEMI (calc_timi_stemi)
4. GRACE 2.0 Risk Score (calc_grace)
5. Classificação de Killip-Kimball no IAM (calc_killip)
6. CHA2DS2-VASc — Risco Tromboembólico na FA (calc_cha2ds2_vasc)
7. HAS-BLED — Risco Hemorrágico na FA (calc_has_bled)
8. ATRIA Bleeding Risk Score (calc_atria)
9. HEMORR2HAGES Score (calc_hemorr2hages)
10. Critérios de Framingham para Insuficiência Cardíaca (calc_framingham_ic)
11. Perfil Clínico-Hemodinâmico de Stevenson & NYHA (calc_stevenson_nyha)
12. MAGGIC Risk Score — Mortalidade na IC (calc_maggic)
"""

from .common import NOREPINEPHRINE_PROTOCOL, DOBUTAMINE_PROTOCOL, NITROGLYCERIN_PROTOCOL


def _axis(axis_id: str, label: str, system: str = "Cardiovascular", unit: str = "pts") -> dict:
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


def get_heart() -> dict:
    return {
        "id": "calc_heart",
        "slug": "heart-score",
        "name": "HEART Score para Dor Torácica Aguda na Emergência",
        "acronym": "HEART",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Síndrome Coronariana Aguda e Dor Torácica",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Síndromes Coronarianas Agudas",
        "description": "Estratificação rápida de risco de eventos cardiovasculares adversos maiores (MACE em 6 semanas: IAM, ICP, CRM ou óbito) em pacientes admitidos com dor torácica aguda na sala de emergência.",
        "summary": "Estratificação de risco de MACE em 6 semanas para dor torácica aguda no pronto-socorro (0 a 10 pontos).",
        "clinicalObjective": "Identificar com segurança pacientes de baixo risco (0-3 pts) elegíveis para alta precoce (protocolo 0/1h ou 0/3h de troponina de alta sensibilidade) e pacientes de alto risco que exigem internação e estratégia invasiva.",
        "targetPopulation": "Adultos (>= 18 anos) atendidos no departamento de emergência com dor torácica não traumática sem supradesnivelamento agudo de ST.",
        "calculationType": "additive_points",
        "formulaExpression": "Historia + ECG + Idade + Fatores_Risco + Troponina",
        "evidenceSource": "Six AJ, Backus BE, Kelder JC. Chest pain in the emergency room: value of the HEART score. Neth Heart J. 2008;16(6):191-196. ESC ACS Guidelines 2023.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "Atenção: O HEART Score não deve ser aplicado em pacientes com IAM com Supradesnivelamento do Segmento ST (IAMCSST) evidente no ECG inicial — nesses casos, acionar imediatamente o protocolo de reperfusão primária (angioplastia primária em <= 90-120 min ou fibrinólise). Mesmo em HEART 0-3, se troponina seriada (0h e 1h/3h) mostrar curva ascendente significativa, reclassificar para internação.",
        "radarAxes": [
            _axis("axis_heart_clin", "História Clínica Anginosa", "Cardiovascular", "pts"),
            _axis("axis_heart_ecg", "Alteração Eletrocardiográfica", "Cardiovascular", "pts"),
            _axis("axis_heart_risk", "Idade e Carga Aterosclerótica", "Vascular", "pts"),
            _axis("axis_heart_trop", "Injúria Miocárdica (Troponina)", "Cardiovascular", "x LSN"),
        ],
        "parameterGroups": [
            _grp("grp_heart_h", "1. History (História Clínica da Dor Torácica)", "heart-history", "axis_heart_clin", 1, "Característica clínica da dor torácica (retroesternal opressiva, irradiação, fatores desencadeantes e de alívio).", [
                _opt("opt_heart_h_0", "Pouco suspeita (0 pts) — Dor atípica (pontada, pleurítica, reproduzível à palpação)", 0, True, 0.0, 1, "Ausência de características típicas de angina instável."),
                _opt("opt_heart_h_1", "Moderadamente suspeita (1 pt) — Combinação de elementos típicos e atípicos", 1, False, 0.5, 2, "Presença parcial de elementos anginosos ou equivalente isquêmico."),
                _opt("opt_heart_h_2", "Altamente suspeita (2 pts) — Dor típica retroesternal opressiva com irradiação e sudorese", 2, False, 1.0, 3, "Quadro clássico de angina pectoris instável ou equivalente isquêmico franco."),
            ]),
            _grp("grp_heart_e", "2. ECG (Eletrocardiograma de 12 Derivações)", "heart-ecg", "axis_heart_ecg", 2, "Análise de repolarização ventricular no ECG realizado em até 10 minutos da chegada.", [
                _opt("opt_heart_e_0", "Normal (0 pts) — Ritmo sinusal sem alterações de ST-T", 0, True, 0.0, 1, "ECG completamente normal ou com alterações inespecíficas mínimas."),
                _opt("opt_heart_e_1", "Alteração inespecífica da repolarização (1 pt) — BRE, HVE, marca-passo, uso de digoxina", 1, False, 0.5, 2, "Distúrbios de condução ou alterações secundárias da repolarização sem infra de ST dinâmico."),
                _opt("opt_heart_e_2", "Desvio significativo do segmento ST (2 pts) — Infradesnivelamento de ST >= 0,5 mm ou inversão de onda T simétrica", 2, False, 1.0, 3, "Infradesnivelamento de ST ou inversão profunda de onda T não atribuível a BRE ou HVE."),
            ]),
            _grp("grp_heart_a", "3. Age (Faixa Etária)", "heart-age", "axis_heart_risk", 3, "Idade cronológica do paciente na admissão.", [
                _opt("opt_heart_a_0", "< 45 anos (0 pts)", 0, True, 0.0, 1, "Faixa etária jovem com menor prevalência basal de DAC obstrutiva."),
                _opt("opt_heart_a_1", "45 a 64 anos (1 pt)", 1, False, 0.5, 2, "Faixa etária intermediária."),
                _opt("opt_heart_a_2", ">= 65 anos (2 pts)", 2, False, 1.0, 3, "Idoso com maior risco basal de doença coronariana multiarterial."),
            ]),
            _grp("grp_heart_r", "4. Risk Factors (Fatores de Risco Cardiovascular e DAC)", "heart-risk", "axis_heart_risk", 4, "Fatores de risco: HAS, DM, Dislipidemia, Tabagismo atual (< 90 dias), Obesidade (IMC >= 30 kg/m²) e História familiar precoce de DAC (< 55a H / < 65a M).", [
                _opt("opt_heart_r_0", "Nenhum fator de risco conhecido (0 pts)", 0, True, 0.0, 1, "Ausência de fatores de risco tradicionais e de doença aterosclerótica."),
                _opt("opt_heart_r_1", "1 ou 2 fatores de risco tradicionais (1 pt)", 1, False, 0.5, 2, "Presença de 1 a 2 fatores de risco sem doença aterosclerótica estabelecida."),
                _opt("opt_heart_r_2", ">= 3 fatores de risco OU história de DAC/IAM/ICP/CRM/AVC/DAOP prévia (2 pts)", 2, False, 1.0, 3, "Múltiplos fatores de risco ou doença aterosclerótica clínica manifesta."),
            ]),
            _grp("grp_heart_t", "5. Troponin (Troponina Cardíaca na Admissão)", "heart-troponin", "axis_heart_trop", 5, "Relação entre o valor medido de Troponina (preferencialmente hs-cTn) e o Limite Superior da Normalidade (LSN / percentil 99).", [
                _opt("opt_heart_t_0", "<= 1x o Limite Superior da Normalidade (LSN) (0 pts)", 0, True, 0.0, 1, "Troponina dentro da faixa de referência normal (<= percentil 99)."),
                _opt("opt_heart_t_1", "> 1x a <= 3x o LSN (1 pt)", 1, False, 0.5, 2, "Elevação discreta a moderada de troponina cardíaca."),
                _opt("opt_heart_t_2", "> 3x o LSN (2 pts)", 2, False, 1.0, 3, "Elevação acentuada compatível com infarto agudo do miocárdio sem supra de ST."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_heart_low",
                "label": "Baixo Risco (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Risco de MACE em 6 semanas de 0,9% a 1,7%. Candidato a alta precoce e segura da emergência se 2ª troponina (protocolo 0/1h ou 0/3h) permanecer normal e sem variação (delta negativo).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_heart_low_1", "Analgesia Direcionada / Sintomáticos", "Dipirona 1g IV/VO se dor osteomuscular ou IBP (Omeprazol 40mg) se dispepsia", "VO ou IV", "Dose única ou conforme sintoma", "Diluir em 10 mL AD se IV lento.", "Sem ajuste em dose única.", "Evitar AINEs se suspeita residual de doença coronariana ou DRC.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_heart_low_1", "Alta Precoce Segura após Delta de Troponina Negativo", "Alta Orientada / Ambulatório", "Seriar ECG e Troponina de alta sensibilidade (0/1h ou 0/3h). Se delta negativo e paciente assintomático, liberar com retorno ambulatorial cardiológico em 72h.", lab="Troponina de alta sensibilidade (hs-cTn) seriada (0h e 1h/3h), ECG de 12 derivações seriado.")
                ]
            },
            {
                "id": "tier_heart_mod",
                "label": "Risco Moderado (4 a 6 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 6,
                "statisticalOutcome": "Risco de MACE em 6 semanas de 12% a 16,6%. Indicação formal de observação hospitalar em Unidade de Dor Torácica, seriação enzimática e estratificação complementar.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_heart_mod_aas", "Ácido Acetilsalicílico (AAS)", "150 a 300 mg VO mastigados (ataque), seguido de 100 mg/dia", "Via Oral", "Ataque imediato + 1x/dia", "Comprimidos não tamponados para absorção rápida.", "Sem necessidade de ajuste renal.", "Alergia grave a salicilatos, sangramento digestivo ativo ou suspeita de dissecção aguda de aorta."),
                    _rx("rx_heart_mod_enox", "Enoxaparina Sódica (se SCA confirmada)", "1 mg/kg SC de 12/12h (ou 0,75 mg/kg 12/12h se >= 75 anos)", "Subcutânea", "12/12 horas", "Seringa preenchida pronta para uso.", "Se ClCr 15-30 mL/min: 1 mg/kg SC 1x/dia (24/24h). Se ClCr < 15 mL/min: preferir HNF IV.", "Sangramento ativo maior, plaquetopenia < 50.000/mm³ ou história de TIH.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_heart_mod_1", "Admissão em Unidade de Dor Torácica (UDT)", "Observação / Unidade Coronariana", "Monitorização cardíaca contínua, ECG seriado a cada 3-6h ou se recorrência de dor, curva de troponina.", proc="Estratificação anatômica (Angio-TC de coronárias) ou funcional (Eco com estresse / Cintilografia) se troponina negativa; Cinecoronariografia se troponina positiva.", lab="Troponina seriada, função renal, eletrólitos, perfil lipídico, hemograma.")
                ]
            },
            {
                "id": "tier_heart_high",
                "label": "Alto Risco (7 a 10 pontos)",
                "severityLevel": "critical",
                "minScore": 7,
                "maxScore": 10,
                "statisticalOutcome": "Risco de MACE em 6 semanas de 50% a 65%. Internação imediata em Unidade Coronariana (UCO/UTI), dupla antiagregação, anticoagulação plena e estratégia invasiva precoce (< 24h).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_heart_high_dapt", "AAS 300mg + Ticagrelor 180mg (ou Clopidogrel 300-600mg)", "AAS 300mg VO mastigado + Ticagrelor 180mg VO ataque (manutenção 90mg 12/12h)", "Via Oral", "Ataque na emergência (ou P2Y12 na sala de hemodinâmica conforme anatomia)", "Administrar via oral.", "Sem ajuste renal para AAS/Ticagrelor.", "Hemorragia intracraniana prévia, sangramento ativo ou indicação de anticoagulação oral crônica (preferir Clopidogrel)."),
                    _rx("rx_heart_high_enox", "Enoxaparina Sódica ou Heparina Não Fracionada (HNF)", "Enoxaparina 1 mg/kg SC 12/12h (ou HNF bolus 60 UI/kg máx 4.000 UI + 12 UI/kg/h IV)", "SC ou IV contínua", "12/12h (Enoxa) ou contínua guiada por TTPa (HNF)", "HNF: 25.000 UI (5 mL) em 245 mL SF 0,9% (100 UI/mL).", "Enoxaparina: 1 mg/kg 24/24h se ClCr 15-30 mL/min; usar HNF se ClCr < 15 mL/min.", "Sangramento ativo ou plaquetopenia induzida por heparina."),
                    _rx("rx_heart_high_ntg", "Nitroglicerina (Tridil) se angina refratária ou congestão pulmonar", "5 a 200 mcg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua titulada por dor e PA", "1 ampola (50 mg/10 mL) em 240 mL SG 5% ou SF 0,9% (200 mcg/mL) em frasco de vidro/polietileno.", "Sem ajuste renal.", "PAS < 90 mmHg, infarto de ventrículo direito (VD) ou uso de sildenafil/vardenafil (< 24h) ou tadalafil (< 48h).", NITROGLYCERIN_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_heart_high_1", "Internação em UCO e Estratégia Invasiva Precoce", "UTI / Unidade Coronariana / Hemodinâmica", "Monitorização eletrocardiográfica contínua, oximetria e controle rigoroso de PA e FC.", proc="Cinecoronariografia (Cateterismo Cardíaco) precoce (< 24h; ou imediata < 2h se instabilidade hemodinâmica, elétrica ou angina refratária).", vent="Oxigenoterapia suplementar apenas se SpO2 < 90%.", vasc="Dois acessos venosos periféricos calibrosos (preferir membro superior esquerdo para preservar radial direita para cateterismo).", lab="Troponina hs, CK-MB, BNP/NT-proBNP, creatinina, ureia, Na, K, Mg, coagulograma, hemograma, glicemia."),
                ],
                "infusionProtocol": NITROGLYCERIN_PROTOCOL
            }
        ]
    }


def get_timi_scasst() -> dict:
    return {
        "id": "calc_timi_scasst",
        "slug": "timi-scasst",
        "name": "TIMI Risk Score para IAMSSST e Angina Instável",
        "acronym": "TIMI-SCASST",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Síndrome Coronariana Aguda sem Supra de ST",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Síndromes Coronarianas Agudas",
        "description": "Escore prognóstico clássico do grupo TIMI (0 a 7 pontos) para estimar o risco composto em 14 dias de mortalidade por todas as causas, novo ou recorrente IAM, ou isquemia grave exigindo revascularização urgente em pacientes com Angina Instável ou IAMSSST.",
        "summary": "Risco em 14 dias de óbito, reinfarto ou isquemia recorrente grave na SCASST (0 a 7 pontos).",
        "clinicalObjective": "Guiar a intensidade da terapia antitrombótica e o timing da estratégia invasiva (cinecoronariografia precoce vs. seletiva) em pacientes com SCASST.",
        "targetPopulation": "Pacientes adultos com Angina Instável (AI) ou Infarto Agudo do Miocárdio sem Supradesnivelamento do Segmento ST (IAMSSST).",
        "calculationType": "additive_points",
        "formulaExpression": "Idade65 + TresFatoresRisco + EstenosePrevia50 + DesvioST + DoisEpisodiosAngina24h + UsoAAS7d + MarcadoresNecrose",
        "evidenceSource": "Antman EM, Cohen M, Bernink PJ, et al. The TIMI risk score for unstable angina/non-ST elevation MI: A method for prognostication and therapeutic decision making. JAMA. 2000;284(7):835-842.",
        "minPossibleScore": 0,
        "maxPossibleScore": 7,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "Escore TIMI >= 3 pontos identifica pacientes com benefício claro de estratégia invasiva precoce (cateterismo em < 24-48h) e anticoagulação plena associada a dupla antiagregação plaquetária.",
        "radarAxes": [
            _axis("axis_timi_sca_age_risk", "Idade e Risco Aterosclerótico", "Vascular", "pts"),
            _axis("axis_timi_sca_angina", "Instabilidade Anginosa e AAS", "Cardiovascular", "pts"),
            _axis("axis_timi_sca_ecg", "Desvio Dinâmico de ST", "Cardiovascular", "pts"),
            _axis("axis_timi_sca_trop", "Necrose Miocárdica", "Cardiovascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_timi_sca_1", "1. Idade >= 65 anos", "timi-sca-idade", "axis_timi_sca_age_risk", 1, "Idade na admissão hospitalar.", [
                _opt("opt_timi_sca_1_0", "Idade < 65 anos (0 pts)", 0, True, 0.0, 1, "Paciente com menos de 65 anos."),
                _opt("opt_timi_sca_1_1", "Idade >= 65 anos (1 pt)", 1, False, 1.0, 2, "Idoso (>= 65 anos): fator independente de reserva coronariana reduzida."),
            ]),
            _grp("grp_timi_sca_2", "2. >= 3 Fatores de Risco para DAC", "timi-sca-fatores-risco", "axis_timi_sca_age_risk", 2, "Fatores: HAS, DM, Dislipidemia, Tabagismo ativo, História familiar precoce de DAC.", [
                _opt("opt_timi_sca_2_0", "< 3 fatores de risco para DAC (0 pts)", 0, True, 0.0, 1, "Zero, um ou dois fatores de risco tradicionais."),
                _opt("opt_timi_sca_2_1", ">= 3 fatores de risco para DAC (1 pt)", 1, False, 1.0, 2, "Três ou mais fatores de risco cardiovasculares clássicos."),
            ]),
            _grp("grp_timi_sca_3", "3. Estenose Coronariana Conhecida >= 50%", "timi-sca-estenose-previa", "axis_timi_sca_age_risk", 3, "Documentação prévia por cateterismo, angio-TC ou história de ICP/CRM.", [
                _opt("opt_timi_sca_3_0", "Ausente ou desconhecida (0 pts)", 0, True, 0.0, 1, "Sem documentação prévia de lesão coronariana obstrutiva >= 50%."),
                _opt("opt_timi_sca_3_1", "Estenose coronariana prévia documentada >= 50% (1 pt)", 1, False, 1.0, 2, "DAC obstrutiva conhecida ou revascularização prévia."),
            ]),
            _grp("grp_timi_sca_4", "4. Desvio do Segmento ST >= 0,5 mm no ECG", "timi-sca-desvio-st", "axis_timi_sca_ecg", 4, "Infradesnivelamento de ST >= 0,5 mm ou supradesnivelamento transitório (< 20 min).", [
                _opt("opt_timi_sca_4_0", "Sem desvio de ST >= 0,5 mm (0 pts)", 0, True, 0.0, 1, "Ausência de depressão ou elevação transitória significativa do segmento ST."),
                _opt("opt_timi_sca_4_1", "Desvio do segmento ST >= 0,5 mm (1 pt)", 1, False, 1.0, 2, "Infradesnivelamento dinâmico de ST >= 0,5 mm em derivações contíguas."),
            ]),
            _grp("grp_timi_sca_5", "5. Angina Grave (>= 2 episódios nas últimas 24 horas)", "timi-sca-angina-24h", "axis_timi_sca_angina", 5, "Recorrência de episódios anginosos em repouso ou mínimos esforços nas últimas 24h.", [
                _opt("opt_timi_sca_5_0", "< 2 episódios anginosos em 24h (0 pts)", 0, True, 0.0, 1, "Episódio único ou dor controlada."),
                _opt("opt_timi_sca_5_1", ">= 2 episódios de angina nas últimas 24h (1 pt)", 1, False, 1.0, 2, "Angina instável recorrente indicando placa vulnerável com trombose ativa."),
            ]),
            _grp("grp_timi_sca_6", "6. Uso de AAS nos últimos 7 dias", "timi-sca-aas-previo", "axis_timi_sca_angina", 6, "Uso regular de Ácido Acetilsalicílico na última semana antes do evento agudo.", [
                _opt("opt_timi_sca_6_0", "Não usou AAS nos últimos 7 dias (0 pts)", 0, True, 0.0, 1, "Sem uso recente de aspirina."),
                _opt("opt_timi_sca_6_1", "Uso de AAS nos últimos 7 dias (1 pt)", 1, False, 1.0, 2, "Evento isquêmico ocorrido na vigência de bloqueio da COX-1 plaquetária (falha terapêutica)."),
            ]),
            _grp("grp_timi_sca_7", "7. Marcadores de Necrose Miocárdica Elevados", "timi-sca-troponina", "axis_timi_sca_trop", 7, "Troponina I/T (ou CK-MB) acima do percentil 99 do método.", [
                _opt("opt_timi_sca_7_0", "Marcadores normais / negativos (0 pts)", 0, True, 0.0, 1, "Troponina sérica dentro da normalidade."),
                _opt("opt_timi_sca_7_1", "Troponina ou CK-MB elevada acima do LSN (1 pt)", 1, False, 1.0, 2, "Necrose de cardiomiócitos confirmando diagnóstico de IAMSSST."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_timi_sca_low",
                "label": "Baixo Risco (0 a 2 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Risco em 14 dias de óbito, IAM ou revascularização urgente: 4,7% (0-1 pt) a 8,3% (2 pts). Permite estratificação não invasiva ou cinecoronariografia seletiva se troponina negativa e sem recorrência de dor.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_timi_sca_low_aas", "AAS + Estatina de Alta Potência", "AAS 300mg VO ataque (manutenção 100mg/dia) + Atorvastatina 80mg/dia ou Rosuvastatina 40mg/dia", "Via Oral", "1x/dia", "Administrar imediatamente.", "Sem ajuste renal para Atorvastatina/AAS.", "Alergia a AAS ou hepatopatia aguda descompensada.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_sca_low_1", "Observação em Unidade de Dor Torácica e Teste Provocativo", "Observação / Enfermaria Cardiológica", "ECG e troponina seriados. Se ambos negativos e paciente estável, realizar teste isquêmico ou Angio-TC coronariana.", lab="Troponina hs 0h/3h, perfil lipídico, função renal, hemograma.")
                ]
            },
            {
                "id": "tier_timi_sca_mod",
                "label": "Risco Intermediário (3 a 4 pontos)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 4,
                "statisticalOutcome": "Risco em 14 dias de eventos adversos maiores: 13,2% (3 pts) a 19,9% (4 pts). Indicação de internação em Unidade Coronariana, anticoagulação plena e estratégia invasiva (< 24-72h).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_timi_sca_mod_dapt", "Dupla Antiagregação (AAS + Inibidor P2Y12) + Enoxaparina", "AAS 300mg VO + Ticagrelor 180mg VO (ou Clopidogrel 300-600mg) + Enoxaparina 1 mg/kg SC 12/12h", "VO e SC", "Ataque imediato + manutenção 12/12h", "Enoxaparina: reduzir para 0,75 mg/kg 12/12h sem bolus se >= 75 anos.", "Enoxaparina 1 mg/kg 24/24h se ClCr 15-30 mL/min.", "Sangramento ativo, plaquetas < 50.000/mm³."),
                    _rx("rx_timi_sca_mod_bb", "Metoprolol (Succinato ou Tartarato) se sem congestão", "25 a 50 mg VO a cada 12h (alvo FC 50-60 bpm)", "Via Oral", "12/12h", "Iniciar via oral apenas em paciente euvolêmico.", "Sem ajuste renal significativo.", "Killip >= II (estertores pulmonares), FC < 60 bpm, PAS < 100 mmHg, BAV de 2º/3º grau ou broncoespasmo ativo.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_sca_mod_1", "Internação em UCO e Cinecoronariografia", "Unidade Coronariana (UCO)", "Monitorização contínua de ST e arritmias.", proc="Cinecoronariografia (Cateterismo Cardíaco) durante a internação (idealmente < 24h se troponina positiva ou infra de ST).", lab="Curva de troponina, BNP, ecocardiograma transtorácico para avaliação de FEVE e contratilidade segmentar.")
                ]
            },
            {
                "id": "tier_timi_sca_high",
                "label": "Alto Risco (5 a 7 pontos)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 7,
                "statisticalOutcome": "Risco em 14 dias de óbito, reinfarto ou isquemia refratária: 26,2% (5 pts) a 40,9% (6-7 pts). Alto risco de doença multiarterial ou tronco de coronária esquerda; requer estratégia invasiva precoce (< 24h).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_timi_sca_high_antithromb", "AAS + Ticagrelor + Anticoagulação Plena (Enoxaparina ou HNF)", "AAS 300mg + Ticagrelor 180mg VO + Enoxaparina 1 mg/kg SC 12/12h (ou HNF IV)", "VO / SC / IV", "Contínua / 12/12h", "Se altíssimo risco de cirurgia de revascularização (CRM) de urgência, considerar postergar P2Y12 até conhecer anatomia no cateterismo.", "Ajustar enoxaparina se ClCr < 30 mL/min.", "Sangramento ativo ou história de AVC hemorrágico."),
                    _rx("rx_timi_sca_high_ntg", "Nitroglicerina Endovenosa (Tridil)", "10 a 200 mcg/min IV em BIC para controle de isquemia persistente ou congestão", "Intravenosa contínua em BIC", "Contínua", "50 mg (10 mL) em 240 mL SG 5% (200 mcg/mL) em frasco de vidro/polietileno.", "Sem ajuste renal.", "Hipotensão (PAS < 90 mmHg), infarto de VD ou uso recente de inibidores da PDE-5.", NITROGLYCERIN_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_sca_high_1", "Estratégia Invasiva Precoce (< 24h) ou Imediata (< 2h)", "UTI / Unidade Coronariana / Sala de Hemodinâmica", "Monitorização hemodinâmica invasiva ou contínua rigorosa.", proc="Cateterismo cardíaco precoce (< 24h) com revascularização percutânea (ICP com stent farmacológico) ou cirúrgica (CRM) conforme SYNTAX Score e Heart Team.", vasc="Preservar artéria radial direita para acesso transradial; punção venosa periférica contralateral.", lab="Troponina hs, gasometria se dispneia, lactato, função renal, eletrólitos (manter K > 4,0 mEq/L e Mg > 2,0 mg/dL).")
                ],
                "infusionProtocol": NITROGLYCERIN_PROTOCOL
            }
        ]
    }


def get_timi_stemi() -> dict:
    return {
        "id": "calc_timi_stemi",
        "slug": "timi-stemi",
        "name": "TIMI Risk Score para IAMCSST (STEMI)",
        "acronym": "TIMI-STEMI",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Infarto Agudo do Miocárdio com Supra de ST",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Síndromes Coronarianas Agudas",
        "description": "Escore prognóstico à beira do leito (0 a 14 pontos) validado para estimar a mortalidade em 30 dias em pacientes com Infarto Agudo do Miocárdio com Supradesnivelamento do Segmento ST (IAMCSST / STEMI).",
        "summary": "Predição de mortalidade em 30 dias no IAM com Supradesnivelamento de ST (0 a 14 pontos).",
        "clinicalObjective": "Quantificar rapidamente o risco de óbito em 30 dias no IAMCSST a partir de 8 variáveis clínicas simples na admissão, identificando pacientes candidatos a suporte hemodinâmico avançado e transferência prioritária.",
        "targetPopulation": "Pacientes adultos com IAMCSST (< 12h de evolução) elegíveis para terapia de reperfusão (ICP primária ou fibrinólise).",
        "calculationType": "additive_points",
        "formulaExpression": "Idade + DM_HAS_Angina + PAS_100 + FC_100 + Killip_II_IV + Peso_67 + SupraAnterior_BRE + TempoReperfusao_4h",
        "evidenceSource": "Morrow DA, Antman EM, Charlesworth A, et al. TIMI risk score for ST-elevation myocardial infarction: A convenient, bedside, clinical score for risk assessment at presentation. Circulation. 2000;102(17):2031-2037.",
        "minPossibleScore": 0,
        "maxPossibleScore": 14,
        "baseScore": 0,
        "badge": "emergencia",
        "clinicalWarning": "TEMPO É MÚSCULO: O cálculo do TIMI-STEMI jamais deve atrasar a ativação da hemodinâmica (meta porta-balão <= 60-90 min) ou a infusão do fibrinolítico (meta porta-agulha <= 30 min se ICP indisponível em <= 120 min). Escores >= 5 indicam mortalidade > 12% em 30 dias.",
        "radarAxes": [
            _axis("axis_timi_st_age", "Reserva Etária e Antropometria", "Cardiovascular", "pts"),
            _axis("axis_timi_st_hemo", "Instabilidade Hemodinâmica (PAS/FC/Killip)", "Cardiovascular", "pts"),
            _axis("axis_timi_st_territory", "Território Isquêmico (Parede Anterior/BRE)", "Cardiovascular", "pts"),
            _axis("axis_timi_st_time", "Atraso de Reperfusão e Comorbidades", "Vascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_timi_st_1", "1. Faixa Etária", "timi-stemi-idade", "axis_timi_st_age", 1, "A idade é o mais forte preditor isolado de mortalidade no IAMCSST.", [
                _opt("opt_timi_st_1_0", "< 65 anos (0 pts)", 0, True, 0.0, 1, "Idade inferior a 65 anos."),
                _opt("opt_timi_st_1_2", "65 a 74 anos (2 pts)", 2, False, 0.66, 2, "Faixa etária de 65 a 74 anos."),
                _opt("opt_timi_st_1_3", ">= 75 anos (3 pts)", 3, False, 1.0, 3, "Idoso >= 75 anos (alto risco de complicações mecânicas e choque)."),
            ]),
            _grp("grp_timi_st_2", "2. Antecedente de Diabetes, Hipertensão ou Angina", "timi-stemi-comorbidades", "axis_timi_st_time", 2, "Presença de pelo menos uma das três condições na história clínica.", [
                _opt("opt_timi_st_2_0", "Ausente — Sem DM, HAS ou Angina prévia (0 pts)", 0, True, 0.0, 1, "Sem histórico de diabetes, hipertensão ou angina."),
                _opt("opt_timi_st_2_1", "Presente — História de DM, HAS ou Angina pectoris (1 pt)", 1, False, 1.0, 2, "Presença de pelo menos uma comorbidade vascular maior."),
            ]),
            _grp("grp_timi_st_3", "3. Pressão Arterial Sistólica (PAS) na Admissão", "timi-stemi-pas", "axis_timi_st_hemo", 3, "Aferição da PAS inicial na chegada à emergência.", [
                _opt("opt_timi_st_3_0", "PAS >= 100 mmHg (0 pts)", 0, True, 0.0, 1, "Pressão sistólica preservada."),
                _opt("opt_timi_st_3_3", "PAS < 100 mmHg (3 pts)", 3, False, 1.0, 2, "Hipotensão arterial admissional (forte preditor de pré-choque ou choque cardiogênico)."),
            ]),
            _grp("grp_timi_st_4", "4. Frequência Cardíaca (FC) na Admissão", "timi-stemi-fc", "axis_timi_st_hemo", 4, "Frequência cardíaca basal no ECG de admissão.", [
                _opt("opt_timi_st_4_0", "FC <= 100 bpm (0 pts)", 0, True, 0.0, 1, "Frequência cardíaca controlada."),
                _opt("opt_timi_st_4_2", "FC > 100 bpm (2 pts)", 2, False, 1.0, 2, "Taquicardia sinusal reflexa por hiperatividade simpática ou disfunção ventricular esquerda."),
            ]),
            _grp("grp_timi_st_5", "5. Classificação de Killip-Kimball na Admissão", "timi-stemi-killip", "axis_timi_st_hemo", 5, "Presença de sinais clínicos de insuficiência ventricular esquerda aguda.", [
                _opt("opt_timi_st_5_0", "Killip I — Sem sinais de congestão pulmonar (0 pts)", 0, True, 0.0, 1, "Ausculta pulmonar limpa, sem B3 ou turgência jugular."),
                _opt("opt_timi_st_5_2", "Killip II a IV — Estertores, B3, EAP ou Choque Cardiogênico (2 pts)", 2, False, 1.0, 2, "Evidência clínica de falência de bomba ventricular esquerda."),
            ]),
            _grp("grp_timi_st_6", "6. Peso Corporal", "timi-stemi-peso", "axis_timi_st_age", 6, "Peso corporal estimado ou aferido na admissão.", [
                _opt("opt_timi_st_6_0", "Peso >= 67 kg (0 pts)", 0, True, 0.0, 1, "Peso corporal >= 67 kg."),
                _opt("opt_timi_st_6_1", "Peso < 67 kg (1 pt)", 1, False, 1.0, 2, "Baixo peso corporal (< 67 kg): associado a menor calibre coronariano e maior risco hemorrágico."),
            ]),
            _grp("grp_timi_st_7", "7. Localização do Infarto no ECG", "timi-stemi-ecg", "axis_timi_st_territory", 7, "Território eletrocardiográfico acometido.", [
                _opt("opt_timi_st_7_0", "Parede Inferior, Lateral ou Dorsal isolada (0 pts)", 0, True, 0.0, 1, "Supradesnivelamento restrito a derivações inferiores/laterais."),
                _opt("opt_timi_st_7_1", "Supra de ST Anterior (V1-V4) ou Bloqueio de Ramo Esquerdo (BRE) novo (1 pt)", 1, False, 1.0, 2, "Acometimento territorial extenso de artéria descendente anterior (ADA) ou tronco."),
            ]),
            _grp("grp_timi_st_8", "8. Tempo do Início da Dor até o Tratamento de Reperfusão", "timi-stemi-tempo", "axis_timi_st_time", 8, "Delta T total de isquemia (início dos sintomas até abertura da artéria/fibrinólise).", [
                _opt("opt_timi_st_8_0", "Tempo <= 4 horas (0 pts)", 0, True, 0.0, 1, "Reperfusão precoce com alto salvamento miocárdico."),
                _opt("opt_timi_st_8_1", "Tempo > 4 horas (1 pt)", 1, False, 1.0, 2, "Isquemia prolongada (> 4h) com maior extensão de necrose transmural."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_timi_st_low",
                "label": "Baixo Risco no IAMCSST (0 a 2 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade em 30 dias de 0,8% (0 pts), 1,6% (1 pt) a 2,2% (2 pts). Excelente prognóstico pós-reperfusão primária bem-sucedida.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_timi_st_low_dapt", "AAS + Prasugrel ou Ticagrelor (para ICP Primária) / Clopidogrel (se Fibrinólise)", "AAS 300mg VO + Ticagrelor 180mg VO (ou Prasugrel 60mg se anatomia conhecida; ou Clopidogrel 300mg se trombólise)", "Via Oral", "Dose de ataque imediata", "Se >= 75 anos submetido a fibrinólise, fazer Clopidogrel 75mg sem dose de ataque.", "Sem ajuste renal para antiagregantes.", "Prasugrel contraindicado em AVC/AIT prévio; reduzir manutenção para 5mg se < 60 kg ou >= 75 anos.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_st_low_1", "Angioplastia Primária Imediata e UCO", "Sala de Hemodinâmica -> Unidade Coronariana", "Monitorização contínua em UCO por 24-48h pós-ICP primária sem complicações; considerar alta hospitalar precoce em 48-72h se FEVE preservada.", proc="Angioplastia Coronariana Transluminal Percutânea (ICP) Primária em <= 90 minutos.", lab="Troponina, CK-MB, perfil lipídico, HbA1c, função renal, Ecocardiograma antes da alta.")
                ]
            },
            {
                "id": "tier_timi_st_mod",
                "label": "Risco Intermediário no IAMCSST (3 a 5 pontos)",
                "severityLevel": "intermediate",
                "minScore": 3,
                "maxScore": 5,
                "statisticalOutcome": "Mortalidade em 30 dias de 4,4% (3 pts), 7,3% (4 pts) a 12,4% (5 pts). Requer vigilância intensiva para disfunção ventricular esquerda e arritmias ventriculares.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_timi_st_mod_reperf", "Terapia de Reperfusão + Anticoagulação + IECA/Betabloqueador nas primeiras 24h", "HNF 70-100 UI/kg IV na ICP (ou Tenecteplase IV em bolus conforme peso + Enoxaparina se fibrinólise)", "Intravenosa / SC", "Protocolo de Reperfusão", "Tenecteplase: <60kg=30mg; 60-69kg=35mg; 70-79kg=40mg; 80-89kg=45mg; >=90kg=50mg (reduzir 50% da dose se >= 75 anos no protocolo STREAM).", "Ajustar Enoxaparina se ClCr < 30 mL/min.", "Contraindicações absolutas à trombólise: AVC hemorrágico prévio, AVCi < 3 meses, neoplasia SNC, dissecção de aorta, sangramento ativo.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_st_mod_1", "Reperfusão de Emergência e Ecocardiografia Precoce", "UTI Cardiológica / UCO", "Monitorização contínua de ritmo, PA e balanço hídrico; ECG 60-90 min pós-fibrinólise para avaliar redução >= 50% do supra de ST (se falha, angioplastia de resgate imediata).", proc="ICP Primária ou Estratégia Fármaco-Invasiva (cateterismo em 2-24h pós-fibrinólise).", lab="Eletrólitos (manter K > 4,0 e Mg > 2,0), função renal, lactato, Ecocardiograma transtorácico.")
                ]
            },
            {
                "id": "tier_timi_st_high",
                "label": "Alto / Altíssimo Risco no IAMCSST (6 a 14 pontos)",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 14,
                "statisticalOutcome": "Mortalidade em 30 dias de 16,1% (6 pts), 23,4% (7 pts), 26,8% (8 pts) e 35,9% (> 8 pts). Elevadíssimo risco de choque cardiogênico, edema agudo de pulmão e óbito intra-hospitalar.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_timi_st_high_norepi", "Noradrenalina (se Choque Cardiogênico com PAS < 90 mmHg / PAM < 65 mmHg)", "0,05 a 1,0 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL).", "Sem ajuste renal.", "Evitar doses excessivas sem suporte inotrópico pelo aumento da pós-carga ventricular esquerda.", NOREPINEPHRINE_PROTOCOL),
                    _rx("rx_timi_st_high_dobuta", "Dobutamina (Inotrópico de escolha no Choque Cardiogênico Isquêmico)", "2,5 a 15 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "1 ampola (250 mg = 20 mL) em 230 mL SG 5% ou SF 0,9% (1.000 mcg/mL).", "Sem ajuste renal.", "Taquiarritmias ventriculares não controladas ou obstrução dinâmica da VSVE.", DOBUTAMINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_timi_st_high_1", "Reperfusão Mecânica da Artéria Culpada (Estudo CULPRIT-SHOCK) e UTI", "Sala de Hemodinâmica -> UTI Cardiológica", "PAI invasiva, CVC, sonda vesical de demora, monitorização de ScvO2 e lactato a cada 2-4h.", proc="ICP Primária imediata focada exclusivamente na artéria culpada no choque cardiogênico (CULPRIT-SHOCK); considerar suporte circulatório mecânico (BIA / Impella / ECMO-VA) em choque refratário e descartar complicações mecânicas ao Eco (CIV, ruptura de músculo papilar ou parede livre).", vent="VNI (CPAP/BiPAP) se EAP sem choque grave; Intubação Orotraqueal precoce se choque cardiogênico refratário para reduzir consumo de O2 da musculatura respiratória.", vasc="Acesso arterial radial/femoral + CVC jugular/subclávio + PAI.", lab="Gasometria arterial e venosa central, lactato seriado, troponina, função renal, coagulograma.")
                ],
                "infusionProtocol": DOBUTAMINE_PROTOCOL
            }
        ]
    }


def get_grace() -> dict:
    return {
        "id": "calc_grace",
        "slug": "grace-score",
        "name": "GRACE Risk Score 2.0 (Global Registry of Acute Coronary Events)",
        "acronym": "GRACE",
        "version": "2.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Síndrome Coronariana Aguda",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Síndromes Coronarianas Agudas",
        "description": "Padrão-ouro das diretrizes ESC/AHA/SBC para estratificação prognóstica de mortalidade intra-hospitalar e em 6 meses em todo o espectro da Síndrome Coronariana Aguda (IAMCSST, IAMSSST e Angina Instável), integrando 8 variáveis clínicas, hemodinâmicas, eletrocardiográficas e laboratoriais.",
        "summary": "Predição de mortalidade intra-hospitalar e em 6 meses na SCA e definição de cateterismo precoce < 24h (1 a 372 pontos).",
        "clinicalObjective": "Identificar pacientes com SCASST de alto risco (GRACE > 140) que se beneficiam de estratégia invasiva precoce (< 24 horas, Classe I pelas diretrizes ESC/SBC).",
        "targetPopulation": "Pacientes adultos admitidos com diagnóstico de Síndrome Coronariana Aguda (com ou sem supradesnivelamento de ST).",
        "calculationType": "additive_points",
        "formulaExpression": "Idade + FC + PAS + Creatinina + Killip + PCR_Admissao + Desvio_ST + Troponina_Elevada",
        "evidenceSource": "Granger CB, Goldberg RJ, Dabbous O, et al. Predictors of hospital mortality in the global registry of acute coronary events. Arch Intern Med. 2003;163(19):2345-2353. ESC ACS Guidelines 2023.",
        "minPossibleScore": 1,
        "maxPossibleScore": 372,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "DIRETRIZ ESC / SBC DE SCASST: Pacientes com GRACE Score > 140 pontos possuem indicação Classe I para Estratégia Invasiva Precoce (cinecoronariografia em menos de 24 horas da admissão). Em presença de choque cardiogênico, angina refratária ou arritmias malignas, o cateterismo deve ser Imediato (< 2 horas) independentemente do escore.",
        "radarAxes": [
            _axis("axis_grace_hemo", "Hemodinâmica (FC, PAS e Killip)", "Cardiovascular", "pts"),
            _axis("axis_grace_renal_age", "Reserva Etária e Renal (Creatinina)", "Renal", "pts"),
            _axis("axis_grace_ischemia", "Injúria e Eletrocardiograma (ST e Troponina)", "Cardiovascular", "pts"),
            _axis("axis_grace_arrest", "Evento Arrítmico Crítico (PCR)", "Cardiovascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_grace_age", "1. Idade (anos)", "grace-idade", "axis_grace_renal_age", 1, "Idade do paciente na admissão hospitalar.", [
                _opt("opt_grace_age_0", "< 30 anos (0 pts)", 0, True, 0.0, 1, "Menos de 30 anos."),
                _opt("opt_grace_age_8", "30 a 39 anos (8 pts)", 8, False, 0.08, 2, "Faixa de 30 a 39 anos."),
                _opt("opt_grace_age_25", "40 a 49 anos (25 pts)", 25, False, 0.25, 3, "Faixa de 40 a 49 anos."),
                _opt("opt_grace_age_41", "50 a 59 anos (41 pts)", 41, False, 0.41, 4, "Faixa de 50 a 59 anos."),
                _opt("opt_grace_age_58", "60 a 69 anos (58 pts)", 58, False, 0.58, 5, "Faixa de 60 a 69 anos."),
                _opt("opt_grace_age_75", "70 a 79 anos (75 pts)", 75, False, 0.75, 6, "Faixa de 70 a 79 anos."),
                _opt("opt_grace_age_91", "80 a 89 anos (91 pts)", 91, False, 0.91, 7, "Faixa de 80 a 89 anos."),
                _opt("opt_grace_age_100", ">= 90 anos (100 pts)", 100, False, 1.0, 8, "90 anos ou mais."),
            ]),
            _grp("grp_grace_hr", "2. Frequência Cardíaca (FC em bpm)", "grace-fc", "axis_grace_hemo", 2, "Frequência cardíaca registrada na apresentação.", [
                _opt("opt_grace_hr_0", "< 50 bpm (0 pts)", 0, False, 0.1, 1, "Bradicardia sinusal (< 50 bpm)."),
                _opt("opt_grace_hr_3", "50 a 69 bpm (3 pts)", 3, True, 0.0, 2, "Frequência cardíaca basal fisiológica (50-69 bpm)."),
                _opt("opt_grace_hr_9", "70 a 89 bpm (9 pts)", 9, False, 0.2, 3, "Frequência cardíaca normal-alta (70-89 bpm)."),
                _opt("opt_grace_hr_15", "90 a 109 bpm (15 pts)", 15, False, 0.35, 4, "Taquicardia limítrofe (90-109 bpm)."),
                _opt("opt_grace_hr_24", "110 a 149 bpm (24 pts)", 24, False, 0.6, 5, "Taquicardia moderada (110-149 bpm)."),
                _opt("opt_grace_hr_38", "150 a 199 bpm (38 pts)", 38, False, 0.85, 6, "Taquicardia acentuada (150-199 bpm)."),
                _opt("opt_grace_hr_46", ">= 200 bpm (46 pts)", 46, False, 1.0, 7, "Taquiarritmia extrema (>= 200 bpm)."),
            ], unit="bpm"),
            _grp("grp_grace_sbp", "3. Pressão Arterial Sistólica (PAS em mmHg)", "grace-pas", "axis_grace_hemo", 3, "Quanto menor a PAS na admissão, maior a pontuação de risco de choque.", [
                _opt("opt_grace_sbp_0", ">= 200 mmHg (0 pts)", 0, False, 0.1, 1, "Hipertensão severa na admissão."),
                _opt("opt_grace_sbp_10", "160 a 199 mmHg (10 pts)", 10, False, 0.15, 2, "PAS 160-199 mmHg."),
                _opt("opt_grace_sbp_24", "140 a 159 mmHg (24 pts)", 24, False, 0.25, 3, "PAS 140-159 mmHg."),
                _opt("opt_grace_sbp_34", "120 a 139 mmHg (34 pts)", 34, True, 0.0, 4, "PAS normotensa (120-139 mmHg)."),
                _opt("opt_grace_sbp_43", "100 a 119 mmHg (43 pts)", 43, False, 0.5, 5, "PAS limítrofe (100-119 mmHg)."),
                _opt("opt_grace_sbp_53", "80 a 99 mmHg (53 pts)", 53, False, 0.85, 6, "Hipotensão arterial (80-99 mmHg)."),
                _opt("opt_grace_sbp_58", "< 80 mmHg (58 pts)", 58, False, 1.0, 7, "Hipotensão severa / Choque franco (< 80 mmHg)."),
            ], unit="mmHg"),
            _grp("grp_grace_cr", "4. Creatinina Sérica Inicial (mg/dL)", "grace-creatinina", "axis_grace_renal_age", 4, "Dosagem sérica de creatinina na admissão.", [
                _opt("opt_grace_cr_1", "0,0 a 0,39 mg/dL (1 pt)", 1, False, 0.0, 1, "Creatinina muito baixa."),
                _opt("opt_grace_cr_4", "0,40 a 0,79 mg/dL (4 pts)", 4, True, 0.0, 2, "Creatinina normal baixa."),
                _opt("opt_grace_cr_7", "0,80 a 1,19 mg/dL (7 pts)", 7, False, 0.1, 3, "Creatinina normal."),
                _opt("opt_grace_cr_10", "1,20 a 1,59 mg/dL (10 pts)", 10, False, 0.35, 4, "Disfunção renal leve (1,20-1,59 mg/dL)."),
                _opt("opt_grace_cr_13", "1,60 a 1,99 mg/dL (13 pts)", 13, False, 0.55, 5, "Disfunção renal moderada (1,60-1,99 mg/dL)."),
                _opt("opt_grace_cr_21", "2,00 a 3,99 mg/dL (21 pts)", 21, False, 0.8, 6, "Disfunção renal importante (2,00-3,99 mg/dL)."),
                _opt("opt_grace_cr_28", ">= 4,00 mg/dL (28 pts)", 28, False, 1.0, 7, "Insuficiência renal grave ou dialítica (>= 4,0 mg/dL)."),
            ], unit="mg/dL"),
            _grp("grp_grace_killip", "5. Classe de Killip na Admissão", "grace-killip", "axis_grace_hemo", 5, "Grau de insuficiência cardíaca aguda na apresentação.", [
                _opt("opt_grace_k_1", "Killip I — Sem congestão pulmonar (0 pts)", 0, True, 0.0, 1, "Ausculta pulmonar limpa, sem B3."),
                _opt("opt_grace_k_2", "Killip II — Estertores em bases (< 50%), B3 ou TJP (20 pts)", 20, False, 0.35, 2, "Congestão pulmonar leve a moderada."),
                _opt("opt_grace_k_3", "Killip III — Edema Agudo de Pulmão (> 50% dos campos) (39 pts)", 39, False, 0.7, 3, "Edema agudo de pulmão franco."),
                _opt("opt_grace_k_4", "Killip IV — Choque Cardiogênico (PAS < 90 + hipoperfusão) (59 pts)", 59, False, 1.0, 4, "Colapso circulatório cardiogênico."),
            ]),
            _grp("grp_grace_pcr", "6. Parada Cardiorrespiratória (PCR) na Admissão", "grace-pcr", "axis_grace_arrest", 6, "Ocorrência de PCR pré-hospitalar ou na chegada à emergência com retorno da circulação espontânea.", [
                _opt("opt_grace_pcr_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem parada cardíaca na apresentação."),
                _opt("opt_grace_pcr_39", "Presente — PCR reanimada na admissão (39 pts)", 39, False, 1.0, 2, "FV/TV sem pulso ou AESP/Assistolia revertida na chegada."),
            ]),
            _grp("grp_grace_st", "7. Desvio do Segmento ST no ECG Inicial", "grace-desvio-st", "axis_grace_ischemia", 7, "Infradesnivelamento ou supradesnivelamento agudo do segmento ST.", [
                _opt("opt_grace_st_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem desvio significativo do segmento ST."),
                _opt("opt_grace_st_28", "Presente — Desvio de ST >= 0,5-1,0 mm (28 pts)", 28, False, 1.0, 2, "Desvio dinâmico do segmento ST indicando isquemia subendocárdica ou transmural."),
            ]),
            _grp("grp_grace_trop", "8. Biomarcadores de Necrose Miocárdica Elevados", "grace-troponina", "axis_grace_ischemia", 8, "Troponina cardíaca (hs-cTnI / hs-cTnT) acima do percentil 99.", [
                _opt("opt_grace_trop_0", "Normais / Negativos (0 pts)", 0, True, 0.0, 1, "Marcadores de necrose dentro da faixa normal."),
                _opt("opt_grace_trop_14", "Elevados (Troponina positiva > p99) (14 pts)", 14, False, 1.0, 2, "Injúria miocárdica aguda confirmada laboratorialmente."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_grace_low",
                "label": "Baixo Risco (1 a 108 pontos)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 108,
                "statisticalOutcome": "Mortalidade intra-hospitalar < 1% (mortalidade em 6 meses < 3% se escore <= 88). Na SCASST sem critérios de alto risco, permite estratégia invasiva seletiva ou teste não invasivo.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_grace_low_1", "AAS + Estatina de Alta Potência + Antianginoso", "AAS 100mg/dia (após ataque 300mg) + Atorvastatina 80mg/dia + Metoprolol 25-50mg 12/12h", "Via Oral", "Diário", "Administrar por via oral.", "Sem ajuste renal para AAS e Atorvastatina.", "Bradicardia ou hipotensão para betabloqueador.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_grace_low_1", "Estratificação Seletiva ou Anatômica Não Invasiva", "Unidade de Dor Torácica / Enfermaria", "Monitorização clínica e ECG seriado; curva de troponina de alta sensibilidade.", proc="Angio-TC de coronárias ou teste funcional de isquemia antes da alta hospitalar.", lab="Troponina hs, perfil lipídico, glicemia, creatinina.")
                ]
            },
            {
                "id": "tier_grace_mod",
                "label": "Risco Intermediário (109 a 140 pontos)",
                "severityLevel": "intermediate",
                "minScore": 109,
                "maxScore": 140,
                "statisticalOutcome": "Mortalidade intra-hospitalar de 1% a 3% (mortalidade em 6 meses de 3% a 8%). Indicação de internação em Unidade Coronariana e cinecoronariografia durante a internação (< 24 a 72h).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_grace_mod_1", "Dupla Antiagregação (AAS + Ticagrelor/Clopidogrel) + Enoxaparina", "AAS 300mg + Ticagrelor 180mg VO + Enoxaparina 1 mg/kg SC 12/12h (ou Fondaparinux 2,5mg SC 1x/dia)", "VO e SC", "12/12h ou 24/24h", "Se usar Fondaparinux (estudo OASIS-5), associar obrigatoriamente bolus de HNF 85 UI/kg durante a angioplastia para evitar trombose de cateter.", "Fondaparinux contraindicado se ClCr < 20 mL/min; Enoxaparina 1 mg/kg 1x/dia se ClCr 15-30 mL/min.", "Sangramento ativo.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_grace_mod_1", "Internação em UCO e Cateterismo Cardíaco", "Unidade Coronariana (UCO)", "Telemetria contínua, vigilância de função renal e balanço hídrico.", proc="Cinecoronariografia em até 24-72h.", lab="Ecocardiograma transtorácico, troponina, BNP, função renal.")
                ]
            },
            {
                "id": "tier_grace_high",
                "label": "Alto Risco (141 a 372 pontos)",
                "severityLevel": "critical",
                "minScore": 141,
                "maxScore": 372,
                "statisticalOutcome": "Mortalidade intra-hospitalar > 3% (chegando a > 20-40% em escores > 200 com Killip III/IV). Indicação Classe I de Estratégia Invasiva Precoce (< 24h) ou Imediata (< 2h se instabilidade).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_grace_high_1", "Terapia Antitrombótica Plena + Suporte Vasoativo / Anti-isquêmico", "AAS 300mg + Inibidor P2Y12 + HNF IV ou Enoxaparina SC", "VO / IV / SC", "Contínua", "Em pacientes instáveis ou candidatos a cateterismo imediato, preferir HNF IV pela meia-vida curta e reversibilidade com protamina.", "HNF não exige ajuste renal inicial (titular por TTPa 1,5-2,5x).", "Sangramento ativo grave."),
                    _rx("rx_grace_high_dob", "Dobutamina / Noradrenalina se Killip III-IV ou Choque Cardiogênico", "Dobutamina 2,5-15 mcg/kg/min + Noradrenalina 0,05-1,0 mcg/kg/min IV em BIC", "Intravenosa contínua em BIC", "Contínua", "Dobutamina 250mg em 230 mL SG 5% (1.000 mcg/mL); Noradrenalina 16mg em 234 mL SG 5% (64 mcg/mL).", "Sem ajuste renal.", "Taquiarritmias ventriculares malignas sem controle.", DOBUTAMINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_grace_high_1", "Estratégia Invasiva Precoce (< 24h) / Imediata (< 2h) em UTI Cardiológica", "UTI Cardiológica / Hemodinâmica", "Monitorização hemodinâmica invasiva (PAI) se PAS < 90 mmHg ou Killip >= III.", proc="Cinecoronariografia precoce (< 24h) com revascularização da artéria culpada; suporte mecânico se choque refratário.", vasc="Acesso radial para ICP; CVC se uso de aminas vasoativas.", lab="Gasometria arterial/venosa, lactato, troponina hs, função renal, eletrólitos.")
                ],
                "infusionProtocol": DOBUTAMINE_PROTOCOL
            }
        ]
    }


def get_killip() -> dict:
    return {
        "id": "calc_killip",
        "slug": "killip-kimball",
        "name": "Classificação de Killip-Kimball no Infarto Agudo do Miocárdio",
        "acronym": "Killip",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Insuficiência Cardíaca Aguda e Choque Cardiogênico",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Síndromes Coronarianas Agudas e Hemodinâmica",
        "description": "Classificação clínica e hemodinâmica clássica à beira do leito (Classes I a IV) para quantificar o grau de falência ventricular esquerda aguda e estimar a mortalidade hospitalar em pacientes com Infarto Agudo do Miocárdio.",
        "summary": "Estratificação clínica de congestão pulmonar e choque cardiogênico no IAM (Classes I a IV, 1 a 4 pontos).",
        "clinicalObjective": "Guiar o manejo hemodinâmico imediato no IAM (liberação cautelosa de betabloqueadores no Killip I vs. vasodilatadores/VNI no Killip III vs. suporte inotrópico/vasopressor e reperfusão mecânica de emergência no Killip IV).",
        "targetPopulation": "Pacientes adultos admitidos com Infarto Agudo do Miocárdio (com ou sem supradesnivelamento de ST).",
        "calculationType": "additive_points",
        "formulaExpression": "Classe_Killip_I_a_IV",
        "evidenceSource": "Killip T 3rd, Kimball JT. Treatment of myocardial infarction in a coronary care unit. A two year experience with 250 patients. Am J Cardiol. 1967;20(4):457-464.",
        "minPossibleScore": 1,
        "maxPossibleScore": 4,
        "baseScore": 0,
        "badge": "emergencia",
        "clinicalWarning": "PROIBIÇÃO DE BETABLOQUEADOR EM CONGESTÃO AGUDA: Em pacientes com Killip >= II (estertores pulmonares, B3, edema agudo de pulmão ou choque cardiogênico), a administração precoce de betabloqueadores (especialmente venosos) é formalmente contraindicada pelo risco de precipitar choque cardiogênico fatal (Estudo COMMIT).",
        "radarAxes": [
            _axis("axis_killip_cong", "Congestão Venocapilar Pulmonar", "Respiratório", "classe"),
            _axis("axis_killip_output", "Débito Cardíaco e Perfusão Tecidual", "Cardiovascular", "classe"),
            _axis("axis_killip_fill", "Pressão de Enchimento de VE (B3/TJP)", "Cardiovascular", "classe"),
        ],
        "parameterGroups": [
            _grp("grp_killip_class", "Classificação Clínica de Killip-Kimball à Beira do Leito", "killip-classe", "axis_killip_output", 1, "Avaliação simultânea da ausculta pulmonar, presença de 3ª bulha (B3), turgência jugular patológica (TJP) e perfusão periférica/PAS.", [
                _opt("opt_killip_1", "Classe I (1 pt) — Sem sinais clínicos de insuficiência cardíaca (ausculta limpa, sem B3)", 1, True, 0.0, 1, "Campos pulmonares limpos à ausculta, bulhas normofonéticas sem B3 e perfusão periférica normal."),
                _opt("opt_killip_2", "Classe II (2 pts) — Estertores crepitantes em < 50% dos campos pulmonares, 3ª bulha (B3) ou turgência jugular", 2, False, 0.35, 2, "Insuficiência ventricular esquerda leve a moderada com congestão restrita às bases ou terços inferiores."),
                _opt("opt_killip_3", "Classe III (3 pts) — Edema Agudo de Pulmão franco (estertores em > 50% dos campos pulmonares)", 3, False, 0.75, 3, "Edema alveolar difuso com insuficiência respiratória hipoxêmica aguda e ortopneia dramática."),
                _opt("opt_killip_4", "Classe IV (4 pts) — Choque Cardiogênico (PAS < 90 mmHg com oligúria, extremidades frias, lactato alto e confusão)", 4, False, 1.0, 4, "Colapso circulatório cardiogênico por perda crítica de massa contrátil ventricular (> 40% do VE) ou complicação mecânica."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_killip_1",
                "label": "Killip I — Sem Insuficiência Cardíaca (1 ponto)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Mortalidade intra-hospitalar contemporânea de 2% a 6%. Hemodinâmica preservada permitindo introdução segura de neuro-hormonais orais nas primeiras 24h.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_killip_1_bb_ieca", "Terapia Padrão Pós-IAM (DAPT + Estatina + Betabloqueador oral + IECA)", "Metoprolol 25-50mg VO 12/12h + Enalapril 2,5-5mg VO 12/12h (ou Ramipril) nas primeiras 24h", "Via Oral", "12/12 horas", "Iniciar em doses baixas e titular conforme PA e FC.", "Ajustar IECA se queda de TFG > 30% ou hipercalemia.", "Evitar IECA se PAS < 100 mmHg ou hipercalemia > 5,5 mEq/L.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_killip_1_1", "Cuidados Padrão em Unidade Coronariana", "Unidade Coronariana (UCO)", "Monitorização contínua de ECG, PA e SpO2; reavaliação da ausculta pulmonar a cada 6h.", proc="Reperfusão coronariana conforme protocolo de IAM.", lab="Troponina, função renal, eletrólitos, Ecocardiograma transtorácico.")
                ]
            },
            {
                "id": "tier_killip_2",
                "label": "Killip II — Congestão Pulmonar Leve a Moderada (2 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade intra-hospitalar estimada de 10% a 17%. Exige descongestão venosa com diurético de alça e suspensão temporária de betabloqueadores até compensação.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_killip_2_furo", "Furosemida Endovenosa", "20 a 40 mg IV em bolus lento (ou 1-2x a dose diária domiciliar prévia)", "Intravenosa", "Bolus inicial; repetir de 6/6h ou 8/8h conforme diurese", "Administrar sem diluição ou diluído em 10 mL SF 0,9% lento.", "Doses maiores (40-80 mg) podem ser necessárias se DRC prévia.", "Hipovolemia, hipocalemia grave não corrigida ou infarto isolado de ventrículo direito.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_killip_2_1", "Manejo de Congestão Pulmonar em UCO", "Unidade Coronariana (UCO)", "Balanço hídrico rigoroso (meta negativa), cabeceira elevada a 45°, restrição hídrica e sódica.", vent="Oxigenoterapia sob cateter nasal ou máscara se SpO2 < 90%.", lab="Sódio, potássio, magnésio, ureia, creatinina, BNP/NT-proBNP, radiografia de tórax e ultrassom pulmonar (linhas B).")
                ]
            },
            {
                "id": "tier_killip_3",
                "label": "Killip III — Edema Agudo de Pulmão (3 pontos)",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade intra-hospitalar de 30% a 38%. Emergência cardiopulmonar crítica exigindo VNI imediata, vasodilatação venosa/arterial em BIC e diurético de alça.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    _rx("rx_killip_3_ntg", "Nitroglicerina Endovenosa (Tridil) em BIC", "10 a 200 mcg/min IV contínua (titular a cada 5 min se PAS > 100 mmHg)", "Intravenosa contínua em BIC", "Contínua", "1 ampola (50 mg/10 mL) em 240 mL SG 5% ou SF 0,9% (200 mcg/mL) em frasco de vidro/polietileno.", "Sem ajuste renal.", "PAS < 90 mmHg, estenose aórtica crítica, infarto de VD ou uso recente de sildenafil/tadalafil.", NITROGLYCERIN_PROTOCOL),
                    _rx("rx_killip_3_furo", "Furosemida Endovenosa", "40 a 80 mg IV em bolus", "Intravenosa", "Bolus imediato", "Puro ou diluído em SF 0,9%.", "Monitorar calemia e função renal.", "Choque hipovolêmico.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_killip_3_1", "Ventilação Não Invasiva (VNI) Imediata e Cateterismo de Urgência", "UTI Cardiológica / Sala Vermelha", "Monitorização contínua multiparamétrica, sondagem vesical para controle horário de diurese.", proc="Cinecoronariografia de urgência (< 2h) após estabilização ventilatória; Ecocardiograma urgente para avaliar válvula mitral e FEVE.", vent="VNI com pressão positiva (CPAP 8-10 cmH2O ou BiPAP IPAP 12-16 / EPAP 6-8 cmH2O) imediata para reduzir pré e pós-carga do VE.", lab="Gasometria arterial, lactato, eletrólitos, troponina, BNP.")
                ],
                "infusionProtocol": NITROGLYCERIN_PROTOCOL
            },
            {
                "id": "tier_killip_4",
                "label": "Killip IV — Choque Cardiogênico (4 pontos)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Mortalidade intra-hospitalar de 50% a 80% se não reperfundido imediatamente. Requer revascularização imediata da artéria culpada (CULPRIT-SHOCK), inotrópico + vasopressor e ecocardiograma imediato à beira do leito.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_killip_4_norepi", "Noradrenalina (Vasopressor de 1ª escolha no Choque Cardiogênico — Estudo SOAP II)", "0,05 a 1,5 mcg/kg/min IV contínua em BIC para restaurar PAM >= 65 mmHg", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL). Veículo mandatório SG 5%.", "Sem ajuste renal.", "Preferir Noradrenalina à Dopamina (menor incidência de arritmias e menor mortalidade no subgrupo cardiogênico do SOAP II).", NOREPINEPHRINE_PROTOCOL),
                    _rx("rx_killip_4_dobuta", "Dobutamina (Inotrópico Beta-1 agonista)", "2,5 a 20 mcg/kg/min IV contínua em BIC associada à Noradrenalina", "Intravenosa contínua em BIC", "Contínua", "1 ampola (250 mg = 20 mL) em 230 mL SG 5% ou SF 0,9% (1.000 mcg/mL).", "Sem ajuste renal.", "Cautela se PAS < 80 mmHg sem vasopressor concomitante devido à vasodilatação periférica beta-2.", DOBUTAMINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_killip_4_1", "Revascularização Imediata (< 2h), Ecocardiograma de Emergência e Suporte Mecânico", "Sala de Hemodinâmica -> UTI Cardiológica", "PAI radial/femoral contínua, CVC para ScvO2 (> 70%), clearance de lactato a cada 2h e diurese horária (> 0,5 mL/kg/h).", proc="Cinecoronariografia imediata com ICP exclusiva da lesão culpada (CULPRIT-SHOCK); Ecocardiograma urgente para descartar complicações mecânicas cirúrgicas (ruptura de septo interventricular, ruptura de músculo papilar com IM aguda grave ou tamponamento por ruptura de parede livre); considerar assistência circulatória mecânica.", vent="Intubação orotraqueal e ventilação mecânica invasiva precoce se insuficiência respiratória ou acidose lática refratária.", vasc="CVC + PAI + Introdutor arterial na hemodinâmica.", lab="Gasometria arterial e venosa central, lactato, função renal, transaminases (hepatite hipóxico-isquêmica), coagulograma.")
                ],
                "infusionProtocol": DOBUTAMINE_PROTOCOL
            }
        ]
    }


def get_cha2ds2_vasc() -> dict:
    return {
        "id": "calc_cha2ds2_vasc",
        "slug": "cha2ds2-vasc",
        "name": "CHA2DS2-VASc Score para Risco Tromboembólico na Fibrilação Atrial",
        "acronym": "CHA2DS2-VASc",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Arritmias Cardíacas e Anticoagulação",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Arritmias e Tromboembolismo",
        "description": "Escore clínico padrão (0 a 9 pontos) para estratificação do risco anual de acidente vascular cerebral isquêmico (AVCi), ataque isquêmico transitório (AIT) e embolia sistêmica em pacientes com Fibrilação Atrial (FA) ou Flutter Atrial não valvar.",
        "summary": "Estratificação do risco anual de AVC e tromboembolismo na Fibrilação Atrial (0 a 9 pontos).",
        "clinicalObjective": "Identificar pacientes de verdadeiro baixo risco tromboembólico que não necessitam de anticoagulação e pacientes com indicação formal (Classe I ou IIa) de anticoagulação oral crônica (DOACs ou Varfarina).",
        "targetPopulation": "Pacientes adultos com Fibrilação Atrial ou Flutter Atrial não valvar (ausência de prótese valvar mecânica ou estenose mitral moderada a grave).",
        "calculationType": "additive_points",
        "formulaExpression": "ICC_1 + HAS_1 + Idade(0_1_2) + DM_1 + AVC_AIT_2 + DoencaVascular_1 + SexoFeminino_1",
        "evidenceSource": "Lip GY, Nieuwlaat R, Pisters R, Lane DA, Crijns HJ. Refining clinical risk stratification for predicting stroke and thromboembolism in atrial fibrillation using a novel risk factor-based approach: the euro heart survey on atrial fibrillation. Chest. 2010;137(2):263-272.",
        "minPossibleScore": 0,
        "maxPossibleScore": 9,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "EXCEÇÕES DE FA VALVAR: Pacientes com prótese valvar cardíaca mecânica ou estenose mitral reumática moderada a grave têm indicação obrigatória de anticoagulação com antagonista da vitamina K (Varfarina) independentemente do escore CHA2DS2-VASc, sendo os DOACs contraindicados nesse grupo (Estudos RE-ALIGN e INVICTUS). O sexo feminino é um modificador de risco dependente da idade e isoladamente (1 pt sem outros fatores) não indica anticoagulação.",
        "radarAxes": [
            _axis("axis_cha_neuro", "Histórico Tromboembólico / AVC Prévio", "Neurológico", "pts"),
            _axis("axis_cha_age", "Fator Etário e Modificador de Sexo", "Vascular", "pts"),
            _axis("axis_cha_cardio", "Miocardiopatia (IC) e Hipertensão", "Cardiovascular", "pts"),
            _axis("axis_cha_vasc", "Diabetes e Doença Aterosclerótica", "Metabólico", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_cha_c", "1. C — Congestive Heart Failure (Insuficiência Cardíaca / Disfunção de VE)", "cha2ds2-icc", "axis_cha_cardio", 1, "IC clínica descompensada recente ou FEVE <= 40% documentada ao ecocardiograma (ou cardiomiopatia hipertrófica).", [
                _opt("opt_cha_c_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Função ventricular preservada e ausência de sinais/sintomas de IC."),
                _opt("opt_cha_c_1", "Presente — IC clínica ou FEVE <= 40% (1 pt)", 1, False, 1.0, 2, "Estase sanguínea atrial acentuada por disfunção sistólica ou diastólica do VE."),
            ]),
            _grp("grp_cha_h", "2. H — Hypertension (Hipertensão Arterial Sistêmica)", "cha2ds2-has", "axis_cha_cardio", 2, "PA de repouso > 140/90 mmHg em pelo menos 2 ocasiões ou em uso de anti-hipertensivos.", [
                _opt("opt_cha_h_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Normotenso sem medicação."),
                _opt("opt_cha_h_1", "Presente — Diagnóstico de HAS ou em tratamento (1 pt)", 1, False, 1.0, 2, "Remodelamento atrial esquerdo secundário à sobrecarga pressórica crônica."),
            ]),
            _grp("grp_cha_a", "3. A2 / A — Age (Faixa Etária)", "cha2ds2-idade", "axis_cha_age", 3, "Idade cronológica na avaliação.", [
                _opt("opt_cha_a_0", "< 65 anos (0 pts)", 0, True, 0.0, 1, "Idade inferior a 65 anos."),
                _opt("opt_cha_a_1", "65 a 74 anos (1 pt)", 1, False, 0.5, 2, "Risco intermediário ligado à fibrose atrial senil."),
                _opt("opt_cha_a_2", ">= 75 anos (2 pts)", 2, False, 1.0, 3, "Fator de risco maior independente para AVC cardioembólico."),
            ]),
            _grp("grp_cha_d", "4. D — Diabetes Mellitus", "cha2ds2-dm", "axis_cha_vasc", 4, "Glicemia de jejum >= 126 mg/dL, HbA1c >= 6,5% ou tratamento com hipoglicemiantes orais/insulina.", [
                _opt("opt_cha_d_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem diabetes mellitus."),
                _opt("opt_cha_d_1", "Presente — Diabetes Mellitus tipo 1 ou 2 (1 pt)", 1, False, 1.0, 2, "Estado pró-trombótico e disfunção endotelial associada ao diabetes."),
            ]),
            _grp("grp_cha_s", "5. S2 — Stroke / TIA / Thromboembolism (AVC, AIT ou Embolia Prévia)", "cha2ds2-avc", "axis_cha_neuro", 5, "Antecedente pessoal de AVC isquêmico, Ataque Isquêmico Transitório ou embolia arterial periférica/visceral.", [
                _opt("opt_cha_s_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem eventos tromboembólicos prévios."),
                _opt("opt_cha_s_2", "Presente — AVC, AIT ou Embolia Sistêmica prévia (2 pts)", 2, False, 1.0, 2, "Principal preditor de recorrência cardioembólica cerebral (indica anticoagulação isoladamente)."),
            ]),
            _grp("grp_cha_v", "6. V — Vascular Disease (Doença Vascular Aterosclerótica)", "cha2ds2-vascular", "axis_cha_vasc", 6, "IAM prévio, Doença Arterial Obstrutiva Periférica (DAOP) ou placa ateromatosa complexa na aorta.", [
                _opt("opt_cha_v_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem doença arterial coronariana, periférica ou aórtica documentada."),
                _opt("opt_cha_v_1", "Presente — IAM prévio, DAOP ou placa aórtica complexa (1 pt)", 1, False, 1.0, 2, "Carga aterotrombótica sistêmica associada."),
            ]),
            _grp("grp_cha_sc", "7. Sc — Sex Category (Categoria de Sexo)", "cha2ds2-sexo", "axis_cha_age", 7, "Modificador de risco (pontua apenas na presença de >= 1 outro fator de risco não ligado ao sexo).", [
                _opt("opt_cha_sc_0", "Sexo Masculino (0 pts)", 0, True, 0.0, 1, "Sexo biológico masculino."),
                _opt("opt_cha_sc_1", "Sexo Feminino (1 pt)", 1, False, 0.5, 2, "Modificador de risco em mulheres quando associado a outros fatores (idade >= 65 ou comorbidades)."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_cha_low",
                "label": "Baixo Risco Tromboembólico (0 pts em Homens ou 1 pt isolado por Sexo Feminino)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Taxa anual de AVC isquêmico de 0,0% a 0,2%. Nenhuma terapia antitrombótica é recomendada (antiagregantes isolados não são indicados para prevenção de AVC na FA).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_cha_low_1", "Controle de Frequência ou Ritmo (Sem Anticoagulação Crônica)", "Metoprolol 25-100mg VO 12/12h ou Diltiazem 60mg 8/8h (alvo FC repouso < 110 bpm — estudo RACE II)", "Via Oral", "Diário", "Não prescrever AAS isolado com finalidade de profilaxia de AVC em FA.", "Sem ajuste renal para Metoprolol.", "Evitar bloqueadores de canal de cálcio não-diidropiridínicos (Verapamil/Diltiazem) se FEVE <= 40%.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_cha_low_1", "Seguimento Ambulatorial e Reavaliação Periódica", "Ambulatório de Cardiologia", "Reavaliar o escore CHA2DS2-VASc em 4 a 6 meses e anualmente, pois o surgimento de HAS, DM ou avanço etário muda a indicação.", lab="TSH, T4 livre, eletrólitos, função renal e Ecocardiograma transtorácico.")
                ]
            },
            {
                "id": "tier_cha_mod",
                "label": "Risco Intermediário (1 ponto em Homens; ou 1 pt em Mulheres sem outros fatores / 2 pts em Mulheres)",
                "severityLevel": "intermediate",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Taxa anual de AVC de ~1,3% (se 1 fator de risco não-sexo). Se o único ponto for Sexo Feminino (CHA2DS2-VASc = 1 em mulher jovem sem comorbidades), o risco real é < 0,5%/ano (sem indicação de ACO). Se 1 ponto em homem, considerar anticoagulação oral (Classe IIa ESC/SBC).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_cha_mod_doac", "Anticoagulante Oral Direto — DOAC (se 1 fator de risco real não-sexo)", "Apixabana 5mg VO 12/12h ou Rivaroxabana 20mg VO 1x/dia (junto à refeição) ou Dabigatrana 150mg 12/12h", "Via Oral", "12/12h ou 24/24h", "Rivaroxabana 20mg/15mg deve ser ingerida obrigatoriamente com alimentos para garantir biodisponibilidade > 80%.", "Apixabana: reduzir para 2,5mg 12/12h se >= 2 critérios (Idade >= 80a, Peso <= 60kg, Cr >= 1,5 mg/dL). Rivaroxabana: 15mg/dia se ClCr 15-49 mL/min.", "Prótese valvar mecânica ou estenose mitral moderada/grave.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_cha_mod_1", "Decisão Compartilhada e Avaliação do HAS-BLED", "Ambulatório", "Pesar benefício líquido da anticoagulação frente ao risco hemorrágico (HAS-BLED) e preferência do paciente.", lab="Creatinina (ClCr por Cockcroft-Gault para ajuste de DOAC), hemograma, função hepática.")
                ]
            },
            {
                "id": "tier_cha_high",
                "label": "Alto Risco Tromboembólico (>= 2 pontos em Homens ou >= 3 em Mulheres)",
                "severityLevel": "critical",
                "minScore": 2,
                "maxScore": 9,
                "statisticalOutcome": "Taxa anual de AVC sem anticoagulação de 2,2% (2 pts), 3,2% (3 pts), 4,0% (4 pts), 6,7% (5 pts), 9,8% (6 pts) até 15,2% (9 pts). Indicação Classe I Nível A para Anticoagulação Oral plena, preferencialmente com DOACs.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_cha_high_apix", "Apixabana (ou Rivaroxabana / Edoxabana / Dabigatrana) — 1ª Escolha (Classe I)", "Apixabana 5 mg VO de 12/12h (ou 2,5 mg 12/12h se >= 2 critérios ABC: Age >= 80, Body weight <= 60kg, Creatinine >= 1,5)", "Via Oral", "12/12 horas", "Não partir ou macerar cápsulas de Dabigatrana (aumenta absorção em 75%); Apixabana e Rivaroxabana podem ser trituradas para SNE se necessário.", "Rivaroxabana: 15 mg 1x/dia se ClCr 15-49 mL/min. Edoxabana: 30 mg 1x/dia se ClCr 15-50 mL/min ou peso <= 60 kg. Dabigatrana contraindicada se ClCr < 30 mL/min.", "Estenose mitral moderada/grave ou prótese mecânica (usar Varfarina com meta de RNI 2,0-3,0 ou 2,5-3,5)."),
                    _rx("rx_cha_high_warf", "Varfarina Sódica (se FA Valvar, SAAF triplo positivo ou indisponibilidade de DOAC)", "5 mg VO 1x/dia inicialmente, titulada para manter RNI entre 2,0 e 3,0 (TTR > 70%)", "Via Oral", "1x/dia", "Monitorar RNI semanalmente no início e mensalmente após estabilidade.", "Preferida em DRC dialítica (ClCr < 15 mL/min) onde a evidência de DOACs é limitada.", "Gestação no 1º trimestre (teratogênica), sangramento ativo maior.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_cha_high_1", "Anticoagulação Plena Contínua e Controle de Fatores Modificáveis", "Ambulatório / Enfermaria", "Monitorar adesão medicamentosa, função renal semestral (ou a cada ClCr/10 meses se DRC) e corrigir fatores de risco hemorrágico (HAS-BLED).", proc="Considerar Oclusão Percutânea do Apêndice Atrial Esquerdo (OAAE / Watchman) apenas em pacientes com contraindicação absoluta e irreversível à anticoagulação oral (ex: angiopatia amiloide cerebral com HIC lobar recorrente).", lab="Hemograma, plaquetas, creatinina, TGO/TGP, RNI (se uso de AVK).")
                ]
            }
        ]
    }


def get_has_bled() -> dict:
    return {
        "id": "calc_has_bled",
        "slug": "has-bled",
        "name": "HAS-BLED Score para Risco de Sangramento Maior em Anticoagulação",
        "acronym": "HAS-BLED",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Arritmias Cardíacas e Anticoagulação",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Arritmias e Tromboembolismo",
        "description": "Ferramenta clínica validada no Euro Heart Survey (0 a 9 pontos) para estimar o risco em 1 ano de sangramento maior (intracraniano, hospitalização, queda de Hb > 2 g/dL ou transfusão >= 2 CH) em pacientes com Fibrilação Atrial sob anticoagulação oral.",
        "summary": "Estimativa do risco anual de sangramento maior em pacientes com FA anticoagulados (0 a 9 pontos).",
        "clinicalObjective": "Identificar e corrigir sistematicamente fatores de risco hemorrágico modificáveis (PA não controlada, RNI lábil, uso concomitante de AINEs/antiagregantes e etilismo) sem suspender indevidamente a anticoagulação.",
        "targetPopulation": "Pacientes adultos com Fibrilação Atrial candidatos a ou em uso de anticoagulação oral (Varfarina ou DOACs).",
        "calculationType": "additive_points",
        "formulaExpression": "Hipertensao + Renal_Hepatico(0_1_2) + AVC + Sangramento + RNI_Labil + Idade65 + Drogas_Alcool(0_1_2)",
        "evidenceSource": "Pisters R, Lane DA, Nieuwlaat R, de Vos CB, Crijns HJ, Lip GY. A novel user-friendly score (HAS-BLED) to assess 1-year risk of major bleeding in patients with atrial fibrillation: the Euro Heart Survey. Chest. 2010;138(5):1093-1100.",
        "minPossibleScore": 0,
        "maxPossibleScore": 9,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "REGRA DE OURO DAS DIRETRIZES ESC/SBC: Um escore HAS-BLED elevado (>= 3 pontos) NÃO é contraindicação isolada ao início ou manutenção da anticoagulação oral! Seu propósito clínico é sinalizar a necessidade de corrigir os fatores modificáveis (controlar PAS < 130-140 mmHg, suspender AAS/AINEs desnecessários, cessar álcool, trocar Varfarina com TTR < 60% por DOAC como Apixabana) e agendar retornos mais frequentes.",
        "radarAxes": [
            _axis("axis_hb_vasc", "Fragilidade Vascular (HAS, AVC e Idade)", "Vascular", "pts"),
            _axis("axis_hb_organ", "Disfunção Renal e Hepática", "Renal", "pts"),
            _axis("axis_hb_hemo", "Diátese Hemorrágica e Labilidade de RNI", "Hematológico", "pts"),
            _axis("axis_hb_drugs", "Exposição a Fármacos (AINEs/AAS) e Álcool", "Metabólico", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_hb_h", "1. H — Hypertension (Hipertensão Arterial Não Controlada)", "hasbled-hipertensao", "axis_hb_vasc", 1, "Definida estritamente como Pressão Arterial Sistólica (PAS) persistentemente > 160 mmHg.", [
                _opt("opt_hb_h_0", "PAS <= 160 mmHg (Normotenso ou HAS controlada) (0 pts)", 0, True, 0.0, 1, "Pressão arterial controlada."),
                _opt("opt_hb_h_1", "PAS > 160 mmHg (Hipertensão não controlada) (1 pt)", 1, False, 1.0, 2, "Hipertensão sistólica severa (> 160 mmHg): eleva drasticamente o risco de hemorragia intracraniana."),
            ]),
            _grp("grp_hb_a", "2. A — Abnormal Renal and/or Liver Function (Função Renal e/ou Hepática Anormal)", "hasbled-renal-hepatico", "axis_hb_organ", 2, "Renal: diálise crônica, transplante renal ou Cr >= 2,26 mg/dL (200 µmol/L). Hepática: cirrose ou bilirrubina > 2x LSN com TGO/TGP/FA > 3x LSN.", [
                _opt("opt_hb_a_0", "Função renal e hepática preservadas (0 pts)", 0, True, 0.0, 1, "Sem disfunção renal ou hepática significativa."),
                _opt("opt_hb_a_1", "Disfunção Renal OU Hepática isolada (1 pt)", 1, False, 0.5, 2, "Apenas uma das duas disfunções orgânicas presentes."),
                _opt("opt_hb_a_2", "Ambas: Disfunção Renal E Hepática concomitantes (2 pts)", 2, False, 1.0, 3, "Comprometimento simultâneo da depuração renal e da síntese hepática de fatores de coagulação."),
            ]),
            _grp("grp_hb_s", "3. S — Stroke (Acidente Vascular Cerebral Prévio)", "hasbled-avc", "axis_hb_vasc", 3, "Histórico prévio de AVC isquêmico ou hemorrágico (especialmente lacunar ou micro-hemorragias).", [
                _opt("opt_hb_s_0", "Sem histórico de AVC (0 pts)", 0, True, 0.0, 1, "Ausência de eventos cerebrovasculares prévios."),
                _opt("opt_hb_s_1", "História prévia de AVC (1 pt)", 1, False, 1.0, 2, "Leito vascular cerebral vulnerável à transformação hemorrágica."),
            ]),
            _grp("grp_hb_b", "4. B — Bleeding (História ou Predisposição a Sangramento)", "hasbled-sangramento", "axis_hb_hemo", 4, "Episódio prévio de sangramento maior, anemia crônica ou plaquetopenia / diátese hemorrágica.", [
                _opt("opt_hb_b_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem histórico de sangramento ou anemia."),
                _opt("opt_hb_b_1", "Sangramento maior prévio, anemia ou diátese hemorrágica (1 pt)", 1, False, 1.0, 2, "Lesão mucosa prévia (ex: úlcera péptica, angiodisplasia colônica) ou distúrbio hemostático."),
            ]),
            _grp("grp_hb_l", "5. L — Labile INRs (RNI Lábil em Uso de Antagonista da Vitamina K)", "hasbled-rni-labil", "axis_hb_hemo", 5, "RNI instável/alto ou Tempo na Faixa Terapêutica (TTR) < 60% (pontuar 0 se paciente em uso de DOAC ou virgem de Varfarina).", [
                _opt("opt_hb_l_0", "Ausente, TTR >= 60% ou em uso de DOAC (0 pts)", 0, True, 0.0, 1, "Anticoagulação estável ou uso de DOAC."),
                _opt("opt_hb_l_1", "RNI lábil / TTR < 60% em uso de Varfarina (1 pt)", 1, False, 1.0, 2, "Oscilações frequentes de RNI (> 3,5) aumentando eventos hemorrágicos."),
            ]),
            _grp("grp_hb_e", "6. E — Elderly (Idade > 65 anos)", "hasbled-idade", "axis_hb_vasc", 6, "Idade > 65 anos ou fragilidade biológica acentuada.", [
                _opt("opt_hb_e_0", "Idade <= 65 anos (0 pts)", 0, True, 0.0, 1, "Paciente com 65 anos ou menos."),
                _opt("opt_hb_e_1", "Idade > 65 anos (1 pt)", 1, False, 1.0, 2, "Maior fragilidade capilar e risco de quedas."),
            ]),
            _grp("grp_hb_d", "7. D — Drugs or Alcohol (Fármacos Antiplaquetários/AINEs e/ou Álcool)", "hasbled-drogas-alcool", "axis_hb_drugs", 7, "Fármacos (1 pt): uso concomitante de AAS, Clopidogrel ou AINEs. Álcool (1 pt): consumo abusivo >= 8 doses/semana.", [
                _opt("opt_hb_d_0", "Nenhum — Sem uso de antiagregantes/AINEs e sem abuso de álcool (0 pts)", 0, True, 0.0, 1, "Sem exposição a cofatores tóxicos/farmacológicos."),
                _opt("opt_hb_d_1", "Uso de Antiplaquetários/AINEs OU Abuso de Álcool isolado (1 pt)", 1, False, 0.5, 2, "Presença de um dos dois cofatores modificáveis."),
                _opt("opt_hb_d_2", "Ambos: Uso de Antiplaquetários/AINEs E Abuso de Álcool (2 pts)", 2, False, 1.0, 3, "Sinergismo crítico de lesão de mucosa gástrica e disfunção plaquetária/hepática."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_hb_low",
                "label": "Baixo Risco Hemorrágico (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Incidência anual de sangramento maior de 1,02% (1,13 sangramentos/100 pacientes-ano com 0 pts e 1,02/100 pacientes-ano com 1 pt). Segura iniciação de anticoagulação oral conforme CHA2DS2-VASc.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_hb_low_1", "Anticoagulação Oral Padrão (DOAC de escolha)", "Apixabana 5mg 12/12h, Rivaroxabana 20mg/dia, Dabigatrana 150mg 12/12h ou Edoxabana 60mg/dia", "Via Oral", "Diário", "Manter dose plena padrão exceto se critérios formais de redução de bula.", "Revisar ClCr anualmente.", "Evitar subdosagem off-label de DOACs (aumenta risco de AVC sem reduzir sangramento).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hb_low_1", "Seguimento Ambulatorial Padrão", "Ambulatório", "Orientar sinais de alerta de sangramento (melena, hematúria, epistaxe persistente) e proibição de automedicação com AINEs.", lab="Hemograma e função renal anuais.")
                ]
            },
            {
                "id": "tier_hb_mod",
                "label": "Risco Hemorrágico Moderado (2 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Incidência anual de sangramento maior de 1,88 por 100 pacientes-ano. Anticoagulação permanece indicada, com foco na eliminação de fatores modificáveis.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_hb_mod_1", "Preferir DOACs com Menor Taxa de Sangramento GI e Intracraniano + IBP se risco digestivo", "Apixabana 5mg 12/12h (ou Edoxabana 60mg/dia) + Pantoprazol 40mg VO em jejum se antecedente dispéptico/uso de antiplaquetário", "Via Oral", "Diário", "No estudo ARISTOTLE, a Apixabana reduziu sangramento maior em 31% comparada à Varfarina.", "Ajustar dose conforme critérios ABC (Apixabana) ou ClCr.", "Suspender AAS concomitante se DAC crônica estável > 12 meses pós-ICP (estudo AFIRE).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hb_mod_1", "Revisão Semestral e Controle Pressórico Estrito", "Ambulatório", "Manter PAS estritamente < 130-140 mmHg; suspender anti-inflamatórios não esteroidais.", lab="Hemograma, ferritina, função renal e hepática a cada 6 meses.")
                ]
            },
            {
                "id": "tier_hb_high",
                "label": "Alto Risco Hemorrágico (3 a 9 pontos)",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 9,
                "statisticalOutcome": "Incidência de sangramento maior de 3,74% (3 pts), 8,70% (4 pts) a > 12,5% (>= 5 pts). Atenção: NÃO suspender anticoagulação pelo escore isolado; intervir agressivamente nos fatores modificáveis e realizar vigilância estreita.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_hb_high_1", "Otimização da Anticoagulação (Switch para Apixabana/Edoxabana) + Proteção Gástrica", "Substituir Varfarina (se TTR < 60% e FA não valvar) por Apixabana + Omeprazol/Pantoprazol 40mg/dia", "Via Oral", "Diário", "Suspender imediatamente antiagregantes plaquetários sem indicação aguda recente (< 6-12m de stent).", "Ajuste estrito pelo ClCr (Cockcroft-Gault).", "Em caso de sangramento ativo ameaçador à vida: acionar Complexo Protrombínico de 4 fatores (25-50 UI/kg IV), Idarucizumabe 5g IV (para Dabigatrana) ou Andexanet alfa.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hb_high_1", "Mitigação Multidisciplinar de Risco Hemorrágico", "Ambulatório de Alto Risco / Anticoagulação", "Retornos a cada 1 a 3 meses; controle rigoroso da PA; cessação do etilismo; prevenção de quedas em idosos; investigação endoscópica se anemia ferropriva.", proc="Avaliar Oclusão Percutânea do Apêndice Atrial Esquerdo apenas se houver sangramento intracraniano irreversível (ex: angiopatia amiloide) ou sangramento GI intratável.", lab="Hemograma completo, reticulócitos, função renal, TGO/TGP, bilirrubinas e pesquisa de sangue oculto nas fezes.")
                ]
            }
        ]
    }


def get_atria() -> dict:
    return {
        "id": "calc_atria",
        "slug": "atria-bleeding",
        "name": "ATRIA Bleeding Risk Score na Fibrilação Atrial",
        "acronym": "ATRIA",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Arritmias Cardíacas e Anticoagulação",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Arritmias e Tromboembolismo",
        "description": "Escore quantitativo ponderado (0 a 10 pontos) derivado da coorte Anticoagulation and Risk Factors in Atrial Fibrillation (ATRIA) para predição de hemorragia maior em pacientes anticoagulados por Fibrilação Atrial, atribuindo forte peso à anemia e à doença renal grave.",
        "summary": "Predição de hemorragia maior em FA anticoagulada com ponderação para anemia e DRC grave (0 a 10 pontos).",
        "clinicalObjective": "Quantificar o risco anual de hemorragia maior em pacientes com FA em programação de anticoagulação, destacando o impacto prognóstico da anemia basal e da insuficiência renal avançada.",
        "targetPopulation": "Pacientes adultos com Fibrilação Atrial em uso ou candidatos a anticoagulação oral.",
        "calculationType": "additive_points",
        "formulaExpression": "Anemia_3 + DRC_Grave_3 + Idade75_2 + HemorragiaPrevia_1 + Hipertensao_1",
        "evidenceSource": "Fang MC, Go AS, Chang Y, et al. A new risk scheme to predict warfarin-associated hemorrhage: The ATRIA (Anticoagulation and Risk Factors in Atrial Fibrillation) Study. J Am Coll Cardiol. 2011;58(4):395-401.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "A presença isolada de Anemia (3 pts) + Doença Renal Crônica Estágio 4/5 (3 pts) já classifica o paciente em Alto Risco Hemorrágico (6 pts, risco anual ~5,8%), exigindo investigação da causa da anemia e seleção criteriosa do anticoagulante e sua posologia renal.",
        "radarAxes": [
            _axis("axis_atria_heme", "Reserva Hematológica e Sangramento Prévio", "Hematológico", "pts"),
            _axis("axis_atria_renal", "Função Renal (TFG / Diálise)", "Renal", "pts"),
            _axis("axis_atria_age_bp", "Senescência (>= 75a) e Hipertensão", "Vascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_atria_1", "1. Anemia (Hemoglobina < 13 g/dL em Homens ou < 12 g/dL em Mulheres)", "atria-anemia", "axis_atria_heme", 1, "Dosagem de hemoglobina basal antes ou durante a anticoagulação.", [
                _opt("opt_atria_1_0", "Ausente — Hemoglobina normal (0 pts)", 0, True, 0.0, 1, "Níveis normais de hemoglobina sérica."),
                _opt("opt_atria_1_3", "Presente — Anemia documentada (3 pts)", 3, False, 1.0, 2, "Principal preditor laboratorial de sangramento digestivo oculto ou reserva hemostática reduzida."),
            ]),
            _grp("grp_atria_2", "2. Doença Renal Grave (TFG < 30 mL/min/1,73m² ou Diálise)", "atria-drc", "axis_atria_renal", 2, "Insuficiência renal crônica estágios G4 ou G5.", [
                _opt("opt_atria_2_0", "Ausente — TFG >= 30 mL/min/1,73m² (0 pts)", 0, True, 0.0, 1, "Função renal preservada ou disfunção leve a moderada."),
                _opt("opt_atria_2_3", "Presente — TFG < 30 mL/min ou Hemodiálise (3 pts)", 3, False, 1.0, 2, "Disfunção plaquetária urêmica e acúmulo plasmático de anticoagulantes de excreção renal."),
            ]),
            _grp("grp_atria_3", "3. Idade >= 75 anos", "atria-idade", "axis_atria_age_bp", 3, "Idade cronológica do paciente.", [
                _opt("opt_atria_3_0", "Idade < 75 anos (0 pts)", 0, True, 0.0, 1, "Menos de 75 anos."),
                _opt("opt_atria_3_2", "Idade >= 75 anos (2 pts)", 2, False, 1.0, 2, "Fragilidade vascular senil e maior risco de hematoma subdural e sangramento GI."),
            ]),
            _grp("grp_atria_4", "4. Qualquer Hemorragia Prévia Diagnosticada", "atria-hemorragia", "axis_atria_heme", 4, "Histórico prévio de hemorragia digestiva, intracraniana, urinária ou cirúrgica importante.", [
                _opt("opt_atria_4_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem episódios hemorrágicos prévios."),
                _opt("opt_atria_4_1", "Presente — Antecedente de hemorragia (1 pt)", 1, False, 1.0, 2, "Vulnerabilidade anatômica ou mucosa preexistente."),
            ]),
            _grp("grp_atria_5", "5. Hipertensão Arterial Sistêmica Diagnosticada", "atria-has", "axis_atria_age_bp", 5, "História clínica de hipertensão arterial ou uso de anti-hipertensivos.", [
                _opt("opt_atria_5_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem diagnóstico de hipertensão."),
                _opt("opt_atria_5_1", "Presente — Diagnóstico de Hipertensão Arterial (1 pt)", 1, False, 0.5, 2, "Sobrecarga pressórica arterial sistêmica."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_atria_low",
                "label": "Baixo Risco Hemorrágico (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Taxa anual de hemorragia maior de ~0,76% (< 1% ao ano). Perfil altamente favorável para anticoagulação oral.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_atria_low_1", "DOAC em Dose Padrão", "Apixabana 5mg 12/12h, Rivaroxabana 20mg/dia, Dabigatrana 150mg 12/12h ou Edoxabana 60mg/dia", "Via Oral", "Diário", "Administrar conforme posologia padrão.", "Monitorar ClCr anualmente.", "FA valvar mecânica ou mitral moderada/grave.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_atria_low_1", "Acompanhamento Ambulatorial Habitual", "Ambulatório", "Manter controle pressórico e revisar exames laboratoriais anualmente.", lab="Hemograma e creatinina sérica.")
                ]
            },
            {
                "id": "tier_atria_mod",
                "label": "Risco Hemorrágico Intermediário (4 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Taxa anual de hemorragia maior de ~2,62% ao ano. Requer atenção especial à função renal e investigação de eventual queda de hemoglobina.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_atria_mod_1", "DOAC Ajustado à Função Renal + Inibidor de Bomba de Prótons", "Apixabana 5mg (ou 2,5mg 12/12h se critérios ABC) + Pantoprazol 40mg VO/dia", "Via Oral", "Diário", "Evitar Dabigatrana se ClCr próximo a 30 mL/min devido à excreção renal de 80%.", "Ajustar Rivaroxabana (15mg) ou Edoxabana (30mg) se ClCr 15-50 mL/min.", "Uso concomitante de AINEs.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_atria_mod_1", "Monitoramento Semestral de Hemoglobina e ClCr", "Ambulatório", "Investigar ferropenia caso hemoglobina limítrofe; controlar PA < 130/80 mmHg.", lab="Hemograma completo, cinética de ferro, creatinina e TFG a cada 6 meses.")
                ]
            },
            {
                "id": "tier_atria_high",
                "label": "Alto Risco Hemorrágico (5 a 10 pontos)",
                "severityLevel": "high",
                "minScore": 5,
                "maxScore": 10,
                "statisticalOutcome": "Taxa anual de hemorragia maior de ~5,76% ao ano. Exige investigação etiológica da anemia (EDA/Colonoscopia), ajuste rigoroso para DRC avançada e revisão de medicamentos concomitantes.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_atria_high_1", "Apixabana Ajustada ou Varfarina sob Controle Estrito (se TFG < 15 mL/min)", "Apixabana 2,5mg a 5mg 12/12h (menor excreção renal entre os DOACs: 27%) ou Varfarina titulada para RNI 2,0-2,5", "Via Oral", "12/12h ou 1x/dia", "Em ClCr < 15 mL/min ou diálise, discutir individualmente com nefrologia/cardiologia.", "Contraindicados Dabigatrana (ClCr < 30) e Rivaroxabana/Edoxabana (ClCr < 15).", "Sangramento digestivo ativo não tratado.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_atria_high_1", "Investigação Endoscópica de Anemia e Seguimento Conjunto Cardio-Nefro", "Ambulatório Especializado / Hospital-Dia", "Realizar EDA e colonoscopia se anemia ferropriva antes ou logo no início da anticoagulação; suspender qualquer antiagregante concomitante não essencial.", proc="Endoscopia Digestiva Alta / Colonoscopia diagnóstica e terapêutica; considerar OAAE se sangramento recorrente intratável.", lab="Hemograma seriado, reticulócitos, ferritina, ureia, creatinina, potássio e RNI.")
                ]
            }
        ]
    }


def get_hemorr2hages() -> dict:
    return {
        "id": "calc_hemorr2hages",
        "slug": "hemorr2hages",
        "name": "HEMORR2HAGES Score para Risco de Sangramento em Anticoagulação",
        "acronym": "HEMORR2HAGES",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Arritmias Cardíacas e Anticoagulação",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Arritmias e Tromboembolismo",
        "description": "Escore multidimensional (0 a 12 pontos) derivado do National Registry of Atrial Fibrillation para quantificar o risco de hemorragia maior em pacientes idosos ou frágeis submetidos à anticoagulação, incorporando risco de quedas, malignidade, anemia, plaquetopenia e polimorfismos farmacogenéticos.",
        "summary": "Avaliação abrangente do risco hemorrágico em anticoagulação incluindo quedas, neoplasia e anemia (0 a 12 pontos).",
        "clinicalObjective": "Estimar a taxa de sangramento por 100 pacientes-ano em pacientes com FA com múltiplas comorbidades geriátricas, oncológicas ou hematológicas.",
        "targetPopulation": "Pacientes adultos e idosos com Fibrilação Atrial candidatos à terapia anticoagulante.",
        "calculationType": "additive_points",
        "formulaExpression": "HepaticoRenal + EtanolCancer + Idade75Quedas + Rebleeding_2 + AnemiaPlaquetas + HAS_AVC_CYP2C9",
        "evidenceSource": "Gage BF, Yan Y, Milligan PE, et al. Clinical classification schemes for predicting hemorrhage: results from the National Registry of Atrial Fibrillation (NRAF). Am Heart J. 2006;151(3):713-719.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "O escore HEMORR2HAGES é especialmente útil em pacientes geriátricos e oncológicos por contemplar o risco de quedas frequentes/demência e neoplasia ativa. O antecedente de sangramento prévio (Re-bleeding) recebe peso duplo (2 pontos).",
        "radarAxes": [
            _axis("axis_hem_rebleed", "Histórico de Ressangramento e Plaquetas/Anemia", "Hematológico", "pts"),
            _axis("axis_hem_organ", "Disfunção Hepática, Renal e Neoplasia", "Renal", "pts"),
            _axis("axis_hem_geriatric", "Idade > 75a, Risco de Quedas e Neurovascular", "Neurológico", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_hem_1", "1. H — Hepatic or Renal Disease (Doença Hepática e/ou Renal)", "hemorr2hages-hepatico-renal", "axis_hem_organ", 1, "Cirrose/hepatopatia crônica (1 pt) e/ou Insuficiência Renal moderada a grave Cr > 2,0 mg/dL (1 pt).", [
                _opt("opt_hem_1_0", "Ausente — Função hepática e renal normais (0 pts)", 0, True, 0.0, 1, "Sem disfunção hepática ou renal."),
                _opt("opt_hem_1_1", "Doença Hepática OU Doença Renal isolada (1 pt)", 1, False, 0.5, 2, "Presença de uma das duas disfunções orgânicas."),
                _opt("opt_hem_1_2", "Ambas: Doença Hepática E Doença Renal concomitantes (2 pts)", 2, False, 1.0, 3, "Comprometimento combinado hepatorrenal."),
            ]),
            _grp("grp_hem_2", "2. E / M — Ethanol Abuse & Malignancy (Abuso de Álcool e/ou Neoplasia Ativa)", "hemorr2hages-etanol-cancer", "axis_hem_organ", 2, "Etilismo pesado atual (1 pt) e/ou Malignidade/Câncer ativo ou metastático (1 pt).", [
                _opt("opt_hem_2_0", "Ausente — Sem etilismo e sem neoplasia ativa (0 pts)", 0, True, 0.0, 1, "Ausência de abuso de álcool e de câncer em atividade."),
                _opt("opt_hem_2_1", "Abuso de Álcool OU Neoplasia Ativa isolada (1 pt)", 1, False, 0.5, 2, "Presença de um fator (etilismo ou malignidade)."),
                _opt("opt_hem_2_2", "Ambos: Abuso de Álcool E Neoplasia Ativa (2 pts)", 2, False, 1.0, 3, "Associação de neoplasia ativa e etilismo."),
            ]),
            _grp("grp_hem_3", "3. O / E — Older Age (> 75 anos) & Excessive Fall Risk (Risco de Quedas/Demência)", "hemorr2hages-idade-quedas", "axis_hem_geriatric", 3, "Idade > 75 anos (1 pt) e/ou Alto risco de quedas (demência, Parkinson, síncope recorrente, fragilidade) (1 pt).", [
                _opt("opt_hem_3_0", "Idade <= 75 anos e sem risco elevado de quedas (0 pts)", 0, True, 0.0, 1, "Sem vulnerabilidade geriátrica ou postural."),
                _opt("opt_hem_3_1", "Idade > 75 anos OU Alto Risco de Quedas/Demência (1 pt)", 1, False, 0.5, 2, "Presença de um critério geriátrico."),
                _opt("opt_hem_3_2", "Ambos: Idade > 75 anos E Alto Risco de Quedas/Demência (2 pts)", 2, False, 1.0, 3, "Idoso longevo com instabilidade postural ou síndrome demencial (alto risco de hematoma subdural)."),
            ]),
            _grp("grp_hem_4", "4. R2 — Re-bleeding Risk (História de Sangramento Maior Prévio — Peso 2)", "hemorr2hages-rebleeding", "axis_hem_rebleed", 4, "Qualquer hospitalização prévia por sangramento maior (digestivo, intracraniano, retroperitoneal).", [
                _opt("opt_hem_4_0", "Ausente — Sem sangramento prévio (0 pts)", 0, True, 0.0, 1, "Sem histórico de eventos hemorrágicos."),
                _opt("opt_hem_4_2", "Presente — Antecedente de Sangramento Maior (2 pts)", 2, False, 1.0, 2, "Principal fator isolado para ressangramento sob anticoagulação."),
            ]),
            _grp("grp_hem_5", "5. R / A — Reduced Platelet Count/Function & Anemia (Plaquetas e Anemia)", "hemorr2hages-plaquetas-anemia", "axis_hem_rebleed", 5, "Plaquetopenia < 100.000/mm³ ou uso de AAS/AINE (1 pt) e/ou Anemia Hb < 13 H / < 12 M (1 pt).", [
                _opt("opt_hem_5_0", "Plaquetas normais (sem antiagregante) e Hemoglobina normal (0 pts)", 0, True, 0.0, 1, "Série vermelha e hemostasia primária normais."),
                _opt("opt_hem_5_1", "Plaquetopenia/Uso de AAS OU Anemia isolada (1 pt)", 1, False, 0.5, 2, "Alteração isolada da série vermelha ou plaquetária."),
                _opt("opt_hem_5_2", "Ambos: Plaquetopenia/Uso de AAS E Anemia presentes (2 pts)", 2, False, 1.0, 3, "Duplo comprometimento hematológico."),
            ]),
            _grp("grp_hem_6", "6. H / G / S — Hypertension, Genetic CYP2C9 & Stroke (HAS, Genética e AVC)", "hemorr2hages-has-avc-gen", "axis_hem_geriatric", 6, "Hipertensão não controlada (1 pt), AVC prévio (1 pt) ou polimorfismo genético CYP2C9 metabolizador lento de varfarina (1 pt).", [
                _opt("opt_hem_6_0", "Nenhum destes fatores presentes (0 pts)", 0, True, 0.0, 1, "PA controlada, sem AVC prévio."),
                _opt("opt_hem_6_1", "1 fator presente (HAS não controlada OU AVC prévio) (1 pt)", 1, False, 0.5, 2, "Presença de um fator neurovascular."),
                _opt("opt_hem_6_2", ">= 2 fatores presentes (ex: HAS não controlada + AVC prévio/CYP2C9) (2 pts)", 2, False, 1.0, 3, "Múltiplos fatores de vulnerabilidade cerebrovascular ou farmacogenética."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_hem_low",
                "label": "Baixo Risco Hemorrágico (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Incidência de sangramento maior de 1,9 (0 pts) a 2,5 (1 pt) por 100 pacientes-ano. Anticoagulação oral recomendada com segurança.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_hem_low_1", "DOAC em Dose Plena Padrão", "Apixabana 5mg 12/12h, Rivaroxabana 20mg/dia ou Edoxabana 60mg/dia", "Via Oral", "Diário", "Administrar conforme rotina.", "Revisão anual de ClCr.", "FA valvar mecânica.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hem_low_1", "Acompanhamento Clínico Anual", "Ambulatório", "Manter adesão e orientações gerais de anticoagulação.", lab="Hemograma e função renal anuais.")
                ]
            },
            {
                "id": "tier_hem_mod",
                "label": "Risco Hemorrágico Intermediário (2 a 3 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Incidência de sangramento maior de 5,3 (2 pts) a 8,4 (3 pts) por 100 pacientes-ano. Preferir DOACs com melhor perfil de segurança em idosos (Apixabana/Edoxabana).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_hem_mod_1", "Apixabana ou Edoxabana + Protetor Gástrico (IBP)", "Apixabana 5mg (ou 2,5mg 12/12h se critérios ABC) + Pantoprazol 40mg/dia", "Via Oral", "Diário", "Evitar Varfarina se suspeita de metabolizador lento CYP2C9 ou labilidade.", "Ajustar pela TFG/ClCr.", "Suspender antiagregantes plaquetários concomitantes.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hem_mod_1", "Prevenção de Quedas e Vigilância Hematológica", "Ambulatório", "Fisioterapia de equilíbrio, adaptação domiciliar contra quedas e controle pressórico.", lab="Hemograma, plaquetas, função renal e hepática semestrais.")
                ]
            },
            {
                "id": "tier_hem_high",
                "label": "Alto Risco Hemorrágico (4 a 12 pontos)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 12,
                "statisticalOutcome": "Incidência de sangramento maior de 10,4 (4 pts) a 12,3 (>= 5 pts) por 100 pacientes-ano. Exige avaliação individualizada rigorosa entre Cardiologia, Geriatria/Oncologia e Hematologia.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_hem_high_1", "Anticoagulação Criteriosa com DOAC de Menor Risco GI/HIC ou Suspensão se Plaquetas < 50.000/mm³", "Apixabana ajustada (se plaquetas > 50.000/mm³ e sem sangramento ativo) + IBP em dose plena", "Via Oral", "12/12h", "Em pacientes oncológicos com tumores luminais GI ou geniturinários intactos, Apixabana ou HBPM tem menor risco de sangramento mucoso que Rivaroxabana/Edoxabana.", "Ajuste estrito por peso, idade e creatinina.", "Plaquetopenia grave < 25.000-50.000/mm³ ou sangramento ativo.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_hem_high_1", "Reabilitação Geriátrica, Revisão Oncológica e Consideração de Oclusão de Apêndice Atrial", "Ambulatório Multidisciplinar", "Monitoramento mensal/bimestral de hemograma; se contraindicação permanente à anticoagulação, avaliar oclusão percutânea do apêndice atrial esquerdo (OAAE).", proc="Avaliação para OAAE (Watchman / Amplatzer Amulet) se ressangramento grave recorrente.", lab="Hemograma completo, plaquetas, coagulograma, função renal e hepática.")
                ]
            }
        ]
    }


def get_framingham_ic() -> dict:
    return {
        "id": "calc_framingham_ic",
        "slug": "framingham-ic",
        "name": "Critérios de Framingham para Diagnóstico de Insuficiência Cardíaca",
        "acronym": "Framingham-IC",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Insuficiência Cardíaca",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Insuficiência Cardíaca e Miocardiopatias",
        "description": "Sistema diagnóstico clínico clássico validado pelo Framingham Heart Study para confirmação sindrômica de Insuficiência Cardíaca à beira do leito: cada Critério Maior soma 2 pontos e cada Critério Menor soma 1 ponto. A soma >= 4 pontos (2 Maiores ou 1 Maior + 2 Menores) confirma o diagnóstico clínico de IC.",
        "summary": "Diagnóstico clínico de Insuficiência Cardíaca por Critérios Maiores (2 pts) e Menores (1 pt); >= 4 pts confirma IC.",
        "clinicalObjective": "Estabelecer o diagnóstico sindrômico de Insuficiência Cardíaca no pronto-socorro ou ambulatório antes mesmo da confirmação ecocardiográfica.",
        "targetPopulation": "Pacientes adultos com dispneia, fadiga, ortopneia ou síndrome edematosa suspeita de Insuficiência Cardíaca.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma(Criterios_Maiores * 2) + Soma(Criterios_Menores * 1)",
        "evidenceSource": "McKee PA, Castelli WP, McNamara PM, Kannel WB. The natural history of congestive heart failure: the Framingham study. N Engl J Med. 1971;285(26):1441-1446.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "REGRA DIAGNÓSTICA DE FRAMINGHAM: O diagnóstico clínico definitivo de Insuficiência Cardíaca requer >= 4 pontos obtidos por pelo menos 2 Critérios Maiores (4 pts) OU 1 Critério Maior (2 pts) + 2 Critérios Menores (2 pts). Critérios menores só são contabilizados se não puderem ser atribuídos a outra condição clínica (ex: DPOC, cirrose hepática ou síndrome nefrótica).",
        "radarAxes": [
            _axis("axis_fram_left", "Congestão Pulmonar / Esquerda (DPN, EAP, Estertores)", "Respiratório", "pts"),
            _axis("axis_fram_right", "Congestão Sistêmica / Direita (TJP, RHJ, Edema, Hepato)", "Cardiovascular", "pts"),
            _axis("axis_fram_struct", "Remodelamento e Disfunção (B3 e Cardiomegalia)", "Cardiovascular", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_fram_maj1", "1. Critério Maior: Dispneia Paroxística Noturna (DPN) ou Ortopneia", "framingham-dpn", "axis_fram_left", 1, "Episódios de despertar súbito por falta de ar aliviada ao sentar-se, ou intolerância ao decúbito dorsal.", [
                _opt("opt_fram_maj1_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Dorme em decúbito habitual sem despertar dispneico."),
                _opt("opt_fram_maj1_2", "Presente — DPN ou Ortopneia (Critério Maior: 2 pts)", 2, False, 1.0, 2, "Redistribuição noturna de fluido para o território venocapilar pulmonar."),
            ]),
            _grp("grp_fram_maj2", "2. Critério Maior: Turgência Jugular Patológica (TJP) ou Refluxo Hepatojugular", "framingham-tjp", "axis_fram_right", 2, "Distensão venosa cervical a 45° ou elevação sustentada (> 3 cm por > 15s) à compressão do hipocôndrio direito.", [
                _opt("opt_fram_maj2_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Pressão venosa central estimada normal."),
                _opt("opt_fram_maj2_2", "Presente — TJP a 45° ou Refluxo Hepatojugular positivo (Critério Maior: 2 pts)", 2, False, 1.0, 2, "Elevação da pressão de enchimento de câmaras direitas (> 16 cmH2O)."),
            ]),
            _grp("grp_fram_maj3", "3. Critério Maior: Estertores Crepitantes Pulmonares ou Edema Agudo de Pulmão", "framingham-estertores", "axis_fram_left", 3, "Crepitações teleinspiratórias bilaterais ou edema alveolar radiográfico/clínico.", [
                _opt("opt_fram_maj3_0", "Ausente — Ausculta pulmonar limpa (0 pts)", 0, True, 0.0, 1, "Murmúrio vesicular fisiológico sem ruídos adventícios."),
                _opt("opt_fram_maj3_2", "Presente — Estertores Pulmonares ou EAP (Critério Maior: 2 pts)", 2, False, 1.0, 2, "Transudação alveolar secundária à hipertensão venocapilar pulmonar."),
            ]),
            _grp("grp_fram_maj4", "4. Critério Maior: Galope por 3ª Bulha (B3) ou Cardiomegalia no RX", "framingham-b3-cardiomegalia", "axis_fram_struct", 4, "B3 audível em foco mitral/tricúspide ou Índice Cardiotorácico (ICT) > 0,50 na radiografia de tórax.", [
                _opt("opt_fram_maj4_0", "Ausente — Bulhas rítmicas em 2 tempos e ICT <= 0,50 (0 pts)", 0, True, 0.0, 1, "Sem B3 e área cardíaca normal."),
                _opt("opt_fram_maj4_2", "Presente — Galope por B3 ou Cardiomegalia no RX (Critério Maior: 2 pts)", 2, False, 1.0, 2, "Marcador altamente específico de sobrecarga de volume e disfunção ventricular."),
            ]),
            _grp("grp_fram_min1", "5. Critérios Menores Sistêmicos: Edema Maleolar Bilateral e/ou Hepatomegalia", "framingham-menores-sistemicos", "axis_fram_right", 5, "Cada critério menor vale 1 ponto: Edema de tornozelos bilateral (1 pt) e Hepatomegalia congestiva dolorosa (1 pt).", [
                _opt("opt_fram_min1_0", "Ausentes (0 pts)", 0, True, 0.0, 1, "Sem edema periférico ou hepatomegalia."),
                _opt("opt_fram_min1_1", "1 Critério Menor presente (Edema maleolar OU Hepatomegalia) (1 pt)", 1, False, 0.5, 2, "Sinal isolado de congestão venosa sistêmica."),
                _opt("opt_fram_min1_2", "2 Critérios Menores presentes (Edema maleolar E Hepatomegalia) (2 pts)", 2, False, 1.0, 3, "Congestão sistêmica combinada em membros inferiores e fígado."),
            ]),
            _grp("grp_fram_min2", "6. Critérios Menores Respiratórios: Dispneia aos Esforços, Tosse Noturna, Derrame Pleural ou FC >= 120 bpm", "framingham-menores-resp", "axis_fram_left", 6, "Cada critério menor vale 1 ponto (não atribuível a pneumopatia primária).", [
                _opt("opt_fram_min2_0", "Ausentes (0 pts)", 0, True, 0.0, 1, "Sem sintomas respiratórios menores ou taquicardia >= 120 bpm."),
                _opt("opt_fram_min2_1", "1 Critério Menor presente (ex: Dispneia aos esforços isolada) (1 pt)", 1, False, 0.5, 2, "Um critério menor respiratório/hemodinâmico presente."),
                _opt("opt_fram_min2_2", ">= 2 Critérios Menores presentes (ex: Dispneia aos esforços + Tosse noturna/Derrame pleural) (2 pts)", 2, False, 1.0, 3, "Dois ou mais critérios menores respiratórios presentes."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_fram_low",
                "label": "Diagnóstico Improvável pelos Critérios de Framingham (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Critérios clínicos insuficientes para Insuficiência Cardíaca. Investigar diagnósticos diferenciais de dispneia ou edema (DPOC, asma, anemia, insuficiência venosa crônica, hipoalbuminemia).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_fram_low_1", "Tratamento Direcionado à Causa Base Não Cardíaca", "Evitar diureticoterapia empírica sem evidência de congestão", "Via Oral", "Conforme etiologia", "Não aplicável.", "Não aplicável.", "Furosemida em pacientes hipovolêmicos ou com edema puramente linfático/venoso pode causar azotemia pré-renal.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_fram_low_1", "Investigação Diferencial de Dispneia / Edema", "Ambulatório", "Dosar BNP (< 35 pg/mL ou NT-proBNP < 125 pg/mL no ambulatório exclui IC com VPN > 95%).", lab="BNP ou NT-proBNP, ECG, RX de tórax, espirometria, hemograma, TSH, função renal e albumina.")
                ]
            },
            {
                "id": "tier_fram_mod",
                "label": "Suspeita Intermediária / Indeterminada (2 a 3 pontos)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Presença de apenas 1 Critério Maior isolado ou 2 a 3 Critérios Menores sem critério maior. Exige confirmação com Peptídeos Natriuréticos (BNP/NT-proBNP) e Ecocardiograma Transtorácico.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_fram_mod_1", "Diurético de Alça Criterioso (se sinais objetivos de congestão) + Investigação", "Furosemida 20 a 40 mg VO/IV se sobrecarga hídrica evidente", "VO ou IV", "1x a 2x/dia", "Reavaliar resposta clínica e diurese.", "Ajustar conforme função renal.", "Hipotensão arterial ou desidratação.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_fram_mod_1", "Confirmação Biomarcadora e Ecocardiográfica", "Observação / Ambulatório Prioritário", "Solicitar Ecocardiograma com Doppler tecidual (avaliar FEVE, E/e', volume atrial esquerdo e PSAP) e dosar BNP/NT-proBNP.", lab="BNP (corte PS > 100 pg/mL) ou NT-proBNP (corte PS > 300 pg/mL; ajustado por idade: > 450 se <50a, > 900 se 50-75a, > 1800 se >75a).")
                ]
            },
            {
                "id": "tier_fram_high",
                "label": "Diagnóstico Clínico Confirmado de Insuficiência Cardíaca (4 a 12 pontos)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 12,
                "statisticalOutcome": "Critérios de Framingham POSITIVOS (>= 2 Maiores ou 1 Maior + 2 Menores, sensibilidade de 92% e especificidade de 79% para IC sistólica/congestiva). Iniciar descongestão imediata e terapia modificadora de mortalidade (Quarteto Fantástico na ICFEr).",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_fram_high_furo", "Furosemida (Alívio Congestivo Imediato)", "40 a 80 mg IV (na IC aguda descompensada) ou 40 mg VO/dia (no paciente ambulatorial)", "IV ou VO", "8/8h a 12/12h conforme congestão", "Na IC aguda, administrar IV em até 60 min da chegada e avaliar sódio urinário em 2h (> 50-70 mEq/L) ou diurese > 100-150 mL/h.", "Doses dobradas se DRC.", "Choque hipovolêmico."),
                    _rx("rx_fram_high_gdmt", "Terapia Quádrupla Modificadora de Doença (após compensação se ICFEr FEVE <= 40%)", "Sacubitril/Valsartana (ou IECA) + Betabloqueador (Carvedilol/Bisoprolol/Succinato de Metoprolol) + Espironolactona 25mg + Dapagliflozina/Empagliflozina 10mg", "Via Oral", "Diário", "Respeitar washout de 36h entre suspensão do IECA e início do Sacubitril/Valsartana pelo risco de angioedema.", "Monitorar K e Cr 1-2 semanas após início de IECA/ARNI/Espironolactona.", "Não iniciar betabloqueador na vigência de congestão pulmonar aguda franca ou uso de inotrópicos.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_fram_high_1", "Classificação Fenotípica (ICFEr, ICFElr, ICFEp) e Perfil de Stevenson", "Enfermaria Cardiológica / UCO ou Ambulatório de IC", "Classificar imediatamente o Perfil Hemodinâmico de Stevenson (A, B, C ou L) se descompensação aguda; peso diário em jejum e controle hídrico.", proc="Ecocardiograma transtorácico obrigatório para definir Fração de Ejeção do VE e etiologia (isquêmica, hipertensiva, chagásica, valvar).", lab="BNP/NT-proBNP, troponina, sódio, potássio, ureia, creatinina, ferritina e saturação de transferrina (repor carboximaltose férrica IV se ferritina < 100 ou 100-299 com IST < 20%), TSH e sorologia para Chagas.")
                ]
            }
        ]
    }


def get_stevenson_nyha() -> dict:
    return {
        "id": "calc_stevenson_nyha",
        "slug": "stevenson-nyha",
        "name": "Perfil Clínico-Hemodinâmico de Stevenson & NYHA na IC Aguda",
        "acronym": "Stevenson-NYHA",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Insuficiência Cardíaca Aguda Descompensada",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Insuficiência Cardíaca e Hemodinâmica",
        "description": "Classificação matricial 2x2 de Nohria-Stevenson combinada à Classe Funcional NYHA para avaliação hemodinâmica à beira do leito da Insuficiência Cardíaca Aguda Descompensada em 4 perfis clínicos (Perfil A: Quente e Seco; Perfil B: Quente e Úmido; Perfil L: Frio e Seco; Perfil C: Frio e Úmido).",
        "summary": "Matriz hemodinâmica 2x2 (Congestão vs. Perfusão) e NYHA na IC Aguda (Perfis A, B, L e C).",
        "clinicalObjective": "Guiar a terapêutica imediata na sala de emergência e UTI conforme o quadrante hemodinâmico: vasodilatadores + diuréticos no Perfil B (Quente e Úmido), prova volêmica cautelosa no Perfil L (Frio e Seco) e inotrópicos/vasopressores no Perfil C (Frio e Úmido).",
        "targetPopulation": "Pacientes adultos admitidos com Insuficiência Cardíaca Aguda Descompensada (ICAD).",
        "calculationType": "branching_decision",
        "formulaExpression": "Congestao(Seco=0, Umido=2) + Perfusao(Quente=0, Frio=4) + NYHA(I_II=0, III_IV=1)",
        "evidenceSource": "Nohria A, Tsang SW, Fang JC, et al. Clinical assessment identifies hemodynamic profiles that predict outcomes in patients admitted with heart failure. J Am Coll Cardiol. 2003;41(10):1797-1804. Diretriz Brasileira de IC Aguda SBC.",
        "minPossibleScore": 0,
        "maxPossibleScore": 7,
        "baseScore": 0,
        "badge": "emergencia",
        "clinicalWarning": "DIRETRIZ DE MANEJO POR PERFIL: (1) No Perfil B (Quente e Úmido), NUNCA iniciar inotrópicos (Dobutamina aumenta mortalidade e arritmias quando a perfusão é normal); o tratamento é Diurético IV + Vasodilatador (Nitroglicerina) + VNI. (2) No Perfil C (Frio e Úmido), suspender betabloqueador se choque franco e iniciar Dobutamina (+/- Noradrenalina se PAS < 85-90 mmHg).",
        "radarAxes": [
            _axis("axis_stev_cong", "Eixo de Congestão (Pressão de Enchimento / PCWP)", "Respiratório", "pts"),
            _axis("axis_stev_perf", "Eixo de Hipoperfusão (Índice Cardíaco)", "Cardiovascular", "pts"),
            _axis("axis_stev_nyha", "Limitação Funcional (Classe NYHA)", "Cardiovascular", "classe"),
        ],
        "parameterGroups": [
            _grp("grp_stev_cong", "1. Eixo de Congestão à Beira do Leito (Seco vs. Úmido)", "stevenson-congestao", "axis_stev_cong", 1, "Avaliar: ortopneia, DPN, turgência jugular, refluxo hepatojugular, estertores pulmonares, B3, ascite, edema de MMII e linhas B ao ultrassom pulmonar.", [
                _opt("opt_stev_seco", "SECO (Sem Congestão — PCWP estimada normal <= 18 mmHg) (0 pts)", 0, True, 0.0, 1, "Ausência de sinais clínicos ou ultrassonográficos de sobrecarga volêmica pulmonar ou sistêmica."),
                _opt("opt_stev_umido", "ÚMIDO (Congestão Presente — PCWP elevada > 18 mmHg) (2 pts)", 2, False, 1.0, 2, "Presença de ortopneia, turgência jugular, estertores crepitantes, edema periférico ou hepatomegalia congestiva."),
            ]),
            _grp("grp_stev_perf", "2. Eixo de Perfusão Periférica (Quente vs. Frio)", "stevenson-perfusao", "axis_stev_perf", 2, "Avaliar: pressão de pulso estreita (< 25% da PAS), pulso filiforme/alternante, extremidades frias e sudoreicas, enchimento capilar > 3s, oligúria, sonolência/confusão e lactato elevado.", [
                _opt("opt_stev_quente", "QUENTE (Perfusão Preservada — Índice Cardíaco >= 2,2 L/min/m²) (0 pts)", 0, True, 0.0, 1, "Extremidades aquecidas, pressão de pulso preservada, sensório lúcido e diurese adequada."),
                _opt("opt_stev_frio", "FRIO (Hipoperfusão Tecidual / Baixo Débito — IC < 2,2 L/min/m²) (4 pts)", 4, False, 1.0, 2, "Extremidades frias/pegajosas, pressão de pulso convergente, oligúria, confusão mental e hiperlactatemia."),
            ]),
            _grp("grp_stev_nyha", "3. Classe Funcional da New York Heart Association (NYHA)", "stevenson-nyha", "axis_stev_nyha", 3, "Grau de limitação funcional aos esforços físicos.", [
                _opt("opt_stev_nyha_12", "NYHA I ou II — Sem limitação (I) ou dispneia apenas aos esforços habituais/moderados (II) (0 pts)", 0, True, 0.25, 1, "Capacidade funcional basal preservada ou levemente reduzida."),
                _opt("opt_stev_nyha_34", "NYHA III ou IV — Dispneia aos mínimos esforços (III) ou em repouso/ortopneia (IV) (1 pt)", 1, False, 1.0, 2, "Limitação funcional acentuada aos pequenos esforços ou sintomas em repouso."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_stev_a",
                "label": "Perfil A de Stevenson — Quente e Seco (Compensado) (0 a 1 ponto)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 1,
                "statisticalOutcome": "Hemodinâmica compensada (PCWP normal e Índice Cardíaco normal; mortalidade em 6 meses ~2%). Foco na titulação ambulatorial das 4 classes modificadoras de mortalidade na ICFEr.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_stev_a_gdmt", "Otimização do Quarteto Modificador de Doença (ARNI/IECA + BB + ARM + iSGLT2)", "Sacubitril/Valsartana até 97/103mg 12/12h + Carvedilol até 25-50mg 12/12h + Espironolactona 25mg/dia + Dapagliflozina 10mg/dia", "Via Oral", "Diário", "Titular doses a cada 2-4 semanas até dose-alvo de ensaio clínico ou máxima tolerada.", "Monitorar função renal e potássio.", "Angioedema prévio, gestação ou hipercalemia > 5,5 mEq/L.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_stev_a_1", "Seguimento Ambulatorial e Reabilitação Cardiopulmonar", "Alta / Ambulatório de IC", "Reabilitação cardíaca supervisionada, vacinação atualizada (Influenza e Pneumococo) e educação sobre peso diário.", lab="BNP/NT-proBNP, K, Na, Cr, ferritina e saturação de transferrina.")
                ]
            },
            {
                "id": "tier_stev_b",
                "label": "Perfil B de Stevenson — Quente e Úmido (Congestão com Perfusão Normal) (2 a 3 pontos)",
                "severityLevel": "high",
                "minScore": 2,
                "maxScore": 3,
                "statisticalOutcome": "Representa ~65-70% das internações por IC Aguda. Mortalidade intra-hospitalar de 3% a 7%. Tratamento pilar: Diurético de Alça IV + Vasodilatador IV (Nitroglicerina) + VNI se desconforto respiratório.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_stev_b_furo", "Furosemida Endovenosa (com bloqueio sequencial de néfron se resistência)", "40 a 80 mg IV em bolus inicial (pelo menos 1x a 2,5x a dose oral diária domiciliar — estudo DOSE)", "Intravenosa", "Bolus de 6/6h a 12/12h ou infusão contínua", "Avaliar diurese em 2h (meta > 100-150 mL/h) e sódio urinário em amostra isolada em 2h (meta > 50-70 mEq/L); se insuficiente, dobrar a dose e considerar associar Hidroclorotiazida ou Acetazolamida 500mg IV (estudo ADVOR).", "Doses maiores necessárias na DRC.", "Hipocalemia severa (repor KCl concomitante)."),
                    _rx("rx_stev_b_ntg", "Nitroglicerina Endovenosa (Tridil) em BIC (se PAS > 110 mmHg / Perfil B Vascular)", "10 a 200 mcg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua titulada a cada 5-10 min", "1 ampola (50 mg/10 mL) em 240 mL SG 5% ou SF 0,9% (200 mcg/mL) em frasco de vidro/polietileno.", "Preferir Nitroglicerina ao Nitroprussiato se houver doença coronariana isquêmica associada (evita roubo coronariano).", "PAS < 90-100 mmHg ou uso recente de sildenafil/tadalafil.", NITROGLYCERIN_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_stev_b_1", "Descongestão Guiada por Diurese/Ultrassom Pulmonar e VNI", "Sala de Emergência / UCO / Enfermaria", "MANTER o betabloqueador domiciliar (ou reduzir em 50% apenas se congestão grave; estudo B-CONVINCED). Monitorar peso diário e balanço hídrico.", vent="VNI (CPAP 8-10 cmH2O ou BiPAP) precoce se FR > 25 irpm ou SpO2 < 90% em edema agudo de pulmão.", lab="Sódio urinário em 2h, ureia, creatinina, Na, K, Mg, BNP/NT-proBNP e gasometria se desconforto.")
                ],
                "infusionProtocol": NITROGLYCERIN_PROTOCOL
            },
            {
                "id": "tier_stev_l",
                "label": "Perfil L de Stevenson — Frio e Seco (Hipoperfusão sem Congestão) (4 a 5 pontos)",
                "severityLevel": "high",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Representa ~5% das descompensações (geralmente por diureticoterapia excessiva ou disfunção grave de VE/VD sem hipervolemia). Exige prova volêmica cautelosa e ajuste de diuréticos/vasodilatadores.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    _rx("rx_stev_l_fluid", "Desafio Volêmico Cauteloso com Cristaloide + Suspensão Temporária de Diuréticos", "Ringer Lactato ou SF 0,9% 250 mL IV em 15 a 30 minutos com reavaliação auscultatória e ultrassonográfica", "Intravenosa", "Alíquota única reavaliável", "Suspender furosemida e vasodilatadores; se após restaurar euvolemia o paciente permanecer Frio (hipoperfundido), iniciar Dobutamina.", "Monitorar débito urinário.", "Suspender infusão imediatamente se surgirem estertores ou linhas B pulmonares (migração para Perfil C).")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_stev_l_1", "Avaliação Ecocardiográfica de Volume Sistólico e Veia Cava Inferior", "Unidade Coronariana / UTI", "Avaliar colapsabilidade da veia cava inferior e VTI da via de saída do VE ao POCUS antes e após alíquota de 250 mL.", lab="Lactato arterial, gasometria venosa central, função renal e eletrólitos.")
                ]
            },
            {
                "id": "tier_stev_c",
                "label": "Perfil C de Stevenson — Frio e Úmido (Choque Cardiogênico / Baixo Débito Congestivo) (6 a 7 pontos)",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 7,
                "statisticalOutcome": "Representa ~20% das IC agudas, com mortalidade intra-hospitalar de 15% a > 40%. Exige suporte inotrópico imediato (Dobutamina, Milrinona ou Levosimendana), associação de Noradrenalina se PAS < 85-90 mmHg e diurético apenas após restaurar perfusão.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_stev_c_dobuta", "Dobutamina Endovenosa em BIC (ou Levosimendana / Milrinona se betabloqueado crônico)", "2,5 a 15 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "1 ampola (250 mg = 20 mL) em 230 mL SG 5% ou SF 0,9% (1.000 mcg/mL).", "Sem ajuste renal para Dobutamina (Milrinona exige redução se ClCr < 50 mL/min).", "Se paciente em uso crônico de Carvedilol e PAS > 90 mmHg, Levosimendana (0,05-0,1 mcg/kg/min sem bolus) ou Milrinona atua pós-receptor beta.", DOBUTAMINE_PROTOCOL),
                    _rx("rx_stev_c_norepi", "Noradrenalina em BIC (se PAS < 85-90 mmHg ou PAM < 65 mmHg)", "0,05 a 1,0 mcg/kg/min IV contínua em BIC", "Intravenosa contínua em BIC", "Contínua", "4 ampolas (16 mg) em 234 mL SG 5% (64 mcg/mL). Veículo mandatório SG 5%.", "Sem ajuste renal.", "Restaurar pressão de perfusão coronariana e renal antes de forçar diurese com furosemida.", NOREPINEPHRINE_PROTOCOL)
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_stev_c_1", "Ressuscitação Hemodinâmica em UTI Cardiológica", "UTI Cardiológica", "Suspender betabloqueador e IECA/BRA na vigência de choque cardiogênico; instalar PAI e CVC; monitorar ScvO2 (> 70%), lactato e diurese horária (> 0,5 mL/kg/h).", proc="POCUS cardíaco imediato; considerar cateter de artéria pulmonar (Swan-Ganz) ou dispositivo de assistência circulatória mecânica em choque refratário (INTERMACS 1-2).", vasc="Cateter Venoso Central + Pressão Arterial Invasiva.", lab="Lactato seriado a cada 2-4h, ScvO2, gasometria arterial, função renal, transaminases, coagulograma, troponina e BNP.")
                ],
                "infusionProtocol": DOBUTAMINE_PROTOCOL
            }
        ]
    }


def get_maggic() -> dict:
    return {
        "id": "calc_maggic",
        "slug": "maggic-score",
        "name": "MAGGIC Risk Score para Mortalidade na Insuficiência Cardíaca",
        "acronym": "MAGGIC",
        "version": "1.0.0",
        "blockId": "block_02",
        "blockFile": "block_02.json",
        "category": "Cardiologia e Hemodinâmica",
        "subcategory": "Insuficiência Cardíaca Crônica e Avançada",
        "categorySlug": "bloco-02-cardiologia-hemodinamica",
        "categoryName": "Cardiologia e Hemodinâmica",
        "moduleName": "Insuficiência Cardíaca e Miocardiopatias",
        "description": "Escore prognóstico multidimensional derivado da Meta-Analysis Global Group in Chronic Heart Failure (39.372 pacientes de 30 estudos) para estimar a probabilidade de óbito em 1 e 3 anos na Insuficiência Cardíaca (tanto ICFEr quanto ICFEp).",
        "summary": "Predição de mortalidade em 1 e 3 anos na IC com FEVE reduzida ou preservada (0 a 50 pontos).",
        "clinicalObjective": "Identificar pacientes com Insuficiência Cardíaca de alto risco de mortalidade candidatos a terapias avançadas (Ressincronização Cardíaca, CDI, assistência ventricular ou listagem para Transplante Cardíaco).",
        "targetPopulation": "Pacientes adultos com Insuficiência Cardíaca crônica ou após compensação hospitalar (qualquer Fração de Ejeção).",
        "calculationType": "additive_points",
        "formulaExpression": "FEVE + Idade + PAS + IMC + Creatinina + NYHA_Comorbidades_NeuroHormonal",
        "evidenceSource": "Pocock SJ, Ariti CA, McMurray JJ, et al. Predicting survival in heart failure: a risk score based on 39 372 patients from 30 studies. Eur Heart J. 2013;34(19):1404-1413.",
        "minPossibleScore": 0,
        "maxPossibleScore": 50,
        "baseScore": 0,
        "badge": "cardiologia",
        "clinicalWarning": "PARADOXO DA OBESIDADE E DA PRESSÃO ARTERIAL NA IC: No MAGGIC Score, valores mais baixos de IMC (< 20 kg/m² refletindo caquexia cardíaca catabólica) e de PAS (< 110 mmHg refletindo menor reserva inotrópica e intolerância a neuro-hormonais) conferem MAIOR pontuação e pior prognóstico.",
        "radarAxes": [
            _axis("axis_maggic_lv", "Disfunção Ventricular (FEVE e PAS)", "Cardiovascular", "pts"),
            _axis("axis_maggic_renal_age", "Reserva Etária e Síndrome Cardiorrenal", "Renal", "pts"),
            _axis("axis_maggic_nutri", "Estado Nutricional / Caquexia (IMC)", "Metabólico", "pts"),
            _axis("axis_maggic_nyha", "Capacidade Funcional (NYHA) e Comorbidades", "Respiratório", "pts"),
        ],
        "parameterGroups": [
            _grp("grp_maggic_1", "1. Fração de Ejeção do Ventrículo Esquerdo (FEVE %)", "maggic-feve", "axis_maggic_lv", 1, "FEVE aferida pelo método de Simpson biplanar ao ecocardiograma.", [
                _opt("opt_maggic_1_0", "FEVE >= 40% (ICFEp / ICFElr) (0 pts)", 0, True, 0.0, 1, "Fração de ejeção preservada ou levemente reduzida."),
                _opt("opt_maggic_1_2", "FEVE 35% a 39% (2 pts)", 2, False, 0.3, 2, "Disfunção sistólica moderada."),
                _opt("opt_maggic_1_3", "FEVE 30% a 34% (3 pts)", 3, False, 0.5, 3, "Disfunção sistólica moderada a importante."),
                _opt("opt_maggic_1_5", "FEVE 25% a 29% (5 pts)", 5, False, 0.75, 4, "Disfunção sistólica grave."),
                _opt("opt_maggic_1_7", "FEVE < 25% (7 pts)", 7, False, 1.0, 5, "Disfunção sistólica muito grave do ventrículo esquerdo."),
            ], unit="%"),
            _grp("grp_maggic_2", "2. Faixa Etária (Ponderada pela FEVE)", "maggic-idade", "axis_maggic_renal_age", 2, "Idade cronológica do paciente.", [
                _opt("opt_maggic_2_0", "< 55 anos (0 pts)", 0, True, 0.0, 1, "Menos de 55 anos."),
                _opt("opt_maggic_2_4", "55 a 64 anos (4 pts)", 4, False, 0.25, 2, "Faixa de 55 a 64 anos."),
                _opt("opt_maggic_2_8", "65 a 74 anos (8 pts)", 8, False, 0.55, 3, "Faixa de 65 a 74 anos."),
                _opt("opt_maggic_2_12", "75 a 79 anos (12 pts)", 12, False, 0.8, 4, "Faixa de 75 a 79 anos."),
                _opt("opt_maggic_2_15", ">= 80 anos (15 pts)", 15, False, 1.0, 5, "Idoso longevo (>= 80 anos)."),
            ], unit="anos"),
            _grp("grp_maggic_3", "3. Pressão Arterial Sistólica Basal (PAS em mmHg)", "maggic-pas", "axis_maggic_lv", 3, "PAS basal em repouso (valores menores refletem menor reserva contrátil).", [
                _opt("opt_maggic_3_0", "PAS >= 140 mmHg (0 pts)", 0, True, 0.0, 1, "Reserva pressórica ampla."),
                _opt("opt_maggic_3_2", "PAS 120 a 139 mmHg (2 pts)", 2, False, 0.35, 2, "PAS normotensa habitual."),
                _opt("opt_maggic_3_3", "PAS 110 a 119 mmHg (3 pts)", 3, False, 0.65, 3, "PAS limítrofe."),
                _opt("opt_maggic_3_5", "PAS < 110 mmHg (5 pts)", 5, False, 1.0, 4, "Hipotensão relativa associada a baixo débito e menor tolerância a titulação de fármacos."),
            ], unit="mmHg"),
            _grp("grp_maggic_4", "4. Índice de Massa Corporal (IMC em kg/m²)", "maggic-imc", "axis_maggic_nutri", 4, "Paradoxo nutricional na IC: o baixo peso / caquexia cardíaca agrava a mortalidade.", [
                _opt("opt_maggic_4_0", "IMC >= 30 kg/m² (0 pts)", 0, True, 0.0, 1, "Reserva metabólica preservada."),
                _opt("opt_maggic_4_2", "IMC 25,0 a 29,9 kg/m² (2 pts)", 2, False, 0.3, 2, "Sobrepeso."),
                _opt("opt_maggic_4_4", "IMC 20,0 a 24,9 kg/m² (4 pts)", 4, False, 0.65, 3, "Eutrofia."),
                _opt("opt_maggic_4_6", "IMC < 20,0 kg/m² — Caquexia Cardíaca / Sarcopenia (6 pts)", 6, False, 1.0, 4, "Estado hipercatabólico inflamatório da IC avançada."),
            ], unit="kg/m2"),
            _grp("grp_maggic_5", "5. Creatinina Sérica (mg/dL)", "maggic-creatinina", "axis_maggic_renal_age", 5, "Função renal basal refletindo síndrome cardiorrenal.", [
                _opt("opt_maggic_5_0", "Creatinina < 1,0 mg/dL (< 90 µmol/L) (0 pts)", 0, True, 0.0, 1, "Função renal normal."),
                _opt("opt_maggic_5_2", "Creatinina 1,0 a 1,49 mg/dL (90-130 µmol/L) (2 pts)", 2, False, 0.3, 2, "Disfunção renal leve."),
                _opt("opt_maggic_5_5", "Creatinina 1,5 a 2,49 mg/dL (131-220 µmol/L) (5 pts)", 5, False, 0.65, 3, "Síndrome cardiorrenal moderada."),
                _opt("opt_maggic_5_8", "Creatinina >= 2,5 mg/dL (> 220 µmol/L) (8 pts)", 8, False, 1.0, 4, "Síndrome cardiorrenal grave."),
            ], unit="mg/dL"),
            _grp("grp_maggic_6", "6. Classe Funcional NYHA, Comorbidades (DM/DPOC) e Bloqueio Neuro-Hormonal", "maggic-nyha-comorb", "axis_maggic_nyha", 6, "Integra NYHA (I a IV), presença de Diabetes/DPOC/Tabagismo e uso de Betabloqueador + IECA/BRA/ARNI.", [
                _opt("opt_maggic_6_0", "NYHA I-II em uso otimizado de Betabloqueador + IECA/BRA/ARNI sem DM/DPOC (0 pts)", 0, True, 0.0, 1, "Boa classe funcional sob bloqueio neuro-hormonal completo."),
                _opt("opt_maggic_6_4", "NYHA II-III OU presença de Diabetes Mellitus / DPOC (4 pts)", 4, False, 0.5, 2, "Limitação moderada ou comorbidades sistêmicas associadas."),
                _opt("opt_maggic_6_9", "NYHA III-IV com DM/DPOC e/ou intolerância a Betabloqueador/IECA (9 pts)", 9, False, 1.0, 3, "IC avançada sintomática com perda de tolerância ao bloqueio neuro-hormonal."),
            ]),
        ],
        "riskTiers": [
            {
                "id": "tier_maggic_low",
                "label": "Baixo Risco Prognóstico (0 a 16 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 16,
                "statisticalOutcome": "Mortalidade estimada em 1 ano < 7% e em 3 anos < 17%. Bom prognóstico sob manutenção da terapia farmacológica modificadora de doença.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    _rx("rx_maggic_low_1", "Manutenção do Quarteto Modificador de Doença (GDMT)", "Sacubitril/Valsartana + Carvedilol/Bisoprolol/Metoprolol + Espironolactona + Dapagliflozina/Empagliflozina", "Via Oral", "Diário", "Na ICFEp (FEVE >= 50%), o pilar com benefício comprovado (DELIVER / EMPEROR-Preserved) é o iSGLT2 (Dapagliflozina/Empagliflozina 10mg/dia) + diurético se congestão.", "Monitorar K e Cr.", "Hipercalemia > 5,5 mEq/L.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_maggic_low_1", "Reabilitação Cardíaca e Seguimento Ambulatorial Semestral", "Ambulatório de Cardiologia", "Exercício aeróbico supervisionado (melhora VO2 pico e qualidade de vida).", lab="Eletrólitos, função renal, perfil de ferro e ECG anual.")
                ]
            },
            {
                "id": "tier_maggic_mod",
                "label": "Risco Intermediário (17 a 24 pontos)",
                "severityLevel": "intermediate",
                "minScore": 17,
                "maxScore": 24,
                "statisticalOutcome": "Mortalidade estimada em 1 ano de 7% a 15% e em 3 anos de 18% a 35%. Requer titulação máxima das terapias, correção de ferropenia IV e avaliação de elegibilidade para dispositivos eletrônicos implantáveis (CDI / TRC).",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    _rx("rx_maggic_mod_1", "Titulação Máxima de GDMT + Carboximaltose Férrica IV (se ferropenia) + Ivabradina (se FC >= 70 em sinusal)", "Carboximaltose férrica 500-1000mg IV (se ferritina < 100 ou 100-299 com IST < 20%) + Ivabradina 5-7,5mg 12/12h se ritmo sinusal com FC >= 70 bpm sob dose máxima de BB", "VO e IV", "Conforme protocolo", "A reposição venosa de ferro reduz hospitalizações por IC (estudos AFFIRM-AHF e IRONMAN).", "Sem ajuste renal para Carboximaltose.", "Ivabradina é ineficaz e contraindicada na Fibrilação Atrial.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_maggic_mod_1", "Avaliação Eletrofisiológica para CDI e Terapia de Ressincronização (TRC)", "Ambulatório de IC Especializado", "Se FEVE <= 35% após >= 3 meses de tratamento otimizado: indicar CDI para prevenção primária de morte súbita; se BRE completo com QRS >= 150 ms (ou 130-149 ms), indicar Ressincronizador (TRC-D).", proc="Implante de CDI ou Ressincronizador Cardíaco (TRC-D) conforme ECG e FEVE.", lab="ECG de 12 derivações (medir duração e morfologia do QRS), Ecocardiograma, Holter 24h, ferritina e IST.")
                ]
            },
            {
                "id": "tier_maggic_high",
                "label": "Alto / Altíssimo Risco — IC Avançada (25 a 50 pontos)",
                "severityLevel": "critical",
                "minScore": 25,
                "maxScore": 50,
                "statisticalOutcome": "Mortalidade em 1 ano de 16% a > 40% e em 3 anos de 37% a > 75% (critérios I NEED HELP de IC avançada). Encaminhamento prioritário para Centro de Insuficiência Cardíaca Avançada / Transplante Cardíaco.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    _rx("rx_maggic_high_1", "Manejo de IC Avançada (Diureticoterapia Combinada, Vericiguat ou Inotrópicos em Ponte)", "Furosemida em altas doses (+/- Tiazídico) + Vericiguat 2,5-10mg VO/dia (pós-descompensação, estudo VICTORIA) ou Levosimendana/Dobutamina em ponte", "VO ou IV", "Diário / Hospital-Dia", "Se intolerância progressiva a IECA/ARNI/BB por hipotensão sintomática, reconhecer transição para IC estágio D.", "Cautela com síndrome cardiorrenal tipo 2.", "Contraindicações específicas a cada agente.")
                ],
                "nonPharmacologicalActions": [
                    _nonrx("nonrx_maggic_high_1", "Avaliação para Transplante Cardíaco, Dispositivo de Assistência Ventricular (LVAD) ou Cuidados Paliativos", "Centro de IC Avançada e Transplante", "Realizar Teste Cardiopulmonar de Exercício (Ergoespirometria: VO2 pico < 12 mL/kg/min em uso de BB ou < 14 sem BB indica listagem para Transplante Cardíaco) e Cateterismo Direito (medir resistência vascular pulmonar).", proc="Ergoespirometria, Cateterismo Cardíaco Direito (Swan-Ganz), avaliação para LVAD (HeartMate 3) ou Transplante Cardíaco.", lab="Painel imunológico (PRA), sorologias pré-transplante, BNP/NT-proBNP, função renal e hepática.")
                ]
            }
        ]
    }


def get_block_02_calculators() -> list[dict]:
    return [
        get_heart(),
        get_timi_scasst(),
        get_timi_stemi(),
        get_grace(),
        get_killip(),
        get_cha2ds2_vasc(),
        get_has_bled(),
        get_atria(),
        get_hemorr2hages(),
        get_framingham_ic(),
        get_stevenson_nyha(),
        get_maggic(),
    ]


BLOCK_02_SYNONYMS: dict[str, list[str]] = {
    "calc_heart": [
        "heart", "heart score", "escore heart", "dor toracica", "dor torácica", "dor no peito",
        "emergencia cardiologica", "pronto socorro dor toracica", "mace", "troponina",
        "angina", "infarto", "iam", "scasst", "alta precoce dor toracica", "six 2008",
    ],
    "calc_timi_scasst": [
        "timi", "timi scasst", "timi iamssst", "timi angina instavel", "angina instável",
        "iam sem supra", "infarto sem supra", "scasst", "nstemi", "escore timi",
        "antman", "dupla antiagregacao", "cateterismo precoce", "dor anginosa",
    ],
    "calc_timi_stemi": [
        "timi stemi", "timi iamcsst", "timi com supra", "infarto com supra", "iam com supra",
        "stemi", "supradesnivelamento de st", "angioplastia primaria", "trombolise",
        "tenecteplase", "fibrinolise", "mortalidade iam 30 dias", "morrow",
    ],
    "calc_grace": [
        "grace", "grace 2.0", "grace score", "escore grace", "mortalidade sca",
        "sindrome coronariana aguda", "síndrome coronariana aguda", "estrategia invasiva precoce",
        "cateterismo 24h", "iamssst", "iamcsst", "granger", "risco coronariano",
    ],
    "calc_killip": [
        "killip", "killip kimball", "classificacao de killip", "classificação de killip",
        "estertores pulmonares", "edema agudo de pulmao", "eap", "choque cardiogenico",
        "choque cardiogênico", "terceira bulha", "b3", "infarto agudo do miocardio",
        "dobutamina", "noradrenalina", "nitroglicerina", "tridil",
    ],
    "calc_cha2ds2_vasc": [
        "cha2ds2 vasc", "cha2ds2-vasc", "cha2ds2vasc", "chads2", "chads vasc",
        "fibrilacao atrial", "fibrilação atrial", "fa", "flutter atrial", "risco de avc",
        "anticoagulacao", "anticoagulação", "doac", "apixabana", "rivaroxabana",
        "dabigatrana", "edoxabana", "varfarina", "tromboembolismo",
    ],
    "calc_has_bled": [
        "has bled", "has-bled", "hasbled", "escore has-bled", "risco de sangramento",
        "sangramento maior", "hemorragia anticoagulacao", "fibrilacao atrial sangramento",
        "rni labil", "inr labil", "varfarina sangramento", "pisters",
    ],
    "calc_atria": [
        "atria", "atria score", "atria bleeding", "escore atria", "sangramento fa",
        "risco hemorragico atria", "anemia anticoagulacao", "insuficiencia renal fa",
        "hemorragia varfarina", "fang 2011", "fibrilacao atrial",
    ],
    "calc_hemorr2hages": [
        "hemorr2hages", "hemorrhages", "escore hemorr2hages", "sangramento idoso",
        "risco de quedas anticoagulacao", "cancer anticoagulacao", "plaquetopenia fa",
        "ressangramento", "rebleeding", "cyp2c9", "gage 2006",
    ],
    "calc_framingham_ic": [
        "framingham", "framingham ic", "criterios de framingham", "critérios de framingham",
        "diagnostico insuficiencia cardiaca", "diagnóstico insuficiência cardíaca",
        "dispneia paroxistica noturna", "ortopneia", "turgencia jugular", "cardiomegalia",
        "refluxo hepatojugular", "edema maleolar", "galope b3",
    ],
    "calc_stevenson_nyha": [
        "stevenson", "perfil de stevenson", "nohria stevenson", "nyha", "classe funcional nyha",
        "quente e seco", "quente e umido", "quente e úmido", "frio e umido", "frio e seco",
        "perfil a", "perfil b", "perfil c", "perfil l", "ic aguda descompensada",
        "insuficiencia cardiaca aguda", "dobutamina", "tridil", "furosemida",
    ],
    "calc_maggic": [
        "maggic", "maggic score", "escore maggic", "mortalidade insuficiencia cardiaca",
        "sobrevida ic", "prognostico ic", "icfer", "icfep", "fracao de ejecao",
        "fração de ejeção", "paradoxo da obesidade", "caquexia cardiaca", "pocock 2013",
    ],
}
