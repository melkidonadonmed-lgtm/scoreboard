"""
Common protocols and definitions for Scoreboard App calculators.
"""

NOREPINEPHRINE_PROTOCOL = {
    "drugId": "drug_noradrenalina",
    "drugName": "Noradrenalina (Hemitartarato de Norepinefrina)",
    "standardSolution": {
        "ampoules": "4 ampolas (16 mg = 16 mL)",
        "diluent": "Soro Glicosado a 5% (SG 5%) 234 mL",
        "totalVolumeMl": 250,
        "concentrationMcgMl": 64,
        "mandatoryVehicleNotice": "Veículo MANDATÓRIO: SG 5% (pH ácido 3,5–5,0 protege contra oxidação rápida). Proibida infusão contínua prolongada em SF 0,9%.",
        "indication": "Choque Séptico, Choque Vasoplégico e Choque Cardiogênico com hipotensão grave (PAM < 65 mmHg)"
    },
    "concentratedSolution": {
        "ampoules": "8 ampolas (32 mg = 32 mL)",
        "diluent": "Soro Glicosado a 5% (SG 5%) 218 mL",
        "totalVolumeMl": 250,
        "concentrationMcgMl": 128,
        "mandatoryVehicleNotice": "Solução Concentrada para restrição hídrica severa, SDRA ou LRA anúrica.",
        "indication": "Restrição volêmica estrita / Choque refratário"
    },
    "doseUnit": "mcg/kg/min",
    "initialDose": 0.05,
    "maintenanceDoseMin": 0.1,
    "maintenanceDoseMax": 0.5,
    "maxDose": 2.0,
    "defaultDose": 0.1,
    "isFixedDose": False,
    "administrationRoute": "Acesso Venoso Central exclusivo (em emergência extrema fora da UTI, veia antecubital calibrosa por no máx. 2 a 4h até punção central)",
    "containerCompatibility": "qualquer",
    "nursingPrecautions": "Monitorização de PAM invasiva (PAI) preferencial. Verificar refluxo de sangue no cateter a cada 2h para descartar extravasamento tecidual. Se dose > 0,25 mcg/kg/min, acionar alerta imediato para associação precoce de Vasopressina (0,01 a 0,04 UI/min).",
    "titrationAdvice": "Titular a cada 5 a 10 minutos em passos de 0,02 a 0,05 mcg/kg/min visando PAM >= 65 mmHg (ou >= 80 mmHg em TCE com hipertensão intracraniana).",
    "weaningCriteria": "Iniciar desmame somente após estabilização hemodinâmica persistente por >= 6-12h com lactato em queda e débito urinário > 0,5 mL/kg/h."
}

VASOPRESSIN_PROTOCOL = {
    "drugId": "drug_vasopressina",
    "drugName": "Vasopressina (Arginina Vasopressina)",
    "standardSolution": {
        "ampoules": "1 ampola (20 UI = 1 mL)",
        "diluent": "SF 0,9% ou SG 5% 99 mL",
        "totalVolumeMl": 100,
        "concentrationMcgMl": 200,
        "mandatoryVehicleNotice": "Compatível com SF 0,9% e SG 5%.",
        "indication": "Segundo vasopressor no Choque Séptico refratário a Noradrenalina (> 0,25 mcg/kg/min) e Choque Vasoplégico"
    },
    "doseUnit": "UI/min",
    "initialDose": 0.01,
    "maintenanceDoseMin": 0.01,
    "maintenanceDoseMax": 0.04,
    "maxDose": 0.04,
    "defaultDose": 0.03,
    "isFixedDose": True,
    "administrationRoute": "Acesso Venoso Central exclusivo",
    "containerCompatibility": "qualquer",
    "nursingPrecautions": "DOSE FIXA NÃO TITULÁVEL no choque séptico: 0,01 a 0,04 UI/min (padrão ouro 0,03 UI/min = 9 mL/h). Proibido bolus ou doses > 0,04 UI/min pelo risco de isquemia coronariana grave e necrose mesentérica. Taxa fixa: 0,01 = 3 mL/h; 0,02 = 6 mL/h; 0,03 = 9 mL/h; 0,04 = 12 mL/h.",
    "titrationAdvice": "Não titular para cima! Manter fixa a 0,03 UI/min (9 mL/h) para efeito poupador de catecolamina.",
    "weaningCriteria": "Desmamar preferencialmente após desmame completo ou doses baixas de Noradrenalina (< 0,1 mcg/kg/min)."
}

