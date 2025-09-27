"""
You need to implement a bank system that will allow a certain group of actions.
* register_account account_name (unique)
    registers an account, account name needs to be unique
* deposit account_name amount (0 < amount <= 10000)
    deposits name to an existing account, needs to validate amount constraints
* balance account_name
    checks balance for a valid account
* withdraw account_name amount (0 < amount <= min(10000, balance))
    withdraws amount from a valid account, needs to validate amount constraints
* logs account_name
    prints all actions executed in order over an account.
"""
class AccountNotFoundError(Exception):
    """Raised when an account does not exist."""
    pass

account_balances = {}
account_logs = {}

def register_account(account_name):
    if account_name in account_balances:
        print("Account name already exists.")
        return
    account_balances[account_name] = 0
    account_logs[account_name] = []
    account_logs[account_name].append("Account registered")
    print(f"Account {account_name} registered")

def deposit(account_name, amount):
    existing_account(account_name)          
    amount = round(float(amount), 2)
    if not (0 < amount <= 10000):
        print("Invalid deposit amount.")
        return
    account_balances[account_name] += amount
    print(f"Deposited {amount} to {account_name}")
    account_logs[account_name].append(f"Deposited {amount}")

def balance(account_name):
    existing_account(account_name)
    balance = account_balances[account_name]
    print(f"Balance for {account_name} is {balance}")
    account_logs[account_name].append(f"Checked balance: {balance}")

def withdraw(account_name, amount):
    existing_account(account_name)          
    amount = round(float(amount), 2)
    if not (0 < amount <= 10000):
        print("Invalid withdrawal amount")
        return
    if account_balances[account_name] - amount < 0:
        print("Insufficient funds")
        return
    account_balances[account_name] -= amount
    print(f"Withdrew {amount} from {account_name}")
    account_logs[account_name].append(f"Withdrew {amount}")

def logs(account_name):
    existing_account(account_name)
    print(f"Logs for {account_name}:")
    for log in account_logs[account_name]:
        print(log)

def existing_account(account_name):
    if account_name not in account_balances:
        raise AccountNotFoundError("Account does not exist")

actions = {
    "register_account": register_account,
    "deposit": deposit,
    "balance": balance,
    "withdraw": withdraw,
    "logs": logs,
}
if __name__ == "__main__":
    print("Welcome to The Beast Bank!")
    print("--------------------------")
    command_count = 0
    while True:
        try:
            command = input(f"Command {command_count}:\n")
            command_pieces = command.split(" ")
            action = command_pieces[0]
            parameters = command_pieces[1: ]
            actions[action](*parameters)
        except KeyboardInterrupt:
            print("\n\nStopping bank.")
            break
        except KeyError:
            print("Not known command!!!")
        except (IndexError, ValueError, TypeError):
            # this might be swallowing errors...
            print("Invalid command.")
        except AccountNotFoundError:
            print("Account does not exist")
        else:
            command_count += 1