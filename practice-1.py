"Implement banking system"

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

transfers = []

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

def deposit(amount):
    login_check(user.current)
    existing_account(user.current)          
    amount = round(float(amount), 2)
    if not (0 < amount <= 10000):
        print("Invalid deposit amount.")
        return
    account_balances[user.current] += amount
    print(f"Deposited {amount} to {user.current}")
    account_logs[user.current].append(f"Deposited {amount}")

def balance():
    login_check(user.current)
    existing_account(user.current)
    balance = account_balances[user.current]
    print(f"Balance for {user.current} is {balance}")
    account_logs[user.current].append(f"Checked balance: {balance}")

def withdraw(amount):
    login_check(user.current)
    existing_account(user.current)          
    amount = round(float(amount), 2)
    if not (0 < amount <= 10000):
        print("Invalid withdrawal amount")
        return
    if account_balances[user.current] - amount < 0:
        print("Insufficient funds")
        return
    account_balances[user.current] -= amount
    print(f"Withdrew {amount} from {user.current}")
    account_logs[user.current].append(f"Withdrew {amount}")

def logs():
    login_check(user.current)
    existing_account(user.current)
    print(f"Logs for {user.current}:")
    for log in account_logs[user.current]:
        print(log)

def existing_account(account_name):
    if account_name not in account_balances:
        raise AccountNotFoundError(f"The account {account_name} does not exist")
    
def login_check(account_name):
    if user.current is None:
        raise NotLoggedInError("Must be logged in")
    if user.current != account_name:
        raise AlreadyLoggedInError(f"Must be logged in as {account_name} (currently logged in as {user.current})")
    
def transfer(recipient_name, amount):
    login_check(user.current)
    existing_account(user.current) #cannot transfer from an account that does not exist"
    existing_account(recipient_name) #cannot transfer to an account that does not exist"
    withdraw(amount) #cannot withdraw insufficient funds

    transfers.append({"from":user.current, "to":recipient_name, "amount":amount})
    print(f"Sending {round(float(amount), 2)} to {recipient_name}")

def list_pending():
    login_check(user.current)
    existing_account(user.current)

    pending = []
    for transfer in transfers:
        if transfer["to"] == user.current:
            pending.append({"from": transfer["from"], "amount": transfer["amount"]})

    print(pending) #format this better

def accept_transfer(sender_name, amount):
    login_check(user.current)
    existing_account(user.current)

    for transfer in transfers:
        if transfer["to"] == user.current and transfer["from"] == sender_name and transfer["amount"] == amount:
            transfers.remove(transfer)
            deposit(amount)
            return
        
    print(f"Transfer of {amount} not found")

def reject_transfer(sender_name, amount):
    login_check(user.current)
    existing_account(user.current)

    for transfer in transfers:
        if transfer["to"] == user.current and transfer["from"] == sender_name and transfer["amount"] == amount:
            transfers.remove(transfer)
            account_balances[sender_name] += float(amount)
            print(f"Returned {amount} to {sender_name}")
            return
        
    print(f"Transfer of {amount} not found")
        
def cancel_transfer(recipient_name, amount):
    login_check(user.current)
    existing_account(user.current)

    for transfer in transfers:
        if transfer["to"] == recipient_name and transfer["from"] == user.current and transfer["amount"] == amount:
            transfers.remove(transfer)
            deposit(amount)
            return
    
    print(f"Transfer of {amount} not found")
    

actions = {
    "register": register_account,
    "deposit": deposit,
    "balance": balance,
    "withdraw": withdraw,
    "logs": logs,
    "login": login,
    "logout": logout,
    "transfer": transfer,
    "list_pending": list_pending,
    "accept_transfer": accept_transfer,
    "reject_transfer": reject_transfer,
    "cancel_transfer": cancel_transfer
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