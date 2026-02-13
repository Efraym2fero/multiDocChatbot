import streamlit as st
from chains import Chain


class ChatUI:
    def __init__(self):
        self.chain = Chain()
    
    def pageConfig(self,title = "Fero's chatbot pdf-assistant",icon = "🤖",header = "Fero's chatbot assistant 🤖"):
        st.set_page_config(page_title = title, page_icon = icon)
        st.header(header)
    
    def sideBar(self):
        if "vectorstore" not in st.session_state:
            st.session_state.vectorstore = None

        with st.sidebar:
            st.subheader("Your docs")
            docs = st.file_uploader("Upload your docs here",accept_multiple_files = True)
            if st.button("Process"):
                    with st.spinner("Processing documents..."):
                        rawText = self.chain.pdfToText(docs)
                        chunks = self.chain.textToChunks(rawText)
                        vs = self.chain.chunksToEmbeddings(chunks)
                        st.session_state.vectorstore = vs
                        st.success("Ready!")

    def pageForm(self):

        if 'messages' not in st.session_state:
            st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi there!I am Fero, How can I help you today?")
            }
        ]


        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        userText = st.chat_input("Ask something")
        
        if userText:
            st.session_state.messages.append(
                {"role": "user", "content": userText})
            with st.chat_message("user"):
                st.markdown(userText)
            with st.chat_message("assistant"):
                if st.session_state.vectorstore is None:
                    reply = "Please upload and process documents first."
                else:
                    with st.spinner("Thinking..."):
                        reply = self.chain.getRAGChain(
                                st.session_state.vectorstore,userText)                            
                st.session_state.messages.append(
                        {"role": "assistant", "content": reply})
                st.markdown(reply)
        
        
                


                


            
