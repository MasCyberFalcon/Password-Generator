#!/usr/bin/env python3

-- coding: utf-8 --

"""
Falcon Safe Password Toolkit v3

Random Strong Password Generator

Password Strength Checker

Pattern-based Wordlist Creator (AUTHORIZED USE ONLY)
"""


import math, random, string
from datetime import datetime

=== Colors ===

R = "\033[1;91m"
G = "\033[1;92m"
Y = "\033[1;93m"
C = "\033[1;96m"
W = "\033[0m"

===== Helper Functions =====

def estimate_entropy(pw: str) -> float:
pools = 0
if any(c.islower() for c in pw): pools += 26
if any(c.isupper() for c in pw): pools += 26
if any(c.isdigit() for c in pw): pools += 10
if any(c in string.punctuation for c in pw): pools += len(string.punctuation)
return math.log2(pools) * len(pw) if pools else 0.0

def strength_label(entropy: float) -> str:
if entropy < 28: return R + "Very Weak" + W
if entropy < 36: return R + "Weak" + W
if entropy < 60: return Y + "Moderate" + W
if entropy < 80: return G + "Strong" + W
return G + "Very Strong" + W

def generate_random_password(length=16, count=10) -> list:
alphabet = string.ascii_letters + string.digits + string.punctuation
return [''.join(random.SystemRandom().choice(alphabet) for _ in range(length)) for _ in range(count)]

def check_password(pw: str):
ent = estimate_entropy(pw)
return {
"length": len(pw),
"has_lower": any(c.islower() for c in pw),
"has_upper": any(c.isupper() for c in pw),
"has_digit": any(c.isdigit() for c in pw),
"has_symbol": any(c in string.punctuation for c in pw),
"entropy": round(ent, 2),
"label": strength_label(ent)
}

def make_pattern_wordlist(words, prefixes=None, suffixes=None, numbers=True, leet=False, max_combos=50000):
prefixes = prefixes or ['']
suffixes = suffixes or ['']
results = set()
for a in words:
for p in prefixes:
for s in suffixes:
base = f"{p}{a}{s}"
results.add(base)
if numbers:
for n in ('123','2024','2025','01','007'):
results.add(base+n)
if leet:
leet_map = str.maketrans("aAeEoOtTsS","@44300175")
results.add(base.translate(leet_map))
if len(results) >= max_combos:
return list(results)
return list(results)

def save_list(path, items):
with open(path,'w',encoding='utf-8') as f:
for it in items: f.write(str(it)+'\n')
return path

===== Banner & Menu =====
def banner():
    print(C + r"""
       .---.        .-----------
      /     \  __  /    ------
     / /     \(😈)/    -----
    //////   ' \/ `   ---
   //// / // :    : ---
  // /   /  /`    '--
 //          //..\\
        ====UU====UU====
             '//||\\`
               '' ''
   FALCON PASSWORD TOOLKIT v3
==========🦅🦅🦅==================""" + W)
###def banner():
print(C + "\n=======🦅🦅🦅🦅🦅=====================")
print("   FALCON PASSWORD TOOLKIT v3 ")
print("==========🦅🦅🦅🦅🦅🦅==================" + W)

def menu():
print(G + "\n[1]" + W + " Generate Random Strong Passwords")
print(G + "[2]" + W + " Check Password Strength")
print(G + "[3]" + W + " Create Pattern-based Wordlist")
print(G + "[0]" + W + " Exit")
return input(Y + "Choose an option: " + W).strip()

===== Main Program =====

def main():
banner()
while True:
ch = menu()
if ch == '0':
print(C + "Bye. Stay Secure, Falcon!" + W)
break

if ch == '1':  
        while True:  
            try:  
                length = int(input("Password length (default 16): ") or "16")  
                count = int(input("How many (default 10): ") or "10")  
                break  
            except ValueError:  
                print(R + "🥵🤦 Invalid input! Enter numbers only." + W)  
        pwds = generate_random_password(length, count)  
        for p in pwds:  
            info = check_password(p)  
            print(G + p + W + f" -> {info['label']} (Entropy {info['entropy']})")  
        if input("Save to file? (y/N): ").lower() == 'y':  
            fname = f"falcon_random_pw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"  
            save_list(fname, pwds)  
            print(C + f"🥰 Saved to {fname}" + W)  

    elif ch == '2':  
        pw = input("Enter password to check: ").strip()  
        if not pw:  
            print(R + "🥵 Empty password!" + W)  
            continue  
        info = check_password(pw)  
        print(f"\nLength: {info['length']}")  
        print("Lowercase:", "✔" if info['has_lower'] else "✘")  
        print("Uppercase:", "✔" if info['has_upper'] else "✘")  
        print("Digits:", "✔" if info['has_digit'] else "✘")  
        print("Symbols:", "✔" if info['has_symbol'] else "✘")  
        print("Entropy:", info['entropy'])  
        print("Strength:", info['label'])  
        print(C + "Tip: Use a long passphrase with mixed types or a password manager.\n" + W)  

    elif ch == '3':  
        print(Y + "** AUTHORIZED USE ONLY **" + W)  
        raw = input("Words (comma separated): ").strip()  
        if not raw:  
            print(R + "🥵 No words provided." + W)  
            continue  
        words = [w.strip() for w in raw.split(',') if w.strip()]  
        prefixes = ['']  
        suffixes = ['']  
        if input("Use prefixes? (y/N): ").strip().lower() == 'y':  
            pre = input("Prefixes (comma separated): ").strip()  
            prefixes = [p.strip() for p in pre.split(',') if p.strip()] or ['']  
        if input("Use suffixes? (y/N): ").strip().lower() == 'y':  
            suf = input("Suffixes (comma separated): ").strip()  
            suffixes = [s.strip() for s in suf.split(',') if s.strip()] or ['']  
        numbers = input("Include numeric tails? (Y/n): ").strip().lower() != 'n'  
        leet = input("Include leet variants? (y/N): ").strip().lower() == 'y'  
        wl = make_pattern_wordlist(words, prefixes, suffixes, numbers, leet)  
        print(G + f"\nGenerated {len(wl)} entries" + W)  
        if input("Save to file? (y/N): ").lower() == 'y':  
            fname = f"falcon_wordlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"  
            save_list(fname, wl)  
            print(C + f"🦅😈 Saved to {fname}" + W)  
        else:  
            print(Y + "Preview (first 30):" + W)  
            for e in wl[:30]:  
                print(" -", e)  
    else:  
        print(R + "🥵🤦 Invalid choice!" + W)

if name == "main":
try:
main()
except KeyboardInterrupt:
print("\n" + R + "Interrupted by user. Exiting..." + W)


