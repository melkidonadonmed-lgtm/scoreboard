# Diretrizes de Engenharia e Integridade Clínica: Scoreboard App

Estas regras aplicam-se a todos os agentes operando no repositório `scoreboard-app`.

## 1. Proibição de Condensação Destrutiva (Anti-Truncation)
- **Preservação de Conteúdo:** É expressamente proibido descartar, suprimir ou abreviar ferramentas clínicas, parâmetros laboratoriais, tabelas de pontos ou condutas farmacológicas presentes nos 98 dossiês clínicos monográficos estruturados em `docs/01_especificacoes_clinicas/`.
- **Integridade de Schemas de Dados:** Schemas de dados estruturados (ex.: o modelo Seed JSON do HEART Score com `calculator`, `radar_axes`, `pharmacological_actions`, `non_pharmacological_actions`) devem ser preservados e utilizados como base para a modelagem TypeScript/Zod em `src/types/clinical.ts`.
- **Diferenciação entre Síntese e Especificação:** Matrizes resumidas (como `MATRIZ_TAXONOMIA_20_MODULOS.md`) são apenas resumos ilustrativos; a especificação definitiva do catálogo são os 98 dossiês clínicos originais.

## 2. Arquitetura de Dados Modulares (Zero Monolito)
- **Modularização por Bloco:** Os 98 escores clínicos devem ser organizados em 9 arquivos JSON modulares independentes (`src/data/blocks/block_01.json` a `block_09.json`) com carregamento sob demanda (*lazy-loading*).
- **Manifesto Leve:** O carregamento inicial utiliza um manifesto de busca leve (~30KB), garantindo inicialização rápida (<100ms) no celular.
- **Motores Puros:** Os motores de cálculo (`calculationEngine.ts`, `infusionEngine.ts`, `radarEngine.ts`, `pepExportEngine.ts`) devem residir em `src/engines/`, como funções TypeScript puras sem dependência de UI e com 100% de testes unitários no Vitest.

## 3. Diretrizes Médicas Vigentes
- **Sepse:** qSOFA com aviso mandatório da Surviving Sepsis Campaign (SSC 2021) desaconselhando uso isolado para exclusão de sepse; SOFA completo para confirmação de disfunção multiorgânica.
- **DPOC:** Classificação moderna GOLD ABE (2024/2025).
- **Queimaduras:** Padrão ABA moderno ($2\text{ mL/kg/% SCQ}$ de Ringer Lactato) como recomendado; Parkland tradicional ($4\text{ mL}$) comutável para trauma elétrico.
- **Nefrologia:** Equação CKD-EPI 2021 sem variável de raça.
- **Hepatologia:** MELD-Na (padrão Brasil/SUS) com opção de análise comparativa para MELD 3.0.
- **Drogas Vasoativas em BIC:** Noradrenalina diluída preferencialmente em SG 5%; Vasopressina em dose fixa ($0,01\text{ a }0,04\text{ UI/min}$); Nitroglicerina em frasco de vidro ou polietileno/poliolefina.

## 4. Privacidade e Segurança (Zero LGPD Risk)
- Nenhum dado identificador de paciente (nome, CPF, prontuário) pode ser enviado para servidores externos.
- O modo "Meus Leitos" deve operar exclusivamente via IndexedDB local com rótulos anônimos transitórios ("Leito 04 - UTI").
