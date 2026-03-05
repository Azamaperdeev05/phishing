try:
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash("testpassword")
    print(f"Hashed: {hashed}")
    verified = pwd_context.verify("testpassword", hashed)
    print(f"Verified: {verified}")
except Exception as e:
    import traceback

    traceback.print_exc()
