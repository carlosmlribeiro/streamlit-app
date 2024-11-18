import streamlit as st
from langchain_community.llms import OpenAI
#from openinference.instrumentation.openai import OpenAIInstrumentor
#from phoenix.otel import register
from lida import Manager, TextGenerationConfig , llm

text_gen = llm("openai") # for openai

#tracer_provider = register(
#  project_name="lida-chatbot",
#  endpoint="https://app.phoenix.arize.com/v1/traces"
#)
#OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

st.title("LIDA framework example")

#openai_api_key = st.sidebar.text_input("openai API key", type="password")
csv_data = st.sidebar.text_input("Path to Data", type="default")
persona = st.sidebar.text_input("Persona", type="default")

openai_api_key = st.secrets["OPENAI_API_KEY"]

lida = Manager(text_gen = llm("openai", api_key=openai_api_key))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o-mini", use_cache=True)

if st.button("Generate goals") and csv_data.startswith("http"):
    summary = lida.summarize(csv_data, summary_method="default", textgen_config=textgen_config)
    if persona:
        goals = lida.goals(summary, n=2, persona=persona, textgen_config=textgen_config)
    else:
        goals = lida.goals(summary, n=2, persona=persona, textgen_config=textgen_config)

    # Convert the string to a Python list
    goal_questions = [goal.question for goal in goals]
    goal_viz = [goal.visualization for goal in goals]

    selected_goal = st.selectbox('Pick a goal', 
                                 options=goal_questions, 
                                 index=None,
                                 placeholder="Select a goal...",)

    if selected_goal:
        selected_goal_index = goal_questions.index(selected_goal)
        st.write(selected_goal)
        st.button("generate viz")