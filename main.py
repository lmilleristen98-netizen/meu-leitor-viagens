import streamlit as st
import google.generativeai as genai
import pypdf

# Configuração da página
st.set_page_config(page_title="Leitor de Cotações", page_icon="✈️")
st.title("✈️ Analisador de Cotações Inteligente")

# Configuração da Chave API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chave API não configurada nos Secrets.")
    st.stop()

arquivo = st.file_uploader("Arraste seu PDF aqui", type="pdf")

if arquivo:
    with st.spinner('Analisando cotação...'):
        try:
            # Extração de texto simplificada
            reader = pypdf.PdfReader(arquivo)
            texto_completo = ""
            for pagina in reader.pages:
                texto_completo += pagina.extract_text()
            
            # Chamada da IA
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Resuma os pontos principais desta cotação de viagem (Voos, Datas, Preços): {texto_completo}"
            
            resposta = model.generate_content(prompt)
            
            st.subheader("📋 Resumo")
            st.write(resposta.text)
            st.balloons()
            
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
