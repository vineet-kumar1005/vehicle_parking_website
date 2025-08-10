from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    try:
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("Admin user already exists")
                return True

            admin = User(username='admin',email='admin@parking.com',full_name='System Administrator',password_hash=generate_password_hash('admin123'),is_admin=True)

            db.session.add(admin)
            db.session.commit()
            print("Yeah - Admin user created")
            print("Username: admin")
            print("Password: admin123")
            return True

    except Exception as e:
        print(f"Error creating admin: {e}")
        return False

if __name__ == "__main__":
    create_admin()