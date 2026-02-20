import streamlit as st
import google.generativeai as genai
import pypdf

# 1. Configuração Visual (O que você vê na tela)
st.set_page_config(page_title="Analisador de Viagens", page_icon="✈️")

st.title("✈️ Analisador de Cotações Inteligente")
st.markdown("---")

# 2. Conexão com a IA (Resolvendo o erro de Chave e o Erro 404)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usando a versão 'latest' para evitar o erro 404 mostrado na sua imagem
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
else:
    st.error("Erro: A chave API não foi configurada nos Secrets do Streamlit.")
    st.stop()

# 3. Área de Upload (O campo azul que você quer usar)
arquivo = st.file_uploader("Suba seu PDF de cotação aqui", type="pdf")

if arquivo:
    with st.spinner('✨ IA analisando os detalhes da viagem...'):
        try:
            # Lendo o PDF enviado
            reader = pypdf.PdfReader(arquivo)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text()
            
            # Instrução para a IA gerar o resumo bonito
            prompt = f"Aja como um agente de viagens sênior. Resuma esta cotação em tópicos com emojis, destacando: Atendente, Voos, Horários, Cia, Preço Total e Bagagem. Texto: {texto}"
            
            resposta = model.generate_content(prompt)
            
            # Exibindo o resultado na tela
            st.subheader("📋 Resumo da Cotação")
            st.info(resposta.text)
            st.balloons() # Balões de comemoração quando termina!
            
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
