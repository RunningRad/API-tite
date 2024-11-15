# main.py
import json
import os
from openai import OpenAI
client = OpenAI()

def load_store_data(file_path):
    """Loads store JSON data from a given file path."""
    path = os.getcwd() + "/backend/Stores/" + file_path
    with open(path, 'r') as f:
        data = json.load(f)
    return data
def list_store_files():
    """Lists available store JSON files in the current directory."""
    path = os.getcwd() + "/backend/Stores"
    return [f for f in os.listdir(path) if f.endswith('.json')]

def chat_with_gpt(prompt):
    """Sends a prompt to the ChatGPT API and returns the response."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def getStoreRecommendations(prompt):
    """Sends a prompt to the ChatGPT API and returns the stores that have the food closest to what the user wants"""
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # Edit to get a list of stores based off of what food the customer wants, and the type of food that the stores have.
            {"role": "system", "content": "You are a helpful assistant. Give a list of the stores that contain food closest to what the user wants."},
            {"role": "user", "content": prompt}
        ]   
    )
    print(completion.__dict__)

def main():
    # Load available store files
    store_files = list_store_files()
    # Lists all of the store choices in /Stores for now
    store_choices = "\n".join([f"{i+1}. {store_files[i]}" for i in range(len(store_files))])
    
    print("Welcome to the ordering system! What type of food are you in the mood for?")
    # store_choices = getStoreRecommendations(input())
    print(store_choices)
    
    # Ask user to select a store
    store_index = int(input(f"Please select a store (1-{len(store_files)}): ")) - 1
    selected_store_file = store_files[store_index]
    store_data = load_store_data(selected_store_file)
    
    print(f"You've selected: {store_data['store']['provider_type']}")
    
    # Initialize order variables
    order = {
        "store_reference": store_data["reference"],
        "delivery_address": "",
        "delivery_phone": "",
        "dropoff_instructions": "",
        "items": []
    }
    
    # Ask user for delivery details
    order['delivery_address'] = input("Enter your delivery address: ")
    order['delivery_phone'] = input("Enter your delivery phone number: ")
    order['dropoff_instructions'] = input("Enter any special dropoff instructions: ")

    # Generate menu options and let user pick items
    menu_prompt = f"The menu for {store_data['store']['provider_type']} is: \n"
    for category in store_data['menu']['categories']:
        menu_prompt += f"\n{category['name']}:\n"
        for item in category['items']:
            menu_prompt += f"- {item['name']}: {item['description']}\n"
    
    menu_prompt += "\nPlease specify what you'd like to order (e.g., 'I want a Burrito Scram-Bowl and Cherry bubly')."
    
    user_input = input("What would you like to order? ")
    print(menu_prompt)
    # chat_response = chat_with_gpt(menu_prompt + "\n\nUser input: " + user_input)
    
    # print("\nBased on your input, your order is:")
    # print(chat_response)
    
    # # Confirm and finalize the order
    # order['items'] = chat_response
    # print("\nFinal Order Summary:")
    # print(json.dumps(order, indent=2))

    # # Save or process the order further as needed.

if __name__ == "__main__":
    main()
