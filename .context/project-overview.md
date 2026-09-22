# Visão Geral do Projeto: Scoreboard App

## 1. O Problema: O Fim do "Garimpo de Tabelas"
Calculadoras médicas tradicionais (como MDCalc ou QxMD) calculam uma pontuação numérica isolada e entregam uma classificação vaga (ex: "HEART Score 4: Risco Intermediário").
No ambiente de emergência, UTI ou enfermaria, o médico precisa imediatamente de respostas práticas:
- Qual é a dose exata de ataque e manutenção da medicação indicada?
- Como diluir a droga vasoativa em bomba de infusão contínua (BIC)? Qual a vazão inicial em mL/h?
- Qual o destino assistencial imediato (alta, observação, enfermaria ou UTI)?
- Quais os ajustes necessários para função renal e peso?

Para obter essas respostas, o médico precisa interromper o raciocínio, abrir múltiplos PDFs no celular, buscar tabelas espalhadas na internet ou consultar guias desatualizados. Isso causa lentidão no atendimento e sobrecarga cognitiva.

## 2. A Solução: Scoreboard App
O **Scoreboard App** é um Sistema Móvel de Suporte à Decisão Clínica (*Mobile-First CDSS*) de alta velocidade e operação offline-first projetado para democratizar a segurança clínica e facilitar a rotina de **qualquer médico**.

Toda pontuação calculada converte-se automaticamente em **quatro pilares imediatos na mesma tela**:
1. **Estratificação de Risco e Desfecho Estatístico Concreto:** Probabilidade empírica validada na literatura primária (ex.: mortalidade intra-hospitalar em 28 dias, risco de MACE em 6 semanas, probabilidade de TEP).
2. **Conduta Farmacológica Acionável na Mesma Tela:** Fármacos de primeira linha com doses de ataque e manutenção, diluições hospitalares padronizadas, vazão em BIC (mL/h) e alertas de ajuste renal/peso.
3. **Conduta Não Farmacológica e Destino Assistencial:** Indicação clara de destino (Alta Orientada, Observação, Enfermaria com Telemetria ou UTI), suporte ventilatório e metas de tempo porta-procedimento.
4. **Dashboard de Desvio Fisiológico (Radar SVG 60fps):** Visualização gráfica espacial em tempo real comparando a homeostase de um indivíduo sadio de referência (polígono verde central) com a distorção multieixo do paciente (polígono de sobreposição dinâmico).

## 3. Catálogo Clínico: 9 Blocos e 20 Módulos (98 Dossiês Monográficos)
O escopo abrange 98 escores clínicos divididos em 9 blocos de especialidades:
- **Bloco 1:** Emergência, Choque e Terapia Intensiva (Módulos 01 a 04)
- **Bloco 2:** Cardiologia e Hemodinâmica (Módulos 05 a 07)
- **Bloco 3:** Neurologia e Neurocirurgia (Módulo 08)
- **Bloco 4:** Pneumologia (Módulos 09 e 10)
- **Bloco 5:** Cirurgia Geral e Trauma (Módulos 11 a 13)
- **Bloco 6:** Nefrologia e Meio Interno (Módulos 14 e 15)
- **Bloco 7:** Hepatologia e Gastroenterologia (Módulos 16 e 17)
- **Bloco 8:** Pediatria e Neonatologia (Módulos 18 e 19)
- **Bloco 9:** Hematologia e Reumatologia (Módulo 20)

## 4. Recursos de Produtividade Médica
- **Modo Score Avulso Direto:** Acesso direto a qualquer escore com preenchimento em segundos.
- **Favoritos do Plantão (Quick-Pins ⭐):** Fixação rápida dos escores mais usados na rotina de cada profissional.
- **Botão "Copiar para PEP":** Formatação de sumário clínico em texto puro compatível com Tasy, MV Soul, Epimed, Philips e Pixeon.
- **Modo "Meus Leitos":** Acompanhamento rápido da evolução dos pacientes do plantão sem identificação nominal (apenas apelidos transitórios como "Leito 04 - UTI").
