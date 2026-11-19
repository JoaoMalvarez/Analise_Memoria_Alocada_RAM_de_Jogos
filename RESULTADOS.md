# Resultados

Valores em **MB**. Cada linha da tabela principal é a **média dos testes** daquele jogo naquele computador.

## Resumo por jogo e computador

| Jogo | PC | Virtual (média) | Virtual (máx. medido) | Pico alocado (SO) | Residente (média) | Residente (máx. medido) | Pico residente (SO) |
|---|---|---|---|---|---|---|---|
| Brawlhalla | PCJ | 2.453 | 2.487 | 2.487 | 2.383 | 2.413 | 2.413 |
| Brawlhalla | PCR | 2.499 | 2.606 | 2.619 | 2.388 | 2.493 | 2.497 |
| Deadlock | PCJ | 9.753 | 10.485 | 11.007 | 4.595 | 5.418 | 6.191 |
| CS2 | PCJ | 8.478 | 8.926 | 9.814 | 4.354 | 4.671 | 4.681 |
| CS2 | PCR | 8.811 | 9.400 | 9.736 | 6.150 | 6.594 | 6.605 |

## Variação entre os testes (média ± desvio padrão)

| Jogo | PC | Testes | Virtual (média) | Residente (média) | Pico alocado (SO) | Pico residente (SO) |
|---|---|---|---|---|---|---|
| Brawlhalla | PCJ | 1 | 2.453 | 2.383 | 2.487 | 2.413 |
| Brawlhalla | PCR | 2 | 2.499 ± 64 | 2.388 ± 57 | 2.619 ± 52 | 2.497 ± 66 |
| Deadlock | PCJ | 3 | 9.753 ± 1.099 | 4.595 ± 1.050 | 11.007 ± 661 | 6.191 ± 914 |
| CS2 | PCJ | 1 | 8.478 | 4.354 | 9.814 | 4.681 |
| CS2 | PCR | 2 | 8.811 ± 621 | 6.150 ± 504 | 9.736 ± 66 | 6.605 ± 711 |

Onde aparece só um valor, há apenas um teste, então não existe desvio padrão.

## Resultados de cada teste

| Jogo | PC | Teste | Duração (s) | Virtual (média) | Virtual (máx. medido) | Pico alocado (SO) | Residente (média) | Residente (máx. medido) | Pico residente (SO) |
|---|---|---|---|---|---|---|---|---|---|
| Brawlhalla | PCJ | 1 | 600 | 2.453 | 2.487 | 2.487 | 2.383 | 2.413 | 2.413 |
| Brawlhalla | PCR | 2 | 600 | 2.544 | 2.651 | 2.656 | 2.429 | 2.544 | 2.544 |
| Brawlhalla | PCR | 3 | 600 | 2.453 | 2.560 | 2.582 | 2.347 | 2.442 | 2.450 |
| Deadlock | PCJ | 1 | 600 | 8.587 | 9.541 | 10.247 | 4.090 | 4.743 | 5.149 |
| Deadlock | PCJ | 2 | 600 | 10.770 | 10.923 | 11.326 | 3.893 | 5.204 | 6.565 |
| Deadlock | PCJ | 3 | 600 | 9.902 | 10.991 | 11.449 | 5.802 | 6.307 | 6.859 |
| CS2 | PCJ | 1 | 600 | 8.478 | 8.926 | 9.814 | 4.354 | 4.671 | 4.681 |
| CS2 | PCR | 2 | 600 | 9.250 | 9.776 | 9.783 | 6.507 | 7.106 | 7.108 |
| CS2 | PCR | 3 | 900 | 8.372 | 9.023 | 9.689 | 5.794 | 6.082 | 6.102 |

## Observações

- **Categorias:** Brawlhalla (leve), Deadlock (médio) e CS2 (pesado).
- **Picos do SO:** os valores `Pico alocado (SO)` e `Pico residente (SO)` valem desde que o jogo foi aberto, e não só durante os 10 minutos medidos. Por isso podem ser maiores que o máximo medido.
- **Duração:** o teste 3 do CS2 no PCR tem 900 s, enquanto os demais têm 600 s.
- **Testes ainda faltando:** Brawlhalla e CS2 no PCJ têm 1 teste cada, Brawlhalla e CS2 no PCR têm 2, e o Deadlock ainda não foi medido no PCR.