import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="Leitor de Cotações", page_icon="✈️")
st.title("✈️ Analisador de Cotações Inteligente")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Mudando para a versão 2.0 que é a mais atual
    model = genai.GenerativeModel('gemini-2.0-flash-exp') 
else:
    st.error("Configure a chave nos Secrets.")
    st.stop()

arquivo = st.file_uploader("Suba seu PDF aqui", type="pdf")

if arquivo:
    with st.spinner('IA analisando com Gemini 2.0...'):
        try:
            reader = pypdf.PdfReader(arquivo)
            texto = "".join([page.extract_text() for page in reader.pages])
            
            resposta = model.generate_content(f"Resuma esta cotação: {texto}")
            
            st.subheader("📋 Resumo")
            st.info(resposta.text)
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
