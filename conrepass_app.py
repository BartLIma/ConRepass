import pandas as pd
import streamlit as st
from io import BytesIO

# Senha fixa
senha_correta = "ditre123"

# Campo de senha
senha = st.text_input("Digite a senha para acessar:", type="password")

if senha == senha_correta:
    st.success("Acesso liberado ✅")

    # --- Código principal do Conrepass ---
    df = pd.read_csv(
        "convenios.csv",
        sep=";",   
        encoding="latin1",
        dtype={"CNPJ": str},
        converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
    )
    df.columns = df.columns.str.strip()

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
                st.write(f"**Situação:** {resultado.iloc[0].get('Situacao', '')}")
                st.write(f"**Processo SEI:** {resultado.iloc[0].get('Processo SEI', '')}")

            # ... demais blocos iguais ao seu código ...

            # Botão para salvar alterações
            if st.button("Salvar alterações"):
                df.loc[resultado.index[0], 'Data de Envio da  PC'] = data_envio_pc
                df.loc[resultado.index[0], 'ANOTACOES OBS'] = anotacoes_obs
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.success("Alterações salvas com sucesso!")

            # Botão para baixar CSV
            csv_data = df.to_csv(sep=";", index=False).encode("latin1")
            st.download_button(
                label="📥 Baixar planilha em CSV",
                data=csv_data,
                file_name="convenios_atualizado.csv",
                mime="text/csv"
            )

else:
    st.warning("Digite a senha correta para acessar o sistema.")

# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:green;'>Bartolomeu Lima</p>",
    unsafe_allow_html=True
)
