const API_URL = 'http://localhost:5000/api';

// DOM Elements
const playerHand = document.getElementById('playerHand');
const computerHand = document.getElementById('computerHand');
const resultMessage = document.getElementById('resultMessage');
const choiceBtns = document.querySelectorAll('.choice-btn');
const resetBtn = document.getElementById('resetBtn');
const playerWinsEl = document.getElementById('playerWins');
const computerWinsEl = document.getElementById('computerWins');
const drawsEl = document.getElementById('draws');
const totalGamesEl = document.getElementById('totalGames');

let isPlaying = false;

// Hand icons mapping
const handIcons = {
    rock: 'fa-hand-rock',
    paper: 'fa-hand-paper',
    scissors: 'fa-hand-scissors'
};

// Initialize game
async function initGame() {
    await loadStats();
}

// Load statistics from backend
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const stats = await response.json();
        updateStatsDisplay(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        resultMessage.textContent = 'Error connecting to server';
        resultMessage.className = 'result-message lose';
    }
}

// Update stats display
function updateStatsDisplay(stats) {
    playerWinsEl.textContent = stats.player_wins;
    computerWinsEl.textContent = stats.computer_wins;
    drawsEl.textContent = stats.draws;
    totalGamesEl.textContent = stats.total_games;
}

// Update hand icon
function updateHandIcon(element, choice, isComputer = false) {
    const icon = element.querySelector('i');
    icon.className = `fas ${handIcons[choice]} fa-5x`;
}

// Play game
async function playGame(playerChoice) {
    if (isPlaying) return;
    
    isPlaying = true;
    disableButtons();
    
    // Reset to rock position
    updateHandIcon(playerHand, 'rock');
    updateHandIcon(computerHand, 'rock', true);
    
    // Clear previous result
    resultMessage.textContent = '';
    resultMessage.className = 'result-message';
    
    // Add shake animation
    playerHand.classList.add('shake');
    computerHand.classList.add('shake');
    
    // Wait for animation to complete
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Remove shake animation
    playerHand.classList.remove('shake');
    computerHand.classList.remove('shake');
    
    try {
        // Send choice to backend
        const response = await fetch(`${API_URL}/play`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ choice: playerChoice })
        });
        
        const data = await response.json();
        
        // Update hands with final choices
        updateHandIcon(playerHand, data.player_choice);
        updateHandIcon(computerHand, data.computer_choice, true);
        
        // Display result
        displayResult(data.result);
        
        // Update stats
        updateStatsDisplay(data.stats);
        
    } catch (error) {
        console.error('Error playing game:', error);
        resultMessage.textContent = 'Error connecting to server';
        resultMessage.className = 'result-message lose';
    }
    
    isPlaying = false;
    enableButtons();
}

// Display game result
function displayResult(result) {
    if (result === 'player') {
        resultMessage.textContent = '🎉 You Win!';
        resultMessage.className = 'result-message win';
    } else if (result === 'computer') {
        resultMessage.textContent = '😢 Computer Wins!';
        resultMessage.className = 'result-message lose';
    } else {
        resultMessage.textContent = "🤝 It's a Draw!";
        resultMessage.className = 'result-message draw';
    }
}

// Disable buttons during animation
function disableButtons() {
    choiceBtns.forEach(btn => btn.disabled = true);
}

// Enable buttons after animation
function enableButtons() {
    choiceBtns.forEach(btn => btn.disabled = false);
}

// Reset statistics
async function resetStats() {
    if (!confirm('Are you sure you want to reset all statistics?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/reset`, {
            method: 'POST'
        });
        
        const data = await response.json();
        updateStatsDisplay(data.stats);
        
        resultMessage.textContent = 'Statistics reset successfully!';
        resultMessage.className = 'result-message';
        
        // Reset hands to rock
        updateHandIcon(playerHand, 'rock');
        updateHandIcon(computerHand, 'rock', true);
        
    } catch (error) {
        console.error('Error resetting stats:', error);
        resultMessage.textContent = 'Error resetting statistics';
        resultMessage.className = 'result-message lose';
    }
}

// Event listeners
choiceBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const choice = btn.dataset.choice;
        playGame(choice);
    });
});

resetBtn.addEventListener('click', resetStats);

// Initialize on page load
initGame();
let playerStreak = 0;
let bestStreak = 0;
let comboMultiplier = 1;

// Add countdown before revealing result
async function showCountdown() {
    const countdown = document.createElement('div');
    countdown.className = 'countdown-overlay';
    countdown.innerHTML = '<div class="countdown-number">3</div>';
    document.body.appendChild(countdown);
    
    for (let i = 3; i > 0; i--) {
        countdown.querySelector('.countdown-number').textContent = i;
        soundManager.play('click');
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    countdown.remove();
}

// Update streak tracking
function updateStreak(result) {
    if (result === 'player') {
        playerStreak++;
        if (playerStreak > bestStreak) {
            bestStreak = playerStreak;
        }
        if (playerStreak >= 3) {
            comboMultiplier = Math.floor(playerStreak / 3) + 1;
            showComboEffect(comboMultiplier);
        }
    } else if (result === 'computer') {
        playerStreak = 0;
        comboMultiplier = 1;
    }
    
    document.getElementById('currentStreak').textContent = playerStreak;
    document.getElementById('bestStreak').textContent = bestStreak;
}

// Show combo effect
function showComboEffect(multiplier) {
    const combo = document.createElement('div');
    combo.className = 'combo-popup';
    combo.innerHTML = `<h2>🔥 ${multiplier}x COMBO! 🔥</h2>`;
    document.body.appendChild(combo);
    
    setTimeout(() => combo.remove(), 2000);
}
