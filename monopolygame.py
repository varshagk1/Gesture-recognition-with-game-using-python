import cv2
import mediapipe as mp
import pygame
import random
import time

# ---------- Initialize pygame ----------
pygame.init()
WIDTH, HEIGHT = 1100, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎲 Gesture Controlled Monopoly (Tamil Nadu Edition)")

font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

# ---------- Board setup ----------
places = [
    {"name": "Chennai", "price": 1000},
    {"name": "Madurai", "price": 900},
    {"name": "Coimbatore", "price": 800},
    {"name": "Salem", "price": 750},
    {"name": "Erode", "price": 700},
    {"name": "Trichy", "price": 950},
    {"name": "Tirunelveli", "price": 600},
    {"name": "Vellore", "price": 700},
    {"name": "Thoothukudi", "price": 650},
    {"name": "Kanchipuram", "price": 800},
    {"name": "Tanjore", "price": 750},
    {"name": "Nagercoil", "price": 850},
    {"name": "Dindigul", "price": 600},
    {"name": "Cuddalore", "price": 650},
    {"name": "Karur", "price": 550},
    {"name": "Sivakasi", "price": 500},
    {"name": "Villupuram", "price": 550},
    {"name": "Nagapattinam", "price": 600},
    {"name": "Pudukkottai", "price": 500},
    {"name": "Ooty", "price": 1000}
]

tile_w, tile_h = 180, 80
cols = 5
board_x, board_y = 80, 80

# ---------- Player setup ----------
players = [
    {"color": (255, 0, 0), "pos": 0, "money": 5000, "name": "Player 1", "properties": []},
    {"color": (0, 0, 255), "pos": 0, "money": 5000, "name": "Player 2", "properties": []}
]
turn = 0
dice_value = 1
roll_allowed = True
last_roll_time = 0

# ---------- Mediapipe Setup ----------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
last_x = None

# ---------- Game Logic ----------
def roll_dice():
    global dice_value, roll_allowed, last_roll_time, turn
    dice_value = random.randint(1, 6)
    player = players[turn]
    player["pos"] = (player["pos"] + dice_value) % len(places)
    place = places[player["pos"]]
    print(f"🎲 {player['name']} rolled {dice_value} and landed on {place['name']}")

    # Buy property if available
    if place["name"] not in player["properties"]:
        if player["money"] >= place["price"]:
            player["money"] -= place["price"]
            player["properties"].append(place["name"])
            print(f"{player['name']} bought {place['name']} for ₹{place['price']}")
        else:
            print(f"{player['name']} doesn't have enough money for {place['name']}")
    else:
        # If owned by someone else, pay rent
        for p in players:
            if p != player and place["name"] in p["properties"]:
                rent = place["price"] // 10
                player["money"] -= rent
                p["money"] += rent
                print(f"{player['name']} paid ₹{rent} rent to {p['name']}")

    roll_allowed = False
    last_roll_time = time.time()
    turn = (turn + 1) % len(players)

def draw_board():
    screen.fill((240, 240, 240))

    # Draw places grid
    for i, place in enumerate(places):
        row, col = divmod(i, cols)
        x = board_x + col * tile_w
        y = board_y + row * tile_h
        rect = pygame.Rect(x, y, tile_w, tile_h)
        pygame.draw.rect(screen, (220, 220, 220), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        name_text = font.render(f"{i+1}. {place['name']}", True, (0, 0, 0))
        price_text = font.render(f"₹{place['price']}", True, (60, 60, 60))
        screen.blit(name_text, (x + 10, y + 10))
        screen.blit(price_text, (x + 10, y + 40))

    # Draw players
    for p in range(len(players)):
        row, col = divmod(players[p]["pos"], cols)
        px = board_x + col * tile_w + 130 + (p * 20)
        py = board_y + row * tile_h + 40
        pygame.draw.circle(screen, players[p]["color"], (px, py), 15)

    # Dice display
    dice_rect = pygame.Rect(850, 550, 120, 120)
    pygame.draw.rect(screen, (255, 255, 255), dice_rect)
    pygame.draw.rect(screen, (0, 0, 0), dice_rect, 3)
    dice_text = font.render(str(dice_value), True, (0, 0, 0))
    screen.blit(dice_text, (905, 600))

    # Player Info
    y_info = 500
    for p in players:
        info = font.render(
            f"{p['name']}: ₹{p['money']} (at {places[p['pos']]['name']})", True, p["color"]
        )
        screen.blit(info, (100, y_info))
        y_info += 40

    pygame.display.flip()

# ---------- Main Loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Gesture detection (move right to roll dice)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = hand_landmarks.landmark[0].x

            if last_x is not None:
                move = x - last_x
                if move > 0.08 and roll_allowed:
                    roll_dice()
            last_x = x

    # Allow roll again after 2 sec
    if not roll_allowed and time.time() - last_roll_time > 2:
        roll_allowed = True

    draw_board()
    cv2.imshow("🎥 Gesture Control", frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
