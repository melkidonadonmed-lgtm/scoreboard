# DESIGN.md — Scoreboard App (Clinical Decision Support System)

> **Contrato Visual e Arquitetura de Interface (SSOT):** Este documento define os tokens semânticos, a escala tipográfica, a hierarquia visual em 3 níveis, a composição espacial mobile-first e os estados finitos (FSM) do **Scoreboard App**, alinhados ao domínio médico-assistencial (Emergência, UTI, Neurocirurgia e Clínica Médica).

---

## 1. Visão Geral e Atmosfera

- **Tarefa Primária do Usuário:** Consultar e calcular rapidamente escores clínicos à beira do leito no celular (operação *One-Thumb*), visualizar a estratificação de risco e copiar a conduta/prescrição estruturada para o prontuário eletrônico (PEP).
- **Polaridade Luminosa (Dual Theme Adaptativo):**
  - **Modo Diurno (`:root` / Light Mode):** Superfícies claras de alto contraste (`#F8FAFC` / `#FFFFFF`) otimizadas para leitura rápida sob iluminação intensa de enfermaria, ambulatório e pronto-socorro.
  - **Modo Plantão Noturno (`.dark` / Dark Mode):** Superfícies escuras de baixo ofuscamento (`#090D16` / `#0F172A`) para uso em UTI e sala vermelha noturna.
- **Densidade Espacial:** **Compacta e Escaneável no Mobile** — listas de seleção exibem de 6 a 8 escores simultâneos na tela vertical do celular (apenas **Sigla/Nome + Função Clínica** em 1 linha concisa), e a tela de cálculo prioriza os **Parâmetros de Entrada no topo**, posicionando os **Gráficos (Radar Fisiológico) na base analítica** da página.

---

## 2. Tokens Semânticos de Cor

| Token CSS | Papel Semântico | Light Mode (`:root`) | Dark Mode (`.dark`) | Contraste Mínimo |
| :--- | :--- | :--- | :--- | :--- |
| `--color-canvas` | Plano de fundo base da aplicação | `#F8FAFC` | `#090D16` | — |
| `--color-surface` | Superfície primária de cards e listas | `#FFFFFF` | `#0F172A` | — |
| `--color-surface-raised` | Superfície secundária, opções e agrupamentos | `#F1F5F9` | `#1E293B` | — |
| `--color-border-subtle` | Bordas estruturais e divisores sutis | `#E2E8F0` | `#1E293B` | — |
| `--color-text-primary` | Títulos, siglas de escores e valores numéricos | `#0F172A` | `#F8FAFC` | `>= 12:1` (AAA) |
| `--color-text-secondary` | Função do escore, rótulos auxiliares e unidades | `#64748B` | `#94A3B8` | `>= 4.8:1` (AA) |
| `--accent-primary` | Ação primária, item selecionado e letra ativa | `#2563EB` | `#3B82F6` | `>= 4.5:1` (AA) |
| `--clinical-stable` | Baixo risco / Homeostase fisiológica | `#10B981` | `#10B981` | Semântico |
| `--clinical-warning` | Risco intermediário / Alerta clínico (ex.: SSC 2021) | `#F59E0B` | `#F59E0B` | Semântico |
| `--clinical-critical` | Alto risco / Emergência / Disfunção grave | `#EF4444` | `#EF4444` | Semântico |
| `--clinical-info` | Protocolo de Bomba de Infusão Contínua (BIC) | `#0EA5E9` | `#38BDF8` | Semântico |

**Regra de Equilíbrio 90 / 8 / 2:**
- `90%` superfícies neutras (`--color-canvas`, `--color-surface`);
- `8%` bordas estruturais sutis (`--color-border-subtle`) e agrupamentos;
- `2%` acento semântico (`brand` ou cor do estrato de risco ativo).

---

## 3. Tipografia e Hierarquia

- **Famílias Tipográficas:**
  - `--font-sans`: `Inter, system-ui, -apple-system, sans-serif` para leitura clínica rápida.
  - `--font-mono`: `JetBrains Mono, ui-monospace, SFMono-Regular, monospace` para pontuações, vazões de BIC (`mL/h`), doses (`mcg/kg/min`) e latência.
- **Regras Numéricas Obrigatórias:**
  - `font-variant-numeric: tabular-nums` (`.tabular-nums`) em todos os contadores de escore, badges de pontos (`+1 pt`, `0 pts`), vazões de infusão e réguas alfabéticas.
  - Unidades clínicas (`.clinical-unit`: `mg/dL`, `mcg/kg/min`, `mL/h`, `mmHg`) com `white-space: nowrap` para impedir quebra de linha separada do número.
