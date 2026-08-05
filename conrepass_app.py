import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# Senha fixa
senha_correta = "ditre123"

# Inicializa o estado de acesso na sessão se não existir
if "acesso_liberado" not in st.session_state:
    st.session_state["acesso_liberado"] = False

# --- TELA DE LOGIN SEGURA ---
if not st.session_state["acesso_liberado"]:
    st.title("🔐 Guardiã dos Dados - Autenticação")
    
    col_login, _ = st.columns()
    with col_login:
        senha = st.text_input("Digite a senha para acessar:", type="password")
        if st.button("Entrar", use_container_width=True):
            if senha == senha_correta:
                st.session_state["acesso_liberado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta! Tente novamente.")

# --- APLICATIVO PRINCIPAL LIBERADO ---
if st.session_state["acesso_liberado"]:
    
    # Carregamento da base de dados
    df = pd.read_csv(
        "convenios.csv",
        sep=";",   
        encoding="latin1",
        dtype={"CNPJ": str},
        converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
    )
    df.columns = df.columns.str.strip()

    st.title("🔍 Consulta de Convênios (Conrepass)")

    # Seleção de convênio compacta
    col_sel, _ = st.columns()
    with col_sel:
        instrumentos = sorted(df["Instrumento"].dropna().unique())
        instrumento = st.selectbox("Selecione o número do convênio:", instrumentos)

    if instrumento:
        # Filtra o registro selecionado
        resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
        
        if not resultado.empty:
            idx_registro = resultado.index[0]
            
            # --- MEMÓRIA ESTÁVEL PARA EDIÇÃO (Garante digitação fluida) ---
            key_data = f"data_pc_{instrumento}"
            key_obs = f"obs_{instrumento}"
            
            if key_data not in st.session_state:
                valor_inicial_data = resultado["Data de Envio da  PC"].values[0]
                st.session_state[key_data] = str(valor_inicial_data).strip() if pd.notna(valor_inicial_data) else ""
                
            if key_obs not in st.session_state:
                valor_inicial_obs = resultado["ANOTACOES OBS"].values[0]
                st.session_state[key_obs] = str(valor_inicial_obs).strip() if pd.notna(valor_inicial_obs) else ""

            # --- MENU LATERAL VERTICALIZADO ---
            st.sidebar.header("Menu de Controle")
            
            menu_blocos = st.sidebar.radio(
                "Selecione o Bloco de Informações",
                [
                    "🔑 Identificação",
                    "📅 Vigência / Datas",
                    "📊 Execução Financeira",
                    "📑 Prestação de Contas",
                    "📝 Monitoramento",
                    "⚠️ Alertas",
                    "🗒️ Anotações e OBS"
                ]
            )
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("Ações do Repass")

            # Botão de Salvar Alterações
            if st.sidebar.button("💾 Salvar Alterações", use_container_width=True):
                df.loc[idx_registro, 'Data de Envio da  PC'] = st.session_state[key_data]
                df.loc[idx_registro, 'ANOTACOES OBS'] = st.session_state[key_obs]
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.sidebar.success("Alterações salvas com sucesso!")

            # Botão de Exportar CSV
            csv_data = df.to_csv(sep=";", index=False).encode("latin1")
            st.sidebar.download_button(
                label="📥 Baixar Base Completa",
                data=csv_data,
                file_name="convenios_atualizado.csv",
                mime="text/csv",
                use_container_width=True
            )

            # --- CONTEÚDO DINÂMICO CONFORME SELEÇÃO DO MENU ---
            st.markdown("---")
            st.subheader(f"📌 {menu_blocos} — Convênio nº {instrumento}")

            if "🔑 Identificação" in menu_blocos:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Instrumento:** {resultado['Instrumento'].values[0]}")
                    st.write(f"**Ano:** {resultado['Ano'].values[0]}")
                    st.write(f"**Modalidade:** {resultado['Modalidade'].values[0]}")
                    st.write(f"**Processo SEI:** {resultado['Processo SEI'].values[0]}")
                with col_b:
                    st.write(f"**Nome Proponente:** {resultado['Nome Proponente'].values[0]}")
                    st.write(f"**CNPJ:** {resultado['CNPJ'].values[0]}")
                    st.write(f"**Situação:** {resultado['Situacao'].values[0]}")
                st.info(f"**Objeto:** {resultado['Objeto'].values[0]}")

            elif "📅 Vigência / Datas" in menu_blocos:
                st.write(f"**Início Vigência:** {resultado['Inicio Vigencia'].values[0]}")
                st.write(f"**Fim Vigência:** {resultado['Fim Vigencia'].values[0]}")
                st.write(f"**Data Limite para Apresentar PC:** {resultado['Data Limite para Apresentar PC'].values[0]}")
                
                # Campo totalmente editável e liberado para digitação
                st.text_input("📅 Prestação de Contas Apresentada em:", key=key_data)

            elif "📊 Execução Financeira" in menu_blocos:
                col_c, col_d = st.columns(2)
                with col_c:
                    st.write(f"**Valor Global:** R$ {resultado['Valor Global'].values[0]}")
                    st.write(f"**Valor Empenhado:** R$ {resultado['Valor Empenhado'].values[0]}")
                    st.write(f"**Valor Liberado:** R$ {resultado['Valor Liberado'].values[0]}")
                    st.write(f"**Valor de Contrapartida:** R$ {resultado['Valor de Contrapartida'].values[0]}")
                    st.write(f"**Ingresso de R$ (Rendimentos/Contrapartida):** {resultado['Ingresso de $'].values[0]}")
                with col_d:
                    st.write(f"**Total em Movimentações:** R$ {resultado['Total em Movimentacoes Financeiras'].values[0]}")
                    st.write(f"**Saldo em Conta:** R$ {resultado['Saldo em conta'].values[0]}")
                    st.write(f"**Vl Devolvido:** R$ {resultado['Vl Devolvido'].values[0]}")
                    st.write(f"**Execução Financeira Conc./Conv.:** R$ {resultado['Execucao  Financeira Concedente  e Convenente'].values[0]}")
                    st.write(f"**Devolução de Saldo p/ União:** R$ {resultado['Devolucao de Saldo p Uniao'].values[0]}")
                st.warning(f"**Resto a Pagar:** R$ {resultado['Resto a Pagar'].values[0]}")

            elif "📑 Prestação de Contas" in menu_blocos:
                col_e, col_f = st.columns(2)
                with col_e:
                    st.write(f"**Dias de Atraso Envio da PC:** {resultado['Dias de Atraso Envio da PC'].values[0]}")
                    st.write(f"**PC Informatizada:** {resultado['PC Informatizada'].values[0]}")
                    st.write(f"**Nota de Risco:** {resultado['Nota de Risco'].values[0]}")
                    st.write(f"**Limite Toler Risco:** {resultado['Limite Toler  Risco'].values[0]}")
                    faixa = resultado['Faixa de Risco'].values[0]
                    st.write(f"**Faixa de Risco:** {faixa if not pd.isna(faixa) else 'Não informado'}")
                    st.write(f"**Grau de Prioridade:** {resultado['Grau de Prioridade'].values[0]}")
                with col_f:
                    st.write(f"**Relatórios de Execução:** {resultado['Relatorios de Execucao'].values[0]}")
                    st.write(f"**Ação de Monitoramento:** {resultado['Acao de Monitoramnto'].values[0]}")
                    st.write(f"**Parecer Financeiro:** {resultado['Parecer Financeiro'].values[0]}")
                    st.write(f"**Parecer Tec-Mérito:** {resultado['Parecer Tec -Merito'].values[0]}")
                    st.write(f"**Análise de Equipamentos:** {resultado['Analise de Equipamentos'].values[0]}")
                    st.write(f"**Ação de Análise de PC:** {resultado['Acao de Analise de PC'].values[0]}")
                st.info(f"**Percentual de Evolução da Análise:** {resultado['Percentual de Evolucao da Analise'].values[0]}")
                st.write(f"**Pareceres Incluídos na Plataforma:** {resultado['Pareceres Incluidos na Plataforma'].values[0]}")

            elif "📝 Monitoramento" in menu_blocos:
                col_g, col_h = st.columns(2)
                with col_g:
                    st.write(f"**Situação do Convênio:** {resultado['Status de Execucao'].values[0]}")
                    st.write(f"**Percentual de Execução:** {resultado['Percental  Exec'].values[0]}")
                with col_h:
                    st.write(f"**Técnico / Analista:** {resultado['Tecnico / Analista'].values[0]}")
                    st.write(f"**Data de Vínculo Fiscal:** {resultado['Data de Vinculo Fiscal'].values[0]}")

            elif "⚠️ Alertas" in menu_blocos:
                st.error(f"⚠️ **ALERTA de Execução Financeira:** {resultado['ALERTA de Execucao Financeira'].values[0]}")
                st.error(f"⚠️ **ALERTA Sem Desembolso:** {resultado['ALERTA Sem Desembolso'].values[0]}")
                st.error(f"⚠️ **ALERTA Sem Pgt + 150 Dias:** {resultado['ALERTA Sem Pgt + 150 Dias'].values[0]}")
                st.write(f"**Acórdão TCU1203:** {resultado['Acordao  TCU1203'].values[0]}")
                st.write(f"**Grau de Prioridade:** {resultado['GRAU DE PRIORIDADE'].values[0]}")

            elif "🗒️ Anotações e OBS" in menu_blocos:
                # Campo de texto totalmente fluido, reativo e desbloqueado
                st.text_area("🗒️ Modifique as observações do convênio:", key=key_obs, height=250)

# --- RODAPÉ DISCRETO PADRONIZADO ---
st.markdown("---")
st.markdown("Bartolomeu Lima - Corecon-ES 1541",unsafe_allow_html=True)
