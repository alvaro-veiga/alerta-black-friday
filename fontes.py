# -*- coding: utf-8 -*-
"""Leitura das ofertas nos sites."""
import json
import re
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def next_data(pagina):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', pagina, re.S)
    return json.loads(m.group(1))["props"]["pageProps"] if m else {}


def _foto_promobit(caminho):
    if not caminho:
        return None
    if caminho.startswith("http"):
        return caminho
    if not caminho.startswith("/"):
        caminho = "/static/p/" + caminho
    return "https://www.promobit.com.br" + caminho


def promobit(paginas=3):
    """Ofertas mais recentes do Promobit (12 por página)."""
    ofertas, after = [], None
    for _ in range(paginas):
        url = "https://www.promobit.com.br/promocoes/recentes/"
        if after:
            url += "?after=" + urllib.parse.quote(after)
        so = next_data(baixar(url)).get("serverOffers") or {}
        for o in so.get("offers", []):
            ofertas.append({
                "id": "pb-%s" % o.get("offerId"),
                "titulo": o.get("offerTitle", ""),
                "preco": o.get("offerPrice"),
                "cupom": o.get("offerCoupon"),
                "loja": o.get("storeName", ""),
                "foto": _foto_promobit(o.get("offerPhoto")),
                "link": "https://www.promobit.com.br/oferta/%s/" % o.get("offerSlug", ""),
            })
        after = so.get("after")
        if not after:
            break
    return ofertas


def _preco_no_titulo(t):
    m = re.search(r"R\$\s?([\d.]+(?:,\d{2})?)", t)
    if not m:
        return None
    try:
        return float(m.group(1).replace(".", "").replace(",", "."))
    except ValueError:
        return None


def pelando():
    """Ofertas recentes do Pelando (não traz preço, tenta tirar do título)."""
    import html
    pag = baixar("https://www.pelando.com.br/recentes")
    m = re.search(r'<script id="feed-schema" type="application/ld\+json">(.*?)</script>', pag, re.S)
    if not m:
        return []
    ofertas = []
    for p in json.loads(m.group(1)).get("mainEntity", {}).get("hasPart", []):
        titulo = html.unescape(p.get("name", ""))
        ofertas.append({
            "id": "pl-" + p.get("url", ""),
            "titulo": titulo,
            "preco": _preco_no_titulo(titulo),
            "cupom": None,
            "loja": "Pelando",
            "foto": None,
            "link": p.get("url", ""),
        })
    return ofertas


def kabum(termo):
    """Produtos disponíveis numa busca da Kabum, com o preço atual."""
    url = "https://www.kabum.com.br/busca/" + urllib.parse.quote(termo.replace(" ", "-"))
    dados = next_data(baixar(url)).get("data") or {}
    if isinstance(dados, str):
        dados = json.loads(dados)
    itens = []
    for x in (dados.get("catalogServer") or {}).get("data", []):
        if not x.get("available"):
            continue
        preco = x.get("priceWithDiscount") or x.get("price")
        oferta = x.get("offer") or {}
        if isinstance(oferta, dict) and oferta.get("priceWithDiscount"):
            preco = min(preco, oferta["priceWithDiscount"])
        itens.append({
            "id": "kb-%s" % x.get("code"),
            "titulo": x.get("name", ""),
            "preco": preco,
            "cupom": None,
            "loja": "KaBuM!",
            "foto": x.get("image"),
            "link": "https://www.kabum.com.br/produto/%s/%s" % (x.get("code"), x.get("friendlyName", "")),
        })
    return itens
