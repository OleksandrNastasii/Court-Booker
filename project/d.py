from werkzeug.security import generate_password_hash

print(generate_password_hash("secpassword", method='pbkdf2:sha256'))