DOBUTAMINE_PROTOCOL = {
    "drugId": "drug_dobutamina",
    "drugName": "Dobutamina (Cloridrato de Dobutamina)",
    "standardSolution": {
        "ampoules": "1 ampola (250 mg = 20 mL)",
        "diluent": "SG 5% ou SF 0,9% 230 mL",
        "totalVolumeMl": 250,
        "concentrationMcgMl": 1000,
        "mandatoryVehicleNotice": "Veículo: SG 5% ou SF 0,9%. Solução límpida (pode apresentar coloração levemente rosada por oxidação branda sem perda de potência).",
        "indication": "Choque Cardiogênico (Killip III-IV), disfunção miocárdica séptica com ScvO2 < 70% e hipoperfusão persistente"
    },
    "concentratedSolution": {
        "ampoules": "2 ampolas (500 mg = 40 mL)",
        "diluent": "SG 5% ou SF 0,9% 210 mL",
        "totalVolumeMl": 250,
        "concentrationMcgMl": 2000,
        "mandatoryVehicleNotice": "Solução Concentrada (2.000 mcg/mL) para restrição hídrica estrita em insuficiência cardíaca descompensada.",
        "indication": "Restrição volêmica severa / EAP"
    },
    "doseUnit": "mcg/kg/min",
    "initialDose": 2.5,
    "maintenanceDoseMin": 5.0,
    "maintenanceDoseMax": 15.0,
    "maxDose": 20.0,
    "defaultDose": 5.0,
    "isFixedDose": False,
    "administrationRoute": "Acesso Venoso Central ou Periférico Calibroso",
    "containerCompatibility": "qualquer",
    "nursingPrecautions": "Monitorar ECG contínuo para taquicardia sinusal, taquiarritmias ventriculares ou extrassístoles. Atenção ao risco de vasodilatação reflexa periférica beta-2 com queda da PAS; em pacientes hipotensos, associar Noradrenalina previamente.",
    "titrationAdvice": "Titular em incrementos de 2,5 mcg/kg/min a cada 15 a 30 minutos guiado por ScvO2, débito urinário e perfusão periférica.",
    "weaningCriteria": "Reduzir 2,5 mcg/kg/min a cada 2 a 4 horas com monitorização hemodinâmica."
}

NITROGLYCERIN_PROTOCOL = {
    "drugId": "drug_nitroglicerina",
    "drugName": "Nitroglicerina (Tridil)",
    "standardSolution": {
        "ampoules": "1 ampola (50 mg = 10 mL)",
        "diluent": "SG 5% ou SF 0,9% 240 mL",
        "totalVolumeMl": 250,
        "concentrationMcgMl": 200,
        "mandatoryVehicleNotice": "Veículo: SG 5% ou SF 0,9%. Frasco e equipo especiais MANDATÓRIOS.",
        "indication": "Edema Agudo de Pulmão hipertensivo, SCA com dor isquêmica refratária, emergência hipertensiva perioperatória"
    },
    "doseUnit": "mcg/min",
    "initialDose": 5.0,
    "maintenanceDoseMin": 10.0,
    "maintenanceDoseMax": 100.0,
    "maxDose": 200.0,
    "defaultDose": 10.0,
    "isFixedDose": False,
    "administrationRoute": "Acesso Venoso Periférico ou Central",
    "containerCompatibility": "vidro_polietileno_obrigatorio",
    "nursingPrecautions": "MANDATÓRIO frasco de VIDRO ou POLIOLEFINA/POLIETILENO com equipo próprio livre de PVC. PROIBIDO frasco ou equipo de PVC comum: sofre adsorção plástica de 40% a 80% do princípio ativo! Monitorar pressão arterial a cada 5 min durante titulação; suspender se PAS < 90 mmHg.",
    "titrationAdvice": "Iniciar com 5 a 10 mcg/min (1,5 a 3 mL/h). Titular de 5 a 10 mcg/min a cada 5 a 10 minutos até controle dos sintomas ou PAS atingir meta.",
    "weaningCriteria": "Desmame gradual concomitante à introdução de vasodilatadores orais (IECA/BRA ou Nitrato oral)."
}


