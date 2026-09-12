import json
import os

os.makedirs("data/categories", exist_ok=True)

# ============================================================================
# TABELAS OFICIAIS DE TESOUROS DE TORMENTA20 (Jogo do Ano, Cap 8, págs 333-345)
# VERBATIM VERIFICATION STRICTLY APPLIED
# ============================================================================

treasure_entities = []

# Subcategorias oficiais:
SUB_ND = "Tabela de Tesouro por ND"
SUB_COMUNS = "Riqueza/Equipamentos/Itens/Superiores"
SUB_MAGICOS = "Itens Mágicos"

# ----------------------------------------------------------------------------
# 1. TABELA 8-1: TESOURO POR NÍVEL DE DESAFIO (ND 1/4 a ND 20)
# ----------------------------------------------------------------------------

nd_tables = [
    {
        "nd": "1/4", "nd_num": 0.25, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 30, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 31, "d100Max": 70, "label": "1d6 x 10 TC (Tibares de Cobre)", "moneyFormula": "1d6 * 10 TC"},
            {"d100Min": 71, "d100Max": 95, "label": "1d4 x 100 TC", "moneyFormula": "1d4 * 100 TC"},
            {"d100Min": 96, "d100Max": 100, "label": "1d6 x 10 T$", "moneyFormula": "1d6 * 10 T$"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 50, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 51, "d100Max": 75, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 76, "d100Max": 100, "label": "1 Equipamento Comum (Tabela 8-4)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"}
        ]
    },
    {
        "nd": "1/2", "nd_num": 0.5, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 25, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 26, "d100Max": 70, "label": "2d6 x 10 TC", "moneyFormula": "2d6 * 10 TC"},
            {"d100Min": 71, "d100Max": 95, "label": "2d8 x 10 T$", "moneyFormula": "2d8 * 10 T$"},
            {"d100Min": 96, "d100Max": 100, "label": "1d4 x 100 T$", "moneyFormula": "1d4 * 100 T$"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 45, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 46, "d100Max": 70, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 71, "d100Max": 100, "label": "1 Equipamento Comum (Tabela 8-4)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"}
        ]
    },
    {
        "nd": "1", "nd_num": 1, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 21, "d100Max": 70, "label": "3d8 x 10 T$", "moneyFormula": "3d8 * 10 T$"},
            {"d100Min": 71, "d100Max": 95, "label": "4d12 x 10 T$", "moneyFormula": "4d12 * 10 T$"},
            {"d100Min": 96, "d100Max": 100, "label": "1 riqueza menor (Tabela 8-2A)", "moneyFormula": "1 riqueza menor"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 40, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 41, "d100Max": 65, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 66, "d100Max": 90, "label": "1 Equipamento Comum (Tabela 8-4)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "1 poção (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"}
        ]
    },
    {
        "nd": "2", "nd_num": 2, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 15, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 16, "d100Max": 55, "label": "3d10 x 10 T$", "moneyFormula": "3d10 * 10 T$"},
            {"d100Min": 56, "d100Max": 85, "label": "2d4 x 100 T$", "moneyFormula": "2d4 * 100 T$"},
            {"d100Min": 86, "d100Max": 95, "label": "(2d6+1) x 100 T$", "moneyFormula": "(2d6+1) * 100 T$"},
            {"d100Min": 96, "d100Max": 100, "label": "1 riqueza menor (Tabela 8-2A)", "moneyFormula": "1 riqueza menor"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 30, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 31, "d100Max": 40, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 41, "d100Max": 70, "label": "1 Equipamento Comum (Tabela 8-4)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"},
            {"d100Min": 71, "d100Max": 90, "label": "1 poção (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 91, "d100Max": 100, "label": "Superior (1 melhoria) (Tabela 8-5)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "3", "nd_num": 3, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 20, "label": "4d12 x 10 T$", "moneyFormula": "4d12 * 10 T$"},
            {"d100Min": 21, "d100Max": 60, "label": "1d4 x 100 T$", "moneyFormula": "1d4 * 100 T$"},
            {"d100Min": 61, "d100Max": 90, "label": "1d8 x 10 TO (Tibares de Ouro)", "moneyFormula": "1d8 * 10 TO"},
            {"d100Min": 91, "d100Max": 100, "label": "1d3 riquezas menores (Tabela 8-2A)", "moneyFormula": "1d3 riquezas menores"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 25, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 26, "d100Max": 35, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 36, "d100Max": 60, "label": "1 Equipamento Comum (Tabela 8-4)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"},
            {"d100Min": 61, "d100Max": 85, "label": "1 poção (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 86, "d100Max": 100, "label": "Superior (1 melhoria) (Tabela 8-5)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "4", "nd_num": 4, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 50, "label": "1d6 x 100 T$", "moneyFormula": "1d6 * 100 T$"},
            {"d100Min": 51, "d100Max": 80, "label": "1d12 x 100 T$", "moneyFormula": "1d12 * 100 T$"},
            {"d100Min": 81, "d100Max": 90, "label": "1 riqueza menor (+20% na rolagem)", "moneyFormula": "1 riqueza menor (+20%)"},
            {"d100Min": 91, "d100Max": 100, "label": "1d3 riquezas menores (+20% na rolagem)", "moneyFormula": "1d3 riquezas menores (+20%)"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 30, "label": "1 Item Diverso (Tabela 8-3)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-3-itens-diversos"},
            {"d100Min": 31, "d100Max": 55, "label": "1 Equipamento Comum (2D: role 2d6 e escolha)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-4a-equipamento-armas"},
            {"d100Min": 56, "d100Max": 80, "label": "1 poção (+20% na rolagem)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 81, "d100Max": 100, "label": "Superior (1 melhoria, 2D)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "5", "nd_num": 5, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 15, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 16, "d100Max": 65, "label": "1d8 x 100 T$", "moneyFormula": "1d8 * 100 T$"},
            {"d100Min": 66, "d100Max": 95, "label": "3d4 x 10 TO", "moneyFormula": "3d4 * 10 TO"},
            {"d100Min": 96, "d100Max": 100, "label": "1 riqueza média (Tabela 8-2B)", "moneyFormula": "1 riqueza média"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 70, "label": "1 poção (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 71, "d100Max": 90, "label": "Superior (1 melhoria)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "Superior (2 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "6", "nd_num": 6, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 15, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 16, "d100Max": 60, "label": "2d6 x 100 T$", "moneyFormula": "2d6 * 100 T$"},
            {"d100Min": 61, "d100Max": 90, "label": "2d10 x 100 T$", "moneyFormula": "2d10 * 100 T$"},
            {"d100Min": 91, "d100Max": 100, "label": "(1d3+1) riquezas menores", "moneyFormula": "(1d3+1) riquezas menores"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 65, "label": "1 poção (+20% na rolagem)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 66, "d100Max": 95, "label": "Superior (1 melhoria)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 96, "d100Max": 100, "label": "Superior (2 melhorias, 2D)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "7", "nd_num": 7, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 60, "label": "2d8 x 100 T$", "moneyFormula": "2d8 * 100 T$"},
            {"d100Min": 61, "d100Max": 90, "label": "2d12 x 10 TO", "moneyFormula": "2d12 * 10 TO"},
            {"d100Min": 91, "d100Max": 100, "label": "(1d4+1) riquezas menores", "moneyFormula": "(1d4+1) riquezas menores"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 60, "label": "1d3 poções (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 61, "d100Max": 90, "label": "Superior (2 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "Superior (3 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "8", "nd_num": 8, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 55, "label": "2d10 x 100 T$", "moneyFormula": "2d10 * 100 T$"},
            {"d100Min": 56, "d100Max": 95, "label": "(1d4+1) riquezas menores", "moneyFormula": "(1d4+1) riquezas menores"},
            {"d100Min": 96, "d100Max": 100, "label": "1 riqueza média (+20%)", "moneyFormula": "1 riqueza média (+20%)"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 75, "label": "1d3 poções (Tabela 8-12)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 76, "d100Max": 95, "label": "Superior (2 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 96, "d100Max": 100, "label": "Superior (3 melhorias, 2D)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"}
        ]
    },
    {
        "nd": "9", "nd_num": 9, "page": 334,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 35, "label": "1 riqueza média (Tabela 8-2B)", "moneyFormula": "1 riqueza média"},
            {"d100Min": 36, "d100Max": 85, "label": "4d6 x 100 T$", "moneyFormula": "4d6 * 100 T$"},
            {"d100Min": 86, "d100Max": 100, "label": "1d3 riquezas médias", "moneyFormula": "1d3 riquezas médias"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 70, "label": "1 poção (+20% na rolagem)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 71, "d100Max": 95, "label": "Superior (3 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 96, "d100Max": 100, "label": "Mágico (menor)", "itemCategory": "Mágico Menor"}
        ]
    },
    {
        "nd": "10", "nd_num": 10, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 30, "label": "4d6 x 100 T$", "moneyFormula": "4d6 * 100 T$"},
            {"d100Min": 31, "d100Max": 85, "label": "4d10 x 10 TO", "moneyFormula": "4d10 * 10 TO"},
            {"d100Min": 86, "d100Max": 100, "label": "(1d3+1) riquezas médias", "moneyFormula": "(1d3+1) riquezas médias"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 50, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 51, "d100Max": 75, "label": "(1d3+1) poções", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 76, "d100Max": 90, "label": "Superior (3 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "Mágico (menor)", "itemCategory": "Mágico Menor"}
        ]
    },
    {
        "nd": "11", "nd_num": 11, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 45, "label": "2d4 x 1.000 T$", "moneyFormula": "2d4 * 1000 T$"},
            {"d100Min": 46, "d100Max": 85, "label": "1d3 riquezas médias", "moneyFormula": "1d3 riquezas médias"},
            {"d100Min": 86, "d100Max": 100, "label": "2d6 x 100 TO", "moneyFormula": "2d6 * 100 TO"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 45, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 46, "d100Max": 70, "label": "(1d4+1) poções", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 71, "d100Max": 90, "label": "Superior (3 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "Mágico (menor, 2D)", "itemCategory": "Mágico Menor"}
        ]
    },
    {
        "nd": "12", "nd_num": 12, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 45, "label": "1 riqueza média (+20%)", "moneyFormula": "1 riqueza média (+20%)"},
            {"d100Min": 46, "d100Max": 80, "label": "2d6 x 1.000 T$", "moneyFormula": "2d6 * 1000 T$"},
            {"d100Min": 81, "d100Max": 100, "label": "(1d4+1) riquezas médias", "moneyFormula": "(1d4+1) riquezas médias"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 45, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 46, "d100Max": 70, "label": "(1d3+1) poções (+20%)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 71, "d100Max": 85, "label": "Superior (4 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 86, "d100Max": 100, "label": "Mágico (menor)", "itemCategory": "Mágico Menor"}
        ]
    },
    {
        "nd": "13", "nd_num": 13, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 45, "label": "4d4 x 1.000 T$", "moneyFormula": "4d4 * 1000 T$"},
            {"d100Min": 46, "d100Max": 80, "label": "(1d3+1) riquezas médias", "moneyFormula": "(1d3+1) riquezas médias"},
            {"d100Min": 81, "d100Max": 100, "label": "4d6 x 100 TO", "moneyFormula": "4d6 * 100 TO"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 40, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 41, "d100Max": 65, "label": "(1d4+1) poções (+20%)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 66, "d100Max": 95, "label": "Superior (4 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 96, "d100Max": 100, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"}
        ]
    },
    {
        "nd": "14", "nd_num": 14, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 45, "label": "(1d3+1) riquezas médias", "moneyFormula": "(1d3+1) riquezas médias"},
            {"d100Min": 46, "d100Max": 80, "label": "3d6 x 1.000 T$", "moneyFormula": "3d6 * 1000 T$"},
            {"d100Min": 81, "d100Max": 100, "label": "1 riqueza maior (Tabela 8-2C)", "moneyFormula": "1 riqueza maior"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 40, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 41, "d100Max": 65, "label": "(1d4+1) poções (+20%)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 66, "d100Max": 90, "label": "Superior (4 melhorias)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 91, "d100Max": 100, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"}
        ]
    },
    {
        "nd": "15", "nd_num": 15, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 45, "label": "1 riqueza média (+20%)", "moneyFormula": "1 riqueza média (+20%)"},
            {"d100Min": 46, "d100Max": 80, "label": "2d10 x 1.000 T$", "moneyFormula": "2d10 * 1000 T$"},
            {"d100Min": 81, "d100Max": 100, "label": "1d4 x 1.000 TO", "moneyFormula": "1d4 * 1000 TO"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 35, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 36, "d100Max": 45, "label": "(1d6+1) poções", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 46, "d100Max": 85, "label": "Superior (4 melhorias, 2D)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 86, "d100Max": 100, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"}
        ]
    },
    {
        "nd": "16", "nd_num": 16, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 11, "d100Max": 40, "label": "3d6 x 1.000 T$", "moneyFormula": "3d6 * 1000 T$"},
            {"d100Min": 41, "d100Max": 75, "label": "3d10 x 100 TO", "moneyFormula": "3d10 * 100 TO"},
            {"d100Min": 76, "d100Max": 100, "label": "1d3 riquezas maiores", "moneyFormula": "1d3 riquezas maiores"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 35, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 36, "d100Max": 45, "label": "(1d6+1) poções (+20%)", "itemCategory": "Comum", "itemRollTableRef": "tabela-8-12-pocoes"},
            {"d100Min": 46, "d100Max": 80, "label": "Superior (4 melhorias, 2D)", "itemCategory": "Superior", "itemRollTableRef": "tabela-8-5a-itens-superiores-armas"},
            {"d100Min": 81, "d100Max": 100, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"}
        ]
    },
    {
        "nd": "17", "nd_num": 17, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 5, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 6, "d100Max": 40, "label": "4d6 x 1.000 T$", "moneyFormula": "4d6 * 1000 T$"},
            {"d100Min": 41, "d100Max": 75, "label": "1d3 riquezas médias (+20%)", "moneyFormula": "1d3 riquezas médias (+20%)"},
            {"d100Min": 76, "d100Max": 100, "label": "2d4 x 1.000 TO", "moneyFormula": "2d4 * 1000 TO"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 20, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 21, "d100Max": 40, "label": "Mágico (menor)", "itemCategory": "Mágico Menor"},
            {"d100Min": 41, "d100Max": 80, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"},
            {"d100Min": 81, "d100Max": 100, "label": "Mágico (maior)", "itemCategory": "Mágico Maior"}
        ]
    },
    {
        "nd": "18", "nd_num": 18, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 5, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 6, "d100Max": 40, "label": "4d10 x 1.000 T$", "moneyFormula": "4d10 * 1000 T$"},
            {"d100Min": 41, "d100Max": 75, "label": "1 riqueza maior (Tabela 8-2C)", "moneyFormula": "1 riqueza maior"},
            {"d100Min": 76, "d100Max": 100, "label": "(1d3+1) riquezas maiores", "moneyFormula": "(1d3+1) riquezas maiores"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 15, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 16, "d100Max": 40, "label": "Mágico (menor, 2D)", "itemCategory": "Mágico Menor"},
            {"d100Min": 41, "d100Max": 70, "label": "Mágico (médio)", "itemCategory": "Mágico Médio"},
            {"d100Min": 71, "d100Max": 100, "label": "Mágico (maior)", "itemCategory": "Mágico Maior"}
        ]
    },
    {
        "nd": "19", "nd_num": 19, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 5, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 6, "d100Max": 40, "label": "4d12 x 1.000 T$", "moneyFormula": "4d12 * 1000 T$"},
            {"d100Min": 41, "d100Max": 75, "label": "1 riqueza maior (+20%)", "moneyFormula": "1 riqueza maior (+20%)"},
            {"d100Min": 76, "d100Max": 100, "label": "1d12 x 1.000 TO", "moneyFormula": "1d12 * 1000 TO"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 10, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 11, "d100Max": 40, "label": "Mágico (menor, 2D)", "itemCategory": "Mágico Menor"},
            {"d100Min": 41, "d100Max": 60, "label": "Mágico (médio, 2D)", "itemCategory": "Mágico Médio"},
            {"d100Min": 61, "d100Max": 100, "label": "Mágico (maior)", "itemCategory": "Mágico Maior"}
        ]
    },
    {
        "nd": "20", "nd_num": 20, "page": 335,
        "money": [
            {"d100Min": 1, "d100Max": 5, "label": "Nenhum", "moneyFormula": "0 T$"},
            {"d100Min": 6, "d100Max": 40, "label": "2d4 x 1.000 TO", "moneyFormula": "2d4 * 1000 TO"},
            {"d100Min": 41, "d100Max": 75, "label": "1d3 riquezas maiores", "moneyFormula": "1d3 riquezas maiores"},
            {"d100Min": 76, "d100Max": 100, "label": "(1d3+1) riquezas maiores (+20%)", "moneyFormula": "(1d3+1) riquezas maiores (+20%)"}
        ],
        "items": [
            {"d100Min": 1, "d100Max": 5, "label": "Nenhum", "itemCategory": "Nenhum"},
            {"d100Min": 6, "d100Max": 40, "label": "Mágico (menor, 2D)", "itemCategory": "Mágico Menor"},
            {"d100Min": 41, "d100Max": 50, "label": "Mágico (médio, 2D)", "itemCategory": "Mágico Médio"},
            {"d100Min": 51, "d100Max": 100, "label": "Mágico (maior, 2D)", "itemCategory": "Mágico Maior"}
        ]
    }
]

