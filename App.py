 import pandas as pd
import streamlit as st

# Leitura do CSV com tratamento especial para o campo Ano
df = pd.read_csv(
    "convenios.csv",
    sep=";",
    encoding="latin1",
    dtype={"CNPJ": str},
    converters={"Ano": lambda x: str(x).replace(".0", "")}
)

st.title("Consulta de Convênios")

instrumentos = sorted(df["Instrumento"].dropna().unique())
instrumento = st.selectbox("Selecione o número do convênio (Instrumento):", instrumentos)

if instrumento:
    resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
    if not resultado.empty:
        st.subheader(f"Convênio nº {instrumento}")

        # 🔑 Bloco 1 — Identificação
        with st.expander("Identificação"):
            st.write(f"**Instrumento:** {resultado.iloc[0].get('Instrumento', '')}")
            st.write(f"**Ano:** {resultado.iloc[0].get('Ano', '')}")
            st.write(f"**Modalidade:** {resultado.iloc[0].get('Modalidade', '')}")
            st.write(f"**Objeto:** {resultado.iloc[0].get('Objeto', '')}")
            st.write(f"**Nome Proponente:** {resultado.iloc[0].get('Nome Proponente', '')}")
            st.write(f"**CNPJ:** {resultado.iloc[0].get('CNPJ', '')}")
            st.write(f"**Situação:** {resultado.iloc[0].get('Situação', '')}")
            st.write(f"**Processo SEI:** {resultado.iloc[0].get('Processo SEI', '')}")

        # 💰 Bloco 2 — Vigência
        with st.expander("Vigência"):
            st.write(f"**Início Vigência:** {resultado.iloc[0].get('Inicio Vigencia', '')}")
            st.write(f"**Fim Vigência:** {resultado.iloc[0].get('Fim Vigencia', '')}")
