from openai import OpenAI
from scripts.utils.config import GROQ_API_KEY, GROQ_MODEL

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def format_answer(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)
    prompt = f"""You are a very friendly Hunza travel agent. 
    Answer the question below using only the provided context. If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        print("LLM Error:", e)
        return "Sorry, something went wrong while generating the answer."