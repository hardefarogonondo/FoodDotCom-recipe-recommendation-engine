# Import Libraries
import requests
import streamlit as st


def get_available_users():
    response = requests.get('http://backend:8000/available_users')
    if response.status_code == 200:
        return response.json()["user_ids"]
    else:
        return []


def get_user_data(user_id):
    response = requests.get(f'http://backend:8000/recommend/{user_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error": "Error fetching data."}


def main():
    st.title("Food.com Recipe Recommendation Engine")
    st.write("Find the best recipes tailored for you based on your past preferences!")
    available_users = get_available_users()
    if not available_users:
        st.write("No available users.")
        return
    user_id = st.selectbox("Select User ID", available_users)
    if st.button("Submit"):
        user_data = get_user_data(user_id)
        if "Error" in user_data:
            st.write("Error fetching data from the server.")
            return
        col1, col2 = st.columns(2)
        col1.subheader(f"Recipes Rated by User {user_id}")
        past_rated_recipes = user_data.get("past_rated_recipes", [])
        scrollable_rated_recipes = '<div style="height: 250px; overflow-y: auto;">'
        for recipe in past_rated_recipes:
            scrollable_rated_recipes += f"<p>{recipe}</p>"
        scrollable_rated_recipes += "</div>"
        col1.write(scrollable_rated_recipes, unsafe_allow_html=True)
        col2.subheader(f"Recommended Recipes for User {user_id}")
        recommended_recipes = user_data.get("recommended_recipes", [])
        scrollable_recommended_recipes = '<div style="height: 250px; overflow-y: auto;">'
        for recipe in recommended_recipes:
            scrollable_recommended_recipes += f"<p>{recipe}</p>"
        scrollable_recommended_recipes += "</div>"
        col2.write(scrollable_recommended_recipes, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
