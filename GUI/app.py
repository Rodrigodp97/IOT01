import pyvisual as pv
from ui.ui import create_ui
import serial
import serial.tools.list_ports
import threading
import time
import platform
import sys
import os
import json
import socket
from pathlib import Path

# Importar módulo de mapas y forzar recarga
import importlib
import mapa_manager
importlib.reload(mapa_manager)  # Forzar recarga del módulo
from mapa_manager import abrir_mapa

# Importar servidor GPS WiFi
try:
    from servidor_gps_wifi import iniciar_servidor_thread
    SERVIDOR_GPS_DISPONIBLE = True
except ImportError:
    print("⚠ Advertencia: servidor_gps_wifi no disponible (Flask podría no estar instalado)")
    SERVIDOR_GPS_DISPONIBLE = False

# Forzar salida inmediata de prints
sys.stdout.flush()

# Establecer el directorio de trabajo al directorio del script
# Esto es crucial para que las rutas relativas funcionen en Windows
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
print(f"Directorio de trabajo establecido en: {SCRIPT_DIR}", flush=True)

# ===================================================
# ================ 1. LOGIC CODE ====================
# ===================================================

# Variables de configuración
retraso_deteccion = 0
tiempo_medidas = 0
distancia_deteccion = 0

# Servidor GPS WiFi (recibe ubicación desde Android vía HTTP)
servidor_gps_thread = None
servidor_gps_activo = False
PUERTO_SERVIDOR_GPS = 5000

# Configuración del puerto serial
arduino_port = None
lectura_activa = False
hilo_lectura = None

# Control de modo GPS activo
gps_modo_mapas = False  # True cuando GPS está activo solo para visualización en mapas

# Monitor de conectividad para mapas (online/offline)
monitoreo_red_activo = False
hilo_monitoreo_red = None

# Trayectoria GPS para visualización en mapa
# Lista de tuplas (latitud, longitud) que registra el recorrido
trayectoria_gps = []
ultima_coordenada = None  # Última posición GPS recibida

# Archivo temporal para compartir ubicación GPS con el mapa
GPS_TEMP_FILE = Path(SCRIPT_DIR) / "gps_actual.json"

# Archivo temporal para guardar trayectoria de fumigación
TRAYECTORIA_FUMIGACION_FILE = Path(SCRIPT_DIR) / "fumigacion_trayectoria.json"

# Archivo temporal para guardar trayectoria de fumigación
TRAYECTORIA_FUMIGACION_FILE = Path(SCRIPT_DIR) / "fumigacion_trayectoria.json"

