import cv2
import numpy as np
import os

# --- Function to display the main menu ---
def show_main_menu():
    menu_image = np.zeros((400, 600, 3), dtype=np.uint8)

    # Add menu title and options
    cv2.putText(menu_image, "BOARD GAMES MENU", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    cv2.putText(menu_image, "1. Snake and Ladder", (150, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(menu_image, "2. Monopoly Business", (150, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(menu_image, "3. Gesture Shooter", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(menu_image, "Press 1, 2 or 3 to select", (120, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the image
    cv2.imshow("Main Menu", menu_image)
    key = cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

    return key

# --- Individual Game Launchers ---
def play_snake_and_ladder():
    print("🎲 You selected Snake and Ladder!")
    os.system("python snakeandladdergame.py")  # Replace with your filename

def play_monopoly_business():
    print("🏢 You selected Monopoly Business!")
    os.system("python monopolygame.py")

def play_gesture_shooter():
    print("🔫 You selected Gesture Shooter!")
    os.system("python shootinggame.py")

# --- Main Program ---
if __name__ == "__main__":
    user_choice = show_main_menu()

    if user_choice == ord('1'):
        play_snake_and_ladder()
    elif user_choice == ord('2'):
        play_monopoly_business()
    elif user_choice == ord('3'):
        play_gesture_shooter()
    else:
        print("Invalid selection, please try again.")

