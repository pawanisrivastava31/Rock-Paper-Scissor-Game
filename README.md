# Rock-Paper-Scissor-Game
## Interactive Rock Paper Scissors Game
A full-stack, interactive "Rock Paper Scissors" game built with a Python & Flask backend and a dynamic HTML, CSS, & JavaScript frontend. This project features real-time gameplay against a computer AI, persistent statistics tracking with a database, and engaging animations and sound effects.

## Features
Interactive Gameplay: Play against a computer AI with a clean and responsive user interface.
Dynamic Animations: Includes a "hand-shaking" animation before each result is revealed and celebratory confetti on a win.
Persistent Statistics: Game scores (wins, losses, draws, total games) are saved to an SQLite database, so your stats are never lost.
Sound Effects: Audio feedback for game actions, wins, losses, and draws to enhance the user experience.
Streak Tracking: Tracks your current and best winning streaks, which are saved in the browser's local storage.
Win Rate Calculator: A visual progress bar displays your win percentage in real-time.
Fully Responsive: The layout adapts smoothly to devices of all sizes, from mobile phones to desktops.
RESTful API: A well-defined API built with Flask handles all game logic and data management.

## Technologies Used

Backend:
Python 3: Core language for server-side logic.
Flask: A lightweight web framework to create the API.
Flask-CORS: To handle cross-origin requests from the frontend.
SQLite: Serverless database for storing game statistics.

Frontend:
HTML5: For the application's structure.
CSS3: For styling, responsiveness (Flexbox), and animations (@keyframes).
JavaScript (ES6+): For DOM manipulation, interactivity, and API communication (Fetch API).
Font Awesome: For scalable vector icons (the hands).

## Project Structure
text
rock-paper-scissors/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # Database logic (connect, read, write)
│   ├── requirements.txt    # Python dependencies
│   └── game_stats.db       # SQLite database file (auto-generated)
│
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── style.css           # Stylesheet for the UI
│   ├── script.js           # Frontend logic and API calls
│   └── sounds.js           # Sound effect manager

## API Endpoints
The backend provides the following RESTful API endpoints:

Method	Endpoint	Description
POST	/api/play	Submit a player's choice ('rock', 'paper', or 'scissors') and get the result.
GET	/api/stats	Retrieve the current game statistics (wins, losses, draws, etc.).
POST	/api/reset	Reset all game statistics in the database to zero.
GET	/api/health	A simple health check endpoint to confirm the server is running.

 ## Future Enhancements
 
Multiplayer Mode: Add real-time, player-vs-player gameplay using WebSockets.
Advanced AI: Implement a "Hard Mode" where the computer analyzes player patterns.
User Accounts: Add user authentication to track multiple players' stats.
Leaderboard: Create a global leaderboard to rank players by their win streaks.
Gesture Control: Use a library like TensorFlow.js to allow players to play using their webcam.

## License
This project is free to use for educational and academic purposes.


