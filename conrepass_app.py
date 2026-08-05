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
    
    # Caixa de login compacta usando colunas
    col_login, _ = st.columns([1, 2])
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
    
    # Carregamento seguro da base de dados
    df = pd.read_csv(
        "convenios.csv",
        sep=";",   
        encoding="latin1",
        dtype={"CNPJ": str},
        converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
    )
    df.columns = df.columns.str.strip()

    st.title("🔍 Consulta de Convênios (Conrepass)")

    # Seleção de convênio em formato compacto no topo da tela
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        instrumentos = sorted(df["Instrumento"].dropna().unique())
        instrumento = st.selectbox("Selecione o número do convênio:", instrumentos)

    if instrumento:
        # Filtra o registro selecionado
        resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
        
        if not resultado.empty:
            idx_registro = resultado.index[0]
            
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

            # Armazena inputs modificáveis no session_state para não perder dados ao mudar de bloco
            key_data = f"data_pc_{instrumento}"
            key_obs = f"obs_{instrumento}"
            
            if key_data not in st.session_state:
                st.session_state[key_data] = str(resultado.iloc[0].get('Data de Envio da  PC', '')).strip()
            if key_obs not in st.session_state:
                st.session_state[key_obs] = str(resultado.iloc[0].get('ANOTACOES OBS', '')).strip()

            # Botão de Salvar Alterações fixo na barra lateral
            if st.sidebar.button("💾 Salvar Alterações", use_container_width=True):
                df.loc[idx_registro, 'Data de Envio da  PC'] = st.session_state[key_data]
                df.loc[idx_registro, 'ANOTACOES OBS'] = st.session_state[key_obs]
                df.to_csv("convenios.csv", sep=";", encoding="latin1", index=False)
                st.sidebar.success("Alterações salvas!")

            # Botão de Exportar CSV geral fixo na barra lateral
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
                    st.write(f"**Instrumento:** {resultado.iloc[0].get('Instrumento', '')}")
                    st.write(f"**Ano:** {resultado.iloc[0].get('Ano', '')}")
                    st.write(f"**Modalidade:** {resultado.iloc[0].get('Modalidade', '')}")
                    st.write(f"**Processo SEI:** {resultado.iloc[0].get('Processo SEI', '')}")
                with col_b:
                    st.write(f"**Nome Proponente:** {resultado.iloc[0].get('Nome Proponente', '')}")
                    st.write(f"**CNPJ:** {resultado.iloc[0].get('CNPJ', '')}")
                    st.write(f"**Situação:** {resultado.iloc[0].get('Situacao', '')}")
                st.info(f"**Objeto:** {resultado.iloc[0].get('Objeto', '')}")

            elif "📅 Vigência / Datas" in menu_blocos:
                st.write(f"**Início Vigência:** {resultado.iloc[0].get('Inicio Vigencia', '')}")
                st.write(f"**Fim Vigência:** {resultado.iloc[0].get('Fim Vigencia', '')}")
                st.write(f"**Data Limite para Apresentar PC:** {resultado.iloc[0].get('Data Limite para Apresentar PC', '')}")
                
                # Campo editável (Sincronizado com a memória)
                st.session_state[key_data] = st.text_input(
                    "📅 Prestação de Contas Apresentada em:",
                    value=st.session_state[key_data]
                )

            elif "📊 Execução Financeira" in menu_blocos:
                col_c, col_d = st.columns(2)
                with col_c:
                    st.write(f"**Valor Global:** R$ {resultado.iloc[0].get('Valor Global', '')}")
                    st.write(f"**Valor Empenhado:** R$ {resultado.iloc[0].get('Valor Empenhado', '')}")
                    st.write(f"**Valor Liberado:** R$ {resultado.iloc[0].get('Valor Liberado', '')}")
                    st.write(f"**Valor de Contrapartida:** R$ {resultado.iloc[0].get('Valor de Contrapartida', '')}")
                    st.write(f"**Ingresso de R$ (Rendimentos/Contrapartida):** {resultado.iloc[0].get('Ingresso de $', '')}")
                with col_d:
                    st.write(f"**Total em Movimentações:** R$ {resultado.iloc[0].get('Total em Movimentacoes Financeiras', '')}")
                    st.write(f"**Saldo em Conta:** R$ {resultado.iloc[0].get('Saldo em conta', '')}")
                    st.write(f"**Vl Devolvido:** R$ {resultado.iloc[0].get('Vl Devolvido', '')}")
                    st.write(f"**Execução Financeira Conc./Conv.:** R$ {resultado.iloc[0].get('Execucao  Financeira Concedente  e Convenente', '')}")
                    st.write(f"**Devolução de Saldo p/ União:** R$ {resultado.iloc[0].get('Devolucao de Saldo p Uniao', '')}")
                st.warning(f"**Resto a Pagar:** R$ {resultado.iloc[0].get('Resto a Pagar', '')}")

            elif "📑 Prestação de Contas" in menu_blocos:
                col_e, col_f = st.columns(2)
                with col_e:
                    st.write(f"**Dias de Atraso Envio da PC:** {resultado.iloc[0].get('Dias de Atraso Envio da PC', '')}")
                    st.write(f"**PC Informatizada:** {resultado.iloc[0].get('PC Informatizada', '')}")
                    st.write(f"**Nota de Risco:** {resultado.iloc[0].get('Nota de Risco', '')}")
                    st.write(f"**Limite Toler Risco:** {resultado.iloc[0].get('Limite Toler  Risco', '')}")
                    faixa = resultado.iloc[0].get('Faixa de Risco', '')
                    st.write(f"**Faixa de Risco:** {faixa if not pd.isna(faixa) else 'Não informado'}")
                    st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('Grau de Prioridade', '')}")
                with col_f:
                    st.write(f"**Relatórios de Execução:** {resultado.iloc[0].get('Relatorios de Execucao', '')}")
                    st.write(f"**Ação de Monitoramento:** {resultado.iloc[0].get('Acao de Monitoramnto', '')}")
                    st.write(f"**Parecer Financeiro:** {resultado.iloc[0].get('Parecer Financeiro', '')}")
                    st.write(f"**Parecer Tec-Mérito:** {resultado.iloc[0].get('Parecer Tec -Merito', '')}")
                    st.write(f"**Análise de Equipamentos:** {resultado.iloc[0].get('Analise de Equipamentos', '')}")
                    st.write(f"**Ação de Análise de PC:** {resultado.iloc[0].get('Acao de Analise de PC', '')}")
                st.info(f"**Percentual de Evolução da Análise:** {resultado.iloc[0].get('Percentual de Evolucao da Analise', '')}")
                st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.iloc[0].get('Pareceres Incluidos na Plataforma', '')}")

            elif "📝 Monitoramento" in menu_blocos:
                col_g, col_h = st.columns(2)
                with col_g:
                    st.write(f"**Situação do Convênio:** {resultado.iloc[0].get('Status de Execucao', '')}")
                    st.write(f"**Percentual de Execução:** {resultado.iloc[0].get('Percental  Exec', '')}")
                with col_h:
                    st.write(f"**Técnico / Analista:** {resultado.iloc[0].get('Tecnico / Analista', '')}")
                    st.write(f"**Data de Vínculo Fiscal:** {resultado.iloc[0].get('Data de Vinculo Fiscal', '')}")

            elif "⚠️ Alertas" in menu_blocos:
                st.error(f"⚠️ **ALERTA de Execução Financeira:** {resultado.iloc[0].get('ALERTA de Execucao Financeira', '')}")
                st.error(f"⚠️ **ALERTA Sem Desembolso:** {resultado.iloc[0].get('ALERTA Sem Desembolso', '')}")
                st.error(f"⚠️ **ALERTA Sem Pgt + 150 Dias:** {resultado.iloc[0].get('ALERTA Sem Pgt + 150 Dias', '')}")
                st.write(f"**Acórdão TCU1203:** {resultado.iloc[0].get('Acordao  TCU1203', '')}")
                st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('GRAU DE PRIORIDADE', '')}")

            elif "🗒️ Anotações e OBS" in menu_blocos:
