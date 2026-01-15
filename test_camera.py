import cv2

print("Buscando cámaras disponibles...")
print("-" * 40)

# Intentar abrir las primeras 5 cámaras
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✓ Cámara encontrada en índice {i}")
            print(f"  Resolución: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print(f"✗ Cámara en índice {i} existe pero no puede capturar")
        cap.release()
    else:
        print(f"✗ No hay cámara en índice {i}")
    
print("-" * 40)
print("Prueba completada")
