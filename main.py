import streamlit as st
import google.generativeai as genai
import pypdf

# Configuração da Página
st.set_page_config(page_title="Analisador Preciso", page_icon="✈️")
st.title("✈️ Analisador de Cotações (Versão Colab)")

# 1. Configuração de Segurança (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chave API não configurada nos Secrets.")
    st.stop()

# Função que você usou no Colab para nunca errar o modelo
def buscar_modelo_disponivel():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return None

arquivo = st.file_uploader("Suba seu PDF aqui", type="pdf")

if arquivo:
    with st.spinner('A IA está lendo conforme as configurações que deram certo...'):
        try:
            # Lógica de leitura do seu código do Colab
            reader = pypdf.PdfReader(arquivo)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text()

            # Busca automática do melhor modelo (Gemini 1.5, 2.5, etc)
            modelo_nome = buscar_modelo_disponivel()
            
            if not modelo_nome:
                st.error("Nenhum modelo disponível para esta chave.")
            else:
                model = genai.GenerativeModel(modelo_nome)
                
                # Usei o seu prompt exato
                prompt = f"""
                Resuma esta cotação de viagem em tópicos simples e claros.
                Identifique detalhadamente:
                - Nome da Cia Aérea
                - Todos os voos e números
                - Horários e tempos de escala (muito importante)
                - Preços totais
                
                Texto: {texto}
                """
                
                resposta = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📋 Resumo da Cotação")
                st.info(resposta.text)
                
                # Opções de compartilhamento
                st.download_button("📥 Baixar Resumo", resposta.text, file_name="resumo.txt")
                
                zap_link = f"https://wa.me/?text={resposta.text[:900].replace(' ', '%20')}"
                st.markdown(f'[📲 Enviar para WhatsApp]({zap_link})')
                
                st.balloons()
                
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
