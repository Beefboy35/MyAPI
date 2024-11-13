localization = {
    "en": {
        "User already exists.": "User already exists.",
        "Invalid email address.": "Invalid email address.",
        "User '{}' not found.": "User '{}' not found.",
        "invalid_user_data": "Invalid user data.",
        "user_not_found": "User not found.",
        "Email already exists.": "Email already exists.",
        "Could not validate credentials": "Could not validate credentials",
        "Incorrect username or password": "Incorrect username or password",
    },
    "ru": {
        "User already exists.": "Пользователь уже существует.",
        "Invalid email address.": "Некорректный адрес электронной почты.",
        "User '{}' not found.": "Пользователь '{}' не найден.",
        "invalid_user_data": "Некорректные данные пользователя.",
        "user_not_found": "Пользователь не найден.",
        "Email already exists.": "Электронная почта уже существует.",
        "Could not validate credentials": "Не удалось подтвердить учетные данные.",
        "Incorrect username or password": "Неправильное имя пользователя или пароль.",
    }
}

def translate_message(message: str, language: str):
    return localization.get(language, "cum").get(message, message)