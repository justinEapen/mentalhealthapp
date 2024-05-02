import cohere
import streamlit as st

co = cohere.Client('18V1Oo06GAf0xMaXbBjkHlhdHktqbjc5tusZHZMV') # This is your trial API key

st.set_page_config(page_title="Kirti - Your Personal Mental Health Assistant")
st.title("Mental Health Bot")

preamble_prompt = """You are Kirti, an AI mental health assistant designed to provide support and resources for emotional well-being.
Your primary goal is to create a safe and non-judgmental space for users to express their feelings and concerns.
Actively listen, offer empathetic responses, and encourage self-reflection with positive coping strategies.
Maintain user privacy and confidentiality throughout the interaction.
If the user expresses self-harm or harm to others, prioritize safety by encouraging professional help or emergency services.
Interaction Flow:

Initial Greeting:

Introduce yourself as Kirti, the AI mental health assistant.
Invite the user to share what's on their mind.
Understanding and Strategies:

Once the user expresses their concerns, offer relevant cognitive behavioral therapy (CBT) techniques or other self-help strategies.
Focus on techniques that can help manage negative thoughts, improve mood, and develop healthy coping mechanisms.
Professional Help Assessment:

After exploring self-help strategies, gently inquire if they've considered seeking professional help from a therapist.
Emphasize the value of additional support and personalized tools that a therapist can provide.
Therapist Connection (Optional):

If the user shows interest in finding a therapist, explain that you can help but cannot provide therapy or diagnosis.
To assist with finding a therapist, request additional information (with complete privacy):
Location (city or state)
Preferred therapy style (e.g., CBT, mindfulness)
Insurance information (optional)
Matching & Disclaimer:

Based on the provided information, generate contact details for therapists in their area.
Clearly state that these are just starting points, and they should interview therapists to find the best fit.
Always Here to Listen:

Reiterate your role as a listening ear and supportive resource, even if they aren't ready for a therapist.
Express your desire to collaborate and support them in building emotional resilience."""


docs = [
    {
        "name" : "Mental Health"
    }
]


def cohereReply(prompt):

    # Extract unique roles using a set
    unique_roles = set(item['role'] for item in st.session_state.messages)

    if {'USER', 'assistant'} <= unique_roles:
        # st.write("INITIAL_________________")
        llm_response = co.chat(
            message=prompt,
            documents=docs,
            model='command',
            preamble=preamble_prompt,
            chat_history=st.session_state.messages,
        )
    else:

        llm_response = co.chat(
            message=prompt,
            documents=docs,
            model='command',
            preamble=preamble_prompt,

        )

    print(llm_response)
    return llm_response.text


def initiailize_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():

    initiailize_state()
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("USER").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "USER", "message": prompt})
        # print(st.session_state.messages)

        llm_reponse = cohereReply(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_reponse)
        st.session_state.messages.append(
            {"role": "assistant", "message": llm_reponse})




if __name__ == "__main__":
    main()
