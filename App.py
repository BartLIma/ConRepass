   import pandas as pd
import streamlit as st

# Forçar CNPJ como texto e Ano como string
df = pd.read_csv(
    "convenios.csv",
    sep=";",
    encoding="latin1",
    dtype={"CNPJ": str, "Ano": str}
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
