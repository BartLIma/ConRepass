import pandas as pd
import streamlit as st

# Forçar CNPJ como texto para evitar notação científica
df = pd.read_csv("convenios.csv", sep=";", encoding="latin1", dtype={"CNPJ": str})

st.title("Consulta de Convênios")

# Lista de instrumentos únicos
instrumentos = sorted(df["Instrumento"].dropna().unique())
instrumento = st.selectbox("Selecione o número do convênio (Instrumento):", instrumentos)

if instrumento:
    resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
    if not resultado.empty:
        st.subheader(f"Convênio nº {instrumento}")

        # 🔑 Bloco 1 — Identificação
        with st.expander("Identificação"):
            st.write(f"**Instrumento:** {resultado.iloc[0].get('Instrumento', '')}")
            ano = resultado.iloc[0].get('Ano', '')
# Se for float, converte para inteiro
if isinstance(ano, float):
    ano = int(ano)
# Se ainda assim não for número, garante como string
ano = str(ano)
st.write(f"**Ano:** {ano}")
            st.write(f"**Modalidade:** {resultado.iloc[0].get('Modalidade', '')}")
            st.write(f"**Objeto:** {resultado.iloc[0].get('Objeto', '')}")
            st.write(f"**Nome Proponente:** {resultado.iloc[0].get('Nome Proponente', '')}")
            st.write(f"**CNPJ:** {resultado.iloc[0].get('CNPJ', '')}")
            st.write(f"**Status de Execução:** {resultado.iloc[0].get('Status de Execucao', '')}")
            st.write(f"**Processo SEI:** {resultado.iloc[0].get('Processo SEI', '')}")

        # 💰 Bloco 2 — Valores e Vigência
        with st.expander("Valores e Vigência"):
            st.write(f"**Início Vigência:** {resultado.iloc[0].get('Inicio Vigencia', '')}")
            st.write(f"**Fim Vigência:** {resultado.iloc[0].get('Fim Vigencia', '')}")
            st.write(f"**Data Limite para Apresentar PC:** {resultado.iloc[0].get('Data Limite para Apresentar PC', '')}")

        # 📑 Bloco 3 — Prestação de Contas / Execução
        with st.expander("Prestação de Contas / Execução"):
            st.write(f"**Data de Envio da PC:** {resultado.iloc[0].get('Data de Envio da PC', '')}")
            st.write(f"**Dias de Atraso:** {resultado.iloc[0].get('Dias de Atraso', '')}")
            st.write(f"**Dias Após Envio da PC:** {resultado.iloc[0].get('Dias apos Envio da PC', '')}")
            st.write(f"**PC Informatizada:** {resultado.iloc[0].get('PC Informatizada', '')}")
            st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('Grau de Prioridade', '')}")
            st.write(f"**Relatórios de Execução:** {resultado.iloc[0].get('Relatorios de Execucao', '')}")
            st.write(f"**Ação de Monitoramento:** {resultado.iloc[0].get('Acao de Monitoramnto', '')}")
            st.write(f"**Percentual Execução:** {resultado.iloc[0].get('Percental Exec', '')}")
            st.write(f"**Parecer Financeiro:** {resultado.iloc[0].get('Parecer Financeiro', '')}")
            st.write(f"**Parecer Tec-Mérito:** {resultado.iloc[0].get('Parecer Tec -Merito', '')}")
            st.write(f"**Análise de Equipamentos:** {resultado.iloc[0].get('Analise de Equipamentos', '')}")
            st.write(f"**Ação de Análise de PC:** {resultado.iloc[0].get('Acao de Analise de PC', '')}")
            st.write(f"**Percentual de Evolução da Análise:** {resultado.iloc[0].get('Percentual de Evolucoo da Analise', '')}")
            st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.iloc[0].get('Pareceres Incluidos na Plataforma', '')}")

        # 📊 Bloco 4 — Execução Financeira
        with st.expander("Execução Financeira"):
            st.write(f"**Valor Global:** {resultado.iloc[0].get('Valor Global', '')}")
            st.write(f"**Valor Empenhado:** {resultado.iloc[0].get('Valor Empenhado', '')}")
            st.write(f"**Valor Liberado:** {resultado.iloc[0].get('Valor Liberado', '')}")
            st.write(f"**Contrapartida:** {resultado.iloc[0].get('Contrapartida', '')}")
            st.write(f"**Total em Movimentações Financeiras:** {resultado.iloc[0].get('Total em Movimentacoes Financeiras', '')}")
            st.write(f"**Saldo em Conta:** {resultado.iloc[0].get('Saldo em conta', '')}")
            st.write(f"**Vl Devolvido:** {resultado.iloc[0].get('Vl Devolvido', '')}")
            st.write(f"**Execução Financeira Concedente e Convenente:** {resultado.iloc[0].get('Execucao  Finaceira Concedente  e Convenente', '')}")
            st.write(f"**Devolução de Saldo p/ União:** {resultado.iloc[0].get('Devolucao de Saldo p Uniao', '')}")
            st.write(f"**Resto a Pagar:** {resultado.iloc[0].get('Resto a Pagar', '')}")

        # 📝 Bloco 5 — Risco e Observações
        with st.expander("Risco e Observações"):
            st.write(f"**Técnico / Analista:** {resultado.iloc[0].get('Tecnico / Analista', '')}")
            st.write(f"**Nota de Risco:** {resultado.iloc[0].get('Nota de Risco', '')}")
            st.write(f"**Limite Toler Risco:** {resultado.iloc[0].get('Limite Toler  Risco', '')}")
            st.write(f"**Faixa de Risco:** {resultado.iloc[0].get('Faixa de Risco', '')}")
            st.write(f"**Data de Vínculo Fiscal:** {resultado.iloc[0].get('Data de Vinculo Fiscal', '')}")
            st.write(f"**Dias após Envio da PC:** {resultado.iloc[0].get('Dias apos Envio da PC', '')}")
            st.write(f"**Anotações / Observações:** {resultado.iloc[0].get('ANOTACOES OBS', '')}")

        # ⚠️ Bloco 6 — Alertas
        with st.expander("Alertas"):
            st.write(f"**ALERTA de Execução Financeira:** {resultado.iloc[0].get('ALERTA de  Execucao Financeira', '')}")
            st.write(f"**ALERTA Sem Desembolso:** {resultado.iloc[0].get('ALERTA Sem Desembolso', '')}")
            st.write(f"**ALERTA Sem Pgt + 150 Dias:** {resultado.iloc[0].get('ALERTA Sem Pgt + 150 Dias', '')}")
            st.write(f"**Acórdão TCU1203:** {resultado.iloc[0].get('Acordao  TCU1203', '')}")
            st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('GRAU DE PRIORIDADE', '')}")

    else:
        st.warning("Convênio não encontrado na base de dados.")

# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima</p>",
    unsafe_allow_html=True
)