for t in nd_tables:
    entries = []
    for m in t["money"]:
        entries.append({
            "d100Min": m["d100Min"],
            "d100Max": m["d100Max"],
            "label": m["label"],
            "moneyFormula": m["moneyFormula"],
            "description": f"Rolagem D% para Dinheiro em ND {t['nd']}: {m['label']}.",
            "entryType": "money"
        })
    for it in t["items"]:
        entries.append({
            "d100Min": it["d100Min"],
            "d100Max": it["d100Max"],
            "label": it["label"],
            "itemCategory": it["itemCategory"],
            "itemRollTableRef": it.get("itemRollTableRef"),
            "description": f"Rolagem D% para Itens em ND {t['nd']}: {it['label']}.",
            "entryType": "item"
        })

    slug_id = f"tesouro-tabela-nd-{str(t['nd']).replace('/', '-')}"
    treasure_entities.append({
        "id": slug_id,
        "name": f"Tabela 8-1: Tesouro por ND {t['nd']}",
        "category": "tesouro",
        "subcategory": SUB_ND,
        "threatLevelMin": t["nd_num"],
        "threatLevelMax": t["nd_num"],
        "threatLevelLabel": f"ND {t['nd']}",
        "summary": f"Tabela oficial de espólios e recompensas por D% para combates de ND {t['nd']}.",
        "description": f"Para determinar o tesouro de um combate de ND {t['nd']}, faça duas rolagens de d% (d100), uma na coluna Dinheiro e outra na coluna Itens.",
        "entries": entries,
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano",
            "page": t["page"],
            "section": "Capítulo 8: Recompensas - Tesouro em Combate",
            "version": "1.3"
        }],
        "tags": ["tesouro", "recompensa", "d%", "d100", f"nd {t['nd']}", "dinheiro", "espólio"]
    })

# ----------------------------------------------------------------------------
# 2. GRUPO: Riqueza/Equipamentos/Itens/Superiores
# ----------------------------------------------------------------------------

# 2.1 TABELA 8-2: RIQUEZAS (DIVIDIDAS POR MENOR, MÉDIA E MAIOR)

riqueza_menor_entries = [
    {"d100Min": 1, "d100Max": 25, "label": "4d4 T$ (Média 10 T$)", "description": "Ágata ou hematita (1/2); barril de farinha ou gaiola com galinhas (5)."},
    {"d100Min": 26, "d100Max": 40, "label": "1d4x10 T$ (Média 25 T$)", "description": "Quartzo rosa ou topázio (1/2); caixa de tabaco ou rolo de linho (1); jarro de especiarias, como canela, gorad, pimenta ou sal (2)."},
    {"d100Min": 41, "d100Max": 55, "label": "2d4x10 T$ (Média 50 T$)", "description": "Bracelete de ouro finamente trabalhado (1/2); estatueta de osso ou marfim entalhado ou rolo de seda (1); vaso de prata (2)."},
    {"d100Min": 56, "d100Max": 70, "label": "4d6x10 T$ (Média 140 T$)", "description": "Ametista ou pérola branca (1/2); lingote de prata ou cálice de prata com gemas de lápis-lazúli (1); tapeçaria grande e bem-feita de lã (5)."},
    {"d100Min": 71, "d100Max": 85, "label": "1d6x100 T$ (Média 350 T$)", "description": "Alexandrita ou pérola negra (1/2); espada cerimonial ornada com prata e gema negra no cabo ou pente de prata com pedras preciosas (1)."},
    {"d100Min": 86, "d100Max": 95, "label": "2d6x100 T$ (Média 700 T$)", "description": "Pente em forma de dragão com olhos de gema vermelha (1); harpa de madeira exótica com ornamentos de zircão e marfim (5)."},
    {"d100Min": 96, "d100Max": 99, "label": "2d8x100 T$ (Média 900 T$)", "description": "Opala negra ou tapa-olho com um olho falso de safira (1/2); luva bordada e adornada com gemas ou pingente de opala vermelha com corrente de ouro (1); lingote de ouro ou pintura antiga (2)."},
    {"d100Min": 100, "d100Max": 100, "label": "4d10x100 T$ (Média 2.200 T$)", "description": "Esmeralda verde ou pingente de safira (1/2); caixinha de música de ouro ou tornozeleira com gemas (1); manto bordado em veludo e seda com inúmeras pedras preciosas (2)."}
]

treasure_entities.append({
    "id": "tabela-8-2a-riqueza-menor",
    "name": "Tabela 8-2A: Riquezas — Menor",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 1,
    "threatLevelMax": 4,
    "threatLevelLabel": "Menor (d100)",
    "summary": "Tabela de sorteio D% para Riquezas Menores (Gemas, joias simples e objetos de arte comerciais).",
    "description": "Role 1d100 quando a tabela de tesouro por ND indicar '1 Riqueza Menor'.",
    "entries": riqueza_menor_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 336,
        "section": "Capítulo 8: Tabela 8-2 - Riquezas (Coluna Menor)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "riquezas", "gemas", "joias", "riqueza menor", "d%", "d100"]
})

riqueza_media_entries = [
    {"d100Min": 1, "d100Max": 10, "label": "2d4x10 T$ (Média 50 T$)", "description": "Bracelete de ouro finamente trabalhado (1/2); estatueta de osso ou marfim entalhado ou rolo de seda (1); vaso de prata (2)."},
    {"d100Min": 11, "d100Max": 30, "label": "4d6x10 T$ (Média 140 T$)", "description": "Ametista ou pérola branca (1/2); lingote de prata ou cálice de prata com gemas de lápis-lazúli (1); tapeçaria grande e bem-feita de lã (5)."},
    {"d100Min": 31, "d100Max": 50, "label": "1d6x100 T$ (Média 350 T$)", "description": "Alexandrita ou pérola negra (1/2); espada cerimonial ornada com prata e gema negra no cabo ou pente de prata com pedras preciosas (1)."},
    {"d100Min": 51, "d100Max": 65, "label": "2d6x100 T$ (Média 700 T$)", "description": "Pente em forma de dragão com olhos de gema vermelha (1); harpa de madeira exótica com ornamentos de zircão e marfim (5)."},
    {"d100Min": 66, "d100Max": 80, "label": "2d8x100 T$ (Média 900 T$)", "description": "Opala negra ou tapa-olho com um olho falso de safira (1/2); luva bordada e adornada com gemas ou pingente de opala vermelha com corrente de ouro (1); lingote de ouro ou pintura antiga (2)."},
    {"d100Min": 81, "d100Max": 90, "label": "4d10x100 T$ (Média 2.200 T$)", "description": "Esmeralda verde ou pingente de safira (1/2); caixinha de música de ouro ou tornozeleira com gemas (1); manto bordado em veludo e seda com inúmeras pedras preciosas (2)."},
    {"d100Min": 91, "d100Max": 95, "label": "6d12x100 T$ (Média 3.900 T$)", "description": "Anel de prata e safira ou correntinha com pequenas pérolas rosas, diamante branco (1/2); ídolo de ouro puro maciço (5)."},
    {"d100Min": 96, "d100Max": 99, "label": "2d10x1.000 T$ (Média 11.000 T$)", "description": "Anel de ouro e rubi ou diamante vermelho (1/2); conjunto de taças de ouro decoradas com esmeraldas (2)."},
    {"d100Min": 100, "d100Max": 100, "label": "6d8x1.000 T$ (Média 27.000 T$)", "description": "Coroa de ouro adornada com centenas de gemas, pertencente a um antigo monarca (1); baú de mitral com coleção de diamantes (2)."}
]

treasure_entities.append({
    "id": "tabela-8-2b-riqueza-media",
    "name": "Tabela 8-2B: Riquezas — Média",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 5,
    "threatLevelMax": 13,
    "threatLevelLabel": "Média (d100)",
    "summary": "Tabela de sorteio D% para Riquezas Médias (Joias finas, lingotes de metais nobres e obras de arte).",
    "description": "Role 1d100 quando a tabela de tesouro por ND indicar '1 Riqueza Média'.",
    "entries": riqueza_media_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 336,
        "section": "Capítulo 8: Tabela 8-2 - Riquezas (Coluna Média)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "riquezas", "gemas", "joias", "riqueza média", "d%", "d100"]
})

riqueza_maior_entries = [
    {"d100Min": 1, "d100Max": 5, "label": "1d6x100 T$ (Média 350 T$)", "description": "Alexandrita ou pérola negra (1/2); espada cerimonial ornada com prata e gema negra no cabo ou pente de prata com pedras preciosas (1)."},
    {"d100Min": 6, "d100Max": 15, "label": "2d6x100 T$ (Média 700 T$)", "description": "Pente em forma de dragão com olhos de gema vermelha (1); harpa de madeira exótica com ornamentos de zircão e marfim (5)."},
    {"d100Min": 16, "d100Max": 25, "label": "2d8x100 T$ (Média 900 T$)", "description": "Opala negra ou tapa-olho com um olho falso de safira (1/2); luva bordada e adornada com gemas ou pingente de opala vermelha com corrente de ouro (1); lingote de ouro ou pintura antiga (2)."},
    {"d100Min": 26, "d100Max": 40, "label": "4d10x100 T$ (Média 2.200 T$)", "description": "Esmeralda verde ou pingente de safira (1/2); caixinha de música de ouro ou tornozeleira com gemas (1); manto bordado em veludo e seda com inúmeras pedras preciosas (2)."},
    {"d100Min": 41, "d100Max": 60, "label": "6d12x100 T$ (Média 3.900 T$)", "description": "Anel de prata e safira ou correntinha com pequenas pérolas rosas, diamante branco (1/2); ídolo de ouro puro maciço (5)."},
    {"d100Min": 61, "d100Max": 75, "label": "2d10x1.000 T$ (Média 11.000 T$)", "description": "Anel de ouro e rubi ou diamante vermelho (1/2); conjunto de taças de ouro decoradas com esmeraldas (2)."},
    {"d100Min": 76, "d100Max": 85, "label": "6d8x1.000 T$ (Média 27.000 T$)", "description": "Coroa de ouro adornada com centenas de gemas, pertencente a um antigo monarca (1); baú de mitral com coleção de diamantes (2)."},
    {"d100Min": 86, "d100Max": 95, "label": "1d10x10.000 T$ (Média 55.000 T$)", "description": "Arca de madeira reforçada repleta de lingotes de prata e ouro, além de pedras preciosas de vários tipos (20)."},
    {"d100Min": 96, "d100Max": 100, "label": "4d12x10.000 T$ (Média 260.000 T$)", "description": "Uma sala forrada de moedas! Mover todo esse dinheiro exige trabalhadores e carroças (ou outra ideia por parte dos jogadores), além de atrair a atenção de bandidos, coletores de impostos e aproveitadores de vários tipos..."}
]

