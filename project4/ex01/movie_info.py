import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurações das APIs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def create_prompt(movie_title: str):
	# Prompt pré-preenchido para ser utilizado
	user_prompt = f"""
	Provide information about the movie "{movie_title}" in JSON format.

	Start your response with:
	{{
		"title": "{movie_title}",
	"""
	return user_prompt.strip()

def call_gemini(prompt):
	genai.configure(api_key=GOOGLE_API_KEY)
	model = genai.GenerativeModel("gemini-1.5-flash")
	response_json = model.generate_content(prompt)
	return response_json.text

def structured_output(response):
	movie_info = ["title", "year", "director", "genre", "plot"]
	output = {}
	for info in movie_info:
		if info in response:
			output[info] = response[info]
		else:
			output[info] = None
	return output

def get_movie_info(text):
	prompt = create_prompt(text)
	result = call_gemini(prompt)
	result_json = json.loads(result)
	return structured_output(result_json)

# Como o seu programa será chamado:
movie_titles = ["The Matrix", "Inception", "Pulp Fiction", "The Shawshank Redemption", "The Godfather"]

for title in movie_titles:
	print(f"\nAnalyzing: {title}")
	result = get_movie_info(title)
	if result:
		for key, value in result.items():
			print(f"{key}: {value}")
	else:
		# Tratamento de erro adequado
		print("Erro ao obter informações do filme.")
	print("-" * 50)
