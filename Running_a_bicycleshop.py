MENU = {
    "flat_fix": {
        "base_cost": 25,  # $12 for inner tube + $13 for labor
        "optional_parts": {
            "rim_tape": 10,
            "tire": 40
        },
        "inventory": {
            "inner_tube": 1,
            "rim_tape": 0,
            "tire": 0
        }
    },
    "cable_replacement": {
        "base_cost": 21,  # $8 for cable + $13 for labor
        "optional_parts": {},
        "inventory": {
            "cable": 1
        }
    },
    "brake_pad_replacement": {
        "base_cost": 35,  # $15 for brake pads + $20 for labor
        "optional_parts": {},
        "inventory": {
            "brake_pads": 1
        }
    },
    "gear_adjustment": {
        "base_cost": 20,  # $20 for labor
        "optional_parts": {},
        "inventory": {}
    },
    "brake_adjustment": {
        "base_cost": 20,  # $20 for labor
        "optional_parts": {},
        "inventory": {}
    }
}

inventory = {
    "inner_tube": 100,
    "tire": 20,
    "rim_tape": 100,
    "cable_brake": 100,
    "cable_gear": 50,
    "brake_pads": 100
}

profit = 0


def is_resource_sufficient(order_inventory):
    """Returns True when order can be made, False if inventory is insufficient."""
    for item in order_inventory:
        if order_inventory[item] > inventory[item]:
            print(f"Sorry, there is not enough {item.replace('_', ' ')}.")
            return False
    return True


def process_payment(cost):
    """Process the payment and return the total amount paid."""
    payment_method = input("Would you like to pay with credit card or cash? (card/cash): ").lower()
    if payment_method == "card":
        print("Processing payment through credit card terminal...")
        return cost
    elif payment_method == "cash":
        print("Please insert cash.")
        total = int(input("How many quarters?: ")) * 0.25
        total += int(input("How many dimes?: ")) * 0.1
        total += int(input("How many nickles?: ")) * 0.05
        total += int(input("How many pennies?: ")) * 0.01
        total += int(input("How many $1 bills?: ")) * 1
        total += int(input("How many $5 bills?: ")) * 5
        total += int(input("How many $10 bills?: ")) * 10
        total += int(input("How many $20 bills?: ")) * 20
        return total
    else:
        print("Invalid payment method.")
        return 0


def is_transaction_successful(money_received, cost):
    """Return True when the payment is accepted, or False if money is insufficient."""
    if money_received >= cost:
        change = round(money_received - cost, 2)
        if change > 0:
            print(f"Here is ${change} in change.")
        global profit
        profit += cost
        return True
    else:
        print("Sorry, that's not enough money. Money refunded.")
        return False


def perform_service(service_name, service_details):
    """Perform the service and deduct the required inventory."""
    for item in service_details["inventory"]:
        inventory[item] -= service_details["inventory"][item]
    print(f"The {service_name.replace('_', ' ')} has been completed.")


is_on = True

while is_on:
    choice = input("What service would you like? (flat_fix/cable_replacement/brake_pad_replacement/gear_adjustment/brake_adjustment): ")
    if choice == "off":
        is_on = False
    elif choice == "report":
        print(f"Inner Tubes: {inventory['inner_tube']}")
        print(f"Tires: {inventory['tire']}")
        print(f"Rim Tapes: {inventory['rim_tape']}")
        print(f"Cables (Brake): {inventory['cable_brake']}")
        print(f"Cables (Gear): {inventory['cable_gear']}")
        print(f"Brake Pads: {inventory['brake_pads']}")
        print(f"Profit: ${profit}")
    else:
        service = MENU[choice]
        if is_resource_sufficient(service["inventory"]):
            total_cost = service["base_cost"]
            if "optional_parts" in service:
                for part, cost in service["optional_parts"].items():
                    if input(f"Would you like to add {part.replace('_', ' ')} for ${cost}? (yes/no): ").lower() == "yes":
                        total_cost += cost
                        if part in inventory:
                            service["inventory"][part] = 1

            payment = process_payment(total_cost)
            if is_transaction_successful(payment, total_cost):
                perform_service(choice, service)