treasure_entities.append({
    "id": "tabela-8-2c-riqueza-maior",
    "name": "Tabela 8-2C: Riquezas — Maior",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 14,
    "threatLevelMax": 20,
    "threatLevelLabel": "Maior (d100)",
    "summary": "Tabela de sorteio D% para Riquezas Maiores (Artefatos de arte inestimáveis, coroas e fortunas imperiais).",
    "description": "Role 1d100 quando a tabela de tesouro por ND indicar '1 Riqueza Maior'.",
    "entries": riqueza_maior_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 336,
        "section": "Capítulo 8: Tabela 8-2 - Riquezas (Coluna Maior)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "riquezas", "gemas", "joias", "riqueza maior", "d%", "d100"]
})

# 2.2 TABELA 8-3: ITENS DIVERSOS
tabela_diversos_entries = [
    {"d100Min": 1, "d100Max": 2, "label": "Ácido", "description": "Frasco de ácido alquímico (T$ 10)."},
    {"d100Min": 3, "d100Max": 4, "label": "Água benta", "description": "Água purificada e consagrada (T$ 50)."},
    {"d100Min": 5, "d100Max": 5, "label": "Alaúde élfico", "description": "Instrumento musical de altíssima qualidade (T$ 300)."},
    {"d100Min": 6, "d100Max": 6, "label": "Algemas", "description": "Algemas de aço com chave (T$ 15)."},
    {"d100Min": 7, "d100Max": 8, "label": "Baga-de-fogo", "description": "Fruta alquímica inflamável (T$ 10)."},
    {"d100Min": 9, "d100Max": 23, "label": "Bálsamo restaurador", "description": "Pomada curativa que recupera 2d4 PV (T$ 10)."},
    {"d100Min": 24, "d100Max": 24, "label": "Bandana", "description": "Acessório de vestuário elegante (T$ 5)."},
    {"d100Min": 25, "d100Max": 25, "label": "Bandoleira de poções", "description": "Permite sacar poções e itens alquímicos como ação livre (T$ 20)."},
    {"d100Min": 26, "d100Max": 30, "label": "Bomba", "description": "Explosivo alquímico que causa 6d6 de dano de fogo em área (T$ 50)."},
    {"d100Min": 31, "d100Max": 31, "label": "Botas reforçadas", "description": "Vestuário resistente para intempéries (T$ 20)."},
    {"d100Min": 32, "d100Max": 32, "label": "Camisa bufante", "description": "Traje vistoso (T$ 25)."},
    {"d100Min": 33, "d100Max": 33, "label": "Capa esvoaçante", "description": "Capa de corte fino (T$ 25)."},
    {"d100Min": 34, "d100Max": 34, "label": "Capa pesada", "description": "Proteção contra intempéries e frio (T$ 20)."},
    {"d100Min": 35, "d100Max": 35, "label": "Casaco longo", "description": "Vestuário resistente (T$ 30)."},
    {"d100Min": 36, "d100Max": 36, "label": "Chapéu arcano", "description": "Item de estudo acadêmico e mágico (T$ 50)."},
    {"d100Min": 37, "d100Max": 38, "label": "Coleção de livros", "description": "Compêndio de tomos e estudos (T$ 100)."},
    {"d100Min": 39, "d100Max": 40, "label": "Cosmético", "description": "Artigos de toalete refinados (T$ 20)."},
    {"d100Min": 41, "d100Max": 42, "label": "Dente-de-dragão", "description": "Item alquímico de combate (T$ 50)."},
    {"d100Min": 43, "d100Max": 43, "label": "Enfeite de elmo", "description": "Adorno metálico ou pluma para elmo (T$ 15)."},
    {"d100Min": 44, "d100Max": 44, "label": "Elixir do amor", "description": "Preparado alquímico (T$ 100)."},
    {"d100Min": 45, "d100Max": 46, "label": "Equipamento de viagem", "description": "Saco de dormir, corda e provisões (T$ 10)."},
    {"d100Min": 47, "d100Max": 56, "label": "Essência de mana", "description": "Poção revigorante que recupera 1d4 PM (T$ 50)."},
    {"d100Min": 57, "d100Max": 57, "label": "Estojo de disfarces", "description": "Kit de maquiagem e próteses (T$ 50)."},
    {"d100Min": 58, "d100Max": 58, "label": "Farrapos de ermitão", "description": "Vestes místicas rudimentares (T$ 5)."},
    {"d100Min": 59, "d100Max": 59, "label": "Flauta mística", "description": "Instrumento musical místico (T$ 100)."},
    {"d100Min": 60, "d100Max": 66, "label": "Fogo alquímico", "description": "Frasco de óleo incandescente que causa 1d6 de dano de fogo por rodada (T$ 10)."},
    {"d100Min": 67, "d100Max": 67, "label": "Gorro de ervas", "description": "Proteção e infusões (T$ 15)."},
    {"d100Min": 68, "d100Max": 69, "label": "Líquen lilás", "description": "Ingrediente alquímico (T$ 25)."},
    {"d100Min": 70, "d100Max": 70, "label": "Luneta", "description": "Instrumento óptico de observação (T$ 250)."},
    {"d100Min": 71, "d100Max": 71, "label": "Luva de pelica", "description": "Luvas de couro fino refinadas (T$ 10)."},
    {"d100Min": 72, "d100Max": 73, "label": "Maleta de medicamentos", "description": "Kits de primeiros socorros profissionais (T$ 50)."},
    {"d100Min": 74, "d100Max": 74, "label": "Manopla", "description": "Luva de metal (T$ 5)."},
    {"d100Min": 75, "d100Max": 75, "label": "Manto eclesiástico", "description": "Traje sacerdotal (T$ 50)."},
    {"d100Min": 76, "d100Max": 78, "label": "Mochila de aventureiro", "description": "Aumenta o limite de carga do personagem em 2 espaços (T$ 50)."},
    {"d100Min": 79, "d100Max": 80, "label": "Musgo púrpura", "description": "Componente alquímico (T$ 25)."},
    {"d100Min": 81, "d100Max": 81, "label": "Organizador de pergaminhos", "description": "Estojo protetor para pergaminhos (T$ 25)."},
    {"d100Min": 82, "d100Max": 83, "label": "Ossos de monstro", "description": "Material para artesanato e misticismo (T$ 20)."},
    {"d100Min": 84, "d100Max": 85, "label": "Pó de cristal", "description": "Componente para magias e alquimia (T$ 30)."},
    {"d100Min": 86, "d100Max": 87, "label": "Pó de giz", "description": "Usado para marcações ritualísticas (T$ 5)."},
    {"d100Min": 88, "d100Max": 88, "label": "Pó do desaparecimento", "description": "Alquimia de ocultamento (T$ 100)."},
    {"d100Min": 89, "d100Max": 89, "label": "Robe místico", "description": "Veste arcana refinada (T$ 50)."},
    {"d100Min": 90, "d100Max": 91, "label": "Saco de sal", "description": "Conservante e ingrediente (T$ 5)."},
    {"d100Min": 92, "d100Max": 92, "label": "Sapatos de camurça", "description": "Calçado macio e silencioso (T$ 15)."},
    {"d100Min": 93, "d100Max": 94, "label": "Seixo de âmbar", "description": "Pedra resinosa para focos (T$ 20)."},
    {"d100Min": 95, "d100Max": 95, "label": "Sela", "description": "Arreio completo de montaria (T$ 20)."},
    {"d100Min": 96, "d100Max": 96, "label": "Tabardo", "description": "Veste heráldica sobre a armadura (T$ 10)."},
    {"d100Min": 97, "d100Max": 97, "label": "Traje da corte", "description": "Vestuário nobre (+2 em Diplomacia e Nobreza) (T$ 100)."},
    {"d100Min": 98, "d100Max": 99, "label": "Terra de cemitério", "description": "Componente de necromancia (T$ 10)."},
    {"d100Min": 100, "d100Max": 100, "label": "Veste de seda", "description": "Traje luxuoso de altíssima qualidade (T$ 300)."}
]

treasure_entities.append({
    "id": "tabela-8-3-itens-diversos",
    "name": "Tabela 8-3: Itens Diversos",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 0.25,
    "threatLevelMax": 10,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para itens consumíveis, alquimias, ferramentas e vestuário.",
    "description": "Role 1d100 quando a tabela de tesouro indicar 'Diverso' para determinar o item encontrado.",
    "entries": tabela_diversos_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 337,
        "section": "Capítulo 8: Tabela 8-3 - Itens Diversos",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens diversos", "d%", "d100", "alquimia", "consumíveis"]
})

# 2.3 TABELA 8-4: EQUIPAMENTO (ARMAS, ARMADURAS & ESCUDOS, ESOTÉRICOS)

tabela_8_4a_entries = [
    {"d100Min": 1, "d100Max": 3, "label": "Adaga", "description": "Arma simples de ataque leve ou arremesso."},
    {"d100Min": 4, "d100Max": 5, "label": "Alabarda", "description": "Arma marcial de duas mãos com haste."},
    {"d100Min": 6, "d100Max": 7, "label": "Alfange", "description": "Arma marcial de lâmina curva."},
    {"d100Min": 8, "d100Max": 10, "label": "Arco curto", "description": "Arma simples de ataque à distância."},
    {"d100Min": 11, "d100Max": 13, "label": "Arco longo", "description": "Arma marcial de grande alcance."},
    {"d100Min": 14, "d100Max": 15, "label": "Azagaia", "description": "Lança curta de arremesso."},
    {"d100Min": 16, "d100Max": 16, "label": "Balas (20)", "description": "Munição para armas de fogo."},
    {"d100Min": 17, "d100Max": 18, "label": "Besta leve", "description": "Arma simples mecânica."},
    {"d100Min": 19, "d100Max": 20, "label": "Besta pesada", "description": "Arma marcial potente."},
    {"d100Min": 21, "d100Max": 23, "label": "Bordão", "description": "Arma simples dupla de impacto."},
    {"d100Min": 24, "d100Max": 24, "label": "Chicote", "description": "Arma exótica de alcance."},
    {"d100Min": 25, "d100Max": 27, "label": "Cimitarra", "description": "Arma marcial cortante."},
    {"d100Min": 28, "d100Max": 30, "label": "Clava", "description": "Arma simples de impacto."},
    {"d100Min": 31, "d100Max": 31, "label": "Corrente de espinhos", "description": "Arma exótica flexível."},
    {"d100Min": 32, "d100Max": 33, "label": "Espada bastarda", "description": "Arma exótica/marcial versátil."},
    {"d100Min": 34, "d100Max": 38, "label": "Espada curta", "description": "Arma marcial de perfuração."},
    {"d100Min": 39, "d100Max": 43, "label": "Espada longa", "description": "Arma marcial tradicional."},
    {"d100Min": 44, "d100Max": 46, "label": "Flechas (20)", "description": "Munição para arcos."},
    {"d100Min": 47, "d100Max": 49, "label": "Florete", "description": "Arma marcial ágil."},
    {"d100Min": 50, "d100Max": 51, "label": "Foice", "description": "Arma simples de corte."},
    {"d100Min": 52, "d100Max": 53, "label": "Funda", "description": "Arma simples de arremesso."},
    {"d100Min": 54, "d100Max": 55, "label": "Gadanho", "description": "Arma marcial de duas mãos."},
    {"d100Min": 56, "d100Max": 56, "label": "Katana", "description": "Arma exótica/marcial oriental."},
    {"d100Min": 57, "d100Max": 59, "label": "Lança", "description": "Arma simples de haste."},
    {"d100Min": 60, "d100Max": 60, "label": "Lança montada", "description": "Arma marcial para carga a cavalo."},
    {"d100Min": 61, "d100Max": 63, "label": "Maça", "description": "Arma simples de impacto."},
    {"d100Min": 64, "d100Max": 66, "label": "Machadinha", "description": "Arma simples de arremesso/corte."},
    {"d100Min": 67, "d100Max": 67, "label": "Machado anão", "description": "Arma exótica tradicional dos anões."},
    {"d100Min": 68, "d100Max": 70, "label": "Machado de batalha", "description": "Arma marcial potente."},
    {"d100Min": 71, "d100Max": 73, "label": "Machado de guerra", "description": "Arma marcial de duas mãos."},
    {"d100Min": 74, "d100Max": 74, "label": "Machado táurico", "description": "Arma exótica devastadora dos minotauros."},
    {"d100Min": 75, "d100Max": 76, "label": "Mangual", "description": "Arma marcial de corrente."},
    {"d100Min": 77, "d100Max": 77, "label": "Marreta", "description": "Arma marcial pesada de duas mãos."},
    {"d100Min": 78, "d100Max": 80, "label": "Martelo de guerra", "description": "Arma marcial de impacto."},
    {"d100Min": 81, "d100Max": 83, "label": "Montante", "description": "Espada de duas mãos de alto dano."},
    {"d100Min": 84, "d100Max": 84, "label": "Mosquete", "description": "Arma de fogo de duas mãos."},
    {"d100Min": 85, "d100Max": 85, "label": "Pedras (20)", "description": "Munição para funda."},
    {"d100Min": 86, "d100Max": 88, "label": "Picareta", "description": "Arma marcial de perfuração."},
    {"d100Min": 89, "d100Max": 90, "label": "Pique", "description": "Arma simples de alcance de 3m."},
    {"d100Min": 91, "d100Max": 92, "label": "Pistola", "description": "Arma de fogo leve de uma mão."},
    {"d100Min": 93, "d100Max": 93, "label": "Rede", "description": "Arma exótica de imobilização."},
    {"d100Min": 94, "d100Max": 96, "label": "Tacape", "description": "Arma simples pesada."},
    {"d100Min": 97, "d100Max": 98, "label": "Tridente", "description": "Arma marcial de perfuração/manobras."},
    {"d100Min": 99, "d100Max": 100, "label": "Virotes (20)", "description": "Munição para bestas."}
]

