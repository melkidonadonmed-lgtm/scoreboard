"""
Block 03 Stroke & Neurovascular Module:
1. NIHSS (National Institutes of Health Stroke Scale)
2. ASPECTS (Alberta Stroke Program Early CT Score)
3. ICH Score (Intracerebral Hemorrhage)
4. ABCD2 Score (Risco de AVC pós-AIT)
"""

from calculators.common import NOREPINEPHRINE_PROTOCOL

def get_nihss():
    return {
        "id": "calc_nihss",
        "slug": "nihss",
        "name": "National Institutes of Health Stroke Scale (NIHSS)",
        "acronym": "NIHSS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurologia Vascular / AVC Agudo",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Doença Cerebrovascular e AVC Agudo",
        "description": "Escala padronizada de 11 domínios funcionais / 15 parâmetros (0 a 42 pontos) para quantificar o déficit neurológico agudo, estratificar risco de oclusão de grande vaso e selecionar reperfusão (trombólise IV e trombectomia mecânica).",
        "summary": "Escala quantitativa de déficit neurológico agudo avaliando 11 domínios funcionais / 15 parâmetros (0 a 42 pontos).",
        "clinicalObjective": "Mensuração padronizada da gravidade do déficit no AVC agudo, monitoramento de deterioração clínica e indicação de terapias de reperfusão cerebral.",
        "targetPopulation": "Pacientes com suspeita clínica de AVC isquêmico ou hemorrágico agudo nas primeiras 24 horas do ictus.",
        "calculationType": "additive_points",
        "formulaExpression": "Soma_de_todos_os_15_itens_operacionais",
        "evidenceSource": "Brott T, Adams HP Jr, Olinger CP, et al. Measurements of acute cerebral infarction: a clinical examination scale. Stroke. 1989;20(7):864-870. AHA/ASA Stroke Guidelines 2019/2021.",
        "minPossibleScore": 0,
        "maxPossibleScore": 42,
        "baseScore": 0,
        "badge": "avc-agudo",
        "clinicalWarning": "METAS PRESSÓRICAS MANDATÓRIAS NO AVC AGUDO: Para pacientes candidatos a trombólise endovenosa (Alteplase ou Tenecteplase), a Pressão Arterial DEVE ser mantida estritamente abaixo de 185/110 mmHg antes da infusão e abaixo de 180/105 mmHg nas primeiras 24 horas. Se NIHSS >= 6, suspeitar fortemente de Oclusão de Grande Vaso (LVO) e acionar Angio-TC e equipe de Neurorradiologia Intervencionista para Trombectomia Mecânica em janela estendida de até 24 horas.",
        "radarAxes": [
            {
                "id": "axis_nihss_consciousness",
                "label": "Nível de Consciência",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_nihss_motor",
                "label": "Déficit Motor (Braços/Pernas)",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_nihss_vision_gaze",
                "label": "Olhar e Campos Visuais",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_nihss_language",
                "label": "Linguagem e Disartria",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_nihss_sensory_neglect",
                "label": "Sensibilidade e Inatenção",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_nihss_1a",
                "name": "1a. Nível de Consciência (NdC)",
                "slug": "nihss-1a-ndc",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_consciousness",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Responsividade global e alerta do paciente.",
                "options": [
                    {
                        "id": "opt_nihss_1a_0",
                        "label": "0: Alerta / Prontamente responsivo",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Vigil e atento a estímulos habituais."
                    },
                    {
                        "id": "opt_nihss_1a_1",
                        "label": "1: Sonolento (desperta ao estímulo verbal leve ou tátil)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Sonolento, mas desperta a estímulo sonoro ou toque suave."
                    },
                    {
                        "id": "opt_nihss_1a_2",
                        "label": "2: Estuporoso (requer estímulo doloroso vigoroso/repetido)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.66,
                        "sortOrder": 3,
                        "description": "Requer estímulos nociceptivos fortes para esboçar resposta motora voluntária."
                    },
                    {
                        "id": "opt_nihss_1a_3",
                        "label": "3: Comatoso (respostas apenas reflexas ou flacidez total)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Coma não responsivo ou respostas reflexas motoras/autonômicas."
                    }
                ]
            },
            {
                "id": "grp_nihss_1b",
                "name": "1b. Perguntas sobre NdC (Mês atual e Idade)",
                "slug": "nihss-1b-perguntas",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_consciousness",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Apenas a primeira resposta é pontuada. Não ajudar.",
                "options": [
                    {
                        "id": "opt_nihss_1b_0",
                        "label": "0: Responde ambas as perguntas corretamente",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Acerta o mês atual e a idade exata."
                    },
                    {
                        "id": "opt_nihss_1b_1",
                        "label": "1: Responde apenas uma corretamente (ou disartria/intubado)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Acerta apenas uma pergunta."
                    },
                    {
                        "id": "opt_nihss_1b_2",
                        "label": "2: Erra ambas as perguntas (ou afásico global/comatoso)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Erra ambas as perguntas ou incapacidade total de comunicação."
                    }
                ]
            },
            {
                "id": "grp_nihss_1c",
                "name": "1c. Comandos de NdC (Abrir/fechar olhos e mão)",
                "slug": "nihss-1c-comandos",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_consciousness",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Pode demonstrar por mímica se houver déficit de compreensão.",
                "options": [
                    {
                        "id": "opt_nihss_1c_0",
                        "label": "0: Executa ambos os comandos corretamente",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Abre/fecha olhos e abre/fecha a mão não parética."
                    },
                    {
                        "id": "opt_nihss_1c_1",
                        "label": "1: Executa apenas um comando corretamente",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Executa somente uma das tarefas solicitadas."
                    },
                    {
                        "id": "opt_nihss_1c_2",
                        "label": "2: Não executa nenhum comando",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Não responde a nenhuma das solicitações."
                    }
                ]
            },
            {
                "id": "grp_nihss_2",
                "name": "2. Olhar Conjugado Horizontal",
                "slug": "nihss-2-olhar",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_vision_gaze",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Testar movimentos oculares horizontais voluntários ou de perseguição.",
                "options": [
                    {
                        "id": "opt_nihss_2_0",
                        "label": "0: Movimentação ocular conjugada normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Olhar conjugado simétrico e completo."
                    },
                    {
                        "id": "opt_nihss_2_1",
                        "label": "1: Paresia parcial do olhar (superável por reflexo oculocefálico)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Déficit parcial superável por manobra dos olhos de boneca."
                    },
                    {
                        "id": "opt_nihss_2_2",
                        "label": "2: Desvio conjugado forçado e fixo do olhar (não superável)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Desvio forçado fixo do olhar conjugado não superável por reflexos."
                    }
                ]
            },
            {
                "id": "grp_nihss_3",
                "name": "3. Campos Visuais (Confrontação por Quadrantes)",
                "slug": "nihss-3-campos-visuais",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_vision_gaze",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Testar contagem de dedos ou reflexo de ameaça em cada quadrante.",
                "options": [
                    {
                        "id": "opt_nihss_3_0",
                        "label": "0: Sem perda de campo visual (visão normal)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Campos visuais preservados bilateralmente."
                    },
                    {
                        "id": "opt_nihss_3_1",
                        "label": "1: Hemianopsia parcial / quadrantanopsia homônima",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Perda parcial do campo visual (quadrantanopsia)."
                    },
                    {
                        "id": "opt_nihss_3_2",
                        "label": "2: Hemianopsia completa homônima",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.66,
                        "sortOrder": 3,
                        "description": "Perda completa da metade do campo visual em ambos os olhos."
                    },
                    {
                        "id": "opt_nihss_3_3",
                        "label": "3: Cegueira cortical bilateral / Hemianopsia bilateral",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Cegueira completa em ambos os olhos."
                    }
                ]
            },
            {
                "id": "grp_nihss_4",
                "name": "4. Paresia Facial",
                "slug": "nihss-4-paresia-facial",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "helpText": "Pedir para mostrar dentes, fechar olhos e erguer sobrancelhas.",
                "options": [
                    {
                        "id": "opt_nihss_4_0",
                        "label": "0: Movimentação facial simétrica e normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Mímica facial preservada bilateralmente."
                    },
                    {
                        "id": "opt_nihss_4_1",
                        "label": "1: Paresia leve (apagamento do sulco nasolabial, assimetria discreta)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Assimetria sutil ao sorrir ou franzir."
                    },
                    {
                        "id": "opt_nihss_4_2",
                        "label": "2: Paresia moderada (paralisia completa da metade inferior da face)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.66,
                        "sortOrder": 3,
                        "description": "Paralisia facial central nítida com preservação frontal."
                    },
                    {
                        "id": "opt_nihss_4_3",
                        "label": "3: Paralisia facial completa (superior e inferior uni ou bilateral)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Ausência total de movimentos faciais em um ou ambos os lados."
                    }
                ]
            },
            {
                "id": "grp_nihss_5a",
                "name": "5a. Motricidade Braço Esquerdo (MSE)",
                "slug": "nihss-5a-mse",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "helpText": "Manter membro estendido a 90° (sentado) ou 45° (supino) por 10 segundos.",
                "options": [
                    {
                        "id": "opt_nihss_5a_0",
                        "label": "0: Sem queda por 10 segundos completos",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sustenta o braço sem declínio por 10s."
                    },
                    {
                        "id": "opt_nihss_5a_1",
                        "label": "1: Queda antes de 10s, mas não toca o leito",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Queda lenta antes dos 10 segundos."
                    },
                    {
                        "id": "opt_nihss_5a_2",
                        "label": "2: Toca o leito antes de 10s, mas vence a gravidade",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "Apresenta esforço contra a gravidade antes de cair."
                    },
                    {
                        "id": "opt_nihss_5a_3",
                        "label": "3: Queda imediata, não vence gravidade (move no plano)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Movimenta apenas no plano do leito sem elevar o membro."
                    },
                    {
                        "id": "opt_nihss_5a_4",
                        "label": "4: Paralisia completa (nenhum movimento muscular voluntário)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Plegia completa do membro superior esquerdo."
                    },
                    {
                        "id": "opt_nihss_5a_un",
                        "label": "UN: Amputação ou fusão articular (0 pts sem penalização)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 6,
                        "description": "Membro não testável por amputação ou anquilose."
                    }
                ]
            },
            {
                "id": "grp_nihss_5b",
                "name": "5b. Motricidade Braço Direito (MSD)",
                "slug": "nihss-5b-msd",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "helpText": "Manter membro estendido a 90° (sentado) ou 45° (supino) por 10 segundos.",
                "options": [
                    {
                        "id": "opt_nihss_5b_0",
                        "label": "0: Sem queda por 10 segundos completos",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sustenta o braço sem declínio por 10s."
                    },
                    {
                        "id": "opt_nihss_5b_1",
                        "label": "1: Queda antes de 10s, mas não toca o leito",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Queda lenta antes dos 10 segundos."
                    },
                    {
                        "id": "opt_nihss_5b_2",
                        "label": "2: Toca o leito antes de 10s, mas vence a gravidade",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "Apresenta esforço contra a gravidade antes de cair."
                    },
                    {
                        "id": "opt_nihss_5b_3",
                        "label": "3: Queda imediata, não vence gravidade (move no plano)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Movimenta apenas no plano do leito sem elevar o membro."
                    },
                    {
                        "id": "opt_nihss_5b_4",
                        "label": "4: Paralisia completa (nenhum movimento muscular voluntário)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Plegia completa do membro superior direito."
                    },
                    {
                        "id": "opt_nihss_5b_un",
                        "label": "UN: Amputação ou fusão articular (0 pts sem penalização)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 6,
                        "description": "Membro não testável por amputação ou anquilose."
                    }
                ]
            },
            {
                "id": "grp_nihss_6a",
                "name": "6a. Motricidade Perna Esquerda (MIE)",
                "slug": "nihss-6a-mie",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 9,
                "helpText": "Manter perna estendida a 30° em decúbito dorsal por 5 segundos.",
                "options": [
                    {
                        "id": "opt_nihss_6a_0",
                        "label": "0: Sem queda por 5 segundos completos",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sustenta a perna a 30° por 5s."
                    },
                    {
                        "id": "opt_nihss_6a_1",
                        "label": "1: Queda antes de 5s, mas não toca a cama",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Queda lenta sem tocar o leito."
                    },
                    {
                        "id": "opt_nihss_6a_2",
                        "label": "2: Toca a cama antes de 5s, mas vence a gravidade",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "Esforço contra gravidade com queda rápida."
                    },
                    {
                        "id": "opt_nihss_6a_3",
                        "label": "3: Queda imediata ao leito, não vence gravidade (move no plano)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Move apenas artelhos ou coxa no plano da cama."
                    },
                    {
                        "id": "opt_nihss_6a_4",
                        "label": "4: Paralisia completa (nenhuma movimentação voluntária)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Plegia completa da perna esquerda."
                    },
                    {
                        "id": "opt_nihss_6a_un",
                        "label": "UN: Amputação ou fusão articular (0 pts sem penalização)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 6,
                        "description": "Membro não testável por amputação ou anquilose."
                    }
                ]
            },
            {
                "id": "grp_nihss_6b",
                "name": "6b. Motricidade Perna Direita (MID)",
                "slug": "nihss-6b-mid",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 10,
                "helpText": "Manter perna estendida a 30° em decúbito dorsal por 5 segundos.",
                "options": [
                    {
                        "id": "opt_nihss_6b_0",
                        "label": "0: Sem queda por 5 segundos completos",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sustenta a perna a 30° por 5s."
                    },
                    {
                        "id": "opt_nihss_6b_1",
                        "label": "1: Queda antes de 5s, mas não toca a cama",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.25,
                        "sortOrder": 2,
                        "description": "Queda lenta sem tocar o leito."
                    },
                    {
                        "id": "opt_nihss_6b_2",
                        "label": "2: Toca a cama antes de 5s, mas vence a gravidade",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 3,
                        "description": "Esforço contra gravidade com queda rápida."
                    },
                    {
                        "id": "opt_nihss_6b_3",
                        "label": "3: Queda imediata ao leito, não vence gravidade (move no plano)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.75,
                        "sortOrder": 4,
                        "description": "Move apenas artelhos ou coxa no plano da cama."
                    },
                    {
                        "id": "opt_nihss_6b_4",
                        "label": "4: Paralisia completa (nenhuma movimentação voluntária)",
                        "pointValue": 4,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 5,
                        "description": "Plegia completa da perna direita."
                    },
                    {
                        "id": "opt_nihss_6b_un",
                        "label": "UN: Amputação ou fusão articular (0 pts sem penalização)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 6,
                        "description": "Membro não testável por amputação ou anquilose."
                    }
                ]
            },
            {
                "id": "grp_nihss_7",
                "name": "7. Ataxia Apendicular (Index-nariz e Calcanhar-joelho)",
                "slug": "nihss-7-ataxia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_motor",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 11,
                "helpText": "Ataxia deve estar fora de proporção em relação à fraqueza motora.",
                "options": [
                    {
                        "id": "opt_nihss_7_0",
                        "label": "0: Ausente (movimentos coordenados bilaterais)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Coordenação apendicular perfeita."
                    },
                    {
                        "id": "opt_nihss_7_1",
                        "label": "1: Presente em um membro (dismetria desproporcional à fraqueza)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Dismetria cerebelar em um membro."
                    },
                    {
                        "id": "opt_nihss_7_2",
                        "label": "2: Presente em dois ou mais membros",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Ataxia apendicular em múltiplos membros."
                    }
                ]
            },
            {
                "id": "grp_nihss_8",
                "name": "8. Sensibilidade (Picada de Agulha)",
                "slug": "nihss-8-sensibilidade",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_sensory_neglect",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 12,
                "helpText": "Testar com estímulo tátil doloroso em face, tronco e 4 membros.",
                "options": [
                    {
                        "id": "opt_nihss_8_0",
                        "label": "0: Normal (sensibilidade simétrica e preservada)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sensibilidade dolorosa normal e simétrica."
                    },
                    {
                        "id": "opt_nihss_8_1",
                        "label": "1: Perda sensitiva leve a moderada (sensação embotada)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Sente a picada menos nítida no hemicorpo afetado."
                    },
                    {
                        "id": "opt_nihss_8_2",
                        "label": "2: Perda sensitiva grave ou anestesia completa",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Não percebe estímulo nociceptivo no hemicorpo."
                    }
                ]
            },
            {
                "id": "grp_nihss_9",
                "name": "9. Melhor Linguagem (Figuras, Cena e Leitura)",
                "slug": "nihss-9-linguagem",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_language",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 13,
                "helpText": "Avaliação de compreensão, nomeação e fluência.",
                "options": [
                    {
                        "id": "opt_nihss_9_0",
                        "label": "0: Sem afasia (fluência, nomeação e compreensão normais)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Linguagem perfeitamente normal."
                    },
                    {
                        "id": "opt_nihss_9_1",
                        "label": "1: Afasia leve a moderada (redução de fluência, mas comunica)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.33,
                        "sortOrder": 2,
                        "description": "Compreensão ou expressão alteradas, porém consegue comunicar ideias."
                    },
                    {
                        "id": "opt_nihss_9_2",
                        "label": "2: Afasia grave (afasia densa de Broca ou Wernicke, comunicação mínima)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.66,
                        "sortOrder": 3,
                        "description": "Comunicação fragmentária e mínima pelo examinador."
                    },
                    {
                        "id": "opt_nihss_9_3",
                        "label": "3: Mudo ou afasia global completa (sem emissão verbal compreensível)",
                        "pointValue": 3,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 4,
                        "description": "Incapacidade total de expressão ou compreensão verbal."
                    }
                ]
            },
            {
                "id": "grp_nihss_10",
                "name": "10. Disartria (Leitura de Palavras Padronizadas)",
                "slug": "nihss-10-disartria",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_language",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 14,
                "helpText": "Articulação das palavras na repetição de vocábulos.",
                "options": [
                    {
                        "id": "opt_nihss_10_0",
                        "label": "0: Articulação normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Fala clara e bem articulada."
                    },
                    {
                        "id": "opt_nihss_10_1",
                        "label": "1: Disartria leve a moderada (fala pastosa/arrastada, mas compreensível)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Fala arrastada, porém compreensível."
                    },
                    {
                        "id": "opt_nihss_10_2",
                        "label": "2: Disartria grave (fala ininteligível ou anartria total)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Fala ininteligível ou incapacidade de produzir fonação."
                    },
                    {
                        "id": "opt_nihss_10_un",
                        "label": "UN: Paciente intubado ou barreira física mecânica (0 pts)",
                        "pointValue": 0,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 4,
                        "description": "Não testável por intubação endotraqueal."
                    }
                ]
            },
            {
                "id": "grp_nihss_11",
                "name": "11. Extinção e Desatenção (Negligência Espacial/Sensorial)",
                "slug": "nihss-11-negligencia",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_nihss_sensory_neglect",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 15,
                "helpText": "Estímulo simultâneo bilateral tátil e visual.",
                "options": [
                    {
                        "id": "opt_nihss_11_0",
                        "label": "0: Sem negligência (reconhece estímulos simultâneos bilaterais)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Atenção íntegra para ambos os hemicorpos."
                    },
                    {
                        "id": "opt_nihss_11_1",
                        "label": "1: Inatenção em uma modalidade sensorial (visual, tátil ou espacial)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Extingue estímulo bilateral em uma modalidade sensorial."
                    },
                    {
                        "id": "opt_nihss_11_2",
                        "label": "2: Hemi-inatenção profunda em mais de uma modalidade (ignora hemicorpo)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Negligência hemiespacial grave em múltiplas modalidades."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_nihss_zero",
                "label": "Sem Déficit Mensurável (0 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Ausência de déficit objetivo mensurável pelo NIHSS. Investigar ativamente mimetismos de AVC (stroke mimics - crise focal, enxaqueca com aura, hipoglicemia).",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_nihss_mimic",
                        "drugName": "Investigação Etiológica e Sintomáticos",
                        "dosage": "Individualizada conforme diagnóstico de stroke mimic",
                        "route": "VO ou IV",
                        "frequency": "Conforme necessidade",
                        "contraindications": "Trombólise endovenosa não indicada se ausência de déficit funcional incapacitante."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_nihss_zero_obs",
                        "recommendationTitle": "Vigilância Clínica e Neuroimagem",
                        "dispositionTarget": "Observação / Unidade de AVC",
                        "monitoringPlan": "Glicemia capilar imediata, TC de crânio e monitorização horária."
                    }
                ]
            },
            {
                "id": "tier_nihss_minor",
                "label": "AVC Leve / Menor (1 a 4 pontos)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 4,
                "statisticalOutcome": "Mortalidade em 30 dias < 3%. Até 15% evoluem com dependência funcional caso o déficit seja incapacitante (ex.: afasia ou hemianopsia).",
                "colorHex": "#34d399",
                "pharmacologicalActions": [
                    {
                        "id": "rx_nihss_dapt",
                        "drugName": "Dupla Antiagregação Plaquetária (DAPT CHANCE/POINT) se NIHSS <= 3",
                        "dosage": "AAS 160-300 mg ataque VO + Clopidogrel 300 mg ataque VO, seguido de AAS 100 mg + Clopidogrel 75 mg/dia por 21 dias contínuos",
                        "route": "Via Oral",
                        "frequency": "Diária",
                        "contraindications": "Não utilizar DAPT se trombólise IV realizada nas últimas 24h."
                    },
                    {
                        "id": "rx_nihss_lysis_disabling",
                        "drugName": "Alteplase (ou Tenecteplase) se Déficit Incapacitante e Delta T <= 4,5h",
                        "dosage": "Alteplase 0,9 mg/kg IV (máx 90 mg; 10% em bolus de 1 min, 90% em 60 min) OU Tenecteplase 0,25 mg/kg IV bolus único (máx 25 mg)",
                        "route": "Intravenosa",
                        "frequency": "Dose única",
                        "dilutionInstructions": "Manter PA estritamente < 185/110 mmHg pré-lise e < 180/105 mmHg pós-lise.",
                        "contraindications": "Hemorragia ativa, plaquetas < 100.000, RNI > 1,7 ou uso de DOAC nas últimas 48h."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_nihss_minor_unit",
                        "recommendationTitle": "Admissão em Unidade de AVC / Telemetria",
                        "dispositionTarget": "Unidade de AVC",
                        "monitoringPlan": "Angio-TC de vasos cerebrais e cervicais de urgência para pesquisar estenose de grande vaso."
                    }
                ]
            },
            {
                "id": "tier_nihss_mod",
                "label": "AVC Moderado (5 a 15 pontos)",
                "severityLevel": "intermediate",
                "minScore": 5,
                "maxScore": 15,
                "statisticalOutcome": "Elevadíssimo risco de Oclusão de Grande Vaso proximal (LVO > 60-80% se NIHSS >= 6). Dependência funcional > 50% sem recanalização mecânica rápida.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_nihss_thrombolysis_full",
                        "drugName": "Alteplase 0,9 mg/kg IV (ou Tenecteplase 0,25 mg/kg IV bolus)",
                        "dosage": "Alteplase 0,9 mg/kg IV (10% bolus em 1 min, 90% em 60 min; máx 90 mg) ou Tenecteplase 0,25 mg/kg bolus em 5-10s (máx 25 mg)",
                        "route": "Intravenosa",
                        "frequency": "Dose única de emergência (Janela <= 4,5h)",
                        "dilutionInstructions": "Proibido qualquer antiagregante ou anticoagulante nas primeiras 24 horas pós-trombolítico.",
                        "contraindications": "PA persistente >= 185/110 mmHg apesar de anti-hipertensivos IV."
                    },
                    {
                        "id": "rx_nihss_bp_control",
                        "drugName": "Nitroprussiato de Sódio (ou Esmolol) para Controle Pressórico Estrito",
                        "dosage": "0,25 a 10 mcg/kg/min IV contínua para manter PA < 185/110 mmHg",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "dilutionInstructions": "1 ampola (50 mg) em 248 mL SG 5% com fotoproteção."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_nihss_evts",
                        "recommendationTitle": "Triagem Imediata para Trombectomia Mecânica (TM)",
                        "dispositionTarget": "Sala de Hemodinâmica / UTI Neurocrítica",
                        "monitoringPlan": "Acionar código AVC de emergência (tempo porta-agulha < 45-60 min e porta-virilha < 90-120 min).",
                        "interventionalProcedure": "Trombectomia Mecânica endovascular imediata (janela até 6h na rotina; 6 a 24h em janela estendida guiada por neuroimagem nos ensaios DAWN e DEFUSE-3).",
                        "ventilatorySupport": "Manter cabeceira reta a 0° até recanalização para maximizar fluxo colateral se tolerado sem broncoaspiração."
                    }
                ]
            },
            {
                "id": "tier_nihss_mod_sev",
                "label": "AVC Moderado-Grave (16 a 20 pontos)",
                "severityLevel": "high",
                "minScore": 16,
                "maxScore": 20,
                "statisticalOutcome": "Oclusão de tronco da ACM ou artéria carótida interna em > 85% dos casos. Alto risco de deterioração neurológica por edema citotóxico progressivo.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    {
                        "id": "rx_nihss_mod_sev_rx",
                        "drugName": "Trombólise Endovenosa (se <= 4,5h) + Manejo Pressórico",
                        "dosage": "Tenecteplase 0,25 mg/kg ou Alteplase 0,9 mg/kg IV",
                        "route": "Intravenosa",
                        "frequency": "Dose única"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_nihss_mod_sev_evts",
                        "recommendationTitle": "Trombectomia Mecânica de Emergência e Vaga em UTI",
                        "dispositionTarget": "Hemodinâmica / UTI Neurocrítica",
                        "monitoringPlan": "Vigilância horária do NIHSS para detectar deterioração precoce.",
                        "interventionalProcedure": "Trombectomia Mecânica urgente; avaliação precoce de risco de infarto maligno de ACM."
                    }
                ]
            },
            {
                "id": "tier_nihss_severe",
                "label": "AVC Grave / Gravíssimo (21 a 42 pontos)",
                "severityLevel": "critical",
                "minScore": 21,
                "maxScore": 42,
                "statisticalOutcome": "Mortalidade em 30 dias de 40% a 60%. Altíssimo risco de edema cerebral maligno de ACM com desvio de linha média e herniação uncal.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_nihss_osmotherapy",
                        "drugName": "Solução Salina Hipertônica 3% (ou Manitol 20%)",
                        "dosage": "150 a 250 mL IV bolus em 15 minutos se deterioração por hipertensão intracraniana ou herniação uncal",
                        "route": "Intravenosa",
                        "frequency": "Sob demanda",
                        "dilutionInstructions": "Preparo 3% em acesso calibroso."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_nihss_craniectomy",
                        "recommendationTitle": "Craniectomia Descompressiva Hemisférica Precoce (< 48h)",
                        "dispositionTarget": "Centro Cirúrgico de Urgência / UTI Neurocrítica",
                        "monitoringPlan": "Intubação orotraqueal e ventilação mecânica protetora (PaCO2 35-40 mmHg).",
                        "interventionalProcedure": "Avaliação neurocirúrgica urgente para Craniectomia Hemidescompressiva Fronto-têmporo-parietal ampla (diâmetro >= 12 a 15 cm com duroplastia de ampliação) em pacientes com idade < 60 anos nas primeiras 48 horas do início dos sintomas para prevenir herniação fatal (ensaios DECIMAL, DESTINY e HAMLET)."
                    }
                ]
            }
        ]
    }

