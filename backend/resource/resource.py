from flask_restful import Resource,Api,reqparse,marshal_with,fields,marshal
from backend.models.model import *
from flask import request,jsonify,g,make_response
from datetime import datetime,timedelta
from werkzeug.security import check_password_hash,generate_password_hash
import jwt
from sqlalchemy.exc import IntegrityError
from functools import wraps
from config import DevelopmentConfig
import re
import uuid

api = Api(prefix='/api')


def create_token(user):
    payload = { 
        'user_id' : user.id ,
        'email': user.email,
        'role': user.roles[0].name if user.roles else None,
        'exp': datetime.utcnow() + timedelta(days=1)
        }
    token = jwt.encode(payload,DevelopmentConfig.SECRET_KEY,algorithm='HS256')
    return token

def token_required(roles=[]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None

            # Check Authorization header for Bearer token
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

            if not token:
                return {'message': 'Token is missing!'}, 401

            try:
                payload = jwt.decode(token, DevelopmentConfig.SECRET_KEY, algorithms=['HS256'])

                if roles and payload.get('role') not in roles:
                    return jsonify({'message': 'You do not have permission to access this resource based on roles'}), 403

                request.user = payload  # attach user info to request object

            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',type=str,required= True,help='Email is required') #email syntax verified
        parser.add_argument('password',type=str,required=True,help='Password is required')

        args = parser.parse_args() # now args is dictionary having email and password as keys
        email = args['email']
        password = args['password']

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return {'message': 'Invalid email format'}, 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {'message': 'User not found'}, 404

        if check_password_hash(user.password,password):

            utcnow = datetime.utcnow()
            time_diff = timedelta(hours=5,minutes=30)  # Adjust for IST (UTC+5:30)
            istnow = utcnow + time_diff
            user.last_login_at = istnow
            token = create_token(user)
            
            db.session.commit()
            
            return {'token':token},200
        else:
            return {'message': 'Invalid password'}, 401


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        # ----------- arguments -----------
        parser.add_argument('first_name',      type=str,   required=True, help='First name is required')
        parser.add_argument('last_name',       type=str,   required=True, help='Last name is required')
        parser.add_argument('email',           type=str,   required=True, help='Email is required')
        parser.add_argument('password',        type=str,   required=True, help='Password is required')
        parser.add_argument('address_line1',   type=str,   required=True, help='Address Line 1 is required')
        parser.add_argument('address_line2',   type=str)
        parser.add_argument('city',            type=str,   required=True)
        parser.add_argument('state',           type=str,   required=True)
        parser.add_argument('country',         type=str,   required=True)
        parser.add_argument('pincode',         type=str)
        parser.add_argument('phone_number',    type=str)
        parser.add_argument('gender',          type=str)
        parser.add_argument('date_of_birth',   type=str)
        parser.add_argument('username',        type=str,   required=True, help='Username is required')

        args = parser.parse_args()

        # ----------- basic validation -----------
        email    = args['email']
        username = args['username']

        # email format
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            return {'error': 'Invalid email format'}, 400

        # date parsing
        try:
            dob = datetime.strptime(args['date_of_birth'], '%Y-%m-%d').date() if args['date_of_birth'] else None
        except ValueError:
            return {'error': 'Date of Birth must be YYYY-MM-DD'}, 400

        # ----------- create user object -----------
        new_user = User(
            email=email,
            username=username,
            first_name=args['first_name'],
            last_name=args['last_name'],
            password=generate_password_hash(args['password']),
            active=True,
            address_line1=args['address_line1'],
            address_line2=args.get('address_line2', ''),
            city=args['city'],
            state=args['state'],
            country=args['country'],
            pincode=args['pincode'],
            phone_number=args['phone_number'],
            gender=args['gender'],
            date_of_birth=dob,
            fs_uniquifier=str(uuid.uuid4())
        )
        # ----------- role assignment (default to 'user') -----------
        user_role = Role.query.filter_by(name='user').first()

        new_user.roles.append(user_role)

        

        # ----------- DB commit with safety net -----------
        try:
            db.session.add(new_user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()

            # Detect which unique constraint failed
            if 'email' in str(e.orig):
                return {'error': 'Email is already registered'}, 409
            if 'username' in str(e.orig):
                return {'error': 'Username is already taken'}, 409
            return {'error': 'Integrity error'}, 400

        except Exception as e:
            db.session.rollback()
            return {'error': 'Server error'}, 500

        # ----------- success -----------
        return {
            'message': 'User registered successfully'
        }, 201

class CreateParkingLot(Resource):
    
    @token_required(roles=['admin'])   # ✅ guard every HTTP verb
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument('prime_location_name', type=str,  required=True, help='Prime location name is required')
        parser.add_argument('price',               type=float, required=True, help='Price must be a number')
        parser.add_argument('address_line1',       type=str,  required=True, help='Address Line 1 is required')
        parser.add_argument('address_lin2',        type=str)
        parser.add_argument('city',                type=str,  required=True)
        parser.add_argument('state',               type=str,  required=True)
        parser.add_argument('country',             type=str,  required=True)
        parser.add_argument('pincode',             type=str,  required=True)
        parser.add_argument('number_of_spot',      type=int,  required=True, help='Number of spots must be integer')

        args = parser.parse_args()

        # ---------- extra business validations ----------
        if args['price'] < 0:
            return {'error': 'Price cannot be negative'}, 400

        if args['number_of_spot'] < 0:
            return {'error': 'Number of spots cannot be negative'}, 400

        # Optional: prevent duplicate location per city
        dup = ParkingLot.query.filter_by(
            prime_location_name=args['prime_location_name'],
            city=args['city']
        ).first()
        if dup:
            return {'error': 'A parking lot with this name already exists in that city'}, 409

        # ---------- create new parking‑lot ----------
        try:
            lot = ParkingLot(
            prime_location_name=args['prime_location_name'],
            price=args['price'],
            address_line1=args['address_line1'],
            address_lin2=args.get('address_lin2', ''),
            city=args['city'],
            state=args['state'],
            country=args['country'],
            pincode=args['pincode'],
            number_of_spot=args['number_of_spot']
        )

        
            db.session.add(lot)
            db.session.flush()

            #creating parking spots
            for _ in range(args['number_of_spot']):
                spot = ParkingSpot(
                    parking_lot_id=lot.id,
                    status='available'
                )
                db.session.add(spot)
            db.session.commit()
            return {'message': 'Parking lot with spot created successfully'}, 201

        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'DB integrity error'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'Server error'}, 500

         

class ParkingLotsWithSpots(Resource):
    @token_required(roles=['admin'])  # Allow both admin roles
    def get(self):
        lots = ParkingLot.query.filter_by(deleted_at=None).all()
        if not lots:
            return {'message': 'No parking lots found'}, 404
        result = []

        for lot in lots:
            # Fetch spots for this lot
            spots = ParkingSpot.query.filter_by(parking_lot_id=lot.id).all()
            spot_data = [
                {
                    'id': spot.id,
                    'status': spot.status
                } for spot in spots
            ]

            # Add lot + its spots to the result
            result.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address_line1': lot.address_line1,
                'address_lin2': lot.address_lin2,
                'city': lot.city,
                'state': lot.state,
                'country': lot.country,
                'pincode': lot.pincode,
                'number_of_spot': lot.number_of_spot,
                'spots': spot_data
            })

        return result, 200
    
