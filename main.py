import streamlit as st
import google.generativeai as genai
import pypdf

# Configuração visual do site
st.set_page_config(page_title="Analisador de Viagens", page_icon="✈️")

st.title("✈️ Analisador de Cotações Inteligente")
st.markdown("---")

# Puxa a chave de forma segura dos Secrets do Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Erro: A chave API não foi configurada nos Secrets do Streamlit.")
    st.stop()

arquivo = st.file_uploader("Arraste seu PDF de cotação aqui", type="pdf")

if arquivo:
    with st.spinner('✨ IA analisando os detalhes da viagem...'):
        try:
            # Lendo o PDF
            reader = pypdf.PdfReader(arquivo)
            texto = "".join([page.extract_text() for page in reader.pages])
            
            # Comando para a IA
            prompt = f"Aja como um agente de viagens sênior. Resuma esta cotação em tópicos com emojis, destacando Voos, Horários, Cia, Preço Total e Bagagem. Texto: {texto}"
            resposta = model.generate_content(prompt)
            
            # Mostra o resultado bonito
            st.subheader("📋 Resumo da Cotação")
            st.info(resposta.text)
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