def get_aspects():
    return {
        "id": "calc_aspects",
        "slug": "aspects",
        "name": "Alberta Stroke Program Early CT Score (ASPECTS)",
        "acronym": "ASPECTS",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neuroimagem Vascular / AVC Agudo de ACM",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Doença Cerebrovascular e AVC Agudo",
        "description": "Sistema topográfico quantitativo em TC de crânio sem contraste que subtrai pontos de uma pontuação basal de 10 para cada uma das 10 zonas da ACM com hipoatenuação isquêmica precoce.",
        "summary": "Escore tomográfico topográfico (0 a 10 pontos) avaliando 10 zonas da artéria cerebral média para seleção de trombectomia mecânica.",
        "clinicalObjective": "Quantificar a extensão precoce do núcleo isquêmico irreversível no território da artéria cerebral média (ACM) para indicação de Trombectomia Mecânica.",
        "targetPopulation": "Adultos com AVC isquêmico agudo no território da ACM em janela de reperfusão (0 a 24 horas).",
        "calculationType": "additive_points",
        "formulaExpression": "10 (baseScore) - Soma_de_regioes_com_isquemia_precoce",
        "evidenceSource": "Barber PA, Demchuk AM, Zhang J, Buchan AM. Validity and reliability of a quantitative computed tomography score in predicting outcome of hyperacute stroke patients. Lancet. 2000;355(9216):1670-1674. SELECT2 Trial. N Engl J Med. 2023;388(14):1253-1263.",
        "minPossibleScore": 0,
        "maxPossibleScore": 10,
        "baseScore": 10,
        "badge": "neuroimagem",
        "clinicalWarning": "AJUSTE MANDATÓRIO DE JANELA ('STROKE WINDOW'): A TC de crânio sem contraste DEVE ser avaliada em janela de contraste estreita (largura de 40 HU e nível central de 40 HU) para detectar hipodensidades precoces sutis e apagamento córtico-subcortical. O ASPECTS aplica-se exclusivamente ao território da ACM. Ensaios clínicos randomizados modernos (SELECT2, ANGEL-ASPECT, TENSION em 2023) comprovaram benefício da Trombectomia Mecânica mesmo em pacientes selecionados com ASPECTS 3 a 5 (grande core).",
        "radarAxes": [
            {
                "id": "axis_aspects_deep",
                "label": "Núcleos da Base e Cápsula",
                "system": "Imagem",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_aspects_cortex_inf",
                "label": "Córtex Inferior (M1-M3, Ínsula)",
                "system": "Imagem",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_aspects_cortex_sup",
                "label": "Córtex Superior (M4-M6)",
                "system": "Imagem",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_aspects_c",
                "name": "C - Núcleo Caudado",
                "slug": "aspects-caudado",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_deep",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Avaliação de hipodensidade na cabeça do núcleo caudado.",
                "options": [
                    {
                        "id": "opt_aspects_c_normal",
                        "label": "Normal (Sem isquemia precoce)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Atenuação tomográfica normal da cabeça do caudado."
                    },
                    {
                        "id": "opt_aspects_c_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Perda de atenuação ou hipodensidade precoce no caudado."
                    }
                ]
            },
            {
                "id": "grp_aspects_l",
                "name": "L - Núcleo Lenticular (Putâmen / Globo Pálido)",
                "slug": "aspects-lenticular",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_deep",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Apagamento precoce do núcleo lenticular.",
                "options": [
                    {
                        "id": "opt_aspects_l_normal",
                        "label": "Normal (Sem isquemia precoce)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Atenuação preservada do putâmen e globo pálido."
                    },
                    {
                        "id": "opt_aspects_l_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Apagamento lenticular precoce."
                    }
                ]
            },
            {
                "id": "grp_aspects_ic",
                "name": "IC - Cápsula Interna (Braço Posterior)",
                "slug": "aspects-capsula-interna",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_deep",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Apagamento do braço posterior da cápsula interna.",
                "options": [
                    {
                        "id": "opt_aspects_ic_normal",
                        "label": "Normal (Sem isquemia precoce)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Cápsula interna com sinal normal."
                    },
                    {
                        "id": "opt_aspects_ic_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade do braço posterior da cápsula interna."
                    }
                ]
            },
            {
                "id": "grp_aspects_i",
                "name": "I - Fita Insular (Córtex Insular)",
                "slug": "aspects-insula",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_inf",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Perda da diferenciação córtico-subcortical na ínsula ('sinal da fita insular').",
                "options": [
                    {
                        "id": "opt_aspects_i_normal",
                        "label": "Normal (Sem isquemia precoce)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Fita insular nítida e preservada."
                    },
                    {
                        "id": "opt_aspects_i_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Apagamento da fita insular córtico-subcortical."
                    }
                ]
            },
            {
                "id": "grp_aspects_m1",
                "name": "M1 - Córtex ACM Anterior (Opérculo Frontal)",
                "slug": "aspects-m1",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_inf",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Córtex da ACM no corte ganglionar anterior.",
                "options": [
                    {
                        "id": "opt_aspects_m1_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M1 normal."
                    },
                    {
                        "id": "opt_aspects_m1_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M1."
                    }
                ]
            },
            {
                "id": "grp_aspects_m2",
                "name": "M2 - Córtex ACM Lateral (Lobo Temporal Anterior)",
                "slug": "aspects-m2",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_inf",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 6,
                "helpText": "Córtex da ACM no corte ganglionar lateral adjacente à ínsula.",
                "options": [
                    {
                        "id": "opt_aspects_m2_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M2 normal."
                    },
                    {
                        "id": "opt_aspects_m2_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M2."
                    }
                ]
            },
            {
                "id": "grp_aspects_m3",
                "name": "M3 - Córtex ACM Posterior (Lobo Temporal Posterior)",
                "slug": "aspects-m3",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_inf",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 7,
                "helpText": "Córtex da ACM no corte ganglionar posterior.",
                "options": [
                    {
                        "id": "opt_aspects_m3_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M3 normal."
                    },
                    {
                        "id": "opt_aspects_m3_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M3."
                    }
                ]
            },
            {
                "id": "grp_aspects_m4",
                "name": "M4 - Córtex ACM Anterior Superior",
                "slug": "aspects-m4",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_sup",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 8,
                "helpText": "Nível supraganglionar anterior (acima dos ventrículos).",
                "options": [
                    {
                        "id": "opt_aspects_m4_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M4 normal."
                    },
                    {
                        "id": "opt_aspects_m4_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M4."
                    }
                ]
            },
            {
                "id": "grp_aspects_m5",
                "name": "M5 - Córtex ACM Lateral Superior",
                "slug": "aspects-m5",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_sup",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 9,
                "helpText": "Nível supraganglionar lateral.",
                "options": [
                    {
                        "id": "opt_aspects_m5_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M5 normal."
                    },
                    {
                        "id": "opt_aspects_m5_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M5."
                    }
                ]
            },
            {
                "id": "grp_aspects_m6",
                "name": "M6 - Córtex ACM Posterior Superior",
                "slug": "aspects-m6",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_aspects_cortex_sup",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 10,
                "helpText": "Nível supraganglionar posterior.",
                "options": [
                    {
                        "id": "opt_aspects_m6_normal",
                        "label": "Normal",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Região M6 normal."
                    },
                    {
                        "id": "opt_aspects_m6_affected",
                        "label": "Isquêmico / Hipoatenuado (-1 ponto)",
                        "pointValue": -1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipodensidade precoce em M6."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_aspects_large_core",
                "label": "Core Isquêmico Extenso (ASPECTS 0 a 5)",
                "severityLevel": "critical",
                "minScore": 0,
                "maxScore": 5,
                "statisticalOutcome": "Infarto volumoso (core >= 70-100 mL). Alto risco de edema cerebral maligno, transformação hemorrágica sintomática (PH2) e mortalidade > 40%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_aspects_contraind_lysis",
                        "drugName": "Contraindicação Formal de Trombólise Endovenosa (se > 1/3 da ACM)",
                        "dosage": "Trombólise química formalmente contraindicada por risco hemorrágico fatal",
                        "route": "Não aplicável",
                        "frequency": "Não aplicável",
                        "contraindications": "Alteplase ou Tenecteplase contraindicadas se hipodensidade franca > 1/3 do território da ACM."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_aspects_large_core_tm",
                        "recommendationTitle": "Trombectomia Mecânica em Grande Core (SELECT2 / ANGEL-ASPECT)",
                        "dispositionTarget": "Hemodinâmica / UTI Neurocrítica",
                        "monitoringPlan": "Ensaios clínicos modernos demonstraram melhora funcional relevante com Trombectomia Mecânica em pacientes selecionados com ASPECTS 3 a 5 vs tratamento clínico isolado.",
                        "interventionalProcedure": "Trombectomia mecânica urgente em centros com capacidade neurocirúrgica imediata; vigilância de edema maligno para craniectomia hemidescompressiva."
                    }
                ]
            },
            {
                "id": "tier_aspects_moderate",
                "label": "Core Moderado / Elegibilidade Padrão de Diretriz (ASPECTS 6 a 7)",
                "severityLevel": "intermediate",
                "minScore": 6,
                "maxScore": 7,
                "statisticalOutcome": "Excelente resposta terapêutica à recanalização mecânica com expressiva redução de morbidade e dependência funcional.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_aspects_mod_lysis",
                        "drugName": "Trombólise Endovenosa se Janela <= 4,5h",
                        "dosage": "Tenecteplase 0,25 mg/kg IV bolus ou Alteplase 0,9 mg/kg IV",
                        "route": "Intravenosa",
                        "frequency": "Dose única"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_aspects_mod_tm",
                        "recommendationTitle": "Indicação Formal Classe IA de Trombectomia Mecânica",
                        "dispositionTarget": "Sala de Hemodinâmica",
                        "monitoringPlan": "Monitorização hemodinâmica contínua (manter PAS >= 140 mmHg enquanto artéria ocluída para perfusão colateral).",
                        "interventionalProcedure": "Trombectomia mecânica por aspiração e/ou stent retriever."
                    }
                ]
            },
            {
                "id": "tier_aspects_small_core",
                "label": "Core Pequeno / Infarto Restrito (ASPECTS 8 a 10)",
                "severityLevel": "low",
                "minScore": 8,
                "maxScore": 10,
                "statisticalOutcome": "Independência funcional aos 90 dias (mRS 0-2) superior a 55-65% após recanalização completa (TICI 2b-3). Risco hemorrágico muito baixo.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_aspects_small_lysis",
                        "drugName": "Trombólise Química Imediata se Delta T <= 4,5h",
                        "dosage": "Tenecteplase 0,25 mg/kg ou Alteplase 0,9 mg/kg IV",
                        "route": "Intravenosa",
                        "frequency": "Dose única"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_aspects_small_tm",
                        "recommendationTitle": "Trombectomia Mecânica de Emergência (Janela até 24h)",
                        "dispositionTarget": "Hemodinâmica / UTI Neurocrítica",
                        "monitoringPlan": "Angio-TC de emergência para documentar oclusão proximal de ACM ou carótida.",
                        "interventionalProcedure": "Trombectomia mecânica imediata."
                    }
                ]
            }
        ]
    }

