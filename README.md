# Uso de memória RAM em jogos de diferentes pesos

Projeto que mede quanta memória RAM jogos **leves, médios e pesados** utilizam, em computadores com características diferentes. Este repositório guarda o script de medição, os dados coletados e a documentação da metodologia.

## Objetivo

Testar a hipótese de que **quanto mais pesado o jogo, mais memória ele aloca**, e observar como isso muda de um computador para outro.

## Métricas medidas

| Métrica | O que significa | Campo no Windows | Coluna no CSV |
|---|---|---|---|
| Memória virtual alocada | Tudo o que o jogo reservou (commit / Private Bytes) | `vms` | `virtual_MB` |
| Pico de memória alocada | Maior valor de memória virtual desde que o processo abriu | `peak_pagefile` | `pico_virtual_SO_MB` |
| Memória residente em RAM | Parte que de fato está na RAM (Working Set) | `rss` | `residente_MB` |
| Pico de memória residente | Maior valor de Working Set desde que o processo abriu | `peak_wset` | `pico_residente_SO_MB` |

> **Atenção:** os picos reportados pelo sistema operacional valem desde que o jogo foi aberto, e não apenas durante a janela de medição. Por isso podem ser maiores que o máximo observado nas colunas `virtual_MB` e `residente_MB`.

## Estrutura do repositório

```
.
├── README.md
├── scripts/
│   └── medir.py              # script de medição
├── dados/
│   ├── brutos/               # CSVs originais, exatamente como o script gerou
│   └── excel/                # versões com ";" para abrir direto no Excel (pt-BR)
└── docs/
    └── passo_a_passo.md      # guia de execução (opcional)
```

## Como medir

### Requisitos

- Windows (o script também funciona em Linux)
- Python 3.8 ou superior
- Biblioteca `psutil`

```
python -m pip install psutil
```

### Passo a passo

1. Reinicie o computador e feche programas em segundo plano. Anote a RAM livre no início.
2. Abra o jogo e deixe-o no ponto de teste.
3. Descubra o nome do executável: Gerenciador de Tarefas (`Ctrl + Shift + Esc`) > aba **Detalhes**.
4. Rode o script:

```
python scripts/medir.py NOME_DO_JOGO.exe --duration 600 --out jogo_pcX_testeN.csv
```

| Argumento | Descrição | Padrão |
|---|---|---|
| `process` | Nome do executável do jogo | obrigatório |
| `--duration` | Duração da medição em segundos | 600 |
| `--interval` | Intervalo entre leituras em segundos | 1.0 |
| `--out` | Nome do arquivo de saída | `medicao.csv` |

5. Jogue normalmente durante a medição. Para parar antes, use `Ctrl + C` (o CSV já foi gravado a cada leitura).

## Formato dos dados

Os arquivos CSV usam **vírgula** como separador e **ponto** como decimal. Colunas:

```
t_s, virtual_MB, residente_MB, pico_virtual_SO_MB, pico_residente_SO_MB
```

Uma linha por leitura (1 por segundo), com valores em **MB**.

Para abrir no Excel em português, use a versão da pasta `dados/excel/` (separador `;`) ou, no Excel, vá em **Dados > Texto para Colunas > Delimitado > Vírgula**.

### Convenção de nomes

```
jogo_pcX_testeN.csv
```

Exemplos: `cs2_pc1_teste1.csv`, `brawlhalla_pcV_teste2.csv`.

## Metodologia

- **Classificação dos jogos:** *(descrever o critério usado, por exemplo requisitos mínimos oficiais, tamanho em disco ou tipo de gráfico)*.
- **Cenário padronizado:** o mesmo tipo de atividade em todos os testes (por exemplo, 10 minutos no campo de treino, mesmo mapa e mesmas configurações gráficas).
- **Duração:** 600 segundos por teste.
- **Repetições:** 3 testes por jogo em cada computador, usando média e desvio padrão.
- **Controle do ambiente:** PC reiniciado antes do teste e programas em segundo plano fechados.

## Jogos testados

| Jogo | Categoria |
|---|---|
| Brawlhalla | Leve |
| Deadlock | Médio |
| CS2 | Pesado |

## Computadores testados

| PC | Processador | RAM (quantidade e velocidade) | Placa de vídeo / VRAM | Sistema operacional | Armazenamento (SSD/HDD) |
|---|---|---|---|---|---|
| PCJ | 12th Gen Intel(R) Core(TM) i5-1245HX, 2400Mhz, 8 Núcleos, 12 Processadores | 16,0GB e 4800MT/s | NVIDIA GeForce RTX 3050 6GB | Microsoft Windows 11 | SSD |
| PCR | | | | | |

## Resultados preliminares

Valores em MB, de testes individuais (ainda sem média das repetições).

| Jogo | PC | Virtual (média) | Virtual (máx. medido) | Pico alocado (SO) | Residente (média) | Residente (máx. medido) | Pico residente (SO) |
|---|---|---|---|---|---|---|---|
| Brawlhalla | PC1 | 2.453 | 2.487 | 2.487 | 2.383 | 2.413 | 2.413 |
| Brawlhalla | PCV | 2.544 | 2.651 | 2.656 | 2.429 | 2.544 | 2.544 |
| Deadlock | PC1 | 8.587 | 9.541 | 10.247 | 4.090 | 4.743 | 5.149 |
| CS2 | PC1 | 8.478 | 8.926 | 9.814 | 4.354 | 4.671 | 4.681 |
| CS2 | PCV | 9.250 | 9.776 | 9.783 | 6.507 | 7.106 | 7.108 |

## Explicação técnica

O Windows usa **memória virtual com paginação sob demanda**: quando o jogo pede memória, o sistema reserva espaço (memória virtual alocada), mas só coloca a página na RAM física quando ela é realmente usada (memória residente). Por isso a memória virtual é sempre maior ou igual à residente.

O efeito vale até o **limite de commit** do sistema (RAM + arquivo de paginação). Quando a RAM física enche, o Windows envia páginas pouco usadas para o disco, a memória residente deixa de crescer e o disco vira o gargalo, causando engasgos e quedas de FPS.

## Limitações

- Cada valor vem de poucas medições e de computadores específicos.
- O script soma todos os processos com o mesmo nome; jogos com launcher ou processos auxiliares exigem conferir qual é o executável principal.
- O pico "amostrado" depende do intervalo de leitura.
- A memória de vídeo (VRAM) não é medida por este script.

## Autores

*(nomes dos integrantes do grupo)*

## Licença

*(escolher uma licença, por exemplo MIT para o código e CC BY 4.0 para os dados)*
