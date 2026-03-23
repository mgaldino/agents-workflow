#!/usr/bin/env python3
"""Processamento e merge dos datasets V-Dem e CEPII Gravity.

Este script:
1. Carrega os dados brutos de V-Dem (indices de democracia) e CEPII Gravity (comercio bilateral)
2. Padroniza codigos de paises (ISO 3166-1 alpha-3)
3. Faz merge bilateral: indices de democracia tanto do pais de origem quanto de destino
4. Gera o painel final: democracy_trade_panel.csv

Resultado: dataset no nivel pais_origem-pais_destino-ano com variaveis
de comercio bilateral e indices de democracia de ambos os parceiros.
"""

import logging
from pathlib import Path
from datetime import datetime
import glob

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def find_latest_file(pattern):
    """Encontra o arquivo mais recente que casa com o pattern no diretorio raw."""
    files = sorted(RAW_DIR.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado com pattern '{pattern}' em {RAW_DIR}")
    return files[-1]  # Mais recente (pela data no nome)


def load_vdem():
    """Carrega e limpa dados do V-Dem."""
    filepath = find_latest_file("vdem_v14_cy_*.csv")
    logger.info(f"Carregando V-Dem de {filepath}")

    df = pd.read_csv(filepath, encoding="utf-8")

    # Renomear para padrao consistente
    df = df.rename(columns={
        "country_text_id": "iso3",
        "country_name": "country_name",
    })

    # Verificar e reportar missings
    democracy_cols = [c for c in df.columns if c.startswith("v2x_")]
    for col in democracy_cols:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            logger.warning(f"V-Dem: {col} tem {n_missing} valores missing ({n_missing/len(df)*100:.1f}%)")

    logger.info(f"V-Dem carregado: {len(df)} observacoes, {df['iso3'].nunique()} paises")
    return df


def load_gravity():
    """Carrega e limpa dados do CEPII Gravity."""
    filepath = find_latest_file("cepii_gravity_*.csv")
    logger.info(f"Carregando CEPII Gravity de {filepath}")

    df = pd.read_csv(filepath, encoding="utf-8")

    # Renomear para padrao consistente
    df = df.rename(columns={
        "iso3_o": "iso3_o",
        "iso3_d": "iso3_d",
    })

    # Criar variavel de comercio consolidada:
    # Preferir tradeflow_baci, complementar com comtrade
    df["trade_flow"] = df["tradeflow_baci"]
    mask = df["trade_flow"].isna()
    if "tradeflow_comtrade_o" in df.columns:
        df.loc[mask, "trade_flow"] = df.loc[mask, "tradeflow_comtrade_o"]

    # Log trade (comum em modelos gravitacionais)
    import numpy as np
    df["ln_trade"] = np.log(df["trade_flow"].clip(lower=1))  # clip para evitar log(0)
    df["ln_distw"] = np.log(df["distw"].clip(lower=1))

    logger.info(f"Gravity carregado: {len(df)} pares bilaterais-ano")
    return df


def merge_datasets(vdem_df, gravity_df):
    """Faz merge de V-Dem com Gravity, adicionando democracia de ambos parceiros."""

    # Selecionar colunas de democracia do V-Dem
    vdem_cols = ["iso3", "year", "v2x_polyarchy", "v2x_libdem", "v2x_partipdem",
                 "v2x_delibdem", "v2x_egaldem"]
    vdem_slim = vdem_df[vdem_cols].copy()

    # Merge 1: Adicionar democracia do pais de ORIGEM
    vdem_origin = vdem_slim.rename(columns={
        "iso3": "iso3_o",
        "v2x_polyarchy": "polyarchy_o",
        "v2x_libdem": "libdem_o",
        "v2x_partipdem": "partipdem_o",
        "v2x_delibdem": "delibdem_o",
        "v2x_egaldem": "egaldem_o",
    })

    merged = gravity_df.merge(
        vdem_origin,
        on=["iso3_o", "year"],
        how="left",
        validate="m:1",
    )

    n_before = len(gravity_df)
    n_matched_o = merged["polyarchy_o"].notna().sum()
    logger.info(f"Merge origem: {n_matched_o}/{n_before} pares com democracia do pais de origem ({n_matched_o/n_before*100:.1f}%)")

    # Merge 2: Adicionar democracia do pais de DESTINO
    vdem_dest = vdem_slim.rename(columns={
        "iso3": "iso3_d",
        "v2x_polyarchy": "polyarchy_d",
        "v2x_libdem": "libdem_d",
        "v2x_partipdem": "partipdem_d",
        "v2x_delibdem": "delibdem_d",
        "v2x_egaldem": "egaldem_d",
    })

    merged = merged.merge(
        vdem_dest,
        on=["iso3_d", "year"],
        how="left",
        validate="m:1",
    )

    n_matched_d = merged["polyarchy_d"].notna().sum()
    logger.info(f"Merge destino: {n_matched_d}/{n_before} pares com democracia do pais de destino ({n_matched_d/n_before*100:.1f}%)")

    # Criar variaveis derivadas uteis para pesquisa
    merged["both_democratic"] = (
        (merged["polyarchy_o"] >= 0.5) & (merged["polyarchy_d"] >= 0.5)
    ).astype(float)

    merged["polyarchy_diff"] = abs(merged["polyarchy_o"] - merged["polyarchy_d"])
    merged["polyarchy_min"] = merged[["polyarchy_o", "polyarchy_d"]].min(axis=1)
    merged["polyarchy_max"] = merged[["polyarchy_o", "polyarchy_d"]].max(axis=1)
    merged["polyarchy_product"] = merged["polyarchy_o"] * merged["polyarchy_d"]

    return merged


def process():
    """Pipeline principal de processamento."""
    logger.info("Iniciando processamento e merge...")

    # Carregar dados
    vdem_df = load_vdem()
    gravity_df = load_gravity()

    # Merge
    panel = merge_datasets(vdem_df, gravity_df)

    # Salvar
    today = datetime.now().strftime("%Y%m%d")
    output_path = PROCESSED_DIR / "democracy_trade_panel.csv"
    panel.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"Painel final salvo em {output_path}")
    logger.info(f"Dimensoes finais: {panel.shape[0]} linhas x {panel.shape[1]} colunas")
    logger.info(f"Paises de origem: {panel['iso3_o'].nunique()}")
    logger.info(f"Paises de destino: {panel['iso3_d'].nunique()}")
    logger.info(f"Anos: {panel['year'].min()}-{panel['year'].max()}")

    # Estatisticas descritivas resumidas
    logger.info("\n--- Estatisticas descritivas ---")
    key_vars = ["trade_flow", "ln_trade", "polyarchy_o", "polyarchy_d",
                "both_democratic", "polyarchy_diff"]
    available_vars = [v for v in key_vars if v in panel.columns]
    logger.info(f"\n{panel[available_vars].describe().to_string()}")

    return output_path


if __name__ == "__main__":
    process()
