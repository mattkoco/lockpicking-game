import random
import time
import json
import os

# INSTRUCTIONS
# 1.) Select which lock you'd like (default is 5-pin lock)
# 2.) Guess the pin positions to find the binding pin. You will not be able to pick the lock until you find the binding pin.
# 3.) Once you find the binding pin, guess the pin positions to unlock the lock.
# 4.) The game will tell you how many pins are correct out of the total number of pins, kinda like wordle.
# 5.) Pick the lock as fast as you can. Good luck!
# PLANNED FEATURES
# 1.) DONE
# 2.) Add items and tools to help you pick the lock faster. (Better picks, rakes, bump keys, etc..)
# 3.) Add a scoring system based on how fast you can pick the lock, which coorelates to money earned and eligiability to pick harder locks.
# 4.) Tkinter interface for more user-friendly experience.
# 5.) DONE
# 6.) User created locks.


DATA_FILE = 'lockpicking_game_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {'user_data': {}, 'locks': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def generate_lock(pin_count):
    return [random.randint(0, 9) for _ in range(pin_count)]

def find_binding_pin(lock):
    return random.randint(0, len(lock) - 1)

def get_feedback(lock, guess):
    correct_pins = sum([1 for i in range(len(lock)) if lock[i] == guess[i]])
    return f'{correct_pins} out of {len(lock)} pins are correct'

def select_lock():
    print("Select a lock:")
    print("1. Default 5-pin lock")
    print("2. 4-pin lock")
    print("3. 6-pin lock")
    choice = input("Enter the number of your choice: ")
    
    if choice == '1':
        return 5
    elif choice == '2':
        return 4
    elif choice == '3':
        return 6
    else:
        print("Invalid choice. Using default 5-pin lock.")
        return 5

def update_user_data(data, pin_count, elapsed_time):
    lock_key = f'{pin_count}-pin'
    if lock_key not in data['user_data']:
        data['user_data'][lock_key] = {'attempts': 0, 'fastest_time': None}
    
    data['user_data'][lock_key]['attempts'] += 1
    if data['user_data'][lock_key]['fastest_time'] is None or elapsed_time < data['user_data'][lock_key]['fastest_time']:
        data['user_data'][lock_key]['fastest_time'] = elapsed_time

def main():
    data = load_data()
    
    pin_count = select_lock()
    lock = generate_lock(pin_count)
    binding_pin = find_binding_pin(lock)
    
    print("Welcome to the Lockpicking Game!")
    print(f"You are working with a {pin_count}-pin lock.")
    print("You need to find the binding pin first.")
    print("Guess the pin positions (separated by spaces).")
    
    start_time = time.time()
    found_binding_pin = False
    
    while not found_binding_pin:
        guess = list(map(int, input("Enter your guess: ").split()))
        
        if len(guess) != pin_count:
            print(f"Invalid input. You must enter {pin_count} numbers.")
            continue
        
        if guess[binding_pin] == lock[binding_pin]:
            print(f"Binding pin found! The pin at position {binding_pin + 1} is correct.")
            found_binding_pin = True
        else:
            print("Try again to find the binding pin.")
    
    print("Now, guess the positions of the remaining pins to unlock the lock.")
    
    while True:
        guess = list(map(int, input("Enter your guess: ").split()))
        
        if len(guess) != pin_count:
            print(f"Invalid input. You must enter {pin_count} numbers.")
            continue
        
        feedback = get_feedback(lock, guess)
        print(feedback)
        
        if feedback == f'{pin_count} out of {pin_count} pins are correct':
            elapsed_time = time.time() - start_time
            print(f"Congratulations! You've unlocked the lock in {elapsed_time:.2f} seconds!")
            
            update_user_data(data, pin_count, elapsed_time)
            save_data(data)
            
            break

if __name__ == "__main__":
    main()
