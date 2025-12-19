from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="text-embedding-004"
    )