treasure_entities.append({
    "id": "tabela-8-4a-equipamento-armas",
    "name": "Tabela 8-4A: Equipamento — Armas",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 0.25,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para Armas Simples, Marciais, Exóticas e de Fogo.",
    "description": "Role 1d100 quando o resultado do equipamento for Arma (1-3 no d6).",
    "entries": tabela_8_4a_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 337,
        "section": "Capítulo 8: Tabela 8-4 - Equipamento (Armas)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "equipamento", "armas", "d%", "d100"]
})

tabela_8_4b_entries = [
    {"d100Min": 1, "d100Max": 5, "label": "Couro", "description": "Armadura leve (Defesa +2, Penalidade 0)."},
    {"d100Min": 6, "d100Max": 10, "label": "Brunea", "description": "Armadura pesada (Defesa +5, Penalidade -2)."},
    {"d100Min": 11, "d100Max": 25, "label": "Completa", "description": "Armadura pesada (Defesa +10, Penalidade -5)."},
    {"d100Min": 26, "d100Max": 30, "label": "Cota de malha", "description": "Armadura pesada (Defesa +6, Penalidade -2)."},
    {"d100Min": 31, "d100Max": 45, "label": "Couraça", "description": "Armadura leve (Defesa +5, Penalidade -4)."},
    {"d100Min": 46, "d100Max": 55, "label": "Couro batido", "description": "Armadura leve (Defesa +3, Penalidade -1)."},
    {"d100Min": 56, "d100Max": 65, "label": "Escudo leve", "description": "Escudo (Defesa +1, Penalidade -1)."},
    {"d100Min": 66, "d100Max": 80, "label": "Escudo pesado", "description": "Escudo (Defesa +2, Penalidade -2)."},
    {"d100Min": 81, "d100Max": 85, "label": "Gibão de peles", "description": "Armadura leve (Defesa +4, Penalidade -3)."},
    {"d100Min": 86, "d100Max": 90, "label": "Loriga segmentada", "description": "Armadura pesada (Defesa +7, Penalidade -3)."},
    {"d100Min": 91, "d100Max": 100, "label": "Meia armadura", "description": "Armadura pesada (Defesa +8, Penalidade -4)."}
]

treasure_entities.append({
    "id": "tabela-8-4b-equipamento-armaduras",
    "name": "Tabela 8-4B: Equipamento — Armaduras & Escudos",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 0.25,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para Armaduras Leves, Pesadas e Escudos.",
    "description": "Role 1d100 quando o resultado do equipamento for Armadura ou Escudo (4-5 no d6).",
    "entries": tabela_8_4b_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 337,
        "section": "Capítulo 8: Tabela 8-4 - Equipamento (Armaduras)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "equipamento", "armaduras", "escudos", "d%", "d100"]
})

tabela_8_4c_entries = [
    {"d100Min": 1, "d100Max": 10, "label": "Bolsa de pó", "description": "Foco esotérico (T$ 50)."},
    {"d100Min": 11, "d100Max": 25, "label": "Cajado arcano", "description": "Foco esotérico (T$ 100)."},
    {"d100Min": 26, "d100Max": 35, "label": "Cetro elemental", "description": "Foco esotérico (T$ 150)."},
    {"d100Min": 36, "d100Max": 42, "label": "Costela de lich", "description": "Foco esotérico (T$ 200)."},
    {"d100Min": 43, "d100Max": 50, "label": "Dedo de ente", "description": "Foco esotérico (T$ 150)."},
    {"d100Min": 51, "d100Max": 55, "label": "Luva de ferro", "description": "Foco esotérico (T$ 100)."},
    {"d100Min": 56, "d100Max": 65, "label": "Medalhão de prata", "description": "Foco esotérico (T$ 50)."},
    {"d100Min": 66, "d100Max": 75, "label": "Orbe cristalino", "description": "Foco esotérico (T$ 100)."},
    {"d100Min": 76, "d100Max": 85, "label": "Tomo hermético", "description": "Foco esotérico (T$ 200)."},
    {"d100Min": 86, "d100Max": 100, "label": "Varinha arcana", "description": "Foco esotérico (T$ 50)."}
]

treasure_entities.append({
    "id": "tabela-8-4c-equipamento-esotericos",
    "name": "Tabela 8-4C: Equipamento — Esotéricos",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 0.25,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para Itens Esotéricos e Focos Arcanos/Divinos.",
    "description": "Role 1d100 quando o resultado do equipamento for Esotérico (6 no d6).",
    "entries": tabela_8_4c_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 337,
        "section": "Capítulo 8: Tabela 8-4 - Equipamento (Esotéricos)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "equipamento", "esotéricos", "focos", "d%", "d100"]
})

# 2.4 TABELA 8-5: ITENS SUPERIORES (ARMAS, ARMADURAS & ESCUDOS, ESOTÉRICOS)

tabela_8_5a_entries = [
    {"d100Min": 1, "d100Max": 10, "label": "Atroz", "description": "Conta como duas melhorias. Se o item só possuir uma, role novamente."},
    {"d100Min": 11, "d100Max": 13, "label": "Banhada a ouro", "description": "Melhoria estética superior."},
    {"d100Min": 14, "d100Max": 23, "label": "Certeira", "description": "+1 em testes de ataque com a arma."},
    {"d100Min": 24, "d100Max": 26, "label": "Cravejada de gemas", "description": "Melhoria estética de valor elevado."},
    {"d100Min": 27, "d100Max": 36, "label": "Cruel", "description": "+1 nas rolagens de dano."},
    {"d100Min": 37, "d100Max": 39, "label": "Discreta", "description": "+5 em Furtividade para ocultá-la."},
    {"d100Min": 40, "d100Max": 44, "label": "Equilibrada", "description": "+2 em testes de manobra com a arma."},
    {"d100Min": 45, "d100Max": 48, "label": "Harmonizada", "description": "Reduz o custo de uma habilidade de ataque em -1 PM."},
    {"d100Min": 49, "d100Max": 53, "label": "Injeção alquímica", "description": "Permite acoplar e injetar item alquímico no alvo ao acertar."},
    {"d100Min": 54, "d100Max": 55, "label": "Macabra", "description": "+2 em Intimidação enquanto empunhada."},
    {"d100Min": 56, "d100Max": 65, "label": "Maciça", "description": "Aumenta o multiplicador de crítico em +1."},
    {"d100Min": 66, "d100Max": 75, "label": "Material especial", "description": "Role 1d6 para definir o material: 1) aço-rubi, 2) adamante, 3) gelo eterno, 4) madeira Tollon, 5) matéria vermelha, 6) mitral."},
    {"d100Min": 76, "d100Max": 80, "label": "Mira telescópica", "description": "Aumenta o alcance da arma à distância em uma categoria."},
    {"d100Min": 81, "d100Max": 90, "label": "Precisa", "description": "Aumenta a margem de ameaça de crítico em +1."},
    {"d100Min": 91, "d100Max": 100, "label": "Pungente", "description": "Conta como duas melhorias. Se o item só possuir uma, role novamente."}
]

treasure_entities.append({
    "id": "tabela-8-5a-itens-superiores-armas",
    "name": "Tabela 8-5A: Itens Superiores — Armas",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 2,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para melhorias e materiais especiais aplicados a Armas Superiores.",
    "description": "Role 1d100 nesta tabela para cada melhoria que a arma superior possuir.",
    "entries": tabela_8_5a_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 332,
        "section": "Capítulo 8: Tabela 8-5 - Itens Superiores (Armas)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens superiores", "armas", "melhorias", "d%", "d100"]
})

tabela_8_5b_entries = [
    {"d100Min": 1, "d100Max": 15, "label": "Ajustada", "description": "Diminui a penalidade de armadura em 1."},
    {"d100Min": 16, "d100Max": 19, "label": "Banhada a ouro", "description": "Melhoria estética superior."},
    {"d100Min": 20, "d100Max": 23, "label": "Cravejada de gemas", "description": "Melhoria estética nobre."},
    {"d100Min": 24, "d100Max": 28, "label": "Delicada", "description": "Permite aplicar Destreza completa na Defesa."},
    {"d100Min": 29, "d100Max": 32, "label": "Discreta", "description": "+5 em Furtividade para disfarçar uso."},
    {"d100Min": 33, "d100Max": 37, "label": "Espinhos", "description": "Causa 1d6 de dano de perfuração em agarrar."},
    {"d100Min": 38, "d100Max": 40, "label": "Macabra", "description": "+2 em Intimidação enquanto vestida."},
    {"d100Min": 41, "d100Max": 50, "label": "Material especial", "description": "Role 1d6 para definir o material: 1) aço-rubi, 2) adamante, 3) gelo eterno, 4) madeira Tollon, 5) matéria vermelha, 6) mitral."},
    {"d100Min": 51, "d100Max": 55, "label": "Polida", "description": "+2 na Defesa no primeiro ataque da cena."},
    {"d100Min": 56, "d100Max": 80, "label": "Reforçada", "description": "Aumenta o bônus na Defesa em +1."},
    {"d100Min": 81, "d100Max": 90, "label": "Selada", "description": "+2 em testes de resistência contra gases e venenos."},
    {"d100Min": 91, "d100Max": 100, "label": "Sob medida", "description": "Conta como duas melhorias. Se o item só possuir uma, role novamente."}
]

treasure_entities.append({
    "id": "tabela-8-5b-itens-superiores-armaduras",
    "name": "Tabela 8-5B: Itens Superiores — Armaduras & Escudos",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 2,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para melhorias e materiais especiais de Armaduras e Escudos Superiores.",
    "description": "Role 1d100 nesta tabela para cada melhoria que a armadura ou escudo superior possuir.",
    "entries": tabela_8_5b_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 332,
        "section": "Capítulo 8: Tabela 8-5 - Itens Superiores (Armaduras)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens superiores", "armaduras", "escudos", "melhorias", "d%", "d100"]
})

tabela_8_5c_entries = [
    {"d100Min": 1, "d100Max": 4, "label": "Banhado a ouro", "description": "+2 em testes sociais enquanto empunhado."},
    {"d100Min": 5, "d100Max": 19, "label": "Canalizador", "description": "Reduz o custo de magias de área em -1 PM."},
    {"d100Min": 20, "d100Max": 23, "label": "Cravejado de gemas", "description": "Item esotérico ornamentado."},
    {"d100Min": 24, "d100Max": 27, "label": "Discreto", "description": "+5 em Furtividade para ocultá-lo."},
    {"d100Min": 28, "d100Max": 42, "label": "Energético", "description": "+1 no dano de magias por dado."},
    {"d100Min": 43, "d100Max": 57, "label": "Harmonizado", "description": "Reduz o custo de 1 magia específica em -1 PM."},
    {"d100Min": 58, "d100Max": 60, "label": "Macabro", "description": "+2 em Intimidação e magias de necromancia."},
    {"d100Min": 61, "d100Max": 69, "label": "Material especial", "description": "Role 1d6 para definir o material: 1) aço-rubi, 2) adamante, 3) gelo eterno, 4) madeira Tollon, 5) matéria vermelha, 6) mitral."},
    {"d100Min": 70, "d100Max": 85, "label": "Poderoso", "description": "Aumenta a CD para resistir às suas magias em +1."},
    {"d100Min": 86, "d100Max": 100, "label": "Vigilante", "description": "+2 na Defesa e Percepção enquanto empunhado."}
]

treasure_entities.append({
    "id": "tabela-8-5c-itens-superiores-esotericos",
    "name": "Tabela 8-5C: Itens Superiores — Esotéricos",
    "category": "tesouro",
    "subcategory": SUB_COMUNS,
    "threatLevelMin": 2,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela de sorteio por D% (01 a 100) para melhorias e materiais especiais de Itens Esotéricos Superiores.",
    "description": "Role 1d100 nesta tabela para cada melhoria que o item esotérico superior possuir.",
    "entries": tabela_8_5c_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 332,
        "section": "Capítulo 8: Tabela 8-5 - Itens Superiores (Esotéricos)",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens superiores", "esotéricos", "focos", "melhorias", "d%", "d100"]
})

# ----------------------------------------------------------------------------
# 3. GRUPO: Itens Mágicos (Tabelas 8-8 a 8-15 VERBATIM INTEGRAL DO LIVRO)
# ----------------------------------------------------------------------------

