import random
secret = random.randint(1, 20)
guess = int(input("Guess a number between 1 and 20: "))

if guess > secret:
   print("Too High!")
elif guess < secret:
   print("Too Low!")
else:
   print("Correct! you win!")