from app.modules.auth.services.auth_service import AuthService
from app.shared.security import hash_password, verify_password

# Test manual
password = "TestPass123!"
hashed = hash_password(password)

print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Verify result: {verify_password(password, hashed)}")

# Test con AuthService
hashed2 = AuthService.hash_password(password)
print(f"\nAuthService Hash: {hashed2}")
print(f"AuthService Verify: {AuthService.verify_password(password, hashed2)}")

# Cross-verify
print(f"\nCross verify 1: {verify_password(password, hashed2)}")
print(f"Cross verify 2: {AuthService.verify_password(password, hashed)}")