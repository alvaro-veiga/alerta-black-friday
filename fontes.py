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
