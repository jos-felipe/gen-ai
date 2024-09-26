import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurações das APIs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def format_prompt(document: str):
    # return zero_shot_prompt(document)
    return few_shot_prompt(document)

def zero_shot_prompt(document: str):
    """Formata a descrição da vaga em um zero shot prompt estruturado"""

    prompt = f"""Analise a seguinte descrição de emprego e extraia as seguintes informações em um formato estruturado:
    
    * **Cargo:**
    * **Empresa:**
    * **Localização:**
    * **Responsabilidades Principais:** (liste no máximo 5)
    * **Qualificações Necessárias:** (liste no máximo 5)
    * **Salário:** (se mencionado)
    * **Benefícios:** (se mencionados)
    
    **Descrição do Emprego:**
    ```
    {document}
    ```
    """
    return prompt


def few_shot_prompt(document: str):
    """Formata a descrição da vaga em um few shot prompt estruturado"""

    prompt = f"""Analise a seguinte descrição de emprego e extraia as seguintes informações em um formato estruturado:
    
    **Exemplo 1:**

    * **Descrição do Emprego:** "Estamos buscando um Desenvolvedor de Software experiente para se juntar à nossa equipe em São Paulo. Você será responsável por projetar, desenvolver e testar novas funcionalidades para nosso aplicativo móvel. Precisamos de alguém com fortes habilidades em Java e experiência com desenvolvimento Android. Oferecemos um salário competitivo e um excelente pacote de benefícios."

    * **Informações Extraídas:**
        * Cargo: Desenvolvedor de Software
        * Empresa: Não mencionada
        * Localização: São Paulo
        * Responsabilidades Principais:
            * Projetar novas funcionalidades
            * Desenvolver funcionalidades
            * Testar funcionalidades
        * Qualificações Necessárias:
            * Fortes habilidades em Java
            * Experiência com desenvolvimento Android
        * Salário: Competitivo
        * Benefícios: Excelente pacote

    **Exemplo 2:**

    * **Descrição do Emprego:** "Procuramos um Analista de Marketing Digital para criar e gerenciar campanhas de marketing online. O candidato ideal terá experiência com ferramentas de análise de dados e mídias sociais. Esta é uma posição remota com salário a combinar."

    * **Informações Extraídas:**
        * Cargo: Analista de Marketing Digital
        * Empresa: Não mencionada
        * Localização: Remota
        * Responsabilidades Principais:
            * Criar campanhas de marketing online
            * Gerenciar campanhas de marketing online
        * Qualificações Necessárias:
            * Experiência com ferramentas de análise de dados
            * Experiência com mídias sociais
        * Salário: A combinar
        * Benefícios: Não mencionados
    
    **Agora, analise a seguinte descrição de emprego e extraia as mesmas informações:**
    ```
    {document}
    ```
    """
    return prompt


def process_gemini(content: dict):
    return content["candidates"][0]["content"]["parts"][0]["text"]


def process_groq(content: dict):
    return content["choices"][0]["message"]["content"]


def process_qwen2(content: bytes):
    lines = content.decode("utf-8").splitlines()

    response_parts = []

    for line in lines:
        try:
            data = json.loads(line)
            if data.get("done"):
                break
            response_parts.append(data["response"])
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {line}")

    full_response = "".join(response_parts)
    return full_response


def query_gemini(prompt: str):
    print("Consultando Gemini...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Erro na requisição da API do Gemini: {e}"
        )


def query_groq(prompt: str):
    print("Consultando Groq...")
    try:
        url = f"https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "model": "llama3-8b-8192",
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Erro na requisição da API do Groq: {e}"
        )


def query_qwen2(prompt: str):
    print("Consultando Ollama...")
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "qwen2:1.5b",
            "prompt": prompt,
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Erro na requisição da API do Ollama: {e}"
        )


def query_all_models(prompt: str):
    """Consulta todos os modelos e retorna as respostas."""
    return {
        "Gemini_1.5_Flash": process_gemini(query_gemini(prompt)),
        "Groq_Llama3_8b_8192": process_groq(query_groq(prompt)),
        "Ollama_Qwen2:1.5b": process_qwen2(query_qwen2(prompt)),
    }


def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()

    formatted_prompt = format_prompt(job_description)
    results = query_all_models(formatted_prompt)
    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)


if __name__ == "__main__":
    main()
