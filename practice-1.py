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

class NotLoggedInError(Exception):
    """Raised when not logged into an account."""
    pass

class AlreadyLoggedInError(Exception):
    """Raised when already logged into a different account."""
    pass

class User:
    def __init__(self):
        self.current = None

user = User()

account_balances = {}
account_logs = {}

def login(account_name):
    existing_account(account_name)
    if user.current:
        print(f"Already logged into {user.current}")
        return
    user.current = account_name
    print(f"Successfully logged in {account_name}")

def logout(account_name):
    if not user.current:
        print("No one is logged in")
    elif account_name != user.current:
        print("Logged into a different account")
    else:
        user.current = None
        print(f"Successfully logged out {account_name}")

def register_account(account_name):
    if account_name in account_balances:
        print("Account name already exists.")
        return
    account_balances[account_name] = 0
    account_logs[account_name] = []
    account_logs[account_name].append("Account registered")
    print(f"Account {account_name} registered")

def deposit(account_name, amount):
    login_check(account_name)
    existing_account(account_name)          
    amount = round(float(amount), 2)
    if not (0 < amount <= 10000):
        print("Invalid deposit amount.")
        return
    account_balances[account_name] += amount
    print(f"Deposited {amount} to {account_name}")
    account_logs[account_name].append(f"Deposited {amount}")

def balance(account_name):
    login_check(account_name)
    existing_account(account_name)
    balance = account_balances[account_name]
    print(f"Balance for {account_name} is {balance}")
    account_logs[account_name].append(f"Checked balance: {balance}")

def withdraw(account_name, amount):
    login_check(account_name)
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
    login_check(account_name)
    existing_account(account_name)
    print(f"Logs for {account_name}:")
    for log in account_logs[account_name]:
        print(log)

def existing_account(account_name):
    if account_name not in account_balances:
        raise AccountNotFoundError("Account does not exist")
    
def login_check(account_name):
    if user.current is None:
        raise NotLoggedInError("Must be logged in")
    if user.current != account_name:
        raise AlreadyLoggedInError(f"Must be logged in as {account_name} (currently logged in as {user.current})")

actions = {
    "register_account": register_account,
    "deposit": deposit,
    "balance": balance,
    "withdraw": withdraw,
    "logs": logs,
    "login": login,
    "logout": logout
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
        except NotLoggedInError:
            print("Not logged in")
        except AlreadyLoggedInError:
            print("Already logged into a different account")
        else:
            command_count += 1