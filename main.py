import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Analisador de Viagens", page_icon="✈️")
st.title("✈️ Analisador de Cotações Ultra-Preciso")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("Configure a chave nos Secrets.")
    st.stop()

arquivo = st.file_uploader("Suba sua cotação (PDF)", type="pdf")

if arquivo:
    with st.spinner('🕵️ Analisando o documento visualmente para não errar...'):
        try:
            # Enviando o arquivo diretamente para a IA (sem extração manual de texto)
            # Isso evita que as colunas do PDF se misturem
            pdf_data = arquivo.read()
            conteudo_input = [
                {
                    "mime_type": "application/pdf",
                    "data": pdf_data
                },
                f"""
                Analise visualmente este documento de cotação. Não invente dados.
                Se houver tabelas, leia linha por linha com cuidado.
                
                ESTRUTURA OBRIGATÓRIA:
                ✈️ NOME DA CIA AÉREA: (Identifique a empresa principal)
                
                🛫 TRECHOS E VOOS: (Liste cada voo com sua origem e destino exatos)
                
                ⏱️ HORÁRIOS E DURAÇÃO: (Saída, Chegada e o tempo total de voo de cada trecho)
                
                🔄 ESCALAS: (Identifique as paradas. Calcule o tempo entre a chegada do voo anterior e a saída do próximo)
                
                🧳 BAGAGEM E REGRAS: (O que está incluso e o que é pago)
                
                💰 VALORES: (Preço total final com taxas)
                """
            ]
            
            resposta = model.generate_content(conteudo_input)
            
            st.markdown("---")
            st.subheader("📋 Relatório de Viagem")
            st.info(resposta.text)
            
            # Botões de Ação
            st.download_button("📥 Baixar Resumo", resposta.text, file_name="cotacao_corrigida.txt")
            
            zap_link = f"https://wa.me/?text={resposta.text[:900].replace(' ', '%20')}"
            st.markdown(f'[📲 Enviar para o WhatsApp]({zap_link})')
            
        except Exception as e:
            st.error(f"Erro na análise: {e}")
