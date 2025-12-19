from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv() 


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3
    )

# if __name__ == "__main__":
#     llm = get_llm()
#     res = llm.invoke("Say hello in one sentence")
#     print(res.content)
