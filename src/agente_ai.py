# src/agente_ai.py

import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o modelo de linguagem do Azure OpenAI
llm = AzureChatOpenAI(
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

def gerar_testes(caminho_arquivo: str) -> str:
    """
    Lê um arquivo Python, envia seu conteúdo para o modelo de IA e
    retorna o código de teste gerado.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            codigo_fonte = file.read()
    except FileNotFoundError:
        return f"Erro: Arquivo não encontrado em '{caminho_arquivo}'"

    prompt = f"""
    Você é um agente de IA especializado em gerar testes de unidade para código Python usando a biblioteca 'pytest'.
    Sua tarefa é analisar o código Python fornecido e gerar um arquivo de teste completo e funcional.

    Requisitos:
    1. O código de teste deve começar com 'import pytest'.
    2. Crie funções de teste (def test_*) para cada função no código-fonte.
    3. Inclua testes para casos de sucesso e, quando aplicável, para casos de falha (usando pytest.raises).
    4. Adicione comentários curtos para explicar o propósito de cada teste.
    5. O código retornado deve ser apenas o conteúdo puro do arquivo de teste, sem textos adicionais, explicações ou blocos de código markdown.
    
    Código-fonte Python para análise:
    ---
    {codigo_fonte}
    ---
    
    Código de teste gerado:
    """
    
    # Envia o prompt para o modelo de IA e obtém a resposta
    resposta = llm.invoke(prompt)
    
    # Retorna o conteúdo da resposta, que é o código de teste
    return resposta.content

def main(caminho_arquivo: str):
    """
    Função principal que orquestra a leitura do arquivo, a geração de testes e o salvamento.
    """
    print(f"Gerando testes para o arquivo: {caminho_arquivo}...")
    
    # Gera o código de teste
    codigo_teste = gerar_testes(caminho_arquivo)
    
    if codigo_teste.startswith("Erro"):
        print(codigo_teste)
        return

    # Define o nome do arquivo de saída
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_teste = f"test_{nome_base}.py"
    
    diretorio_saida = "tests"
    os.makedirs(diretorio_saida, exist_ok=True)
    caminho_saida = os.path.join(diretorio_saida, nome_teste)

    # Salva o código de teste em um novo arquivo
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(codigo_teste)
    
    print(f"Sucesso! Testes gerados e salvos em: {caminho_saida}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python agente_ai.py <caminho_do_arquivo_python>")
        sys.exit(1)
        
    caminho_do_arquivo = sys.argv[1]
    main(caminho_do_arquivo)