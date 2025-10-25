import hashlib
import random
import string
import secrets


permitted_chars = string.ascii_letters + string.digits + r'~!@#$%^&*()_+=-`[]{}\|'
with open('generated_passwords.csv', 'w', encoding='cp949') as file:
    for k in range(1, 201):
        password = ''.join(secrets.choice(permitted_chars) for _ in range(12))
        salt = ''.join(secrets.choice(permitted_chars) for _ in range(12))
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        file.write(f'"user{k}","{hashed_pw};{salt}","{password}"\n')
