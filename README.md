
# Equatorial - Assistente Jurídico

**Equatorial - Assistente Jurídico** é uma aplicação Python, construída com Streamlit e Vertex AI, projetada para ajudar no processamento e análise de documentos jurídicos, automatizando extração de dados e fornecendo classificações automáticas para casos jurídicos. A aplicação faz upload de arquivos, processa informações e interage com modelos generativos da Google Cloud Vertex AI.

## Características

- Upload e visualização de arquivos PDF.
- Extração automática de dados relevantes (autor, CPF/CNPJ, advogado, etc.) dos documentos.
- Geração de respostas com diferentes tons (casual ou formal).
- Classificação automatizada dos motivos dos processos jurídicos.
- Integração com Google Cloud Vertex AI para uso de modelos generativos.

## Estrutura do Projeto

```
Equatorial-Assistente-Jurídico
│
├── config            # Configurações do sistema e prompts
│   └── config.py
├── data              # Contém o logo da empresa e outros arquivos de dados
│   └── logo.png
├── src               # Scripts principais do projeto
│   └── gemini.py     # Interação com o modelo generativo do Vertex AI
├── home.py           # Script principal que define a interface e a lógica da aplicação
├── Dockerfile        # Definições para a criação do container Docker
├── cloudbuild.yaml   # Configurações do Cloud Build para CI/CD
├── README.md         # Documentação do projeto
└── requirements.txt  # Dependências necessárias para o projeto
```

## Configuração do Ambiente

O projeto depende de variáveis de ambiente que podem ser definidas diretamente no ambiente de execução:

- `GCP_PROJECT`: ID do projeto no Google Cloud.
- `GCP_REGION`: Região configurada no Google Cloud para executar os serviços.

## Requisitos

O projeto depende de várias bibliotecas de terceiros, listadas no arquivo `requirements.txt`. Para instalá-las, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Uso

Após configurar o ambiente e instalar as dependências, você pode iniciar o projeto localmente com o Streamlit:

```bash
streamlit run home.py
```

Isso abrirá a interface do Assistente Jurídico, permitindo o upload de arquivos, extração de dados e geração de respostas.

## Implantação

O projeto está configurado para ser implantado no Google Cloud Run, utilizando um fluxo de CI/CD definido no arquivo `cloudbuild.yaml`. O processo inclui os seguintes passos:

1. Construir a imagem Docker.
2. Fazer o push da imagem para o Google Artifact Registry.
3. Implantar a imagem no Cloud Run.

## Construído Com

- Python
- Streamlit
- Google Cloud Vertex AI
- Google Cloud Storage

## Autores

Equipe de Desenvolvimento - Equatorial Energia

---

Distribuído sob a Licença MIT.
