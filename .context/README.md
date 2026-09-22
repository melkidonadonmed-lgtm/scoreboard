# Contexto do Projeto: Scoreboard App

Esta pasta `.context/` é a fonte viva da verdade arquitetural, clínica e técnica do **Scoreboard App**, mantida diretamente no controle de versão (Git). Ela serve como memória permanente para desenvolvedores e agentes autônomos de IA.

## Índice de Documentos de Contexto

1. **[`project-overview.md`](./project-overview.md)**  
   Visão geral do produto, problema clínico abordado (o fim do "garimpo de tabelas"), proposta de valor e os 4 pilares de entrega imediata em cada cálculo.

2. **[`architecture.md`](./architecture.md)**  
   Arquitetura de software, stack técnica (React 18 + Vite + TS + Tailwind), modelo de dados modular ("Zero Monolito" com 9 blocos JSON lazy-loaded), motores de cálculo puros, radar fisiológico em SVG nativo e persistência local via IndexedDB.

3. **[`clinical-guidelines.md`](./clinical-guidelines.md)**  
   Diretrizes médicas contemporâneas mandatórias (SSC 2021 para sepse, GOLD ABE 2024/2025, ABA 2mL/kg/%SCQ para queimaduras, CKD-EPI 2021 sem raça, MELD-Na SUS, protocolos de infusão em BIC).

4. **[`current-state.md`](./current-state.md)**  
   Fotografia do estado atual do repositório: o que já foi concluído (especificações monográficas, matrizes MECE, design system, organização do Drive) e o que está pendente.

5. **[`roadmap-and-backlog.md`](./roadmap-and-backlog.md)**  
   Plano de execução detalhado em 4 fases determinísticas, backlog de tarefas prioritárias e critérios de aceitação.

---

## Regras de Manutenção deste Contexto
- Qualquer decisão arquitetural ou alteração no escopo clínico deve ser refletida imediatamente nestes arquivos.
- A regra de **Anti-Truncamento** (preservação estrita dos 98 dossiês clínicos sem simplificações destrutivas) é inviolável.
- Nenhum dado de paciente pode trafegar ou persistir fora da memória local do cliente (Zero LGPD Risk).
