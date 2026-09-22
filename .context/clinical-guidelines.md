# Diretrizes Clínicas Vigentes e Normas Médicas

O Scoreboard App fundamenta-se estritamente nas diretrizes clínicas de sociedades médicas nacionais e internacionais vigentes. O cumprimento das seguintes diretrizes é obrigatório em toda a modelagem de dados e cálculo.

---

## 1. Sepse e Disfunção Orgânica (SSC 2021)
- **qSOFA:** Obrigatório exibir o aviso mandatório da *Surviving Sepsis Campaign (SSC 2021)* desaconselhando o uso isolado do qSOFA como ferramenta de triagem única para excluir sepse.
- **SOFA Completo:** Deve ser indicado para confirmação formal e estratificação de disfunção multiorgânica quando houver suspeita de sepse.
- **Lactato:** Alerta de hiperlactatemia ($> 2\text{ mmol/L}$) associada a hipotensão refratária a volume como definidor de choque séptico.

---

## 2. Doença Pulmonar Obstrutiva Crônica (GOLD ABE 2024/2025)
- Classificação moderna **GOLD ABE**:
  - Eliminação da antiga distinção C e D isolada; unificação no **Grupo E** (pacientes com $\ge 2$ exacerbações moderadas ou $\ge 1$ exacerbação que levou à hospitalização).
  - Grupos **A** e **B** baseados na carga sintomática (mMRC ou CAT) com baixo histórico de exacerbação ($\le 1$ moderada sem internação).

---

## 3. Ressuscitação Volêmica em Grandes Queimados (ABA vs. Parkland)
- **Padrão Moderno American Burn Association (ABA):** $2\text{ mL/kg/% SCQ}$ de Ringer Lactato nas primeiras 24 horas (metade nas primeiras 8h a contar da hora da queimadura).
- **Parkland Tradicional:** $4\text{ mL/kg/% SCQ}$ disponível como comutação orientada prioritariamente para queimaduras elétricas de alta voltagem, lesão por inalação associada ou atraso de ressuscitação.
- **Meta de Débito Urinário:** Alvo de $0,5\text{ a }1,0\text{ mL/kg/h}$ em adultos ($1,0\text{ a }1,5\text{ mL/kg/h}$ em queimadura elétrica com mioglobinúria).

---

## 4. Nefrologia e Filtração Glomerular (CKD-EPI 2021)
- **Equação CKD-EPI 2021:** Utilizar a versão atualizada que **não inclui a variável de raça** (race-free), em conformidade com as diretrizes do KDIGO e National Kidney Foundation (NKF).
- **Cockcroft-Gault:** Mantida como alternativa específica para ajuste de dose de fármacos de bula estrita que ainda exigem clearance estimado por Cockcroft-Gault.

---

## 5. Hepatologia e Alocação de Fígado (MELD-Na SUS vs. MELD 3.0)
- **Padrão SUS / Brasil:** Utilizar a fórmula oficial **MELD-Na** preconizada pela Portaria do Ministério da Saúde para lista de transplante hepático no Brasil.
- **Comparativo:** Permitir comutação/comparação visual informativa com **MELD 3.0** (que inclui albumina e correção para sexo feminino).

---

## 6. Drogas Vasoativas e Bomba de Infusão Contínua (BIC)
- **Noradrenalina (Hemitartarato de Norepinefrina):**
  - Diluição preferencial e obrigatória em **Soro Glicosado a 5% (SG 5%)** para proteção contra oxidação da catecolamina (evitar SF 0,9% como veículo primário).
  - Concentração padrão: 4 ampolas (16 mg) + 234 mL SG 5% ($64\ \mu\text{g/mL}$).
  - Alvo hemodinâmico: PAM $\ge 65\text{ mmHg}$.
- **Vasopressina:**
  - Dose fixa de $0,01\text{ a }0,04\text{ UI/min}$ no choque refratário a noradrenalina.
  - Não titular livremente como a noradrenalina; atua como poupador de catecolamina.
- **Nitroglicerina (Tridil):**
  - Exigência mandatória de frasco de **vidro ou polietileno/poliolefina** devido à adsorção do fármaco em recipientes e equipos de cloreto de polivinila (PVC).
- **Dobutamina:**
  - Concentração padrão: 1 ampola (250 mg) + 230 mL SG 5% ($1.000\ \mu\text{g/mL}$).
  - Faixa usual: $2,5\text{ a }20\ \mu\text{g/kg/min}$.

---

## 7. Conformidade Regulatória (RDC ANVISA 657/2022)
- Software classificado como **Software como Dispositivo Médico (SaMD)** de classe I/Apoio à Decisão Clínica informada.
- O aplicativo não toma decisões autônomas; fornece dados, referências primárias e protocolos padronizados ao médico assistente.
