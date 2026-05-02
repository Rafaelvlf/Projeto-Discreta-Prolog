"""
csv_to_prolog.py
Converte o CSV de DPS do Terraria para uma base de conhecimento Prolog.

Uso:
    python csv_to_prolog.py [input.csv] [output.pl]

Padrões:
    input  -> Terraria DPS_TV1.4.4.9_V1 - Sheet1.csv
    output -> weapons.pl
"""

import csv
import re
import sys
from pathlib import Path

# ── Configurações ─────────────────────────────────────────────────────────────

INPUT_CSV = "Terraria DPS_TV1.4.4.9_V1 - Sheet1.csv"
OUTPUT_PL = "weapons.pl"

COL_NAME       = "NAME"
COL_CLASS      = "CLASS"
COL_PROG       = "GAME PROGRESSION"
COL_DPS_SINGLE = "DPS (SINGLE TARGET)"


# ── Helpers ───────────────────────────────────────────────────────────────────

def to_atom(text: str) -> str:
    """Converte uma string para átomo Prolog válido (minúsculas, sem espaços)."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)   # substitui caracteres especiais por _
    text = text.strip("_")
    # Átomos que começam com dígito precisam de aspas simples
    if text and text[0].isdigit():
        text = f"'{text}'"
    return text if text else "unknown"


def format_dps(value: str) -> str:
    """Retorna o DPS como número ou o átomo 'unknown' se ausente."""
    value = value.strip()
    if not value:
        return "unknown"
    try:
        # Remove separadores de milhar e converte
        num = float(value.replace(",", ""))
        # Prolog prefere inteiros quando possível
        return str(int(num)) if num == int(num) else str(num)
    except ValueError:
        return "unknown"


def build_fact(name: str, cls: str, prog: str, dps: str) -> str:
    """Monta um fato Prolog: weapon(name, class, game_progression, dps_single_target)."""
    return f"weapon({name}, {cls}, {prog}, {dps})."


# ── Principal ─────────────────────────────────────────────────────────────────

def convert(input_path: Path, output_path: Path) -> None:
    facts = []
    skipped = 0

    with input_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Valida colunas obrigatórias
        required = {COL_NAME, COL_CLASS, COL_PROG, COL_DPS_SINGLE}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Colunas ausentes no CSV: {missing}")

        for i, row in enumerate(reader, start=2):   # linha 2 = primeira de dados
            name_raw = row[COL_NAME].strip()

            # Pula linhas sem nome (separadores, totais, etc.)
            if not name_raw:
                skipped += 1
                continue

            name  = to_atom(name_raw)
            cls   = to_atom(row[COL_CLASS])
            prog  = to_atom(row[COL_PROG])
            dps   = format_dps(row[COL_DPS_SINGLE])

            facts.append(build_fact(name, cls, prog, dps))

    header = "\n".join([
        "% Base de conhecimento – Armas do Terraria",
        "% Gerado automaticamente por csv_to_prolog.py",
        "%",
        "% Formato:",
        "%   weapon(Name, Class, GameProgression, DpsSingleTarget).",
        "%",
        f"% Total de armas: {len(facts)}",
        "",
    ])

    output_path.write_text(header + "\n".join(facts) + "\n", encoding="utf-8")

    print(f"✓ {len(facts)} fatos gerados → {output_path}")
    if skipped:
        print(f"  (linhas vazias ignoradas: {skipped})")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    input_path  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(INPUT_CSV)
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(OUTPUT_PL)

    if not input_path.exists():
        print(f"Erro: arquivo de entrada não encontrado → {input_path}")
        sys.exit(1)

    convert(input_path, output_path)