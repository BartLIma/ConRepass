import pandas as pd
import streamlit as st
from io import BytesIO
from fpdf import FPDF

# Leitura do CSV com tratamento especial para o campo Ano
df = pd.read_csv(
    "convenios.csv",
    sep=";",   # separador correto
    encoding="latin1",
    dtype={"CNPJ": str},
    converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
)

# Remove espaços extras dos nomes das colunas
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

        # 📊 Bloco 3 — Execução Financeira
        with st.expander("Execução Financeira"):
            st.write(f"**Valor Global:** {resultado.iloc[0].get('Valor Global', '')}")
            st.write(f"**Valor Empenhado:** {resultado.iloc[0].get('Valor Empenhado', '')}")
            st.write(f"**Valor Liberado:** {resultado.iloc[0].get('Valor Liberado', '')}")
            st.write(f"**Valor de Contrapartida:** {resultado.iloc[0].get('Valor de Contrapartida', '')}")
            st.write(f"**Ingresso de $ (Rendimentos e Contrapartida):** {resultado.iloc[0].get('Contrapartida', '')}")
            st.write(f"**Total em Movimentações Financeiras:** {resultado.iloc[0].get('Total em Movimentacoes Financeiras', '')}")
            st.write(f"**Saldo em Conta:** {resultado.iloc[0].get('Saldo em conta', '')}")
            st.write(f"**Vl Devolvido:** {resultado.iloc[0].get('Vl Devolvido', '')}")
            st.write(f"**Execução Financeira Concedente e Convenente:** {resultado.iloc[0].get('Execucao  Financeira Concedente  e Convenente', '')}")
            st.write(f"**Devolução de Saldo p/ União:** {resultado.iloc[0].get('Devolucao de Saldo p Uniao', '')}")
            st.write(f"**Resto a Pagar:** {resultado.iloc[0].get('Resto a Pagar', '')}")

        # 📑 Bloco 4 — Prestação de Contas / Execução
        with st.expander("Prestação de Contas / Execução"):
            st.write(f"**Dias de Atraso Envio da PC:** {resultado.iloc[0].get('Dias de Atraso Envio da PC', '')}")
            st.write(f"**PC Informatizada:** {resultado.iloc[0].get('PC Informatizada', '')}")
            st.write(f"**Nota de Risco:** {resultado.iloc[0].get('Nota de Risco', '')}")
            st.write(f"**Limite Toler Risco:** {resultado.iloc[0].get('Limite Toler  Risco', '')}")
            faixa_risco = resultado.iloc[0].get('Faixa de Risco', '')
            if pd.isna(faixa_risco):
                faixa_risco = "Não informado"
            st.write(f"**Faixa de Risco:** {faixa_risco}")
            st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('Grau de Prioridade', '')}")
            st.write(f"**Relatórios de Execução:** {resultado.iloc[0].get('Relatorios de Execucao', '')}")
            st.write(f"**Ação de Monitoramento:** {resultado.iloc[0].get('Acao de Monitoramnto', '')}")
            st.write(f"**Parecer Financeiro:** {resultado.iloc[0].get('Parecer Financeiro', '')}")
            st.write(f"**Parecer Tec-Mérito:** {resultado.iloc[0].get('Parecer Tec -Merito', '')}")
            st.write(f"**Análise de Equipamentos:** {resultado.iloc[0].get('Analise de Equipamentos', '')}")
            st.write(f"**Ação de Análise de PC:** {resultado.iloc[0].get('Acao de Analise de PC', '')}")
            st.write(f"**Percentual de Evolução da Análise:** {resultado.iloc[0].get('Percentual de Evolucao da Analise', '')}")
            st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.iloc[0].get('Pareceres Incluidos na Plataforma', '')}")

        # 📝 Bloco 5 — Monitoramento
        with st.expander("Monitoramento"):
            st.write(f"**Situação do Convênio:** {resultado.iloc[0].get('Status de Execucao', '')}")
            st.write(f"**Percentual de Execução:** {resultado.iloc[0].get('Percental  Exec', '')}")
            st.write(f"**Técnico / Analista:** {resultado.iloc[0].get('Tecnico / Analista', '')}")
            st.write(f"**Data de Vínculo Fiscal:** {resultado.iloc[0].get('Data de Vinculo Fiscal', '')}")

        # ⚠️ Bloco 6 — Alertas
        with st.expander("Alertas"):
            st.write(f"**ALERTA de Execução Financeira:** {resultado.iloc[0].get('ALERTA de Execucao Financeira', '')}")
            st.write(f"**ALERTA Sem Desembolso:** {resultado.iloc[0].get('ALERTA Sem Desembolso', '')}")
            st.write(f"**ALERTA Sem Pgt + 150 Dias:** {resultado.iloc[0].get('ALERTA Sem Pgt + 150 Dias', '')}")
            st.write(f"**Acórdão TCU1203:** {resultado.iloc[0].get('Acordao  TCU1203', '')}")
            st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('GRAU DE PRIORIDADE', '')}")

        # 🗒️ Bloco 7 — Anotações e Observações
        with st.expander("Anotações e Observações"):
            anotacoes_obs = st.text_area(
                "ANOTAÇÕES OBS:",
                value=resultado.iloc[0].get('ANOTACOES OBS', '')
            )

        # --- Botões de ação ---
        if st.button("Salvar alterações"):
            # Atualiza os valores editados no DataFrame
            df.loc[resultado.index[0], 'Data de Envio da  PC'] = data_envio_pc
            df.loc[resultado.index[0], 'ANOTACOES OBS'] = anotacoes_obs
            # Salva de volta no CSV
            df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
            st.success("Alterações salvas com sucesso!")

        # Botão para baixar toda a planilha em CSV
        csv_data = df.to_csv(sep=";", index=False).encode("latin1")
        st.download_button(
            label="📥 Baixar planilha em CSV",
            data=csv_data,
            file_name="convenios_atualizado.csv",
            mime="text/c
