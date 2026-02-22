import { levels, LevelParams } from './levels';

export interface GameEngineCallbacks {
    updateStats: (level: number, strokes: number) => void;
    logAction: (message: string, type?: 'info' | 'error' | 'success') => void;
    onLevelComplete: (level: number, strokes: number, message: string) => void;
    updateObjective: (text: string) => void;
}

export class GameEngine {
    private gridElement: HTMLElement;
    private callbacks: GameEngineCallbacks;

    private currentLevelIndex: number = 0;
    private strokes: number = 0;

    // Grid state
    private gridMap: string[][] = [];
    private width: number = 0;
    private height: number = 0;

    // Cursor State
    private cx: number = 0;
    private cy: number = 0;

    private cursorElement: HTMLElement | null = null;

    constructor(gridElement: HTMLElement, callbacks: GameEngineCallbacks) {
        this.gridElement = gridElement;
        this.callbacks = callbacks;
    }

    public start() {
        this.currentLevelIndex = 0;
        this.loadCurrentLevel();
        this.callbacks.logAction('VimQuest Initialized.', 'success');
    }

    public loadNextLevel() {
        this.currentLevelIndex++;
        if (this.currentLevelIndex >= levels.length) {
            this.callbacks.logAction('Game Complete! Thanks for playing.', 'success');
            // reset or handle game over
            this.currentLevelIndex = 0;
        }
        this.loadCurrentLevel();
    }

    private loadCurrentLevel() {
        this.strokes = 0;
        const levelData = levels[this.currentLevelIndex];

        this.callbacks.updateStats(this.currentLevelIndex + 1, this.strokes);
        this.callbacks.updateObjective(levelData.objective);
        this.callbacks.logAction(`Loaded Level ${this.currentLevelIndex + 1}: ${levelData.name}`);

        this.parseMap(levelData.map);
        this.renderGrid();
    }

    private parseMap(mapString: string) {
        const lines = mapString.trim().split('\n').map(l => l.trimEnd());
        this.height = lines.length;
        this.width = Math.max(...lines.map(l => l.length));

        this.gridMap = [];
        for (let y = 0; y < this.height; y++) {
            const row: string[] = [];
            for (let x = 0; x < this.width; x++) {
                const char = lines[y][x] || ' ';
                if (char === 'C') {
                    this.cx = x;
                    this.cy = y;
                    row.push(' '); // Empty space where cursor starts
                } else {
                    row.push(char);
                }
            }
            this.gridMap.push(row);
        }
    }

