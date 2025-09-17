import re

# example database
users = {
    1: {
        "email": "user@example.com",
        "name": "username",
        "password": "password",
        "is_admin": False
    }
}

#register function
def register_user(email:str, name:str, password:str) -> dict:
    """takes email, name, and password, and checks if the 
    user exists  and verify their password.
    Validation: email must contain 'a', password must be at least 8 characters long
    and contain at least one digit, email must be unique
    action: if valid, create a new user with a unique id,
    default 'is_admin' to False
    Return: {"status": "success", "message": "User registered successfully, "user_id":2} or 
    {"status": "error", "message": "user email already exists."}
    """

    #email validation checks
    if '@' not in email:
        return {"status": "error", "message": "Invalid email format.Email must contain '@' followed by mail provider e.g. 'gmail.com'."}
    if any(user['email'] == email for user in users.values()):
        return {"status": "error", "message": "User email already exists."}
    if len(password) < 8 or not re.search(r'\d', password):
        return {"status": "error", "message": "Invalid password. Password must be at least 8 characters long and contain at least one digit."}

    # If all checks pass, create a new user
    last_user_id = int(list(users.keys())[-1]) if users else 0 
    user_id = last_user_id + 1 
    users[user_id] = {
        "email": email,
        "name": name,
        "password": password,
        "is_admin": False 
    }
    return {"status": "success", "message": "User registered successfully.", "user_id": str(user_id)}

#login function
def user_login(email:str, password:str) -> dict:
    """action: check if user exists with email and if password matches
    return: {"status": "success", "message": "Login successful.", "user_id":1} or 
    {"status": "error", "message": "Invalid email or password."}
    """    
    for user_id, user in users.items():
        if user['email'] == email and user['password'] == password:
            return {"status": "success", "message": "Login successful.", "user_id": str(user_id)}
    return {"status": "error", "message": "Invalid email or password."}

#remove user function
def remove_user(user_id:int) -> dict:
    """action: remove user with given user_id if exists
    return: {"status": "success", "message": "User removed successfully."} or 
    {"status": "error", "message": "User not found."}
    """
    if user_id in users:
        del users[user_id]
        return {"status": "success", "message": "User removed successfully."}
    else:
        return {"status": "error", "message": "User not found."}


#list users function
def list_users() -> dict:
    """action: return list of all users
    return: all users' id, emails, name but never passwords
    return: {"status": "success", "users": [{"id":1, "email":....}]} or
    {"status": "error", "message": "No users found."}
    """
    if users:
        user_list = [(user_id, user["email"], user["name"]) for user_id, user in users.items()]
        return {"status": "success", "users": user_list}
    else:
        return {"status": "error", "message": "No users found."}
    
#update user password function
def update_user_password(user_id:int, old_password:str, new_password:str):
    """check that user exists, validate old password and replace with new password"""
    for id in users.keys():
        if user_id == id and old_password == users[id]['password']:
            users[id]['password'] = new_password
            return {"status": "success", "message": "Password updated successfully."}

    return {"status": "error", "message": "Old password is incorrect."}

# test block
if __name__ == "__main__":
    # Example usage
    print("Registering test user...")
    print(register_user("aria@gmail.com", "aria_khan", "password!q1"))

    print("\nTrying to login...")
    print(user_login("aria@gmail.com", "password!q1"))

    print("\nRemoving user ID 2...")
    print(remove_user(2))

    print("\nCurrent users:")
    print(users)
