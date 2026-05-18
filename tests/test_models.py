from models import User

def test_user_password_hash():
    user = User(username="test")
    user.set_password("test")

    assert user.password_hash is not None
    assert user.check_password("test") == True
    assert user.check_password("wrong") == False
