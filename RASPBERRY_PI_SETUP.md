# 🍓 Guía de Instalación en Raspberry Pi

## Requisitos Previos
- Raspberry Pi 3/4/5 con Raspberry Pi OS (Bullseye o Bookworm recomendado)
- Conexión a internet
- Tarjeta SD de al menos 16GB
- Arduino conectado vía USB

---

## 📋 PASO 1: Preparar Raspberry Pi OS

### 1.1 Actualizar el Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Instalar Dependencias del Sistema

**Dependencias esenciales** (mínimo necesario):
```bash
# Python y herramientas básicas
sudo apt install -y python3-pip python3-dev

# Para pyserial (comunicación Arduino)
# No requiere dependencias adicionales del sistema

# Para OpenCV (si usas cámara)
sudo apt install -y python3-opencv libopenblas0

# Para cámaras USB
sudo apt install -y v4l-utils
```

**Dependencias opcionales** (solo si las necesitas):
```bash
# Si usas cámara oficial Raspberry Pi:
sudo apt install -y libcamera-dev libcamera-apps

# Si pyvisual requiere Qt:
sudo apt install -y python3-pyqt5 libqt5gui5

# Si pyvisual requiere GTK:
sudo apt install -y libgtk-3-0

# Habilitar cámara Raspberry Pi (si usas cámara oficial)
sudo raspi-config
# Ir a: Interface Options -> Camera -> Enable
```

**Nota**: Si encuentras errores de NumPy sobre librerías matemáticas, instala:
```bash
sudo apt install -y libopenblas0 libatlas3-base
```

---

## 📦 PASO 2: Configurar Python Global

### 2.1 Preparar Directorio de Trabajo
```bash
cd ~
mkdir proyectos
cd proyectos
```

### 2.2 Actualizar pip Global
```bash
pip3 install --upgrade pip setuptools wheel
```

---

## 🚀 PASO 3: Transferir el Proyecto

### Opción A: Usando Git (Recomendado)
```bash
# Desde tu Raspberry Pi
cd ~/proyectos
git clone https://github.com/Rodrigodp97/IOT01.git pyvisual
cd pyvisual
```

### Opción B: Usando SCP/SFTP
```bash
# Desde tu PC Windows (PowerShell)
scp -r "C:\Users\IXJUX7Q\OneDrive-Deere&Co\OneDrive - Deere & Co\Escritorio\Python\Rodrigo\pyvisual" pi@<IP_RASPBERRY>:~/proyectos/
```

### Opción C: Usando USB
1. Copia la carpeta `pyvisual` a una memoria USB
2. En la Raspberry Pi:
```bash
cp -r /media/pi/USB/pyvisual ~/proyectos/
```

---

## 📚 PASO 4: Instalar Dependencias del Proyecto

```bash
cd ~/proyectos/pyvisual

# Instalar desde requirements.txt (globalmente)
pip3 install -r requirements.txt

# Si pyvisual tiene problemas, instalar manualmente:
pip3 install pyvisual opencv-python-headless pyserial "numpy<2.0"
```

### 4.1 Nota sobre OpenCV
Si `opencv-python` causa problemas, usa la versión del sistema:
```bash
pip uninstall opencv-python
# Usar el OpenCV instalado con apt (python3-opencv)
```

---

## 🔌 PASO 5: Configurar Permisos Serial

```bash
# Agregar usuario al grupo dialout para acceso serial
sudo usermod -a -G dialout $USER
sudo usermod -a -G tty $USER

# Reiniciar sesión o aplicar cambios
newgrp dialout

# Verificar que el Arduino está conectado
ls -l /dev/ttyUSB* /dev/ttyACM*

# Dar permisos (si es necesario)
sudo chmod 666 /dev/ttyUSB0  # o el puerto que uses
```

---

## ▶️ PASO 6: Ejecutar la Aplicación

### 6.1 Ejecución Manual
```bash
cd ~/proyectos/pyvisual
python3 app.py
```

### 6.2 Crear Script de Inicio
```bash
nano ~/start_pyvisual.sh
```

Contenido del script:
```bash
#!/bin/bash
cd ~/proyectos/pyvisual
python3 app.py
```

Hacer ejecutable:
```bash
chmod +x ~/start_pyvisual.sh
```

### 6.3 Ejecutar al Inicio (Opcional)
```bash
# Editar crontab
crontab -e

# Agregar al final:
@reboot sleep 30 && ~/start_pyvisual.sh
```

---

## 🔧 PASO 7: Configuración de Display

### Para ejecutar con GUI (monitor conectado)
```bash
export DISPLAY=:0
python3 app.py
```

### Para VNC (acceso remoto con GUI)
1. Habilitar VNC en Raspberry Pi:
```bash
sudo raspi-config
# Interface Options -> VNC -> Enable
```

2. Conectar con VNC Viewer desde tu PC
3. Ejecutar la aplicación desde la sesión VNC

### Para SSH sin GUI (headless)
Si no necesitas interfaz gráfica, modifica el código para modo consola.

---

## 🐛 PASO 8: Solución de Problemas

### Si no detecta el Arduino:
```bash
# Ver dispositivos USB
lsusb

# Ver puertos seriales
ls -l /dev/tty*

# Probar comunicación
python3 -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
```

### Si hay problemas con la cámara:
```bash
# Listar cámaras disponibles
v4l2-ctl --list-devices

# Probar cámara
libcamera-hello

# En OpenCV, usar índice correcto
# cv2.VideoCapture(0) o cv2.VideoCapture('/dev/video0')
```

### Si hay problemas de memoria:
```bash
# Aumentar swap
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Cambiar CONF_SWAPSIZE=100 a CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Si pyvisual no funciona correctamente:
```bash
# Verificar instalación
pip list | grep pyvisual
pip show pyvisual

# Reinstalar
pip uninstall pyvisual
pip install pyvisual --no-cache-dir
```

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real:
```bash
python3 app.py 2>&1 | tee app.log
```

### Verificar uso de recursos:
```bash
htop  # (instalar con: sudo apt install htop)
```

---

## ⚡ Optimizaciones para Raspberry Pi

### Mejorar Rendimiento:
1. **Reducir resolución de cámara** si es necesario
2. **Overclocking** (opcional, en raspi-config)
3. **Deshabilitar servicios innecesarios**:
```bash
sudo systemctl disable bluetooth
sudo systemctl disable cups
```

### Configuración de OpenCV para mejor rendimiento:
Agregar al inicio de `app.py`:
```python
import cv2
cv2.setNumThreads(4)  # Ajustar según núcleos disponibles
```

---

## ✅ Checklist Final

- [ ] Sistema actualizado
- [ ] Python 3 y pip instalados globalmente
- [ ] Proyecto transferido
- [ ] Dependencias instaladas globalmente
- [ ] Permisos serial configurados
- [ ] Arduino conectado y detectado
- [ ] Aplicación ejecutándose correctamente
- [ ] (Opcional) Script de inicio configurado
- [ ] (Opcional) Acceso VNC habilitado

---

## 📞 Ayuda Adicional

### Versiones recomendadas:
- Raspberry Pi OS: Bookworm (Debian 12)
- Python: 3.9 o superior
- OpenCV: 4.x

### Recursos:
- [Documentación Raspberry Pi](https://www.raspberrypi.com/documentation/)
- [PySerial en Linux](https://pyserial.readthedocs.io/)
- [OpenCV en Raspberry Pi](https://docs.opencv.org/4.x/)