    private renderGrid() {
        this.gridElement.innerHTML = '';

        const wrapper = document.createElement('div');
        wrapper.className = 'grid-world';
        wrapper.style.gridTemplateColumns = `repeat(${this.width}, 1.5rem)`;
        wrapper.style.gridTemplateRows = `repeat(${this.height}, 1.5rem)`;

        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                const val = this.gridMap[y][x];

                if (val === '#') {
                    cell.classList.add('wall');
                    cell.textContent = '#';
                } else if (val === 'E') {
                    cell.classList.add('exit');
                    cell.textContent = 'E';
                } else {
                    cell.textContent = val !== ' ' ? val : '';
                }

                wrapper.appendChild(cell);
            }
        }

        // Add Cursor
        this.cursorElement = document.createElement('div');
        this.cursorElement.className = 'cursor';
        this.cursorElement.textContent = '@';
        this.updateCursorVisual();

        wrapper.appendChild(this.cursorElement);
        this.gridElement.appendChild(wrapper);
    }

    private updateCursorVisual() {
        if (!this.cursorElement) return;
        // 1.5rem = 24px (assuming 16px base)
        // using inline styles for translation
        this.cursorElement.style.transform = `translate(calc(${this.cx} * 1.5rem), calc(${this.cy} * 1.5rem))`;
    }

    public handleInput(key: string) {
        let moved = false;

        switch (key) {
            case 'h': moved = this.move(-1, 0); break;
            case 'j': moved = this.move(0, 1); break;
            case 'k': moved = this.move(0, -1); break;
            case 'l': moved = this.move(1, 0); break;
            case 'w': moved = this.doW(); break;
            case 'b': moved = this.doB(); break;
            case 'e': moved = this.doE(); break;
        }

        if (moved) {
            this.strokes++;
            this.callbacks.updateStats(this.currentLevelIndex + 1, this.strokes);
            this.updateCursorVisual();
            this.checkEnvironment();
        } else if (['h', 'j', 'k', 'l', 'w', 'b', 'e'].includes(key)) {
            // Log bump
            const bumpMessages = ["Ouch!", "Bump.", "Wall ahead."];
            this.callbacks.logAction(bumpMessages[Math.floor(Math.random() * bumpMessages.length)], 'error');
        }
    }

    private move(dx: number, dy: number): boolean {
        const nx = this.cx + dx;
        const ny = this.cy + dy;

        if (nx >= 0 && nx < this.width && ny >= 0 && ny < this.height) {
            if (this.gridMap[ny][nx] !== '#') {
                this.cx = nx;
                this.cy = ny;
                return true;
            }
        }
        return false;
    }

    private moveTo(nx: number, ny: number): boolean {
        this.cx = nx;
        this.cy = ny;
        return true;
    }

    private isWordChar(char: string | undefined): boolean {
        return !!char && char !== ' ' && char !== '#';
    }

    private getLinearNext(x: number, y: number, dir: 1 | -1): { x: number, y: number } | null {
        let nx = x + dir;
        let ny = y;
        if (nx >= this.width) {
            nx = 0;
            ny++;
        } else if (nx < 0) {
            nx = this.width - 1;
            ny--;
        }
        if (ny >= this.height || ny < 0) return null;
        return { x: nx, y: ny };
    }

    private doW(): boolean {
        let pos = { x: this.cx, y: this.cy };
        let char = this.gridMap[pos.y][pos.x];
        let inWord = this.isWordChar(char);

        while (true) {
            let next = this.getLinearNext(pos.x, pos.y, 1);
            if (!next) break;
            pos = next;
            let nextChar = this.gridMap[pos.y][pos.x];

            if (nextChar === '#') break; // stop passing through walls

            if (!inWord && this.isWordChar(nextChar)) {
                return this.moveTo(pos.x, pos.y);
            }
            inWord = this.isWordChar(nextChar);
        }
        return false;
    }

    private doB(): boolean {
        let pos = { x: this.cx, y: this.cy };
        let prev = this.getLinearNext(pos.x, pos.y, -1);
        if (!prev) return false;

        pos = prev;
        while (pos) {
            let char = this.gridMap[pos.y][pos.x];
            if (char === '#') break;

            let before = this.getLinearNext(pos.x, pos.y, -1);
            let beforeChar = before ? this.gridMap[before.y][before.x] : ' ';

            if (this.isWordChar(char) && !this.isWordChar(beforeChar)) {
                return this.moveTo(pos.x, pos.y);
            }
            pos = before as { x: number, y: number };
            if (!pos) break;
        }
        return false;
    }

    private doE(): boolean {
        let pos = { x: this.cx, y: this.cy };
        let next = this.getLinearNext(pos.x, pos.y, 1);
        if (!next) return false;

        pos = next;
        while (pos) {
            let char = this.gridMap[pos.y][pos.x];
            if (char === '#') break;

            let after = this.getLinearNext(pos.x, pos.y, 1);
            let afterChar = after ? this.gridMap[after.y][after.x] : ' ';

            if (this.isWordChar(char) && !this.isWordChar(afterChar)) {
                return this.moveTo(pos.x, pos.y);
            }
            pos = after as { x: number, y: number };
            if (!pos) break;
        }
        return false;
    }

    private checkEnvironment() {
        const currentCell = this.gridMap[this.cy][this.cx];
        if (currentCell === 'E') {
            this.callbacks.logAction('Reached the exit!', 'success');
            setTimeout(() => {
                this.callbacks.onLevelComplete(
                    this.currentLevelIndex + 1,
                    this.strokes,
                    getCompletionMessage(this.strokes, levels[this.currentLevelIndex].par)
                );
            }, 200);
        }
    }
}

function getCompletionMessage(strokes: number, par: number): string {
    if (strokes <= par) return "Perfect navigation! You're a true Vim master.";
    if (strokes <= par + 5) return "Great job! Keep practicing to reduce your keystrokes.";
    return `Level Complete. (Your strokes: ${strokes}, Par: ${par})`;
}
