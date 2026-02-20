main.py
%%writefile app.py
import streamlit as st
import google.generativeai as genai
import pypdf

# Configuração visual da página
st.set_page_config(page_title="Assistente de Viagens", page_icon="✈️", layout="centered")

# Estilo visual (CSS) para ficar bonitão
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Analisador de Cotações Inteligente")
st.info("Suba seu PDF e deixe a IA organizar tudo para você.")

# Sua chave API
genai.configure(api_key="AIzaSyDlKxhPf_I3Jepq1ay9gYTM4J4y2W8Xx6I")
model = genai.GenerativeModel('gemini-1.5-flash')

arquivo = st.file_uploader("Arraste seu PDF aqui", type="pdf")

if arquivo:
    with st.spinner('✨ IA analisando os detalhes da viagem...'):
        # Lendo o PDF
        reader = pypdf.PdfReader(arquivo)
        texto = "".join([page.extract_text() for page in reader.pages])

        # Prompt para um resumo elegante
        prompt = f"Aja como um agente de viagens sênior. Resuma esta cotação em um formato elegante com emojis, destacando Voos, Horários, Companhia, Preço Total e observações de Bagagem. Texto: {texto}"
        
        try:
            resposta = model.generate_content(prompt)
            st.subheader("📋 Resumo Organizado")
            st.markdown(resposta.text)
            st.balloons() # Efeito de celebração quando termina
        except Exception as e:
            st.error(f"Erro: {e}")
