import sys
import os

def main():
    print("--- Day 3 Python App ---")
    
    # Check if we are in a CI environment
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("Running inside GitHub Actions!")
    else:
        print("Running locally.")
        
    print("Logic check passed.")

if __name__ == "__main__":
    main()
