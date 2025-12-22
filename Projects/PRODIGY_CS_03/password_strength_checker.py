import re
import getpass

def assess_password_strength(password):
    feedback = []
    strength = 0
    length = len(password)

    # Calculate length score and check minimum length
    length_score = 0
    if length >= 16:
        length_score = 3
    elif length >= 12:
        length_score = 2
    elif length >= 8:
        length_score = 1
    else:
        feedback.append("Password is too short (minimum 8 characters required).")
    strength += length_score

    # Check for character types using regular expressions
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'[0-9]', password) is not None
    has_special = re.search(r'[^A-Za-z0-9]', password) is not None

    # Update feedback and strength based on character types
    if not has_upper:
        feedback.append("Password must include at least one uppercase letter.")
    else:
        strength += 1

    if not has_lower:
        feedback.append("Password must include at least one lowercase letter.")
    else:
        strength += 1

    if not has_digit:
        feedback.append("Password must include at least one number.")
    else:
        strength += 1

    if not has_special:
        feedback.append("Password must include at least one special character.")
    else:
        strength += 1

    # Determine the strength category
    if length < 8:
        strength_category = "Very Weak"
    else:
        if strength <= 2:
            strength_category = "Weak"
        elif 3 <= strength <= 4:
            strength_category = "Medium"
        elif 5 <= strength <= 6:
            strength_category = "Strong"
        else:  # strength is 7
            strength_category = "Very Strong"

    return {
        'strength': strength_category,
        'feedback': feedback
    }

if __name__ == "__main__":
    password = getpass.getpass("Enter your password: ")
    result = assess_password_strength(password)
    print(f"\nPassword Strength: {result['strength']}")
    if result['feedback']:
        print("Feedback:")
        for msg in result['feedback']:
            print(f"- {msg}")