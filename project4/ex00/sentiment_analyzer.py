import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurações das APIs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

github_comments = [
	{
    	"text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
    	"sentiment": ""
	},
	{
    	"text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
    	"sentiment": ""
	},
	{
    	"text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
    	"sentiment": ""
	},
	{
    	"text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
    	"sentiment": ""
	},
	{
    	"text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
    	"sentiment": ""
	},
	{
    	"text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
    	"sentiment": ""
	},
	{
    	"text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
    	"sentiment": ""
	},
	{
    	"text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
    	"sentiment": ""
	},
	{
    	"text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
    	"sentiment": ""
	},
	{
    	"text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
    	"sentiment": ""
	}
]

def create_prompt(comment: str):
    # Estrutura do prompt com as tags XML
    prompt = f"""
    <prompt>
		Nossa equipe de atendimento ao cliente está sobrecarregada com feedback não estruturado. Sua tarefa é classificar os sentimentos dos comentários do GitHub. Use estas classificações: Positivo e Negativo. Aqui estão dois exemplos:

        <exemplos>
			Texto: Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.
			<resposta_esperada>Sentimento: Positivo</resposta_esperada>
            
            Texto: Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.
			<resposta_esperada>Sentimento: Negativo</resposta_esperada>
		</exemplos>
        
        Aqui está o comentário que você deve classificar:
        {comment}
	</prompt>
    """
    return prompt.strip()

def call_gemini(prompt):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def call_llm(text):
	prompt = create_prompt(text)
	return call_gemini(prompt)

def parse_llm_response(response):
    sentiment = response.split("Sentimento: ")[1].strip()
    return sentiment

def analyze_sentiments(comments):
	for comment in comments:
		llm_response = call_llm(comment["text"])
		comment["sentiment"] = parse_llm_response(llm_response)

analyze_sentiments(github_comments)

# Imprimir resultados
for comment in github_comments:
	print(f"Texto: {comment['text']}")
	print(f"Sentimento: {comment['sentiment']}")
	print("-" * 50)