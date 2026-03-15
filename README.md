# Pompom House

PomPom House is a student accommodation platform designed to connect landlords with international students. It provides a responsive and secure booking experience.

## Core Features

* **Custom Email Authentication:** Bypasses default Django username login, allowing users to register and log in securely using their university `.ac.uk` email addresses.
* **Interactive Booking Workflow:** Uses AJAX to handle asynchronous booking requests (approve/reject/cancel) without requiring full page reloads.
* **Property Mapping:** Integrates the Google Maps JavaScript API with lazy loading to dynamically plot exact property locations.
* **Secure Sandbox Payments:** Incorporates the Stripe API to handle deposit payments externally, ensuring sensitive financial data is never stored on the local server.
* **Production-Ready & Accessible:** Built with a fully responsive pure CSS Flexbox/Grid layout (no Bootstrap). Deployed using Gunicorn and WhiteNoise for static asset optimization, and strictly adheres to WCAG 2.2 accessibility standards.

## Project Technology

* **Backend:** Python, Django 
* **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript, AJAX
* **External APIs:** Stripe Checkout API, Google Maps API
* **Deployment & Testing:** Gunicorn, WhiteNoise, Django `TestCase`

## Instructions

Follow these steps to run the PomPom House project on your local machine.

### 1. Prerequisites
Ensure you have Python 3.10 installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Application
```bash
python manage.py runserver
```

### 5. Running Tests
The project includes an automated test suite covering database models, view rendering, and access control. To run the tests, execute:
```bash
python manage.py test
```
