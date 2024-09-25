import streamlit as st
import base64
import vertexai
import pandas as pd
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from streamlit_pdf_viewer import pdf_viewer
from streamlit_js_eval import streamlit_js_eval
from io import BytesIO
import os
from src.gemini import gemini, str2json
from config.config import *  
import textwrap

# Page configurations
st.set_page_config(
    page_title="Equatorial - Assistente Jurídico",
    page_icon="👤",
    layout="wide"
)

header_col1, header_col2 = st.columns([2, 10])
header_col2.header('Assistente Jurídico')
header_col1.image("data/logo.png")

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

# Initialize variables

part_extension = {"pdf":"application/pdf", "jpeg":"image/jpeg", "jpg":"image/jpeg", "png":"image/png", "mp4":"video/mp4", "xlsx":"text/plain"}

project_id = os.environ.get("GCP_PROJECT")  # Your Google Cloud Project ID
location_id = os.environ.get("GCP_REGION")  # Your Google Cloud Project Region
page_height = streamlit_js_eval(js_expressions='screen.height', key='height',  want_output = True,)

vertexai.init(project=project_id, location=location_id)

if "page" not in st.session_state:
  st.session_state.page = "juridico"
elif st.session_state.page != "juridico":
    st.session_state.bt_run = False
    clear_cache()
    st.rerun()
if "uploaded_file"not in st.session_state:
    st.session_state.uploaded_file = False
if "model" not in st.session_state:
    st.session_state.model = GenerativeModel(
        "gemini-1.5-pro-001",
        system_instruction=[INSTRUCOES_SISTEMA],
    )

uploaded_file = st.file_uploader("Subir inicial:", type=['pdf'] )

tom = st.radio(
    "Qual o tom da resposta?",
    ["Casual", "Formal"],
)

if tom == "Casual":
    tonalidade = PROMPT_TOM_CASUAL
else:
    tonalidade = PROMPT_TOM_FORMAL

if uploaded_file is not None:
    st.session_state.bytes_data = uploaded_file.read()
    filename = uploaded_file.name
    file_extension = filename.split('.')[-1]
    mime_type = part_extension[file_extension]
    st.session_state.file = Part.from_data(
        mime_type=mime_type, data = st.session_state.bytes_data)
    st.session_state.uploaded_file = True

    if st.button("Obter dados"):
        st.session_state.dados_processo = {}
        st.session_state.motivo = {}
        response = ""

        ok = False
        i = 0
        while (not ok) & (i < 5):
            with st.spinner('Processando...'):
                try:
                    response = st.session_state.model.generate_content(
                        [PROMPT_DADOS.format(tonalidade = tonalidade), st.session_state.file, "JSON: "],
                        generation_config=GENERATION_CONFIG,
                        safety_settings=SAFETY_SETTINGS,
                        stream=False,
                    ).text
                    st.session_state.dados_processo = str2json(response)
                    
                    if "pedidos" not in st.session_state.dados_processo:
                        content = [PROMPT_MOTIVO, "**Processo**: ", st.session_state.file, "JSON: "]
                    else:
                        if type(st.session_state.dados_processo["pedidos"]) == list:
                            if st.session_state.dados_processo["pedidos"][-1][0] == '-':
                                st.session_state.dados_processo["pedidos"] = '\n'.join(st.session_state.dados_processo["pedidos"])
                            else:
                                st.session_state.dados_processo["pedidos"] = '\n- '.join(st.session_state.dados_processo["pedidos"])
                                st.session_state.dados_processo["pedidos"] = '- '+st.session_state.dados_processo["pedidos"]

                            
                            print(st.session_state.dados_processo["pedidos"])
                        content = [PROMPT_MOTIVO, "**Pedidos**: ",st.session_state.dados_processo["pedidos"], "JSON: "]
                    response = st.session_state.model.generate_content(
                        content,
                        generation_config=GENERATION_CONFIG,
                        safety_settings=SAFETY_SETTINGS,
                        stream=False,
                    ).text
                    st.session_state.motivo = str2json(response)
                    ok = True
                except Exception as e:
                    st.write("Aconteceu um erro, vamos reprocessar")
                    st.error(e)
                    st.write(response)
            i = i + 1

if "dados_processo" in st.session_state:

    col1, col2 = st.columns([3,2])

    with col1:
        if "autor" in st.session_state.dados_processo:
            st.markdown("**Autor:**")
            st.markdown(st.session_state.dados_processo["autor"])
        if "cpf_cnpj" in st.session_state.dados_processo:
            st.markdown("**CPF/CNPJ:**")
            st.markdown(st.session_state.dados_processo["cpf_cnpj"])
        if "endereco" in st.session_state.dados_processo:
            st.markdown("**Endereço:**")
            st.markdown(st.session_state.dados_processo["endereco"])
        if "representante" in st.session_state.dados_processo:
            st.markdown("**Representante:**")
            st.markdown(st.session_state.dados_processo["representante"])
        if "representante" in st.session_state.dados_processo:
            st.markdown("**Unidade Consumidora:**")
            st.markdown(st.session_state.dados_processo["uc"])
        if "cpf" in st.session_state.dados_processo:
            st.markdown("**CPF:**")
            st.markdown(st.session_state.dados_processo["cpf"])
        if "advogado" in st.session_state.dados_processo:
            st.markdown("**Advogado:**")
            st.markdown(st.session_state.dados_processo["advogado"])
        if "fatos" in st.session_state.dados_processo:
            st.markdown("**Fatos:**")
            texto_formatado = st.session_state.dados_processo["fatos"].replace("$", r"\$")
            st.write(texto_formatado)

        if "pedidos" in st.session_state.dados_processo:
            st.markdown("**Pedidos:**")
            texto_formatado = st.session_state.dados_processo["pedidos"].replace("$", r"\$")
            st.write(texto_formatado)

        st.markdown("#### Motivos principais:")
        for key, value in st.session_state.motivo.items():
            if value:
                st.markdown("- "+key)
        st.write("")
        st.write("Obs: É possível alterar a forma que os resultados são gerados.")
        st.write("Obs: Os motivos principais devem ser mapeados para aparecerem adequadamente.")
    
    with col2:
        pdf_viewer(st.session_state.bytes_data, height=int(page_height))

else:
    st.markdown("### Suba um arquivo.")

st.write("")
if st.button("Reiniciar Demo"):
    clear_cache()
    st.rerun()