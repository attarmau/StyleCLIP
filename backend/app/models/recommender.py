# recommender.py

from typing import List
from backend.app.controllers.clothing_controller import get_clothing_items_by_style

def generate_recommendations(style: str, user_behavior: List[str]) -> List[str]:
    """
    Generate clothing recommendations based on the given style and user behavior.
    
    :param style: The clothing style the user prefers
    :param user_behavior: A list of items the user has previously interacted with
    :return: A list of recommended clothing items
    """
    
    # Example: If the style is available in the database or in the controller, fetch matching items
    # Note: might use a more complex recommendation algorithm here later
  
    recommended_items = get_clothing_items_by_style(style)
    
    # Filter or adjust the recommendations based on user behavior
    # This could be using a collaborative filtering approach or item-based filtering
    filtered_items = [item for item in recommended_items if item in user_behavior]
    
    return filtered_items
