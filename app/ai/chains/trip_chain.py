# # from fastapi import FastAPI, HTTPException
# from app.ai.client import get_llm
# from app.ai.vectorstore import get_vectorstore
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_classic.chains.retrieval import create_retrieval_chain
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# from app.ai.prompts.system_prompt import itinerary_prompt
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
# from app.schemas.trip_response import TripItinerary

# llm = get_llm()

# structured_llm=llm.with_structured_output(TripItinerary)

# vectorstore = get_vectorstore()

# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# prompt = ChatPromptTemplate.from_messages([
#     ("system", itinerary_prompt),
#     ("human", "{input}")
# ])

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)


# rag_chain=(
#     {
#     "context":retriever |format_docs, "input":RunnablePassthrough()
#     }
#     |prompt
    
#     |structured_llm
    
#     )

# def invoke_chain(user_query:str)->str:
#         response = rag_chain.invoke(user_query)
#         return response
    





         

        
    
from app.ai.client import get_llm
from app.ai.vectorstore import get_vectorstore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.ai.prompts.system_prompt import itinerary_prompt

llm = get_llm()

vectorstore = get_vectorstore()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", itinerary_prompt),
        ("human", "{input}")
    ]
)


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


rag_chain = (
    {
        "context": retriever | format_docs,
        "input": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


async def stream_chain(user_query: str):

    async for chunk in rag_chain.astream(user_query):
        yield chunk