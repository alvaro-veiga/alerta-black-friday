# -*- coding: utf-8 -*-
"""Decide se uma oferta é de algum produto da lista."""
import re
import unicodedata

from produtos import LOJAS_PREFERIDAS, PRODUTOS


def normalizar(txt):
    txt = unicodedata.normalize("NFKD", txt or "")
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return " " + re.sub(r"\s+", " ", txt.lower()) + " "


def _tem(termo, texto):
    return normalizar(termo).strip(" ") in texto if termo.strip() else False


def combina(oferta):
    """Retorna o produto da lista que bate com a oferta, ou None."""
    t = normalizar(oferta["titulo"])
    for prod in PRODUTOS:
        if any(_tem(x, t) for x in prod["excluir"]):
            continue
        if not all(any(normalizar(p)[1:-1] in t for p in grupo) for grupo in prod["todas"]):
            continue
        preco = oferta.get("preco")
        # preço de R$ 0,01 é cupom/vitrine: não dá pra comparar, deixa passar
        if prod["max"] is not None and preco and preco > 1 and preco > prod["max"]:
            continue
        return prod
    return None


def loja_preferida(oferta):
    texto = normalizar(oferta.get("loja", "") + " " + oferta.get("titulo", ""))
    return any(l in texto for l in LOJAS_PREFERIDAS)


def formatar_preco(preco):
    if preco and preco > 1:
        s = "{:,.2f}".format(preco).replace(",", "X").replace(".", ",").replace("X", ".")
        return "R$ " + s
    return "preço na página"
