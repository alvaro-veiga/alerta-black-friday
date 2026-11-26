# -*- coding: utf-8 -*-
"""Lista de produtos vigiados. Edite à vontade.

Cada produto:
  todas   = grupos de palavras; precisa bater pelo menos UMA de cada grupo
  excluir = se aparecer qualquer uma no título, ignora
  max     = preço máximo em R$ (None = avisa qualquer preço)
  prioridade = toca com urgência no celular
"""

EXCLUIR_ACESSORIOS = ["capa", "capinha", "pelicula", "case", "carregador", "cabo"]

PRODUTOS = [
    {
        "nome": "★ Memória RAM Ballistix 8GB",
        "prioridade": True,
        "todas": [["ballistix"]],
        "excluir": [],
        "max": None,  # a Crucial parou de fabricar a Ballistix: avisa sempre
    },
    {
        "nome": "★ Memória RAM Crucial DDR4 8GB/16GB",
        "prioridade": True,
        "todas": [["crucial"], ["ddr4"], ["8gb", "16gb", "2x8"]],
        "excluir": ["notebook", "sodimm", "so-dimm", "ssd"],
        "max": 450,
    },
    {
        "nome": "SSD 1TB",
        "todas": [["ssd"], ["1tb", "1 tb", "1000gb"]],
        "excluir": ["externo", "portatil", "case", "gaveta", "adaptador"],
        "max": 550,
    },
    {
        "nome": "Placa de vídeo GDDR6 12GB+",
        "todas": [
            ["placa de video", "rtx", "radeon", " rx ", "arc "],
            ["3060 12", "rtx 3060", "4060 ti 16", "4070", "6700 xt", "6750 xt",
             "6800", "7600 xt", "7700 xt", "7800 xt", "7900", "9060 xt 16",
             "9070", "b580", "a770", "gddr6"],
        ],
        "excluir": ["gddr6x", "8gb", "notebook", "laptop", "gddr7"],
        "max": 2800,
    },
    {
        "nome": "Frigobar",
        "todas": [["frigobar", "mini geladeira", "minibar", "refrigerador compacto"]],
        "excluir": ["capa", "adesivo", "puxador", "borracha"],
        "max": 1300,
    },
    {
        "nome": "Monitor 144Hz+ 24 a 27\"",
        "todas": [
            ["monitor"],
            ["144hz", "144 hz", "165hz", "165 hz", "170hz", "180hz", "180 hz",
             "200hz", "240hz", "240 hz"],
            ['24"', "24 pol", "24'", "23.8", "23,8", '25"', "25 pol", '27"',
             "27 pol", "27'", " 24 ", " 27 "],
        ],
        "excluir": ["suporte", "braco articulado", "cabo"],
        "max": 1100,
    },
    {"nome": "iPhone 14", "todas": [["iphone 14"]], "excluir": EXCLUIR_ACESSORIOS, "max": 2800},
    {"nome": "iPhone 15", "todas": [["iphone 15"]], "excluir": EXCLUIR_ACESSORIOS, "max": 3300},
    {"nome": "iPhone 16", "todas": [["iphone 16"]], "excluir": EXCLUIR_ACESSORIOS, "max": 4300},
    {"nome": "iPhone 17", "todas": [["iphone 17", "iphone air"]], "excluir": EXCLUIR_ACESSORIOS, "max": 5500},
    {
        "nome": "Jogo PS5 AAA",
        "todas": [
            ["ps5", "playstation 5"],
            ["gta", "grand theft auto", "ghost of yotei", "spider-man", "spiderman",
             "god of war", "elden ring", "wukong", "resident evil", "death stranding",
             "call of duty", "black ops", "ea sports fc", "fc 26", "battlefield",
             "assassin", "hogwarts", "red dead", "final fantasy", "stellar blade",
             "silent hill", "monster hunter", "astro bot", "gran turismo",
             "mafia", "007", "borderlands", "expedition 33", "clair obscur",
             "the last of us", "horizon", "cyberpunk", "mortal kombat", "nba 2k",
             "ghost of tsushima", "doom", "metal gear", "wolverine", "forza"],
        ],
        "excluir": ["console", "controle", "dualsense", "headset", "slim",
                    "playstation portal", "capa", "skin"],
        "max": 220,
    },
]

# Lojas preferidas: só elas tocam. As outras ficam só anotadas.
LOJAS_PREFERIDAS = ["mercado livre", "mercadolivre", "kabum"]

# Buscas feitas direto na Kabum (preço real da loja).
KABUM_BUSCAS = [
    "ballistix",
    "memoria crucial ddr4 8gb",
    "ssd 1tb",
    "placa de video 12gb gddr6",
    "placa de video 16gb gddr6",
    "monitor gamer 27 144hz",
    "monitor gamer 24 165hz",
    "frigobar",
    "iphone",
]
