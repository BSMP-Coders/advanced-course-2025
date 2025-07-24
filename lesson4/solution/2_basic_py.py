import random

choices = ["Rock", "Paper", "Scissors"]

print("Rock Paper Scissors")
print("Type your choice (Rock, Paper, or Scissors). Type 'quit' to exit.")

while True:
    player = input("Your choice: ").capitalize()
    if player == "Quit":
        print("Goodbye!")
        break
    if player not in choices:
        print("Invalid choice. Try again.")
        continue
    computer = random.choice(choices)
    print(f"Computer chose: {computer}")
    if player == computer:
        print("It's a tie!\n")
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        print("You win!\n")
    else:
        print("Computer wins!\n")