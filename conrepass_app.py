    import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
from io import BytesIO

# Carregar variáveis do .env
load_dotenv()
senha_correta = os.getenv("APP_PASSWORD")  # valor definido no .env

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

            # 📅 Bloco 2 — Vigência / Datas
            with st.expander("Vigência / Datas"):
                st.write(f"**Início Vigência:** {resultado.iloc[0].get('Inicio Vigencia', '')}")
                st.write(f"**Fim Vigência:** {resultado.iloc[0].get('Fim Vigencia', '')}")
                st.write(f"**Data Limite para Apresentar PC:** {resultado.iloc[0].get('Data Limite para Apresentar PC', '')}")
                data_envio_pc = st.text_input(
                    "Prestação de Contas Apresentada em:",
                    value=resultado.iloc[0].get('Data de Envio da  PC', '')
                )

            # 📊 Bloco 3 — Execução Financeira
            with st.expander("Execução Financeira"):
                st.write(f"**Valor Global: R$** {resultado.iloc[0].get('Valor Global', '')}")
                st.write(f"**Valor Empenhado: R$** {resultado.iloc[0].get('Valor Empenhado', '')}")
                st.write(f"**Valor Liberado: R$** {resultado.iloc[0].get('Valor Liberado', '')}")
                st.write(f"**Valor de Contrapartida: R$** {resultado.iloc[0].get('Valor de Contrapartida', '')}")
                st.write(f"**Ingresso de R$ (Rendimentos e Contrapartida):** {resultado.iloc[0].get('Ingresso de $', '')}")
                st.write(f"**Total em Movimentações Financeiras: R$** {resultado.iloc[0].get('Total em Movimentacoes Financeiras', '')}")
                st.write(f"**Saldo em Conta: R$** {resultado.iloc[0].get('Saldo em conta', '')}")
                st.write(f"**Vl Devolvido: R$** {resultado.iloc[0].get('Vl Devolvido', '')}")
                st.write(f"**Execução Financeira Concedente e Convenente: R$** {resultado.iloc[0].get('Execucao  Financeira Concedente  e Convenente', '')}")
                st.write(f"**Devolução de Saldo p/ União: R$** {resultado.iloc[0].get('Devolucao de Saldo p Uniao', '')}")
                st.write(f"**Resto a Pagar: R$** {resultado.iloc[0].get('Resto a Pagar', '')}")

            # ... demais blocos (Prestação de Contas, Monitoramento, Alertas, Observações) iguais ao seu código ...

            # Botão para salvar alterações
            if st.button("Salvar alterações"):
                df.loc[resultado.index[0], 'Data de Envio da  PC'] = data_envio_pc
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

# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:green;'>Bartolomeu Lima</p>",
    unsafe_allow_html=True
)
