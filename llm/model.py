from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(streaming: bool = False):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3,
        streaming=streaming,

        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
        }
    )


# if __name__ == "__main__":
#     llm = get_llm()
#     res = llm.invoke("Say hello in one sentence")
#     print(res.content)