def calcular_distancia_gps(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en metros entre dos coordenadas GPS usando la fórmula de Haversine.
    Retorna la distancia en metros.
    """
    from math import radians, sin, cos, sqrt, atan2
    
    # Radio de la Tierra en metros
    R = 6371000
    
    # Convertir a radianes
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distancia = R * c
    
    return distancia

def agregar_coordenada_gps(lat, lon):
    """
    Agrega una coordenada GPS a la trayectoria solo si se ha movido más de 1 metro.
    """
    global trayectoria_gps, ultima_coordenada
    
    # Primera coordenada, siempre agregar
    if ultima_coordenada is None:
        trayectoria_gps.append((lat, lon))
        ultima_coordenada = (lat, lon)
        print(f"✅ GPS ACEPTADO (1ra coordenada): {lat:.6f}, {lon:.6f}")
        print(f"   Total trayectoria: {len(trayectoria_gps)} puntos")
        # Guardar en archivo de fumigación
        guardar_trayectoria_fumigacion()
        return True
    
    # Calcular distancia desde última coordenada guardada
    distancia = calcular_distancia_gps(
        ultima_coordenada[0], ultima_coordenada[1],
        lat, lon
    )
    
    # Solo agregar si se movió más de 1 metro
    if distancia >= 1.0:
        trayectoria_gps.append((lat, lon))
        ultima_coordenada = (lat, lon)
        print(f"✅ GPS ACEPTADO: {lat:.6f}, {lon:.6f}")
        print(f"   Distancia: {distancia:.2f}m desde último punto")
        print(f"   Total trayectoria: {len(trayectoria_gps)} puntos")
        # Guardar en archivo de fumigación
        guardar_trayectoria_fumigacion()
        return True
    else:
        print(f"❌ GPS RECHAZADO: {lat:.6f}, {lon:.6f}")
        print(f"   Distancia: {distancia:.2f}m (mínimo 1.00m requerido)")
        return False

def limpiar_trayectoria_gps():
    """
    Limpia la trayectoria GPS al iniciar una nueva secuencia.
    """
    global trayectoria_gps, ultima_coordenada
    trayectoria_gps.clear()
    ultima_coordenada = None
    print("🗑️  Trayectoria GPS limpiada")    
    # Limpiar archivo de fumigación
    try:
        if TRAYECTORIA_FUMIGACION_FILE.exists():
            TRAYECTORIA_FUMIGACION_FILE.unlink()
            print("✓ Archivo de fumigación eliminado")
    except:
        pass

def guardar_trayectoria_fumigacion():
    """
    Guardar la trayectoria actual en archivo JSON para visualización en mapa.
    """
    try:
        with open(TRAYECTORIA_FUMIGACION_FILE, 'w') as f:
            json.dump({"puntos": trayectoria_gps}, f)
    except Exception as e:
        print(f"Error guardando trayectoria: {e}")
def mostrar_trayectoria_gps():
    """
    Muestra en consola todos los puntos GPS guardados en la trayectoria actual.
    """
    global trayectoria_gps, ultima_coordenada
    
    print("\n" + "="*60)
    print("📍 TRAYECTORIA GPS ACTUAL")
    print("="*60)
    print(f"Total de puntos guardados: {len(trayectoria_gps)}")
    
    if len(trayectoria_gps) == 0:
        print("⚠️  No hay puntos GPS guardados todavía")
    else:
        print("\nÚltima coordenada recibida:")
        if ultima_coordenada:
            print(f"  Lat: {ultima_coordenada[0]:.6f}, Lon: {ultima_coordenada[1]:.6f}")
        
        print(f"\nPrimeros 5 puntos:")
        for i, (lat, lon) in enumerate(trayectoria_gps[:5]):
            print(f"  {i+1}. Lat: {lat:.6f}, Lon: {lon:.6f}")
        
        if len(trayectoria_gps) > 10:
            print(f"  ... ({len(trayectoria_gps) - 10} puntos intermedios)")
        
        if len(trayectoria_gps) > 5:
            print(f"\nÚltimos 5 puntos:")
            for i, (lat, lon) in enumerate(trayectoria_gps[-5:]):
                idx = len(trayectoria_gps) - 5 + i + 1
                print(f"  {idx}. Lat: {lat:.6f}, Lon: {lon:.6f}")
        
        # Calcular distancia total aproximada
        distancia_total = 0
        for i in range(1, len(trayectoria_gps)):
            distancia_total += calcular_distancia_gps(
                trayectoria_gps[i-1][0], trayectoria_gps[i-1][1],
                trayectoria_gps[i][0], trayectoria_gps[i][1]
            )
        print(f"\n📏 Distancia total recorrida: {distancia_total:.2f} metros ({distancia_total/1000:.3f} km)")
    
    print("="*60 + "\n")

def buscar_puerto_arduino():
    """
    Busca automáticamente el puerto COM del Arduino en Windows o Linux.
    Retorna el nombre del puerto o None si no lo encuentra.
    """
    puertos = serial.tools.list_ports.comports()
    sistema = platform.system()
    
    for puerto in puertos:
        # En Windows buscar CH340, Arduino, USB-SERIAL
        if sistema == "Windows":
            if any(keyword in puerto.description.upper() for keyword in ["CH340", "ARDUINO", "USB-SERIAL"]):
                print(f"✓ Arduino encontrado: {puerto.device} - {puerto.description}")
                return puerto.device
        # En Linux buscar ttyUSB o ttyACM
        elif sistema == "Linux":
            if "ttyUSB" in puerto.device or "ttyACM" in puerto.device:
                print(f"✓ Arduino encontrado: {puerto.device} - {puerto.description}")
                return puerto.device
    
    print("✗ No se encontró Arduino conectado")
    return None

def conectar_arduino():
    """
    Busca y conecta con el Arduino automáticamente.
    """
    global arduino_port
    
    puerto = buscar_puerto_arduino()
    
    if puerto is None:
        print("✗ No se pudo encontrar el Arduino")
        return False
    
    try:
        arduino_port = serial.Serial(puerto, 9600, timeout=1)
        print(f"✓ Arduino conectado en {puerto}")
        return True
    except Exception as e:
        print(f"✗ Error al conectar Arduino: {e}")
        return False

def enviar_mensaje_arduino(mensaje):
    """
    Envía un mensaje al Arduino por puerto serial.
    """
    global arduino_port
    
    if arduino_port and arduino_port.is_open:
        try:
            arduino_port.write((mensaje + '\n').encode())
            print(f">>> Enviado a Arduino: {mensaje}")
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
    else:
        print("Arduino no conectado")

def leer_sensor_continuo(ui):
    """
    Lee continuamente los valores del sensor desde Arduino.
    """
    global arduino_port, lectura_activa, retraso_deteccion, tiempo_medidas, distancia_deteccion
    
    while lectura_activa:
        if arduino_port and arduino_port.is_open:
            try:
                if arduino_port.in_waiting > 0:
                    linea = arduino_port.readline().decode('utf-8').strip()
                    print(f"<<< Arduino: {linea}")  # Mostrar todo lo que envía el Arduino
                    
                    # Procesar mensajes de estado
                    if linea.startswith("ESTADO:"):
                        estado = linea.split(":")[1]
                        print(f"    Estado: {estado}")
                    
                    # Procesar versión del firmware
                    elif linea.startswith("VERSION:") or linea.startswith("FW:"):
                        # Acepta tanto "VERSION:1.0.0" como "FW:1.0.0"
                        separador = "VERSION:" if linea.startswith("VERSION:") else "FW:"
                        version = linea.split(separador)[1].strip()
                        if "page_0" in ui and "TextVersionFW" in ui["page_0"]:
                            ui["page_0"]["TextVersionFW"].text = f"Version FW: {version}"
                        print(f"    Versión FW recibida: {version}")
                    
                    # Procesar estado del relé
                    elif linea.startswith("RELE:"):
                        estado_rele = linea.split(":")[1].strip()
                        if "page_1" in ui:
                            if estado_rele == "ON" or estado_rele == "1":
                                # Relé activado - LED verde
                                ui["page_1"]["LedRele"].idle_color = (0, 200, 0, 1)  # Verde
                                ui["page_1"]["TextEstadoRele"].text = "FUMIGANDO"
                                ui["page_1"]["TextEstadoRele"].font_color = (0, 150, 0, 1)  # Verde oscuro
                                print(f"    Relé activado")
                            else:
                                # Relé desactivado - LED gris
                                ui["page_1"]["LedRele"].idle_color = (150, 150, 150, 1)  # Gris
                                ui["page_1"]["TextEstadoRele"].text = "DETENIDO"
                                ui["page_1"]["TextEstadoRele"].font_color = (100, 100, 100, 1)  # Gris oscuro
                                print(f"    Relé desactivado")
                    
                    # Procesar coordenadas GPS
                    elif linea.startswith("GPS:"):
                        try:
                            # Formato esperado: "GPS:latitud,longitud" o "GPS:NO_FIX"
                            datos_gps = linea[4:]  # Quitar "GPS:"
                            
                            if datos_gps == "NO_FIX":
                                # GPS sin señal satelital
                                print(f"    📡 GPS sin señal (buscando satélites...)")
                            else:
                                # Parsear coordenadas: "latitud,longitud"
                                partes = datos_gps.split(",")
                                if len(partes) == 2:
                                    lat = float(partes[0])
                                    lon = float(partes[1])
                                    
                                    # Guardar ubicación actual en archivo para el mapa
                                    try:
                                        with open(GPS_TEMP_FILE, 'w') as f:
                                            json.dump({"lat": lat, "lon": lon}, f)
                                    except:
                                        pass
                                    
                                    # Solo agregar a trayectoria de fumigación si NO está en modo mapas
                                    # (en modo mapas, gps_modo_mapas = True)
                                    if not gps_modo_mapas:
                                        agregar_coordenada_gps(lat, lon)
                                else:
                                    print(f"    ⚠ Formato GPS inválido: {linea}")
                                    print(f"    Partes recibidas: {partes}")
                        except ValueError as e:
                            print(f"    ⚠ Error parseando GPS: {e}")
                            print(f"    Datos recibidos: {linea}")
                    
                    # Procesar valores de configuración recibidos
                    elif linea.startswith("RETRASO:"):
                        valor = int(linea.split(":")[1])
                        retraso_deteccion = valor
                        ui["page_2"]["TextRetrasoValor"].text = str(valor)
                        print(f"    Retraso configurado: {valor}")
                    
                    elif linea.startswith("TIEMPO:"):
                        valor = int(linea.split(":")[1])
                        tiempo_medidas = valor
                        ui["page_2"]["TextTiempoValor"].text = str(valor)
                        print(f"    Tiempo configurado: {valor}")
                    
                    elif linea.startswith("DISTANCIA:"):
                        valor = int(linea.split(":")[1])
                        distancia_deteccion = valor
                        ui["page_2"]["TextDistanciaValor"].text = str(valor)
                        print(f"    Distancia configurada: {valor}")
                    
                    # Procesar valores de resultados de uso
                    elif linea.startswith("ARBOLES:"):
                        valor = int(linea.split(":")[1])
                        if "page_4" in ui and "TextArbolesValor" in ui["page_4"]:
                            ui["page_4"]["TextArbolesValor"].text = str(valor)
                        print(f"    Árboles fumigados: {valor}")
                    
                    elif linea.startswith("LITROS:"):
                        valor = float(linea.split(":")[1])
                        if "page_4" in ui and "TextLitrosValor" in ui["page_4"]:
                            ui["page_4"]["TextLitrosValor"].text = f"{valor:.1f}"
                            # Actualizar visualización del depósito (capacidad 600L)
                            capacidad_deposito = 600.0
                            litros_restantes = max(0, capacidad_deposito - valor)
                            # Altura máxima del depósito: 170px
                            altura_nivel = int((litros_restantes / capacidad_deposito) * 170)
                            # Ajustar posición Y para que baje desde arriba
                            pos_y = 395 + (170 - altura_nivel)
                            ui["page_4"]["DepositoNivel"].height = altura_nivel
                            ui["page_4"]["DepositoNivel"].y = pos_y
                        print(f"    Litros fumigados: {valor}")
                    
                    # Procesar valores numéricos del sensor
                    else:
                        try:
                            valor = int(linea)
                            # Actualizar los widgets en la interfaz
                            ui["page_3"]["TextValorSensor"].text = str(valor)
                            # Actualizar ancho de barra (máximo 500px para 200cm)
                            ancho_barra = min((valor / 200.0) * 500, 500)
                            ui["page_3"]["BarraDistancia"].width = int(ancho_barra)
                            print(f"    Sensor: {valor} cm")
                        except ValueError:
                            pass  # Ignorar líneas que no sean números ni comandos conocidos
            except Exception as e:
                print(f"Error al leer sensor: {e}")
        time.sleep(0.1)  # Leer cada 100ms

def iniciar_lectura_sensor(ui):
    """
    Inicia el hilo de lectura continua del sensor.
    """
    global lectura_activa, hilo_lectura
    
    if not lectura_activa:
        lectura_activa = True
        hilo_lectura = threading.Thread(target=leer_sensor_continuo, args=(ui,), daemon=True)
        hilo_lectura.start()
        print("Lectura de sensor iniciada")

def detener_lectura_sensor():
    """
    Detiene el hilo de lectura del sensor.
    """
    global lectura_activa
    lectura_activa = False
    print("Lectura de sensor detenida")


def hay_conectividad_tiles(timeout=1.5):
    """Verifica conectividad al servidor de tiles de mapas."""
    try:
        with socket.create_connection(("mt0.google.com", 443), timeout=timeout):
            return True
    except OSError:
        return False


def actualizar_estado_red_ui(ui, online):
    """Actualiza el indicador visual ONLINE/OFFLINE en la pantalla de inicio."""
    try:
        if "page_0" in ui and "TextEstadoMapa" in ui["page_0"]:
            if online:
                ui["page_0"]["TextEstadoMapa"].text = "ONLINE"
                ui["page_0"]["TextEstadoMapa"].font_color = (0, 150, 0, 1)
                if "IconWifiEstado" in ui["page_0"]:
                    ui["page_0"]["IconWifiEstado"].text = "📶"
                    ui["page_0"]["IconWifiEstado"].font_color = (0, 150, 0, 1)
            else:
                ui["page_0"]["TextEstadoMapa"].text = "OFFLINE"
                ui["page_0"]["TextEstadoMapa"].font_color = (180, 0, 0, 1)
                if "IconWifiEstado" in ui["page_0"]:
                    ui["page_0"]["IconWifiEstado"].text = "📵"
                    ui["page_0"]["IconWifiEstado"].font_color = (180, 0, 0, 1)
    except Exception:
        pass


def monitor_conectividad_mapa(ui):
    """Monitorea conectividad de mapas y refresca estado visual cada pocos segundos."""
    global monitoreo_red_activo
    estado_anterior = None

    while monitoreo_red_activo:
        online = hay_conectividad_tiles(timeout=1.5)

        if estado_anterior is None or online != estado_anterior:
            actualizar_estado_red_ui(ui, online)
            estado_anterior = online

        time.sleep(3)


def iniciar_monitor_conectividad(ui):
    """Inicia hilo daemon para monitor de conectividad online/offline."""
    global monitoreo_red_activo, hilo_monitoreo_red

    if monitoreo_red_activo:
        return

    monitoreo_red_activo = True
    hilo_monitoreo_red = threading.Thread(target=monitor_conectividad_mapa, args=(ui,), daemon=True)
    hilo_monitoreo_red.start()
    print("Monitor de conectividad de mapas iniciado")


def detener_monitor_conectividad():
    """Detiene monitor de conectividad de mapas."""
    global monitoreo_red_activo
    monitoreo_red_activo = False
    print("Monitor de conectividad de mapas detenido")

def configurar_webcam_ajuste(ui):
    """
    Evita que el widget de webcam cambie su geometria y estira la imagen
    para rellenar el area fija del widget.
    """
    cam = ui.get("page_1", {}).get("Webcam_4")
    if not cam:
        return

    # Importes locales para evitar dependencia global.
    import types
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QTransform

    def _configure_style_fill(self):
        if self._pixmap is None or self._pixmap.isNull():
            return

        transform = QTransform()
        if self._flip_h:
            transform.scale(-1, 1)
        if self._flip_v:
            transform.scale(1, -1)
        transform.rotate(self._rotate)

        transformed = self._pixmap.transformed(transform, Qt.SmoothTransformation)
        final_width = int(self._target_width * self._scale)
        final_height = int(self._target_height * self._scale)

        # Estirar para llenar el area del widget sin cambiar su geometria.
        self._pixmap = transformed.scaled(
            final_width,
            final_height,
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )

    cam.configure_style = types.MethodType(_configure_style_fill, cam)
    cam.setFixedSize(800, 450)

# ===================================================
# ============== 2. EVENT BINDINGS ==================
# ===================================================


def attach_events(ui):
    """
    Bind events to UI components.
    :param ui: Dictionary containing UI components.
    """
    # Botón "INICIO SECUENCIA" lleva a la página 1 e inicia la cámara
    def start_sequence(btn):
        enviar_mensaje_arduino("MENU SECUENCIA")  # Enviar al Arduino
        ui["pages"].set_current_page(1)
        # Reiniciar la cámara si es necesario
        if hasattr(ui.get("page_1", {}).get("Webcam_4"), 'start'):
            ui["page_1"]["Webcam_4"].start()
    
    ui["page_0"]["Button_0"].on_click = start_sequence
    
    # Botón "CONFIGURACION" lleva a la página 2
    def abrir_configuracion(btn):
        enviar_mensaje_arduino("MENU CONFIGURACIONES")  # Enviar al Arduino
        ui["pages"].set_current_page(2)
        # Esperar un momento para que lleguen los valores y actualizar UI
        time.sleep(0.5)
        ui["page_2"]["TextRetrasoValor"].text = str(retraso_deteccion)
        ui["page_2"]["TextTiempoValor"].text = str(tiempo_medidas)
        ui["page_2"]["TextDistanciaValor"].text = str(distancia_deteccion)
    
    ui["page_0"]["Button_1"].on_click = abrir_configuracion
    
    # Botón "PRUEBA SENSOR" lleva a la página 3
    def abrir_prueba_sensor(btn):
        enviar_mensaje_arduino("MENU PRUEBA SENSOR")  # Enviar al Arduino
        ui["pages"].set_current_page(3)
    
    ui["page_0"]["Button_2"].on_click = abrir_prueba_sensor
    
    # Variables para rastrear el estado de los modos
    modo_activo = {"automatico": False, "manual": False}
    color_fondo_original = (255, 255, 255, 1)
    color_fondo_activo = (200, 220, 255, 1)  # Azul claro para indicar selección
    
    # Estado de pausa (compartido entre funciones)
    pausa_activa = {"estado": False}
    
    # Botón "AUTOMATICO" en página 1
    def toggle_modo_automatico(btn):
        if modo_activo["automatico"]:
            # Desactivar modo automático
            enviar_mensaje_arduino("MENU SECUENCIA")
            enviar_mensaje_arduino("STOP_GPS")  # Detener envío de GPS
            ui["page_1"]["Button_3"].idle_color = color_fondo_original
            modo_activo["automatico"] = False
            # Ocultar botón de pausa y resetear texto
            if "ButtonPausa" in ui["page_1"]:
                ui["page_1"]["ButtonPausa"].is_visible = False
                ui["page_1"]["ButtonPausa"].text = "PAUSA"
                pausa_activa["estado"] = False
            print("Modo automático desactivado")
        else:
            # Primero desactivar manual si estaba activo
            if modo_activo["manual"]:
                ui["page_1"]["Button_1"].idle_color = color_fondo_original
                modo_activo["manual"] = False
            
            # Luego activar modo automático (sin limpiar trayectoria para acumular puntos)
            enviar_mensaje_arduino("MODO AUTOMATICO")
            ui["page_1"]["Button_3"].idle_color = color_fondo_activo
            modo_activo["automatico"] = True
            # Mostrar botón de pausa y resetear su estado
            if "ButtonPausa" in ui["page_1"]:
                ui["page_1"]["ButtonPausa"].is_visible = True
                ui["page_1"]["ButtonPausa"].text = "PAUSA"
                pausa_activa["estado"] = False
            print("Modo automático activado")
    
    # Botón "MANUAL" en página 1
    def toggle_modo_manual(btn):
        if modo_activo["manual"]:
            # Desactivar modo manual
            enviar_mensaje_arduino("MENU SECUENCIA")
            ui["page_1"]["Button_1"].idle_color = color_fondo_original
            modo_activo["manual"] = False
            print("Modo manual desactivado")
        else:
            # Primero desactivar automático si estaba activo
            if modo_activo["automatico"]:
                ui["page_1"]["Button_3"].idle_color = color_fondo_original
                modo_activo["automatico"] = False
                # Ocultar botón de pausa al cambiar a modo manual
                if "ButtonPausa" in ui["page_1"]:
                    ui["page_1"]["ButtonPausa"].is_visible = False
                    ui["page_1"]["ButtonPausa"].text = "PAUSA"
                    pausa_activa["estado"] = False
            
            # Luego activar modo manual (sin limpiar trayectoria para acumular puntos)
            enviar_mensaje_arduino("MODO MANUAL")
            ui["page_1"]["Button_1"].idle_color = color_fondo_activo
            modo_activo["manual"] = True
            print("Modo manual activado")
    
    if "page_1" in ui and "Button_3" in ui["page_1"]:
        ui["page_1"]["Button_3"].on_click = toggle_modo_automatico
    
    if "page_1" in ui and "Button_1" in ui["page_1"]:
        ui["page_1"]["Button_1"].on_click = toggle_modo_manual
    
    # Botón de pausa para modo automático
    def toggle_pausa(btn):
        if pausa_activa["estado"]:
            # Reanudar
            enviar_mensaje_arduino("PAUSAR")
            ui["page_1"]["ButtonPausa"].text = "PAUSA"
            pausa_activa["estado"] = False
            print("Secuencia reanudada")
        else:
            # Pausar
            enviar_mensaje_arduino("PAUSAR")
            ui["page_1"]["ButtonPausa"].text = "REANUDAR"
            pausa_activa["estado"] = True
            print("Secuencia pausada")
    
    if "page_1" in ui and "ButtonPausa" in ui["page_1"]:
        ui["page_1"]["ButtonPausa"].on_click = toggle_pausa
    
    # Botón "RESULTADOS" lleva a la página 4
    def abrir_resultados(btn):
        enviar_mensaje_arduino("MENU RESULTADOS USO")
        ui["pages"].set_current_page(4)
    
    ui["page_0"]["Button_4"].on_click = abrir_resultados
    
    # Botón "MAPAS" lleva a la página 5
    def abrir_menu_mapas(btn):
        enviar_mensaje_arduino("MENU MAPAS")
        ui["pages"].set_current_page(5)
    
    ui["page_0"]["Button_5"].on_click = abrir_menu_mapas
    
    # Iconos de página 1, 2, 3 y 4 vuelven a la página 0
    def volver_inicio(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    # Botón atrás de página 1 (modo funcionamiento) muestra trayectoria GPS
    def volver_desde_funcionamiento(icon):
        mostrar_trayectoria_gps()  # Mostrar trayectoria antes de salir

        
        # Resetear estado visual de los botones
        if modo_activo["automatico"]:
            ui["page_1"]["Button_3"].idle_color = color_fondo_original
            modo_activo["automatico"] = False
        if modo_activo["manual"]:
            ui["page_1"]["Button_1"].idle_color = color_fondo_original
            modo_activo["manual"] = False
        
        # Ocultar botón de pausa si está visible
        if "ButtonPausa" in ui["page_1"]:
            ui["page_1"]["ButtonPausa"].is_visible = False
            ui["page_1"]["ButtonPausa"].text = "PAUSA"
            pausa_activa["estado"] = False
        
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_1" in ui and "Icon_2" in ui["page_1"]:
        ui["page_1"]["Icon_2"].on_click = volver_desde_funcionamiento
    
    if "page_2" in ui and "Icon_1" in ui["page_2"]:
        ui["page_2"]["Icon_1"].on_click = volver_inicio
    
    # Icono de página 3 vuelve a página 0
    def volver_desde_prueba(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_3" in ui and "Icon_1" in ui["page_3"]:
        ui["page_3"]["Icon_1"].on_click = volver_desde_prueba
    
    # Icono de página 4 vuelve a página 0
    def volver_desde_resultados(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_4" in ui and "Icon_1" in ui["page_4"]:
        ui["page_4"]["Icon_1"].on_click = volver_desde_resultados
    
    # Icono de página 5 vuelve a página 0
    def volver_desde_mapa(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_5" in ui and "Icon_1" in ui["page_5"]:
        ui["page_5"]["Icon_1"].on_click = volver_desde_mapa
    
    # Botón "HUERTAS LEON 1" en página 5 abre directamente el mapa
    def abrir_huertas_leon_1(btn):
        global gps_modo_mapas
        # Pedir al Arduino que envíe GPS cada segundo
        gps_modo_mapas = True  # Activar modo mapas (no guardar en trayectoria)
        enviar_mensaje_arduino("START_GPS")
        enviar_mensaje_arduino("MAPA HUERTAS LEON 1")
        print("="*50)
        print("ABRIENDO MAPA HUERTAS DE LEÓN 1 DIRECTAMENTE")
        print("="*50)
        try:
            resultado = abrir_mapa('huertas_leon_1')
            print(f"Resultado: {resultado}")
        except Exception as e:
            print(f"Error al abrir mapa: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Desactivar GPS al cerrar el mapa
            enviar_mensaje_arduino("STOP_GPS")
            gps_modo_mapas = False  # Desactivar modo mapas
            print("GPS desactivado al cerrar mapa")
    
    if "page_5" in ui and "Button_3" in ui["page_5"]:
        ui["page_5"]["Button_3"].on_click = abrir_huertas_leon_1
    
    # Botón "HUERTAS LEON 2" en página 5 abre directamente el mapa
    def abrir_huertas_leon_2(btn):
        global gps_modo_mapas
        enviar_mensaje_arduino("START_GPS")
        gps_modo_mapas = True
        enviar_mensaje_arduino("MAPA HUERTAS LEON 2")
        print("="*50)
        print("ABRIENDO MAPA HUERTAS DE LEÓN 2 DIRECTAMENTE")
        print("="*50)
        try:
            resultado = abrir_mapa('huertas_leon_2')
            print(f"Resultado: {resultado}")
        except Exception as e:
            print(f"Error al abrir mapa: {e}")
            import traceback
            traceback.print_exc()
        finally:
            enviar_mensaje_arduino("STOP_GPS")
            gps_modo_mapas = False
            print("GPS desactivado al cerrar mapa")
    
    if "page_5" in ui and "Button_4" in ui["page_5"]:
        ui["page_5"]["Button_4"].on_click = abrir_huertas_leon_2
    
    # Botón "LANCHAR" en página 5 abre directamente el mapa
    def abrir_lanchar(btn):
        global gps_modo_mapas
        enviar_mensaje_arduino("START_GPS")
        gps_modo_mapas = True
        enviar_mensaje_arduino("MAPA LANCHAR")
        print("="*50)
        print("ABRIENDO MAPA LANCHAR DIRECTAMENTE")
        print("="*50)
        try:
            resultado = abrir_mapa('lanchar')
            print(f"Resultado: {resultado}")
        except Exception as e:
            print(f"Error al abrir mapa: {e}")
            import traceback
            traceback.print_exc()
        finally:
            enviar_mensaje_arduino("STOP_GPS")
            gps_modo_mapas = False
            print("GPS desactivado al cerrar mapa")
    
    if "page_5" in ui and "Button_6" in ui["page_5"]:
        ui["page_5"]["Button_6"].on_click = abrir_lanchar
    
    # Icono de página 6 vuelve a página 5 (menú mapas)
    def volver_desde_huertas_leon_1(icon):
        enviar_mensaje_arduino("MENU MAPAS")
        ui["pages"].set_current_page(5)
    
    if "page_6" in ui and "Icon_1" in ui["page_6"]:
        ui["page_6"]["Icon_1"].on_click = volver_desde_huertas_leon_1
    
    # Botón para abrir mapa interactivo en página 6
    def abrir_mapa_huertas_leon_1(btn):
        print("=" * 50)
        print("BOTÓN MAPA CLICKEADO")
        print(f"Función abrir_mapa: {abrir_mapa}")
        print(f"Módulo: {abrir_mapa.__module__}")
        print("=" * 50)
        try:
            print("Llamando a abrir_mapa('huertas_leon_1')...")
            resultado = abrir_mapa('huertas_leon_1')
            print(f"Resultado de abrir_mapa: {resultado}")
        except Exception as e:
            print(f"EXCEPCIÓN al abrir mapa: {e}")
            import traceback
            traceback.print_exc()
        print("=" * 50)
    
    if "page_6" in ui and "ButtonAbrirMapa" in ui["page_6"]:
        print("✓ Conectando evento on_click al botón 'ABRIR MAPA INTERACTIVO'")
        ui["page_6"]["ButtonAbrirMapa"].on_click = abrir_mapa_huertas_leon_1
        print(f"✓ Evento conectado. Handler: {ui['page_6']['ButtonAbrirMapa'].on_click}")
    else:
        print("✗ ERROR: No se encontró el botón ButtonAbrirMapa en page_6")
        print(f"   page_6 existe: {'page_6' in ui}")
        if 'page_6' in ui:
            print(f"   Elementos en page_6: {list(ui['page_6'].keys())}")
    
    # Controles de retraso de detección (solo modifican variables locales)
    def incrementar_retraso(btn):
        global retraso_deteccion
        retraso_deteccion += 10
        ui["page_2"]["TextRetrasoValor"].text = str(retraso_deteccion)
    
    def decrementar_retraso(btn):
        global retraso_deteccion
        retraso_deteccion = max(0, retraso_deteccion - 10)  # No permitir valores negativos
        ui["page_2"]["TextRetrasoValor"].text = str(retraso_deteccion)
    
    ui["page_2"]["ButtonRetrasoUp"].on_click = incrementar_retraso
    ui["page_2"]["ButtonRetrasoDown"].on_click = decrementar_retraso
    
    # Controles de tiempo de medidas (solo modifican variables locales)
    def incrementar_tiempo(btn):
        global tiempo_medidas
        tiempo_medidas += 10
        ui["page_2"]["TextTiempoValor"].text = str(tiempo_medidas)
    
    def decrementar_tiempo(btn):
        global tiempo_medidas
        tiempo_medidas = max(0, tiempo_medidas - 10)
        ui["page_2"]["TextTiempoValor"].text = str(tiempo_medidas)
    
    ui["page_2"]["ButtonTiempoUp"].on_click = incrementar_tiempo
    ui["page_2"]["ButtonTiempoDown"].on_click = decrementar_tiempo
    
    # Controles de distancia de detección (solo modifican variables locales)
    def incrementar_distancia(btn):
        global distancia_deteccion
        distancia_deteccion += 10
        ui["page_2"]["TextDistanciaValor"].text = str(distancia_deteccion)
    
    def decrementar_distancia(btn):
        global distancia_deteccion
        distancia_deteccion = max(0, distancia_deteccion - 10)
        ui["page_2"]["TextDistanciaValor"].text = str(distancia_deteccion)
    
    ui["page_2"]["ButtonDistanciaUp"].on_click = incrementar_distancia
    ui["page_2"]["ButtonDistanciaDown"].on_click = decrementar_distancia
    
    # Botón GUARDAR envía todas las configuraciones al Arduino
    def guardar_configuracion(btn):
        global retraso_deteccion, tiempo_medidas, distancia_deteccion
        print(f"Guardando configuración: Retraso={retraso_deteccion}, Tiempo={tiempo_medidas}, Distancia={distancia_deteccion}")
        enviar_mensaje_arduino(f"CONFIG_RETRASO:{retraso_deteccion}")
        time.sleep(0.1)  # Pequeña pausa entre comandos
        enviar_mensaje_arduino(f"CONFIG_TIEMPO:{tiempo_medidas}")
        time.sleep(0.1)
        enviar_mensaje_arduino(f"CONFIG_DISTANCIA:{distancia_deteccion}")
    
    ui["page_2"]["Button_5"].on_click = guardar_configuracion

# ===================================================
# ========= 2. SERVIDOR GPS WiFi ==================
# ===================================================

def iniciar_servidor_gps():
    """Inicia el servidor Flask para recibir GPS desde Android"""
    global servidor_gps_thread, servidor_gps_activo
    
    if not SERVIDOR_GPS_DISPONIBLE:
        print("⚠ Servidor GPS WiFi no disponible (instala Flask)")
        return False
    
    if servidor_gps_activo:
        print("⚠ Servidor GPS WiFi ya está en ejecución")
        return False
    
    try:
        print("\n🚀 Iniciando Servidor GPS WiFi...")
        servidor_gps_thread = iniciar_servidor_thread(puerto=PUERTO_SERVIDOR_GPS)
        servidor_gps_activo = True
        print(f"✅ Servidor GPS WiFi iniciado en puerto {PUERTO_SERVIDOR_GPS}")
        print(f"   Endpoint: POST http://<IP_RASPBERRY>:{PUERTO_SERVIDOR_GPS}/gps")
        print(f"   Esperando datos de Tasker en Android...\n")
        return True
    except Exception as e:
        print(f"❌ Error iniciando Servidor GPS WiFi: {e}")
        servidor_gps_activo = False
        return False

def detener_servidor_gps():
    """Detiene el servidor Flask (nota: Flask corre en daemon thread)"""
    global servidor_gps_activo
    
    if not servidor_gps_activo:
        return
    
    try:
        print("\n🛑 Deteniendo Servidor GPS WiFi...")
        servidor_gps_activo = False
        # Nota: Flask corre en thread daemon, se cerrará cuando termina la app
        print("✓ Servidor GPS WiFi detenido\n")
    except Exception as e:
        print(f"⚠ Error deteniendo Servidor GPS WiFi: {e}")

# ===================================================
# ============== 3. MAIN FUNCTION ==================
# ===================================================


def main():
    print("=" * 50, flush=True)
    print("INICIANDO APLICACIÓN PYVISUAL", flush=True)
    print("=" * 50, flush=True)
    
    # Inicializar archivo de ubicación GPS actual
    try:
        if GPS_TEMP_FILE.exists():
            print("  → Limpiando archivo GPS anterior...", flush=True)
            GPS_TEMP_FILE.unlink()
        else:
            print("  → Creando archivo GPS...", flush=True)
        
        GPS_TEMP_FILE.write_text(json.dumps({"lat": 0.0, "lon": 0.0}))
        print("✓ Archivo GPS temporal inicializado", flush=True)
    except Exception as e:
        print(f"⚠ Error inicializando archivo GPS: {e}", flush=True)
    
    # Inicializar archivo de trayectoria de fumigación
    try:
        if TRAYECTORIA_FUMIGACION_FILE.exists():
            print("  → Limpiando archivo de fumigación anterior...", flush=True)
            TRAYECTORIA_FUMIGACION_FILE.unlink()
        else:
            print("  → Creando archivo de fumigación...", flush=True)
        
        TRAYECTORIA_FUMIGACION_FILE.write_text(json.dumps({"puntos": []}))
        print("✓ Archivo de fumigación inicializado", flush=True)
    except Exception as e:
        print(f"⚠ Error inicializando archivo de fumigación: {e}", flush=True)
    
    # Conectar con Arduino al iniciar
    print("\n[1] Buscando Arduino...", flush=True)
    if conectar_arduino():
        # Esperar a que Arduino se inicialice (reset al conectar serial)
        print("[2] Esperando inicialización del Arduino...", flush=True)
        time.sleep(2)
    else:
        print("[!] ADVERTENCIA: No se pudo conectar con Arduino", flush=True)
    
    print("[3] Creando interfaz gráfica...", flush=True)
    app = pv.PvApp()
    
    try:
        ui = create_ui()
        print(f"    Páginas creadas: {list(ui.keys())}", flush=True)
    except Exception as e:
        print(f"    ✗ Error al crear UI: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return

    configurar_webcam_ajuste(ui)
    
    attach_events(ui)
    
    # Iniciar hilo de lectura serial desde el inicio
    print("[4] Iniciando lectura del puerto serial...", flush=True)
    iniciar_lectura_sensor(ui)

    # Iniciar monitor visual online/offline para mapas
    iniciar_monitor_conectividad(ui)
    
    # Solicitar información inicial del Arduino
    if arduino_port and arduino_port.is_open:
        print("[5] Solicitando información inicial del Arduino...", flush=True)
        time.sleep(0.5)  # Dar tiempo al hilo de lectura para iniciarse
        
        # Solicitar versión del firmware
        enviar_mensaje_arduino("GET_VERSION")
        time.sleep(0.3)
        
        # Solicitar configuración inicial
        enviar_mensaje_arduino("MENU CONFIGURACIONES")
        time.sleep(1)  # Esperar a que lleguen los valores
        print(f"[6] Valores recibidos - Retraso: {retraso_deteccion}, Tiempo: {tiempo_medidas}, Distancia: {distancia_deteccion}", flush=True)
    
    # Iniciar servidor GPS WiFi
    print("[7] Iniciando servidor GPS WiFi...", flush=True)
    iniciar_servidor_gps()
    print("[8] Mostrando ventana...", flush=True)
    print("=" * 50, flush=True)
    ui["window"].show()
    app.run()
    
    # Detener lectura y cerrar puerto serial al salir
    detener_lectura_sensor()
    detener_monitor_conectividad()
    detener_servidor_gps()
    if arduino_port and arduino_port.is_open:
        arduino_port.close()
        print("Conexión con Arduino cerrada")


if __name__ == '__main__':
    main()
