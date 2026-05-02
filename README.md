# Knowledge Engine – Terraria

Projeto da disciplina **Lógica e Matemática Discreta (2026/1)** — Insper.

Aluno: Rafael Victor Lemos Ferreira.

Construção de uma base de conhecimento em Prolog a partir de um dataset público de armas do jogo Terraria, com queries sofisticadas usando lógica de primeira ordem.

---

## Dataset

**Terraria DPS — v1.4.4.9**  
Fonte: Kaggle  
Arquivo original: `Terraria DPS_TV1.4.4.9_V1 - Sheet1.csv`

Cada registro representa uma arma do jogo com os seguintes campos utilizados:

| Campo | Descrição |
|---|---|
| `NAME` | Nome da arma |
| `CLASS` | Classe da arma (Melee, Mage, Ranger, Summoner) |
| `GAME PROGRESSION` | Fase do jogo em que a arma se torna disponível |
| `DPS (SINGLE TARGET)` | Dano por segundo contra um único alvo |

Total de registros: **395 armas**.

---

## Estrutura do Repositório

```
.
├── Terraria DPS_TV1.4.4.9_V1 - Sheet1.csv  # Dataset original
├── csv_to_prolog.py                          # Script ETL: CSV → Prolog
├── weapons.pl                         # Base de conhecimento + queries
└── README.md
```

---

## Como Rodar

### 1. Gerar a base de conhecimento

Requer Python 3 com a biblioteca `pandas`:

```bash
pip install pandas
python csv_to_prolog.py
```

Isso gera o arquivo `weapons.pl` com os 395 fatos no formato:

```prolog
weapon(zenith, melee, post_moonlord, 4800).
weapon(last_prism, mage, post_moonlord, 3657).
...
```

### 2. Rodar as queries no SWISH

1. Acesse [https://swish.swi-prolog.org](https://swish.swi-prolog.org)
2. Crie um novo notebook
3. Cole o conteúdo de `knowledge_base.pl` na área **Program**
4. Execute as queries abaixo na área **Query**

---

## Perguntas e Queries

### Pergunta 1 — Qual classe domina cada fase do jogo?

Calcula o DPS médio de cada classe em cada fase e retorna a classe vencedora por fase.

```prolog
?- ranking_por_fase(Tabela).
```

Resultado esperado (exemplo):
```
post_moonlord - melee  - 2950
post_cultist  - melee  - 1300
post_wof      - mage   - 297
pre_boss      - mage   - 64
...
```

Técnicas usadas: `findall`, `sum_list`, `length`, negação por falha (`\+`), `maplist`, `setof`.

---

### Pergunta 2 — Ranking geral das classes por DPS médio

Agrega o DPS médio de todas as armas de cada classe e ordena do maior para o menor.

```prolog
?- ranking_classes(Ranking).
```

Resultado esperado:
```
mage     → 393.48
melee    → 264.88
ranger   → 237.70
summoner → 102.21
```

Técnicas usadas: `setof` (ordenação + remoção de duplicatas), `reverse`, aritmética.

---

### Pergunta 3 — Melhor arma de cada classe em uma fase específica

Dado um estágio do jogo, retorna a arma com maior DPS de cada classe disponível naquele estágio.

```prolog
?- melhores_armas_por_fase(post_moonlord, Resultado).
?- melhores_armas_por_fase(post_plantera, Resultado).
```

Resultado esperado para `post_moonlord`:
```
melee    → zenith                  (4800)
mage     → last_prism              (3657)
ranger   → celebration_mk_2       (1709)
summoner → rainbow_crystal_staff   (350)
```

Técnicas usadas: `max_list`, `findall`, composição de predicados auxiliares (`dps_maximo_na_fase`, `melhor_arma_na_fase`).

---

## Predicados Auxiliares

| Predicado | Descrição |
|---|---|
| `classe(C)` | Define o domínio das 4 classes |
| `dps_medio_global(Classe, Media)` | DPS médio de uma classe em todo o dataset |
| `dps_medio_classe_progressao(Classe, Fase, Media)` | DPS médio de uma classe em uma fase específica |
| `melhor_classe_na_fase(Fase, Classe, Media)` | Classe com maior DPS médio na fase |
| `dps_maximo_na_fase(Classe, Fase, Max)` | Maior DPS de uma classe numa fase |
| `melhor_arma_na_fase(Classe, Fase, Arma, DPS)` | Arma campeã de cada classe na fase |
