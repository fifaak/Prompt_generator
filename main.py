import streamlit as st
from openai import OpenAI
import google.generativeai as genai

Task = st.text_input("Task")

Persona = st.text_input("Persona")

Aim = st.text_input("Aim")

Recipients = st.text_input("Recipients")

Theme = st.text_input("Theme")

Structure = st.text_input("Structure")

Chain_of_Thought = st.text_input("Chain of Thought")

Few_shot = st.text_input("Few_shot")

def create_opentyphoon_client():
    API_KEY='KEY'
    return OpenAI(
        api_key=API_KEY,
        base_url="https://api.opentyphoon.ai/v1",
    )
    
def call_typhoon(user_input="", Task=Task, Persona=Persona, Aim=Aim, Recipients=Recipients, Theme=Theme, Structure=Structure, Chain_of_Thought=Chain_of_Thought, Few_shot=Few_shot):
    client = create_opentyphoon_client()

    stream = client.chat.completions.create(
    model="typhoon-instruct",
    messages=[
    {
            "role": "systemp",
            "content": f'คุณมีหน้าที่สรุป prompt ให้เข้าใจง่าย',
        },
        {
            "role": "user",
            "content": f"""
            <Task>
            {Task}
            
            <Persona>
            {Persona}
            
            <Aim>
            {Aim}
            
            <Recipients>
            {Recipients}
            
            <Theme>
            {Theme}
            
            <Structure>
            {Structure}
            
            ***
            <Chain of Thought>
            {Chain_of_Thought}
            
            <Example>
            {Few_shot}
            """
            
        }
    ],

    max_tokens=300,
    temperature=0,
    top_p=0.99,
    stream=True,
    )

    respond=[]
    for chunk in stream:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                if choice.delta.content is not None:
                    respond.append(choice.delta.content)
    return "".join(respond)

def call_google(user_input="", Task=Task, Persona=Persona, Aim=Aim, Recipients=Recipients, Theme=Theme, Structure=Structure, Chain_of_Thought=Chain_of_Thought, Few_shot=Few_shot):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    genai.configure(api_key='KEY')
    response = model.generate_content(f"""
            คุณมีหน้าที่สรุป prompt ให้เข้าใจง่าย
            
            <Task>
            {Task}
            
            <Persona>
            {Persona}
            
            <Aim>
            {Aim}
            
            <Recipients>
            {Recipients}
            
            <Theme>
            {Theme}
            
            <Structure>
            {Structure}
            
            ***
            <Chain of Thought>
            {Chain_of_Thought}
            
            <Example>
            {Few_shot}
            """)
    return response.text
    

check_gemini =st.checkbox("gemini")
check_typhoon = st.checkbox("typhoon")

submit = st.button("submit")
with st.spinner("Loading..."):
    if check_gemini and submit:
        st.write(call_typhoon())
    if check_typhoon and submit:
        st.write(call_google())
    