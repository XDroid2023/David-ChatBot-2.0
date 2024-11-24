def main():
    print("Hi! I'm David, your friendly chatbot!")
    
    # Ask for name
    name = input("What's your name? ")
    
    # Ask for age
    while True:
        try:
            age = int(input(f"Nice to meet you, {name}! How old are you? "))
            break
        except ValueError:
            print("Please enter a valid number for your age.")
    
    # Respond based on age
    if age < 18:
        print(f"Wow {name}, you're still young! Enjoy your youth!")
    elif age < 30:
        print(f"Cool {name}, your twenties are a great time!")
    elif age < 50:
        print(f"Nice {name}, you must have lots of life experience!")
    else:
        print(f"Wonderful {name}, you have so many stories to share!")
    
    print("It was great chatting with you!")

if __name__ == "__main__":
    main()
