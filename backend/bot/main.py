from dotenv import load_dotenv
import os
import cohere


load_dotenv()

api = os.getenv('api')
co = cohere.Client(api)

def generate(chat, documents=None):

    if documents==None:
        response = co.generate(
            model='command',
            prompt=f"""
        Explain the following legal clause in simple terms:
        {chat}
        Your answer should be easy to understand by someone with no legal background.
        """,
            max_tokens=200,
        )
    else:
        response = co.generate(
            model='xlarge',
            prompt=f"""
        Explain the following legal clause in simple terms:
        {chat}
        Your answer should be easy to understand by someone with no legal background.
        """,
            max_tokens=100,
            documents=documents
        )
    return response
    


def test():
    chat = input("Your prompt: ")
    response = generate(chat)
    print(response.generations[0].text)

if __name__ == "__main__":
    test()