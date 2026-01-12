import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_vectors")

PROMPT_TEMPLATE = """
CONTEXTO DISPONÍVEL:
{context}

INSTRUÇÕES OBRIGATÓRIAS:

Responda exclusivamente com base nas informações explicitamente presentes no CONTEXTO.

Não utilize conhecimento externo, prévio ou implícito.

Não faça inferências, deduções, suposições ou interpretações além do que está literalmente escrito.

Não complemente informações ausentes, mesmo que pareçam óbvias.

Não emita opiniões, avaliações, julgamentos ou conclusões próprias.

REGRA DE FALTA DE INFORMAÇÃO:
Se a resposta não estiver clara, completa ou explicitamente descrita no CONTEXTO, responda exatamente com a frase abaixo (sem alterações):

"Não tenho informações necessárias para responder sua pergunta."

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:

Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

FORMATO DA RESPOSTA:

Seja objetivo e direto.

Use apenas o texto necessário para responder.

Não explique o raciocínio.

Não cite trechos do contexto a menos que a pergunta peça explicitamente.

PERGUNTA DO USUÁRIO:
{question}

"""

def get_embeddings_model():
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif os.getenv("GOOGLE_API_KEY"):
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    else:
        raise ValueError("Nenhuma API Key encontrada (OPENAI ou GOOGLE).")

def get_llm():
    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("OPENAI_CHAT_MODEL")
        if not model:
            model = "gpt-5-nano"
        return ChatOpenAI(model=model, temperature=0)
    elif os.getenv("GOOGLE_API_KEY"):
        model = os.getenv("GEMINI_CHAT_MODEL")
        if not model:
            model = "gemini-2.5-flash-lite"
        return ChatGoogleGenerativeAI(model=model, temperature=0)
    else:
        raise ValueError("Nenhuma API Key encontrada.")
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def search_prompt(question):
    embeddings = get_embeddings_model()
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}"