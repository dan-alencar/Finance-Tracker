from FinanceTracker.core.balance import get_balance, set_balance, add_to_balance, subtract_from_balance, format_brl
from FinanceTracker.interface.animations import clear_screen, print_frame, print_menu, menu_transition, color

def launch_cli(user):
    while True:
        clear_screen()
        print_frame(f"{user.first_name} {user.last_name}")
        print_menu([
            "Check current balance",
            "Set current balance",
            "Add/Subtract value",
            "Set current income",
            "Add installment payment",
            "Remove installment payment",
            "Add monthly payment",
            "Remove monthly payment",
            "Add investment",
            "Remove investment",
            "Exit"
        ])

        try:
            choice = int(input(color("\nEnter your choice: ", fg="yellow", bold=True)).strip())
        except ValueError:
            menu_transition("Invalid Input", ["❌ Invalid input. Please try again."])
            continue

        try:
            if choice == 1:
                current = get_balance(user.user_id)
                menu_transition("Current Balance", [f"💰 Balance: {format_brl(current)}"])

            elif choice == 2:
                value = float(input("Enter new balance (R$): ").replace(",", "."))
                set_balance(user.user_id, value)
                menu_transition("Balance Updated", ["✅ Balance updated successfully."])

            elif choice == 3:
                value = float(input("Enter value (positive to add, negative to subtract): ").replace(",", "."))
                if value >= 0:
                    add_to_balance(user.user_id, value)
                    menu_transition("Balance Increased", [f"➕ Added {format_brl(value)} to balance."])
                else:
                    subtract_from_balance(user.user_id, -value)
                    menu_transition("Balance Decreased", [f"➖ Subtracted {format_brl(-value)} from balance."])

            elif choice == 11:
                menu_transition("Goodbye", ["👋 Farewell, dwarf accountant."], pause=False)
                break
            else:
                menu_transition("Not Implemented", ["[TODO] This option is not yet implemented."])

        except ValueError as e:
            menu_transition("Error", [f"❌ {str(e)}"])