tabela_8_8_entries = [
    {"d100Min": 1, "d100Max": 5, "label": "Ameaçadora", "description": "A margem de ameaça da arma duplica. Por exemplo, uma espada longa ameaçadora tem margem de ameaça 17. Efeitos que duplicam a margem de ameaça são aplicados antes de quaisquer efeitos que a aumentem."},
    {"d100Min": 6, "d100Max": 10, "label": "Anticriatura", "description": "A arma é letal contra um tipo de criatura (ou uma raça de humanoides). Uma vez por rodada, quando ataca uma criatura desse tipo, você pode gastar 2 PM. Se fizer isso e acertar o ataque, causa +4d8 de dano. Para determinar o tipo de criatura aleatoriamente, role 1d6: 1) animal; 2) construto; 3) espírito; 4) monstro; 5) morto-vivo; 6) uma raça de humanoides."},
    {"d100Min": 11, "d100Max": 12, "label": "Arremesso", "description": "A arma pode ser arremessada em alcance curto. Caso já pudesse ser arremessada, seu alcance aumenta em uma categoria. Após o ataque, se estiver livre, a arma volta voando para você. Pegá-la é uma reação."},
    {"d100Min": 13, "d100Max": 14, "label": "Assassina", "description": "A arma aumenta os dados de dano extra de um ataque furtivo para d8. Além disso, quando faz um Ataque Furtivo, você pode gastar 2 PM. Se fizer isso, pode rolar novamente quaisquer resultados 1 nesses dados de dano extra."},
    {"d100Min": 15, "d100Max": 16, "label": "Caçadora", "description": "A arma persegue o alvo, anulando penalidades por camuflagem leve e total e por cobertura leve. Caso a arma seja de ataque à distância, seu alcance também aumenta em uma categoria."},
    {"d100Min": 17, "d100Max": 21, "label": "Congelante", "description": "A arma causa +1d6 de dano de frio. Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso e acertar o ataque, a vítima fica enredada por uma rodada. Uma arma congelante é coberta por uma camada de gelo e névoa."},
    {"d100Min": 22, "d100Max": 23, "label": "Conjuradora", "description": "Um conjurador pode lançar na arma uma magia que tenha como alvo uma criatura ou que afete uma área. A magia não gera efeito na hora; em vez disso, fica guardada no item. Quando acerta um ataque com a arma, você pode descarregar a magia guardada como uma ação livre e sem pagar seu custo. Ela tem como alvo (ou como ponto de origem de sua área) a criatura ou ponto atingido pelo ataque. Uma vez que a magia seja descarregada, outra pode ser armazenada."},
    {"d100Min": 24, "d100Max": 28, "label": "Corrosiva", "description": "A arma causa +1d6 de dano de ácido. Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso e acertar o ataque, a vítima sofre 4d4 pontos de dano de ácido na próxima rodada. Uma arma corrosiva exala vapores e goteja líquido tóxico."},
    {"d100Min": 29, "d100Max": 30, "label": "Dançarina", "description": "Você pode gastar uma ação de movimento e 1 PM para fazer a arma flutuar e atacar uma criatura em alcance curto a sua escolha, com as mesmas estatísticas que teria se você a estivesse empunhando. Este efeito tem duração sustentada; se parar de sustentá-lo, a arma cai no chão."},
    {"d100Min": 31, "d100Max": 34, "label": "Defensora", "description": "A arma se movimenta para aparar ataques contra você. Você recebe +2 na Defesa."},
    {"d100Min": 35, "d100Max": 36, "label": "Destruidora", "description": "Se usada contra construtos e objetos (com a manobra quebrar), a arma fornece +2 no teste de ataque e causa +2d8 de dano."},
    {"d100Min": 37, "d100Max": 38, "label": "Dilacerante", "description": "A arma inflige ferimentos profundos. Quando faz um acerto crítico com a arma, você causa +10 pontos de dano."},
    {"d100Min": 39, "d100Max": 40, "label": "Drenante", "description": "Quando você faz um acerto crítico em uma criatura viva, a criatura fica fraca e você ganha 2d10 pontos de vida temporários. Uma arma drenante emite um brilho púrpura."},
    {"d100Min": 41, "d100Max": 45, "label": "Elétrica", "description": "A arma causa +1d6 de dano de eletricidade. Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso e acertar o ataque, um raio atinge outra criatura em alcance curto, causando 3d8 pontos de dano de eletricidade. Uma arma elétrica emite faíscas e é coberta de arcos voltaicos."},
    {"d100Min": 46, "d100Max": 46, "label": "Energética", "description": "A arma tem sua parte perigosa (a lâmina de uma espada, a ponta de uma lança...) transformada em magia pura. Ela fornece +4 em testes de ataque, ignora 20 pontos de redução de dano, converte todo o dano causado para essência e emana luz como uma tocha. Pré-requisito: formidável. Conta como dois encantos. Para itens menores, role novamente."},
    {"d100Min": 47, "d100Max": 48, "label": "Excruciante", "description": "A arma inflige dor terrível. Uma criatura viva atingida fica fraca. Se já estiver fraca, mesmo por este efeito, fica debilitada (a condição máxima que esta arma pode causar)."},
    {"d100Min": 49, "d100Max": 53, "label": "Flamejante", "description": "A arma causa +1d6 de dano de fogo. Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso, em vez do ataque normal você dispara uma bola de fogo contra um alvo em alcance médio. O alvo sofre 6d6 pontos de dano. Um teste de Reflexos (CD For ou Des, à sua escolha) reduz à metade. Uma arma flamejante emana chamas como uma tocha."},
    {"d100Min": 54, "d100Max": 63, "label": "Formidável", "description": "A arma é encantada para desferir golpes precisos. Ela fornece +2 em testes de ataque e rolagens de dano."},
    {"d100Min": 64, "d100Max": 64, "label": "Lancinante", "description": "A arma inflige ferimentos mortais. Quando faz um acerto crítico com a arma, você causa +10 pontos de dano ou, além de multiplicar os dados de dano, multiplica também quaisquer bônus numéricos, a sua escolha. Este efeito substitui o efeito de dilacerante. Pré-requisito: dilacerante. Conta como dois encantos. Para itens menores, role novamente."},
    {"d100Min": 65, "d100Max": 72, "label": "Magnífica", "description": "A arma é encantada para desferir golpes perfeitos. Ela fornece +4 em testes de ataque e rolagens de dano. Pré-requisito: formidável. Conta como dois encantos. Para itens menores, role novamente."},
    {"d100Min": 73, "d100Max": 74, "label": "Piedosa", "description": "A arma causa +1d8 de dano, mas todo o dano causado é não letal. Você pode gastar 1 PM para desativar e ativar este encanto."},
    {"d100Min": 75, "d100Max": 76, "label": "Profana", "description": "A arma causa +2d8 de dano contra devotos de deuses que canalizam apenas energia positiva e criaturas bondosas (a critério do mestre). Uma arma profana emite luz rubra pulsante."},
    {"d100Min": 77, "d100Max": 78, "label": "Sagrada", "description": "A arma causa +2d8 de dano contra devotos de deuses que canalizam apenas energia negativa e criaturas malignas (a critério do mestre). Uma arma sagrada emite uma sutil luz pura."},
    {"d100Min": 79, "d100Max": 80, "label": "Sanguinária", "description": "Uma criatura viva atingida fica sangrando. A perda de PV por sangramento causada pela arma é cumulativa — uma criatura atingida duas vezes perde 2d6 PV por sangramento por rodada."},
    {"d100Min": 81, "d100Max": 82, "label": "Trovejante", "description": "A arma emite um trovão ribombante a cada golpe. Quando você faz um acerto crítico, a vítima fica atordoada por uma rodada (apenas uma vez por cena; Fort CD For ou Des, a sua escolha, evita)."},
    {"d100Min": 83, "d100Max": 84, "label": "Tumular", "description": "A arma causa +1d8 de dano de trevas. Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso, o bônus de dano aumenta para +2d8, mas você perde 1d8 pontos de vida. Uma arma tumular drena o calor ao redor."},
    {"d100Min": 85, "d100Max": 88, "label": "Veloz", "description": "Você recebe a habilidade Ataque Extra, do guerreiro, mas só pode usá-la com esta arma. Se já a possui, em vez disso, o custo para usá-la com esta arma diminui em –1 PM."},
    {"d100Min": 89, "d100Max": 90, "label": "Venenosa", "description": "Uma vez por rodada, quando ataca, você pode gastar 2 PM. Se fizer isso e acertar o ataque, a vítima fica envenenada, perdendo 1d12 pontos de vida por rodada durante 3 rodadas. Uma arma venenosa verte um líquido verde e viscoso."},
    {"d100Min": 91, "d100Max": 100, "label": "Arma específica", "description": "Veja a Tabela 8-9"}
]

treasure_entities.append({
    "id": "tabela-8-8-armas-magicas",
    "name": "Tabela 8-8: Armas Mágicas",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 5,
    "threatLevelMax": 20,
    "threatLevelLabel": "Mágico (d100)",
    "summary": "Tabela oficial de encantos mágicos para armas (menores, médios e maiores).",
    "description": "Para gerar uma arma mágica aleatoriamente, role na Tabela 8-4 para definir o tipo de arma. Então role na tabela a seguir para determinar seus encantos. Role uma vez para itens menores, duas para médios e três vezes para itens maiores.",
    "entries": tabela_8_8_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 336,
        "section": "Capítulo 8: Tabela 8-8 - Armas Mágicas",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "armas mágicas", "encantos", "d%", "d100"]
})

tabela_8_9_entries = [
    {"d100Min": 1, "d100Max": 5, "label": "Azagaia dos relâmpagos", "description": "Quando arremessada, esta azagaia se transforma em um Relâmpago (8d6 de dano de eletricidade numa linha com alcance médio; CD For ou Des a sua escolha). Quando atinge o fim do alcance ela volta a ser uma azagaia e volta para você no fim do turno. Preço: T$ 30.000."},
    {"d100Min": 6, "d100Max": 15, "label": "Espada baronial", "description": "Esta espada longa de guarda reta fornece +1 em testes de ataque e rolagens de dano. Este bônus aumenta em +1 se você possuir um código de conduta (de honra, do herói...), for devoto de Khalmyr ou for treinado em Nobreza. Os bônus são cumulativos. Preço: T$ 30.000."},
    {"d100Min": 16, "d100Max": 25, "label": "Lâmina da luz", "description": "De lâmina prateada e reluzente, esta espada bastarda formidável é concedida a cavaleiros da Luz de honra e virtude comprovadas. Você pode gastar uma ação de movimento e 2 PM para erguer a lâmina da luz acima de sua cabeça. Se fizer isso, ela irradia luz brilhante em alcance médio até o fim da cena. Todos os inimigos dentro da luz ficam ofuscados. Preço: T$ 45.000."},
    {"d100Min": 26, "d100Max": 30, "label": "Lança animalesca", "description": "Espinhos e folhas vivas brotam desta lança formidável. Se você usar a habilidade Forma Selvagem, aplica o bônus de +2 em ataque e dano da lança animalesca em suas armas naturais. Preço: T$ 45.000."},
    {"d100Min": 31, "d100Max": 35, "label": "Maça do terror", "description": "Esta maça formidável é feita com um osso e um crânio e permite que você lance a magia Amedrontar (CD For ou Car a sua escolha). Caso já conheça a magia, o custo para lançá-la diminui em –1 PM. Preço: T$ 45.000."},
    {"d100Min": 36, "d100Max": 40, "label": "Florete fugaz", "description": "Este florete formidável tem o cabo e a guarda trabalhados com prata e pedrarias. Quando usa a ação agredir, você pode gastar 1 PM. Se fizer isso e acertar um crítico no turno, pode fazer um ataque adicional contra a mesma criatura. Preço: T$ 50.000."},
    {"d100Min": 41, "d100Max": 45, "label": "Cajado da destruição", "description": "Este bordão formidável escuro e reforçado com ponteiras de metal é procurado por conjuradores de batalha. Conta como um cajado arcano. Além dos benefícios desse esotérico, quando você lança uma magia de dano, ela causa +1 ponto de dano por dado. Preço: T$ 60.000."},
    {"d100Min": 46, "d100Max": 50, "label": "Cajado da vida", "description": "Este bordão formidável branco com runas prateadas é valorizado por curandeiros. Conta como um cajado arcano, mas afeta magias divinas. Além disso, quando você lança uma magia de cura, ela cura +2 pontos de vida por dado. Preço: T$ 60.000."},
    {"d100Min": 51, "d100Max": 55, "label": "Machado silvestre", "description": "O cabo e a lâmina deste machado de batalha formidável são cobertos de gravuras representando plantas e animais selvagens. Quando você usa o machado silvestre em um ambiente ermo e ao ar livre, causa +1d8 de dano e recebe o poder Trespassar. Caso já possua este poder, pode utilizá-lo sem pagar pontos de mana. Preço: T$ 70.000."},
    {"d100Min": 56, "d100Max": 60, "label": "Martelo de Doherimm", "description": "Este martelo de guerra formidável é feito de pedra e aço. Quando empunhado por um anão, adquire o encanto arremesso e aumenta seu dano em +1d8 (ou +2d8 se usado contra criaturas Grandes ou maiores). Preço: T$ 70.000."},
    {"d100Min": 61, "d100Max": 67, "label": "Arco do poder", "description": "O arco do poder conta como um arco longo formidável, mas parece apenas o corpo de um arco — não tem corda e não aceita flechas. Contudo, quando você o empunha e faz o gesto de puxar a corda inexistente, o arco cria uma corda e uma flecha de energia dourada: Flecha Normal (3d8 essência), Flecha Piedosa (4d8 não letal), Flecha Explosiva (3d6 fogo em área) ou Flecha-Rede (imobiliza). Preço: T$ 90.000."},
    {"d100Min": 68, "d100Max": 72, "label": "Língua do deserto", "description": "Esta cimitarra formidável é originária do Deserto da Perdição. Você pode gastar uma ação de movimento e 1 PM para transformar a lâmina dela em chamas até o fim da cena. Nessa condição, o dano da arma aumenta em um passo e passa a ser do tipo fogo. Você pode gastar uma ação de movimento e 2 PM para fazer as chamas brilharem com muita força. Isso deixa os inimigos em alcance curto desprevenidos por uma rodada. Preço: T$ 90.000."},
    {"d100Min": 73, "d100Max": 77, "label": "Besta explosiva", "description": "Esta besta pesada formidável é feita de madeira escurecida. Quando usa uma besta explosiva, você pode gastar 3 PM para transformar o virote disparado por ela em uma Bola de Fogo (6d6 de dano de fogo). Preço: T$ 100.000."},
    {"d100Min": 78, "d100Max": 82, "label": "Punhal sszzaazita", "description": "Esta adaga assassina formidável venenosa tem lâmina negra e ondulada. Você pode gastar uma ação padrão e 2 PM para transformar o punhal sszzaazita em um objeto inofensivo de tamanho similar, como uma colher ou pena. Nenhuma magia é capaz de detectar essa transformação. Preço: T$ 100.000."},
    {"d100Min": 83, "d100Max": 87, "label": "Espada sortuda", "description": "Esta espada curta formidável é cravejada de brilhantes. Você recebe +2 nos testes de resistência e, quando faz um teste, pode gastar 3 PM para rolá-lo novamente. Se possuir o poder Sortudo, em vez disso seu custo diminui em –1 PM. Preço: T$ 110.000."},
    {"d100Min": 88, "d100Max": 92, "label": "Avalanche", "description": "Este machado de guerra de gelo eterno congelante formidável fornece redução de fogo 10. Você pode gastar uma ação padrão e 6 PM para brandi-lo acima de sua cabeça e invocar uma tempestade de gelo que afeta alcance curto ao seu redor (3d6 impacto + 3d6 frio por rodada). Preço: T$ 140.000."},
    {"d100Min": 93, "d100Max": 95, "label": "Cajado do poder", "description": "Este bordão defensor magnífico tem cabo reto e liso, com uma joia cintilante na ponta. Conta como um cajado arcano. Além dos benefícios desse esotérico, o custo de suas magias arcanas diminui em –1 PM e a CD para resistir a elas aumenta em +2. Preço: T$ 180.000."},
    {"d100Min": 96, "d100Max": 100, "label": "Vingadora sagrada", "description": "Esta espada longa formidável revela todo o seu poder apenas quando empunhada por um paladino. Se você for um paladino, recebe +5 em testes de ataque e rolagens de dano, o custo de seu Golpe Divino é reduzido em –1 PM e você e seus aliados em alcance curto recebem resistência a magia +5. Preço: T$ 200.000."}
]

