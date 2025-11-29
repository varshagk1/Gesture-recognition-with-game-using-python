import cv2
import numpy as np
import random
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Game Constants
GRID_SIZE = 10
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // GRID_SIZE

# Snakes and Ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Players
players = [{"name": "Player 1", "position": 1}, {"name": "Player 2", "position": 1}]
current_player_idx = 0

# Initialize Webcam
cap = cv2.VideoCapture(0)

def get_coords(pos):
    """Convert board position (1–100) to x,y pixel coordinates."""
    row = (pos - 1) // GRID_SIZE
    col = (pos - 1) % GRID_SIZE
    if row % 2 == 1:  # reverse direction every alternate row
        col = GRID_SIZE - 1 - col
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)
    return x, y

def draw_board():
    """Draws the game board with players, snakes, ladders."""
    board = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    # Draw grid
    for i in range(GRID_SIZE + 1):
        cv2.line(board, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), (0, 0, 0), 2)
        cv2.line(board, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), (0, 0, 0), 2)

    # Add cell numbers
    for i in range(100):
        num = i + 1
        x, y = get_coords(num)
        cv2.putText(board, str(num), (x - 20, y + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 1)

    # Draw snakes
    for head, tail in snakes.items():
        hx, hy = get_coords(head)
        tx, ty = get_coords(tail)
        cv2.arrowedLine(board, (hx, hy), (tx, ty), (0, 0, 255), 2)

    # Draw ladders
    for start, end in ladders.items():
        sx, sy = get_coords(start)
        ex, ey = get_coords(end)
        cv2.arrowedLine(board, (sx, sy), (ex, ey), (0, 255, 0), 2)

    # Draw players
    for i, player in enumerate(players):
        px, py = get_coords(player["position"])
        color = (255, 0, 0) if i == 0 else (0, 0, 255)
        cv2.circle(board, (px, py), 12, color, -1)

    # Show player info
    for i, player in enumerate(players):
        info = f"{player['name']}: {player['position']}"
        cv2.putText(board, info, (10, 20 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return board

def roll_dice():
    return random.randint(1, 6)

def move_player(player):
    roll = roll_dice()
    print(f"{player['name']} rolled a {roll}")
    player["position"] += roll
    if player["position"] in snakes:
        print(f"{player['name']} bitten by snake! Down to {snakes[player['position']]}")
        player["position"] = snakes[player["position"]]
    elif player["position"] in ladders:
        print(f"{player['name']} climbed ladder! Up to {ladders[player['position']]}")
        player["position"] = ladders[player["position"]]
    if player["position"] > 100:
        player["position"] = 100

def detect_thumbs_up(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            thumb = handLms.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            if thumb.y < index.y:  # Thumbs up gesture
                return True
    return False

def play_game():
    global current_player_idx
    print("Show thumbs up to roll dice. Press 'q' to quit.")
    while True:
        player = players[current_player_idx]
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gesture = detect_thumbs_up(frame)

        if gesture:
            move_player(player)
            board = draw_board()
            cv2.imshow("Snake & Ladder", board)
            cv2.waitKey(1200)

            if player["position"] == 100:
                print(f"{player['name']} wins!")
                break

            current_player_idx = (current_player_idx + 1) % len(players)

        cv2.imshow("Webcam Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    play_game()
