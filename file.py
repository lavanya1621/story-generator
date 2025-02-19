from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Set your OpenAI API key
client = OpenAI(
    api_key=st.secrets["openai"]["OPENAI_API_KEY"]
)


# Function to generate the story using the updated API interface
def generate_story(genre, character_trait, setting, tone):
    # Construct the personalized prompt template using user inputs
    prompt = f"""
    You are a masterful storyteller, known for creating vivid worlds and compelling characters. Your task is to write a {genre} story that draws the reader into a world that gives MAJOR VIBES OF {setting}.
    The main character in this story has this {character_trait}, and this personality should guide their actions and decisions throughout the narrative. 
    The tone of the story is {tone}, and it should resonate throughout, from the opening to the closing scene. 
    Be sure to use highly descriptive language to bring the setting and characters to life, making the reader feel as if they are part of the story. 
    Begin the story by introducing the character and setting in a way that immediately captures the reader's attention.
    Consider how the character's {character_trait} trait influences the world around them and the decisions they make. 
    Allow the {tone} atmosphere to influence the progression of the plot—whether it's tension, warmth, or humor. Make every detail count.
    """
    
    try:
        # Use the new `openai.ChatCompletion` interface
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a master storyteller with an exceptional ability to capture the reader's attention."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Access the generated story
        story = response.choices[0].message.content.strip()
        return story
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
def main():
    st.title("Story Generator")
    st.markdown("### Create your own personalized story!")

    # User input for genre, character trait, setting, and tone
    genre = st.selectbox("Choose the genre:", ["Fantasy", "Sci-Fi", "Thriller", "Romance", "Horror", "Adventure"])
    character_trait = st.selectbox("Choose the main character trait:", ["Brave", "Shy", "Witty", "Intelligent", "Mysterious", "Reckless"])
    setting = st.text_input("Enter the setting:", "A kingdom of eternal night")
    tone = st.selectbox("Choose the tone of the story:", ["Suspenseful", "Light-hearted", "Dark and eerie", "Romantic", "Action-packed", "Emotional"])

    # Button to generate the story
    if st.button("Generate Story"):
        if genre and character_trait and setting and tone:
            with st.spinner('Generating your story...'):
                # Generate the story using OpenAI's model
                story = generate_story(genre, character_trait, setting, tone)
                if story:
                    st.subheader("Your Story:")
                    st.write(story)
                else:
                    st.error("An error occurred while generating the story.")
        else:
            st.error("Please fill in all the fields to generate the story.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
