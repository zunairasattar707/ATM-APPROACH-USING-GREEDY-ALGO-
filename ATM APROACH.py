import time
import datetime
import random

class ATM:
    def __init__(self, denominations):
        # Initialize ATM with denominations and inventory
        self.denominations = sorted(denominations, reverse=True)
        self.inventory = {denom: 10 for denom in self.denominations}  # Each denomination has 10 units initially
        self.balance = sum(denom * 10 for denom in self.denominations)
        self.transaction_logs = []
        self.users = {
            "1234": {"pin": "0000", "balance": 5000, "daily_limit": 2000, "daily_withdrawn": 0},
            "5678": {"pin": "1111", "balance": 3000, "daily_limit": 1500, "daily_withdrawn": 0},
        }

    def authenticate_user(self,card_number, pin):
        user = self.users.get(card_number)
        if user and user["pin"] == pin:
            return True
        return False

    def check_balance(self, card_number):
        return self.users[card_number]["balance"]

    def deposit(self, card_number, deposit_amounts):
        total_deposit = sum(denom * count for denom, count in deposit_amounts.items())
        self.users[card_number]["balance"] += total_deposit
        for denom, count in deposit_amounts.items():
            self.inventory[denom] += country
        self.balance += total_deposit
        self.record_transaction(card_number, "Deposit", total_deposit, details=deposit_amounts)

    def withdraw(self, card_number, amount):
        user = self.users[card_number]
        if amount > user["balance"]:
            return "Insufficient funds in your account."
        if amount > user["daily_limit"] - user["daily_withdrawn"]:
            return "Exceeded daily withdrawal limit."
        if amount > self.balance:
            return "Insufficient funds in ATM."

        original_amount = amount
        dispensed = {}
        for denom in self.denominations:
            if amount >= denom and self.inventory[denom] > 0:
                num_notes = min(amount // denom, self.inventory[denom])
                dispensed[denom] = num_notes
                amount -= denom * num_notes
                self.inventory[denom] -= num_notes

        if amount == 0:
            user["balance"] -= original_amount
            user["daily_withdrawn"] += original_amount
            self.balance -= original_amount
            self.record_transaction(card_number, "Withdrawal", -original_amount, details=dispensed)
            return dispensed
        else:
            for denom, count in dispensed.items():
                self.inventory[denom] += count
            return "Cannot dispense the exact amount with the available denominations."

    def record_transaction(self, card_number, transaction_type, amount, details=None):
        transaction_id = f"T{random.randint(100000, 999999)}"
        self.transaction_logs.append({
            "transaction_id": transaction_id,
            "card_number": card_number,
            "type": transaction_type,
            "amount": amount,
            "details": details,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def transaction_history(self, card_number):
        user_logs = [log for log in self.transaction_logs if log["card_number"] == card_number]
        return user_logs

    def show_inventory(self):
        return self.inventory

    def restock_atm(self, admin_password, restock_amounts):
        if admin_password != "admin123":
            return "Invalid admin password."
        for denom, count in restock_amounts.items():
            if denom in self.denominations:
                self.inventory[denom] += count
                self.balance += denom * count
        return "ATM restocked successfully."

# Interactive Menu
def main():
    atm = ATM([500, 200, 100, 50, 20, 10, 5, 1])

    print("Welcome to the ATM!")
    while True:
        print("\nMenu:")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            card_number = input("Enter your card number: ")
            pin = input("Enter your PIN: ")
            if not atm.authenticate_user(card_number, pin):
                print("Invalid card number or PIN.")
                continue

            while True:
                print("\nUser Menu:")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Transaction History")
                print("5. Logout")
                user_choice = int(input("Enter your choice: "))

                if user_choice == 1:
                    print(f"Account Balance: {atm.check_balance(card_number)}")
                elif user_choice == 2:
                    print("Enter denominations to deposit (e.g., 500:2,200:3):")
                    deposit_input = input()
                    deposit_amounts = {int(k): int(v) for k, v in (item.split(":") for item in deposit_input.split(","))}
                    atm.deposit(card_number, deposit_amounts)
                    print("Money deposited successfully!")
                elif user_choice == 3:
                    amount = int(input("Enter the amount to withdraw: "))
                    result = atm.withdraw(card_number, amount)
                    if isinstance(result, dict):
                        print("Withdrawal successful. Dispensed cash:")
                        for denom, count in result.items():
                            print(f"{denom}: {count}")
                    else:
                        print(result)
                elif user_choice == 4:
                    history = atm.transaction_history(card_number)
                    print("Transaction History:")
                    for log in history:
                        print(log)
                elif user_choice == 5:
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == 2:
            admin_password = input("Enter admin password: ")
            print("Admin Menu:")
            print("1. Show Inventory")
            print("2. Restock ATM")
            admin_choice = int(input("Enter your choice: "))

            if admin_choice == 1:
                inventory = atm.show_inventory()
                print("ATM Inventory:")
                for denom, count in inventory.items():
                    print(f"{denom}: {count}")
            elif admin_choice == 2:
                print("Enter denominations to restock (e.g., 500:5,200:10):")
                restock_input = input()
                restock_amounts = {int(k): int(v) for k, v in (item.split(":") for item in restock_input.split(","))}
                print(atm.restock_atm(admin_password, restock_amounts))
            else:
                print("Invalid choice.")
        elif choice == 3:
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
