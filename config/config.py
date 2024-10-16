import vertexai.preview.generative_models as generative_models


PROMPT_DADOS = """Identifique e extraia exatamente as informações abaixo.
- autor da ação (Nome completo da pessoa ou empresa)
- CPF ou CNPJ do autor da ação
- Se for uma empresa, nome completo do representante
- Se for uma empresa, CPF do representante
- Unidade consumidora (UC), se disponível
- Endereço completo da unidade consumidora
- Advogado da ação (Nome completo)
- Número do processo judicial
- Conta contrato ou instalação
- Texto com um resumo dos fatos: especifique os fatos em dois parágrafos
- Classificação da decisão judicial, se é acordo ou sentença
- Se for sentença, verificar a existência de Acórdão
- Trazer as informações da decisão (o que deve ser realizado pela empresa)
- Uma lista completa com os pedidos resumidos em bullet points
- Números de protocolos mencionados pelo cliente

{tonalidade}

Devolva no formato JSON {{
    "autor":"",
    "cpf_cnpj":"",
    "representante":"",
    "cpf":"",
    "uc":"",
    "endereco":"",
    "advogado":"",
    "numero_processo":"",
    "conta_contrato_instalacao":"",
    "fatos":"",
    "classificacao_decisao":"",
    "existencia_acordao":"",
    "informacoes_decisao":"",
    "pedidos":"",
    "numeros_protocolos":""
}}"""


PROMPT_MOTIVO = """Classificar o motivo do processo, selecionando todas as categorias aplicáveis da lista abaixo. Devolva no formato JSON com valores booleanos

**Motivos:**
- Bloquear Cobrança: O cliente contesta a cobrança e solicita o cancelamento
- Retirar Negativação: Remover registro negativo existente em birôs de crédito como Serasa e SPC
- Bloquear Negativação: Impedir a inclusão de registro negativo em birôs de crédito
- Religação de Energia: Restabelecer o fornecimento de energia interrompido
- Bloquear Corte: Impedir a interrupção do fornecimento de energia
- Ligação Nova: Solicitar a instalação de energia em um novo ponto
- Vistoria: Solicitar uma vistoria técnica na unidade consumidora
- Outros: Motivos não cobertos pelas categorias acima

**Saída**: JSON com valores booleanos indicando as categorias aplicáveis

"""

PROMPT_TOM_CASUAL = "O tom dos resumos deve ser casual, amigável e fácil de entender, como se você estivesse explicando para um amigo que não é da área jurídica. Use linguagem simples, evite jargões e seja conciso"

PROMPT_TOM_FORMAL = "Escreva de forma jurídica para advogados experientes."

INSTRUCOES_SISTEMA = "Você é uma advogada muito experiente que trabalha na empresa Equatorial Energia. Você é muito detalhista, e proativa. Responda de forma minuciosa sobre o processo jurídico."

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

GENERATION_CONFIG = {
    "max_output_tokens": 4048,
    "temperature": 0.0,
    "top_p": 0.8,
}