class ParkingLotDetail(Resource):
    @token_required(roles=['admin'])  # Allow only admin roles
    def get(self, lot_id):
        lot = ParkingLot.query.filter_by(id=lot_id, deleted_at=None).first()
        if not lot:
            return {"error": "Parking lot not found"}, 404

        return {
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price": lot.price,
            "address_line1": lot.address_line1,
            "address_lin2": lot.address_lin2,
            "city": lot.city,
            "state": lot.state,
            "country": lot.country,
            "pincode": lot.pincode
        }, 200

    @token_required(roles=['admin'])  # Allow only admin roles
    def put(self, lot_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("prime_location_name", type=str)
        parser.add_argument("price", type=float)
        parser.add_argument("address_line1", type=str)
        parser.add_argument("address_lin2", type=str)
        parser.add_argument("city", type=str)
        parser.add_argument("state", type=str)
        parser.add_argument("country", type=str)
        parser.add_argument("pincode", type=str)
        args = parser.parse_args()

        lot = ParkingLot.query.filter_by(id=lot_id, deleted_at=None).first()
        if not lot:
            return {"error": "Parking lot not found"}, 404

        for key, value in args.items():
            if value is not None:
                setattr(lot, key, value)

        try:
            db.session.commit()
            return {"message": "Parking lot updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
# -------------------- DELETE (soft‑delete) --------------------
class ParkingLotDelete(Resource):
    method_decorators = [token_required(roles=['admin'])]

    def delete(self, lot_id):
        lot = ParkingLot.query.filter_by(id=lot_id, deleted_at=None).first()
        if not lot:
            return {'error': 'Parking lot not found'}, 404

        # block delete if any spot occupied
        occupied = ParkingSpot.query.filter_by(
            parking_lot_id=lot.id, status='occupied'
        ).first()
        if occupied:
            return {'error': 'Lot has occupied spots; cannot delete'}, 409

        try:
            lot.deleted_at = datetime.utcnow()   # soft delete
            db.session.commit()
            return {'message': 'Parking lot soft‑deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'active': fields.Boolean,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
}
class UserListResource(Resource):
    @token_required(roles=['admin'])  # Allow only admin roles
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users  # marshaled automatically
    

class UserActivationResource(Resource):
    method_decorators = [token_required(roles=['admin'])]  # protect all PATCH methods

    def patch(self, user_id, action):
        """
        PATCH /api/users/<user_id>/<action>
        where <action> is 'activate' or 'deactivate'
        """
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Decide the new status
        if action == 'activate':
            new_status = True
        elif action == 'deactivate':
            new_status = False
        else:
            return {'message': 'Invalid action'}, 400

        # If status already matches, no DB write needed
        if user.active == new_status:
            return {
                'message': f'User is already {"active" if new_status else "inactive"}',
                'id': user.id,
                'active': user.active
            }, 200

        # Update active flag
        try:
            user.active = new_status
            db.session.commit()
            return {
                'message': f'User successfully {"activated" if new_status else "deactivated"}',
                'id': user.id,
                'active': user.active
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Database error', 'details': str(e)}, 500

user_detail_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'phone_number': fields.String,
    'address_line1': fields.String,
    'address_line2': fields.String,
    'city': fields.String,
    'state': fields.String,
    'country': fields.String,
    'pincode': fields.String,
    'gender': fields.String,
    'date_of_birth': fields.DateTime(dt_format='iso8601'),
    'active': fields.Boolean,
    'role': fields.String(attribute=lambda u: u.roles[0].name if u.roles else None)
}

# ---------------- PATCH argument parser -----------------
patch_parser = reqparse.RequestParser()
editable_fields = [
    'first_name', 'last_name', 'phone_number',
    'address_line1', 'address_line2', 'city',
    'state', 'country', 'pincode',
    'gender', 'date_of_birth',
    'active',            # admin/super_admin only
    'role',              # super_admin only
    'new_password'
]
for f in editable_fields:
    patch_parser.add_argument(f)

# ---------------- Resource ------------------------------
class UserDetailResource(Resource):
    @token_required(roles=['admin','user'])  # token required for both GET and PATCH

    # ---------- GET (prefill the form) ----------
    @marshal_with(user_detail_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user

    # ---------- PATCH (save changes) ------------
    @token_required(roles=['admin', 'user'])  # allow user to edit own profile
    def patch(self, user_id):
        payload = getattr(request, "user")  # set by token_required
        logged_in_id = payload.get('user_id')
        caller_role   = payload.get('role')
        print(f"Caller role: {caller_role}, User ID: {user_id}, Logged in ID: {logged_in_id}")

        if caller_role not in ('user', 'admin', 'super_admin'):
            return {'message': 'Role not allowed'}, 403

        target = User.query.get(user_id)
        if not target:
            return {'message': 'User not found'}, 404

        args = patch_parser.parse_args()
        updated_fields = {}

        # ------------ personal editable fields for everyone ------------
        common = [
            'first_name','last_name','phone_number','address_line1',
            'address_line2','city','state','country','pincode',
            'gender','date_of_birth'
        ]
        for field in common:
            value = args.get(field)
            if value is not None:
                if field == 'date_of_birth' and value != '':
                    try:
                        value = datetime.fromisoformat(value).date()
                    except ValueError:
                        return {'message': 'Invalid date_of_birth format'}, 400
                updated_fields[field] = value

        # ------------ password (hashed) ------------
        if args.get('new_password'):
            target.password = generate_password_hash(args['new_password'])

        
        # ------------ apply common field updates ------------
        for k, v in updated_fields.items():
            setattr(target, k, v)

        try:
            db.session.commit()
            return {'message': 'Profile updated'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'DB error', 'details': str(e)}, 500     

parking_lot_fields_search = {
    'id': fields.Integer,
    'prime_location_name': fields.String,
    'price': fields.Float,
    'address_line1': fields.String,
    'address_lin2': fields.String,
    'city': fields.String,
    'state': fields.String,
    'country': fields.String,
    'pincode': fields.String,
    'number_of_spot': fields.Integer
}

class ParkingLotSearchByPincode(Resource):
    @token_required(roles=['user'])  # Allow both admin and user roles
    @marshal_with(parking_lot_fields_search)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=False,location='args' )
        args = parser.parse_args()
        query = args.get('q', '')

        lots = ParkingLot.query.filter(ParkingLot.pincode.startswith(query)).all()
        return lots, 200

class LotAvailability(Resource):
    @token_required(roles=['user'])  
    def get(self, lot_id):
        total = db.session.query(ParkingSpot).filter_by(parking_lot_id=lot_id).count()
        available = db.session.query(ParkingSpot).filter_by(parking_lot_id=lot_id, status='available').count()
        return {'total': total, 'available': available}, 200

reserve_fields = {
    'id':            fields.Integer,
    'parking_spot_id': fields.Integer,
    'parking_cost':  fields.Float,
    'parking_timestamp': fields.DateTime(dt_format='iso8601'),
    'leaving_timestamp': fields.DateTime(dt_format='iso8601')
}

# ---------- GET free spots ----------
class AvailableSpotsResource(Resource):
    method_decorators = [token_required()]   # logged‑in users only

    def get(self, lot_id):
        spots = ParkingSpot.query.filter_by(
            parking_lot_id=lot_id, status='available'
        ).all()
        return [s.id for s in spots], 200

# ---------- POST book a spot ----------
class ReserveSpotResource(Resource):
    method_decorators = [token_required()]   # need user info

    @marshal_with(reserve_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('parking_spot_id', type=int, required=True)
        args = parser.parse_args()

        spot = ParkingSpot.query.get(args['parking_spot_id'])
        if not spot or spot.status != 'available':
            return {'message': 'Spot unavailable'}, 409

        user_id = getattr(request, 'user')['user_id']

        parking_lot = ParkingLot.query.get(spot.parking_lot_id)
        if not parking_lot:
            return {'message': 'Parking lot not found'}, 404

        # Create reservation
        now = datetime.utcnow()
        reservation = ReserveParkingSpot(
            user_id=user_id,
            parking_spot_id=spot.id,
            parking_timestamp=now,
            leaving_timestamp=None,        # set on checkout
            parking_cost=parking_lot.price  # simple pricing
        )
        try:
            spot.status = 'occupied'
            db.session.add(reservation)
            db.session.commit()
            return reservation, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'DB error', 'details': str(e)}, 500


class UserBookingsResource(Resource):
    @token_required(roles=['user'])  # Custom decorator
    def get(self):
        user_id = request.user['user_id']
        bookings = ReserveParkingSpot.query.filter_by(user_id=user_id).all()

        current = []
        history = []
        

        for booking in bookings:
            spot = ParkingSpot.query.get(booking.parking_spot_id)
            lot = ParkingLot.query.get(spot.parking_lot_id)
            start_time = booking.parking_timestamp
            end_time = booking.leaving_timestamp or datetime.utcnow()

            duration_in_hours = (end_time - start_time).total_seconds() / 3600
            cost = round(duration_in_hours * booking.parking_cost, 2)
            start_time = booking.parking_timestamp
            end_time = booking.leaving_timestamp or datetime.utcnow()
            duration = (end_time - start_time).total_seconds() / 3600
            cost = round(duration * booking.parking_cost, 2)

            item = {
                "id": booking.id,
                "spot_id": spot.id,
                "lot_name": lot.prime_location_name,
                "parking_time": start_time.strftime('%Y-%m-%d %H:%M'),
                "leaving_time": booking.leaving_timestamp.strftime('%Y-%m-%d %H:%M') if booking.leaving_timestamp else None,
                "duration": duration,
                "cost": cost,
                
                
            }

            if booking.leaving_timestamp is None:
                current.append(item)  # Append to list instead of overwrite
            else:
                history.append(item)

        return {"current": current, "history": history,"cost_per_hour": lot.price}, 200


class ReleaseSpotResource(Resource):
    @token_required(roles=['user'])  # Allow only logged-in users
    def post(self, id):
        user_id = request.user['user_id']
        booking = ReserveParkingSpot.query.filter_by(id=id, user_id=user_id).first()

        if not booking:
            return {"message": "Booking not found"}, 404

        if booking.leaving_timestamp:
            return {"message": "Already released"}, 400

        booking.leaving_timestamp = datetime.utcnow()

        # Update spot status to available
        spot = ParkingSpot.query.get(booking.parking_spot_id)
        spot.status = 'available'

        db.session.commit()

        return {"message": "Spot released successfully"}

class ParkingSpotDetails(Resource):
    @token_required(roles=["admin", "user"])  # or just "admin" depending on access control
    def get(self, spot_id):
        spot = ParkingSpot.query.get_or_404(spot_id)
        lot = ParkingLot.query.get_or_404(spot.parking_lot_id)

        parking_info = {
            "id": spot.id,
            "status": spot.status,
            "lot_id": lot.id,
            "lot_location": lot.prime_location_name,
            "price_per_hour": lot.price
        }

        booking_data = None

        # Only get booking if the spot is occupied
        if spot.status == "occupied":
            booking = ReserveParkingSpot.query.filter_by(parking_spot_id=spot.id, leaving_timestamp=None).first()
            if booking:
                start_time = booking.parking_timestamp
                now = datetime.utcnow()
                duration_in_hours = (now - start_time).total_seconds() / 3600
                cost = round(duration_in_hours * lot.price, 2)

                booking_data = {
                    "id": booking.id,
                    "user_id": booking.user_id,
                    "parking_time": start_time.strftime('%Y-%m-%d %H:%M'),
                    "duration_hours": round(duration_in_hours, 2),
                    "cost": cost
                }

        print(f"Parking info: {parking_info}"
              f", Booking data: {booking_data}")
        return {
            "parkingDetails": parking_info,
            "booking": booking_data
        }, 200

class ParkingSummaryUser(Resource):
    @token_required(roles=['user'])  # Allow only admin roles
    def get(self):
        user_id = request.user['user_id']

        # Fetch all reservations made by user
        user_reservations = ReserveParkingSpot.query.filter_by(user_id=user_id).all()

        total = len(user_reservations)
        in_use = 0
        completed = 0

        for res in user_reservations:
            if res.parking_spot and res.parking_spot.status == 'occupied':
                in_use += 1
            else:
                completed += 1

        return {
            'total_bookings': total,
            'in_use': in_use,
            'completed': completed
        }, 200

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(CreateParkingLot, '/create_parking_lot')
api.add_resource(ParkingLotsWithSpots, '/parking_lots_with_spots')
api.add_resource(ParkingLotDetail, '/edit_parking_lot/<int:lot_id>')
api.add_resource(ParkingLotDelete, '/delete_parking_lot/<int:lot_id>')
api.add_resource(UserListResource, '/admin_users')
api.add_resource(UserActivationResource,'/users/<int:user_id>/<string:action>')  # action = activate | deactivate
api.add_resource(UserDetailResource, '/edit_users/<int:user_id>')  # user_id is the target user to edit
api.add_resource(ParkingLotSearchByPincode, '/search_parking_lots')
api.add_resource(LotAvailability, '/lot_availability/<int:lot_id>')
api.add_resource(AvailableSpotsResource,
                 '/lot_available_spots/<int:lot_id>')
api.add_resource(ReserveSpotResource,
                 '/reserve')
api.add_resource(ReleaseSpotResource, '/release/<int:id>')
api.add_resource(UserBookingsResource, '/user/bookings')

api.add_resource(ParkingSpotDetails, '/parking_spot_details/<int:spot_id>')
api.add_resource(ParkingSummaryUser, '/user/parking_summary')