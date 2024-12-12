import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Initialize Streamlit app
st.title("AI-Powered Short Story Creator")
st.write("Create captivating short stories with the help of AI.")

# User API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API Key to proceed.")
    st.stop()

# LLM Setup
openai = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo")
prompt_template = PromptTemplate(
    input_variables=["genre", "theme", "characters"],
    template="Write a short story in the {genre} genre. The story should revolve around the theme of '{theme}' and include the following characters: {characters}."
)
chain = LLMChain(llm=openai, prompt=prompt_template)

# User Inputs for Story
st.header("Story Parameters")
genre = st.text_input("Enter the genre (e.g., fantasy, sci-fi, romance):")
theme = st.text_input("Enter the theme (e.g., friendship, adventure, love):")
characters = st.text_area("List the characters (e.g., Jack, a brave knight; Luna, a wise sorceress):")

# Generate Story
if st.button("Create Story"):
    if not genre or not theme or not characters:
        st.error("Please fill in all the fields to create a story.")
    else:
        with st.spinner("Generating your story..."):
            try:
                story = chain.run({
                    "genre": genre,
                    "theme": theme,
                    "characters": characters
                })
                st.success("Your story is ready!")
                st.text_area("Generated Story", value=story, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.write("Powered by [LangChain](https://langchain.readthedocs.io/en/latest/) and OpenAI's GPT-3.5.")
