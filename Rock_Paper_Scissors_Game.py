import random
from colorama import Fore, init
from prettytable import PrettyTable  # For nice scoreboard table

# Initialize Colorama
init(autoreset=True)

# Game Items
ITEMS = ["Rock", "Paper", "Scissor"]

print(Fore.CYAN + "\n===== Rock | Paper | Scissor Game =====\n")
print(Fore.YELLOW + "Rules: Best of 5 rounds. Let's see who wins!\n")

# Score counters
user_score = 0
comp_score = 0
rounds = 5

# Table for results
scoreboard = PrettyTable()
scoreboard.field_names = ["Round", "Your Choice", "Computer Choice", "Winner"]

for i in range(1, rounds + 1):
    print(Fore.MAGENTA + f"\n--- Round {i} ---")
    user_choice = input(Fore.GREEN + "Enter your move (Rock, Paper, Scissor):\n").strip().capitalize()
    
    # Validate input
    while user_choice not in ITEMS:
        user_choice = input(Fore.RED + "Invalid choice! Please enter Rock, Paper, or Scissor:\n").strip().capitalize()

    # Computer choice
    comp_choice = random.choice(ITEMS)
    print(Fore.BLUE + f"\nYou chose: {user_choice}\nComputer chose: {comp_choice}")

    # Decide winner
    if user_choice == comp_choice:
        result = "Tie"
        print(Fore.YELLOW + "Result: It's a Tie!")
    elif (user_choice == "Rock" and comp_choice == "Scissor") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissor" and comp_choice == "Paper"):
        result = "You"
        print(Fore.GREEN + "Result: You Win this round! 🎉")
        user_score += 1
    else:
        result = "Computer"
        print(Fore.RED + "Result: Computer Wins this round! 🤖")
        comp_score += 1

    # Add to table
    scoreboard.add_row([i, user_choice, comp_choice, result])

# Final result
print(Fore.CYAN + "\n===== Game Over =====")
print(scoreboard)  # Show table
print(Fore.GREEN + f"\nYour Score: {user_score}")
print(Fore.RED + f"Computer Score: {comp_score}")

if user_score > comp_score:
    print(Fore.GREEN + "\n🎉 Congratulations! You are the Final Winner! 🎉")
elif comp_score > user_score:
    print(Fore.RED + "\n🤖 Computer Wins the Game! Better luck next time.")
else:
    print(Fore.YELLOW + "\nIt's a Tie! Well played!")