treasure_entities.append({
    "id": "tabela-8-9-armas-especificas",
    "name": "Tabela 8-9: Armas Específicas",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 10,
    "threatLevelMax": 20,
    "threatLevelLabel": "Mágico Maior (d100)",
    "summary": "Tabela de armas mágicas lendárias e específicas com propriedades únicas em Arton.",
    "description": "Todas as armas específicas deste livro são itens maiores. Itens específicos não podem receber encantos.",
    "entries": tabela_8_9_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 337,
        "section": "Capítulo 8: Tabela 8-9 - Armas Específicas",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "armas específicas", "relíquias", "d%", "d100"]
})

tabela_8_10_entries = [
    {"d100Min": 1, "d100Max": 6, "label": "Abascanto", "description": "Você recebe resistência a magia +5."},
    {"d100Min": 7, "d100Max": 10, "label": "Abençoado", "description": "Você recebe redução de trevas 10 e +5 em testes de resistência contra efeitos de necromancia. Um item abençoado é decorado com gravuras de símbolos sagrados de deuses do Bem."},
    {"d100Min": 11, "d100Max": 12, "label": "Acrobático", "description": "Você recebe +5 em Acrobacia e ignora a penalidade de armadura do item para testes dessa perícia."},
    {"d100Min": 13, "d100Max": 14, "label": "Alado", "description": "Você pode gastar 2 PM para fazer asas emergirem de suas costas e receber deslocamento de voo 12m com duração sustentada."},
    {"d100Min": 15, "d100Max": 16, "label": "Animado", "description": "Você pode gastar uma ação de movimento e 1 PM para fazer o escudo flutuar ao seu redor até o fim da cena. Você recebe o mesmo bônus na Defesa que receberia se estivesse empunhando o escudo, mas fica com as duas mãos livres. Apenas escudos. Para armaduras, role novamente."},
    {"d100Min": 17, "d100Max": 18, "label": "Assustador", "description": "Você pode gastar uma ação de movimento e 2 PM para gerar uma onda de medo. Inimigos em alcance curto devem passar num teste de Vontade (CD Car) ou ficarão abalados até o fim da cena. Um item assustador possui manchas de sangue, ossos pendurados e outras decorações horripilantes."},
    {"d100Min": 19, "d100Max": 22, "label": "Cáustica", "description": "Você recebe redução de ácido 10 e pode gastar uma ação de movimento e 2 PM para fazer o item gotejar ácido. Se fizer isso, seus ataques causam +1d4 de dano de ácido até o fim da cena."},
    {"d100Min": 23, "d100Max": 32, "label": "Defensor", "description": "O item é encantado para desviar golpes. O bônus na Defesa do item aumenta em +2."},
    {"d100Min": 33, "d100Max": 34, "label": "Escorregadio", "description": "Você recebe +10 em testes de Acrobacia para escapar e em testes de manobra contra agarrar. Um item escorregadio parece estar sempre coberto de óleo levemente gorduroso."},
    {"d100Min": 35, "d100Max": 36, "label": "Esmagador", "description": "Este escudo fornece +2 em ataques e dano e tem seu dano aumentado em um passo. Apenas escudos. Para armaduras, role novamente."},
    {"d100Min": 37, "d100Max": 38, "label": "Fantasmagórico", "description": "Você pode lançar a magia Manto de Sombras. Um item fantasmagórico é cinzento e esfumaçado."},
    {"d100Min": 39, "d100Max": 40, "label": "Fortificado", "description": "Você recebe 25% de chance (para escudos) e 50% de chance (para armaduras) de ignorar o dano extra de acertos críticos e ataques furtivos."},
    {"d100Min": 41, "d100Max": 44, "label": "Gélido", "description": "Você recebe redução de frio 10 e pode gastar uma ação de movimento e 2 PM para se cobrir de gelo até o fim da cena. Se fizer isso, recebe 10 PV temporários. Um item gélido é azulado e frio ao toque."},
    {"d100Min": 45, "d100Max": 54, "label": "Guardião", "description": "O item emite um campo de força que desvia ataques. O bônus na Defesa do item aumenta em +4. Pré-requisito: defensor. Conta como dois encantos. Para itens menores, role novamente."},
    {"d100Min": 55, "d100Max": 56, "label": "Hipnótico", "description": "Você pode gastar uma ação padrão e 3 PM para emitir luzes coloridas. Inimigos em alcance curto devem passar num teste de Vontade (CD Car) ou ficarão fascinados por 1d6 rodadas. O efeito termina se qualquer criatura afetada for atacada. Um item hipnótico é espalhafatoso e colorido."},
    {"d100Min": 57, "d100Max": 58, "label": "Ilusório", "description": "Você pode gastar uma ação de movimento e 1 PM para fazer o item adquirir a aparência de uma roupa comum, mas mantendo suas propriedades (bônus na Defesa, penalidade de armadura...). A magia Visão da Verdade revela o item disfarçado."},
    {"d100Min": 59, "d100Max": 62, "label": "Incandescente", "description": "Você recebe redução de fogo 10 e pode gastar uma ação de movimento e 2 PM para fazer o item emitir labaredas até o fim da cena. Se fizer isso, no início de cada um de seus turnos você causa 1d6 pontos de dano de fogo em todas as criaturas adjacentes. Um item incandescente é avermelhado e quente ao toque."},
    {"d100Min": 63, "d100Max": 68, "label": "Invulnerável", "description": "Você recebe redução de dano 2 (para escudos) ou 5 (para armaduras)."},
    {"d100Min": 69, "d100Max": 72, "label": "Opaco", "description": "Você recebe redução de ácido, eletricidade, fogo e frio 10. Um item opaco parece sem cor, totalmente comum e desinteressante."},
    {"d100Min": 73, "d100Max": 78, "label": "Protetor", "description": "Você recebe +2 em testes de resistência."},
    {"d100Min": 79, "d100Max": 80, "label": "Refletor", "description": "Uma vez por rodada, quando você é alvo de uma magia, pode gastar PM igual ao custo dela para refleti-la de volta ao conjurador. As características da magia (efeitos, CD...) se mantêm, mas você toma qualquer decisão exigida por ela. Um item refletor parece espelhado."},
    {"d100Min": 81, "d100Max": 84, "label": "Relampejante", "description": "Você recebe redução de eletricidade 10 e pode gastar uma ação de movimento e 2 PM para gerar arcos voltaicos até o fim da cena. Se fizer isso, qualquer criatura que o ataque em corpo a corpo sofre 2d6 pontos de dano de eletricidade. Um item relampejante é decorado com ouro, prata e cobre."},
    {"d100Min": 85, "d100Max": 86, "label": "Reluzente", "description": "Você pode gastar uma ação de movimento e 2 PM para emitir um clarão de luz. Todos os inimigos em alcance curto devem passar num teste de Reflexos (CD Car) ou ficarão cegos por uma rodada. Um item reluzente é polido e brilhante."},
    {"d100Min": 87, "d100Max": 88, "label": "Sombrio", "description": "Você recebe +5 em Furtividade e ignora a penalidade de armadura do item para testes dessa perícia. Um item sombrio é escuro, fosco e bem lubrificado, para não fazer barulho."},
    {"d100Min": 89, "d100Max": 90, "label": "Zeloso", "description": "Uma vez por rodada, se um aliado adjacente for alvo de um ataque, você pode gastar 1 PM para se tornar o alvo do ataque, que então é resolvido normalmente."},
    {"d100Min": 91, "d100Max": 100, "label": "Item específico", "description": "Veja a Tabela 8-11"}
]

treasure_entities.append({
    "id": "tabela-8-10-armaduras-escudos-magicos",
    "name": "Tabela 8-10: Armaduras & Escudos Mágicos",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 5,
    "threatLevelMax": 20,
    "threatLevelLabel": "Mágico (d100)",
    "summary": "Tabela oficial de encantos para armaduras e escudos mágicos.",
    "description": "Para gerar uma armadura ou escudo mágico aleatoriamente, role na Tabela 8-4 para definir o tipo de armadura ou escudo. Então role na tabela a seguir para determinar seus encantos.",
    "entries": tabela_8_10_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 339,
        "section": "Capítulo 8: Tabela 8-10 - Armaduras & Escudos Mágicos",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "armaduras mágicas", "escudos mágicos", "encantos", "d%", "d100"]
})

