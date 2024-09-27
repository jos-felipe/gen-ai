from chroma import ChromaClient
from sentence_transformers import SentenceTransformer
import os
import PyPDF2

def process_pdf_directory(pdf_directory, collection):
	for filename in os.listdir(pdf_directory):
		if filename.endswith(".pdf"):
			file_path = os.path.join(pdf_directory, filename)
			with open(file_path, "rb") as file:
				reader = PyPDF2.PdfFileReader(file)
				text = ""
				for page_num in range(reader.numPages):
					text += reader.getPage(page_num).extract_text()
				metadata = {"source": filename}
				collection.add(text, metadata=metadata)

def main():
	persist_directory = "./chroma_data"
	pdf_directory = "./pdfs"

	chroma_client = ChromaClient(persist_directory=persist_directory)
	
	model_name = "paraphrase-multilingual-MiniLM-L12-v2"
	embedding_function = SentenceTransformer(model_name).encode

	collection_name = "resume_collection"
	if collection_name in chroma_client.list_collections():
		collection = chroma_client.get_collection(collection_name)
	else:
		collection = chroma_client.create_collection(collection_name, embedding_function)

	process_pdf_directory(pdf_directory, collection)

# TODO: Implementar a função interactive_query_loop
interactive_query_loop(collection)
if __name__ == "__main__":
main()