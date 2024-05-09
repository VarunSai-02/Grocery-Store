import pyttsx3
import sys

# Initialize pyttsx3 interface
tempt = pyttsx3.init()

# Dictionary of available products and their rates in rupees
products_rates = {
    "apple": 35,      # ₹35
    "banana": 20,     # ₹20
    "orange": 25      # ₹25
}

# Function to speak and print text
def speak_and_print(text):
    print(text)
    tempt.say(text)
    tempt.runAndWait()

# Function to get user's budget
def get_budget(welcome_message=True):
    if welcome_message:
        speak_and_print("Welcome to the Grocery Store! What is your shopping budget in rupees?")
    while True:
        try:
            speak_and_print("Enter your budget:")
            budget = float(input("₹"))
            return budget
        except ValueError:
            speak_and_print("Please enter a valid number for your budget.")

# Function to ask for user input with validation
def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input == 'yes' or user_input == 'no':
            return user_input
        else:
            speak_and_print("Please enter 'yes' or 'no'.")

# Function to handle when the current budget is insufficient for available items
def handle_insufficient_budget(budget):
    speak_and_print("Sorry, there are no items within your budget.")
    # Prompt to increase budget
    speak_and_print("Would you like to increase your budget? (yes/no): ")
    increase_budget = get_yes_no_input("")
    if increase_budget == "yes":
        new_budget = get_budget(welcome_message=False)  # Get a new budget without showing welcome message
        show_available_items(new_budget)  # Show available items with the new budget
        make_purchase(new_budget)  # Proceed to make a purchase with the new budget
    else:
        speak_and_print("Thank you for visiting. Goodbye!")
        sys.exit()  # Terminate the program

# Function to show available grocery items within the budget
def show_available_items(budget):
    available_items = [(product.capitalize(), rate) for product, rate in products_rates.items() if rate <= budget]
    if available_items:
        text = "Available grocery items within your budget:\n"
        for item, price in available_items:
            text += f"{item}: ₹{price:.2f}\n"
        speak_and_print(text)
        make_purchase(budget)  # Proceed to make a purchase with the current budget
    else:
        handle_insufficient_budget(budget)

# Function to make a purchase
def make_purchase(budget):
    purchased_products = {}
    total_cost = 0.0
    remaining_budget = budget

    while remaining_budget > 0 and len(purchased_products) < len(products_rates):
        try:
            speak_and_print("What would you like to purchase? Enter the product name or 'finish' to complete your purchase.")
            product = input("Product: ").lower()

            if product == "finish":
                if total_cost > budget:
                    raise ValueError("Total cost exceeds the budget!")
                break
                
            if product in products_rates:
                product_cost = products_rates[product]
                speak_and_print(f"How many {product}s would you like?")
                quantity = int(input(f""))
                
                if product_cost * quantity <= remaining_budget:
                    if product in purchased_products:
                        purchased_products[product] += quantity  # Update quantity if the product is already in the cart
                    else:
                        purchased_products[product] = quantity
                    total_cost += product_cost * quantity
                    remaining_budget -= product_cost * quantity
                    text = f"You added {quantity} {product}(s) to your cart for ₹{product_cost * quantity:.2f}. Remaining budget: ₹{remaining_budget:.2f}"
                    speak_and_print(text)
                else:
                    speak_and_print("Sorry, your budget is not sufficient for this quantity.")
            else:
                speak_and_print(f"Sorry, we don't have {product}.")

            speak_and_print("Would you like to add more items, cancel an item, or finish?")
            action = input("Add more items, cancel an item, or finish? (add/cancel/finish): ").lower()
            if action == "cancel":
                speak_and_print("Which item would you like to cancel?")
                cancel_product = input("Product to cancel: ").lower()
                if cancel_product in purchased_products:
                    cancel_quantity = int((input(f"How many {cancel_product}s would you like to cancel?")))
                    if cancel_quantity >= purchased_products[cancel_product]:
                        total_cost -= products_rates[cancel_product] * purchased_products[cancel_product]
                        remaining_budget += products_rates[cancel_product] * purchased_products[cancel_product]
                        del purchased_products[cancel_product]
                        speak_and_print(f"{cancel_quantity} {cancel_product}(s) removed from your cart.")
                    else:
                        total_cost -= products_rates[cancel_product] * cancel_quantity
                        remaining_budget += products_rates[cancel_product] * cancel_quantity
                        purchased_products[cancel_product] -= cancel_quantity
                        speak_and_print(f"{cancel_quantity} {cancel_product}(s) removed from your cart.")
                else:
                    speak_and_print("The selected item is not in your cart.")
            elif action == "finish":
                if total_cost > budget:
                    raise ValueError("Total cost exceeds the budget!")
                break

        except ValueError as e:
            speak_and_print(str(e))

    speak_and_print("Here is your purchase summary:")
    for product, quantity in purchased_products.items():
        text = f"{quantity} {product.capitalize()}"
        speak_and_print(text)

    text = f"Total Cost: ₹{total_cost:.2f}"
    speak_and_print(text)
    text = f"Remaining Budget: ₹{remaining_budget:.2f}"
    speak_and_print(text)
    speak_and_print("Thank you for shopping with us!")
    sys.exit()  # Terminate the program

# Main part of the code
budget = get_budget()

# Show available grocery items within the budget
show_available_items(budget)
