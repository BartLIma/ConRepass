import pandas as pd
import streamlit as st

# Carregar CSV atualizado
df = pd.read_csv("convenios.csv", sep=";", encoding="latin1")

st.title("Consulta de Convênios")

# Lista de instrumentos únicos
instrumentos = sorted(df["Instrumento"].dropna().unique())

# Selectbox para escolher convênio
instrumento = st.selectbox("Selecione o número do convênio (Instrumento):", instrumentos)

if instrumento:
    resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
    if not resultado.empty:
        st.subheader(f"Convênio nº {instrumento}")

        # 🔑 Bloco 1 — Identificação
        with st.expander("Identificação do Convênio"):
            st.write(f"**Órgão Concedente:** {resultado.iloc[0].get('Órgão Concedente', '')}")
            st.write(f"**Objeto:** {resultado.iloc[0].get('Objeto', '')}")

        # 🏛️ Bloco 2 — Dados Institucionais
        with st.expander("Dados Institucionais"):
            st.write(f"**Município:** {resultado.iloc[0].get('Município', '')}")
            st.write(f"**Região de Saúde:** {resultado.iloc[0].get('Região de Saúde', '')}")
            st.write(f"**CNPJ:** {resultado.iloc[0].get('CNPJ', '')}")
            st.write(f"**Fundo de Saúde:** {resultado.iloc[0].get('Fundo de Saúde', '')}")

        # 💰 Bloco 3 — Valores e Vigência
        with st.expander("Valores e Vigência"):
            st.write(f"**Valor Total:** {resultado.iloc[0].get('Valor Total', '')}")
            st.write(f"**Valor Liberado:** {resultado.iloc[0].get('Valor Liberado', '')}")
            st.write(f"**Situação:** {resultado.iloc[0].get('Situação', '')}")
            st.write(f"**Data de Início:** {resultado.iloc[0].get('Data de Início', '')}")
            st.write(f"**Data de Fim:** {resultado.iloc[0].get('Data de Fim', '')}")

        # 📝 Bloco 4 — Alterações
        with st.expander("Alterações"):
            campo_alterar = "Situação"  # exemplo de campo editável
            valor_atual = resultado.iloc[0].get(campo_alterar, "")
            novo_valor = st.text_input(f"Alterar {campo_alterar}:", valor_atual)
            if st.button("Salvar alteração"):
                df.loc[df["Instrumento"] == instrumento, campo_alterar] = novo_valor
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.success(f"{campo_alterar} atualizado com sucesso!")

    else:
        st.warning("Convênio não encontrado na base de dados.")

# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima</p>",
    unsafe_allow_html=True
)
