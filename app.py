"""
CineMax Theater Booking System - Simple JSON-based Application
Flask + JSON Data Storage
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import logging
import os
import json
from pathlib import Path

import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=str(config.TEMPLATES_DIR),
    static_folder=str(config.STATIC_DIR)
)

# Configure app
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

logger.info("Application initialized successfully")


# ============================================================================
# DATA STORAGE - JSON FILE MANAGEMENT
# ============================================================================

DATA_FILE = Path(config.BASE_DIR) / 'data' / 'bookings.json'
MOVIES_FILE = Path(config.BASE_DIR) / 'data' / 'movies.json'
SHOWTIMES_FILE = Path(config.BASE_DIR) / 'data' / 'showtimes.json'


def load_json(filepath):
    """Load data from JSON file"""
    try:
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
    return {}


def save_json(filepath, data):
    """Save data to JSON file"""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving {filepath}: {e}")


def init_data():
    """Initialize sample data if files don't exist"""
    
    # Sample movies
    if not MOVIES_FILE.exists():
        movies = {
            "movies": [
                {
                    "id": "M1",
                    "title": "The Last Guardian",
                    "description": "An action-packed thriller",
                    "genre": "Action",
                    "duration": 148,
                    "rating": 8.5,
                    "poster_url": "/static/images/last.jfif"
                },
                {
                    "id": "M2",
                    "title": "Quantum Dreams",
                    "description": "A mind-bending sci-fi adventure",
                    "genre": "Sci-Fi",
                    "duration": 156,
                    "rating": 8.2,
                    "poster_url": "/static/images/quantam.jpg"
                },
                {
                    "id": "M3",
                    "title": "Love in Paris",
                    "description": "A romantic journey through the city of lights",
                    "genre": "Romance",
                    "duration": 120,
                    "rating": 7.8,
                    "poster_url": "/static/images/love.jfif"
                }
            ]
        }
        save_json(MOVIES_FILE, movies)
        logger.info("Movies file created with sample data")
    
    # Sample showtimes and screens
    if not SHOWTIMES_FILE.exists():
        today = datetime.now().strftime('%Y-%m-%d')
        showtimes = {
            "screens": [
                {"id": "S1", "number": 1, "name": "Screen 1", "rows": 8, "seats_per_row": 12},
                {"id": "S2", "number": 2, "name": "Screen 2", "rows": 10, "seats_per_row": 12}
            ],
            "showtimes": [
                {
                    "id": "ST1",
                    "movie_id": "M1",
                    "screen_id": "S1",
                    "date": today,
                    "start_time": "18:00",
                    "price": 12.99
                },
                {
                    "id": "ST2",
                    "movie_id": "M1",
                    "screen_id": "S1",
                    "date": today,
                    "start_time": "21:00",
                    "price": 14.99
                },
                {
                    "id": "ST3",
                    "movie_id": "M2",
                    "screen_id": "S2",
                    "date": today,
                    "start_time": "19:00",
                    "price": 14.99
                },
                {
                    "id": "ST4",
                    "movie_id": "M3",
                    "screen_id": "S2",
                    "date": today,
                    "start_time": "20:00",
                    "price": 10.99
                }
            ]
        }
        save_json(SHOWTIMES_FILE, showtimes)
        logger.info("Showtimes file created with sample data")
    
    # Initialize bookings file if empty
    if not DATA_FILE.exists():
        bookings_data = {
            "bookings": {},
            "customers": {},
            "last_booking_id": 0
        }
        save_json(DATA_FILE, bookings_data)
        logger.info("Bookings file initialized")


# ============================================================================
# ROUTES - PUBLIC PAGES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    bookings_data = load_json(DATA_FILE)
    total_bookings = len([b for b in bookings_data.get('bookings', {}).values() 
                         if b.get('status') == 'confirmed'])
    movies_data = load_json(MOVIES_FILE)
    total_movies = len(movies_data.get('movies', []))
    total_revenue = sum([b.get('total_price', 0) for b in bookings_data.get('bookings', {}).values()])
    
    return render_template('index.html',
                         theater_name=config.THEATER_NAME,
                         total_bookings=total_bookings,
                         total_movies=total_movies,
                         total_revenue=f"${total_revenue:.2f}")


@app.route('/movies')
def movies_list():
    """Movies listing page"""
    movies_data = load_json(MOVIES_FILE)
    movies = movies_data.get('movies', [])
    return render_template('movies.html', movies=movies)


@app.route('/showtimes')
def showtimes_list():
    """Showtimes listing page"""
    showtimes_data = load_json(SHOWTIMES_FILE)
    movies_data = load_json(MOVIES_FILE)
    
    # Enrich showtimes with movie titles
    movies_map = {m['id']: m['title'] for m in movies_data.get('movies', [])}
    showtimes = showtimes_data.get('showtimes', [])
    for st in showtimes:
        st['movie_title'] = movies_map.get(st.get('movie_id'), 'Unknown')
    
    return render_template('showtimes.html', showtimes=showtimes)


