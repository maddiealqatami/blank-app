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
    template="Write a story in the {genre} genre with dialogue and imagery in the style of the following books and/or authors: {style}. The story should revolve around the theme of '{theme}' and include the following characters: {characters}."
)
chain = LLMChain(llm=openai, prompt=prompt_template)

# User Inputs for Story
st.header("Story Parameters")
genre = st.text_input("Enter the genre (e.g., fantasy, sci-fi, romance):")
theme = st.text_input("Enter the theme (e.g., friendship, adventure, love):")
style = st.text_input("Enter books or authors the story should be written in the style of:")
characters = st.text_area("List the characters (e.g., Jack, a brave knight; Luna, a wise sorceress):")

# Placeholder for the story
story = ""
story_holder = st.empty()

# Generate or Regenerate Story
if st.button("Create Story"):
    if not genre or not theme or not characters or not style:
        st.error("Please fill in all the fields to create a story.")
    else:
        with st.spinner("Generating your story..."):
            try:
                story = chain.run({
                    "genre": genre,
                    "theme": theme,
                    "characters": characters,
                    "style": style
                })
                st.success("Your story is ready!")
                story_holder.text_area("Generated Story", value=story, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Options to Regenerate or Edit Inputs
if story:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate Story"):
            with st.spinner("Regenerating your story..."):
                try:
                    story = chain.run({
                        "genre": genre,
                        "theme": theme,
                        "characters": characters,
                        "style": style
                    })
                    story_holder.text_area("Generated Story", value=story, height=400)
                    st.success("Your story has been regenerated!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    with col2:
        if st.button("Edit Inputs and Regenerate"):
            st.info("You can edit the inputs above and click 'Create Story' again to regenerate.")

# Footer
st.markdown("---")
st.write("Powered by [LangChain](https://langchain.readthedocs.io/en/latest/) and OpenAI's GPT-3.5.")
