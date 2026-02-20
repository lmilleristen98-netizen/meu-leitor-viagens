import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="Analisador de Viagens", page_icon="✈️")
st.title("✈️ Analisador de Cotações Inteligente")

# Conexão com a chave de API dos Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Atualizado para o modelo Gemini 2.5 conforme sugerido pela documentação
    model = genai.GenerativeModel('gemini-2.5-flash') 
else:
    st.error("Configure a chave nos Secrets do Streamlit.")
    st.stop()

arquivo = st.file_uploader("Suba seu PDF de cotação aqui", type="pdf")

if arquivo:
    with st.spinner('✨ IA analisando com Gemini 2.5...'):
        try:
            reader = pypdf.PdfReader(arquivo)
            texto = "".join([page.extract_text() for page in reader.pages])
            
            # Gerando o resumo profissional
            prompt = f"Aja como um agente de viagens sênior. Resuma esta cotação em tópicos com emojis: Voos, Horários, Cia, Preço Total e Bagagem. Texto: {texto}"
            resposta = model.generate_content(prompt)
            
            st.subheader("📋 Resumo da Cotação")
            st.info(resposta.text)
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
