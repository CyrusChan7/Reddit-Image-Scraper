def create_pickle_token():
    credentials = {}
    credentials["client_id"] = input("Reddit Client ID: ")
    credentials["client_secret"] = input("Reddit Client Secret: ")
    credentials["user_agent"] = input("User Agent: ")
    credentials["username"] = input("Reddit Username: ")
    credentials["password"] = input("Reddit Password: ")
    return credentials