RADAR_AXES_ENRICHMENTS: dict = {
    "calc_wells_tvp": [
        {"id": "axis_wtvp_score", "label": "Sinais Locais de TVP", "system": "Vascular", "baselineValue": 0, "maxAxisValue": 9},
        {"id": "axis_wtvp_risk", "label": "Fatores Trombogênicos", "system": "Hemostasia", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_wtvp_prob", "label": "Probabilidade Pré-Teste", "system": "Clínico", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_geneva": [
        {"id": "axis_gen_score", "label": "Pontuação Geneva", "system": "TEV", "baselineValue": 0, "maxAxisValue": 22},
        {"id": "axis_gen_hemo", "label": "Estresse Taquicárdico", "system": "Hemodinâmico", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_gen_risk", "label": "Risco Tromboembólico", "system": "Vascular", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_perc": [
        {"id": "axis_perc", "label": "Critérios Positivos PERC", "system": "PERC", "baselineValue": 0, "maxAxisValue": 8},
        {"id": "axis_perc_cardio", "label": "Reserva Cardiopulmonar", "system": "Cardiorrespiratório", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_perc_thrombo", "label": "Fatores Trombogênicos", "system": "Vascular", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_pesi": [
        {"id": "axis_pesi", "label": "Pontos PESI", "system": "PESI", "baselineValue": 0, "maxAxisValue": 150},
        {"id": "axis_pesi_hemo", "label": "Repercussão Hemodinâmica", "system": "Cardiovascular", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_pesi_resp", "label": "Hipoxemia e Sensório", "system": "Respiratório", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_spesi": [
        {"id": "axis_spesi", "label": "Critérios sPESI", "system": "sPESI", "baselineValue": 0, "maxAxisValue": 6},
        {"id": "axis_spesi_hemo", "label": "Estresse Hemodinâmico", "system": "Cardiovascular", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_spesi_resp", "label": "Oxigenação Arterial", "system": "Respiratório", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_rass": [
        {"id": "axis_rass", "label": "Nível RASS", "system": "Sedação", "baselineValue": 0, "maxAxisValue": 5},
        {"id": "axis_rass_vigil", "label": "Vigilância e Alerta", "system": "Neurológico", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_rass_motor", "label": "Controle Psicomotor", "system": "Comportamental", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_sas": [
        {"id": "axis_sas", "label": "Escore SAS", "system": "Sedação", "baselineValue": 4, "maxAxisValue": 7},
        {"id": "axis_sas_coop", "label": "Cooperação e Calma", "system": "Comportamental", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_sas_safety", "label": "Segurança de Dispositivos", "system": "Intensivismo", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_cam_icu": [
        {"id": "axis_cam", "label": "Features CAM-ICU", "system": "Delirium", "baselineValue": 0, "maxAxisValue": 4},
        {"id": "axis_cam_vigil", "label": "Nível de Consciência", "system": "Neurológico", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_cam_thought", "label": "Organização Cognitiva", "system": "Cognitivo", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_ranson": [
        {"id": "axis_ran_adm", "label": "Admissão (0h)", "system": "Admissão", "baselineValue": 0, "maxAxisValue": 5},
        {"id": "axis_ran_48h", "label": "Evolução (48h)", "system": "48 Horas", "baselineValue": 0, "maxAxisValue": 6},
        {"id": "axis_ran_metab", "label": "Repercussão Sistêmica", "system": "Metabólico", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_balthazar_ctsi": [
        {"id": "axis_ctsi_infl", "label": "Inflamação (Balthazar)", "system": "Radiológico", "baselineValue": 0, "maxAxisValue": 4},
        {"id": "axis_ctsi_necr", "label": "Necrose Pancreática", "system": "Perfusão", "baselineValue": 0, "maxAxisValue": 6},
        {"id": "axis_ctsi_prog", "label": "Risco de Infecção / Morbidade", "system": "Prognóstico", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_wfns": [
        {"id": "axis_wfns_gcs", "label": "Escala de Glasgow", "system": "Neurológico", "unit": "GCS", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_wfns_motor", "label": "Déficit Motor Focal Maior", "system": "Neurológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_wfns_prognosis", "label": "Gravidade Neurovascular HSA", "system": "Prognóstico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_fisher_classic": [
        {"id": "axis_fisher_cl_thickness", "label": "Espessura do Sangue Cisternal", "system": "Imagem", "unit": "mm", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_fisher_cl_ventricular", "label": "Hemoventrículo / Hematoma", "system": "Imagem", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_fisher_cl_vasospasm", "label": "Risco de Vasoespasmo / DCI", "system": "Vascular", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_fisher_modified": [
        {"id": "axis_fm_cisternal", "label": "Carga de Sangue Cisternal", "system": "Imagem", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_fm_ivh", "label": "Hemorragia Intraventricular Bilateral", "system": "Imagem", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_fm_dci", "label": "Risco de Isquemia Tardia (DCI)", "system": "Vascular", "unit": "grau", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_knosp": [
        {"id": "axis_knosp_invasion", "label": "Grau de Invasão Cavernosa", "system": "Oncológico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 4},
        {"id": "axis_knosp_resectability", "label": "Risco de Remanescente Tumoral", "system": "Cirúrgico", "unit": "grau", "baselineValue": 0, "maxAxisValue": 4},
        {"id": "axis_knosp_ica", "label": "Envolvimento Carotídeo (ACI)", "system": "Vascular", "unit": "grau", "baselineValue": 0, "maxAxisValue": 4},
    ],
    "calc_samii_koos": [
        {"id": "axis_koos_size", "label": "Extensão Anatômica no APC", "system": "Oncológico", "unit": "grau", "baselineValue": 1, "maxAxisValue": 4},
        {"id": "axis_koos_stem", "label": "Compressão de Tronco / 4º Ventrículo", "system": "Neurológico", "unit": "grau", "baselineValue": 1, "maxAxisValue": 4},
        {"id": "axis_koos_cranial", "label": "Risco ao Nervo Facial / Coclear", "system": "Funcional", "unit": "grau", "baselineValue": 1, "maxAxisValue": 4},
    ],
    "calc_ds_gpa": [
        {"id": "axis_dsgpa_prognosis", "label": "Índice Prognóstico Global", "system": "Oncológico", "unit": "pts", "baselineValue": 4, "maxAxisValue": 4},
        {"id": "axis_dsgpa_performance", "label": "Status Funcional (KPS)", "system": "Funcional", "unit": "pts", "baselineValue": 1, "maxAxisValue": 1},
        {"id": "axis_dsgpa_burden", "label": "Carga Tumoral Encefálica", "system": "Radiológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_kps": [
        {"id": "axis_kps_performance", "label": "Capacidade Funcional / KPS", "system": "Oncológico/Funcional", "unit": "%", "baselineValue": 100, "maxAxisValue": 100},
        {"id": "axis_kps_autonomy", "label": "Autocuidado e Autonomia", "system": "Funcional", "unit": "%", "baselineValue": 0, "maxAxisValue": 1},
        {"id": "axis_kps_tolerance", "label": "Tolerância Terapêutica", "system": "Oncológico", "unit": "%", "baselineValue": 0, "maxAxisValue": 1},
    ],
    "calc_evans_desh": [
        {"id": "axis_desh_pattern", "label": "Morfologia DESH", "system": "Radiológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
        {"id": "axis_desh_ventricle", "label": "Ventriculomegalia / Evans", "system": "Radiológico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
        {"id": "axis_desh_ependymal", "label": "Dinâmica Liquórica / Transependimária", "system": "Hidrodinâmico", "unit": "pts", "baselineValue": 0, "maxAxisValue": 3},
    ],
    "calc_mrs": [
        {"id": "axis_mrs_autonomy", "label": "Grau de Dependência / AVD", "system": "Funcional", "unit": "grau", "baselineValue": 0, "maxAxisValue": 6},
        {"id": "axis_mrs_mobility", "label": "Mobilidade e Marcha", "system": "Motor", "unit": "grau", "baselineValue": 0, "maxAxisValue": 6},
        {"id": "axis_mrs_instrumental", "label": "Independência Instrumental", "system": "Funcional", "unit": "grau", "baselineValue": 0, "maxAxisValue": 6},
    ],
    "calc_hoehn_yahr": [
        {"id": "axis_hy_stage", "label": "Progressão Motora / H&Y", "system": "Motor", "unit": "estágio", "baselineValue": 0, "maxAxisValue": 5},
        {"id": "axis_hy_balance", "label": "Reflexos Posturais / Equilíbrio", "system": "Postural", "unit": "estágio", "baselineValue": 0, "maxAxisValue": 5},
        {"id": "axis_hy_autonomy", "label": "Independência Motora", "system": "Funcional", "unit": "estágio", "baselineValue": 0, "maxAxisValue": 5},
    ],
    "calc_edss": [
        {"id": "axis_edss_disability", "label": "Incapacidade Global / EDSS", "system": "Neurológico", "unit": "pts", "baselineValue": 0.0, "maxAxisValue": 10.0},
        {"id": "axis_edss_ambulation", "label": "Capacidade de Deambulação", "system": "Motor", "unit": "pts", "baselineValue": 0.0, "maxAxisValue": 10.0},
        {"id": "axis_edss_fs", "label": "Sistemas Funcionais (FS)", "system": "Neurológico", "unit": "pts", "baselineValue": 0.0, "maxAxisValue": 10.0},
    ],
}


GROUP_AXIS_REMAPS: dict = {
    "grp_wtvp_cancer": "axis_wtvp_risk",
    "grp_wtvp_paralysis": "axis_wtvp_risk",
    "grp_wtvp_bedridden": "axis_wtvp_risk",
    "grp_wtvp_history": "axis_wtvp_risk",
    "grp_wtvp_collateral": "axis_wtvp_prob",
    "grp_wtvp_alt_diag": "axis_wtvp_prob",
    "grp_gen_hr": "axis_gen_hemo",
    "grp_gen_age": "axis_gen_risk",
    "grp_gen_prev": "axis_gen_risk",
    "grp_gen_surg": "axis_gen_risk",
    "grp_gen_canc": "axis_gen_risk",
    "grp_perc_hr": "axis_perc_cardio",
    "grp_perc_spo2": "axis_perc_cardio",
    "grp_perc_hemopt": "axis_perc_cardio",
    "grp_perc_leg": "axis_perc_thrombo",
    "grp_perc_surg": "axis_perc_thrombo",
    "grp_perc_prior": "axis_perc_thrombo",
    "grp_perc_estrog": "axis_perc_thrombo",
    "grp_pesi_hr": "axis_pesi_hemo",
    "grp_pesi_sbp": "axis_pesi_hemo",
    "grp_pesi_temp": "axis_pesi_hemo",
    "grp_pesi_rr": "axis_pesi_resp",
    "grp_pesi_spo2": "axis_pesi_resp",
    "grp_pesi_mental": "axis_pesi_resp",
    "grp_spesi_hr": "axis_spesi_hemo",
    "grp_spesi_sbp": "axis_spesi_hemo",
    "grp_spesi_spo2": "axis_spesi_resp",
    "grp_cam_feat3": "axis_cam_vigil",
    "grp_cam_feat4": "axis_cam_thought",
    "grp_ran_calc": "axis_ran_metab",
    "grp_ran_pao2": "axis_ran_metab",
    "grp_ran_be": "axis_ran_metab",
    "grp_ran_seq": "axis_ran_metab",
    "grp_gpa_lesions": "axis_dsgpa_burden",
    "grp_gpa_extracranial": "axis_dsgpa_burden",
    "grp_periventricular_edema": "axis_desh_ependymal",
}


def enrich_and_normalize_calculator(calc: dict) -> None:
    """Ensures every calculator has >= 3 radarAxes and 0.0 baseline radarNormalizedValue."""
    calc_id = calc.get("id", "")
    if calc_id in RADAR_AXES_ENRICHMENTS:
        calc["radarAxes"] = RADAR_AXES_ENRICHMENTS[calc_id]
    for group in calc.get("parameterGroups", []):
        gid = group.get("id", "")
        if gid in GROUP_AXIS_REMAPS:
            group["radarAxisId"] = GROUP_AXIS_REMAPS[gid]
        for opt in group.get("options", []):
            if opt.get("isNormalBaseline") is True:
                opt["radarNormalizedValue"] = 0.0
