import pandas as pd
import streamlit as st

# Forçar CNPJ como texto
df = pd.read_csv("convenios.csv", sep=";", encoding="latin1", dtype={"CNPJ": str})

st.title("Consulta de Convênios")

instrumentos = sorted(df["Instrumento"].dropna().unique())
instrumento = st.selectbox("Selecione o número do convênio (Instrumento):", instrumentos)

if instrumento:
    resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
    if not resultado.empty:
        st.subheader(f"Convênio nº {instrumento}")

        # Identificação
        with st.expander("Identificação do Convênio"):
            st.write(f"**Órgão Concedente:** {resultado.iloc[0].get('Órgão Concedente', '')}")
            st.write(f"**Objeto:** {resultado.iloc[0].get('Objeto', '')}")

        # Dados Institucionais
        with st.expander("Dados Institucionais"):
            st.write(f"**Nome Proponente:** {resultado.iloc[0].get('Nome Proponente', '')}")
            st.write(f"**Modalidade:** {resultado.iloc[0].get('Modalidade', '')}")
            st.write(f"**CNPJ:** {resultado.iloc[0].get('CNPJ', '')}")
            st.write(f"**Situação:** {resultado.iloc[0].get('Situação', '')}")

        # Valores e Vigência
        with st.expander("Valores e Vigência"):
            st.write(f"**Valor Global:** {resultado.iloc[0].get('Valor Global', '')}")
            st.write(f"**Valor Liberado:** {resultado.iloc[0].get('Valor Liberado', '')}")
            st.write(f"**Data de Início:** {resultado.iloc[0].get('Data de Início', '')}")
            st.write(f"**Data de Fim:** {resultado.iloc[0].get('Data de Fim', '')}")

        # Alterações
        with st.expander("Alterações"):
            campo_alterar = "Situação"
            valor_atual = resultado.iloc[0].get(campo_alterar, "")
            novo_valor = st.text_input(f"Alterar {campo_alterar}:", valor_atual)
            if st.button("Salvar alteração"):
                df.loc[df["Instrumento"] == instrumento, campo_alterar] = novo_valor
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.success(f"{campo_alterar} atualizado com sucesso!")
