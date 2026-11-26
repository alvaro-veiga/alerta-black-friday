# Alerta Black Friday

Vigia promoções e toca no celular quando aparece algo da lista com preço bom.

- **Promobit e Pelando**: ofertas novas a cada 1 minuto
- **Kabum**: preço real da loja a cada 3 minutos (avisa queda de 3%+ ou anúncio novo)
- **Lojas preferidas**: Mercado Livre e Kabum tocam; as outras só ficam anotadas
- **Aviso**: push no app [ntfy](https://ntfy.sh) com nome, preço, foto e botão para abrir a oferta

## Produtos

Editar em [`produtos.py`](produtos.py): palavras-chave, exclusões e preço máximo de cada item.

## Rodando na nuvem (PC pode ficar desligado)

1. Instale o app **ntfy** no celular e assine um tópico com nome difícil de adivinhar.
2. No GitHub: *Settings → Secrets and variables → Actions → New repository secret*
   - nome: `NTFY_TOPICO`
   - valor: o nome do tópico
3. Em *Actions → alerta → Run workflow* para começar na hora.

O workflow roda por ~5h40 seguidas e o agendamento de hora em hora emenda a próxima execução.
O estado (ofertas já vistas e preços da Kabum) passa de uma execução para outra pelo cache.

Para parar: *Actions → alerta → ⋯ → Disable workflow*.

## Rodando no PC

```
python alerta.py            # roda até Ctrl+C
python alerta.py --teste    # uma passada, sem avisar
```

Ou dois cliques em `INICIAR_ALERTA.bat`. O tópico vai na variável `NTFY_TOPICO`
ou num arquivo `topico_ntfy.txt` (ignorado pelo git).

| Variável | Padrão | Opções |
|---|---|---|
| `MODO` | `celular` | `celular`, `pc`, `ambos` |
| `OUTRAS_LOJAS` | `silencioso` | `silencioso`, `avisar`, `ignorar` |
| `DURACAO_MINUTOS` | `0` | para sozinho depois de X minutos |
| `INTERVALO_SEGUNDOS` | `60` | |
| `KABUM_A_CADA_SEGUNDOS` | `180` | |

Não rode no PC e na nuvem ao mesmo tempo, senão chega aviso duplicado.
