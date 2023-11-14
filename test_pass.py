from passlib.hash import pbkdf2_sha256 as hasher
password ="adminpw"
hashed = hasher.hash(password)
print(hashed)

print(hasher.verify("adminpw", hashed))
print(hasher.verify("admin_pw", hashed))
