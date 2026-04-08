import re
import getpass

def assess_password_strength(password):
    feedback = []
    length = len(password)

    # --- Length scoring using match-case ---
    match length:
        case l if l >= 16:
            length_score = 3
        case l if l >= 12:
            length_score = 2
        case l if l >= 8:
            length_score = 1
        case _:
            length_score = 0
            feedback.append("Password is too short (minimum 8 characters required).")

    # Character type checks (still using regex – no if-else replacement needed here)
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'[0-9]', password) is not None
    has_special = re.search(r'[^A-Za-z0-9]', password) is not None

    # Build strength score and feedback (each missing type adds feedback)
    strength = length_score

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

    # --- Strength categorization using match-case ---
    if length < 8:
        strength_category = "Very Weak"
    else:
        match strength:
            case 0 | 1 | 2:
                strength_category = "Weak"
            case 3 | 4:
                strength_category = "Medium"
            case 5 | 6:
                strength_category = "Strong"
            case 7:
                strength_category = "Very Strong"
            case _:
                strength_category = "Unknown"  # fallback, should not happen

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
