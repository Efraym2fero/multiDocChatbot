import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS 
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings


from PyPDF2 import PdfReader

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


class Chain:
    def __init__(self):
        self.llm = ChatMistralAI(model = "mistral-small-2506", temperature = 0, api_key = api_key,max_tokens = 256)

    def pdfToText(self,docs):
        txt = ""

        for doc in docs:
            pdfReader = PdfReader(doc)
            for p in pdfReader.pages:
                txt+=p.extract_text()
        return txt

    def textToChunks(self,txt):
        txtSplitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50 )
        chunks = txtSplitter.split_text(txt)
        return chunks
    
    def chunksToEmbeddings(self,chunks):
        embeddings =  HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorStore = FAISS.from_texts(texts=chunks, embedding=embeddings)

        return vectorStore
    
    
    def getRAGChain(self,vectorStore,ques):
        retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

        prompt = ChatPromptTemplate.from_template("""
        You are an assistant for question-answering tasks made by AI Engineer Efraym Emad.

        Use the retrieved context below to answer the question.
        If you don't know the answer, say you don't know.

        Answer in **max 3 concise sentences**.

        Question:
        {question}

        Context:
        {context}

        Answer:
        """)

        rag_chain = (
                {
                    "context": retriever | format_docs,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )
        return rag_chain.invoke(ques)

    