tabela_8_11_entries = [
    {"d100Min": 1, "d100Max": 10, "label": "Cota élfica", "description": "Composta de anéis finíssimos, esta cota de malha defensora de mitral parece ser feita de seda. Ela permite que você aplique sua Destreza na Defesa como se fosse uma armadura leve. Preço: T$ 30.000."},
    {"d100Min": 11, "d100Max": 20, "label": "Couro de monstro", "description": "Usado por chefes bárbaros das Montanhas Sanguinárias, este gibão de peles defensor é feito do couro de monstros, como basiliscos e serpes. Se você usar o poder Ataque Poderoso ou fizer uma investida, recebe um bônus de +2d6 nas rolagens de dano. Preço: T$ 36.000."},
    {"d100Min": 21, "d100Max": 25, "label": "Escudo do conjurador", "description": "Este escudo leve defensor tem uma pequena tira de couro na parte interna, sobre a qual um conjurador pode lançar uma magia. A magia não surte efeito na hora; em vez disso, fica inscrita na tira. A tira pode então ser lida como um pergaminho, descarregando a magia em seus alvos/área. Uma vez que a magia seja descarregada, outra pode ser armazenada. Preço: T$ 45.000."},
    {"d100Min": 26, "d100Max": 32, "label": "Loriga do centurião", "description": "Esta loriga segmentada defensora é dourada com detalhes em vermelho e possui o símbolo de Tauron, antigo Deus da Força, gravado no peitoral. Se estiver liderando uma ou mais criaturas (em termos de jogo, se estiver usando o poder Comandar ou similar), seus ataques corpo a corpo causam +2d6 de fogo. Preço: T$ 45.000."},
    {"d100Min": 33, "d100Max": 42, "label": "Manto da noite", "description": "Este couro batido ajustado defensor sombrio é negro com partes metálicas foscas. Quando usa esta armadura, você não sofre penalidade em testes de Furtividade por se mover em seu deslocamento normal e a penalidade que você sofre em testes de Furtividade por atacar diminui para –10. Preço: T$ 45.000."},
    {"d100Min": 43, "d100Max": 49, "label": "Couraça do comando", "description": "Esta couraça banhada a ouro sob medida defensora irradia uma aura de autoridade. Você recebe +1 em Carisma. Se usar o poder Comandar, o bônus fornecido aumenta para +2. Preço: T$ 45.000."},
    {"d100Min": 50, "d100Max": 59, "label": "Baluarte anão", "description": "Esta armadura completa reforçada defensora de adamante fornece proteção sem igual. Se você não se deslocar em seu turno, a RD que ela fornece aumenta para 10 até seu próximo turno. Preço: T$ 50.000."},
    {"d100Min": 60, "d100Max": 66, "label": "Escudo espinhoso", "description": "Este escudo pesado defensor é coberto de espinhos. Você pode gastar uma ação de movimento e 2 PM para disparar um espinho em um alvo em alcance curto. O espinho acerta automaticamente e causa 1d10+2 pontos de dano de perfuração. Preço: T$ 50.000."},
    {"d100Min": 67, "d100Max": 76, "label": "Escudo do leão", "description": "Este escudo pesado defensor é forjado como uma cabeça de leão rugindo. Uma vez por rodada, você pode gastar 2 PM para fazer a cabeça criar vida e morder uma criatura adjacente. A mordida acerta automaticamente e causa 2d6+2 pontos de dano de perfuração. Preço: T$ 50.000."},
    {"d100Min": 77, "d100Max": 83, "label": "Carapaça demoníaca", "description": "Esta armadura completa macabra reforçada guardiã é forjada para fazer com que o usuário pareça um demônio. Se você for devoto de uma divindade que canaliza apenas energia negativa, os seus ataques corpo a corpo causam +1d8 de dano de trevas. Preço: T$ 63.000."},
    {"d100Min": 84, "d100Max": 88, "label": "Escudo do eclipse", "description": "Este escudo pesado defensor é completamente negro e parece absorver a luz. Ele fornece redução de trevas 10 e causa +1d8 de dano de trevas num ataque. Além disso, você pode gastar uma ação de movimento e 2 PM para lançar Escuridão. Preço: T$ 70.000."},
    {"d100Min": 89, "d100Max": 93, "label": "Escudo de Azgher", "description": "Este escudo pesado guardião é forjado na forma de um sol estilizado. Você pode gastar uma ação padrão e 10 PM para fazê-lo emitir uma luz brilhante e quente num cone com alcance curto. A luz gera os efeitos da magia Visão da Verdade e causa 6d6 pontos de dano de fogo em todos os seus inimigos. Preço: T$ 140.000."},
    {"d100Min": 94, "d100Max": 100, "label": "Armadura da luz", "description": "Esta armadura completa banhada a ouro reforçada guardiã zelosa possui o símbolo de Khalmyr gravado no peitoral. Se você possuir um código de conduta ou for devoto de uma divindade que canaliza apenas energia positiva, recebe redução de dano igual ao seu Carisma. Preço: T$ 150.000."}
]

treasure_entities.append({
    "id": "tabela-8-11-armaduras-escudos-especificos",
    "name": "Tabela 8-11: Armaduras & Escudos Específicos",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 10,
    "threatLevelMax": 20,
    "threatLevelLabel": "Mágico Maior (d100)",
    "summary": "Tabela de armaduras e escudos lendários e específicos de Arton.",
    "description": "Todas as armaduras e escudos específicos deste livro são itens maiores. Itens específicos não podem receber encantos.",
    "entries": tabela_8_11_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 340,
        "section": "Capítulo 8: Tabela 8-11 - Armaduras & Escudos Específicos",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "armaduras específicas", "escudos específicos", "relíquias", "d%", "d100"]
})

tabela_8_12_entries = [
    {"d100Min": 1, "d100Max": 1, "label": "Abençoar Alimentos (óleo)", "description": "T$ 30"},
    {"d100Min": 2, "d100Max": 3, "label": "Área Escorregadia (granada)", "description": "T$ 30"},
    {"d100Min": 4, "d100Max": 6, "label": "Arma Mágica (óleo)", "description": "T$ 30"},
    {"d100Min": 7, "d100Max": 7, "label": "Compreensão", "description": "T$ 30"},
    {"d100Min": 8, "d100Max": 15, "label": "Curar Ferimentos (2d8+2 PV)", "description": "T$ 30"},
    {"d100Min": 16, "d100Max": 18, "label": "Disfarce Ilusório", "description": "T$ 30"},
    {"d100Min": 19, "d100Max": 20, "label": "Escuridão (óleo)", "description": "T$ 30"},
    {"d100Min": 21, "d100Max": 22, "label": "Luz (óleo)", "description": "T$ 30"},
    {"d100Min": 23, "d100Max": 24, "label": "Névoa (granada)", "description": "T$ 30"},
    {"d100Min": 25, "d100Max": 26, "label": "Primor Atlético", "description": "T$ 30"},
    {"d100Min": 27, "d100Max": 28, "label": "Proteção Divina", "description": "T$ 30"},
    {"d100Min": 29, "d100Max": 30, "label": "Resistência a Energia", "description": "T$ 30"},
    {"d100Min": 31, "d100Max": 32, "label": "Sono", "description": "T$ 30"},
    {"d100Min": 33, "d100Max": 33, "label": "Suporte Ambiental", "description": "T$ 30"},
    {"d100Min": 34, "d100Max": 34, "label": "Tranca Arcana (óleo)", "description": "T$ 30"},
    {"d100Min": 35, "d100Max": 35, "label": "Visão Mística", "description": "T$ 30"},
    {"d100Min": 36, "d100Max": 36, "label": "Vitalidade Fantasma", "description": "T$ 30"},
    {"d100Min": 37, "d100Max": 38, "label": "Escudo da Fé (aprimoramento para duração cena)", "description": "T$ 120"},
    {"d100Min": 39, "d100Max": 40, "label": "Alterar Tamanho", "description": "T$ 270"},
    {"d100Min": 41, "d100Max": 42, "label": "Aparência Perfeita", "description": "T$ 270"},
    {"d100Min": 43, "d100Max": 43, "label": "Armamento da Natureza (óleo)", "description": "T$ 270"},
    {"d100Min": 44, "d100Max": 49, "label": "Bola de Fogo (granada)", "description": "T$ 270"},
    {"d100Min": 50, "d100Max": 51, "label": "Camuflagem Ilusória", "description": "T$ 270"},
    {"d100Min": 52, "d100Max": 53, "label": "Concentração de Combate (aprimoramento para duração cena)", "description": "T$ 270"},
    {"d100Min": 54, "d100Max": 62, "label": "Curar Ferimentos (4d8+4 PV)", "description": "T$ 270"},
    {"d100Min": 63, "d100Max": 66, "label": "Físico Divino", "description": "T$ 270"},
    {"d100Min": 67, "d100Max": 68, "label": "Mente Divina", "description": "T$ 270"},
    {"d100Min": 69, "d100Max": 70, "label": "Metamorfose", "description": "T$ 270"},
    {"d100Min": 71, "d100Max": 75, "label": "Purificação", "description": "T$ 270"},
    {"d100Min": 76, "d100Max": 77, "label": "Velocidade", "description": "T$ 270"},
    {"d100Min": 78, "d100Max": 79, "label": "Vestimenta da Fé (óleo)", "description": "T$ 270"},
    {"d100Min": 80, "d100Max": 80, "label": "Voz Divina", "description": "T$ 270"},
    {"d100Min": 81, "d100Max": 82, "label": "Arma Mágica (óleo; aprimoramento para bônus +3)", "description": "T$ 750"},
    {"d100Min": 83, "d100Max": 88, "label": "Curar Ferimentos (7d8+7 PV)", "description": "T$ 1.080"},
    {"d100Min": 89, "d100Max": 89, "label": "Físico Divino (aprimoramento para três atributos)", "description": "T$ 1.080"},
    {"d100Min": 90, "d100Max": 92, "label": "Invisibilidade (aprimoramento para duração cena)", "description": "T$ 1.080"},
    {"d100Min": 93, "d100Max": 96, "label": "Bola de Fogo (granada; aprimoramento para 10d6 de dano)", "description": "T$ 1.470"},
    {"d100Min": 97, "d100Max": 100, "label": "Curar Ferimentos (11d8+11 PV)", "description": "T$ 3.000"}
]

treasure_entities.append({
    "id": "tabela-8-12-pocoes",
    "name": "Tabela 8-12: Poções",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 1,
    "threatLevelMax": 20,
    "threatLevelLabel": "Geral (d100)",
    "summary": "Tabela oficial de poções, óleos e granadas mágicas de Tormenta20.",
    "description": "Poções e pergaminhos contêm o efeito de uma magia. Quando são ativados, geram o efeito dessa magia e então desaparecem. Uma poção é um líquido mágico armazenado em um frasco de vidro ou cerâmica. Poções que afetam objetos também são chamadas de óleos e poções que geram efeito em área também são chamadas de granadas.",
    "entries": tabela_8_12_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 341,
        "section": "Capítulo 8: Tabela 8-12 - Poções",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "poções", "óleos", "granadas", "d%", "d100"]
})

