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
    with st.spinner('Analisando...'):
        try:
            reader = pypdf.PdfReader(arquivo)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text()
            
            # MUDANÇA AQUI: Usando o nome simplificado do modelo
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            resposta = model.generate_content(texto)
            
            st.subheader("📋 Resumo")
            st.write(resposta.text)
            st.balloons()
            
        except Exception as e:
            # Se o erro 404 persistir, ele mostrará detalhes aqui
            st.error(f"Erro ao processar: {e}")
