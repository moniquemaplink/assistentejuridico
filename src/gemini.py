from google.cloud import storage
from google.protobuf.json_format import MessageToDict
import json
import requests
import re
import pandas as pd
import streamlit as st

import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

# src/gemini.py

def gemini(
    project_id: str,
    location: str,
    contents: str,
    temperature: float
) -> dict:

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": temperature,
        "top_p": 0.7,
    }

    response = model.generate_content(contents, stream=False, generation_config=generation_config,
                                     safety_settings=safety_settings,
                                     ).text

    return response

def str2json(text):
    response = text
    json_pos = re.finditer("```json", response)

    start_pos = [m.span()[1] for m in json_pos]
    if len(start_pos) > 0:
        start_pos = start_pos[0]
        response = response[start_pos:]

    json_pos = re.finditer("```", response)
    end_pos = [m.span()[0] for m in json_pos]
    if len(end_pos) > 0:
        end_pos = end_pos[0]
        response = response[:end_pos]
    response = response.replace("False", "false").replace("True", "true")

    try:
        return json.loads(response.strip())
    except Exception as error:
        print(error)
        return {}
