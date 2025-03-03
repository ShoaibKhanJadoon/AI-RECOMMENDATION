
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import get_processed_data

data = get_processed_data()

def id_based_recommendations( item_id, top_n):
    global data
    train_data = data
    # Check if the item name exists in the training data
    if item_id not in train_data['id'].values:
        print(f"Item '{item_id}' not found in the training data.")
        return pd.DataFrame()

    # Create a TF-IDF vectorizer for item descriptions
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Apply TF-IDF vectorization to item descriptions
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['tags'])

    # Calculate cosine similarity between items based on descriptions
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Find the index of the item
    item_index = train_data[train_data['id'] == item_id].index[0]

    # Get the cosine similarity scores for the item
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # Sort similar items by similarity score in descending order
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # Get the top N most similar items (excluding the item itself)
    top_similar_items = similar_items[1:top_n+1]

    # Get the indices of the top similar items
    recommended_item_indices = [x[0] for x in top_similar_items]

    # Get the details of the top similar items
    recommended_items_details = train_data.iloc[recommended_item_indices]

    return recommended_items_details


def main_function_recommendation(item_ids):
    all_recommendations = pd.DataFrame()
    top_n=5
    for item_id in item_ids:
        recommendations = id_based_recommendations(item_id, top_n)
        all_recommendations = pd.concat([all_recommendations, recommendations])

    # Remove duplicates based on 'id'
    all_recommendations = all_recommendations.drop_duplicates(subset=['id']).reset_index(drop=True)

    # Exclude the item_ids from the final recommendations
    all_recommendations = all_recommendations[~all_recommendations['id'].isin(item_ids)].reset_index(drop=True)

    return all_recommendations

def keyword_search(query, top_n=20):
    global data
    df = data
    if df.empty:
        return pd.DataFrame()

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['tags'])

    query_vector = tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    similar_items = list(enumerate(cosine_similarities))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    top_similar_items = similar_items[:top_n]
    recommended_item_indices = [x[0] for x in top_similar_items]

    recommended_items = df.iloc[recommended_item_indices]

    return recommended_items

# # Example usage
# item_ids_list = ["8379a6c5-0a6d-4fb4-bc0b-918906301a37", "34b40420-c3a6-431d-821d-c4ad2f5b0869"]
# result = main_function(df, item_ids_list)
# print("result=",result)

# search_result = keyword_search(df, "white", top_n=20)
# print("search",search_result)