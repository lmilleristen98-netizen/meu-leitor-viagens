import streamlit as st
import google.generativeai as genai
import pypdf
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Analisador Premium", page_icon="✈️")
st.title("✈️ Analisador de Cotações Completo")

# Conexão com a IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("Configure a chave nos Secrets.")
    st.stop()

arquivo = st.file_uploader("Suba sua cotação (PDF)", type="pdf")

if arquivo:
    with st.spinner('🔍 Extraindo absolutamente tudo...'):
        try:
            # 1. Leitura do texto
            reader = pypdf.PdfReader(arquivo)
            texto_bruto = ""
            for page in reader.pages:
                texto_bruto += page.extract_text()
            
            # 2. Prompt Ultra Detalhado
            prompt = f"""
            Aja como um agente de viagens detalhista. Transcreva TODAS as informações deste PDF sem omitir nada.
            
            ESTRUTURA OBRIGATÓRIA:
            - ✈️ NOME DA CIA AÉREA: (Destaque bem grande)
            - 🛫 TRECHOS E VOOS: (Liste todos: Origem, Destino, Número do Voo)
            - ⏱️ HORÁRIOS E DURAÇÃO: (Horário de saída, chegada e tempo total de cada voo)
            - 🔄 ESCALAS: (Local da escala e tempo exato de espera no aeroporto)
            - 🧳 BAGAGEM E REGRAS: (O que está incluso)
            - 💰 VALORES: (Preço por pessoa e total)
            
            Texto original: {texto_bruto}
            """
            
            resposta = model.generate_content(prompt)
            resumo_final = resposta.text
            
            # 3. Exibição na Tela
            st.markdown("---")
            st.subheader("📋 Informações Extraídas")
            st.info(resumo_final)
            
            # 4. BOTÕES DE AÇÃO
            col1, col2 = st.columns(2)
            
            with col1:
                # Botão para baixar em formato de texto (mais fácil para WhatsApp)
                st.download_button(
                    label="📥 Baixar Resumo (TXT)",
                    data=resumo_final,
                    file_name="resumo_viagem.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Link rápido para WhatsApp (copia o texto e abre o zap)
                texto_zap = resumo_final.replace('\n', '%0A')
                link_zap = f"https://wa.me/?text={texto_zap[:1000]}" # Limite de caracteres para o link
                st.markdown(f'''
                    <a href="{link_zap}" target="_blank">
                        <button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                            📲 Compartilhar no WhatsApp
                        </button>
                    </a>
                ''', unsafe_allow_html=True)

            st.balloons()

        except Exception as e:
            st.error(f"Erro: {e}")
