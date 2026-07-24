import pandas as pd
import streamlit as st
from io import BytesIO

# Leitura do CSV
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

        # 📅 Bloco 2 — Vigência / Datas
        with st.expander("Vigência / Datas"):
            st.write(f"**Início Vigência:** {resultado.iloc[0].get('Inicio Vigencia', '')}")
            st.write(f"**Fim Vigência:** {resultado.iloc[0].get('Fim Vigencia', '')}")
            st.write(f"**Data Limite para Apresentar PC:** {resultado.iloc[0].get('Data Limite para Apresentar PC', '')}")
            
            # Campo editável
            data_envio_pc = st.text_input(
                "Prestação de Contas Apresentada em:",
                value=resultado.iloc[0].get('Data de Envio da  PC', '')
            )

        # 🗒️ Bloco 7 — Anotações e Observações
        with st.expander("Anotações e Observações"):
            anotacoes_obs = st.text_area(
                "ANOTAÇÕES OBS:",
                value=resultado.iloc[0].get('ANOTACOES OBS', '')
            )

        # --- Botões de ação lado a lado ---
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            if st.button("💾 Salvar alterações"):
                df.loc[resultado.index[0], 'Data de Envio da  PC'] = data_envio_pc
                df.loc[resultado.index[0], 'ANOTACOES OBS'] = anotacoes_obs
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.success("Alterações salvas com sucesso!")

        with col2:
            if st.button("⬆️ Voltar ao topo"):
                st.markdown(
                    "<script>window.scrollTo(0,0);</script>",
                    unsafe_allow_html=True
                )

        with col3:
            if st.button("🧹 Limpar pesquisa e voltar ao topo"):
                st.session_state.clear()
                st.markdown(
                    "<script>window.scrollTo(0,0);</script>",
                    unsafe_allow_html=True
                )

        # Botão para baixar toda a planilha em CSV
        csv_data = df.to_csv(sep=";", index=False).encode("latin1")
        st.download_button(
            label="📥 Baixar planilha em CSV",
            data=csv_data,
            file_name="convenios_atualizado.csv",
            mime="text/csv"
        )

        # Botão para baixar toda a planilha em Excel
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        st.download_button(
            label="📥 Baixar planilha em Excel",
            data=excel_buffer.getvalue(),
            file_name="convenios_atualizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.warning("Convênio não encontrado na base de dados.")

# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima</p>",
    unsafe_allow_html=True
)
