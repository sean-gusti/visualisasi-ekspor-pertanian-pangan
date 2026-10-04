"""Pemuat data olahan (di-cache). Sumber: BPS."""
from pathlib import Path
import pandas as pd
import streamlit as st

PROC = Path(__file__).resolve().parents[1] / "data" / "processed"


@st.cache_data
def muat(nama: str) -> pd.DataFrame:
    return pd.read_csv(PROC / nama, dtype={"hs2": str})


def chapter_tahun():          return muat("chapter_tahun.csv")
def chapter_negara_tahun():   return muat("chapter_negara_tahun.csv")
def negara_tahun():           return muat("negara_tahun.csv")
def pelabuhan_detail():       return muat("ekspor_hs2_tahun_negara_pelabuhan.csv")