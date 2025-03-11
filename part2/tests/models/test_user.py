from app.models.user import User


def test_user_creation():
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


test_user_creation()


def test_admin_user_creation():
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe.admin@example.com",
        is_admin=True)
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe.admin@example.com"
    assert user.is_admin is True
    print("Admin User creation test passed!")


test_admin_user_creation()
