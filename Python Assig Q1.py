import string

def check_password_strength(password):
    # Criteria checks
    has_min_length = len(password) >= 8
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special_char = any(char in string.punctuation for char in password)

    # Return True only if all conditions are met
    return all([has_min_length, has_uppercase, has_lowercase, has_digit, has_special_char])


# Main script
if __name__ == "__main__":
    user_password = input("Enter a password to check its strength: ")

    if check_password_strength(user_password):
        print("✅ Strong password! ✔")
    else:
        print("❌ Weak password. Make sure it has:")
        print("- At least 8 characters")
        print("- Uppercase and lowercase letters")
        print("- At least one number (0-9)")
        print("- At least one special character (!, @, #, $, %, etc.)")
