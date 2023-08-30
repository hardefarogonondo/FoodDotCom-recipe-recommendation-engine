# Import Libraries
from fastapi import FastAPI
import pandas as pd
import pickle

# Initialization
train_df = pd.read_pickle('/app/data/processed/train.pkl')
test_df = pd.read_pickle('/app/data/processed/test.pkl')
combined_df = pd.concat([train_df, test_df], ignore_index=True)
with open('/app/data/processed/train_sparse_matrix.pkl', 'rb') as file:
    train_matrix = pickle.load(file)
with open('/app/data/processed/user_mapping.pkl', 'rb') as file:
    user_mapping = pickle.load(file)
with open('/app/data/processed/recipe_mapping.pkl', 'rb') as file:
    recipe_mapping = pickle.load(file)
with open('/app/models/best_model.pkl', 'rb') as file:
    knn_model = pickle.load(file)
app = FastAPI()


def get_past_rated_recipes(user_id: int, train_df):
    user_data = train_df[train_df["user_id"] == user_id]
    merged_data = user_data.merge(combined_df, on="recipe_id")
    past_rated_recipes = merged_data["name_x"].tolist()
    unique_past_rated_recipes = list(set(past_rated_recipes))
    return unique_past_rated_recipes


def recommend_recipes(user_id: int):
    try:
        user_index = user_mapping[user_id]
    except KeyError:
        return {"Error": "User ID not found in the mapping."}
    distances, indices = knn_model.kneighbors(
        train_matrix[user_index], n_neighbors=30)
    recommended_recipe_indices = indices.squeeze().tolist()[1:]
    recommended_recipe_ids = []
    unique_recipe_ids = set()
    for index in recommended_recipe_indices:
        recipe_id = [recipe for recipe,
                     idx in recipe_mapping.items() if idx == index][0]
        if recipe_id not in unique_recipe_ids:
            unique_recipe_ids.add(recipe_id)
            recommended_recipe_ids.append(recipe_id)
    recommended_recipes = combined_df[combined_df["recipe_id"].isin(
        recommended_recipe_ids)]["name"].tolist()
    unique_recommended_recipes = list(
        set(recommended_recipes))
    return unique_recommended_recipes


@app.get("/available_users")
def get_available_users():
    available_users = combined_df["user_id"].unique().tolist()
    return {"user_ids": available_users}


@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    past_rated_recipes = get_past_rated_recipes(user_id, combined_df)
    recommended_recipes = recommend_recipes(user_id)
    if "Error" in recommended_recipes:
        return recommended_recipes
    return {
        "recommended_recipes": recommended_recipes,
        "past_rated_recipes": past_rated_recipes
    }
