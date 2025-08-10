import subprocess
import sys

def run_command(command, description):
    print(f"\n {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Vehicle Parking App Setup")
    if not run_command("python create_database.py", "Creating database"):
        sys.exit(1)

    if not run_command("python create_admin.py", "Creating admin user"):
        sys.exit(1)

    print("Setup done!")
    print("Database done")
    print("Admin user done")
    print("Admin login credentials:")
    print("Username: admin")
    print("Password: admin123")

if __name__ == "__main__":
    main()