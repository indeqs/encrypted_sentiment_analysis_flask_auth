# Secure Sentiment Analysis System

A Flask web application for analyzing social media sentiment using homomorphic encryption.

## Features

- User authentication (sign up, login, logout)
- Admin dashboard to manage users
- User banning functionality
- Secure data processing using homomorphic encryption

## Project Structure

The application follows a standard Flask project structure:

- `app.py`: Main Flask application
- `templates/`: HTML templates for the application
- `static/`: Static files (CSS, JavaScript, images)
- `instance/`: Instance-specific files, including the SQLite database

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentiment-analysis-app.git
   cd sentiment-analysis-app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Default Admin Credentials

- Username: `admin`
- Password: `admin`

## Development

### Database

The application uses SQLite as the database, which is stored in the `instance` directory. The database schema is automatically created when the application is first run.

### Adding New Features

To add the actual sentiment analysis functionality, you would need to:

1. Implement the homomorphic encryption module for processing encrypted data
2. Add NLP functionality for analyzing Facebook comments and Twitter tweets
3. Implement the Naive Bayes algorithm for sentiment classification
4. Create data visualization components for the reports

## Security Considerations

- The admin credentials should be changed in a production environment
- Consider implementing additional security measures, such as:
  - Rate limiting
  - CSRF protection
  - Security headers
  - HTTPS
  - More robust password policies

## License

[MIT License](LICENSE)