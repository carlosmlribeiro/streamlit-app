import streamlit as st
from langchain_community.llms import OpenAI
#from openinference.instrumentation.openai import OpenAIInstrumentor
#from phoenix.otel import register
from lida import Manager, TextGenerationConfig , llm
from PIL import Image
import io
import base64

text_gen = llm("openai") # for openai

#tracer_provider = register(
#  project_name="lida-chatbot",
#  endpoint="https://app.phoenix.arize.com/v1/traces"
#)
#OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

st.title("LIDA framework example")

openai_api_key = st.sidebar.text_input("openai API key", type="password")
csv_data = st.sidebar.text_input("Path to Data", type="default")
persona = st.sidebar.text_input("Persona", type="default")

#openai_api_key = st.secrets["OPENAI_API_KEY"]

lida = Manager(text_gen = llm("openai", api_key=openai_api_key))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o-mini", use_cache=True)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def generate_goals():
    st.session_state.clicked = True

def reset():
    st.session_state.clicked = False


if csv_data.startswith("http"):

    if openai_api_key:
        st.button('Start', on_click=generate_goals)
    st.button('Reset', on_click=reset, type="primary")

    if st.session_state.clicked:
        summary = lida.summarize(csv_data, summary_method="default", textgen_config=textgen_config)
        if persona:
            goals = lida.goals(summary, n=4, persona=persona, textgen_config=textgen_config)
        else:
            goals = lida.goals(summary, n=4, textgen_config=textgen_config)

        # Convert the string to a Python list
        goal_questions = [goal.question for goal in goals]
        goal_viz = [goal.visualization for goal in goals]

        if goals:
            selected_goal = st.selectbox('Choose a visualisation', 
                                        options=goal_questions, 
                                        index=None,
                                        placeholder="Select a goal...",)

        if selected_goal:
            selected_goal_index = goal_questions.index(selected_goal)

            textgen_config = TextGenerationConfig(n=1, temperature=0,  model="gpt-4o", use_cache=False)

            visualizations = lida.visualize(
                summary=summary,
                goal=goals[selected_goal_index],
                textgen_config=textgen_config,
                library="seaborn")

            if visualizations:
                chart = visualizations[0]
            
                if chart.raster:

                    imgdata = base64.b64decode(chart.raster)
                    img = Image.open(io.BytesIO(imgdata))
                    st.image(img, caption="visualisation", use_column_width=True)
            
