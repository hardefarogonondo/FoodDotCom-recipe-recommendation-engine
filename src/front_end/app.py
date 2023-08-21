import streamlit as st


def get_user_rated_recipes(user_id):
    return ["Recipe A", "Recipe B", "Recipe C", "Recipe D", "Recipe E", "Recipe F", "Recipe G", "Recipe H", "Recipe I", "Recipe J", "Recipe K", "Recipe L"]


def get_recommendations_for_user(user_id):
    return ["Recipe X", "Recipe Y", "Recipe Z", "Recipe P", "Recipe Q", "Recipe R", "Recipe S", "Recipe T", "Recipe U", "Recipe V", "Recipe W"]


def main():
    st.title("Food.com Recipe Recommendation Engine")
    st.write("Find the best recipes tailored for you based on your past preferences!")
    user_id = st.selectbox("Select User ID", [1, 2, 3, 4, 5])
    if st.button("Submit"):
        col1, col2 = st.columns(2)
        col1.subheader(f"Recipes Rated by User {user_id}")
        user_recipes = get_user_rated_recipes(user_id)
        scrollable_rated_recipes = '<div style="height: 250px; overflow-y: auto;">'
        for recipe in user_recipes:
            scrollable_rated_recipes += f"<p>{recipe}</p>"
        scrollable_rated_recipes += "</div>"
        col1.write(scrollable_rated_recipes, unsafe_allow_html=True)
        col2.subheader(f"Recommended Recipes for User {user_id}")
        recommended_recipes = get_recommendations_for_user(user_id)
        scrollable_recommended_recipes = '<div style="height: 250px; overflow-y: auto;">'
        for recipe in recommended_recipes:
            scrollable_recommended_recipes += f"<p>{recipe}</p>"
        scrollable_recommended_recipes += "</div>"
        col2.write(scrollable_recommended_recipes, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
