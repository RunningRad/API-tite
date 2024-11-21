# main.py
import json
import os
from openai import OpenAI
import json
client = OpenAI()

def load_store_string_data(file_path):
    path = os.getcwd() + "/Stores/" + file_path
    with open(path, 'r', encoding="utf8") as f:
        data = f.read()
        print(data)
    return data
    
def load_store_data(file_path):
    """Loads store JSON data from a given file path."""
    # For convience purposes, I have my path slightly changed.
    path = os.getcwd() + "/Stores/" + file_path
    with open(path, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

def parse_store_data(data):
    # Takes the json data and parses out the resturant name, address, and menu
    res = ''
    if isinstance(data,list):
        print('list')
        res += '['                          # start resturant list
        for resturant in data:
            res += 'name:'
            res += resturant['name']
            res += ', address:'
            res += resturant['address']
            res += ', menu:['
            for item in resturant['dishes']:
                res += item + ', '
            res = res[:-2]
            res += ']; '                     # delimit resturants in list
        
        res += ']'                          # end resturant list
    else: 
        res += '['                          # start resturant list
        res += 'name:'
        res += data['store']['provider_type']
        res += ', address:'
        res += data['store']['address']
        res += ', menu:['
        for cat in data['menu']['categories']:
            for item in cat['items']:
                res += item['name'] + ', '
        res = res[:-2]
        res += ']]'                          # end resturant list
    return res

def list_store_files():
    """Lists available store JSON files in the current directory."""
    print(os.getcwd())
    path = os.getcwd() + "/Stores/"
    # return [f for f in os.listdir(path) if f.endswith('.json')], [load_store_string_data(f) for f in os.listdir(path) if f.endswith('.json')]
    return [f for f in os.listdir(path) if f.endswith('.json')], [parse_store_data(load_store_data(f)) for f in os.listdir(path) if f.endswith('.json')]
    

def chat_with_gpt(prompt):
    """Sends a prompt to the ChatGPT API and returns the response."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def getStoreRecommendations(prompt, store_files):
    """Sends a prompt to the ChatGPT API and returns the stores that have the food closest to what the user wants"""
    final_prompt = prompt + """
    . The user has requested this food as one they want to eat.

    This consists of all of the possible restaurants they can order from, with each restaurant name being labeled as "name" alongside the address as "address" 
    and all food items in "menu".

    Use the provided food that the customer wants, and scan all of the menus. Make sure that a food item that either directly matches, or is mostly the same, is 
    the food item the customer wants.
    
    Please give a list of possible restaurants that the user would want to eat from the restaurants provided.
    Do NOT under any circumstances make up any new restaurants that do not exist within the file. Also please provide the address and full menu of the restaurant. 
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # Edit to get a list of stores based off of what food the customer wants, and the type of food that the stores have.
            {"role": "system", "content": "You are a helpful assistant. Give a list of the stores that contain food closest to what the user wants."},
            {"role": "system", "content": "There is a list of restaurants provided in this string:  ```{store_files}```. Please use this to help determine the food the customer wants."},
            {"role": "user", "content": final_prompt}
        ]   
    )
    print(completion.choices[0].message.content)

def main():
    # Load available store files
    store_files, store_files_data = list_store_files()

    print(store_files_data)
    # Lists all of the store choices in /Stores for now
    store_choices = "\n".join([f"{i+1}. {store_files[i]}" for i in range(len(store_files))])
    
    print(store_files)

    print("Welcome to the ordering system! What type of food are you in the mood for?")
    store_choices = getStoreRecommendations(input(), store_files_data)
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
