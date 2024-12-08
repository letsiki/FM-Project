import os
import json
import itertools
from Coach import Coach

DATA_FOLDER = 'Coach Assigner/data'

# Function to input a coach's attributes from user
def input_coach():
    name = input("Enter coach name: ")
    attributes = {}
    
    # Ask for each attribute
    for attr in ['Dis', 'Det', 'Mot', 'Tec', 'Tac', 'Att', 'Def', 'Men']:
        while True:
            try:
                value = int(input(f"Enter value for {attr} (1-20): "))
                if 1 <= value <= 20:
                    attributes[attr] = value
                    break
                else:
                    print("Please enter a value between 1 and 20.")
            except ValueError:
                print("Please enter a valid integer.")
    
    coach = Coach(name=name, **attributes)
    save_coach_to_json(coach)
    return coach

# Save a coach to a JSON file
def save_coach_to_json(coach):
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    coach_data = {
        'name': coach.name,
        'Dis': coach.Dis,
        'Det': coach.Det,
        'Mot': coach.Mot,
        'Tec': coach.Tec,
        'Tac': coach.Tac,
        'Att': coach.Att,
        'Def': coach.Def,
        'Men': coach.Men
    }
    
    filepath = os.path.join(DATA_FOLDER, f"{coach.name}.json")
    with open(filepath, 'w') as json_file:
        json.dump(coach_data, json_file)
    print(f"Coach {coach.name} saved to {filepath}.")

# Load a coach from a JSON file
def load_coach_from_json(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, 'r') as json_file:
        coach_data = json.load(json_file)
        return Coach(**coach_data)

# Ask if user wants to load existing coaches from JSON files
def load_coaches_from_json():
    if not os.path.exists(DATA_FOLDER):
        print("No saved coaches found.")
        return []

    json_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.json')]
    if not json_files:
        print("No saved coaches found.")
        return []

    print("Saved coaches found:")
    for idx, filename in enumerate(json_files, 1):
        print(f"{idx}. {filename[:-5]}")

    coaches = []
    load_all = input("Do you want to load all coaches? (yes/no): ").strip().lower()

    if load_all == 'yes':
        for filename in json_files:
            coach = load_coach_from_json(filename)
            coaches.append(coach)
            print(f"Coach {coach.name} loaded.")
    else:
        while True:
            choice = input("Enter the number of the coach to load (or type 'done' to stop): ")
            if choice.lower() == 'done':
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(json_files):
                    coach = load_coach_from_json(json_files[idx])
                    coaches.append(coach)
                    print(f"Coach {coach.name} loaded.")
                else:
                    print("Invalid number, please try again.")
            except ValueError:
                print("Invalid input, please enter a number.")
    
    return coaches


# Try to assign each coach to a role based on their best roles
def assign_roles(coaches):
    roles = ['ATe', 'ATa', 'DTe', 'DTa', 'PTe', 'PTa']

    # Generate all permutations of coach-role assignments
    best_combination = None
    best_total_rating = -1

    # Check every possible combination of role assignments
    for permutation in itertools.permutations(coaches, len(roles)):
        total_rating = 0
        valid_combination = True

        # Check if each coach can be assigned to their respective role in the current permutation
        for coach, role in zip(permutation, roles):
            # Get coach's rating for the current role
            coach_best_roles = coach.best_roles()

            # Check if the coach has the current role as a valid option
            role_rating = next((rating for best_role, rating in coach_best_roles if best_role == role), None)
            if role_rating is not None:
                total_rating += role_rating
            else:
                valid_combination = False
                break

        # If it's a valid combination and the total rating is the best so far, save it
        if valid_combination and total_rating > best_total_rating:
            best_total_rating = total_rating
            best_combination = list(zip(permutation, roles))

    if best_combination is None:
        raise ValueError("No valid combination of coaches and roles found.")
    
    return best_combination, best_total_rating

# Main entry point
if __name__ == "__main__":
    coaches = []

    # Ask if user wants to load existing coaches
    load_from_json = input("Do you want to load existing coaches from JSON? (yes/no): ").strip().lower()

    if load_from_json == 'yes':
        coaches += load_coaches_from_json()

    # Keep asking to add more coaches
    while True:
        add_more = input("Do you want to add a new coach? (yes/no): ").strip().lower()
        if add_more == 'yes':
            coach = input_coach()
            coaches.append(coach)
        else:
            break

    # Check if enough coaches were added
    if len(coaches) < 6:
        print(f"You need at least 6 coaches to assign roles, but you only added {len(coaches)}.")
    else:
        # Try to assign coaches to roles
        try:
            best_assignment, best_rating = assign_roles(coaches)
            print(f"Best Assignment (Total Rating: {best_rating}):")
            for coach, role in best_assignment:
                print(f"Coach {coach.name} assigned to role {role} with rating: {getattr(coach, role)}")
        except ValueError as e:
            print(e)
