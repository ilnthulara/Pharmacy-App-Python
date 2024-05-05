# initializing dictionaries to store given customer and product details
customer_list = {
    'Kate': 20, 
    'Tom': 32}
        
product_list = {
    'vitaminC': {'price': 12.0,'prescription_required': False},
    'vitaminE': {'price': 14.5,'prescription_required': False},
    'coldTablet': {'price': 6.4,'prescription_required': False},
    'vaccine': {'price': 32.6,'prescription_required': True},
    'fragrance': {'price': 25.0,'prescription_required': False}
}

# initializing an empty dictionary to store order histroy
orders = {}

# purchasing a product
def make_purchase():
    # getting the customer name
    cus_name = input("Enter the name of the customer [e.g. Kate]: ")

    # getting the product name(s) from user
    pro_input = input("Enter the products [enter a valid products only, e.g. vitaminC, vitaminE](separate by commas): ")
    # converting string into list of strings
    pro_list = [p.strip() for p in pro_input.split(',')]

    # getting the quantities
    quantities = input("Enter the quantities (separate by commas): ")
    quantity_list = [int(q.strip()) for q in quantities.split(',')]

    #  checking if the number of entered products is equal to the number of entered quantities
    if len(pro_list) != len(quantity_list):
        print("ERROR!!!! Number of products and quantities should be similar!!!!")
        return

    total = 0
    # The dictionaries for each item on the customer's receipt are stored in this empty list
    receipt_items = []

    #  iterating over all items that the customer wants to buy
    for pro_name, quantity in zip(pro_list, quantity_list): #zip returns tuple so need to convert it back to a list
        if pro_name not in product_list:
            print(f"ERROR!!!! The product {pro_name} is not valid. Please enter a valid product!!!")
            return
        if quantity <= 0:
            print("ERROR!!!! Quantity must be a positive number!!!!")
            return 
        if product_list[pro_name]['prescription_required']:
            prescription_needed_true = input(f"Do you have a prescription for {pro_name}? (y/n): ").lower()
            while prescription_needed_true not in ['y', 'n']:
                print("The answer is not valid. Please enter 'y' or 'n'!!!!")
                prescription_needed_true = input(f"Do you have a prescription for {pro_name}? (y/n): ").lower()

            if prescription_needed_true == 'n':
                print(f"SORRY!!!! {pro_name} cannot be purchsed without a prescription!!!!!")
                continue
        
        price = product_list[pro_name]['price']
        item_cost = price * quantity
        total += item_cost
        reward_points = round(item_cost)
        customer_list[cus_name] = customer_list.get(cus_name, 0) + reward_points
        #  adding an entry to the receipt dictionary for every valid item
        receipt_items.append({'product_name': pro_name, 'quantity': quantity, 'price': price})

    # Deducting reward points if customer has more than 100
    if customer_list[cus_name] >= 100:
        discount = (customer_list[cus_name] // 100) * 10
        total -= discount
        customer_list[cus_name] -= discount

    # Add order to order history
    if cus_name in orders:
        orders[cus_name].append(receipt_items)
    else:
        orders[cus_name] = [receipt_items]

    # The Receipt
    print("==========================================================")
    print("Receipt")
    print("==========================================================")
    print(f"Name: \t\t\t\t{cus_name}")
    for item in receipt_items:
        print(f"Product: \t\t\t{item['product_name']}, \nQuantity: \t\t\t{item['quantity']}, \nUnit Price: \t\t\t{item['price']:.2f}")
    print("==========================================================")
    print(f"Total cost: \t\t\t{total} (AUD)")
    print(f"Earned reward: \t\t\t{round(total)}")
    print("==========================================================") 

#Adding or updating prodcut information 
def add_update_product():
    # getting information about the product
    pro_info = input("Enter the product information (name, price, dr_prescription)(separate by commas): ")
    # splits the input string into a list
    pro_info = [p.strip() for p in pro_info.split(',')]
    
    for product_info in pro_info:
        info = product_info.split(',')
        # checks the length of the information
        if len(info) != 3:
            print("Invalid format. Please enter in the format: name, price, dr_prescription (separate by commas)")
            return

        pro_name = info[0].strip()
        # removes the dollar sign, strips any spaces, and converts it to a floating-point number
        price = float(info[1].replace('$', '').strip())
        # Assuming 'No Prescription Required' means no prescription needed
        prescription_needed = info[2].strip().lower() == 'no'  

        product_list[pro_name] = {'price': price, 'prescription_required': prescription_needed}
        print(f"{pro_name} updated/added successfully.")

# display existing customers
def display_customers():
    print("\n=============================Existing Customers=============================")
    for customer, reward_points in customer_list.items():
        print(f"{customer}: {reward_points} reward points")

# display existing  products with their prices and whether they require a doctor’s prescription or not
def display_products():
    print("\n=============================Existing Products=============================")
    for product, info in product_list.items():
        prescription_status = "Prescription Required" if info['prescription_required'] else "No Prescription Required"
        print(f"{product}: ${info['price']}, {prescription_status}")

# display customer order history
def display_order_history():
    # getting the customer name
    cus_name = input("Enter your name to view your order history:")
    # checks if the typed name is not  in the dictionary
    while cus_name not in customer_list:
        print("ERROR!!!! Customer Name cannot be found!!!!")  
        cus_name = input("Enter your name to view your order history:")
    print("=====================================================")
    print(f"This is the Order History of {cus_name}")  

    # enumerate allows you to iterate over a list, tuple, or dictionary and return a tuple containing the index of each element and the element itself
    for i, order in enumerate(orders[cus_name], 1):
        total= sum(item['price'] * item['quantity'] for item in order)
        earned_reward_points = round(total)
        print(f"Order {i}:")
        for item in order:
            print(f"{item['product_name']} x {item['quantity']}\t\t\t{item['price']:.2f}")
        print(f"Total Cost: \t\t\t{total:.2f} (AUD)")
        print(f"Earned Reward Points: \t\t\t{earned_reward_points}")

# Main function to run the program
def main():
    while True:
        print("\n=============================WELCOME TO THE RMIT PHARMACY=============================")
        print("\n")
        print("\n=============================MENU=============================")
        print("1. Make A Purchase")
        print("2. Add/Update Information Of Products")
        print("3. Display Existing Customers")
        print("4. Display Existing Products")
        print("5. Display Customer Order History")
        print("6. Exit")

        option = input("Enter your option[one option at a time]: ")
        if option == '1':
            make_purchase()
        elif option == '2':
            add_update_product()
        elif option == '3':
            display_customers()
        elif option == '4':
            display_products()
        elif option =='5':
            display_order_history()
        elif option == '6':
            print("Exiting the program.Thank you for using the program!!!! SEE YOU AGAIN!!!")
            break
        else:
            print("ERROR!!!! Invalid option!!!!!")

main()
