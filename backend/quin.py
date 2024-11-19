# main.py
import json
import os
from openai import OpenAI
client = OpenAI()

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

def load_store_string_data(file_path):
    path = os.getcwd() + "/backend/Stores/" + file_path
    with open(path, 'r', encoding="utf8") as f:
        data = f.read()
        print(data)
    return data

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

def getStoreRecommendations(food_item, restaurant_data):
    '''This takes in a food item and filtered restaurant data (data must be filtered with parse_store_data()) and outputs a string
    of listed stores and potential menu items that match the user input '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that matches food items to restaurant menus."},
            {"role": "user", "content": f"Here is the restaurant data: {restaurant_data}. "
             f"A user wants '{food_item}'. Find restaurants offering similar items and list them as:\n"
             "1. {Restaurant Name (follows after \"name:\" in the string up until the \"address:\" field)}: {List of similar food items (follow after \"menu:[\" and are separated by commas until \"]\" is reached)}\n\n"
             "2. Same thing as 1 but for a new restaurant if applicable"
             "Keep listing off restaurants if they have some food items that correspond with the users request"
             "If nothing is similar, return 'No available food items similar to {food_item}'."}
        ]
    )
    return response.choices[0].message.content


def main():
    # Load available store files
    store_files = list_store_files()
    
    # Lists all of the store choices in /Stores for now
    store_choices = "\n".join([f"{i+1}. {store_files[i]}" for i in range(len(store_files))])
    print(store_choices)
    
    # Ask user to select a store file (choose 2 because this contains all the info)
    store_index = int(input(f"Please select a store (1-{len(store_files)}): ")) - 1
    selected_store_file = store_files[store_index]
    
    # Load and filter the store data
    store_data = load_store_data(selected_store_file)
    filtered_store_data = parse_store_data(store_data)
    
    # Prompt the user for what food type they are ordering and pass it into the chat function along with filtered store data
    foodType = input("Welcome to the ordering system! What type of food are you in the mood for? \n")
    store_choices = getStoreRecommendations(foodType, restaurant_data=filtered_store_data)
    print(store_choices)
    
    
    # print(f"You've selected: {store_data['store']['provider_type']}")
    
    # # Initialize order variables
    # order = {
    #     "store_reference": store_data["reference"],
    #     "delivery_address": "",
    #     "delivery_phone": "",
    #     "dropoff_instructions": "",
    #     "items": []
    # }
    
    # # Ask user for delivery details
    # order['delivery_address'] = input("Enter your delivery address: ")
    # order['delivery_phone'] = input("Enter your delivery phone number: ")
    # order['dropoff_instructions'] = input("Enter any special dropoff instructions: ")

    # # Generate menu options and let user pick items
    # menu_prompt = f"The menu for {store_data['store']['provider_type']} is: \n"
    # for category in store_data['menu']['categories']:
    #     menu_prompt += f"\n{category['name']}:\n"
    #     for item in category['items']:
    #         menu_prompt += f"- {item['name']}: {item['description']}\n"
    
    # menu_prompt += "\nPlease specify what you'd like to order (e.g., 'I want a Burrito Scram-Bowl and Cherry bubly')."
    
    # user_input = input("What would you like to order? ")
    # print(menu_prompt)
    
    
    
    
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
