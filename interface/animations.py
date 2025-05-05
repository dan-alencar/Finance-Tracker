
import sys
import os
import time
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def color(text, fg="white", bold=False):
    colors = {
        "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37
    }
    code = colors.get(fg, 37)
    return f"\033[{1 if bold else 0};{code}m{text}\033[0m"

def typing_print(text, delay=0.003, newline=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        print()

def print_frame(title):
    print("╔" + "═" * 58 + "╗")
    print("║{:^58}║".format("▓▓▓▓▓▓ FINANCE TRACKER ▓▓▓▓▓▓"))
    print("╠" + "═" * 58 + "╣")
    print("║{:^58}║".format(title))
    print("╠" + "═" * 58 + "╣")

def print_menu(options):
    for i, option in enumerate(options, 1):
        typing_print(color(f"║  [{i}] {option:<51}║", fg="white"), delay=0.001)
    print("╚" + "═" * 58 + "╝")

def menu_transition(title, body_lines, pause=True):
    clear_screen()
    print_frame(title)
    for line in body_lines:
        typing_print(color(f"║  {line:<54}║", fg="white"))
        time.sleep(0.05)
    print("╚" + "═" * 58 + "╝")
    if pause:
        typing_print(color("\nPress Enter to continue...", fg="yellow"))
        input()

def opening_animation():
    clear_screen()
    steps = [
        "Initializing dwarven ledger system...",
        "Forging copper-plated budget matrices...",
        "Engraving income streams into stone tablets...",
        "Summoning fiscal overseers...",
        "Finalizing user sanctum...",
        "Sealing vault with obsidian gate..."
    ]
    print("╔" + "═" * 58 + "╗")
    print("║{:^58}║".format("▓▓▓▓▓▓ LAUNCHING FINANCE TRACKER ▓▓▓▓▓▓"))
    print("╠" + "═" * 58 + "╣")
    for step in steps:
        dots = "." * random.randint(3, 6)
        time.sleep(random.uniform(0.3, 0.6))
        print(f"║ {step:<52}{dots}║")
    print("╚" + "═" * 58 + "╝")
    time.sleep(1)
    input("\nPress Enter to begin...")
