import math
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

WORDLIST_SIZE = 2048
COMMON_NAMES = ["john", "mary", "mike", "joe", "alice", "bob"]
OFFLINE_HASH_SPEED = 1e9
ONLINE_ATTEMPTS_PER_SECOND = 5

ph = PasswordHasher()

def analyze_password(password: str):
    length = len(password)
    charset_size = 0
    sets_used = []
    if re.search(r"[a-z]", password):
        charset_size += 26
        sets_used.append("lowercase")
    if re.search(r"[A-Z]", password):
        charset_size += 26
        sets_used.append("uppercase")
    if re.search(r"\d", password):
        charset_size += 10
        sets_used.append("digits")
    if re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/\\|]", password):
        charset_size += 32
        sets_used.append("symbols")
    entropy = length * math.log2(charset_size) if charset_size > 0 else 0
    return {"length": length, "charset_size": charset_size, "sets_used": sets_used, "entropy_bits": round(entropy, 2)}

def analyze_passphrase(passphrase: str):
    words = re.split(r"\s+|-|_", passphrase.strip())
    num_words = len(words)
    entropy = num_words * math.log2(WORDLIST_SIZE)
    return {"passphrase": passphrase, "num_words": num_words, "entropy_bits": round(entropy, 2), "words": words}

def entropy_rating(bits):
    if bits < 28: return "❌ Very Weak"
    elif bits < 36: return "⚠️ Weak"
    elif bits < 60: return "🟡 Reasonable"
    elif bits < 80: return "✅ Strong"
    else: return "🔥 Very Strong"

def human_pattern_warnings_password(password):
    warnings = []
    if password.lower().endswith("1"): warnings.append("Ends with a digit")
    if password.startswith(("@", "!", "#", "$")): warnings.append("Symbol at start")
    if re.search(r"[A-Z][a-z]+", password): warnings.append("Looks like a name or dictionary word")
    if len(password) < 12: warnings.append("Short length")
    return warnings

def human_pattern_warnings_passphrase(words):
    warnings = []
    for w in words:
        if w.lower() in COMMON_NAMES: warnings.append(f"Word '{w}' is a common name")
        if len(w) < 3: warnings.append(f"Word '{w}' is very short")
    return warnings

def improvement_suggestions_password(password, analysis, warnings):
    suggestions = []
    if analysis['length'] < 12: suggestions.append("Increase length to at least 12 characters")
    required_sets = ["lowercase", "uppercase", "digits", "symbols"]
    missing_sets = [s for s in required_sets if s not in analysis['sets_used']]
    if missing_sets: suggestions.append(f"Add character types: {', '.join(missing_sets)}")
    for w in warnings:
        if "symbol at start" in w: suggestions.append("Move symbol to middle or end")
        if "Ends with a digit" in w: suggestions.append("Avoid digits only at the end")
        if "Looks like a name" in w: suggestions.append("Break dictionary words or names with symbols/numbers")
    return suggestions

def improvement_suggestions_passphrase(analysis, warnings):
    suggestions = []
    if analysis['entropy_bits'] < 80: suggestions.append("Increase number of words to >=5")
    for w in warnings: suggestions.append(f"Replace {w} with a less common word")
    return suggestions

def time_to_crack(entropy_bits, offline=True):
    guesses = 2**entropy_bits
    if offline: seconds = guesses / OFFLINE_HASH_SPEED
    else: seconds = guesses / ONLINE_ATTEMPTS_PER_SECOND
    units = [("years", 60*60*24*365), ("days", 60*60*24), ("hours", 3600), ("minutes", 60), ("seconds", 1)]
    for name, div in units:
        if seconds >= div: return f"{seconds/div:.2f} {name}"
    return f"{seconds:.2f} seconds"

choice = input("Analyze (1) single password or (2) passphrase? Enter 1 or 2: ").strip()
if choice == "1":
    pw = input("Enter password: ")
    analysis = analyze_password(pw)
    warnings = human_pattern_warnings_password(pw)
    suggestions = improvement_suggestions_password(pw, analysis, warnings)
    print("\nPassword Analysis\n" + "-"*40)
    print(f"Length: {analysis['length']}")
    print(f"Character sets: {', '.join(analysis['sets_used'])}")
    print(f"Entropy: {analysis['entropy_bits']} bits")
    print(f"Rating: {entropy_rating(analysis['entropy_bits'])}")
    print(f"Offline crack time: {time_to_crack(analysis['entropy_bits'], offline=True)}")
    print(f"Online crack time: {time_to_crack(analysis['entropy_bits'], offline=False)}")
    if warnings:
        print("\nHuman-pattern warnings:")
        for w in warnings: print(" -", w)
    if suggestions:
        print("\nImprovement Suggestions:")
        for s in suggestions: print(" -", s)
    hashed = ph.hash(pw)
    print(f"\nArgon2 hash: {hashed}")
    login_try = input("\nRe-enter password to verify: ")
    try:
        ph.verify(hashed, login_try)
        print("✅ Password verified successfully")
    except:
        print("❌ Verification failed")

elif choice == "2":
    pp = input("Enter passphrase: ")
    analysis = analyze_passphrase(pp)
    warnings = human_pattern_warnings_passphrase(analysis['words'])
    suggestions = improvement_suggestions_passphrase(analysis, warnings)
    print("\nPassphrase Analysis\n" + "-"*40)
    print(f"Passphrase: {analysis['passphrase']}")
    print(f"Number of words: {analysis['num_words']}")
    print(f"Entropy: {analysis['entropy_bits']} bits")
    print(f"Rating: {entropy_rating(analysis['entropy_bits'])}")
    print(f"Offline crack time: {time_to_crack(analysis['entropy_bits'], offline=True)}")
    print(f"Online crack time: {time_to_crack(analysis['entropy_bits'], offline=False)}")
    if warnings:
        print("\nHuman-pattern warnings:")
        for w in warnings: print(" -", w)
    if suggestions:
        print("\nImprovement Suggestions:")
        for s in suggestions: print(" -", s)
    hashed = ph.hash(pp)
    print(f"\nArgon2 hash: {hashed}")
    login_try = input("\nRe-enter passphrase to verify: ")
    try:
        ph.verify(hashed, login_try)
        print("✅ Passphrase verified successfully")
    except:
        print("❌ Verification failed")

else:
    print("Invalid choice. Enter 1 or 2.")
    print("\n✅ No obvious human patterns detected")
    print("✅ No obvious human patterns detected")