# Movie Ticket Booking System - Web Application

A modern web-based movie ticket booking system built with Flask.

## Features

✓ Browse available movies with details
✓ View showtimes for all screens
✓ Interactive seat selection with visual layout
✓ Real-time booking confirmation
✓ View and manage your bookings
✓ Cancel bookings with refund
✓ Modern, responsive UI with dark theme
✓ Mobile-friendly interface

## Project Structure

```
pythonproject/
├── app.py                 # Flask application and backend logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── movies.html       # Movies listing
│   ├── showtimes.html    # Showtimes listing
│   ├── booking.html      # Booking entry page
│   ├── select_showtime.html  # Select showtime
│   ├── select_seats.html # Seat selection interface
│   ├── confirmation.html # Booking confirmation
│   └── my_bookings.html  # View and manage bookings
└── static/               # Static files
    └── style.css         # Stylesheet
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### 1. Home Page

- Browse the theater information
- Quick access to all main features

### 2. Browse Movies

- View all available movies with:
  - Title and genre
  - Duration
  - Rating

### 3. Check Showtimes

- See all available showtimes
- View movie, screen, time, and seat availability
- Price per ticket

### 4. Book Tickets

1. Enter your Customer ID
2. Select a showtime
3. Choose your seats from the visual layout
4. Review the booking summary
5. Confirm booking
6. Receive booking confirmation with Booking ID

### 5. View My Bookings

- Enter your Customer ID
- View all your confirmed bookings
- See booking details (seats, price, date)
- Option to cancel bookings

## Seat Status Colors

- **Green** (◻): Available seats
- **Red** (✕): Already booked
- **Gray** (█): Blocked seats
- **Gold**: Selected seats

## System Architecture

### Backend (Flask)

- Theater management
- Movie and showtime management
- Booking system with seat tracking
- RESTful API endpoints for booking operations

### Frontend (HTML/CSS/JavaScript)

- Responsive design
- Interactive seat selection
- Real-time price calculation
- Dynamic booking management

## Sample Data

The system comes pre-loaded with:

- **Screens**: 2 theaters with 8x12 and 10x12 seating
- **Movies**: 3 current movies
  - The Last Guardian (Action)
  - Quantum Dreams (Sci-Fi)
  - Love in Paris (Romance)
- **Showtimes**: 4 showtimes across today's schedule

## API Endpoints

- `GET /` - Home page
- `GET /movies` - View all movies
- `GET /showtimes` - View all showtimes
- `GET /booking` - Start booking process
- `POST /booking` - Submit customer ID
- `GET /select-showtime` - Select showtime
- `GET /select-seats/<showtime_id>` - Select seats
- `POST /api/book-tickets` - Book tickets (JSON API)
- `GET /confirmation/<booking_id>` - Booking confirmation
- `GET /my-bookings` - View my bookings
- `POST /api/cancel-booking` - Cancel booking (JSON API)

## Customization

### Add More Movies

Edit `app.py` and modify the initialization section:

```python
theater.add_movie("M4", "Movie Title", "Genre", 120, 8.5)
theater.add_showtime("S1", "M4", datetime_object, 12.99)
```

### Change Seating Layout

Modify the Screen initialization:

```python
theater.add_screen("S3", "Screen 3", rows=10, seats_per_row=14)
```

### Customize Styling

Edit `static/style.css` to change colors, fonts, and layout

## System Requirements

- Python 3.7+
- Flask 2.3.3+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Notes

- All bookings are stored in memory (will be lost on restart)
- For production use, implement database persistence
- Add authentication for customer ID management
- Consider adding payment processing integration

## License

© 2026 CineMax Theater - All rights reserved
