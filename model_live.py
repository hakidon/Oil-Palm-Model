from keras.models import load_model
import cv2
import numpy as np
import statistics

import winsound

def play_alert_sound():
    duration = 500  # milliseconds
    frequency = 700  # Hz (A4 note)
    winsound.Beep(frequency, duration)

def draw_pause_button(frame):
    # Draw a rectangle for the button background
    button_x, button_y = 10, 10
    button_width, button_height = 100, 50
    cv2.rectangle(frame, (button_x, button_y), (button_x + button_width, button_y + button_height), (0, 0, 255), -1)

    # Draw the "Pause" text on the button
    text_x, text_y = button_x + 5, button_y + 35
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)
    cv2.putText(frame, "Pause", (text_x, text_y), font, font_scale, font_color, 2)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

count_fps = 0
list_img = []
list_acc = []
paused = False

while True:
    # Grab the web camera's image.
    ret, show_img = camera.read()

    # Show the image in a window
    if not paused:
        
        if count_fps == 30:
            play_alert_sound()
            print("Class: ", statistics.mode(list_img).strip())
            print("Accuracy: ", statistics.mean(list_acc))
            list_img = []
            list_acc = []
            count_fps = 0

        cv2.imshow("Webcam Image", show_img)

    # Check if the camera feed is paused
    if not paused:
        # Resize the raw image to (224-height,224-width) pixels
        image = cv2.resize(show_img, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the model's input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predict the model
        prediction = model.predict(image, verbose=False)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        list_img.append(class_name[2:])
        list_acc.append(np.round(confidence_score * 100))

        count_fps += 1

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the ESC key on your keyboard.
    if keyboard_input == 27:
        break

    # Toggle pause when the button is clicked (left mouse button)
    if keyboard_input == ord('p') or keyboard_input == ord('P') or keyboard_input == 32:  # 'p' or 'P' or spacebar
        count_fps = 0
        list_img = []
        list_acc = []

        if paused == True:
            paused = False
        else:
            paused = True
            draw_pause_button(show_img)
            cv2.imshow("Webcam Image", show_img)

       


camera.release()
cv2.destroyAllWindows()
