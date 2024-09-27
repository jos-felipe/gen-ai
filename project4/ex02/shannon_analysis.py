import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configurações das APIs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def run_gemini(model_name, prompt, system_instructions):
	model=genai.GenerativeModel(
		model_name=model_name,
		system_instruction=system_instructions)
	response = model.generate_content(prompt)
	return response.text

def run_prompt_chain():
	prompt_chain = [
		"""
		<Task>Elaborate an essay about the life and carrer of Claude Shannon.<\Task>
		<Instructions>Include information about his early life, education, and major contributions to the field of computer science.<\Instructions>
		""",
		"""
		<Task>Analyze the contributions of Claude Shannon's on the theory of information.<\Task>
		<Instructions>Discuss the relevance of his work in the context of modern computer science and telecommunications.<\Instructions>
		<Reference_1>
		""",
		"""
		<Task>Explore the impact of Claude Shannon's job on modern computer science and on communication technology.<\Task>
		<Instructions>Discuss the relevance of his work in the context of modern computer science and telecommunications.<\Instructions>
		<Reference_1>
		""",
		"""
		<Task>Elaborate an essay about the life and carrer of Claude Shannon, regarding the given information as reference:<\Task>
		<Instructions>Include information about his early life, education, and major contributions to the field of computer science.<\Instructions>
		<Reference_1>
		""",
	]
	result_1 = run_gemini("gemini-1.5-flash", prompt_chain[0], "Write an essay about Claude Shannon.")
	result_2 = run_gemini("gemini-1.5-flash", prompt_chain[1] + result_1 + "</Reference_1>", "Analyze the contributions of Claude Shannon.")
	result_3 = run_gemini("gemini-1.5-flash", prompt_chain[2] + result_1 + "</Reference_1>\n<Reference_2>" + result_2 + "</Reference_2>\n", "Explore the impact of Claude Shannon's job.")
	result_4 = run_gemini("gemini-1.5-flash", prompt_chain[3] + result_1 + "</Reference_1>\n<Reference_2>" + result_2 + "</Reference_2>\n<Reference_3>" + result_3 + "</Reference_3>", "Write an essay about Claude Shannon.")

	final_result = f"Claude Sannon: A Pioneer in Computer Science\n\nEarly life:\n{result_1}\n\nMajor Contributions:\n{result_2}\n\nImpact on Modern Technology:\n{result_3}\n\Full essay:\n{result_4}"

	print(final_result)
	return final_result

if __name__ == "__main__":
	run_prompt_chain()
