from csv import reader, writer


class BankAccount:
    def __init__(self, owner, pin, balance=0.0):
        self.owner = owner
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

    def check_balance(self):
        return f'Your balance is {self.balance}'

    def update(self):
        with open('bank_clients.csv', 'r') as file:
            client_list = list(reader(file))
        with open('bank_clients.csv', 'w') as file:
            csv_writer = writer(file)
            for client in client_list:
                if client[0] == self.owner and client[1] == self.pin:
                    csv_writer.writerow([self.owner, self.pin, self.balance])
                else:
                    csv_writer.writerow(client)

    def exit(self):
        i = input('Will you like to perform another transaction? Y/N: ').lower()
        while i not in ['n', 'y']:
            print('Please try again')
            i = input(
                'Will you like to perform another transaction? Y/N: ').lower()
        if i == 'n':
            return True
        elif i == 'y':
            return False

def open_account():
    name = input('Please enter your name: ')
    pin = input('Create a PIN (4 digits): ')
    if len(pin) != 4:
        pin = input('Your PIN must have 4 digits. Try again: ')
    balance = int(input('How much will your initial deposit be: '))

    with open('bank_clients.csv', 'a') as file:
        writer(file).writerow([name.lower(), pin, balance])

    print(f'Welcome {name}, to KAMAJ Bank')


def transaction():
    tries = 3
    message = 'SELECT TRANSACTION (Enter number)\n\
                1. Deposit\n\
                2. Withdrawal\n\
                3. Check balance\n\
                4. Cancel transaction\n'

    with open('bank_clients.csv') as file:
        client_list = list(reader(file))
    
    name = input('Please enter your name: ').lower()
    pin = input('Please enter your PIN: ')
    balance = int(''.join([c for [a, b, c] in client_list if a == name and b == pin]))

    client_id = [[a, b] for [a, b, c] in client_list if a == name and b == pin]
    while [name, pin] not in client_id:
        tries -= 1
        if tries > 0:
            print(f'Invalid PIN. You have {tries} attempts remaining')
            name = input('Please enter your name: ')
            pin = input('Please enter your PIN: ')
            client_id = [[a, b]
                         for [a, b, c] in client_list if a == name and b == pin]
        else:
            return print('Your account has been blocked.')
    print(f'Welcome {name.title()}')

    client = BankAccount(name, pin, balance)    # Creating class instance

    while True:
        action = int(input(message))
        while action not in range(1, 5):
            print('Please try again')
            action = input(message)

        # make a deposit
        if action == 1:
            deposit = int(input('Enter amount to deposit: '))
            print(f'Your new balance is {client.deposit(deposit)}')
            client.update()
            if client.exit():
                break

        # make a withdrawal
        elif action == 2:
            withdrawal = int(input('Enter amount to withdraw: '))
            print(f'Your new balance is {client.withdraw(withdrawal)}')
            client.update()
            if client.exit() == 'n':
                break

        # check balance
        elif action == 3:
            print(client.check_balance())
            if client.exit():
                break

        # cancel transaction
        elif action == 4:
            if client.exit():
                break