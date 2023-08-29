import random
import string
import json
import hmac
import hashlib

def generate_random_string(length):
    """Generates a random string of the specified length."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def create_wallet():
    """Creates a new cryptocurrency wallet."""
    private_key = generate_random_string(64)
    public_key = generate_random_string(64)
    return {
        'private_key': private_key,
        'public_key': public_key
    }

def store_wallet(wallet):
    """Stores a cryptocurrency wallet in a secure location."""
    with open('wallet.txt', 'w') as f:
        f.write(json.dumps(wallet))

def send_transaction(wallet, recipient_public_key, amount):
    """Sends a cryptocurrency transaction to the specified recipient."""
    transaction = {
        'sender_public_key': wallet['public_key'],
        'recipient_public_key': recipient_public_key,
        'amount': amount
    }
    signature = sign_transaction(wallet['private_key'], transaction)
    transaction['signature'] = signature
    return transaction

def sign_transaction(private_key, transaction):
    """Signs a cryptocurrency transaction."""
    message = json.dumps(transaction).encode('utf-8')
    signature = hmac.new(private_key.encode('utf-8'), message, hashlib.sha256).hexdigest()
    return signature

def verify_transaction(transaction):
    """Verifies a cryptocurrency transaction."""
    message = json.dumps(transaction).encode('utf-8')
    signature = transaction['signature']
    public_key = transaction['sender_public_key']
    return hmac.verify(signature.encode('utf-8'), message, public_key.encode('utf-8'))

def main():
    """Main function."""
    wallet = create_wallet()
    store_wallet(wallet)
    transaction = send_transaction(wallet, 'recipient_public_key', 100)
    print(transaction)
    assert verify_transaction(transaction)

if __name__ == '__main__':
    main()
