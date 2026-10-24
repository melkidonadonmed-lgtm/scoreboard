"""
Block 05: Cirurgia Geral, Trauma e Risco Cirúrgico (11 Calculadoras Monográficas)
1. calc_alvarado (Escore de Alvarado / MANTRELS — Apendicite Aguda, 0-10 pts)
2. calc_ripasa (Escore RIPASA — Apendicite Aguda de Alta Sensibilidade, 0-16.5 pts)
3. calc_tokyo_tg18 (Critérios de Tokyo TG18 — Colecistite e Colangite Aguda)
4. calc_rts (RTS — Revised Trauma Score no Politrauma, 0-12 pts)
5. calc_iss (ISS — Injury Severity Score, Gravidade Anatômica do Trauma, 0-75 pts)
6. calc_triss (TRISS — Trauma and Injury Severity Score, Probabilidade de Sobrevida)
7. calc_parkland_aba (Ressuscitação Volêmica no Grande Queimado — ABA 2 mL/kg/% SCQ & Parkland 4 mL)
8. calc_asa (Classificação do Estado Físico ASA — ASA I a VI + E)
9. calc_rcri_lee (RCRI — Índice de Risco Cardíaco Revisado de Lee, 0-6 pts)
10. calc_goldman (Índice de Risco Cardíaco Multifatorial de Goldman, 0-53 pts)
11. calc_caprini (Escore de Caprini — Risco de TEV em Pacientes Cirúrgicos, 0-15 pts)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL


def _axis(axis_id: str, label: str, system: str, unit: str = "pts") -> dict:
    return {
        "id": axis_id,
        "label": label,
        "system": system,
        "unit": unit,
        "baselineValue": 0,
        "maxAxisValue": 1,
    }


def _opt(
    opt_id: str,
    label: str,
    pts: float,
    baseline: bool,
    radar: float,
    order: int,
    desc: str,
) -> dict:
    return {
        "id": opt_id,
        "label": label,
        "pointValue": pts,
        "isNormalBaseline": baseline,
        "radarNormalizedValue": radar,
        "sortOrder": order,
        "description": desc,
    }


def _grp(
    grp_id: str,
    name: str,
    slug: str,
    axis_id: str,
    order: int,
    help_text: str,
    options: list[dict],
) -> dict:
    return {
        "id": grp_id,
        "name": name,
        "slug": slug,
        "inputType": "single_choice",
        "radarAxisId": axis_id,
        "normalBaselineValue": 0,
        "maxAxisValue": 1,
        "sortOrder": order,
        "helpText": help_text,
        "options": options,
    }


def _rx(
    rx_id: str,
    drug: str,
    dosage: str,
    route: str,
    freq: str,
    dilution: str | None = None,
    renal: str | None = None,
    contra: str | None = None,
    infusion: dict | None = None,
) -> dict:
    d = {
        "id": rx_id,
        "drugName": drug,
        "dosage": dosage,
        "route": route,
        "frequency": freq,
    }
    if dilution:
        d["dilutionInstructions"] = dilution
    if renal:
        d["renalAdjustment"] = renal
    if contra:
        d["contraindications"] = contra
    if infusion:
        d["infusionProtocol"] = infusion
    return d


def _nonrx(
    nrx_id: str,
    title: str,
    disp: str,
    mon: str,
    proc: str | None = None,
    vent: str | None = None,
    vasc: str | None = None,
    lab: str | None = None,
) -> dict:
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


def _tier(
    tier_id: str,
    label: str,
    sev: str,
    min_s: float,
    max_s: float,
    outcome: str,
    color: str,
    rx_list: list[dict],
    nonrx_list: list[dict],
    infusion: dict | None = None,
) -> dict:
    d = {
        "id": tier_id,
        "label": label,
        "severityLevel": sev,
        "minScore": min_s,
        "maxScore": max_s,
        "statisticalOutcome": outcome,
        "colorHex": color,
        "pharmacologicalActions": rx_list,
        "nonPharmacologicalActions": nonrx_list,
    }
    if infusion:
        d["infusionProtocol"] = infusion
    return d


def get_alvarado() -> dict:
    return {
        "id": "calc_alvarado",
        "slug": "escore-alvarado-mantrels",
        "name": "Escore de Alvarado (MANTRELS) — Apendicite Aguda",
        "acronym": "Alvarado",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Abdome Agudo e Cirurgia de Urgência",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Abdome Agudo e Apendicite",
        "description": "Estratificação diagnóstica clássica (acrônimo MANTRELS, 0 a 10 pontos) para suspeita clínica de apendicite aguda no pronto-socorro, combinando sintomas viscerais, sinais de irritação peritoneal parietal em fossa ilíaca direita e resposta leucocitária aguda.",
        "summary": "Estratificação clínica e laboratorial de probabilidade de apendicite aguda (MANTRELS, 0-10 pts).",
        "clinicalObjective": "Guiar a decisão entre alta com reavaliação, exames de imagem (USG/TC de abdome) ou indicação cirúrgica de apendicectomia laparoscópica precoce.",
        "targetPopulation": "Pacientes adolescentes e adultos atendidos na emergência com dor abdominal aguda em fossa ilíaca direita (FID).",
        "calculationType": "additive_points",
        "formulaExpression": "M(1) + A(1) + N(1) + T(2) + R(1) + E(1) + L(2) + S(1) [0 a 10 pontos]",
        "evidenceSource": "Alvarado A. A practical score for the early diagnosis of acute appendicitis. Ann Emerg Med. 1986;15(5):557-564. Diretrizes WSES Jerusalem 2020.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 0,
        "badge": "cirurgia",
        "clinicalWarning": "Em mulheres em idade fértil (diagnóstico diferencial ginecológico: gravidez ectópica, torção ovariana, DIP) e idosos, recomenda-se exame de imagem (USG ou TC de abdome/pelve) mesmo com Alvarado >= 7 antes da apendicectomia.",
        "radarAxes": [
            _axis("axis_alv_symp", "Sintomas Viscerais (MAN)", "Gastrointestinal"),
            _axis("axis_alv_signs", "Irritação Peritoneal (TRE)", "Cirúrgico"),
            _axis("axis_alv_lab", "Inflamação Leucocitária (LS)", "Hematológico"),
        ],
        "parameterGroups": [
            _grp("grp_alv_migration", "1. Migração da Dor para Fossa Ilíaca Direita (M)", "migracao-dor-fid", "axis_alv_symp", 1, "Dor inicialmente periumbilical/epigástrica visceral que migra para o ponto de McBurney.", [
                _opt("opt_alv_mig_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem relato de migração clássica da dor para FID."),
                _opt("opt_alv_mig_1", "Presente (+1 pt)", 1, False, 0.35, 2, "Dor visceral periumbilical que localiza em fossa ilíaca direita em 6-12h."),
            ]),
            _grp("grp_alv_anorexia", "2. Anorexia ou Cetose Urinária (A)", "anorexia-alvarado", "axis_alv_symp", 2, "Inapetência aguda desde o início do quadro doloroso.", [
                _opt("opt_alv_ano_0", "Ausente / Apetite preservado (0 pts)", 0, True, 0.0, 1, "Apetite preservado sem cetonúria."),
                _opt("opt_alv_ano_1", "Anorexia presente (+1 pt)", 1, False, 0.35, 2, "Perda súbita de apetite ou cetonúria documentada no EAS."),
            ]),
            _grp("grp_alv_nausea", "3. Náuseas ou Vômitos (N)", "nauseas-vomitos-alvarado", "axis_alv_symp", 3, "Náuseas ou episódios eméticos que sucedem o início da dor abdominal.", [
                _opt("opt_alv_nau_0", "Ausentes (0 pts)", 0, True, 0.0, 1, "Sem náuseas ou vômitos associados."),
                _opt("opt_alv_nau_1", "Presentes (+1 pt)", 1, False, 0.35, 2, "Náuseas ou vômitos reflexos secundários à distensão apendicular."),
            ]),
            _grp("grp_alv_tenderness", "4. Defesa / Dor à Palpação em Fossa Ilíaca Direita (T)", "defesa-fid-alvarado", "axis_alv_signs", 4, "Dor máxima localizada à palpação profunda no quadrante inferior direito (Ponto de McBurney).", [
                _opt("opt_alv_ten_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Fossa ilíaca direita indolor e flácida à palpação."),
                _opt("opt_alv_ten_2", "Presente (+2 pts)", 2, False, 0.7, 2, "Dor franca ou defesa muscular localizada em ponto de McBurney."),
            ]),
            _grp("grp_alv_rebound", "5. Descompressão Brusca Dolorosa — Sinal de Blumberg (R)", "blumberg-alvarado", "axis_alv_signs", 5, "Dor aguda à descompressão súbita em FID, indicando irritação peritoneal parietal.", [
                _opt("opt_alv_reb_0", "Ausente / Blumberg negativo (0 pts)", 0, True, 0.0, 1, "Sem sinais de peritonismo parietal em FID."),
                _opt("opt_alv_reb_1", "Presente / Blumberg positivo (+1 pt)", 1, False, 1.0, 2, "Descompressão brusca dolorosa positiva em FID (ou sinais de Rovsing/Dunphy)."),
            ]),
            _grp("grp_alv_elevation", "6. Elevação de Temperatura / Febre >= 37,3 °C (E)", "febre-alvarado", "axis_alv_signs", 6, "Temperatura axilar/oral aferida na admissão >= 37,3 °C.", [
                _opt("opt_alv_fev_0", "Afebril (< 37,3 °C) (0 pts)", 0, True, 0.0, 1, "Temperatura corporal dentro da faixa normal."),
                _opt("opt_alv_fev_1", "Subfebril / Febril (>= 37,3 °C) (+1 pt)", 1, False, 0.5, 2, "Elevação térmica sugestiva de processo inflamatório/infeccioso agudo."),
            ]),
            _grp("grp_alv_leukocytosis", "7. Leucocitose > 10.000/mm³ (L)", "leucocitose-alvarado", "axis_alv_lab", 7, "Contagem global de leucócitos no hemograma de admissão.", [
                _opt("opt_alv_leu_0", "Leucócitos <= 10.000/mm³ (0 pts)", 0, True, 0.0, 1, "Contagem leucocitária normal."),
                _opt("opt_alv_leu_2", "Leucocitose > 10.000/mm³ (+2 pts)", 2, False, 0.75, 2, "Leucocitose aguda corroborando inflamação apendicular."),
            ]),
            _grp("grp_alv_shift", "8. Desvio à Esquerda / Neutrofilia > 75% (S)", "desvio-esquerda-alvarado", "axis_alv_lab", 8, "Predomínio polimorfonuclear (neutrófilos segmentados + bastonetes > 75%).", [
                _opt("opt_alv_shf_0", "Ausente (Neutrófilos <= 75%) (0 pts)", 0, True, 0.0, 1, "Sem neutrofilia ou desvio à esquerda significativo."),
                _opt("opt_alv_shf_1", "Presente (Neutrófilos > 75% ou bastonetose) (+1 pt)", 1, False, 1.0, 2, "Neutrofilia > 75% ou aumento de bastonetes."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_alv_low", "Baixa Probabilidade de Apendicite (0 a 4 pontos)", "low", 0, 4, "Probabilidade de apendicite aguda < 5-10% (VPN > 95% para exclusão clínica inicial).", "#10b981", [
                _rx("rx_alv_low_1", "Dipirona Sódica ou Escopolamina", "Dipirona 1 g IV/VO 6/6h se dor; evitar opioides fortes antes da definição diagnóstica", "IV / VO", "6/6h se dor"),
            ], [
                _nonrx("nrx_alv_low_1", "Investigação de Diagnósticos Diferenciais e Alta com Sinais de Alarme", "Alta Orientada / Observação Breve", "Reavaliação em 12-24h se persistência da dor; solicitar EAS e Beta-hCG em mulheres em idade fértil."),
            ]),
            _tier("tier_alv_mod", "Probabilidade Intermediária / Equívoca (5 a 6 pontos)", "intermediate", 5, 6, "Probabilidade de apendicite aguda de 35% a 60%. Exame de imagem mandatório.", "#f59e0b", [
                _rx("rx_alv_mod_1", "Hidratação Cristaloide e Analgesia Controlada", "Ringer Lactato 1.000 mL IV + Dipirona 1 g IV 6/6h + Ondansetrona 4-8 mg IV 8/8h", "IV", "Regrada", "A analgesia venosa não mascara o exame físico peritoneal e melhora a cooperação no ultrassom."),
            ], [
                _nonrx("nrx_alv_mod_1", "Exame de Imagem Obrigatório (USG Abdome ou TC com Contraste)", "Observação em Pronto-Socorro", "Jejum oral preventivo, USG de abdome total/FID como 1ª linha (ou TC de abdome/pelve se USG inconclusivo ou IMC elevado).", "Avaliação pela Cirurgia Geral após imagem."),
            ]),
            _tier("tier_alv_high", "Alta Probabilidade de Apendicite Aguda (7 a 10 pontos)", "high", 7, 10, "Probabilidade de apendicite aguda de 78% a 93% (em homens jovens > 90%). Indicação cirúrgica.", "#ef4444", [
                _rx("rx_alv_high_1", "Antibioticoprofilaxia / Antibioticoterapia Pré-Operatória", "Cefoxitina 2 g IV na indução anestésica (ou Ceftriaxona 2 g IV + Metronidazol 500 mg IV se suspeita de apendicite complicada/perfurada)", "IV", "30-60 min antes da incisão cirúrgica", "Diluir em 100 mL de SF 0,9%; manter por 3-5 dias se necrose/perfuração transmural."),
                _rx("rx_alv_high_2", "Ressuscitação Cristaloide e Analgesia Multimodal", "Ringer Lactato 20 mL/kg IV + Morfina 2-4 mg IV titulada + Ondansetrona 8 mg IV", "IV", "Pré-operatório imediato"),
            ], [
                _nonrx("nrx_alv_high_1", "Apendicectomia Videolaparoscópica de Urgência", "Centro Cirúrgico / Internação Cirúrgica", "Jejum absoluto (NPO), avaliação cirúrgica imediata. Em mulheres em idade fértil ou idosos, realizar TC/USG rápido pré-operatório.", "Apendicectomia videolaparoscópica."),
            ]),
        ],
    }


def get_ripasa() -> dict:
    return {
        "id": "calc_ripasa",
        "slug": "escore-ripasa-apendicite",
        "name": "Escore RIPASA — Apendicite Aguda de Alta Sensibilidade",
        "acronym": "RIPASA",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Abdome Agudo e Cirurgia de Urgência",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Abdome Agudo e Apendicite",
        "description": "Sistema diagnóstico de 14 parâmetros clínicos, demográficos e laboratoriais (Raja Isteri Pengiran Anak Saleha Appendicitis Score, 0 a 16,5 pontos) desenvolvido para superar a baixa sensibilidade do escore de Alvarado em populações miscigenadas, incorporando tempo de sintomas, sinal de Rovsing e EAS negativo.",
        "summary": "Escore de alta sensibilidade (98%) para apendicite aguda com 8 grupos clínicos e EAS negativo (0-16,5 pts).",
        "clinicalObjective": "Reduzir a taxa de apendicectomias brancas (negativas) e identificar precocemente casos atípicos de apendicite aguda com sensibilidade superior ao Alvarado.",
        "targetPopulation": "Pacientes com dor em fossa ilíaca direita aguda atendidos em unidade de emergência.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma de 8 domínios estruturados (Demografia + Sintomas + Sinais de FID + Laboratório + EAS) [0 a 16,5 pontos]",
        "evidenceSource": "Chong CF, Adi MI, Thien A, et al. Development of the RIPASA score: a new appendicitis scoring system for the diagnosis of acute appendicitis. Singapore Med J. 2010;51(3):220-225.",
        "minPossibleScore": 0,
        "maxPossibleScore": 16.5,
        "baseScore": 0,
        "badge": "cirurgia",
        "clinicalWarning": "O corte RIPASA >= 7,5 pontos apresenta sensibilidade de 98% e especificidade de 81% para apendicite aguda, superando significativamente o Alvarado em pacientes asiáticos, latino-americanos e do Oriente Médio.",
        "radarAxes": [
            _axis("axis_rip_demo", "Demografia e Tempo", "Epidemiológico"),
            _axis("axis_rip_symp", "Sintomas Digestivos", "Gastrointestinal"),
            _axis("axis_rip_signs", "Peritonismo em FID", "Cirúrgico"),
            _axis("axis_rip_lab", "Laboratório e EAS", "Laboratorial"),
        ],
        "parameterGroups": [
            _grp("grp_rip_demo", "1. Perfil Demográfico (Sexo e Faixa Etária)", "demografia-ripasa", "axis_rip_demo", 1, "Pontuação combinada de sexo biológico (Feminino +0,5 / Masculino +1,0) e idade (< 40 anos +1,0 / >= 40 anos +0,5).", [
                _opt("opt_rip_dem_f_old", "Sexo Feminino e Idade >= 40 anos (+1,0 pt)", 1.0, True, 0.2, 1, "Mulher >= 40 anos (0,5 + 0,5 pt)."),
                _opt("opt_rip_dem_f_yng", "Sexo Feminino < 40 anos OU Masculino >= 40 anos (+1,5 pts)", 1.5, False, 0.5, 2, "Mulher jovem (0,5 + 1,0) ou Homem >= 40 anos (1,0 + 0,5)."),
                _opt("opt_rip_dem_m_yng", "Sexo Masculino e Idade < 40 anos (+2,0 pts)", 2.0, False, 0.8, 3, "Homem jovem < 40 anos (1,0 + 1,0 pt): maior incidência epidemiológica."),
                _opt("opt_rip_dem_for", "Masculino < 40 anos + Estrangeiro/Residente temporário (+3,0 pts)", 3.0, False, 1.0, 4, "Inclui fator adicional de apresentação tardia (+1,0 pt do RIPASA original)."),
            ]),
            _grp("grp_rip_pain_duration", "2. Dor em Fossa Ilíaca Direita e Duração dos Sintomas", "dor-fid-duracao-ripasa", "axis_rip_demo", 2, "Dor espontânea em FID (+0,5) associada à duração do quadro (< 48h = +1,0 pt; > 48h = +0,5 pt).", [
                _opt("opt_rip_dur_0", "Sem dor espontânea localizada em FID (0 pts)", 0.0, True, 0.0, 1, "Dor difusa sem localização espontânea em quadrante inferior direito."),
                _opt("opt_rip_dur_late", "Dor em FID com duração > 48 horas (+1,0 pt)", 1.0, False, 0.5, 2, "Dor em FID (+0,5) + evolução prolongada > 48h (+0,5)."),
                _opt("opt_rip_dur_early", "Dor em FID com evolução aguda < 48 horas (+1,5 pts)", 1.5, False, 1.0, 3, "Dor em FID (+0,5) + evolução clássica aguda < 48h (+1,0)."),
            ]),
            _grp("grp_rip_visceral", "3. Migração da Dor, Anorexia e Náuseas/Vômitos", "sintomas-viscerais-ripasa", "axis_rip_symp", 3, "Soma dos sintomas viscerais: Migração para FID (+0,5), Anorexia (+1,0) e Náuseas/Vômitos (+1,0).", [
                _opt("opt_rip_vis_0", "Nenhum sintoma visceral associado (0 pts)", 0.0, True, 0.0, 1, "Sem migração, anorexia ou náuseas."),
                _opt("opt_rip_vis_05", "Apenas migração da dor para FID (+0,5 pt)", 0.5, False, 0.25, 2, "Migração periumbilical isolada sem anorexia/vômitos."),
                _opt("opt_rip_vis_1", "Anorexia OU Náuseas/Vômitos isolados (+1,0 pt)", 1.0, False, 0.45, 3, "Um sintoma digestivo maior presente."),
                _opt("opt_rip_vis_15", "Migração da dor + Anorexia (ou Náuseas) (+1,5 pts)", 1.5, False, 0.65, 4, "Migração + um sintoma digestivo."),
                _opt("opt_rip_vis_2", "Anorexia + Náuseas/Vômitos sem migração (+2,0 pts)", 2.0, False, 0.85, 5, "Ambos os sintomas digestivos presentes."),
                _opt("opt_rip_vis_25", "Tríade completa: Migração + Anorexia + Náuseas/Vômitos (+2,5 pts)", 2.5, False, 1.0, 6, "Todos os 3 sintomas viscerais clássicos presentes."),
            ]),
            _grp("grp_rip_tenderness", "4. Dor à Palpação em FID e Defesa Muscular (Guarding)", "defesa-muscular-ripasa", "axis_rip_signs", 4, "Sensibilidade dolorosa em FID (+1,0) e defesa muscular voluntária/involuntária (+2,0).", [
                _opt("opt_rip_ten_0", "Abdome flácido e indolor em FID (0 pts)", 0.0, True, 0.0, 1, "Palpação superficial e profunda indolor."),
                _opt("opt_rip_ten_1", "Dor à palpação de FID sem defesa muscular (+1,0 pt)", 1.0, False, 0.4, 2, "Sensibilidade localizada no ponto de McBurney sem rigidez parietal."),
                _opt("opt_rip_ten_3", "Dor em FID com Defesa Muscular / Rigidez Parietal (+3,0 pts)", 3.0, False, 1.0, 3, "Sensibilidade em FID (+1,0) + Defesa muscular parietal (+2,0)."),
            ]),
            _grp("grp_rip_peritoneal", "5. Sinais de Blumberg (Descompressão) e Rovsing", "blumberg-rovsing-ripasa", "axis_rip_signs", 5, "Blumberg positivo (+1,0 pt) e Sinal de Rovsing — dor em FID à compressão de FIE (+2,0 pts).", [
                _opt("opt_rip_per_0", "Blumberg e Rovsing negativos (0 pts)", 0.0, True, 0.0, 1, "Sem descompressão dolorosa ou dor contralateral referida."),
                _opt("opt_rip_per_1", "Apenas Sinal de Blumberg positivo (+1,0 pt)", 1.0, False, 0.45, 2, "Descompressão brusca dolorosa em FID."),
                _opt("opt_rip_per_2", "Apenas Sinal de Rovsing positivo (+2,0 pts)", 2.0, False, 0.75, 3, "Palpação profunda em FIE desperta dor em FID por deslocamento gasoso colônico."),
                _opt("opt_rip_per_3", "Sinais de Blumberg E Rovsing positivos (+3,0 pts)", 3.0, False, 1.0, 4, "Francos sinais de peritonite localizada em quadrante inferior direito."),
            ]),
            _grp("grp_rip_fever", "6. Febre (Temperatura > 37,0 °C e < 39,0 °C)", "febre-ripasa", "axis_rip_signs", 6, "Elevação térmica característica da apendicite aguda.", [
                _opt("opt_rip_fev_0", "Afebril (<= 37,0 °C) (0 pts)", 0.0, True, 0.0, 1, "Temperatura corporal normal."),
                _opt("opt_rip_fev_1", "Estado subfebril/febril (> 37,0 °C) (+1,0 pt)", 1.0, False, 1.0, 2, "Febre documentada na admissão (+1,0 pt)."),
            ]),
            _grp("grp_rip_wbc", "7. Leucocitose no Hemograma (> 10.000/mm³)", "leucocitose-ripasa", "axis_rip_lab", 7, "Contagem leucocitária elevada na admissão.", [
                _opt("opt_rip_wbc_0", "Leucócitos normais (<= 10.000/mm³) (0 pts)", 0.0, True, 0.0, 1, "Ausência de leucocitose."),
                _opt("opt_rip_wbc_1", "Leucocitose (> 10.000/mm³) (+1,0 pt)", 1.0, False, 1.0, 2, "Leucocitose laboratorial confirmada (+1,0 pt)."),
            ]),
            _grp("grp_rip_urinalysis", "8. Exame Simples de Urina (EAS / Urina Tipo I Negativo)", "eas-negativo-ripasa", "axis_rip_lab", 8, "Ausência de leucocitúria, hematúria ou nitrito afasta ITU/nefrolitíase e pontua a favor de apendicite.", [
                _opt("opt_rip_uri_pos", "EAS alterado (leucocitúria/hematúria/bacteriúria) (0 pts)", 0.0, True, 0.0, 1, "Sugere diagnóstico diferencial urológico (ITU ou ureterolitíase direita)."),
                _opt("opt_rip_uri_neg", "EAS estritamente normal / negativo (+1,0 pt)", 1.0, False, 1.0, 2, "Afasta causa urinária para a dor em FID (+1,0 pt)."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_rip_unlikely", "Apendicite Improvável (< 5,0 pontos)", "low", 0, 4.5, "Probabilidade muito baixa de apendicite aguda (VPN > 97%).", "#10b981", [
                _rx("rx_rip_low", "Sintomáticos e Analgesia Simples", "Dipirona 1 g VO/IV 6/6h se dor", "VO / IV", "6/6h"),
            ], [
                _nonrx("nrx_rip_low", "Observação Breve e Alta Orientada", "Alta Orientada", "Se dor resolvida e exame físico inocente, alta com retorno imediato se sinais de alarme."),
            ]),
            _tier("tier_rip_lowmod", "Baixa a Moderada Probabilidade (5,0 a 7,0 pontos)", "intermediate", 5.0, 7.0, "Zona diagnóstica intermediária. Indicação formal de ultrassonografia abdominal ou TC.", "#f59e0b", [
                _rx("rx_rip_mod", "Hidratação Venosa e Antiemético", "Ringer Lactato 1.000 mL IV + Ondansetrona 4 mg IV 8/8h", "IV", "Contínua"),
            ], [
                _nonrx("nrx_rip_mod", "Ultrassonografia de Abdome / FID e Reavaliação Seriada", "Observação Hospitalar", "Realizar USG de abdome e repetir exame físico em 6-12h; solicitar parecer cirúrgico se imagem positiva."),
            ]),
            _tier("tier_rip_high", "Alta Probabilidade de Apendicite (7,5 a 11,5 pontos)", "high", 7.5, 11.5, "Sensibilidade de 98% para apendicite aguda confirmada. Indicação de avaliação cirúrgica imediata.", "#f97316", [
                _rx("rx_rip_high", "Antibioticoprofilaxia Cirúrgica", "Cefoxitina 2 g IV (ou Ceftriaxona 2 g IV + Metronidazol 500 mg IV)", "IV", "Dose pré-incisão"),
            ], [
                _nonrx("nrx_rip_high", "Parecer da Cirurgia Geral e Preparo para Apendicectomia", "Centro Cirúrgico / Enfermaria Cirúrgica", "Manter em jejum (NPO), hidratação venosa e encaminhar para apendicectomia videolaparoscópica (em mulheres jovens, confirmar com USG rápido).", "Apendicectomia videolaparoscópica."),
            ]),
            _tier("tier_rip_definite", "Apendicite Aguda Definida (>= 12,0 pontos)", "critical", 12.0, 16.5, "Valor preditivo positivo > 95% para apendicite aguda, frequentemente com gangrena ou peritonite localizada.", "#ef4444", [
                _rx("rx_rip_crit", "Antibioticoterapia de Amplo Espectro para Abdome Agudo", "Ceftriaxona 2 g IV 24/24h + Metronidazol 500 mg IV 8/8h (ou Piperacilina-Tazobactam 4,5 g IV 6/6h se peritonite difusa)", "IV", "Imediato"),
            ], [
                _nonrx("nrx_rip_crit", "Apendicectomia de Emergência Sem Atraso", "Centro Cirúrgico", "Abordagem cirúrgica imediata sem atraso por exames redundantes em homens típicos; monitorização hemodinâmica.", "Apendicectomia videolaparoscópica de urgência."),
            ]),
        ],
    }


def get_tokyo_tg18() -> dict:
    return {
        "id": "calc_tokyo_tg18",
        "slug": "criterios-tokyo-tg18-colecistite-colangite",
        "name": "Critérios de Tokyo (TG18) — Colecistite e Colangite Aguda",
        "acronym": "Tokyo TG18",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Infecções Biliares e Cirurgia Hepatobiliar",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Abdome Agudo e Vias Biliares",
        "description": "Diretrizes internacionais de Tokyo (TG18) para diagnóstico definitivo e estadiamento de gravidade (Graus I Leve, II Moderada e III Grave com disfunção orgânica) da colecistite aguda e colangite aguda, definindo o momento ótimo entre colecistectomia videolaparoscópica precoce versus drenagem biliar percutânea/CPRE de urgência.",
        "summary": "Diagnóstico e estadiamento TG18 (Graus I, II e III) de colecistite e colangite aguda com conduta cirúrgica/CPRE.",
        "clinicalObjective": "Confirmar o diagnóstico pelos critérios A+B+C e classificar a gravidade em Grau I, II ou III para guiar antibioticoterapia biliar, colecistectomia precoce ou drenagem biliar de urgência.",
        "targetPopulation": "Pacientes adultos com dor em hipocôndrio direito (Sinal de Murphy), febre, icterícia (Tríade de Charcot / Pêntade de Reynolds) ou suspeita de sepse biliar.",
        "calculationType": "additive_points",
        "formulaExpression": "Critério A (Local) + Critério B (Sistêmico) + Critério C (Imagem) + Marcadores Grau II + Disfunção Orgânica Grau III",
        "evidenceSource": "Yokoe M, Hata J, Takada T, et al. Tokyo Guidelines 2018: diagnostic criteria and severity grading of acute cholecystitis (with videos). J Hepatobiliary Pancreat Sci. 2018;25(1):41-54.",
        "minPossibleScore": 0,
        "maxPossibleScore": 15,
        "baseScore": 0,
        "badge": "cirurgia",
        "clinicalWarning": "Na Colecistite ou Colangite TG18 Grau III (com disfunção orgânica cardiovascular, neurológica, respiratória, renal, hepática ou hematológica), a drenagem biliar de urgência (CPRE na colangite ou colecistostomia percutânea trans-hepática na colecistite proibitiva) salva vidas e precede a cirurgia definitiva.",
        "radarAxes": [
            _axis("axis_tg18_diag", "Tríade Diagnóstica (A+B+C)", "Hepatobiliar"),
            _axis("axis_tg18_local", "Inflamação Local Grave (Grau II)", "Cirúrgico"),
            _axis("axis_tg18_organ", "Disfunção Orgânica (Grau III)", "Sistêmico"),
        ],
        "parameterGroups": [
            _grp("grp_tg18_crit_a", "1. Critério A — Sinais Locais de Inflamação Biliar", "sinais-locais-tg18", "axis_tg18_diag", 1, "Sinal de Murphy positivo ou dor/massa/defesa em hipocôndrio direito (HCD).", [
                _opt("opt_tg18_a_0", "Ausente (HCD indolor, Murphy negativo) (0 pts)", 0, True, 0.0, 1, "Sem sinais flogísticos em hipocôndrio direito."),
                _opt("opt_tg18_a_1", "Dor ou defesa em HCD / Sinal de Murphy positivo (+1 pt)", 1, False, 0.7, 2, "Interrupção inspiratória brusca à palpação do ponto cístico (Murphy) ou dor em HCD."),
            ]),
            _grp("grp_tg18_crit_b", "2. Critério B — Sinais Sistêmicos de Inflamação / Colestase", "sinais-sistemicos-tg18", "axis_tg18_diag", 2, "Febre > 38 °C, PCR elevada (>= 3 mg/dL), leucocitose (> 10.000) ou icterícia/colestase (na colangite).", [
                _opt("opt_tg18_b_0", "Ausente (afebril, leucócitos e PCR normais) (0 pts)", 0, True, 0.0, 1, "Sem resposta inflamatória sistêmica."),
                _opt("opt_tg18_b_1", "Febre > 38 °C, PCR elevada ou Leucocitose (+1 pt)", 1, False, 0.7, 2, "Confirma resposta inflamatória sistêmica (Critério B positivo)."),
            ]),
            _grp("grp_tg18_crit_c", "3. Critério C — Achados de Imagem (USG / TC / Colangio-RM)", "imagem-biliar-tg18", "axis_tg18_diag", 3, "Espessamento parietal vesicular >= 4 mm, distensão vesicular, cálculo impactado no infundíbulo, líquido pericolecístico, Murphy ultrassonográfico ou dilatação de colédoco.", [
                _opt("opt_tg18_c_0", "Imagem biliar normal sem litíase complicada (0 pts)", 0, True, 0.0, 1, "Vesícula biliar de paredes finas e vias biliares de calibre normal."),
                _opt("opt_tg18_c_2", "Imagem típica de colecistite aguda ou dilatação biliar/coledocolitíase (+2 pts)", 2, False, 1.0, 2, "Confirma diagnóstico definitivo TG18 quando somado aos Critérios A e B."),
            ]),
            _grp("grp_tg18_grade2", "4. Critérios de Gravidade Moderada (TG18 Grau II)", "gravidade-moderada-tg18", "axis_tg18_local", 4, "Leucocitose > 18.000/mm³, massa dolorosa palpável em HCD, duração dos sintomas > 72 horas ou inflamação local acentuada (colecistite gangrenosa, enfisematosa, abscesso pericolecístico ou peritonite biliar).", [
                _opt("opt_tg18_g2_0", "Nenhum critério de Grau II presente (0 pts)", 0, True, 0.0, 1, "Quadro restrito a inflamação vesicular não complicada (Grau I se A+B+C presentes)."),
                _opt("opt_tg18_g2_3", "1 ou mais critérios presentes (Leucócitos > 18.000, > 72h, massa em HCD ou necrose local) (+3 pts)", 3, False, 1.0, 2, "Classifica como TG18 Grau II (Moderada) na ausência de disfunção orgânica."),
            ]),
            _grp("grp_tg18_grade3", "5. Critérios de Gravidade Severa / Disfunção Orgânica (TG18 Grau III)", "disfuncao-organica-tg18", "axis_tg18_organ", 5, "Hipotensão exigindo Noradrenalina/dopamina, alteração de consciência (Glasgow < 15), PaO2/FiO2 < 300, oligúria ou Creatinina > 2,0 mg/dL, INR > 1,5 (colangite) ou Plaquetas < 100.000/mm³.", [
                _opt("opt_tg18_g3_0", "Sem disfunção orgânica aguda (0 pts)", 0, True, 0.0, 1, "Funções orgânicas preservadas."),
                _opt("opt_tg18_g3_8", "Presença de >= 1 Disfunção Orgânica Aguda (Choque, Renal, SNC, PaO2/FiO2 < 300, Plaquetas < 100k) (+8 pts)", 8, False, 1.0, 2, "Classifica imediatamente como TG18 Grau III (Grave / Sepse Biliar)."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_tg18_susp", "Suspeita Incompleta / Sem Critérios Definitivos (0 a 2 pontos)", "low", 0, 2, "Critérios diagnósticos TG18 incompletos. Investigar diagnósticos diferenciais de dor em HCD.", "#64748b", [
                _rx("rx_tg18_0", "Analgesia e Antiespasmódico", "Dipirona 1 g IV + Escopolamina 20 mg IV; evitar morfina isolada se suspeita de cólica biliar simples", "IV", "Se dor"),
            ], [
                _nonrx("nrx_tg18_0", "Completar Investigação Hepatobiliar", "Observação / Pronto-Socorro", "Solicitar perfil hepatobiliar completo (Bilirrubinas, FA, GGT, TGO, TGP, Amilase, Lipase) e USG de abdome superior."),
            ]),
            _tier("tier_tg18_g1", "TG18 Grau I — Colecistite / Colangite Aguda Leve (3 a 4 pontos)", "low", 3, 4, "Diagnóstico confirmado sem critérios de Grau II ou disfunção orgânica. Mortalidade < 1%.", "#10b981", [
                _rx("rx_tg18_g1", "Antibioticoterapia Biliar de 1ª Linha (Grau I)", "Ceftriaxona 2 g IV 24/24h (ou Cefazolina 2 g IV 8/8h na colecistite leve comunitária sem colangite)", "IV", "24/24h", "Suspender antibiótico em até 24h após colecistectomia se infecção restrita à parede vesicular."),
            ], [
                _nonrx("nrx_tg18_g1", "Colecistectomia Videolaparoscópica Precoce (Padrão Ouro)", "Centro Cirúrgico / Enfermaria Cirúrgica", "Indicada colecistectomia videolaparoscópica precoce na mesma internação (idealmente nas primeiras 24-72h do início dos sintomas).", "Colecistectomia videolaparoscópica precoce."),
            ]),
            _tier("tier_tg18_g2", "TG18 Grau II — Colecistite / Colangite Aguda Moderada (5 a 7 pontos)", "high", 5, 7, "Inflamação local grave (> 72h, leucócitos > 18.000 ou plastrão/gangrena). Risco elevado de conversão cirúrgica ou lesão de via biliar.", "#f59e0b", [
                _rx("rx_tg18_g2", "Antibioticoterapia para Infecção Intra-Abdominal Moderada", "Ceftriaxona 2 g IV 24/24h + Metronidazol 500 mg IV 8/8h (ou Piperacilina-Tazobactam 4,5 g IV 6/6h)", "IV", "Regrada", "Manter por 4 a 7 dias após controle do foco infeccioso."),
            ], [
                _nonrx("nrx_tg18_g2", "Centro Laparoscópico Avançado ou Drenagem Biliar Precoce", "Enfermaria Cirúrgica / Centro Cirúrgico", "Se paciente apto (Charlson <= 5, ASA <= II) e equipe experiente: colecistectomia laparoscópica urgente. Se inflamação proibitiva ou colangite Grau II: drenagem biliar precoce (CPRE ou colecistostomia percutânea) em < 24h.", "Colecistectomia laparoscópica especializada ou CPRE/Colecistostomia."),
            ]),
            _tier("tier_tg18_g3", "TG18 Grau III — Grave com Disfunção Orgânica / Sepse Biliar (>= 8 pontos)", "critical", 8, 15, "Sepse de foco biliar com falência orgânica aguda. Mortalidade elevada (10-30%) se não descomprimida imediatamente.", "#ef4444", [
                _rx("rx_tg18_g3_abx", "Antibioticoterapia de Amplo Espectro Anti-Pseudomonas/Enterococo", "Piperacilina-Tazobactam 4,5 g IV 6/6h OU Meropenem 1 g IV 8/8h (associar Vancomicina se risco de Enterococcus resistente)", "IV", "Primeira hora (Pacote de Sepse)"),
                _rx("rx_tg18_g3_dva", "Suporte Vasopressor com Noradrenalina em BIC", "Noradrenalina 0,05 a 0,5 mcg/kg/min IV contínua para PAM >= 65 mmHg", "IV Central", "Contínua em BIC", "4 ampolas (16 mg) em 234 mL de SG 5% (64 mcg/mL).", None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_tg18_g3", "Drenagem Biliar de Urgência (CPRE ou Colecistostomia Percutânea) + UTI", "UTI", "Ressuscitação hemodinâmica imediata + Drenagem biliar urgente (CPRE com papilotomia/prótese na colangite grave; Colecistostomia percutânea trans-hepática guiada por USG na colecistite Grau III com alto risco cirúrgico). Postergar colecistectomia eletiva para 6 semanas após resolução.", "CPRE de emergência ou Colecistostomia Percutânea.", "Suporte ventilatório se PaO2/FiO2 < 300.", "Acesso venoso central e PAM invasiva.", "Hemoculturas (2 pares), cultura da bile drenada, lactato, gasometria, coagulograma."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_rts() -> dict:
    return {
        "id": "calc_rts",
        "slug": "revised-trauma-score-rts",
        "name": "RTS — Revised Trauma Score no Politrauma",
        "acronym": "RTS",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Trauma e Atendimento Inicial ao Politraumatizado",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Trauma e Ressuscitação Volêmica",
        "description": "Escore fisiológico de triagem e prognóstico no politrauma (0 a 12 pontos na versão de triagem T-RTS; 0 a 7,8408 na versão ponderada para o TRISS), integrando Escala de Coma de Glasgow (ECG), Pressão Arterial Sistólica (PAS) e Frequência Respiratória (FR).",
        "summary": "Escore fisiológico de gravidade no politrauma baseado em Glasgow, PAS e Frequência Respiratória (0-12 pts).",
        "clinicalObjective": "Identificar rapidamente no pré-hospitalar e na sala vermelha o politraumatizado grave (RTS <= 11) que requer transferência imediata para Centro de Trauma Nível 1 e acionamento do protocolo de trauma.",
        "targetPopulation": "Pacientes vítimas de trauma contuso ou penetrante no atendimento pré-hospitalar (SAMU/Resgate) ou admissão na Sala de Trauma.",
        "calculationType": "additive_points",
        "formulaExpression": "T-RTS = Código_GCS (0-4) + Código_PAS (0-4) + Código_FR (0-4) [RTS Ponderado = 0,9368*GCS + 0,7326*PAS + 0,2908*FR]",
        "evidenceSource": "Champion HR, Sacco WJ, Copes WS, et al. A revision of the Trauma Score. J Trauma. 1989;29(5):623-629. ATLS 10th Edition.",
        "minPossibleScore": 0,
        "maxPossibleScore": 12,
        "baseScore": 0,
        "badge": "trauma",
        "clinicalWarning": "Qualquer redução de 1 ponto no RTS de triagem (T-RTS <= 11) ou presença de código < 4 em qualquer parâmetro indica encaminhamento mandatório para Centro de Trauma de Alta Complexidade.",
        "radarAxes": [
            _axis("axis_rts_gcs", "Nível de Consciência (GCS)", "Neurológico"),
            _axis("axis_rts_sbp", "Perfusão Hemodinâmica (PAS)", "Cardiovascular"),
            _axis("axis_rts_rr", "Ventilação Espontânea (FR)", "Respiratório"),
        ],
        "parameterGroups": [
            _grp("grp_rts_gcs", "1. Escala de Coma de Glasgow (GCS)", "glasgow-rts", "axis_rts_gcs", 1, "Peso multiplicador no RTS ponderado = 0,9368 (maior impacto na sobrevida do trauma).", [
                _opt("opt_rts_gcs_4", "GCS 13 a 15 — TCE Leve / Alerta (Código 4)", 4, True, 0.0, 1, "Valor ponderado = 4 x 0,9368 = 3,7472."),
                _opt("opt_rts_gcs_3", "GCS 9 a 12 — TCE Moderado (Código 3)", 3, False, 0.35, 2, "Valor ponderado = 3 x 0,9368 = 2,8104."),
                _opt("opt_rts_gcs_2", "GCS 6 a 8 — TCE Grave / Coma (Código 2)", 2, False, 0.7, 3, "Valor ponderado = 2 x 0,9368 = 1,8736. Indicação de via aérea definitiva (IOT)."),
                _opt("opt_rts_gcs_1", "GCS 4 a 5 — Coma Profundo (Código 1)", 1, False, 0.9, 4, "Valor ponderado = 1 x 0,9368 = 0,9368."),
                _opt("opt_rts_gcs_0", "GCS 3 — Arreativo (Código 0)", 0, False, 1.0, 5, "Valor ponderado = 0."),
            ]),
            _grp("grp_rts_sbp", "2. Pressão Arterial Sistólica (PAS em mmHg)", "pas-rts", "axis_rts_sbp", 2, "Peso multiplicador no RTS ponderado = 0,7326.", [
                _opt("opt_rts_sbp_4", "PAS > 89 mmHg (Código 4)", 4, True, 0.0, 1, "Valor ponderado = 4 x 0,7326 = 2,9304."),
                _opt("opt_rts_sbp_3", "PAS 76 a 89 mmHg — Hipotensão Limítrofe (Código 3)", 3, False, 0.4, 2, "Valor ponderado = 3 x 0,7326 = 2,1978. Choque hemorrágico Classe III."),
                _opt("opt_rts_sbp_2", "PAS 50 a 75 mmHg — Choque Grave (Código 2)", 2, False, 0.75, 3, "Valor ponderado = 2 x 0,7326 = 1,4652. Acionar Protocolo de Transfusão Maciça."),
                _opt("opt_rts_sbp_1", "PAS 1 a 49 mmHg — Choque Pré-PCR (Código 1)", 1, False, 0.95, 4, "Valor ponderado = 1 x 0,7326 = 0,7326."),
                _opt("opt_rts_sbp_0", "PAS 0 mmHg / Pulso inaudível (Código 0)", 0, False, 1.0, 5, "Parada cardiorrespiratória traumática."),
            ]),
            _grp("grp_rts_rr", "3. Frequência Respiratória (FR em irpm)", "fr-rts", "axis_rts_rr", 3, "Peso multiplicador no RTS ponderado = 0,2908.", [
                _opt("opt_rts_rr_4", "FR 10 a 29 irpm — Eupneia / Fisiológica (Código 4)", 4, True, 0.0, 1, "Valor ponderado = 4 x 0,2908 = 1,1632."),
                _opt("opt_rts_rr_3", "FR > 29 irpm — Taquipneia Severa (Código 3)", 3, False, 0.4, 2, "Valor ponderado = 3 x 0,2908 = 0,8724. Investigar pneumotórax/hemotórax ou acidose."),
                _opt("opt_rts_rr_2", "FR 6 a 9 irpm — Bradipneia Crítica (Código 2)", 2, False, 0.75, 3, "Valor ponderado = 2 x 0,2908 = 0,5816. Hipoventilação iminente."),
                _opt("opt_rts_rr_1", "FR 1 a 5 irpm — Gasping / Respiração Agônica (Código 1)", 1, False, 0.95, 4, "Valor ponderado = 1 x 0,2908 = 0,2908."),
                _opt("opt_rts_rr_0", "FR 0 irpm — Apneia (Código 0)", 0, False, 1.0, 5, "Parada respiratória — intubação imediata."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_rts_crit", "RTS 0 a 8 — Politrauma Crítico / Choque ou Coma Traumático (0 a 8 pontos)", "critical", 0, 8, "Mortalidade elevada (> 50-85%). Reanimação de controle de danos imediata.", "#ef4444", [
                _rx("rx_rts_crit_iot", "Sequência Rápida de Intubação (SRI) com Estabilização Cervical", "Cetamina 1,5 mg/kg IV ou Etomidato 0,3 mg/kg IV + Rocurônio 1,2 mg/kg IV (ou Succinilcolina 1,5 mg/kg)", "IV", "Bolus de indução"),
                _rx("rx_rts_crit_ptm", "Protocolo de Transfusão Maciça (1:1:1) + Ácido Tranexâmico", "CH : PFC : Plaquetas na proporção 1:1:1 + Ácido Tranexâmico 1 g IV em 10 min + Gluconato de Cálcio 10% 10-20 mL IV", "IV", "Imediato"),
            ], [
                _nonrx("nrx_rts_crit", "Cirurgia de Controle de Danos (Damage Control) e Via Aérea Definitiva", "Centro Cirúrgico de Emergência / UTI", "Intubação orotraqueal imediata se GCS <= 8, descompressão torácica se pneumotórax hipertensivo, laparotomia/toracotomia de controle de danos e prevenção da tríade letal (hipotermia, acidose, coagulopatia).", "Laparotomia / Toracotomia de Controle de Danos ou Craniectomia Descompressiva.", "Ventilação mecânica protetora (normocapnia PaCO2 35-40 mmHg no TCE).", "2 acessos 14G ou introdutor venoso central de alto fluxo (Sheath).", "Gasometria arterial, lactato, tromboelastograma (ROTEM/TEG), fibrinogênio, cálcio iônico."),
            ]),
            _tier("tier_rts_mod", "RTS 9 a 11 — Politrauma Potencialmente Grave (9 a 11 pontos)", "high", 9, 11, "Probabilidade de sobrevida de 60% a 90%. Indicação formal de transferência para Centro de Trauma.", "#f59e0b", [
                _rx("rx_rts_mod_txa", "Ácido Tranexâmico (Estudo CRASH-2 / CRASH-3)", "Ácido Tranexâmico 1 g IV em 10 min (dentro de 3h do trauma) + 1 g IV infundido em 8 horas", "IV", "Dose de ataque + manutenção em 8h", "Diluir 1 g (4 ampolas de 250 mg) em 100 mL de SF 0,9%."),
                _rx("rx_rts_mod_vol", "Ressuscitação Hemostática Balanceada", "Ringer Lactato aquecido 500-1.000 mL IV + Concentrado de Hemácias se choque hemorrágico", "IV", "Guiado por metas"),
            ], [
                _nonrx("nrx_rts_mod", "Ativação da Equipe de Trauma, e-FAST e TC de Corpo Inteiro (Pan-Scan)", "Sala Vermelha / Centro de Trauma", "Dois acessos venosos periféricos calibrosos (14G/16G), e-FAST à beira-leito, tipagem sanguínea e TC multislice se estabilidade hemodinâmica.", "Drenagem torácica se hemopneumotórax; laparotomia se FAST positivo em instável."),
            ]),
            _tier("tier_rts_12", "RTS 12 — Estabilidade Fisiológica Inicial (12 pontos)", "low", 12, 12, "Probabilidade de sobrevida > 97% (RTS ponderado máximo = 7,8408).", "#10b981", [
                _rx("rx_rts_12", "Analgesia e Profilaxia Antitetânica", "Dipirona 1 g IV + Avaliação vacinal antitetânica se ferimento cortocontuso", "IV / IM", "Admissão"),
            ], [
                _nonrx("nrx_rts_12", "Avaliação Primária e Secundária ATLS (XABCDE)", "Sala de Trauma / Observação", "Realizar exame secundário completo e e-FAST se mecanismo cinético de alta energia."),
            ]),
        ],
    }


def _ais_options(prefix: str) -> list[dict]:
    return [
        _opt(f"opt_{prefix}_0", "Sem lesão (AIS 0 — 0 pts)", 0, True, 0.0, 1, "Região anatômica íntegra sem lesão traumática."),
        _opt(f"opt_{prefix}_1", "AIS 1 — Leve (1² = 1 pt)", 1, False, 0.15, 2, "Escoriação superficial, contusão leve ou laceração menor."),
        _opt(f"opt_{prefix}_4", "AIS 2 — Moderada (2² = 4 pts)", 4, False, 0.35, 3, "Fratura simples, laceração parenquimatosa Grau I-II ou pneumotórax pequeno."),
        _opt(f"opt_{prefix}_9", "AIS 3 — Série / Grave sem risco imediato (3² = 9 pts)", 9, False, 0.55, 4, "Fratura exposta/fêmur, hemotórax, contusão pulmonar importante ou lesão visceral Grau III."),
        _opt(f"opt_{prefix}_16", "AIS 4 — Severa com risco de vida (4² = 16 pts)", 16, False, 0.80, 5, "Tórax instável, hematoma intracraniano grande, lesão esplênica/hepática Grau IV."),
        _opt(f"opt_{prefix}_25", "AIS 5 — Crítica com sobrevida incerta (5² = 25 pts)", 25, False, 0.95, 6, "Lesão cerebral difusa grave, ruptura brônquica ou lesão vascular/hepática Grau V."),
        _opt(f"opt_{prefix}_75", "AIS 6 — Lesão Máxima / Incompatível (Atribui ISS = 75 automaticamente)", 75, False, 1.0, 7, "Transecção completa de tronco encefálico ou aorta torácica total: eleva o ISS para 75."),
    ]


def get_iss() -> dict:
    return {
        "id": "calc_iss",
        "slug": "injury-severity-score-iss",
        "name": "ISS — Injury Severity Score (Gravidade Anatômica do Trauma)",
        "acronym": "ISS",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Trauma e Atendimento Inicial ao Politraumatizado",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Trauma e Ressuscitação Volêmica",
        "description": "Padrão-ouro anatômico internacional para quantificação da gravidade do politraumatizado (0 a 75 pontos), calculado pela soma dos quadrados dos maiores escores AIS (Abbreviated Injury Scale, 1 a 5) nas 3 regiões corporais mais gravemente acometidas dentre 6 territórios (Cabeça/Pescoço, Face, Tórax, Abdome/Conteúdo Pélvico, Extremidades/Anel Pélvico e Superfície Externa). Qualquer lesão AIS 6 atribui ISS = 75.",
        "summary": "Soma dos quadrados dos 3 maiores AIS em 6 regiões corporais; ISS > 15 define Politrauma Maior (0-75 pts).",
        "clinicalObjective": "Definir objetivamente Politrauma Maior (ISS > 15), estratificar mortalidade anatômica e alimentar o cálculo de sobrevida do TRISS.",
        "targetPopulation": "Pacientes politraumatizados após avaliação secundária, tomografia de corpo inteiro (Pan-Scan) ou exploração cirúrgica.",
        "calculationType": "additive_points",
        "formulaExpression": "ISS = (AIS_Região1)² + (AIS_Região2)² + (AIS_Região3)² [Se qualquer AIS = 6, ISS = 75]",
        "evidenceSource": "Baker SP, O'Neill B, Haddon W Jr, Long WB. The injury severity score: a method for describing patients with multiple injuries and evaluating emergency care. J Trauma. 1974;14(3):187-196.",
        "minPossibleScore": 0,
        "maxPossibleScore": 75,
        "baseScore": 0,
        "badge": "trauma",
        "clinicalWarning": "Para o cálculo exato do ISS, selecione a pontuação quadrática (AIS²) nas até 3 regiões corporais mais gravemente lesadas (mantenha as demais regiões menos graves em AIS 0). O corte internacional ISS > 15 define o Politraumatizado Grave (Major Trauma).",
        "radarAxes": [
            _axis("axis_iss_neuro", "Cabeça, Pescoço e Face", "Neurológico"),
            _axis("axis_iss_torso", "Tórax e Abdome Visceral", "Toracoabdominal"),
            _axis("axis_iss_ortho", "Pelve, Extremidades e Tegumento", "Musculoesquelético"),
        ],
        "parameterGroups": [
            _grp("grp_iss_head", "1. Cabeça e Pescoço (Crânio, Encéfalo e Coluna Cervical)", "ais-cabeca-pescoco", "axis_iss_neuro", 1, "Pontuação AIS ao quadrado (se entre as 3 regiões mais graves).", _ais_options("iss_hd")),
            _grp("grp_iss_face", "2. Face (Esqueleto Facial, Órbitas e Orelha/Nariz)", "ais-face", "axis_iss_neuro", 2, "Pontuação AIS ao quadrado para o maciço craniofacial.", _ais_options("iss_fc")),
            _grp("grp_iss_chest", "3. Tórax (Caixa Torácica, Pulmões, Coração, Aorta Torácica e Diafragma)", "ais-torax", "axis_iss_torso", 3, "Pontuação AIS ao quadrado para o compartimento torácico.", _ais_options("iss_ch")),
            _grp("grp_iss_abdomen", "4. Abdome e Conteúdo Pélvico Visceral (Fígado, Baço, Rins, Alças e Grandes Vasos)", "ais-abdome", "axis_iss_torso", 4, "Pontuação AIS ao quadrado segundo graduação AAST de vísceras abdominais.", _ais_options("iss_ab")),
            _grp("grp_iss_extremities", "5. Extremidades e Anel Pélvico Ósseo (Fêmur, Bacia, Ossos Longos e Articulações)", "ais-extremidades-pelve", "axis_iss_ortho", 5, "Pontuação AIS ao quadrado para fraturas apendiculares e anel pélvico.", _ais_options("iss_ex")),
            _grp("grp_iss_external", "6. Superfície Externa e Tegumento (Queimaduras, Desluvamento Maior e Hipotermia)", "ais-externa", "axis_iss_ortho", 6, "Pontuação AIS ao quadrado para lesões de partes moles extensas e queimaduras.", _ais_options("iss_sk")),
        ],
        "riskTiers": [
            _tier("tier_iss_minor", "Trauma Leve (ISS 1 a 8 pontos)", "low", 0, 8, "Mortalidade hospitalar < 1%. Baixo risco de falência orgânica pós-traumática.", "#10b981", [
                _rx("rx_iss_low", "Analgesia Regular e Profilaxia Antitetânica", "Dipirona 1 g IV/VO 6/6h + Cetoprofeno 100 mg IV 12/12h (se função renal normal e sem sangramento)", "IV / VO", "Regrada"),
            ], [
                _nonrx("nrx_iss_low", "Tratamento Específico das Lesões e Alta / Observação Curta", "Observação / Alta Orientada", "Sutura de ferimentos, imobilização ortopédica e orientação de sinais de alarme."),
            ]),
            _tier("tier_iss_mod", "Trauma Moderado (ISS 9 a 15 pontos)", "intermediate", 9, 15, "Mortalidade hospitalar de 1% a 3%. Requer internação para tratamento cirúrgico/ortopédico ou observação hospitalar.", "#f59e0b", [
                _rx("rx_iss_mod", "Analgesia Multimodal + Tromboprofilaxia (após hemostasia)", "Dipirona 1 g IV 6/6h + Tramadol 100 mg IV 8/8h + Enoxaparina 40 mg SC 24/24h (iniciar 24h após estabilidade hemostática)", "IV / SC", "Hospitalar"),
            ], [
                _nonrx("nrx_iss_mod", "Internação Hospitalar em Enfermaria Cirúrgica / Ortopédica", "Enfermaria Cirúrgica", "Monitorização clínica e hematimétrica seriada (Hb/Ht a cada 12h se trauma contuso visceral Grau I-II)."),
            ]),
            _tier("tier_iss_severe", "Politrauma Maior / Grave (ISS 16 a 24 pontos)", "high", 16, 24, "Corte clássico de Politrauma Maior (ISS > 15). Mortalidade de 5% a 15%. Alto risco de SIRS pós-traumática.", "#f97316", [
                _rx("rx_iss_sev", "Ácido Tranexâmico + Antibioticoprofilaxia se Fratura Exposta/Lesão Oca", "Ácido Tranexâmico 1 g IV (< 3h) + Cefazolina 2 g IV 8/8h (ou Ceftriaxona + Gentamicina em Gustilo III)", "IV", "Protocolo de Trauma"),
            ], [
                _nonrx("nrx_iss_sev", "Admissão em UTI de Trauma e Ortopedia de Controle de Danos (Early Appropriate Care)", "UTI / Centro Cirúrgico", "Monitorização intensiva, correção de acidose (lactato < 2 mmol/L) antes de osteossíntese definitiva.", "Fixação externa ou definitiva conforme fisiologia."),
            ]),
            _tier("tier_iss_crit", "Politrauma Crítico / Ameaçador à Vida (ISS 25 a 75 pontos)", "critical", 25, 75, "Mortalidade de 25% a > 75% (mortalidade próxima a 90-100% se ISS = 75). Exige Damage Control Resuscitation.", "#ef4444", [
                _rx("rx_iss_crit_ptm", "Ressuscitação Hemostática 1:1:1 + Vasopressor se Choque Neurogênico/Refratário", "Transfusão Maciça 1:1:1 + Ácido Tranexâmico 1 g IV + Noradrenalina se PAM < 65 mmHg após reposição volêmica", "IV Central", "Contínua", None, None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_iss_crit", "Damage Control Surgery (Cirurgia de Controle de Danos) + UTI Neuro/Trauma", "Centro Cirúrgico / UTI", "Controle rápido de hemorragia e contaminação (< 90 min de cirurgia), peritoniostomia à vácuo (Bogotá/VAC), reanimação metabólica na UTI por 24-48h e reabordagem programada.", "Laparotomia/Toracotomia de Controle de Danos e Fixação Externa Pélvica."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_triss() -> dict:
    return {
        "id": "calc_triss",
        "slug": "triss-trauma-injury-severity-score",
        "name": "TRISS — Trauma and Injury Severity Score (Probabilidade de Sobrevida)",
        "acronym": "TRISS",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Trauma e Atendimento Inicial ao Politraumatizado",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Trauma e Ressuscitação Volêmica",
        "description": "Modelo logístico combinado padrão internacional (MTOS — Major Trauma Outcome Study) que integra a reserva fisiológica aguda (RTS), a gravidade anatômica (ISS), o mecanismo de trauma (Contuso vs Penetrante) e a reserva biológica etária (< 55 anos vs >= 55 anos) para estimar a Probabilidade de Sobrevida (Ps) e auditar a qualidade dos Centros de Trauma.",
        "summary": "Predição combinada de sobrevida no trauma integrando Mecanismo, Idade (< 55 vs >= 55), RTS e ISS.",
        "clinicalObjective": "Estimar o índice composto de gravidade fisiológico-anatômico e a probabilidade de sobrevida hospitalar (Ps = 1 / (1 + e^-b)) no politraumatizado.",
        "targetPopulation": "Pacientes adultos admitidos em Centros de Trauma por mecanismo contuso ou penetrante.",
        "calculationType": "additive_points",
        "formulaExpression": "Ps = 1 / (1 + e^-b), onde b = b0 + b1(RTS) + b2(ISS) + b3(Idade >= 55)",
        "evidenceSource": "Boyd CR, Tolson MA, Copes WS. Evaluating trauma care: the TRISS method. Trauma Score and the Injury Severity Score. J Trauma. 1987;27(4):370-378.",
        "minPossibleScore": 0,
        "maxPossibleScore": 20,
        "baseScore": 0,
        "badge": "trauma",
        "clinicalWarning": "No método TRISS, pacientes com Ps >= 50% que evoluem a óbito configuram 'Óbitos Potencialmente Evitáveis' (W-Statistic) em auditoria de qualidade de Centros de Trauma.",
        "radarAxes": [
            _axis("axis_triss_mech", "Mecanismo e Idade", "Epidemiológico"),
            _axis("axis_triss_phys", "Deterioração Fisiológica (RTS)", "Hemodinâmico"),
            _axis("axis_triss_anat", "Carga Lesional Anatômica (ISS)", "Cirúrgico"),
        ],
        "parameterGroups": [
            _grp("grp_triss_mech", "1. Mecanismo Cinético do Trauma (Coeficientes de Regressão MTOS)", "mecanismo-trauma-triss", "axis_triss_mech", 1, "Define a equação logística aplicada (Contuso: b0=-0,4499, b1=0,8085, b2=-0,0835, b3=-1,7430 | Penetrante: b0=-2,5355, b1=0,9934, b2=-0,0651, b3=-1,1360).", [
                _opt("opt_triss_blunt", "Trauma Contuso / Fechado (Colisão automobilística, atropelamento, queda) (0 pts)", 0, True, 0.2, 1, "Aplica coeficientes logísticos de trauma fechado."),
                _opt("opt_triss_pen", "Trauma Penetrante (FAF — Arma de fogo ou FAB — Arma branca) (+2 pts)", 2, False, 0.7, 2, "Maior mortalidade precoce por exsanguinação vascular se RTS reduzido."),
            ]),
            _grp("grp_triss_age", "2. Faixa Etária (Índice de Reserva Fisiológica)", "idade-triss", "axis_triss_mech", 2, "Idade >= 55 anos penaliza o expoente b em -1,7430 no trauma contuso e -1,1360 no penetrante.", [
                _opt("opt_triss_age_0", "Idade < 55 anos (Índice de Idade = 0) (0 pts)", 0, True, 0.0, 1, "Reserva fisiológica cardiorrespiratória preservada."),
                _opt("opt_triss_age_1", "Idade >= 55 anos (Índice de Idade = 1) (+3 pts)", 3, False, 1.0, 2, "Reduz significativamente a probabilidade de sobrevida (Ps) para o mesmo ISS."),
            ]),
            _grp("grp_triss_rts", "3. Estrato Fisiológico na Admissão (RTS Ponderado)", "rts-ponderado-triss", "axis_triss_phys", 3, "Comprometimento de Glasgow, PAS e Frequência Respiratória na sala vermelha.", [
                _opt("opt_triss_rts_norm", "RTS 7,84 (GCS 15, PAS > 89, FR 10-29) — Fisiologia preservada (0 pts)", 0, True, 0.0, 1, "Reserva fisiológica intacta na admissão."),
                _opt("opt_triss_rts_mild", "RTS 6,0 a 7,5 — Disfunção fisiológica leve a moderada (+3 pts)", 3, False, 0.35, 2, "Rebaixamento leve (GCS 9-12) ou hipotensão inicial responsiva."),
                _opt("opt_triss_rts_sev", "RTS 4,0 a 5,9 — Choque Hemorrágico Classe III-IV ou Coma GCS <= 8 (+6 pts)", 6, False, 0.75, 3, "Grave instabilidade hemodinâmica ou neurológica admissional."),
                _opt("opt_triss_rts_crit", "RTS < 4,0 — Politrauma in extremis / Choque refratário e Coma profundo (+9 pts)", 9, False, 1.0, 4, "Colapso cardiorrespiratório ou coma arreativo na admissão."),
            ]),
            _grp("grp_triss_iss", "4. Gravidade Anatômica Global (Faixa do ISS)", "iss-faixa-triss", "axis_triss_anat", 4, "Soma dos quadrados dos 3 maiores AIS (1 a 75 pontos).", [
                _opt("opt_triss_iss_low", "ISS 1 a 15 — Trauma Anatômico Leve a Moderado (0 pts)", 0, True, 0.1, 1, "Sem critério de politrauma anatômico maior."),
                _opt("opt_triss_iss_mod", "ISS 16 a 24 — Politrauma Maior (+2 pts)", 2, False, 0.45, 2, "Lesões multissistêmicas graves (ex.: AIS 3 em duas regiões + AIS 2)."),
                _opt("opt_triss_iss_high", "ISS 25 a 40 — Politrauma Severo (+4 pts)", 4, False, 0.75, 3, "Lesões viscerais/cranianas combinadas AIS 4-5."),
                _opt("opt_triss_iss_max", "ISS 41 a 75 — Lesões Anatômicas Críticas / Limítrofes (+6 pts)", 6, False, 1.0, 4, "Múltiplas lesões AIS 5 ou lesão AIS 6."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_triss_high_ps", "Alta Probabilidade de Sobrevida (Ps > 90% — Escore 0 a 4)", "low", 0, 4, "Probabilidade estimada de sobrevida hospitalar (Ps) entre 90% e 99,5%.", "#10b981", [
                _rx("rx_triss_1", "Analgesia, Tromboprofilaxia e Cuidados Padronizados de Trauma", "Dipirona 1 g IV 6/6h + Enoxaparina 40 mg SC 24/24h (após hemostasia segura)", "IV / SC", "Padrão"),
            ], [
                _nonrx("nrx_triss_1", "Manejo Definitivo Precoce (Early Total Care)", "Enfermaria Cirúrgica / Unidade Semi-Intensiva", "Fisiologia preservada permite fixação definitiva de fraturas e reparo cirúrgico completo em tempo único."),
            ]),
            _tier("tier_triss_mod_ps", "Sobrevida Intermediária / Risco Elevado (Ps 50% a 90% — Escore 5 a 10)", "high", 5, 10, "Probabilidade de sobrevida entre 50% e 89%. Pacientes limítrofes ('Borderline Trauma Patients').", "#f59e0b", [
                _rx("rx_triss_2", "Ácido Tranexâmico + Reposição Hemostática Guiada por ROTEM/TEG", "Ácido Tranexâmico 1 g IV (< 3h) + Concentrado de Fibrinogênio ou Crioprecipitado se Fibrinogênio < 150-200 mg/dL", "IV", "Imediato"),
            ], [
                _nonrx("nrx_triss_2", "Admissão em UTI de Trauma e Reanimação Guiada por Metas", "UTI", "Clareamento do lactato e correção do Base Excess (> -6 mEq/L) antes de procedimentos reconstrutivos prolongados."),
            ]),
            _tier("tier_triss_low_ps", "Baixa Probabilidade de Sobrevida / Crítico (Ps < 50% — Escore 11 a 20)", "critical", 11, 20, "Probabilidade de sobrevida < 50% (caindo para < 15% se escore >= 15). Altíssima letalidade.", "#ef4444", [
                _rx("rx_triss_3", "Protocolo de Transfusão Maciça 1:1:1 + Suporte Vasopressor / Cálcio", "CH:PFC:Plaquetas 1:1:1 + Gluconato de Cálcio 10% 10-20 mL IV + Noradrenalina em BIC se choque refratário", "IV Central", "Contínua", None, None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_triss_3", "Cirurgia de Controle de Danos (Damage Control) e UTI Neuro/Trauma", "Centro Cirúrgico / UTI", "Abreviar tempo cirúrgico (< 60-90 min), controle de hemorragia exsanguinante/REBOA Zona I ou III conforme anatomia e reversão da tríade letal na UTI.", "Damage Control Laparotomy / Craniectomia / Toracotomia de Reanimação."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_parkland_aba() -> dict:
    return {
        "id": "calc_parkland_aba",
        "slug": "parkland-aba-ressuscitacao-grande-queimado",
        "name": "Ressuscitação Volêmica no Grande Queimado — ABA Moderna (2 mL) & Parkland (4 mL)",
        "acronym": "ABA / Parkland",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Queimaduras e Trauma Térmico/Elétrico",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Trauma e Ressuscitação Volêmica",
        "description": "Protocolo normativo de ressuscitação hidroeletrolítica nas primeiras 24 horas do Grande Queimado (> 20% de Superfície Corpórea Queimada de 2º e 3º graus). Segue a diretriz moderna da American Burn Association (ABA / ATLS 10ª Ed.): 2 mL/kg/% SCQ de Ringer Lactato para queimaduras térmicas/químicas em adultos (prevenindo síndrome compartimental abdominal e fluid creep) e Fórmula de Parkland clássica comutável de 4 mL/kg/% SCQ para trauma elétrico de alta voltagem (> 1.000 V) com rabdomiólise/mioglobinúria.",
        "summary": "Cálculo de Ringer Lactato em 24h (50% nas primeiras 8h desde o trauma e 50% nas 16h seguintes): ABA 2 mL/kg/% SCQ (padrão) vs Parkland 4 mL/kg/% SCQ (elétrica).",
        "clinicalObjective": "Determinar a taxa horária inicial de infusão de Ringer Lactato (mL/h nas primeiras 8h contadas a partir da hora exata do acidente e nas 16h subsequentes) e guiar a titulação pelo débito urinário alvo (0,5 a 1,0 mL/kg/h).",
        "targetPopulation": "Adultos com queimaduras de 2º e/ou 3º graus acometendo >= 20% da SCQ (Regra dos Nove de Wallace) ou queimadura elétrica de alta tensão.",
        "calculationType": "additive_points",
        "formulaExpression": "V_24h (mL de Ringer Lactato) = Fator (2 mL ABA ou 4 mL Parkland Elétrico) × Peso (kg) × %SCQ (2º e 3º graus) [50% em 8h do trauma + 50% em 16h]",
        "evidenceSource": "American Burn Association (ABA) Clinical Practice Guidelines on Burn Shock Resuscitation, 2023; ATLS 10th Edition; Baxter CR, Shires T. Physiological response to crystalloid resuscitation of severe burns. Ann N Y Acad Sci. 1968.",
        "minPossibleScore": 0,
        "maxPossibleScore": 16,
        "baseScore": 0,
        "badge": "queimados",
        "clinicalWarning": "DIRETRIZ MANDATÓRIA ABA / ATLS: (1) Queimaduras de 1º grau (eritema solar sem flictenas) NÃO entram no cálculo da %SCQ. (2) Os primeiros 50% do volume devem ser infundidos nas primeiras 8 horas contadas DESDE O MOMENTO DO TRAUMA (e não da chegada ao hospital). (3) Utilizar o padrão ABA 2 mL/kg/% SCQ para queimaduras térmicas para evitar edema pulmonar e síndrome compartimental abdominal, reservando 4 mL/kg/% SCQ para trauma elétrico de alta tensão.",
        "radarAxes": [
            _axis("axis_burn_tbsa", "Extensão da Queimadura (%SCQ)", "Tegumentar"),
            _axis("axis_burn_mech", "Mecanismo (Térmico ABA 2mL vs Elétrico 4mL)", "Fisiopatológico"),
            _axis("axis_burn_airway", "Lesão Inalatória e Peso/Perfusão", "Respiratório"),
        ],
        "parameterGroups": [
            _grp("grp_burn_protocol", "1. Protocolo de Ressuscitação: Padrão ABA (2 mL/kg/% SCQ) vs Parkland Elétrico (4 mL/kg/% SCQ)", "protocolo-aba-vs-parkland", "axis_burn_mech", 1, "Diretriz ABA 2023/ATLS 10ª Ed.: 2 mL/kg/% SCQ de Ringer Lactato como padrão recomendado para queimaduras térmicas; 4 mL/kg/% SCQ comutável para trauma elétrico.", [
                _opt("opt_burn_aba_2ml", "Queimadura Térmica / Química — Padrão ABA Moderno (2 mL × kg × %SCQ de Ringer Lactato) (+1 pt)", 1, True, 0.3, 1, "Recomendação oficial vigente: evita hiper-hidratação ('fluid creep') e síndrome compartimental abdominal. Meta de diurese: 0,5 mL/kg/h."),
                _opt("opt_burn_park_3ml", "Queimadura Pediátrica (< 14 anos / <= 30 kg) — Diretriz ABA Pediátrica (3 mL × kg × %SCQ + manutenção SG 5%) (+2 pts)", 2, False, 0.6, 2, "Crianças exigem 3 mL/kg/%SCQ de Ringer Lactato + manutenção basal com glicose. Meta de diurese: 1,0 mL/kg/h."),
                _opt("opt_burn_park_4ml", "Trauma Elétrico de Alta Voltagem (> 1.000 V) — Parkland Clássico Comutável (4 mL × kg × %SCQ) (+4 pts)", 4, False, 1.0, 3, "Necrose muscular profunda oculta e rabdomiólise maciça: exige 4 mL/kg/%SCQ de Ringer Lactato e meta de diurese de 1,0 a 1,5 mL/kg/h (75-100 mL/h) até clareamento da mioglobinúria."),
            ]),
            _grp("grp_burn_tbsa", "2. Superfície Corpórea Queimada (%SCQ — Apenas 2º e 3º Graus pela Regra dos 9)", "scq-regra-dos-nove", "axis_burn_tbsa", 2, "Regra dos 9 no adulto: Cabeça 9%, Tronco anterior 18%, Tronco posterior 18%, Cada MMSS 9%, Cada MMII 18%, Períneo 1% (Palma da mão do paciente = 1%).", [
                _opt("opt_burn_scq_minor", "SCQ < 20% em adulto (Pequeno/Médio Queimado sem choque térmico) (0 pts)", 0, True, 0.1, 1, "Hidratação oral/venosa de manutenção se sem lesão elétrica ou inalatória."),
                _opt("opt_burn_scq_20_39", "SCQ 20% a 39% — Grande Queimado Moderado (+3 pts)", 3, False, 0.5, 2, "Ex. para 70 kg na ABA (2 mL) com 30% SCQ: 4.200 mL/24h (2.100 mL em 8h = 262 mL/h; 2.100 mL em 16h = 131 mL/h). Em Parkland (4 mL): 8.400 mL/24h."),
                _opt("opt_burn_scq_40_59", "SCQ 40% a 59% — Grande Queimado Extenso (+5 pts)", 5, False, 0.8, 3, "Ex. para 70 kg na ABA (2 mL) com 50% SCQ: 7.000 mL/24h (3.500 mL em 8h = 437 mL/h; 3.500 mL em 16h = 218 mL/h). Alto risco de choque hipovolêmico."),
                _opt("opt_burn_scq_60_plus", "SCQ >= 60% — Grande Queimado Crítico / Maciço (+7 pts)", 7, False, 1.0, 4, "Ex. para 70 kg na ABA (2 mL) com 70% SCQ: 9.800 mL/24h (4.900 mL em 8h = 612 mL/h). Monitorar pressão intra-abdominal e considerar Albumina 5% após 12-24h."),
            ]),
            _grp("grp_burn_weight", "3. Faixa de Peso Corporal Estimado (Referência de Cálculo Volêmico)", "peso-corporal-queimado", "axis_burn_airway", 3, "Peso corporal real/estimado em kg para multiplicação direta e meta de diurese horária (0,5 a 1,0 mL/kg/h).", [
                _opt("opt_burn_wt_60", "Peso 50 a 69 kg (Meta de diurese ABA: 30 a 35 mL/h) (0 pts)", 0, True, 0.2, 1, "Sonda vesical de demora obrigatória para aferição horária rigorosa."),
                _opt("opt_burn_wt_80", "Peso 70 a 89 kg (Meta de diurese ABA: 35 a 45 mL/h) (+1 pt)", 1, False, 0.4, 2, "Ajustar vazão da bomba de infusão em ±20% a cada hora conforme diurese."),
                _opt("opt_burn_wt_100", "Peso >= 90 kg (Meta de diurese ABA: 45 a 60 mL/h) (+2 pts)", 2, False, 0.6, 3, "Em obesos graves, utilizar peso ideal ajustado para evitar síndrome compartimental."),
            ]),
            _grp("grp_burn_inhalation", "4. Lesão Inalatória de Via Aérea ou Queimadura Circunferencial Torácica/Cervical", "lesao-inalatoria-queimado", "axis_burn_airway", 4, "Incêndio em ambiente fechado, escarro carbonáceo, vibrissas nasais queimadas, rouquidão, estridor ou carboxi-hemoglobina > 10%.", [
                _opt("opt_burn_inh_0", "Ausente — Via aérea pérvia sem sinais de inalação de fumaça (0 pts)", 0, True, 0.0, 1, "Manter suplementação de O2 se necessário."),
                _opt("opt_burn_inh_3", "Presente — Suspeita de Lesão Inalatória ou Escara Circunferencial (+3 pts)", 3, False, 1.0, 2, "Aumenta a necessidade real de cristaloides em 30-40% e exige Intubação Orotraqueal Precoce (antes do edema glótico obstrutivo) e O2 a 100%."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_burn_minor", "Pequeno / Médio Queimado (< 20% SCQ Térmica sem Inalação — 0 a 2 pontos)", "low", 0, 2, "Baixo risco de choque do queimado sistêmico. Hidratação basal e controle álgico.", "#10b981", [
                _rx("rx_burn_min", "Hidratação Venosa Basal + Analgesia + Profilaxia Antitetânica", "Ringer Lactato 1.500-2.000 mL/24h + Dipirona 1 g IV 6/6h + Morfina 2-4 mg IV se dor intensa + Vacina dT", "IV", "Manutenção"),
            ], [
                _nonrx("nrx_burn_min", "Curativo Oclusivo com Sulfadiazina de Prata 1% ou Cobertura Biológica", "Observação / Enfermaria Cirúrgica", "Lavagem com SF 0,9% aquecido, debridamento de flictenas rotas e curativo estéril (transferir para Centro de Queimados se acometimento de face, mãos, pés, períneo ou grandes articulações)."),
            ]),
            _tier("tier_burn_aba_std", "Grande Queimado Térmico — Protocolo ABA 2 mL/kg/% SCQ (3 a 7 pontos)", "high", 3, 7, "Choque hipovolêmico distributivo do queimado. Infundir 50% do volume nas primeiras 8h DESDE O TRAUMA e 50% nas 16h seguintes.", "#f59e0b", [
                _rx("rx_burn_aba_rl", "Ringer Lactato Aquecido — Fórmula ABA (2 mL × Peso kg × %SCQ)", "Volume 24h = 2 mL × Peso × %SCQ. Infundir 50% nas primeiras 8h (descontando horas já decorridas desde o acidente) e 50% nas 16h seguintes", "IV (2 acessos calibrosos em pele íntegra ou queimada)", "Contínua em BIC titulada por diurese", "PROIBIDO SF 0,9% em grandes volumes pelo risco de acidose hiperclorêmica severa. Titular vazão horária em ±20% para manter diurese entre 0,5 e 1,0 mL/kg/h."),
                _rx("rx_burn_aba_pain", "Analgesia Venosa Titulada + Profilaxia de Úlcera de Curling", "Morfina 2 a 5 mg IV a cada 2-4h (ou Fentanil contínuo) + Omeprazol 40 mg IV 24/24h", "IV", "Regrada", "PROIBIDO administrar analgésicos por via intramuscular (IM) ou subcutânea (SC) devido à absorção errática no choque e risco de depressão respiratória tardia."),
            ], [
                _nonrx("nrx_burn_aba_care", "Sondagem Vesical de Demora (Diurese Horária 0,5-1,0 mL/kg/h) e Prevenção de Hipotermia", "UTI / Unidade de Tratamento de Queimados (UTQ)", "Passagem obrigatória de sonda vesical de Foley com uromêtro horário, manta térmica, elevação de extremidades queimadas a 30° e avaliação de escarotomia se queimadura circunferencial com redução de pulso Doppler.", "Escarotomia descompressiva longitudinal se síndrome compartimental de extremidade ou restrição torácica."),
            ]),
            _tier("tier_burn_crit_elec", "Grande Queimado Crítico / Trauma Elétrico (Parkland 4 mL/kg/% SCQ) ou Lesão Inalatória (8 a 16 pontos)", "critical", 8, 16, "Altíssima mortalidade por obstrução aguda de via aérea, rabdomiólise maciça (trauma elétrico) ou síndrome compartimental abdominal.", "#ef4444", [
                _rx("rx_burn_crit_park", "Ringer Lactato — Parkland Elétrico (4 mL × Peso kg × %SCQ) ou ABA Titulado", "No Trauma Elétrico: 4 mL × Peso × %SCQ (50% nas primeiras 8h desde o trauma e 50% nas 16h seguintes), ajustado para diurese de 1,0 a 1,5 mL/kg/h (75-100 mL/h) até desaparecimento da mioglobinúria", "IV Central / Calibroso", "Contínua em BIC", "Se queimadura > 50% SCQ ou necessidade de cristaloide exceder 6 mL/kg/%SCQ após 12h ('fluid creep'), associar Albumina Humana 5% (0,5 mL/kg/%SCQ) para reduzir pressão intra-abdominal."),
                _rx("rx_burn_crit_iot", "Intubação Orotraqueal Precoce + Hidroxocobalamina (se intoxicação por Cianeto)", "Intubação com tubo >= 7,5-8,0 mm sem aguardar hipoxemia; se incêndio em local fechado com acidose lática grave (Lactato > 10 mmol/L), administrar Hidroxocobalamina 5 g IV em 15 min", "IV", "Emergência"),
            ], [
                _nonrx("nrx_burn_crit_utq", "Proteção Imediata de Via Aérea, ECG Contínuo (Elétrico) e Escarotomia/Fasciotomia de Urgência", "UTI de Queimados (UTQ) / Sala Vermelha", "Intubação orotraqueal imediata na lesão inalatória; monitorização cardíaca por 24-48h no trauma elétrico (risco de FV/TV); aferição de pressão intra-abdominal (PIA via sonda vesical) a cada 4h; fasciotomia se síndrome compartimental muscular elétrica.", "Intubação Orotraqueal, Escarotomia Torácica/Membros e Fasciotomia.", "Ventilação mecânica com FiO2 100% até COHb < 5%.", "Acesso venoso central guiado por USG.", "CPK total, potássio sérico (a cada 4h no trauma elétrico — risco de hipercalemia letal; PROIBIDO Succinilcolina após 24-48h da queimadura), gasometria com co-oximetria (COHb) e lactato."),
            ]),
        ],
    }


def get_asa() -> dict:
    return {
        "id": "calc_asa",
        "slug": "classificacao-estado-fisico-asa",
        "name": "Classificação do Estado Físico ASA — Risco Anestésico-Cirúrgico",
        "acronym": "ASA",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Avaliação Pré-Operatória e Anestesiologia",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Risco Cirúrgico Pré-Operatório",
        "description": "Sistema universal da American Society of Anesthesiologists (ASA Physical Status Classification System, ASA I a VI com sufixo modificador 'E' para cirurgias de Emergência) para estratificação da reserva fisiológica basal e predição de morbimortalidade perioperatória.",
        "summary": "Classificação clínica pré-anestésica ASA I a VI com modificador de emergência 'E' e conduta perioperatória.",
        "clinicalObjective": "Padronizar a comunicação do estado físico pré-operatório, definir necessidade de exames complementares, monitorização invasiva intraoperatória e reserva de leito de UTI pós-operatório.",
        "targetPopulation": "Todos os pacientes submetidos a procedimentos cirúrgicos ou diagnósticos sob anestesia geral, regional ou sedação.",
        "calculationType": "additive_points",
        "formulaExpression": "Classe Base ASA (1 a 6) + Modificador de Emergência 'E' (+1 pt de gravidade operacional) + Porte Cirúrgico",
        "evidenceSource": "American Society of Anesthesiologists. ASA Physical Status Classification System (Last approved by the ASA House of Delegates on December 13, 2020).",
        "minPossibleScore": 1,
        "maxPossibleScore": 8,
        "baseScore": 0,
        "badge": "anestesia",
        "clinicalWarning": "O sufixo 'E' (Emergência) é adicionado a qualquer classe (ex.: ASA II-E, ASA IV-E) quando o atraso no tratamento cirúrgico implicar aumento significativo de ameaça à vida ou a membro/órgão, duplicando o risco de mortalidade da respectiva classe.",
        "radarAxes": [
            _axis("axis_asa_class", "Estado Físico Sistêmico (ASA I-VI)", "Sistêmico"),
            _axis("axis_asa_emerg", "Urgência / Modificador 'E'", "Cirúrgico"),
            _axis("axis_asa_surg", "Porte e Estresse Cirúrgico", "Hemodinâmico"),
        ],
        "parameterGroups": [
            _grp("grp_asa_status", "1. Classe do Estado Físico Basal (ASA I a ASA VI)", "classe-estado-fisico-asa", "axis_asa_class", 1, "Classificação oficial atualizada da ASA 2020 com exemplos clínicos adultos e obstétricos.", [
                _opt("opt_asa_1", "ASA I — Paciente saudável normal (1 pt)", 1, True, 0.0, 1, "Sem patologias orgânicas, fisiológicas ou psiquiátricas; não tabagista, consumo mínimo/nulo de álcool, IMC < 30 kg/m²."),
                _opt("opt_asa_2", "ASA II — Doença sistêmica leve sem limitação funcional substancial (2 pts)", 2, False, 0.25, 2, "Ex.: HAS ou DM bem controlados, tabagismo ativo, obesidade leve/moderada (IMC 30-39,9), gestação normal, doença pulmonar leve."),
                _opt("opt_asa_3", "ASA III — Doença sistêmica grave com limitação funcional definida (3 pts)", 3, False, 0.55, 3, "Ex.: HAS ou DM mal controlados, DPOC, obesidade mórbida (IMC >= 40), DRC em diálise regular, marca-passo, FE moderadamente reduzida, IAM/AVC/Stent há > 3 meses."),
                _opt("opt_asa_4", "ASA IV — Doença sistêmica grave que representa ameaça constante à vida (4 pts)", 4, False, 0.85, 4, "Ex.: IAM, AVC, AIT ou Stent coronariano há < 3 meses, isquemia miocárdica em curso, disfunção valvar grave, FE severamente reduzida (< 30%), sepse, CIVD, SDRA ou DRC agudizada sem diálise regular."),
                _opt("opt_asa_5", "ASA V — Paciente moribundo sem expectativa de sobrevida sem a operação (5 pts)", 5, False, 1.0, 5, "Ex.: Aneurisma de aorta abdominal roto, politrauma maciço em choque, isquemia mesentérica com falência múltipla de órgãos, hemorragia intracraniana com herniação."),
                _opt("opt_asa_6", "ASA VI — Paciente com morte encefálica declarada para captação de órgãos (6 pts)", 6, False, 1.0, 6, "Doador de órgãos em morte encefálica confirmada sob suporte hemodinâmico em UTI."),
            ]),
            _grp("grp_asa_emergency", "2. Modificador de Emergência ('E')", "modificador-emergencia-asa", "axis_asa_emerg", 2, "Adiciona o sufixo 'E' quando o atraso cirúrgico colocar em risco imediato a vida ou viabilidade de órgão/membro.", [
                _opt("opt_asa_elective", "Cirurgia Eletiva / Programada (Sem sufixo 'E') (0 pts)", 0, True, 0.0, 1, "Tempo hábil para jejum completo (8h sólidos / 2h líquidos claros) e compensação clínica pré-operatória."),
                _opt("opt_asa_emerg_e", "Cirurgia de Emergência — Sufixo 'E' (ASA I-E a V-E) (+1 pt)", 1, False, 1.0, 2, "Estômago cheio (indução em sequência rápida obrigatória) e impossibilidade de adiamento cirúrgico."),
            ]),
            _grp("grp_asa_complexity", "3. Porte Hemodinâmico do Procedimento Cirúrgico", "porte-cirurgico-asa", "axis_asa_surg", 3, "Perda sanguínea estimada e translocação volêmica do procedimento planejado.", [
                _opt("opt_asa_surg_low", "Pequeno / Médio Porte (< 1% de risco cardíaco intrínseco, sem abertura cavitária maior) (0 pts)", 0, True, 0.1, 1, "Cirurgias superficiais, endoscópicas, oftalmológicas, herniorrafia ou colecistectomia laparoscópica simples."),
                _opt("opt_asa_surg_high", "Grande Porte / Alto Risco (> 5% de risco: intraperitoneal maior, intratorácica, vascular suprainguinal/aórtica) (+1 pt)", 1, False, 1.0, 2, "Grandes ressecções oncológicas, cirurgia vascular arterial, esofagectomia, duodenopancreatectomia ou neurocirurgia."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_asa_low", "ASA I a II Eletivo — Baixo Risco Perioperatório (1 a 2 pontos)", "low", 1, 2, "Mortalidade perioperatória < 0,03% (ASA I) a 0,2% (ASA II). Capacidade funcional geralmente >= 4 METs.", "#10b981", [
                _rx("rx_asa_low", "Manejo Medicamentoso Pré-Operatório Padrão", "Manter betabloqueadores e estatinas de uso crônico; suspender IECA/BRA 24h antes se cirurgia com risco de hipotensão; suspender SGLT2 (Empagliflozina/Dapagliflozina) 3 a 4 dias antes da cirurgia", "VO", "Pré-operatório"),
            ], [
                _nonrx("nrx_asa_low", "Monitorização Básica Padrão (Cardioscopia, PNI, SpO2, Capnografia e Temperatura)", "Centro Cirúrgico Ambulatorial / Enfermaria", "Dispensa exames laboratoriais extensos de rotina em ASA I assintomático submetido a cirurgia de pequeno porte."),
            ]),
            _tier("tier_asa_mod", "ASA III ou ASA II-E / Grande Porte — Risco Intermediário a Alto (3 a 4 pontos)", "intermediate", 3, 4, "Mortalidade perioperatória de 1,2% a 3,5%. Requer otimização de comorbidades e monitorização avançada.", "#f59e0b", [
                _rx("rx_asa_mod", "Estabilização Clínica, Controle Glicêmico (140-180 mg/dL) e Profilaxia de NVPO/TEV", "Dexametasona 4-8 mg IV na indução + Ondansetrona 4 mg IV ao final + Cefazolina 2 g IV 30-60 min antes da incisão", "IV", "Intraoperatório"),
            ], [
                _nonrx("nrx_asa_mod", "Avaliação Cardiológica (RCRI), Reserva de Hemocomponentes e UTI conforme Porte", "Unidade Semi-Intensiva / Enfermaria Monitorizada", "Se cirurgia de emergência ('E'), realizar Indução em Sequência Rápida (Rocurônio 1,2 mg/kg ou Succinilcolina) pelo risco de broncoaspiração."),
            ]),
            _tier("tier_asa_crit", "ASA IV, ASA V ou ASA VI — Risco Crítico / Ameaça Imediata à Vida (5 a 8 pontos)", "critical", 5, 8, "Mortalidade perioperatória de 8% a 25% (ASA IV) e 35% a > 70% (ASA V). Exige suporte intensivo avançado.", "#ef4444", [
                _rx("rx_asa_crit", "Suporte Vasopressor Contínuo (Noradrenalina) e Anestesia Balanceada Cardioprotetora", "Noradrenalina em BIC pronta em linha antes da indução anestésica + Etomidato 0,2-0,3 mg/kg ou Cetamina na indução", "IV Central", "Contínua em BIC", None, None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_asa_crit", "Monitorização Hemodinâmica Invasiva (PAI, PVC, Débito Cardíaco) e Leito de UTI Obrigatório", "UTI Cirúrgica", "Punção de pressão arterial invasiva (PAI radial) acordado antes da indução anestésica; acesso venoso central; gasometria e tromboelastometria intraoperatória. Em ASA VI (doador de órgãos), manter metas de manutenção do potencial doador (PAM >= 65 mmHg, diurese 1-3 mL/kg/h, normotermia > 35 °C).", "PAI pré-indução, Acesso Venoso Central e Pós-Operatório em UTI."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_rcri_lee() -> dict:
    return {
        "id": "calc_rcri_lee",
        "slug": "rcri-indice-risco-cardiaco-revisado-lee",
        "name": "RCRI — Índice de Risco Cardíaco Revisado de Lee (Cirurgia Não Cardíaca)",
        "acronym": "RCRI (Lee)",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Avaliação Pré-Operatória e Cardiologia Perioperatória",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Risco Cirúrgico Pré-Operatório",
        "description": "Escore padrão-ouro validado pelas diretrizes SBC, ESC e AHA/ACC (0 a 6 pontos, 6 preditores independentes) para estimativa de Eventos Cardíacos Adversos Maiores (MACE: IAM não fatal, parada cardíaca ressuscitada, edema agudo de pulmão, bloqueio AV total ou óbito cardiovascular em 30 dias) em cirurgias não cardíacas.",
        "summary": "Predição de eventos cardíacos maiores (MACE em 30 dias) em cirurgia não cardíaca com 6 preditores (0-6 pts).",
        "clinicalObjective": "Identificar pacientes de Baixo Risco (0-1 pt, liberados sem testes isquêmicos adicionais se boa capacidade funcional >= 4 METs) versus Risco Elevado (>= 2 pts, candidatos a dosagem de BNP/NT-proBNP, troponina seriada pós-operatória e avaliação funcional).",
        "targetPopulation": "Pacientes com idade >= 45 anos (ou 18-44 anos com doença cardiovascular conhecida) submetidos a cirurgia não cardíaca eletiva ou urgente.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma de 6 variáveis binárias (Cirurgia Alto Risco + DAC + ICC + DCV + DM Insulina + Cr > 2,0 mg/dL) [0 a 6 pts]",
        "evidenceSource": "Lee TH, Marcantonio ER, Mangione CM, et al. Derivation and prospective validation of a simple index for prediction of cardiac risk of major noncardiac surgery. Circulation. 1999;100(10):1043-1049. Diretriz SBC / ESC Perioperatória 2022/2024.",
        "minPossibleScore": 0,
        "maxPossibleScore": 6,
        "baseScore": 0,
        "badge": "pre-operatorio",
        "clinicalWarning": "NUNCA iniciar betabloqueador em altas doses na manhã da cirurgia em paciente virgem de tratamento (aumento de AVC e hipotensão no estudo POISE). Se indicado betabloqueio em alto risco, titular com antecedência mínima de 7 a 30 dias visando FC 60-70 bpm e PAS > 100 mmHg.",
        "radarAxes": [
            _axis("axis_rcri_surg", "Porte Cirúrgico Intrínseco", "Cirúrgico"),
            _axis("axis_rcri_cardio", "Cardiopatia Isquêmica e ICC", "Cardiovascular"),
            _axis("axis_rcri_renomet", "Eixo Neurovascular e Reno-Metabólico", "Sistêmico"),
        ],
        "parameterGroups": [
            _grp("grp_rcri_surg", "1. Cirurgia de Alto Risco Intrínseco (Intraperitoneal, Intratorácica ou Vascular Suprainguinal)", "cirurgia-alto-risco-rcri", "axis_rcri_surg", 1, "Cirurgias abertas de abdome/tórax, aneurisma de aorta ou vascular arterial suprainguinal.", [
                _opt("opt_rcri_surg_0", "Não — Cirurgia de pequeno ou médio porte (0 pts)", 0, True, 0.0, 1, "Procedimento endoscópico, superficial, ortopédico menor ou videolaparoscópico não complexo."),
                _opt("opt_rcri_surg_1", "Sim — Cirurgia intraperitoneal maior, intratorácica ou vascular suprainguinal (+1 pt)", 1, False, 1.0, 2, "Elevado estresse adrenérgico e translocação volêmica intraoperatória."),
            ]),
            _grp("grp_rcri_ihd", "2. História de Cardiopatia Isquêmica (DAC)", "cardiopatia-isquemica-rcri", "axis_rcri_cardio", 2, "História de IAM prévio, teste ergométrico/cintilografia positiva, dor anginosa atual, uso de nitrato ou ondas Q patológicas no ECG.", [
                _opt("opt_rcri_ihd_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem evidência clínica ou eletrocardiográfica de doença arterial coronariana."),
                _opt("opt_rcri_ihd_1", "Presente — IAM prévio, angina, uso de nitrato ou onda Q patológica (+1 pt)", 1, False, 0.85, 2, "Substrato coronariano vulnerável a infarto perioperatório Tipo 1 ou Tipo 2."),
            ]),
            _grp("grp_rcri_chf", "3. História de Insuficiência Cardíaca Congestiva (ICC)", "insuficiencia-cardiaca-rcri", "axis_rcri_cardio", 3, "História de IC clínica, edema agudo de pulmão prévio, dispneia paroxística noturna, B3/estertores bilaterais ou redistribuição vascular na radiografia.", [
                _opt("opt_rcri_chf_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Função ventricular preservada sem histórico de congestão pulmonar."),
                _opt("opt_rcri_chf_1", "Presente — IC compensada ou prévia documentada (+1 pt)", 1, False, 1.0, 2, "Fator de altíssimo impacto na mortalidade pós-operatória."),
            ]),
            _grp("grp_rcri_cvd", "4. História de Doença Cerebrovascular (AVC Isquêmico/Hemorrágico ou AIT)", "doenca-cerebrovascular-rcri", "axis_rcri_renomet", 4, "Antecedente pessoal de Acidente Vascular Cerebral (AVC) ou Ataque Isquêmico Transitório (AIT).", [
                _opt("opt_rcri_cvd_0", "Ausente (0 pts)", 0, True, 0.0, 1, "Sem histórico de eventos neurovasculares."),
                _opt("opt_rcri_cvd_1", "Presente — AVC ou AIT prévio (+1 pt)", 1, False, 0.7, 2, "Marcador de aterosclerose sistêmica difusa e vulnerabilidade cerebral à hipotensão."),
            ]),
            _grp("grp_rcri_insulin", "5. Diabetes Mellitus em Tratamento Pré-Operatório com Insulina", "diabetes-insulina-rcri", "axis_rcri_renomet", 5, "Uso ambulatorial prévio de insulinoterapia (DM1 ou DM2 insulinizado).", [
                _opt("opt_rcri_ins_0", "Não (Não diabético ou apenas antidiabéticos orais) (0 pts)", 0, True, 0.0, 1, "Sem uso pré-operatório crônico de insulina."),
                _opt("opt_rcri_ins_1", "Sim — Diabetes em uso pré-operatório de Insulina (+1 pt)", 1, False, 0.7, 2, "Associa-se a disautonomia cardiovascular e microangiopatia."),
            ]),
            _grp("grp_rcri_creat", "6. Disfunção Renal Pré-Operatória (Creatinina Sérica > 2,0 mg/dL)", "creatinina-maior-2-rcri", "axis_rcri_renomet", 6, "Creatinina sérica basal > 2,0 mg/dL (> 177 micromol/L) ou paciente em programa de diálise.", [
                _opt("opt_rcri_cr_0", "Creatinina sérica <= 2,0 mg/dL (0 pts)", 0, True, 0.0, 1, "Sem disfunção renal avançada pelos critérios de Lee."),
                _opt("opt_rcri_cr_1", "Creatinina sérica > 2,0 mg/dL (+1 pt)", 1, False, 1.0, 2, "Elevado risco de hipervolemia, hipercalemia e MACE perioperatório."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_rcri_1", "RCRI Classe I (0 pontos) — Risco Cardíaco Muito Baixo", "low", 0, 0, "Risco de MACE (IAM, PCR ou óbito cardíaco em 30 dias) = 0,4% (coorte original) a 3,9% (meta-análise moderna com troponina US).", "#10b981", [
                _rx("rx_rcri_1", "Manutenção de Medicações Cardiovasculares Crônicas", "Manter Estatina e AAS (se prevenção secundária com stent prévio, salvo neurocirurgia intracraniana/prostática onde discute-se suspensão de 5-7 dias)", "VO", "Pré-operatório"),
            ], [
                _nonrx("nrx_rcri_1", "Liberação Cirúrgica Direta Sem Testes Isquêmicos Adicionais", "Centro Cirúrgico / Enfermaria", "Prosseguir para cirurgia sem necessidade de cintilografia ou eco de estresse."),
            ]),
            _tier("tier_rcri_2", "RCRI Classe II (1 ponto) — Risco Cardíaco Baixo", "low", 1, 1, "Risco de MACE em 30 dias = 0,9% (coorte original) a 6,0% (com rastreio de MINS por troponina US).", "#22c55e", [
                _rx("rx_rcri_2", "Manter Betabloqueador e Estatina Crônicos", "Se paciente já usa Betabloqueador ou Estatina, manter na manhã da cirurgia com pequeno gole de água; suspender IECA/BRA no dia se risco de hipotensão", "VO", "Manhã da cirurgia"),
            ], [
                _nonrx("nrx_rcri_2", "Avaliar Capacidade Funcional (METs / Questionário DASI)", "Enfermaria Cirúrgica", "Se capacidade funcional >= 4 METs (subir 2 lances de escada sem dispneia/angina), liberar para cirurgia. Se < 4 METs em cirurgia de grande porte, dosar BNP/NT-proBNP basal."),
            ]),
            _tier("tier_rcri_3", "RCRI Classe III (2 pontos) — Risco Cardíaco Moderado / Elevado", "high", 2, 2, "Risco de MACE em 30 dias = 6,6% (coorte original) a 10,1% (meta-análise CCS).", "#f59e0b", [
                _rx("rx_rcri_3", "Estatina de Alta Potência + Vigilância de Injúria Miocárdica (MINS)", "Atorvastatina 40-80 mg VO ou Rosuvastatina 20-40 mg VO + Manter Betabloqueador prévio", "VO", "24/24h"),
            ], [
                _nonrx("nrx_rcri_3", "Dosagem de BNP/NT-proBNP Pré-Operatório e Curva de Troponina Pós-Operatória (48-72h)", "Unidade Semi-Intensiva / Enfermaria com Telemetria", "Solicitar ECG e Troponina de alta sensibilidade no basal, 24h e 48h pós-operatórias para rastrear MINS (Myocardial Injury after Noncardiac Surgery — isquemia silenciosa sob analgesia)."),
            ]),
            _tier("tier_rcri_4", "RCRI Classe IV (>= 3 pontos) — Alto Risco Cardíaco Perioperatório", "critical", 3, 6, "Risco de MACE em 30 dias >= 11,0% a 15,0%. Alta morbimortalidade cardiovascular.", "#ef4444", [
                _rx("rx_rcri_4", "Cardioproteção Estrita (Evitar Taquicardia e Hipotensão PAM < 65 mmHg)", "Manter Hb >= 8-9 g/dL em coronariopatas; manter Betabloqueador/Estatina; corrigir distúrbios de K+ (> 4,0 mEq/L) e Mg2+ (> 2,0 mg/dL)", "IV / VO", "Perioperatório contínuo"),
            ], [
                _nonrx("nrx_rcri_4", "Pós-Operatório em UTI, Ecocardiograma Pré-Operatório e Estratificação Não Invasiva", "UTI Cirúrgica / Unidade Coronariana", "Se cirurgia eletiva e capacidade funcional < 4 METs: realizar ecocardiograma e teste provocativo de isquemia (Cintilografia/Eco com Dobutamina). Monitorização arterial invasiva (PAI) intraoperatória e vigilância intensiva em UTI nas primeiras 48h."),
            ]),
        ],
    }


def get_goldman() -> dict:
    return {
        "id": "calc_goldman",
        "slug": "indice-risco-cardiaco-multifatorial-goldman",
        "name": "Índice de Risco Cardíaco Multifatorial de Goldman (Classes I a IV)",
        "acronym": "Goldman",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Avaliação Pré-Operatória e Cardiologia Perioperatória",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Risco Cirúrgico Pré-Operatório",
        "description": "Primeiro grande escore multifatorial ponderado da cardiologia perioperatória (Goldman et al., NEJM 1977; 0 a 53 pontos, Classes I a IV), atribuindo pesos específicos para descompensação ventricular aguda (B3/turgência jugular +11), IAM recente < 6 meses (+10), arritmias ventriculares/ritmo não sinusal (+14), idade > 70 anos (+5), emergência (+4), cirurgia aórtica/intratorácica/intraperitoneal (+3), estenose aórtica severa (+3) e condição clínica geral ruim (+3).",
        "summary": "Escore multifatorial ponderado de Goldman (0-53 pts, Classes I a IV) com ênfase em B3, IAM recente, arritmias e estenose aórtica.",
        "clinicalObjective": "Quantificar o impacto aditivo de sinais físicos de falência ventricular (B3/TJP), arritmias e estenose aórtica grave antes de cirurgias não cardíacas.",
        "targetPopulation": "Pacientes adultos submetidos a cirurgia não cardíaca sob avaliação cardiológica pré-operatória.",
        "calculationType": "additive_points",
        "formulaExpression": "B3/TJP(11) + IAM<6m(10) + Ritmo/ESV(7+7) + Idade>70(5) + Emergência(4) + Porte/EAo(3+3) + Condição Geral(3) [0 a 53 pts]",
        "evidenceSource": "Goldman L, Caldera DL, Nussbaum SR, et al. Multifactorial index of cardiac risk in noncardiac surgical procedures. N Engl J Med. 1977;297(16):845-850.",
        "minPossibleScore": 0,
        "maxPossibleScore": 53,
        "baseScore": 0,
        "badge": "pre-operatorio",
        "clinicalWarning": "A presença de 3ª bulha (B3) / turgência jugular (+11 pts) ou IAM recente (+10 pts) isoladamente já aproxima ou insere o paciente nas Classes III-IV de Goldman, exigindo compensação clínica antes de qualquer cirurgia eletiva.",
        "radarAxes": [
            _axis("axis_gold_vent", "Função Ventricular e Isquemia (B3 / IAM)", "Cardiovascular"),
            _axis("axis_gold_rhythm", "Arritmias e Valvopatia (Ritmo / ESV / EAo)", "Eletrofisiológico"),
            _axis("axis_gold_surg", "Idade, Emergência, Porte e Estado Geral", "Sistêmico"),
        ],
        "parameterGroups": [
            _grp("grp_gold_s3", "1. Presença de 3ª Bulha (Galope de B3) ou Turgência Jugular Patológica no Exame Físico", "b3-turgencia-jugular-goldman", "axis_gold_vent", 1, "Sinal físico direto de insuficiência cardíaca descompensada e pressão diastólica final do VE elevada.", [
                _opt("opt_gold_s3_0", "Ausente — Sem B3 ou estase jugular (0 pts)", 0, True, 0.0, 1, "Exame físico cardiovascular euvolemico."),
                _opt("opt_gold_s3_11", "Presente — Galope de B3 ou Turgência Jugular (+11 pts)", 11, False, 1.0, 2, "Maior preditor individual do índice de Goldman (+11 pontos)."),
            ]),
            _grp("grp_gold_mi", "2. Infarto Agudo do Miocárdio (IAM) nos Últimos 6 Meses", "iam-recente-goldman", "axis_gold_vent", 2, "Vulnerabilidade de placa coronariana e remodelamento ventricular pós-infarto.", [
                _opt("opt_gold_mi_0", "Ausente ou IAM há > 6 meses (0 pts)", 0, True, 0.0, 1, "Cicatriz miocárdica estabilizada."),
                _opt("opt_gold_mi_10", "Presente — IAM há < 6 meses (+10 pts)", 10, False, 0.95, 2, "Diretrizes modernas destacam risco máximo nos primeiros 30 a 90 dias pós-IAM/stent."),
            ]),
            _grp("grp_gold_rhythm", "3. Ritmo Cardíaco Não Sinusal e Extrassístoles Ventriculares (> 5 ESV/min)", "ritmo-arritmia-goldman", "axis_gold_rhythm", 3, "Ritmo não sinusal ou ESVs no último ECG (+7 pts) e > 5 ESVs/min documentadas em qualquer momento (+7 pts).", [
                _opt("opt_gold_rhy_0", "Ritmo sinusal puro sem extrassístoles ventriculares frequentes (0 pts)", 0, True, 0.0, 1, "Estabilidade elétrica atrial e ventricular."),
                _opt("opt_gold_rhy_7", "Ritmo não sinusal (FA/Flutter) OU > 5 ESV/min isoladamente (+7 pts)", 7, False, 0.55, 2, "Um critério arrítmico de Goldman presente (+7 pontos)."),
                _opt("opt_gold_rhy_14", "Ritmo não sinusal associado a > 5 ESV/min polimórficas (+14 pts)", 14, False, 1.0, 3, "Ambos os critérios arrítmicos presentes (7 + 7 = +14 pontos)."),
            ]),
            _grp("grp_gold_age", "4. Idade Avançada (> 70 Anos)", "idade-70-goldman", "axis_gold_surg", 4, "Reserva fisiológica cardiovascular em septuagenários e octogenários.", [
                _opt("opt_gold_age_0", "Idade <= 70 anos (0 pts)", 0, True, 0.0, 1, "Abaixo do ponto de corte etário de Goldman."),
                _opt("opt_gold_age_5", "Idade > 70 anos (+5 pts)", 5, False, 0.6, 2, "Adiciona +5 pontos ao escore global."),
            ]),
            _grp("grp_gold_emerg", "5. Caráter de Emergência da Cirurgia", "cirurgia-emergencia-goldman", "axis_gold_surg", 5, "Operação de urgência/emergência sem tempo para compensação clínica prévia.", [
                _opt("opt_gold_emg_0", "Cirurgia Eletiva (0 pts)", 0, True, 0.0, 1, "Procedimento programado."),
                _opt("opt_gold_emg_4", "Cirurgia de Emergência (+4 pts)", 4, False, 0.8, 2, "Adiciona +4 pontos pelo estresse catecolaminérgico agudo."),
            ]),
            _grp("grp_gold_surg_aortic", "6. Cirurgia Intraperitoneal/Intratorácica/Aórtica (+3) e Estenose Aórtica Importante (+3)", "porte-estenose-aortica-goldman", "axis_gold_rhythm", 6, "Combinação de cirurgia cavitária maior (+3 pts) e Estenose Valvar Aórtica hemodinamicamente significativa (+3 pts).", [
                _opt("opt_gold_sa_0", "Cirurgia periférica/menor SEM estenose aórtica importante (0 pts)", 0, True, 0.0, 1, "Sem fatores de porte cavitário ou obstrução de via de saída do VE."),
                _opt("opt_gold_sa_3", "Cirurgia Intraperitoneal/Torácica/Aórtica OU Estenose Aórtica Importante (+3 pts)", 3, False, 0.55, 2, "Um dos dois fatores de +3 pontos presente."),
                _opt("opt_gold_sa_6", "Cirurgia Cavitária Maior E Estenose Aórtica Importante (+6 pts)", 6, False, 1.0, 3, "Ambos presentes (3 + 3 = +6 pontos). Alto risco de colapso hemodinâmico na indução."),
            ]),
            _grp("grp_gold_general", "7. Condição Médica Geral Ruim (Distúrbio Metabólico, Renal, Hepático ou Restrição ao Leito)", "condicao-geral-ruim-goldman", "axis_gold_surg", 7, "Qualquer um dos seguintes: PaO2 < 60 ou PaCO2 > 50 mmHg, K+ < 3,0 mEq/L, HCO3- < 20 mEq/L, Ureia > 100 mg/dL (BUN > 50) ou Cr > 3,0 mg/dL, TGO alterada/hepatopatia crônica ou paciente acamado por causa não cardíaca.", [
                _opt("opt_gold_gen_0", "Ausente — Homeostase gasométrica, eletrolítica, renal e hepática preservada (0 pts)", 0, True, 0.0, 1, "Sem desarranjo metabólico ou imobilismo crônico."),
                _opt("opt_gold_gen_3", "Presente — >= 1 critério de condição médica geral ruim (+3 pts)", 3, False, 0.75, 2, "Pontua +3 pontos independente do número de subcritérios metabólicos alterados."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_gold_c1", "Goldman Classe I (0 a 5 pontos) — Risco Cardíaco Baixo", "low", 0, 5, "Complicações cardíacas graves em 0,7% e mortalidade cardíaca em 0,2% (total 0,9%).", "#10b981", [
                _rx("rx_gold_1", "Manutenção da Terapia Basal", "Manter medicações cardiovasculares habituais", "VO", "Pré-operatório"),
            ], [
                _nonrx("nrx_gold_1", "Liberação para o Procedimento Cirúrgico", "Enfermaria / Centro Cirúrgico", "Baixo risco cardiovascular perioperatório."),
            ]),
            _tier("tier_gold_c2", "Goldman Classe II (6 a 12 pontos) — Risco Cardíaco Intermediário", "intermediate", 6, 12, "Complicações cardíacas graves em 5% e mortalidade cardíaca em 2% (total 7%).", "#f59e0b", [
                _rx("rx_gold_2", "Correção de Distúrbios Hidroeletrolíticos (K+ > 4,0 mEq/L) e Controle de FC", "Reposição de Potássio/Magnésio se limítrofes + Betabloqueador se já em uso crônico", "IV / VO", "Pré-operatório"),
            ], [
                _nonrx("nrx_gold_2", "Otimização Clínica e Vigilância Eletrocardiográfica Pós-Operatória", "Enfermaria Monitorizada / Semi-Intensiva", "Realizar ECG no pós-operatório imediato e em 24-48h."),
            ]),
            _tier("tier_gold_c3", "Goldman Classe III (13 a 25 pontos) — Risco Cardíaco Alto", "high", 13, 25, "Complicações cardíacas graves em 11% e mortalidade cardíaca em 2% (total 13-14%).", "#f97316", [
                _rx("rx_gold_3", "Compensação de IC (Furosemida IV se congestão/B3) e Controle de Arritmias", "Furosemida 20-40 mg IV se congestão + Otimização antianginosa/antiarrítmica antes de cirurgia eletiva", "IV", "Pré-operatório"),
            ], [
                _nonrx("nrx_gold_3", "Adiamento de Cirurgia Eletiva para Compensação e UTI Pós-Operatória", "UTI Cirúrgica", "Adiar procedimentos eletivos até desaparecimento de B3/congestão, correção metabólica ou janela segura pós-IAM. Reserva obrigatória de UTI."),
            ]),
            _tier("tier_gold_c4", "Goldman Classe IV (>= 26 pontos) — Risco Proibitivo / Crítico", "critical", 26, 53, "Complicações cardíacas ameaçadoras à vida em 22% e mortalidade cardíaca em 56% (eventos totais 78%).", "#ef4444", [
                _rx("rx_gold_4", "Suporte Hemodinâmico Avançado (Noradrenalina / Dobutamina)", "Noradrenalina em BIC para manter perfusão coronariana + Dobutamina se baixo débito cardíaco", "IV Central", "Contínua em BIC", None, None, None, NOREPINEPHRINE_PROTOCOL),
            ], [
                _nonrx("nrx_gold_4", "Contraindicação a Cirurgias Eletivas (Realizar Apenas Procedimentos Salvadores de Vida)", "UTI Cardiológica / Cirúrgica", "Apenas cirurgias de emergência estrita (ou procedimentos paliativos menos invasivos sob anestesia local/regional se viável). Em estenose aórtica crítica sintomática, considerar Valvoplastia por Balão ou TAVI prévia.", "Monitorização invasiva completa (PAI + Cateter Venoso Central + Ecocardiograma Point-of-Care)."),
            ], NOREPINEPHRINE_PROTOCOL),
        ],
    }


def get_caprini() -> dict:
    return {
        "id": "calc_caprini",
        "slug": "escore-caprini-risco-tev-cirurgico",
        "name": "Escore de Caprini — Estratificação de Risco de TEV em Pacientes Cirúrgicos",
        "acronym": "Caprini",
        "version": "1.0.0",
        "category": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "subcategory": "Tromboprofilaxia Perioperatória e Segurança do Paciente",
        "categorySlug": "bloco-05-cirurgia-geral-trauma",
        "categoryName": "Cirurgia Geral, Trauma e Risco Cirúrgico",
        "moduleName": "Risco Cirúrgico Pré-Operatório",
        "description": "Ferramenta padrão-ouro recomendada pelo American College of Chest Physicians (ACCP 9th Ed.) para estratificação individualizada de risco de Tromboembolismo Venoso (TVP/TEP) em pacientes de cirurgia geral, abdominal, pélvica, vascular, plástica e urológica, ponderando fatores de 1, 2, 3 e 5 pontos para definir a indicação entre deambulação precoce, compressão pneumática intermitente (CPI) e quimioprofilaxia com Enoxaparina/HNF (incluindo profilaxia estendida por 28 dias em cirurgia oncológica).",
        "summary": "Estratificação de risco de TEV perioperatório (Caprini ACCP) com prescrição de CPI e Enoxaparina/HNF.",
        "clinicalObjective": "Prevenir TVP proximal e TEP fatal no pós-operatório, equilibrando a potência da tromboprofilaxia mecânica e farmacológica contra o risco de sangramento cirúrgico.",
        "targetPopulation": "Pacientes adultos submetidos a procedimentos cirúrgicos não ortopédicos ou ortopédicos.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma de Fatores Etários (0-3) + Porte Cirúrgico (0-2) + Clínicos Menores (+1/+2) + Mobilidade (+1/+2) + Trombóticos (+3) + Críticos (+5)",
        "evidenceSource": "Caprini JA. Thrombosis risk assessment as a guide to quality patient care. Dis Mon. 2005;51(2-3):70-78; Gould MK et al. ACCP Evidence-Based Clinical Practice Guidelines (9th Ed). Chest. 2012;141(2 Suppl):e227S-e277S.",
        "minPossibleScore": 0,
        "maxPossibleScore": 15,
        "baseScore": 0,
        "badge": "tromboprofilaxia",
        "clinicalWarning": "Em pacientes submetidos a cirurgia oncológica abdominal ou pélvica de grande porte com Caprini >= 5 pontos, as diretrizes ACCP/ASCO recomendam estender a profilaxia com Enoxaparina 40 mg SC 1x/dia por 4 semanas (28 dias) após a alta hospitalar.",
        "radarAxes": [
            _axis("axis_cap_base", "Idade e Porte Cirúrgico", "Cirúrgico"),
            _axis("axis_cap_immob", "Imobilidade e Comorbidades", "Clínico"),
            _axis("axis_cap_thromb", "Câncer, TEV Prévio e Trauma (3 a 5 pts)", "Hematológico"),
        ],
        "parameterGroups": [
            _grp("grp_cap_age", "1. Faixa Etária do Paciente (1 a 3 pontos)", "faixa-etaria-caprini", "axis_cap_base", 1, "O risco de estase venosa e hipercoagulabilidade endotelial cresce linearmente com a idade.", [
                _opt("opt_cap_age_0", "Idade <= 40 anos (0 pts)", 0, True, 0.0, 1, "Baixo risco etário basal."),
                _opt("opt_cap_age_1", "Idade 41 a 60 anos (+1 pt)", 1, False, 0.35, 2, "Adiciona +1 ponto ao escore de Caprini."),
                _opt("opt_cap_age_2", "Idade 61 a 74 anos (+2 pts)", 2, False, 0.7, 3, "Adiciona +2 pontos."),
                _opt("opt_cap_age_3", "Idade >= 75 anos (+3 pts)", 3, False, 1.0, 4, "Idade muito avançada: +3 pontos isoladamente."),
            ]),
            _grp("grp_cap_surgery", "2. Porte e Duração do Procedimento Cirúrgico Planejado (1 a 2 pontos)", "porte-cirurgico-caprini", "axis_cap_base", 2, "Cirurgia menor (< 45 min) vs Cirurgia aberta ou laparoscópica maior (> 45 min).", [
                _opt("opt_cap_srg_0", "Nenhum procedimento cirúrgico invasivo imediato (0 pts)", 0, True, 0.0, 1, "Sem trauma cirúrgico endotelial."),
                _opt("opt_cap_srg_1", "Cirurgia Menor planejada (< 45 minutos) (+1 pt)", 1, False, 0.45, 2, "Procedimento ambulatorial ou de curta duração (< 45 min)."),
                _opt("opt_cap_srg_2", "Cirurgia Maior Aberta (> 45 min) ou Videolaparoscópica (> 45 min) ou Artroscópica (+2 pts)", 2, False, 1.0, 3, "Qualquer intervenção cirúrgica com anestesia > 45 minutos (+2 pontos)."),
            ]),
            _grp("grp_cap_minor", "3. Fatores Clínicos e Hormonais de 1 Ponto (Obesidade, Varizes, Edema MMII, Sepse, ACO/TRH)", "fatores-1pt-caprini", "axis_cap_immob", 3, "IMC > 25 kg/m², edema de MMII, varizes visíveis, gravidez/puerpério, uso de estrogênio/ACO, sepse/pneumonia (< 1 mês), DPOC, ICC ou DII.", [
                _opt("opt_cap_min_0", "Ausentes (0 pts)", 0, True, 0.0, 1, "Nenhum fator menor de 1 ponto."),
                _opt("opt_cap_min_1", "1 fator presente (ex.: Sobrepeso/Obesidade IMC > 25 ou Varizes) (+1 pt)", 1, False, 0.45, 2, "Um fator clínico de 1 ponto."),
                _opt("opt_cap_min_2", "2 ou mais fatores de 1 ponto combinados (ex.: IMC > 25 + Edema MMII/Sepse) (+2 pts)", 2, False, 1.0, 3, "Múltiplos fatores clínicos menores somados (+2 pontos)."),
            ]),
            _grp("grp_cap_immob_cvc", "4. Mobilidade no Leito, Imobilização Gessada e Acesso Venoso Central (1 a 2 pontos)", "mobilidade-cateter-caprini", "axis_cap_immob", 4, "Paciente clínico em repouso no leito (+1 pt) vs Acamado > 72h, imobilização gessada ou Cateter Venoso Central/PICC (+2 pts).", [
                _opt("opt_cap_mob_0", "Deambulando livremente sem cateter venoso central (0 pts)", 0, True, 0.0, 1, "Bomba muscular da panturrilha ativa."),
                _opt("opt_cap_mob_1", "Restrito ao leito atualmente (< 72 horas) (+1 pt)", 1, False, 0.5, 2, "Redução aguda da mobilidade (< 72h)."),
                _opt("opt_cap_mob_2", "Confinado ao leito > 72h, Imobilização Gessada de MMII ou Cateter Venoso Central (+2 pts)", 2, False, 1.0, 3, "Estase venosa importante ou lesão endotelial por cateter central (+2 pontos)."),
            ]),
            _grp("grp_cap_3pts", "5. Fatores Pró-Trombóticos Maiores de 2 a 3 Pontos (Neoplasia, TEV Prévio, Trombofilia)", "neoplasia-tev-previo-caprini", "axis_cap_thromb", 5, "Neoplasia maligna ativa/prévia (+2 pts); História pessoal de TVP/TEP (+3 pts), História familiar de TEV (+3 pts) ou Trombofilia conhecida — Fator V Leiden, Protrombina, SAF, HIT (+3 pts).", [
                _opt("opt_cap_3p_0", "Ausentes — Sem neoplasia, história de TEV ou trombofilia (0 pts)", 0, True, 0.0, 1, "Sem estados de hipercoagulabilidade primária ou oncológica."),
                _opt("opt_cap_3p_2", "Neoplasia Maligna presente ou prévia (+2 pts)", 2, False, 0.65, 2, "Câncer ativo ou em tratamento oncológico (+2 pontos)."),
                _opt("opt_cap_3p_3", "História Pessoal/Familiar de TVP/TEP ou Trombofilia documentada (+3 pts)", 3, False, 1.0, 3, "Alto risco trombótico intrínseco (+3 pontos)."),
            ]),
            _grp("grp_cap_5pts", "6. Eventos Críticos de 3 a 5 Pontos (Artroplastia, Fratura de Quadril/Pelve/Perna, AVC ou TRM < 1 mês)", "eventos-5pts-caprini", "axis_cap_thromb", 6, "Artroplastia eletiva de quadril ou joelho (+5 pts), Fratura de quadril/pelve/membro inferior (+5 pts), Politrauma grave < 1 mês (+5 pts), Lesão medular aguda/paralisia (+5 pts) ou AVC < 1 mês (+5 pts).", [
                _opt("opt_cap_5p_0", "Ausentes (0 pts)", 0, True, 0.0, 1, "Sem trauma ortopédico maior, artroplastia ou AVC/TRM agudo."),
                _opt("opt_cap_5p_3", "Associação de Neoplasia (+2) com fator adicional (+1) (+3 pts)", 3, False, 0.6, 2, "Combinação oncológica intermediária (+3 pontos)."),
                _opt("opt_cap_5p_5", "Presente — Artroplastia, Fratura de Quadril/Pelve/MMII, Politrauma ou AVC/TRM < 1 mês (+5 pts)", 5, False, 1.0, 3, "Qualquer fator de 5 pontos insere imediatamente o paciente na faixa de Altíssimo Risco de TEV."),
            ]),
        ],
        "riskTiers": [
            _tier("tier_cap_vlow", "Risco Muito Baixo de TEV (Caprini 0 pontos)", "low", 0, 0, "Incidência estimada de TEV sintomático < 0,5% sem profilaxia farmacológica.", "#10b981", [
                _rx("rx_cap_0", "Sem Indicação de Anticoagulação Profilática", "Hidratação adequada; evitar anticoagulantes desnecessários pelo risco de sangramento", "N/A", "Pós-operatório"),
            ], [
                _nonrx("nrx_cap_0", "Deambulação Precoce e Frequente", "Enfermaria / Alta Ambulatorial", "Estimular saída precoce do leito nas primeiras horas pós-operatórias."),
            ]),
            _tier("tier_cap_low", "Risco Baixo de TEV (Caprini 1 a 2 pontos)", "low", 1, 2, "Incidência estimada de TEV em torno de 1,5%.", "#22c55e", [
                _rx("rx_cap_1", "Profilaxia Mecânica Preferencial (Sem Anticoagulante de Rotina)", "Se imobilidade prolongada inesperada e baixo risco de sangramento, considerar HNF 5.000 UI SC 12/12h", "SC", "Opcional"),
            ], [
                _nonrx("nrx_cap_1", "Compressão Pneumática Intermitente (CPI) ou Meias Elásticas de Compressão Graduada + Deambulação", "Enfermaria Cirúrgica", "Instalar perneiras de Compressão Pneumática Intermitente (CPI) no intraoperatório e manter até deambulação plena."),
            ]),
            _tier("tier_cap_mod", "Risco Moderado de TEV (Caprini 3 a 4 pontos)", "intermediate", 3, 4, "Incidência estimada de TEV de 3,0% sem profilaxia (reduzida em > 60% com HBPM).", "#f59e0b", [
                _rx("rx_cap_mod_enox", "Enoxaparina (HBPM) ou Heparina Não Fracionada (HNF)", "Enoxaparina 40 mg SC 1x/dia (iniciar 6-12h após o término da cirurgia após hemostasia segura) OU HNF 5.000 UI SC de 12/12h ou 8/8h", "SC", "24/24h (Enoxaparina)", "Ajuste Renal: Se ClCr < 30 mL/min, reduzir Enoxaparina para 20 mg SC 1x/dia ou preferir HNF 5.000 UI SC 12/12h.", "Se alto risco de sangramento ativo (ex.: neurocirurgia/sangramento cavitário), usar apenas CPI mecânica até hemostasia."),
            ], [
                _nonrx("nrx_cap_mod", "Quimioprofilaxia Farmacológica OU Compressão Pneumática Intermitente (CPI)", "Enfermaria Cirúrgica", "Manter profilaxia durante toda a internação hospitalar até recuperação completa da mobilidade."),
            ]),
            _tier("tier_cap_high", "Alto / Altíssimo Risco de TEV (Caprini >= 5 pontos)", "critical", 5, 15, "Incidência de TEV de 6,0% (Caprini 5-8) até 11-40% (Caprini >= 9) se desprotegido.", "#ef4444", [
                _rx("rx_cap_high_enox", "Profilaxia Dupla Combinada: Enoxaparina 40 mg SC 24/24h + CPI Mecânica", "Enoxaparina 40 mg SC 1x/dia (em obesos mórbidos IMC >= 40 kg/m², considerar Enoxaparina 40 mg SC 12/12h ou 0,5 mg/kg 12/12h) + Compressão Pneumática Intermitente", "SC", "24/24h (estender por 28 dias se cirurgia oncológica abdominal/pélvica ou artroplastia de quadril)", "Se ClCr < 30 mL/min: HNF 5.000 UI SC 8/8h ou Enoxaparina 20 mg SC 24/24h. Se suspeita de HIT (plaquetopenia): Fondaparinux 2,5 mg SC 1x/dia."),
            ], [
                _nonrx("nrx_cap_high", "Associação Obrigatória de Método Farmacológico (HBPM) + Método Mecânico (CPI) e Profilaxia Estendida (28 dias)", "Enfermaria Cirúrgica / UTI", "Combinar CPI intra/pós-operatória com Enoxaparina assim que hemostasia assegurada (12h após retirada de cateter peridural). Prescrever alta com Enoxaparina domiciliar por 28 dias totais em pacientes de cirurgia oncológica abdominal/pélvica ou ortopédica de quadril."),
            ]),
        ],
    }


BLOCK_05_SYNONYMS: dict[str, list[str]] = {
    "calc_alvarado": [
        "alvarado", "escore de alvarado", "mantrels", "apendicite", "apendicite aguda",
        "dor em fossa iliaca direita", "ponto de mcburney", "sinal de blumberg", "migracao da dor",
        "abdome agudo inflamatorio", "apendicectomia", "leucocitose apendicite", "cid k35",
    ],
    "calc_ripasa": [
        "ripasa", "escore ripasa", "apendicite aguda", "alta sensibilidade apendicite", "sinal de rovsing",
        "dor em fid", "defesa abdominal", "eas negativo", "triagem apendicite", "apendicectomia laparoscopica",
        "abdome agudo cirurgico", "mcburney", "cid k35.8",
    ],
    "calc_tokyo_tg18": [
        "tokyo", "tg18", "tokyo guidelines", "criterios de tokyo", "colecistite aguda",
        "colangite aguda", "sinal de murphy", "triade de charcot", "pentade de reynolds", "cpre",
        "colecistectomia videolaparoscopica", "colecistostomia percutanea", "sepse biliar", "cid k81.0", "cid k83.0",
    ],
    "calc_rts": [
        "rts", "revised trauma score", "escore de trauma revisado", "t-rts", "politrauma",
        "triagem de trauma", "glasgow pas fr", "atendimento pre-hospitalar", "sala vermelha trauma",
        "atls", "choque hemorragico", "centro de trauma", "cid t07",
    ],
    "calc_iss": [
        "iss", "injury severity score", "gravidade anatomica do trauma", "abbreviated injury scale",
        "escala ais", "politrauma maior", "iss maior que 15", "trauma multissistemico", "pan-scan trauma",
        "damage control", "controle de danos", "mortalidade no trauma",
    ],
    "calc_triss": [
        "triss", "trauma and injury severity score", "probabilidade de sobrevida no trauma", "mtos",
        "trauma contuso", "trauma penetrante", "arma de fogo faf", "arma branca fab", "rts e iss",
        "auditoria de trauma", "sobrevida politrauma", "atls",
    ],
    "calc_parkland_aba": [
        "parkland", "formula de parkland", "aba queimados", "american burn association", "grande queimado",
        "queimadura", "superficie corporea queimada", "scq", "regra dos 9", "regra de wallace",
        "ringer lactato queimado", "trauma eletrico", "queimadura eletrica", "lesao inalatoria", "cid t31",
    ],
    "calc_asa": [
        "asa", "classificacao asa", "estado fisico asa", "risco anestesico", "anestesiologia",
        "asa i", "asa ii", "asa iii", "asa iv", "modificador de emergencia e",
        "avaliacao pre-anestesica", "risco perioperatorio", "consultorio pre-anestesico",
    ],
    "calc_rcri_lee": [
        "rcri", "indice de lee", "escore de lee", "revised cardiac risk index", "risco cirurgico",
        "risco cardiaco pre-operatorio", "cirurgia nao cardiaca", "mace perioperatorio", "infarto perioperatorio",
        "mins troponina", "capacidade funcional mets", "avaliacao pre-operatoria",
    ],
    "calc_goldman": [
        "goldman", "indice de goldman", "escore de goldman", "risco cardiaco multifatorial",
        "classes de goldman", "terceira bulha b3", "turgencia jugular", "estenose aortica cirurgia",
        "iam recente cirurgia", "extrassistoles ventriculares", "cardiologia perioperatoria",
    ],
    "calc_caprini": [
        "caprini", "escore de caprini", "profilaxia de tev", "tromboprofilaxia cirurgica",
        "tvp pos-operatoria", "embolia pulmonar cirurgica", "enoxaparina profilatica", "clexane cirurgico",
        "compressao pneumatica intermitente", "cpi", "accp guidelines", "cirurgia oncologica tev",
    ],
}


def get_block_05_calculators() -> list[dict]:
    calculators = [
        get_alvarado(),
        get_ripasa(),
        get_tokyo_tg18(),
        get_rts(),
        get_iss(),
        get_triss(),
        get_parkland_aba(),
        get_asa(),
        get_rcri_lee(),
        get_goldman(),
        get_caprini(),
    ]
    for calc in calculators:
        calc["blockId"] = "block_05"
        calc["blockFile"] = "block_05.json"
        calc["categorySlug"] = "bloco-05-cirurgia-geral-trauma"
        calc["categoryName"] = "Cirurgia Geral, Trauma e Risco Cirúrgico"
    return calculators