def get_ich_score():
    return {
        "id": "calc_ich_score",
        "slug": "ich-score",
        "name": "The Intracerebral Hemorrhage (ICH) Score",
        "acronym": "ICH Score",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurologia Vascular e Neurointensivismo / Hemorragia Intracraniana",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Hemorragia Intracraniana Espontânea",
        "description": "Escore de 0 a 6 pontos para estratificação prognóstica e predição de mortalidade em 30 dias em pacientes admitidos com Hemorragia Intracerebral (HIC) espontânea primária parenquimatosa.",
        "summary": "Escore prognóstico de 0 a 6 pontos preditor de mortalidade em 30 dias na hemorragia intracerebral espontânea primária.",
        "clinicalObjective": "Estratificação da gravidade na admissão da HIC espontânea primária baseada em Glasgow, volume do hematoma (ABC/2), hemoventrículo, topografia infratentorial e idade.",
        "targetPopulation": "Adultos admitidos na emergência com HIC espontânea primária (hipertensiva ou angiopatia amiloide) diagnosticada por TC.",
        "calculationType": "additive_points",
        "formulaExpression": "GCS_pontos + Volume_pontos + IVH_pontos + Infratentorial_pontos + Idade_pontos",
        "evidenceSource": "Hemphill JC 3rd, Bonovich DC, Besmertis L, et al. The ICH score: a simple, reliable grading scale for intracerebral hemorrhage. Stroke. 2001;32(4):891-897. AHA/ASA ICH Guidelines 2022.",
        "minPossibleScore": 0,
        "maxPossibleScore": 6,
        "baseScore": 0,
        "badge": "neurovascular",
        "clinicalWarning": "AVISO BIOÉTICO MANDATÓRIO (DIRETRIZ AHA/ASA 2022 - CONTRA A PROFECIA AUTORREALIZÁVEL): O ICH Score NÃO deve ser utilizado de forma isolada para justificar ordens precoces de não-reanimação (DNR) ou limitação de suporte vital nas primeiras 24 a 48 horas da admissão. Tratamento médico intensivo agressivo inicial deve ser mantido, exceto diante de diretivas antecipadas de vontade documentadas previamente ou confirmação de morte encefálica.",
        "radarAxes": [
            {
                "id": "axis_ich_gcs",
                "label": "Nível de Consciência (Glasgow)",
                "system": "Neurológico",
                "unit": "GCS",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_ich_volume",
                "label": "Volume do Hematoma (cm³)",
                "system": "Imagem",
                "unit": "cm³",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_ich_ivh",
                "label": "Hemorragia Intraventricular",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_ich_infratentorial",
                "label": "Origem Infratentorial",
                "system": "Imagem",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_ich_age",
                "label": "Idade >= 80 Anos",
                "system": "Demográfico",
                "unit": "anos",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_ich_gcs",
                "name": "Escala de Coma de Glasgow na Admissão",
                "slug": "ich-glasgow",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_ich_gcs",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Pontuação total do Glasgow pré-intubação/sedação.",
                "options": [
                    {
                        "id": "opt_ich_gcs_13_15",
                        "label": "Glasgow 13 a 15 (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Consciência alerta ou confusão leve."
                    },
                    {
                        "id": "opt_ich_gcs_5_12",
                        "label": "Glasgow 5 a 12 (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Sonolência profunda, estupor ou torpor."
                    },
                    {
                        "id": "opt_ich_gcs_3_4",
                        "label": "Glasgow 3 a 4 (2 pontos)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Coma profundo ou postura patológica."
                    }
                ]
            },
            {
                "id": "grp_ich_volume",
                "name": "Volume do Hematoma Intracerebral (Método ABC/2)",
                "slug": "ich-volume",
                "inputType": "single_choice",
                "unit": "cm³",
                "radarAxisId": "axis_ich_volume",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "Fórmula ABC/2: (A x B x C) / 2 em cm³.",
                "options": [
                    {
                        "id": "opt_ich_vol_lt30",
                        "label": "Volume < 30 cm³ (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Hematoma pequeno ou médio (< 30 mL)."
                    },
                    {
                        "id": "opt_ich_vol_ge30",
                        "label": "Volume >= 30 cm³ (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hematoma volumoso com importante efeito de massa (>= 30 mL)."
                    }
                ]
            },
            {
                "id": "grp_ich_ivh",
                "name": "Hemorragia Intraventricular (HIV / IVH)",
                "slug": "ich-hemoventriculo",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_ich_ivh",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Extensão do sangramento para os ventrículos.",
                "options": [
                    {
                        "id": "opt_ich_ivh_no",
                        "label": "Ausente (Sem sangue intraventricular) (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Ventrículos livres de sangue."
                    },
                    {
                        "id": "opt_ich_ivh_yes",
                        "label": "Presente (Qualquer extensão para os ventrículos) (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Presença de nível de sangue ou inundação ventricular."
                    }
                ]
            },
            {
                "id": "grp_ich_infratentorial",
                "name": "Localização do Hematoma",
                "slug": "ich-localizacao",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_ich_infratentorial",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Topografia supratentorial versus infratentorial.",
                "options": [
                    {
                        "id": "opt_ich_infra_no",
                        "label": "Supratentorial (Lobar, núcleos da base, tálamo) (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Hematoma localizado nos hemisférios cerebrais."
                    },
                    {
                        "id": "opt_ich_infra_yes",
                        "label": "Infratentorial (Tronco encefálico ou cerebelo) (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hematoma em fossa posterior (ponte, mesencéfalo ou cerebelo)."
                    }
                ]
            },
            {
                "id": "grp_ich_age",
                "name": "Idade do Paciente",
                "slug": "ich-idade",
                "inputType": "single_choice",
                "unit": "anos",
                "radarAxisId": "axis_ich_age",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "Ponto de corte de 80 anos.",
                "options": [
                    {
                        "id": "opt_ich_age_lt80",
                        "label": "Idade < 80 anos (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Menor de 80 anos."
                    },
                    {
                        "id": "opt_ich_age_ge80",
                        "label": "Idade >= 80 anos (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Idoso com 80 anos ou mais."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_ich_0",
                "label": "ICH Score 0 (Baixo Risco)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 0,
                "statisticalOutcome": "Mortalidade estimada em 30 dias de 0%. Baixíssimo risco de evolução fatal.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich_bp",
                        "drugName": "Controle Pressórico Emergencial (Meta PAS 130 a 140 mmHg)",
                        "dosage": "Nitroprussiato de Sódio 0,25 a 5 mcg/kg/min IV contínua ou Esmolol em BIC (ensaios INTERACT-2 e ATACH-2)",
                        "route": "Intravenosa contínua em BIC",
                        "frequency": "Contínua",
                        "contraindications": "Evitar reduções bruscas para PAS < 120 mmHg."
                    },
                    {
                        "id": "rx_ich_reversal",
                        "drugName": "Reversão Imediata de Anticoagulantes (se aplicável)",
                        "dosage": "Varfarina: Complexo Protrombínico 4 Fatores (CCP4F) 25 a 50 UI/kg IV + Fitomenadiona 10 mg IV. Dabigatrana: Idarucizumabe 5 g IV (2 frascos de 2,5 g). Inibidores Xa: Andexanet alfa ou CCP4F 50 UI/kg IV.",
                        "route": "Intravenosa",
                        "frequency": "Dose única de emergência"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich_unit",
                        "recommendationTitle": "Internação em UTI Neurológica e TC de Controle",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Monitorização hemodinâmica contínua e TC de crânio de controle em 24 horas para pesquisar expansão do hematoma."
                    }
                ]
            },
            {
                "id": "tier_ich_1",
                "label": "ICH Score 1 (Risco Leve a Moderado)",
                "severityLevel": "low",
                "minScore": 1,
                "maxScore": 1,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em 13%. Bom potencial de sobrevida funcional.",
                "colorHex": "#34d399",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich1_bp",
                        "drugName": "Nitroprussiato de Sódio (Meta PAS 130-140 mmHg)",
                        "dosage": "0,25 a 5 mcg/kg/min IV",
                        "route": "Intravenosa",
                        "frequency": "Contínua em BIC"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich1_icu",
                        "recommendationTitle": "Leito de UTI Neurocrítica",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Vigilância neurológica horária."
                    }
                ]
            },
            {
                "id": "tier_ich_2",
                "label": "ICH Score 2 (Risco Moderado)",
                "severityLevel": "intermediate",
                "minScore": 2,
                "maxScore": 2,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em 26%.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich2_saline",
                        "drugName": "Solução Salina Hipertônica 3% (ou Manitol 20%)",
                        "dosage": "150 a 250 mL IV bolus em 15 minutos para elevação de PIC",
                        "route": "Intravenosa",
                        "frequency": "Sob demanda"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich2_surg",
                        "recommendationTitle": "Avaliação Cirúrgica Urgente (DVE e Descompressão Fossa Posterior)",
                        "dispositionTarget": "UTI Neurocrítica / Centro Cirúrgico",
                        "monitoringPlan": "Passagem de DVE se hidrocefalia associada.",
                        "interventionalProcedure": "Se hematoma cerebelar > 3 cm com compressão de tronco ou hidrocefalia: indicação formal Classe I de Craniectomia Suboccipital e evacuação imediata."
                    }
                ]
            },
            {
                "id": "tier_ich_3",
                "label": "ICH Score 3 (Alto Risco)",
                "severityLevel": "high",
                "minScore": 3,
                "maxScore": 3,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em 72%.",
                "colorHex": "#f97316",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich3_norepi",
                        "drugName": "Noradrenalina IV se Necessidade de Sustentação Pressórica",
                        "dosage": "Titular para manter PPC >= 60-70 mmHg",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua em BIC",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich3_airway",
                        "recommendationTitle": "Proteção de Via Aérea, DVE e Cuidado Intensivo Pleno",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "IOT e ventilação mecânica se GCS <= 8.",
                        "interventionalProcedure": "DVE de emergência e consideração de evacuação cirúrgica ou aspiração minimamente invasiva."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_ich_4",
                "label": "ICH Score 4 (Muito Alto Risco)",
                "severityLevel": "critical",
                "minScore": 4,
                "maxScore": 4,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em 97%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich4_icu",
                        "drugName": "Suporte Intensivo Neuroprotetor Agressivo",
                        "dosage": "Manejo hemodinâmico e osmoterapia sob demanda",
                        "route": "Intravenosa",
                        "frequency": "Contínua",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich4_ethics",
                        "recommendationTitle": "Manutenção Mandatória de Suporte Vital (Aviso Bioético)",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Diretrizes AHA 2022 proíbem limitação precoce de cuidados nas primeiras 24-48 horas. Manter tratamento agressivo pleno."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            },
            {
                "id": "tier_ich_5_6",
                "label": "ICH Score 5 a 6 (Risco Crítico / Extremo)",
                "severityLevel": "critical",
                "minScore": 5,
                "maxScore": 6,
                "statisticalOutcome": "Mortalidade em 30 dias estimada em 100% nas coortes de validação históricas. Manter suporte intensivo inicial.",
                "colorHex": "#991b1b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_ich56_icu",
                        "drugName": "Suporte Vasoativo e Neurointensivo",
                        "dosage": "Titulação de vasopressores em BIC",
                        "route": "Intravenosa contínua",
                        "frequency": "Contínua em BIC",
                        "infusionProtocol": NOREPINEPHRINE_PROTOCOL
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_ich56_align",
                        "recommendationTitle": "Suporte Inicial Pleno e Alinhamento Bioético Familiar",
                        "dispositionTarget": "UTI Neurocrítica",
                        "monitoringPlan": "Suporte intensivo pleno inicial. Conferência familiar multiprofissional sobre metas terapêuticas e diretivas antecipadas após 48 horas de estabilização."
                    }
                ],
                "infusionProtocol": NOREPINEPHRINE_PROTOCOL
            }
        ]
    }

