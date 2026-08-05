import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("🎛️ Painel Guardiã")
st.sidebar.markdown("---")

# Seletor do Aplicativo que gerencia o fluxo de telas
escolha_app = st.sidebar.radio(
    "Selecione o Sistema:",
    [
        "🏠 Menu Inicial",
        "🔍 Consulta Conrepass",
        "📊 Relatório de Acompanhamento"
    ],
    index=["🏠 Menu Inicial", "🔍 Consulta Conrepass", "📊 Relatório de Acompanhamento"].index(st.session_state["app_selecionado"])
)

# Atualiza a memória de navegação caso o usuário altere a opção manual no menu
st.session_state["app_selecionado"] = escolha_app
st.sidebar.markdown("---")

# --- EXECUÇÃO DINÂMICA DAS TELAS ---
if st.session_state["app_selecionado"] == "🏠 Menu Inicial":
    st.title("🛡️ Guardiã dos Dados — Hub Central de Convênios")
    st.subheader("Bem-vindo ao painel integrado de controle e monitoramento de instrumentos.")
    st.markdown("---")
    
    # Criação de cards visuais modernos para seleção rápida no corpo da página
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 🔍 Consulta Conrepass\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        if st.button("Abrir Conrepass ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🔍 Consulta Conrepass"
            st.rerun()
            
    with col_cards_2:
        st.success("### 📊 Relatório de Acompanhamento\nFormulário de preenchimento automatizado em 4 blocos sequenciais com exportação de dados booleanos.")
        if st.button("Abrir Relatório ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📊 Relatório de Acompanhamento"
            st.rerun()
