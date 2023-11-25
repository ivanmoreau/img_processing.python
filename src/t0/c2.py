import cv2
import numpy as np

# Define los umbrales HSV para tu objeto
lower_bound = np.array([161, 155, 84])
upper_bound = np.array([179, 255, 255])

# Inicializa la cámara (asegúrate de que la cámara esté disponible)
cap = cv2.VideoCapture(0)  # Usar 0 para la cámara predeterminada, puedes cambiarlo si tienes múltiples cámaras

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Convierte el frame a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aplica el umbral
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Encuentra los contornos del objeto
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Encuentra el centroide del objeto
        M = cv2.moments(contours[0])
        if M["m00"] != 0:
            M = cv2.moments(contours[0])
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            x, y, w, h = cv2.boundingRect(contours[0])

            # Dibuja un círculo alrededor del centroide
            max_area = (max(int(w / 2), int(h / 2)))
            radius = int(np.sqrt(2 * (max_area ** 2)))
            cv2.circle(frame, (cx, cy), radius, (255, 0, 255), 2)

            # Dibuja un rectángulo alrededor del objeto
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibuja una línea de posición desde el centro de la imagen hasta el centroide
            cv2.line(frame, (frame.shape[1] // 2, frame.shape[0] // 2), (cx, cy), (255, 0, 0), 2)

    # Muestra el frame con los elementos de seguimiento
    cv2.imshow('Seguimiento', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()
