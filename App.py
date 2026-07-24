import pandas as pd
import streamlit as st
from io import BytesIO
from fpdf import FPDF

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

        # Campo editável
        data_envio_pc = st.text_input(
            "Prestação de Contas Apresentada em:",
            value=resultado.iloc[0].get('Data de Envio da  PC', '')
        )

        anotacoes_obs = st.text_area(
            "ANOTAÇÕES OBS:",
            value=resultado.iloc[0].get('ANOTACOES OBS', '')
        )

        # --- Botões de ação ---
        if st.button("Salvar alterações"):
            df.loc[resultado.index[0], 'Data de Envio da  PC'] = data_envio_pc
            df.loc[resultado.index[0], 'ANOTACOES OBS'] = anotacoes_obs
            df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
            st.success("Alterações salvas com sucesso!")

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

        # Botão para gerar PDF com dados do convênio
        if st.button("📄 Gerar PDF do Convênio"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Convênio nº {instrumento}", ln=True, align="C")
            pdf.ln(10)
            pdf.multi_cell(0, 10, f"Prestação de Contas Apresentada em: {data_envio_pc}")
            pdf.multi_cell(0, 10, f"Anotações/Observações: {anotacoes_obs}")

            pdf_buffer = BytesIO()
            pdf.output(pdf_buffer)
            st.download_button(
                label="📄 Baixar PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"convenio_{instrumento}.pdf",
                mime="application/pdf"
            )
