from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Admin, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'myfirstwebsite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Try logging in.", "error")
            return redirect(url_for('register'))
        
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Username already taken. Choose another.", "error")
            return redirect(url_for('register'))

        new_user = User(
            full_name=full_name, 
            email=email, 
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):  # ← password_hash
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid email or password", "error")
    
    return render_template('login.html')


@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    parking_lots = ParkingLot.query.all()
    active_reservations = Reservation.query.filter_by(user_id=user.id, status='active').all()

    return render_template('user_dashboard.html',user=user,parking_lots=parking_lots,active_reservations=active_reservations)

@app.route('/book_parking/<int:lot_id>', methods=['GET', 'POST'])
def book_parking(lot_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if not available_spot:
            flash("No available spots in this parking lot!", "error")
            return redirect(url_for('user_dashboard'))

        new_reservation = Reservation(
            user_id=session['user_id'],
            spot_id=available_spot.id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now()
        )
        available_spot.status = 'O'
        db.session.add(new_reservation)
        db.session.commit()
        flash("Parking spot booked successfully!", "success")
        return redirect(url_for('user_dashboard'))
    
    return render_template('book_parking.html', lot=lot)

@app.route('/release_parking/<int:reservation_id>')
def release_parking(reservation_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id != session['user_id']:
        flash("Unauthorized access!", "error")
        return redirect(url_for('user_dashboard'))
    
    if reservation.leaving_timestamp is None:
        reservation.leaving_timestamp = datetime.now()
        duration = reservation.leaving_timestamp - reservation.parking_timestamp
        hours = duration.total_seconds() / 3600
        lot = reservation.spot.lot
        cost = hours * lot.price_per_hour
        reservation.parking_cost = round(cost, 2)
        reservation.status = 'completed'
        reservation.spot.status = 'A'
        
        db.session.commit()
        flash(f"Parking released! Total cost: ₹{reservation.parking_cost}", "success")
    
    return redirect(url_for('user_dashboard'))

@app.route('/user/history')
def user_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.parking_timestamp.desc()).all()
    return render_template('user_history.html', user=user, reservations=reservations)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = User.query.filter_by(username=username, is_admin=True).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials", "error")
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    parking_lots = ParkingLot.query.all()
    total_users = User.query.count()
    total_reservations = Reservation.query.count()
    active_reservations = Reservation.query.filter_by(status='active').count()
    return render_template('admin_dashboard.html',parking_lots=parking_lots,total_users=total_users,total_reservations=total_reservations,active_reservations=active_reservations)

@app.route('/admin/add_lot', methods=['GET', 'POST'])
def admin_add_lot():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        prime_location_name = request.form['prime_location_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        price_per_hour = float(request.form['price_per_hour'])
        maximum_number_of_spots = int(request.form['maximum_number_of_spots'])

        new_lot = ParkingLot(prime_location_name=prime_location_name,address=address,pin_code=pin_code,price_per_hour=price_per_hour,maximum_number_of_spots=maximum_number_of_spots)

        db.session.add(new_lot)
        db.session.flush() 
        for i in range(1, maximum_number_of_spots + 1):
            spot = ParkingSpot(lot_id=new_lot.id,spot_number=f"S{i:03d}",status='A')
            db.session.add(spot)
        db.session.commit()
        flash("Parking lot and spots created successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_lot.html')

@app.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def admin_edit_lot(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.prime_location_name = request.form['prime_location_name']
        lot.address = request.form['address']
        lot.pin_code = request.form['pin_code']
        lot.price_per_hour = float(request.form['price_per_hour'])

        new_max_spots = int(request.form['maximum_number_of_spots'])
        current_spots = len(lot.spots)

        if new_max_spots > current_spots:
            for i in range(current_spots + 1, new_max_spots + 1):
                spot = ParkingSpot(lot_id=lot.id,spot_number=f"S{i:03d}",status='A')
                db.session.add(spot)
        elif new_max_spots < current_spots:
            spots_to_remove = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').limit(current_spots - new_max_spots).all()
            for spot in spots_to_remove:
                db.session.delete(spot)
        lot.maximum_number_of_spots = new_max_spots
        db.session.commit()
        flash("Parking lot updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit_lot.html', lot=lot)

@app.route('/admin/delete_lot/<int:lot_id>')
def admin_delete_lot(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied_spots > 0:
        flash("Cannot delete lot with occupied spots!", "error")
        return redirect(url_for('admin_dashboard'))
    db.session.delete(lot)
    db.session.commit()
    flash("Parking lot deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_spots/<int:lot_id>')
def admin_view_spots(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    return render_template('admin_view_spots.html', lot=lot, spots=spots)

@app.route('/admin/users')
def admin_view_users():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    users = User.query.all()
    return render_template('admin_view_users.html', users=users)

@app.route('/admin/reservations')
def admin_view_reservations():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    reservations = Reservation.query.order_by(Reservation.parking_timestamp.desc()).all()
    return render_template('admin_view_reservations.html', reservations=reservations)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash("Admin logged out successfully!", "success")
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)