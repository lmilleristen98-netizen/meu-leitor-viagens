import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="Leitor de Cotações", page_icon="✈️")
st.title("✈️ Analisador de Cotações Inteligente")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chave API não configurada nos Secrets.")
    st.stop()

arquivo = st.file_uploader("Arraste seu PDF aqui", type="pdf")

if arquivo:
    with st.spinner('Analisando cotação...'):
        try:
            reader = pypdf.PdfReader(arquivo)
            texto = "".join([page.extract_text() for page in reader.pages])
            
            # Tentamos o 1.5 flash, se falhar, tentamos o 1.0 pro automaticamente
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                resposta = model.generate_content(f"Resuma: {texto}")
            except:
                model = genai.GenerativeModel('gemini-1.0-pro')
                resposta = model.generate_content(f"Resuma esta cotação: {texto}")
            
            st.subheader("📋 Resumo")
            st.write(resposta.text)
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
