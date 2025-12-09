def show_balance(balance):
    print(f"Your current balance is: ${balance:.2f}")
def deposit():
    amount = float(input("Enter amount to be deposited: "))
    if amount < 0:
        print("This is not a valid amount.")
        return 0 
    else:
        return amount
    
def withdraw(balance):
    amount = float(input("Enter amount to be withdrawn: "))

    if amount > balance:
        print("Insufficient balance.")
        return 0
    elif amount < 0:
        print("Amount must be greater than 0.")
        return 0
    else:
        return amount
def main():
    balance = 0
    is_running = True

    while is_running:
        print("**********")
        print("Banking Program")
        print("**********")
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            amount = deposit()
            balance += amount
            print(f"${amount:.2f} deposited successfully.")
        elif choice == '3':
            amount = withdraw(balance)
            balance -= amount
            if amount > 0:
                print(f"${amount:.2f} withdrawn successfully.")
        elif choice == '4':
            is_running = False
            print("Thank you for using the banking program. Goodbye!")
        else:
            print("Invalid option. Please choose a number between 1 and 4.")
    
if __name__ == "__main__":
    main()
