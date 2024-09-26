import os
import requests

# Configurações das APIs
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

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
    
def process_gemini(content: dict):
    return content["candidates"][0]["content"]["parts"][0]["text"]

def create_prompt(role, task, topic, specific_question):
    # Estrutura do prompt com as tags XML
    prompt = f"""
    <prompt>
		A partir da estrutura xml abaixo:
		<role>{role}</role>
		<task>{task}</task>
		<topic>{topic}</topic>
		<specific_question>{specific_question}</specific_question>
		
		Responda a pergunta {specific_question}, usando a estrutura abaixo:
		1. Explicação básica do conceito:

		2. Analogia do cotidiano:
		
		3. Solução passo a passo da pergunta:
		
		4. Exemplo detalhado:
		
		5. Dica prática para iniciantes:
	</prompt>
    """
    return prompt.strip()

# Exemplo de uso
role = "especialista em filosofia e história da ciência"
task = "explicar o pensamento de Descartes e sua influência para iniciantes em filosofia"
topic = "René Descartes e o Método Cartesiano"
specific_question = "Quem foi René Descartes e qual é o significado da frase 'Penso, logo existo'?"

# Gerando o prompt
prompt = create_prompt(role, task, topic, specific_question)
# print(prompt)
response = process_gemini(query_gemini(prompt))
print("\nResposta do Gemini 1.5 Flash:")
print(response)
