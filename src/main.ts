import './style.css';
import { GameEngine } from './engine';

const app = document.querySelector<HTMLDivElement>('#app')!;
const gridElement = document.getElementById('grid')!;
const levelDisplay = document.getElementById('level-display')!;
const strokesDisplay = document.getElementById('strokes-display')!;
const actionLog = document.getElementById('action-log')!;
const modal = document.getElementById('modal')!;
const modalTitle = document.getElementById('modal-title')!;
const modalMessage = document.getElementById('modal-message')!;
const nextLevelBtn = document.getElementById('next-level-btn')!;
const levelObjective = document.getElementById('level-objective')!;

const engine = new GameEngine(
    gridElement,
    {
        updateStats: (level, strokes) => {
            levelDisplay.textContent = `Level ${level}`;
            strokesDisplay.textContent = `Strokes: ${strokes}`;
        },
        logAction: (message, type) => {
            const div = document.createElement('div');
            div.textContent = `> ${message}`;
            if (type === 'error') div.className = 'text-error';
            if (type === 'success') div.className = 'text-success';
            actionLog.appendChild(div);
            // Auto scroll to bottom
            actionLog.scrollTop = actionLog.scrollHeight;
        },
        onLevelComplete: (level, strokes, message) => {
            modal.classList.remove('hidden');
            modalTitle.textContent = `Level ${level} Complete!`;
            modalMessage.textContent = message;
        },
        updateObjective: (text) => {
            levelObjective.textContent = text;
        }
    }
);

engine.start();

// Handle keyboard input
window.addEventListener('keydown', (e) => {
    // Prevent default browser scrolling with keys
    if ([' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        e.preventDefault();
    }

    if (!modal.classList.contains('hidden')) {
        if (e.key === 'Enter') {
            modal.classList.add('hidden');
            engine.loadNextLevel();
        }
        return;
    }

    engine.handleInput(e.key);
});

nextLevelBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
    engine.loadNextLevel();
});
