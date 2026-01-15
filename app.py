import pyvisual as pv
from ui.ui import create_ui
import serial
import serial.tools.list_ports
import threading
import time
import platform
import sys

# Forzar salida inmediata de prints
sys.stdout.flush()

# ===================================================
# ================ 1. LOGIC CODE ====================
# ===================================================

# Variables de configuración
retraso_deteccion = 0
tiempo_medidas = 0
distancia_deteccion = 0

# Configuración del puerto serial
arduino_port = None
lectura_activa = False
hilo_lectura = None

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
    
    # Botón "RESULTADOS" - sin acción por ahora
    # ui["page_0"]["Button_4"].on_click = lambda btn: ui["pages"].set_current_page(3)
    
    # Iconos de página 1, 2 y 3 vuelven a la página 0
    def volver_inicio(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_1" in ui and "Icon_2" in ui["page_1"]:
        ui["page_1"]["Icon_2"].on_click = volver_inicio
    
    if "page_2" in ui and "Icon_1" in ui["page_2"]:
        ui["page_2"]["Icon_1"].on_click = volver_inicio
    
    # Icono de página 3 vuelve a página 0
    def volver_desde_prueba(icon):
        enviar_mensaje_arduino("MENU INICIO")
        ui["pages"].set_current_page(0)
    
    if "page_3" in ui and "Icon_1" in ui["page_3"]:
        ui["page_3"]["Icon_1"].on_click = volver_desde_prueba
    
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
# ============== 3. MAIN FUNCTION ==================
# ===================================================


def main():
    print("=" * 50, flush=True)
    print("INICIANDO APLICACIÓN PYVISUAL", flush=True)
    print("=" * 50, flush=True)
    
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
    
    attach_events(ui)
    
    # Iniciar hilo de lectura serial desde el inicio
    print("[4] Iniciando lectura del puerto serial...", flush=True)
    iniciar_lectura_sensor(ui)
    
    # Solicitar configuración inicial del Arduino
    if arduino_port and arduino_port.is_open:
        print("[5] Solicitando configuración inicial...", flush=True)
        time.sleep(0.5)  # Dar tiempo al hilo de lectura para iniciarse
        enviar_mensaje_arduino("MENU CONFIGURACIONES")
        time.sleep(1)  # Esperar a que lleguen los valores
        print(f"[6] Valores recibidos - Retraso: {retraso_deteccion}, Tiempo: {tiempo_medidas}, Distancia: {distancia_deteccion}", flush=True)
    
    print("[7] Mostrando ventana...", flush=True)
    print("=" * 50, flush=True)
    ui["window"].show()
    app.run()
    
    # Detener lectura y cerrar puerto serial al salir
    detener_lectura_sensor()
    if arduino_port and arduino_port.is_open:
        arduino_port.close()
        print("Conexión con Arduino cerrada")


if __name__ == '__main__':
    main()