@app.route('/booking', methods=['GET', 'POST'])
def booking_start():
    """Start booking - customer info"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        if not email or not name:
            return jsonify({'success': False, 'message': 'Email and name required'}), 400
        
        # Store customer info in session
        session['customer'] = {
            'email': email,
            'name': name,
            'phone': phone
        }
        
        return redirect(url_for('select_showtime'))
    
    return render_template('booking.html')


@app.route('/select-showtime')
def select_showtime():
    """Select showtime"""
    if 'customer' not in session:
        return redirect(url_for('booking_start'))
    
    showtimes_data = load_json(SHOWTIMES_FILE)
    movies_data = load_json(MOVIES_FILE)
    
    # Enrich showtimes with movie and screen info
    movies_map = {m['id']: m for m in movies_data.get('movies', [])}
    screens_map = {s['id']: s for s in showtimes_data.get('screens', [])}
    
    showtimes = []
    for st in showtimes_data.get('showtimes', []):
        movie = movies_map.get(st.get('movie_id'), {})
        screen = screens_map.get(st.get('screen_id'), {})
        showtimes.append({
            **st,
            'movie_title': movie.get('title', 'Unknown'),
            'movie_duration': movie.get('duration', 0),
            'screen_name': screen.get('name', 'Unknown'),
            'full_datetime': f"{st.get('date')} {st.get('start_time')}"
        })
    
    return render_template('select_showtime.html',
                         showtimes=showtimes,
                         customer=session.get('customer'))


@app.route('/select-seats/<showtime_id>')
def select_seats(showtime_id):
    """Select seats"""
    if 'customer' not in session:
        return redirect(url_for('booking_start'))
    
    showtimes_data = load_json(SHOWTIMES_FILE)
    movies_data = load_json(MOVIES_FILE)
    
    # Find showtime
    showtime = None
    for st in showtimes_data.get('showtimes', []):
        if st['id'] == showtime_id:
            showtime = st
            break
    
    if not showtime:
        return redirect(url_for('movies_list'))
    
    # Find movie and screen info
    movies_map = {m['id']: m for m in movies_data.get('movies', [])}
    screens_map = {s['id']: s for s in showtimes_data.get('screens', [])}
    
    movie = movies_map.get(showtime['movie_id'], {})
    screen = screens_map.get(showtime['screen_id'], {})
    
    # Load bookings to find occupied seats
    bookings_data = load_json(DATA_FILE)
    booked_seats = set()
    for booking in bookings_data.get('bookings', {}).values():
        if booking.get('showtime_id') == showtime_id and booking.get('status') == 'confirmed':
            booked_seats.update(booking.get('seats', []))
    
    # Generate seats
    seats_by_row = {}
    for row_num in range(screen.get('rows', 8)):
        row_char = chr(65 + row_num)  # A, B, C, etc.
        seats_by_row[row_char] = []
        for seat_num in range(1, screen.get('seats_per_row', 12) + 1):
            seat_id = f"{row_char}{seat_num}"
            status = 'booked' if seat_id in booked_seats else 'available'
            seats_by_row[row_char].append({
                'row': row_char,
                'number': seat_num,
                'seat_id': seat_id,
                'status': status
            })
    
    return render_template('select_seats.html',
                         showtime_id=showtime_id,
                         movie_title=movie.get('title', 'Unknown'),
                         screen_name=screen.get('name', 'Unknown'),
                         start_time=f"{showtime.get('date')} {showtime.get('start_time')}",
                         price_per_seat=showtime.get('price', 0),
                         seats=seats_by_row,
                         customer=session.get('customer'))


# ============================================================================
# API ROUTES - BOOKING
# ============================================================================

@app.route('/api/book-tickets', methods=['POST'])
def api_book_tickets():
    """Create a booking"""
    try:
        data = request.json
        showtime_id = data.get('showtime_id')
        seat_ids = data.get('seats', [])
        
        if not showtime_id or not seat_ids or 'customer' not in session:
            return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
        # Load all data
        bookings_data = load_json(DATA_FILE)
        showtimes_data = load_json(SHOWTIMES_FILE)
        movies_data = load_json(MOVIES_FILE)
        
        # Find showtime
        showtime = None
        for st in showtimes_data.get('showtimes', []):
            if st['id'] == showtime_id:
                showtime = st
                break
        
        if not showtime:
            return jsonify({'success': False, 'message': 'Invalid showtime'}), 404
        
        # Check if seats are already booked
        booked_seats = set()
        for b in bookings_data.get('bookings', {}).values():
            if b.get('showtime_id') == showtime_id and b.get('status') == 'confirmed':
                booked_seats.update(b.get('seats', []))
        
        overlapping_seats = [s for s in seat_ids if s in booked_seats]
        if overlapping_seats:
            return jsonify({
                'success': False,
                'message': f"One or more seats are already booked: {', '.join(overlapping_seats)}"
            }), 400
        
        # Find movie
        movies_map = {m['id']: m for m in movies_data.get('movies', [])}
        movie = movies_map.get(showtime['movie_id'], {})
        
        # Create booking
        booking_id = f"BK{bookings_data.get('last_booking_id', 0) + 1}"
        bookings_data['last_booking_id'] = int(booking_id[2:])
        
        total_price = len(seat_ids) * showtime.get('price', 0)
        
        booking = {
            'booking_id': booking_id,
            'customer_email': session['customer'].get('email'),
            'customer_name': session['customer'].get('name'),
            'movie_title': movie.get('title', 'Unknown'),
            'showtime_id': showtime_id,
            'seats': seat_ids,
            'total_price': total_price,
            'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'confirmed'
        }
        
        bookings_data['bookings'][booking_id] = booking
        save_json(DATA_FILE, bookings_data)
        
        logger.info(f"Booking created: {booking_id}")
        
        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'booking_number': booking_id,
            'total_price': total_price
        })
    
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        return jsonify({'success': False, 'message': 'Booking failed'}), 500


@app.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    """Booking confirmation page"""
    bookings_data = load_json(DATA_FILE)
    booking = bookings_data.get('bookings', {}).get(booking_id)
    
    if not booking:
        return redirect(url_for('index'))
    
    session.pop('customer', None)
    return render_template('confirmation.html', booking=booking)


@app.route('/my-bookings', methods=['GET', 'POST'])
def my_bookings():
    """View customer bookings"""
    bookings_list = []
    customer = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            bookings_data = load_json(DATA_FILE)
            customer_bookings = [b for b in bookings_data.get('bookings', {}).values()
                               if b.get('customer_email') == email]
            if customer_bookings:
                customer = {'email': email}
                bookings_list = customer_bookings
    
    return render_template('my_bookings.html', bookings=bookings_list, customer=customer)


@app.route('/api/cancel-booking', methods=['POST'])
def api_cancel_booking():
    """Cancel a booking"""
    try:
        data = request.json
        booking_id = data.get('booking_id')
        
        bookings_data = load_json(DATA_FILE)
        booking = bookings_data.get('bookings', {}).get(booking_id)
        
        if not booking:
            return jsonify({'success': False, 'message': 'Booking not found'}), 404
        
        booking['status'] = 'cancelled'
        save_json(DATA_FILE, bookings_data)
        
        logger.info(f"Booking cancelled: {booking_id}")
        
        return jsonify({'success': True, 'message': 'Booking cancelled'})
    
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        return jsonify({'success': False, 'message': 'Cancellation failed'}), 500


@app.route('/api/statistics')
def api_statistics():
    """Get system statistics"""
    try:
        bookings_data = load_json(DATA_FILE)
        movies_data = load_json(MOVIES_FILE)
        
        bookings = bookings_data.get('bookings', {}).values()
        total_bookings = len([b for b in bookings if b.get('status') == 'confirmed'])
        total_revenue = sum([b.get('total_price', 0) for b in bookings])
        total_movies = len(movies_data.get('movies', []))
        total_seats_sold = sum([len(b.get('seats', [])) for b in bookings])
        
        return jsonify({
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue),
            'total_movies': total_movies,
            'total_seats_sold': total_seats_sold,
            'average_booking_value': float(total_revenue / total_bookings) if total_bookings > 0 else 0
        })
    
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# REQUEST/RESPONSE LOGGING
# ============================================================================

@app.before_request
def log_request():
    """Log incoming requests"""
    logger.debug(f"{request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.debug(f"Response: {response.status_code}")
    return response


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    try:
        logger.info("=" * 70)
        logger.info("Starting CineMax Theater Booking System")
        logger.info("=" * 70)
        logger.info(f"Base Directory: {config.BASE_DIR}")
        logger.info(f"Templates: {config.TEMPLATES_DIR.exists()}")
        logger.info(f"Static: {config.STATIC_DIR.exists()}")
        logger.info(f"Data Storage: JSON Files")
        logger.info(f"Server: http://{config.HOST}:{config.PORT}")
        logger.info(f"Debug: {config.DEBUG}")
        logger.info("=" * 70)
        logger.info("Press Ctrl+C to stop the server")
        logger.info("=" * 70)
        
        # Initialize data files
        init_data()
        
        # Run application
        app.run(
            debug=config.DEBUG,
            host=config.HOST,
            port=config.PORT,
            use_reloader=True,
            threaded=config.THREADED
        )
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        raise
