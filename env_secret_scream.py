#!/usr/bin/env python3
# ENV Secret Scream - Because your secrets deserve a proper burial, not a public GitHub funeral

import os
import re
import sys
from pathlib import Path

# The forbidden words that make security teams wake up screaming
SECRET_PATTERNS = [
    r'password\s*=',
    r'api[_-]?key\s*=',
    r'secret\s*=',
    r'token\s*=',
    r'auth\s*=',
    r'credential\s*=',
    r'private[_-]?key\s*=',
]

# Files that should never contain secrets (but often do, because developers)
SUSPECT_FILES = ['.env', 'config.py', 'settings.py', 'secrets.py', 'credentials.json']

def scream_loudly(message):
    """Make the scream audible enough to wake up the intern who committed the .env file"""
    print(f"\n🔴 SCREAMING: {message}")
    return True

def check_file(filepath):
    """Reads files like a nosy neighbor reading your diary"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    scream_loudly(f"{filepath} contains something that looks like '{pattern}'")
                    return True
    except Exception as e:
        print(f"Couldn't read {filepath}: {e}")
    return False

def main():
    """The main event: where secrets go to die (or at least get yelled at)"""
    print("🔍 ENV Secret Scream - Hunting for secrets like they're free pizza")
    print("=" * 60)
    
    found_secrets = False
    
    # Check suspect files first (they're usually guilty)
    for suspect in SUSPECT_FILES:
        if Path(suspect).exists():
            if check_file(suspect):
                found_secrets = True
    
    # Also check for .env files in weird places
    for env_file in Path('.').rglob('*.env*'):
        if env_file.name not in ['.env.example', '.env.sample']:
            if check_file(env_file):
                found_secrets = True
    
    if found_secrets:
        print("\n💀 FOUND SECRETS! Please don't commit these. Your future self will thank you.")
        print("💡 Tip: Add '.env' to .gitignore and use .env.example for templates")
        sys.exit(1)
    else:
        print("✅ No obvious secrets found. You're either secure or very clever at hiding them.")
        sys.exit(0)

if __name__ == "__main__":
    main()
