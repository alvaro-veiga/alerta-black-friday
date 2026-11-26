# -*- coding: utf-8 -*-
"""
Alerta de promoções da Black Friday.

Lê as ofertas novas do Promobit/Pelando a cada minuto e os preços da Kabum a
cada 3 minutos. Quando aparece algo da lista (produtos.py) dentro do preço,
toca no celular pelo app ntfy.

    python alerta.py            roda até apertar Ctrl+C
    python alerta.py --teste    uma passada só, sem avisar ninguém

Configuração por variável de ambiente:
    NTFY_TOPICO       nome do canal no app ntfy (ou arquivo topico_ntfy.txt)
    MODO              celular (padrão), pc ou ambos
    OUTRAS_LOJAS      silencioso (padrão), avisar ou ignorar
    DURACAO_MINUTOS   para sozinho depois de X minutos (0 = nunca)
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import avisos
import fontes
from filtros import combina, formatar_preco, loja_preferida
from produtos import KABUM_BUSCAS

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_ESTADO = os.path.join(PASTA, "estado")
ARQ_VISTOS = os.path.join(PASTA_ESTADO, "vistos.json")
ARQ_PRECOS = os.path.join(PASTA_ESTADO, "precos_kabum.json")
ARQ_LOG = os.path.join(PASTA, "achados.txt")

INTERVALO = int(os.environ.get("INTERVALO_SEGUNDOS", "60"))
KABUM_A_CADA = int(os.environ.get("KABUM_A_CADA_SEGUNDOS", "180"))
QUEDA_MINIMA = float(os.environ.get("QUEDA_MINIMA", "0.03"))
MODO = os.environ.get("MODO", "celular").lower()
OUTRAS_LOJAS = os.environ.get("OUTRAS_LOJAS", "silencioso").lower()
DURACAO = int(os.environ.get("DURACAO_MINUTOS", "0"))
BRT = timezone(timedelta(hours=-3))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def topico_ntfy():
    t = os.environ.get("NTFY_TOPICO", "").strip()
    if not t:
        try:
            with open(os.path.join(PASTA, "topico_ntfy.txt"), encoding="utf-8") as f:
                t = f.read().strip()
        except OSError:
            pass
    return t


def agora():
    return datetime.now(BRT).strftime("%d/%m %H:%M:%S")


def ler_json(caminho, padrao):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return padrao


def gravar_json(caminho, dados):
    os.makedirs(PASTA_ESTADO, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f)


def alertar(o, prod, silencioso, extra=""):
    preferida = loja_preferida(o)
    if not preferida and OUTRAS_LOJAS == "ignorar":
        return
    preco = formatar_preco(o.get("preco")) + extra
    cupom = " | cupom: %s" % o["cupom"] if o.get("cupom") else ""
    marca = "" if preferida else "(outra loja) "
    linha = "[%s] %s%s -> %s | %s | %s%s\n    %s" % (
        agora(), marca, prod["nome"], o["titulo"], preco, o["loja"], cupom, o["link"])
    urgente = bool(prod.get("prioridade")) and preferida
    print("\n" + ("!" * 60 if urgente else "-" * 60))
    print(linha, flush=True)
    with open(ARQ_LOG, "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    if silencioso or (not preferida and OUTRAS_LOJAS == "silencioso"):
        return
    texto = "%s | %s%s\n%s" % (preco, o["loja"], cupom, o["titulo"])
    if MODO in ("celular", "ambos"):
        avisos.celular(topico_ntfy(), prod["nome"], texto, o.get("link"), o.get("foto"), urgente)
    if MODO in ("pc", "ambos"):
        avisos.windows(prod["nome"], texto.replace("\n", " - ")[:200])
        avisos.bipe(urgente)
        if urgente:
            import webbrowser
            webbrowser.open(o["link"])


def passada_ofertas(vistos, silencioso):
    todas = []
    for nome, fonte in (("Promobit", fontes.promobit), ("Pelando", fontes.pelando)):
        try:
            todas += fonte()
        except Exception as e:
            print("  [%s] erro ao ler %s: %s" % (agora(), nome, e))
    achados = 0
    for o in todas:
        if o["id"] in vistos:
            continue
        vistos.add(o["id"])
        prod = combina(o)
        if prod:
            achados += 1
            alertar(o, prod, silencioso)
    return len(todas), achados


def passada_kabum(precos, silencioso):
    """Compara os preços da Kabum com os da última vez."""
    primeira_vez = not precos
    encontrados = {}
    for termo in KABUM_BUSCAS:
        try:
            for o in fontes.kabum(termo):
                encontrados[o["id"]] = o
        except Exception as e:
            print("  [%s] erro na Kabum (%s): %s" % (agora(), termo, e))
        time.sleep(1)
    achados = 0
    for o in encontrados.values():
        prod = combina(o)
        if not prod:
            continue
        antes = precos.get(o["id"])
        precos[o["id"]] = o["preco"]
        if primeira_vez:
            print("  Kabum hoje: %-38s %-12s %s" % (prod["nome"][:38], formatar_preco(o["preco"]), o["titulo"][:60]))
        elif antes is None:
            achados += 1
            alertar(o, prod, silencioso, " (anúncio novo)")
        elif o["preco"] <= antes * (1 - QUEDA_MINIMA):
            achados += 1
            alertar(o, prod, silencioso, " (era %s, caiu %d%%)" % (
                formatar_preco(antes), round((1 - o["preco"] / antes) * 100)))
    return len(encontrados), achados


def main():
    teste = "--teste" in sys.argv
    vistos = set() if teste else set(ler_json(ARQ_VISTOS, []))
    precos = {} if teste else ler_json(ARQ_PRECOS, {})
    fim = time.time() + DURACAO * 60 if DURACAO else None
    ultima_kabum = 0

    if MODO in ("celular", "ambos") and not topico_ntfy():
        print("AVISO: sem NTFY_TOPICO, o celular não vai tocar.")
    print("Alerta Black Friday ligado (modo %s). Ctrl+C para parar." % MODO, flush=True)

    while True:
        lidas, achados = passada_ofertas(vistos, teste)
        print("[%s] %d ofertas lidas, %d da sua lista" % (agora(), lidas, achados), flush=True)

        if time.time() - ultima_kabum >= KABUM_A_CADA:
            ultima_kabum = time.time()
            n, k = passada_kabum(precos, teste)
            print("[%s] Kabum: %d produtos conferidos, %d alertas" % (agora(), n, k), flush=True)

        if not teste:
            gravar_json(ARQ_VISTOS, sorted(vistos)[-5000:])
            gravar_json(ARQ_PRECOS, precos)
        if teste or (fim and time.time() + INTERVALO > fim):
            break
        time.sleep(INTERVALO)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nParado.")
