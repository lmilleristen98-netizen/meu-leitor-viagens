import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Analisador de Viagens", page_icon="✈️")
st.title("✈️ Analisador de Cotações (Modo Precisão)")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("Chave não configurada nos Secrets!")
    st.stop()

arquivo = st.file_uploader("Suba o PDF original aqui", type="pdf")

if arquivo:
    with st.spinner('🕵️ Fazendo varredura visual completa no PDF...'):
        try:
            pdf_data = arquivo.read()
            
            # Comando ultra-rígido para evitar alucinações
            prompt = """
            INSTRUÇÃO CRÍTICA: Extraia os dados deste PDF com precisão cirúrgica. 
            Não tente adivinhar. Se houver tabelas, siga a ordem das linhas.
            
            1. ✈️ CIA AÉREA: Nome da companhia principal.
            2. 🛫 VOOS: Origem, Destino e Número do Voo para CADA trecho.
            3. ⏱️ HORÁRIOS: Saída e Chegada exatas (como no PDF).
            4. 🔄 ESCALAS: Tempo que o passageiro fica parado entre o pouso de um voo e a decolagem do próximo.
            5. 🧳 REGRAS: Bagagens e taxas incluídas.
            6. 💰 TOTAL: Valor final da cotação.
            
            Responda apenas com os dados encontrados, sem comentários adicionais.
            """
            
            conteudo = [
                {"mime_type": "application/pdf", "data": pdf_data},
                prompt
            ]
            
            resposta = model.generate_content(conteudo)
            resultado = resposta.text
            
            st.markdown("---")
            st.subheader("📋 Relatório Conferido")
            st.info(resultado)
            
            # Opções de compartilhamento
            st.download_button("📥 Baixar Relatório", resultado, file_name="resumo_viagem.txt")
            zap_link = f"https://wa.me/?text={resultado[:900].replace(' ', '%20')}"
            st.markdown(f'[📲 Enviar para WhatsApp]({zap_link})')
            
        except Exception as e:
            st.error(f"Erro na análise: {e}")
