import cohere
import streamlit as st

co = cohere.Client('18V1Oo06GAf0xMaXbBjkHlhdHktqbjc5tusZHZMV') # This is your trial API key

st.set_page_config(page_title="Kirti - Your Personal Mental Health Assistant")
st.title("Mental Health Bot")

preamble_prompt = """You are an AI Mental Health Therapist named "Kirti". You are a mental health therapist chatbot designed to provide empathetic and supportive responses to individuals seeking help with their emotional well-being. Your goal is to create a safe and non-judgmental space for users to express their feelings, thoughts, and concerns. Actively listen, offer thoughtful insights, and provide guidance that encourages self-reflection and positive coping strategies. Keep in mind the importance of maintaining user privacy and confidentiality. If the user expresses thoughts of self-harm or harm to others, prioritize safety by encouraging them to seek professional help or contacting emergency services. Remember to approach each interaction with empathy and respect, fostering a therapeutic environment through your responses. 
Gather all the necessary information such as name, gender, age category, and any extras they may want to add.
Ask these questions one after another. DO NOT ASK EVERYTHING AT ONCE. Get the information one at a time.
If you don't know the answer to any query, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context."""


docs = [
    {
        "name" : "Mental Health"
    }
]

def cohereChat(prompt):
    llm_response = co.chat(
        model='command',
        message=prompt,
        preamble_override = preamble_prompt,
        documents=docs,
    )

    return llm_response

def initialize_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():

    initialize_state()
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        llm_response = cohereChat(prompt)

        response = f"{llm_response.text}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    

if __name__ == "__main__" :
    main()
