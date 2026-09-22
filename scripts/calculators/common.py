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