def get_abcd2():
    return {
        "id": "calc_abcd2",
        "slug": "abcd2",
        "name": "Escala ABCD² de Risco de AVC Pós-AIT",
        "acronym": "ABCD²",
        "version": "1.0.0",
        "category": "Neurologia e Neurocirurgia",
        "subcategory": "Neurologia Vascular / Rastreio no AIT",
        "categorySlug": "bloco-03-neurologia-neurocirurgia",
        "categoryName": "Neurologia e Neurocirurgia",
        "moduleName": "Doença Cerebrovascular e AVC Agudo",
        "description": "Escala clínica de triagem de 0 a 7 pontos para estimar o risco de acidente vascular cerebral isquêmico agudo em 48 horas, 7 dias e 90 dias após um Ataque Isquêmico Transitório (AIT).",
        "summary": "Escore de 0 a 7 pontos para estratificação do risco de AVC isquêmico em 48h, 7 dias e 90 dias após AIT.",
        "clinicalObjective": "Identificar pacientes sob elevado risco precoce de AVC isquêmico pós-AIT, orientando internação imediata e instituição de dupla antiagregação plaquetária.",
        "targetPopulation": "Adultos admitidos no pronto-socorro com déficit neurológico focal agudo com resolução clínica espontânea completa em menos de 24 horas.",
        "calculationType": "additive_points",
        "formulaExpression": "Idade_pontos + PA_pontos + Clinica_pontos + Duracao_pontos + Diabetes_pontos",
        "evidenceSource": "Johnston SC, Rothwell PM, Nguyen-Huynh MN, et al. Validation and refinement of scores to predict very early stroke after transient ischaemic attack. Lancet. 2007;369(9558):283-292. CHANCE & POINT Trials.",
        "minPossibleScore": 0,
        "maxPossibleScore": 7,
        "baseScore": 0,
        "badge": "avc-agudo",
        "clinicalWarning": "ARMADILHA DO ABCD² ISOLADO: O escore ABCD² subestima o risco em pacientes com estenose carotídea grave (>= 70%) ou fontes cardioembólicas maiores (Fibrilação Atrial). Paciente com disartria isolada de 15 minutos pontua apenas 1 (falso baixo risco), mas portando estenose carotídea grave apresenta risco de AVC em 48h superior a 20%. A neuroimagem vascular urgente (Angio-TC ou Angio-RM cervical e craniana) NUNCA deve ser dispensada com base em escore baixo.",
        "radarAxes": [
            {
                "id": "axis_abcd2_age",
                "label": "Idade >= 60 Anos",
                "system": "Demográfico",
                "unit": "anos",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_abcd2_bp",
                "label": "Pressão Arterial Inicial",
                "system": "Cardiovascular",
                "unit": "mmHg",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_abcd2_clinical",
                "label": "Déficit Focal / Fraqueza",
                "system": "Neurológico",
                "unit": "pts",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_abcd2_duration",
                "label": "Duração dos Sintomas",
                "system": "Neurológico",
                "unit": "min",
                "baselineValue": 0,
                "maxAxisValue": 1
            },
            {
                "id": "axis_abcd2_diabetes",
                "label": "Diabetes Mellitus",
                "system": "Metabólico",
                "unit": "grau",
                "baselineValue": 0,
                "maxAxisValue": 1
            }
        ],
        "parameterGroups": [
            {
                "id": "grp_abcd2_age",
                "name": "A - Age (Idade do Paciente)",
                "slug": "abcd2-idade",
                "inputType": "single_choice",
                "unit": "anos",
                "radarAxisId": "axis_abcd2_age",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 1,
                "helpText": "Ponto de corte de 60 anos.",
                "options": [
                    {
                        "id": "opt_abcd2_age_lt60",
                        "label": "Idade < 60 anos (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Menor de 60 anos."
                    },
                    {
                        "id": "opt_abcd2_age_ge60",
                        "label": "Idade >= 60 anos (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "60 anos ou mais."
                    }
                ]
            },
            {
                "id": "grp_abcd2_bp",
                "name": "B - Blood Pressure (PA na Avaliação Inicial)",
                "slug": "abcd2-pa",
                "inputType": "single_choice",
                "unit": "mmHg",
                "radarAxisId": "axis_abcd2_bp",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 2,
                "helpText": "PAS >= 140 mmHg e/ou PAD >= 90 mmHg.",
                "options": [
                    {
                        "id": "opt_abcd2_bp_norm",
                        "label": "PAS < 140 mmHg e PAD < 90 mmHg (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Pressão arterial normal."
                    },
                    {
                        "id": "opt_abcd2_bp_high",
                        "label": "PAS >= 140 mmHg e/ou PAD >= 90 mmHg (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Hipertensão na aferição inicial."
                    }
                ]
            },
            {
                "id": "grp_abcd2_clinical",
                "name": "C - Clinical Features (Apresentação Clínica)",
                "slug": "abcd2-clinica",
                "inputType": "single_choice",
                "unit": "pts",
                "radarAxisId": "axis_abcd2_clinical",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 3,
                "helpText": "Sintomas neurológicos predominantes durante o episódio.",
                "options": [
                    {
                        "id": "opt_abcd2_clin_other",
                        "label": "Outros sintomas (ex.: sensoriais puros, visuais sem paresia) (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sintomas sem fraqueza ou alteração da fala."
                    },
                    {
                        "id": "opt_abcd2_clin_speech",
                        "label": "Distúrbio da fala / disfasia isolada sem fraqueza (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Afasia ou disartria sem paresia motora."
                    },
                    {
                        "id": "opt_abcd2_clin_weakness",
                        "label": "Fraqueza unilateral (com ou sem distúrbio da fala) (2 pontos)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Hemiparesia ou monoparesia motora objetiva."
                    }
                ]
            },
            {
                "id": "grp_abcd2_duration",
                "name": "D - Duration (Duração dos Sintomas)",
                "slug": "abcd2-duracao",
                "inputType": "single_choice",
                "unit": "min",
                "radarAxisId": "axis_abcd2_duration",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 4,
                "helpText": "Tempo decorrido do início até resolução clínica completa.",
                "options": [
                    {
                        "id": "opt_abcd2_dur_lt10",
                        "label": "Duração < 10 minutos (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Sintomas fugazes com menos de 10 minutos."
                    },
                    {
                        "id": "opt_abcd2_dur_10_59",
                        "label": "Duração de 10 a 59 minutos (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 0.5,
                        "sortOrder": 2,
                        "description": "Sintomas durando entre 10 e 59 minutos."
                    },
                    {
                        "id": "opt_abcd2_dur_ge60",
                        "label": "Duração >= 60 minutos (2 pontos)",
                        "pointValue": 2,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 3,
                        "description": "Sintomas prolongados com 60 minutos ou mais."
                    }
                ]
            },
            {
                "id": "grp_abcd2_diabetes",
                "name": "D - Diabetes Mellitus",
                "slug": "abcd2-diabetes",
                "inputType": "single_choice",
                "unit": "grau",
                "radarAxisId": "axis_abcd2_diabetes",
                "normalBaselineValue": 0,
                "maxAxisValue": 1,
                "sortOrder": 5,
                "helpText": "História prévia documentada de diabetes.",
                "options": [
                    {
                        "id": "opt_abcd2_dm_no",
                        "label": "Ausência de Diabetes (0 pontos)",
                        "pointValue": 0,
                        "isNormalBaseline": True,
                        "radarNormalizedValue": 0.0,
                        "sortOrder": 1,
                        "description": "Não diabético."
                    },
                    {
                        "id": "opt_abcd2_dm_yes",
                        "label": "Diagnóstico de Diabetes Mellitus Presente (1 ponto)",
                        "pointValue": 1,
                        "isNormalBaseline": False,
                        "radarNormalizedValue": 1.0,
                        "sortOrder": 2,
                        "description": "Diabético conhecido em tratamento."
                    }
                ]
            }
        ],
        "riskTiers": [
            {
                "id": "tier_abcd2_low",
                "label": "Baixo Risco de AVC (0 a 3 pontos)",
                "severityLevel": "low",
                "minScore": 0,
                "maxScore": 3,
                "statisticalOutcome": "Risco de AVC isquêmico em 48h: 1,0%; em 7 dias: 1,2%; em 90 dias: ~3,0%.",
                "colorHex": "#10b981",
                "pharmacologicalActions": [
                    {
                        "id": "rx_abcd2_aspirin",
                        "drugName": "AAS (Ácido Acetilsalicílico) + Atorvastatina",
                        "dosage": "AAS 160 a 300 mg ataque VO seguido de 100 mg/dia VO + Atorvastatina 40 a 80 mg/dia VO",
                        "route": "Via Oral",
                        "frequency": "Diária",
                        "contraindications": "Alergia grave à aspirina (usar Clopidogrel 75 mg/dia)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_abcd2_amb",
                        "recommendationTitle": "Investigação Ambulatorial Rápida (< 48h)",
                        "dispositionTarget": "Observação / Clínica Ambulatorial de AIT",
                        "monitoringPlan": "Ecodoppler de carótidas e vertebrais, ECG, Holter 24h e ecocardiograma transtorácico em menos de 48 horas se suporte social seguro."
                    }
                ]
            },
            {
                "id": "tier_abcd2_mod",
                "label": "Moderado Risco de AVC (4 a 5 pontos)",
                "severityLevel": "intermediate",
                "minScore": 4,
                "maxScore": 5,
                "statisticalOutcome": "Risco de AVC em 48h: 4,1%; em 7 dias: 5,9% a 10%; em 90 dias: ~9,8%. Internação hospitalar obrigatória.",
                "colorHex": "#f59e0b",
                "pharmacologicalActions": [
                    {
                        "id": "rx_abcd2_dapt_protocol",
                        "drugName": "Dupla Antiagregação Plaquetária (DAPT CHANCE / POINT)",
                        "dosage": "AAS 160-300 mg ataque VO + Clopidogrel 300 mg ataque VO, mantendo AAS 100 mg + Clopidogrel 75 mg/dia VO por 21 dias contínuos, seguido de monoterapia com AAS",
                        "route": "Via Oral",
                        "frequency": "Diária por 21 dias",
                        "contraindications": "Sangramento ativo gastrintestinal ou coagulopatia grave."
                    },
                    {
                        "id": "rx_abcd2_statin_high",
                        "drugName": "Atorvastatina de Alta Potência",
                        "dosage": "80 mg VO uma vez ao dia à noite (meta de LDL < 55 mg/dL)",
                        "route": "Via Oral",
                        "frequency": "24/24 horas"
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_abcd2_ward",
                        "recommendationTitle": "Internação Hospitalar Mandatória e Imagem Vascular Urgente",
                        "dispositionTarget": "Enfermaria de Neurologia / Leito Monitorizado",
                        "monitoringPlan": "Telemetria cardíaca contínua por >= 24h para pesquisar Fibrilação Atrial paroxística.",
                        "interventionalProcedure": "Ressonância Magnética de crânio com difusão (DWI) e Angio-TC de vasos cervicais e intracranianos em menos de 24 horas."
                    }
                ]
            },
            {
                "id": "tier_abcd2_high",
                "label": "Alto Risco de AVC (6 a 7 pontos)",
                "severityLevel": "critical",
                "minScore": 6,
                "maxScore": 7,
                "statisticalOutcome": "Risco de AVC em 48h: 8,1%; em 7 dias: 11,7% a 18%; em 90 dias: ~18,0%.",
                "colorHex": "#ef4444",
                "pharmacologicalActions": [
                    {
                        "id": "rx_abcd2_dapt_high",
                        "drugName": "Protocolo DAPT Imediato (AAS + Clopidogrel por 21 dias)",
                        "dosage": "AAS 300 mg ataque + Clopidogrel 300 mg ataque imediato",
                        "route": "Via Oral",
                        "frequency": "Imediata",
                        "contraindications": "Se Fibrilação Atrial confirmada, suspender DAPT e introduzir DOAC pleno (Apixabana 5 mg 12/12h ou Rivaroxabana 20 mg/dia)."
                    }
                ],
                "nonPharmacologicalActions": [
                    {
                        "id": "nonrx_abcd2_cea",
                        "recommendationTitle": "Internação Imediata e Avaliação de Revascularização Carotídea Urgente",
                        "dispositionTarget": "Unidade de AVC / UTI",
                        "monitoringPlan": "Telemetria e vigilância neurológica contínua.",
                        "interventionalProcedure": "Se estenose aterosclerótica carotídea ipsilateral >= 70% detectada na angio-TC: indicação formal de Endarterectomia Carotídea (CEA) ou Angioplastia com Stent em caráter de urgência nas primeiras 48 horas a 7 dias do evento."
                    }
                ]
            }
        ]
    }