- **Hierarquia Visual em 3 Níveis (Squint Test):**
  1. **Nível 1 (Âncora Primária):** No catálogo, a **Sigla/Nome do Escore** (`text-sm font-bold`); na calculadora, o **Placar Numérico + Badge de Risco** e os **Parâmetros Clínicos**.
  2. **Nível 2 (Função e Controles Operacionais):** Na lista, a **Função Clínica em 1 linha** (`line-clamp-1 text-xs`); na calculadora, as opções de resposta e condutas terapêuticas.
  3. **Nível 3 (Análise Gráfica e Metadados):** **Gráfico Radar de Desvio Fisiológico** posicionado no final da calculadora (abaixo dos parâmetros e condutas), seguido da referência bibliográfica.

---

## 4. Espaçamento e Grid (Base-4 / Base-8)

- **Container Mobile-First:** Largura máxima `max-w-md mx-auto` (`448px`) centralizada, garantindo alcance natural do polegar (*One-Thumb Zone*).
- **Catálogo de Escores Compacto (`AzScoreList`):**
  - Cards em linha compacta (`px-3 py-2.5 rounded-xl`, espaçamento vertical `space-y-1.5`), exibindo apenas **Nome/Sigla + Função Clínica**, sem rodapés bibliográficos extensos que inflavam a altura no celular.
  - Margem direita dedicada (`pr-8`) para que a régua alfabética A–Z nunca sobreponha o texto nem o botão de favoritar.
- **Fluxo Vertical da Calculadora (`CalculatorView`):**
  1. Cabeçalho Sticky Compacto (Voltar, Nome do Escore, Reset, Favorito, Copiar PEP).
  2. Barra Resumo de Resultado (Pontuação `tabular-nums` + Badge de Risco + Desfecho conciso).
  3. Aviso Mandatório SSC 2021 (exclusivo quando aplicável, ex.: `qSOFA`).
  4. **Parâmetros Avaliados (Foco Primário no Topo)** — agrupados com espaçamento limpo (`space-y-2.5`) e opções enxutas.
  5. Condutas Clínicas Recomendadas e Micro-Calculadora de Drogas Vasoativas em BIC.
  6. **Gráfico Radar de Desvio Fisiológico (Posicionado embaixo)** + Fonte de Evidência.

---

## 5. Elevação, Bordas e Superfícies

- **Raios de Borda:** `--radius-md` (`0.75rem / 12px`) para itens de lista e botões de opção; `--radius-lg` (`1rem / 16px`) para painéis consolidados.
- **Profundidade Tátil:** Bordas de `1px solid var(--color-border-subtle)` combinadas a sombras leves (`--shadow-card`) e chanfro superior sutil (`--shadow-bevel`).

---

## 6. Diretrizes de Componentes e Estados (FSM)

- **Estados Finitos:**
  - `idle`: Parâmetros no valor basal fisiológico (`0 pts`).
  - `active / calculated`: Atualização reativa instantânea (`< 1ms`) da pontuação, faixa de risco, prescrição BIC e polígono do radar.
  - `empty`: Estado vazio instrutivo na busca sem resultados ou lista de favoritos vazia.
  - `copied`: Feedback imediato (`Copiado!`) ao exportar minuta SOAP/SBAR para o PEP.
- **Régua Alfabética Sincronizada (`AlphabetJumpRail`):**
  - Posicionada de forma fixa/estável na lateral direita da área útil, sem quebrar ou sumir durante a rolagem.
  - **Scroll Spy Ativo:** Acompanha automaticamente os cabeçalhos de letras conforme o usuário rola a lista de nomes, destacando a letra atual em tempo real e exibindo bolha de pré-visualização durante o arraste tátil.

---

## 7. Micro-interações e Acessibilidade

- **Curva de Transição:** `--ease-spring: cubic-bezier(0.22, 1, 0.36, 1)` para feedback de toque nos itens da lista (`hover:translate-x-0.5 active:scale-[0.99]`), indicador lateral de foco e transição suave entre seções alfabéticas.
- **Alvos de Toque:** Área mínima de toque acessível (`>= 44x44px`) em controles interativos.
- **Acessibilidade (WAI-ARIA):** `role="searchbox"`, `role="radiogroup"`, `role="radio"`, `aria-checked`, `aria-live="polite"` no resultado do escore e suporte a `@media (prefers-reduced-motion: reduce)`.

---

## 8. Anti-Padrões do Projeto (Proibições Estritas)

1. **Proibido Caixas Gigantes na Lista Mobile:** Nunca exibir citações bibliográficas longas (JAMA, Lancet, etc.) ou parágrafos múltiplos nos cards da lista de seleção A–Z.
2. **Proibido Gráfico Acima dos Parâmetros:** O Gráfico Radar nunca deve ficar no topo da calculadora empurrando os inputs clínicos para fora da primeira dobra da tela no celular.
3. **Proibido Régua A–Z Estática ou Quebrada:** O índice alfabético lateral não pode desaparecer ao rolar a página nem ficar dessincronizado da letra visível na tela.
4. **Zero Emojis na UI:** Proibido usar emojis em títulos, badges ou estados vazios; utilize exclusivamente ícones vetoriais SVG (`lucide-react`).
