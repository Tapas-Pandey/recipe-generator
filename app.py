import streamlit as st
import requests
import os
API_KEY = os.getenv("SPOONACULAR_API_KEY")

def search_recipes_by_ingredients(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'ingredients': ingredients,
        'number': 5,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    try:
        data = response.json()
        return data if isinstance(data, list) else []
    except ValueError:
        return []

def search_recipes_by_name(name):
    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'query': name,
        'number': 5,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    try:
        data = response.json()
        return data.get('results', [])
    except ValueError:
        return []

def get_recipe_info(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {'apiKey': API_KEY}
    response = requests.get(url, params=params)
    try:
        return response.json()
    except ValueError:
        return {}

st.title("🍽️ Recipe Explorer")
search_type = st.radio("Search by:", ["Ingredients", "Recipe Name"])

if "recipes" not in st.session_state:
    st.session_state.recipes = []
if "index" not in st.session_state:
    st.session_state.index = 0



if search_type == "Ingredients":
    user_input = st.text_input("Enter ingredients (comma-separated):")
else:
    user_input = st.text_input("Enter recipe name:")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔍 Search"):
        if user_input.strip():
            with st.spinner("Searching..."):
                if search_type == "Ingredients":
                    st.session_state.recipes = search_recipes_by_ingredients(user_input)
                else:
                    st.session_state.recipes = search_recipes_by_name(user_input)
                st.session_state.index = 0
        else:
            st.warning("Please enter a search term.")


if st.session_state.recipes:
    current = st.session_state.recipes[st.session_state.index]
    recipe_id = current.get("id")
    full_info = get_recipe_info(recipe_id)

    if full_info:
        st.subheader(full_info.get("title", "No title"))
        st.image(full_info.get("image", ""))

        st.markdown(f"**Ready in:** {full_info.get('readyInMinutes', '?')} minutes")
        st.markdown(f"**Servings:** {full_info.get('servings', '?')}")

        st.markdown("### 📝 Ingredients:")
        for ingredient in full_info.get("extendedIngredients", []):
            st.write(f"- {ingredient.get('original', '')}")

        st.markdown("### 🍳 Instructions:")
        instructions = full_info.get("instructions")
        if instructions:
            st.markdown(instructions, unsafe_allow_html=True)
        else:
            st.write("No instructions available.")


    nav_col1, nav_col2 = st.columns([1, 1])
    with nav_col1:
        if st.session_state.index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.index -= 1
    with nav_col2:
        if st.session_state.index < len(st.session_state.recipes) - 1:
            if st.button("Next ➡️"):
                st.session_state.index += 1
        else:
            st.info("You've reached the last recipe.")