tabela_8_13_entries = [
    {"d100Min": 1, "d100Max": 2, "label": "Anel do sustento", "description": "Você não precisa comer ou beber e precisa dormir apenas duas horas por noite para descansar. Os efeitos do anel só se ativam após uma semana de uso. Preço: T$ 3.000."},
    {"d100Min": 3, "d100Max": 7, "label": "Bainha mágica", "description": "Esta bainha de couro curtido e prata muda de tamanho para acomodar qualquer arma corpo a corpo. Você pode lançar Arma Mágica em qualquer arma na bainha sem pagar seu custo em PM. Preço: T$ 3.000."},
    {"d100Min": 8, "d100Max": 12, "label": "Corda da escalada", "description": "Esta corda de 15m é bastante fina, mas forte o suficiente para suportar até seis criaturas Médias. Com um comando (uma ação de movimento), a corda se move em qualquer direção a 3m por rodada, fixando-se firmemente onde você quiser. Preço: T$ 3.000."},
    {"d100Min": 13, "d100Max": 14, "label": "Ferraduras da velocidade", "description": "Estas ferraduras de ferro aumentam o deslocamento da montaria em +6m. Preço: T$ 3.000."},
    {"d100Min": 15, "d100Max": 19, "label": "Garrafa da fumaça eterna", "description": "Esta garrafa de latão emite uma nuvem de fumaça densa quando destampada. A fumaça preenche um quadrado de 1,5m por rodada até cobrir uma área de 15m de raio. Preço: T$ 3.000."},
    {"d100Min": 20, "d100Max": 24, "label": "Gema da luminosidade", "description": "Esta gema esculpida emite luz brilhante em alcance médio ou um facho de luz que deixa criaturas cegas por 1d4 rodadas (Fort CD 17 evita). Preço: T$ 3.000."},
    {"d100Min": 25, "d100Max": 29, "label": "Manto élfico", "description": "Este manto de cor cinza-esverdeado muda de cor para combinar com o ambiente. Você recebe +5 em Furtividade. Preço: T$ 3.000."},
    {"d100Min": 30, "d100Max": 34, "label": "Mochila de carga", "description": "Esta mochila abre para um espaço extradimensional. Ela pode carregar até 50 espaços de itens sem alterar seu peso constante de 1 espaço. Preço: T$ 3.000."},
    {"d100Min": 35, "d100Max": 40, "label": "Brincos da sagacidade", "description": "Este par de brincos de safira aguça o raciocínio. Você recebe +1 em Inteligência (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 41, "d100Max": 46, "label": "Luvas da delicadeza", "description": "Estas luvas de pelica aguçam o tato. Você recebe +1 em Destreza (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 47, "d100Max": 52, "label": "Manoplas da força do ogro", "description": "Estas manoplas de couro reforçado com metal aumentam a força de quem as veste. Você recebe +1 em Força (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 53, "d100Max": 59, "label": "Manto da resistência", "description": "Este manto prateado protege seu usuário contra perigos. Você recebe +2 em testes de resistência. Preço: T$ 4.500."},
    {"d100Min": 60, "d100Max": 65, "label": "Manto do fascínio", "description": "Este manto de seda bordado torna o usuário atraente e carismático. Você recebe +1 em Carisma (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 66, "d100Max": 71, "label": "Pingente da sensatez", "description": "Este pingente de jade concede sabedoria e clareza mental. Você recebe +1 em Sabedoria (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 72, "d100Max": 77, "label": "Torque do vigor", "description": "Este colar rígido de metal fortalece a saúde do usuário. Você recebe +1 em Constituição (somente após um dia de uso). Preço: T$ 4.500."},
    {"d100Min": 78, "d100Max": 82, "label": "Chapéu do disfarce", "description": "Você pode lançar Disfarce Ilusório (CD Car), com o aprimoramento que inclui odores e sensações e muda o bônus em Enganação para disfarces para +20, sem pagar seu custo em PM. Preço: T$ 6.000."},
    {"d100Min": 83, "d100Max": 84, "label": "Flauta fantasma", "description": "Esta flauta de osso toca sozinha ao seu comando, gerando ilusões sonoras e efeitos de pavor. Preço: T$ 6.000."},
    {"d100Min": 85, "d100Max": 89, "label": "Lanterna da revelação", "description": "Esta lanterna de latão emite luz que revela criaturas e objetos invisíveis em alcance curto. Preço: T$ 6.000."},
    {"d100Min": 90, "d100Max": 96, "label": "Anel da proteção", "description": "Este anel desvia ataques contra seu usuário. Você recebe +2 de Defesa. Preço: T$ 9.000."},
    {"d100Min": 97, "d100Max": 98, "label": "Anel do escudo mental", "description": "Você recebe imunidade a magias e efeitos de adivinhação. Preço: T$ 9.000."},
    {"d100Min": 99, "d100Max": 100, "label": "Pingente da saúde", "description": "Este pingente de rubi concede imunidade a todas as doenças e venenos normais. Preço: T$ 9.000."}
]

treasure_entities.append({
    "id": "tabela-8-13-acessorios-menores",
    "name": "Tabela 8-13: Acessórios Menores",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 1,
    "threatLevelMax": 10,
    "threatLevelLabel": "Mágico Menor (d100)",
    "summary": "Tabela de acessórios mágicos de utilidade e bônus iniciais (menores).",
    "description": "Amuletos de proteção, anéis de invisibilidade, bolas de cristal, tapetes voadores... Todos os itens mágicos que não são armas, armaduras, escudos, poções ou pergaminhos são acessórios.",
    "entries": tabela_8_13_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 342,
        "section": "Capítulo 8: Tabela 8-13 - Acessórios Menores",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "acessórios menores", "d%", "d100"]
})

tabela_8_14_entries = [
    {"d100Min": 1, "d100Max": 4, "label": "Anel de telecinesia", "description": "Você pode lançar Telecinesia (CD Int). Caso já conheça a magia, o custo para lançá-la diminui em –1 PM. Preço: T$ 10.500."},
    {"d100Min": 5, "d100Max": 8, "label": "Bola de cristal", "description": "Esta pequena esfera revela pessoas e lugares distantes. Olhar através dela é uma ação completa e gera a magia Vidência (CD Sab). Preço: T$ 10.500."},
    {"d100Min": 9, "d100Max": 10, "label": "Caveira maldita", "description": "Esta pedra esculpida em formato de crânio gera o efeito da magia Profanar, com o crânio como ponto de origem. Mortos-vivos e devotos de deuses que canalizam apenas energia negativa na área de efeito recebem +2 em testes e Defesa. Preço: T$ 10.500."},
    {"d100Min": 11, "d100Max": 14, "label": "Botas aladas", "description": "Você pode gastar 2 PM para fazer asas brotarem dos calcanhares destas botas e receber deslocamento de voo 12m por uma rodada. Você pode gastar 1 PM no início de cada um de seus turnos para manter esse efeito. Preço: T$ 15.000."},
    {"d100Min": 15, "d100Max": 18, "label": "Braceletes de bronze", "description": "Estes braceletes geram um campo de força invisível, porém tangível. Você recebe +4 na Defesa, cumulativo com outros itens mágicos, mas não com armaduras. Preço: T$ 16.500."},
    {"d100Min": 19, "d100Max": 24, "label": "Anel da energia", "description": "Você recebe +5 PM (somente após um dia de uso). Preço: T$ 21.000."},
    {"d100Min": 25, "d100Max": 30, "label": "Anel da vitalidade", "description": "Você recebe +10 PV (somente após um dia de uso). Preço: T$ 21.000."},
    {"d100Min": 31, "d100Max": 34, "label": "Anel de invisibilidade", "description": "Ao colocar este anel de prata, você fica sob efeito de Invisibilidade. O efeito termina se você fizer um ataque ou lançar uma magia ofensiva, mas você pode tirar e recolocar o anel (uma ação padrão) para que ele volte a funcionar. Preço: T$ 21.000."},
    {"d100Min": 35, "d100Max": 38, "label": "Braçadeiras do arqueiro", "description": "Você recebe +2 em rolagens de dano com armas de ataque à distância (cumulativo com outros itens). Preço: T$ 21.000."},
    {"d100Min": 39, "d100Max": 42, "label": "Brincos de Marah", "description": "Este par de brincos brancos é abençoado pela Deusa da Paz. A primeira criatura que o atacar em uma cena deve fazer um teste de Vontade (CD Car). Se falhar, perderá a ação. Preço: T$ 21.000."},
    {"d100Min": 43, "d100Max": 46, "label": "Faixas do pugilista", "description": "Estes enrolamentos de pano para as mãos e antebraços concedem +2 nos testes de ataque e rolagens de dano desarmados. Preço: T$ 21.000."},
    {"d100Min": 47, "d100Max": 50, "label": "Manto da aranha", "description": "Este manto de teia negra concede deslocamento de escalada igual ao seu deslocamento terrestre e imunidade total a teias. Preço: T$ 21.000."},
    {"d100Min": 51, "d100Max": 54, "label": "Vassoura voadora", "description": "Esta vassoura de palha permite voar pelo ar como um veículo místico para 1 criatura (deslocamento de voo 18m). Preço: T$ 21.000."},
    {"d100Min": 55, "d100Max": 58, "label": "Símbolo abençoado", "description": "Este símbolo sagrado emite aura divina. Aumenta a CD para resistir às suas magias divinas em +2. Preço: T$ 21.000."},
    {"d100Min": 59, "d100Max": 64, "label": "Amuleto da robustez", "description": "Este disco com corrente de ouro é usado como um colar. Você recebe +2 em Constituição (somente após um dia de uso). Preço: T$ 25.500."},
    {"d100Min": 65, "d100Max": 68, "label": "Botas velozes", "description": "Você recebe +3m em seu deslocamento e pode lançar Velocidade (apenas sobre você mesmo). Preço: T$ 25.500."},
    {"d100Min": 69, "d100Max": 74, "label": "Cinto da força do gigante", "description": "Este cinto largo é feito de couro com rebites de ferro. Você recebe +2 em Força (somente após um dia de uso). Preço: T$ 25.500."},
    {"d100Min": 75, "d100Max": 80, "label": "Coroa majestosa", "description": "Esta coroa cravejada de joias irradia nobreza. Você recebe +2 em Carisma (somente após um dia de uso). Preço: T$ 25.500."},
    {"d100Min": 81, "d100Max": 86, "label": "Estola da serenidade", "description": "Esta vestimenta de tecido fino inspira paz e sabedoria. Você recebe +2 em Sabedoria (somente após um dia de uso). Preço: T$ 25.500."},
    {"d100Min": 87, "d100Max": 88, "label": "Manto do morcego", "description": "Este manto negro em forma de asas concede voo, +5 em Furtividade e permite transformar-se em morcego sob comando. Preço: T$ 25.500."},
    {"d100Min": 89, "d100Max": 94, "label": "Pulseiras da celeridade", "description": "Estas pulseiras de prata aguçam os reflexos. Você recebe +2 em Destreza (somente após um dia de uso). Preço: T$ 25.500."},
    {"d100Min": 95, "d100Max": 100, "label": "Tiara da sapiência", "description": "Esta tiara com gema azul expande o intelecto. Você recebe +2 em Inteligência (somente após um dia de uso). Preço: T$ 25.500."}
]

treasure_entities.append({
    "id": "tabela-8-14-acessorios-medios",
    "name": "Tabela 8-14: Acessórios Médios",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 11,
    "threatLevelMax": 16,
    "threatLevelLabel": "Mágico Médio (d100)",
    "summary": "Tabela de acessórios mágicos intermediários e atributos em Arton.",
    "description": "Role 1d100 quando sortear um Acessório Mágico Médio.",
    "entries": tabela_8_14_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 343,
        "section": "Capítulo 8: Tabela 8-14 - Acessórios Médios",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "acessórios médios", "d%", "d100"]
})

tabela_8_15_entries = [
    {"d100Min": 1, "d100Max": 2, "label": "Elmo do teletransporte", "description": "Este elmo reluzente permite lançar a magia Teletransporte 1 vez por dia sem gasto de PM. Preço: T$ 30.000."},
    {"d100Min": 3, "d100Max": 4, "label": "Gema da telepatia", "description": "Esta gema preciosa permite leitura de mentes e comunicação telepática sem limite de distância. Preço: T$ 30.000."},
    {"d100Min": 5, "d100Max": 9, "label": "Gema elemental", "description": "Esta gema bruta contém o poder de um plano elemental. Ao ser quebrada, invoca um Elemental Grande sob seu comando. Preço: T$ 30.000."},
    {"d100Min": 10, "d100Max": 15, "label": "Manual da saúde corporal", "description": "Este livro raro descreve exercícios e dietas místicas. Se passar uma semana estudando o manual, seu valor de Constituição aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 16, "d100Max": 21, "label": "Manual do bom exercício", "description": "Este livro raro contém rotinas de treino lendárias. Se passar uma semana estudando o manual, seu valor de Força aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 22, "d100Max": 27, "label": "Manual dos movimentos precisos", "description": "Este livro raro ensina acrobacias e agilidade extrema. Se passar uma semana estudando o manual, seu valor de Destreza aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 28, "d100Max": 34, "label": "Medalhão de Lena", "description": "Este medalhão abençoado pela Deusa da Vida concede Cura Acelerada 10 e ressurreição automática 1 vez em caso de morte. Preço: T$ 30.000."},
    {"d100Min": 35, "d100Max": 40, "label": "Tomo da compreensão", "description": "Este compêndio traz segredos da intuição e espiritualidade. Se passar uma semana estudando o tomo, seu valor de Sabedoria aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 41, "d100Max": 46, "label": "Tomo da liderança e influência", "description": "Este tomo versa sobre retórica, etiqueta e magnetismo pessoal. Se passar uma semana estudando o tomo, seu valor de Carisma aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 47, "d100Max": 52, "label": "Tomo dos grandes pensamentos", "description": "Este tomo denso contêm teoremas arcanos e filosóficos. Se passar uma semana estudando o tomo, seu valor de Inteligência aumenta permanentemente em +1. Preço: T$ 30.000."},
    {"d100Min": 53, "d100Max": 57, "label": "Anel refletor", "description": "Este aro de platina é poderoso contra conjuradores. Uma vez por rodada, quando você é alvo de uma magia, pode gastar PM igual ao custo dela para refleti-la de volta ao seu conjurador. Preço: T$ 51.000."},
    {"d100Min": 58, "d100Max": 60, "label": "Cinto do campeão", "description": "Este cinturão de ouro é cravejado de joias e possui gravuras de gladiadores. Você recebe +1 em Força e a habilidade Briga. Caso já a possua, seu dano desarmado será calculado como se você possuísse quatro níveis de lutador a mais. Preço: T$ 51.000."},
    {"d100Min": 61, "d100Max": 67, "label": "Colar guardião", "description": "Este diamante lapidado preso em uma corrente de platina deflete ataques contra seu usuário. Você recebe +5 na Defesa. Preço: T$ 51.000."},
    {"d100Min": 68, "d100Max": 72, "label": "Estatueta animista", "description": "Esta pequena escultura de jade pode se transformar em uma criatura real sob seu comando para lutar ao seu lado por 1 cena. Preço: T$ 51.000."},
    {"d100Min": 73, "d100Max": 77, "label": "Anel da liberdade", "description": "Forjado em ouro, este anel é uma relíquia da Igreja de Valkaria. Você fica permanentemente sob efeito de Libertação (imunidade a imobilização, paralisia e lentidão). Preço: T$ 60.000."},
    {"d100Min": 78, "d100Max": 82, "label": "Tapete voador", "description": "Este tapete ricamente bordado flutua pelo ar ao seu comando místico como um veículo voador capaz de carregar até 4 pessoas (deslocamento 12m). Preço: T$ 60.000."},
    {"d100Min": 83, "d100Max": 87, "label": "Braceletes de ouro", "description": "Como braceletes de bronze, mas fornece +8 na Defesa, não cumulativo com braceletes de bronze. Preço: T$ 64.500."},
    {"d100Min": 88, "d100Max": 89, "label": "Espelho da oposição", "description": "Este espelho emoldurado cria uma duplicata idêntica e hostil de qualquer criatura que se refletir nele. Preço: T$ 75.000."},
    {"d100Min": 90, "d100Max": 94, "label": "Robe do arquimago", "description": "Este veste magnífica fornece +5 na Defesa, resistência a magia +5 e reduz o custo de todas as suas magias arcanas em -1 PM. Preço: T$ 90.000."},
    {"d100Min": 95, "d100Max": 96, "label": "Orbe das tempestades", "description": "Esta esfera de cristal negro permite controlar o clima e invocar tempestades e raios devastadores na região. Preço: T$ 97.500."},
    {"d100Min": 97, "d100Max": 98, "label": "Anel da regeneração", "description": "Você recebe Cura Acelerada 5 (somente após um dia de uso). Preço: T$ 150.000."},
    {"d100Min": 99, "d100Max": 100, "label": "Espelho do aprisionamento", "description": "Este espelho místico aprisiona corpos e almas de quem olhar para ele em 1d4+1 dimensões espelhadas. Preço: T$ 150.000."}
]

treasure_entities.append({
    "id": "tabela-8-15-acessorios-maiores",
    "name": "Tabela 8-15: Acessórios Maiores",
    "category": "tesouro",
    "subcategory": SUB_MAGICOS,
    "threatLevelMin": 17,
    "threatLevelMax": 20,
    "threatLevelLabel": "Mágico Maior (d100)",
    "summary": "Tabela de acessórios mágicos de poder supremo, tomos de atributos e relíquias míticas.",
    "description": "Role 1d100 quando sortear um Acessório Mágico Maior.",
    "entries": tabela_8_15_entries,
    "sources": [{
        "book": "Tormenta20 - Jogo do Ano",
        "page": 343,
        "section": "Capítulo 8: Tabela 8-15 - Acessórios Maiores",
        "version": "1.3"
    }],
    "tags": ["tesouro", "itens mágicos", "acessórios maiores", "artefatos", "d%", "d100"]
})

# Salvando a lista de entidades no arquivo de tesouros
with open("data/categories/tesouros.json", "w", encoding="utf-8") as f:
    json.dump(treasure_entities, f, ensure_ascii=False, indent=2)

print(f"[OK] Tabelas de Tesouros extraidas e salvas: {len(treasure_entities)} registros em data/categories/tesouros.json")
