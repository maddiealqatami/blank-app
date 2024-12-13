import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Initialize Streamlit app
st.title("Block Blaster")
st.write("Spur inspiration and overcome writer's block with the help of AI.")

# User API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API Key to proceed.")
    st.stop()

# Temperature Slider
temperature = st.slider("Adjust creativity (temperature):", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# **Story Length Slider**
story_length = st.slider("Story Length (number of words):", min_value=100, max_value=5000, value=1000, step=100)

# LLM Setup
openai = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=temperature)
prompt_template = PromptTemplate(
    input_variables=["genre", "theme", "characters", "style", "story_length"],
    template="You are an award-winning novelist. Write a story with dialogue and imagery in the {genre} genre. The story should revolve around the theme of '{theme}' without explicitly stating the theme. The story should include the following characters: {characters}, and match the style of {style} in tone and word choice. Use literary devices to show, not tell the story. The story should be approximately {story_length} words long."
)
chain = LLMChain(llm=openai, prompt=prompt_template)

# User Inputs for Story
st.header("Story Parameters")
genre = st.text_input("Enter the genre (e.g., fantasy, sci-fi, romance):")
theme = st.text_input("Enter the theme (e.g., friendship, adventure, love):")
characters = st.text_area("List the characters (e.g., Jack, a brave knight; Luna, a wise sorceress):")
style = st.text_area("Enter authors and/or books to use for style inspiration (e.g., J.K. Rowling, The Hobbit):")

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
                    "style": style,
                    "story_length": story_length
                })
                st.success("Your story is ready!")
                story_holder.text_area("Generated Story", value=story, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Save and Download Story
if story:
    st.download_button("Download as Text", story, "short_story.txt")


# Footer
st.markdown("---")
st.write("Powered by [LangChain](https://langchain.readthedocs.io/en/latest/) and OpenAI's GPT-3.5.")
