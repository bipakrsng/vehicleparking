from celery import shared_task
from datetime import datetime,timedelta
from ..models.model import *
from sqlalchemy import func
from .mailservice import send_email

import flask_excel as excel

@shared_task #if i keep it True then the result will not going to stored in backend
#shared task decorator skip the celery instance
def download_csv_closed_request(user_id):
    reservations = ReserveParkingSpot.query \
    .join(ParkingSpot, ReserveParkingSpot.parking_spot_id == ParkingSpot.id) \
    .join(ParkingLot, ParkingSpot.parking_lot_id == ParkingLot.id) \
    .with_entities(
        func.date(ReserveParkingSpot.parking_timestamp).label('arrival_date'),
        func.time(ReserveParkingSpot.parking_timestamp).label('arrival_time'),
        func.date(ReserveParkingSpot.leaving_timestamp).label('leave_date'),
        func.time(ReserveParkingSpot.leaving_timestamp).label('leave_time'),
        ReserveParkingSpot.parking_cost.label('total_cost'),
        ParkingLot.price.label('price_per_hour'),
        ParkingLot.prime_location_name,
        ParkingLot.address_line1,
        ParkingLot.address_lin2,
        ParkingLot.city,
        ParkingLot.state,
        ParkingLot.country,
        ParkingLot.pincode
    ).all()

    csv_output = excel.make_response_from_query_sets(reservations,
        column_names=[
            'Arrival Date',
            'Arrival Time',
            'Leave Date',
            'Leave Time',
            'Total Cost',
            'Price Per Hour',
            'Prime Location Name',
            'Address Line 1',
            'Address Line 2',
            'City',
            'State',
            'Country',
            'Pincode'
        ],
        file_name=f'closed_requests_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        response_type='csv',
        allow_zip=False,
        encoding='utf-8'
    )
    return csv_output #whatever got returned will be stored in backend
#here only filename is being stored not whole data


@shared_task() 
def daily_reminder(message):
    cutoff_time_1 = datetime.now() - timedelta(days=1)

    time_diff = timedelta(hours=5,minutes=30)

    cutoff_time = cutoff_time_1 + time_diff

    user_all = User.query.all()

    for user in user_all:
        if user.last_login_at:
            if isinstance(user.last_login_at,str):
                last_login_at = datetime.strptime(user.last_login_at, '%Y-%m-%d %H:%M:%S')
            else:
                last_login_at = user.last_login_at
            
            if last_login_at < cutoff_time:
                print(f"Sending reminder to {user.email} for inactivity.")
                # Here you can call your email sending function
                # send_email(subject="Reminder", recipient=user.email, body=message)
                subject = "Reminder: Inactivity Alert"
                body = f'Hey {user.first_name},\n\nThis is a reminder that you have not logged in for over 24 hours. Please log in to your account to continue using our services.\n\nBest regards,\nYour Team'

                html_body = f'<p>Hey {user.first_name},</p><p>{message}</p><p>Best regards,<br>Your Team</p>'

                send_email(subject, recipient='21f3001496@ds.study.iitm.ac.in', body=body, html_body=html_body)


