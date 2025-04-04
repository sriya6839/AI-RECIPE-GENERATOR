import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetRecipe(Action):
    def name(self) -> Text:
        return "action_get_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        recipe_name = tracker.get_slot("recipe_name")

        if not recipe_name:
            dispatcher.utter_message(text="Please tell me the name of the recipe you want.")
            return []

        try:
            with open("recipes.json", "r", encoding="utf-8") as f:
                recipes = json.load(f)

            recipe = next((r for r in recipes if r["name"].lower() == recipe_name.lower()), None)

            if recipe:
                response = f"📖 *{recipe['name']}*\n\n"
                response += "📝 *Ingredients:*\n"
                for item in recipe["Ingredients"]:
                    response += f"- {item}\n"
                response += "\n👨‍🍳 *Method:*\n"
                for i, step in enumerate(recipe["METHOD"], 1):
                    response += f"{i}. {step}\n"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the recipe for '{recipe_name}'.")
        except Exception as e:
            dispatcher.utter_message(text=f"⚠️ Error reading recipe data: {e}")

        return []
