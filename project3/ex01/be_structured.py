import re

def format_prompt(descricao_emprego: str) -> str:
    """
    Gera um prompt formatado com base em uma descrição de emprego para ser utilizado em modelos de IA.
    
    :param descricao_emprego: Uma string contendo a descrição completa do emprego.
    :return: Uma string formatada com as principais seções extraídas da descrição do emprego.
    """
    # Dicionário para armazenar as seções formatadas
    secoes_formatadas = {
        'Job Title': '',
        'Location': '',
        'About The Job': '',
        'Minimum Qualifications': '',
        'Preferred Qualifications': '',
        'Responsibilities': ''
    }

    # Expressões regulares para capturar as partes da descrição
    titulo_regex = r'(Software Engineer, Early Career)'
    localizacao_regex = r'(Greater São Paulo Area|Belo Horizonte|São Paulo|State of São Paulo|State of Minas Gerais)'
    sobre_o_trabalho_regex = r'About The Job(.*?)Responsibilities'
    qualificacoes_minimas_regex = r'Minimum qualifications:(.*?)(?:Preferred qualifications|$)'
    qualificacoes_preferidas_regex = r'Preferred qualifications:(.*?)(?:About The Job|Responsibilities|$)'
    responsabilidades_regex = r'Responsibilities(.*?)(?:Google is proud to be an equal opportunity workplace|$)'

    # Capturar as seções relevantes
    titulo_match = re.search(titulo_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if titulo_match:
        secoes_formatadas['Job Title'] = titulo_match.group(1).strip()

    localizacao_match = re.search(localizacao_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if localizacao_match:
        secoes_formatadas['Location'] = localizacao_match.group(1).strip()

    sobre_o_trabalho_match = re.search(sobre_o_trabalho_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if sobre_o_trabalho_match:
        secoes_formatadas['About The Job'] = sobre_o_trabalho_match.group(1).strip()

    qualificacoes_minimas_match = re.search(qualificacoes_minimas_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if qualificacoes_minimas_match:
        secoes_formatadas['Minimum Qualifications'] = qualificacoes_minimas_match.group(1).strip()

    qualificacoes_preferidas_match = re.search(qualificacoes_preferidas_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if qualificacoes_preferidas_match:
        secoes_formatadas['Preferred Qualifications'] = qualificacoes_preferidas_match.group(1).strip()

    responsabilidades_match = re.search(responsabilidades_regex, descricao_emprego, re.IGNORECASE | re.DOTALL)
    if responsabilidades_match:
        secoes_formatadas['Responsibilities'] = responsabilidades_match.group(1).strip()

    # Formatar o prompt para IA
    prompt = (
        f"Job Title: {secoes_formatadas['Job Title']}\n"
        f"Location: {secoes_formatadas['Location']}\n\n"
        f"About The Job:\n{secoes_formatadas['About The Job']}\n\n"
        f"Minimum Qualifications:\n{secoes_formatadas['Minimum Qualifications']}\n\n"
        f"Preferred Qualifications:\n{secoes_formatadas['Preferred Qualifications']}\n\n"
        f"Responsibilities:\n{secoes_formatadas['Responsibilities']}\n"
    )

    return prompt.strip()

def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()
        formatted_prompt = format_prompt(job_description)
        print(formatted_prompt)

if __name__ == "__main__":
	main()