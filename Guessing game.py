import random

secret = random.randint(1, 20)
attempts = 0
guess = None

print("Welcome to the Guessing Game!")
print("I'm thinking of a number between 1 and 20. Can you guess it?")

while guess != secret:
 
   guess = int(input("Guess your number: "))
   attempts += 1

   if guess > secret:
    print("Too High!")
   elif guess < secret:
     print("Too Low!")
   else:
      print(f"Correct! You guessed it in {attempts} attempts!")
   
