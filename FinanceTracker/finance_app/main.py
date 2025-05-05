from FinanceTracker.interface.cli import launch_cli
from FinanceTracker.core.session import init_app_session

def main():
    user = init_app_session()
    if user:
        launch_cli(user)
    else:
        print("❌ Failed to initialize session.")

if __name__ == "__main__":
    main()
