import pyvisual as pv
from ui.ui import create_ui

# ===================================================
# ================ 1. LOGIC CODE ====================
# ===================================================

# Variables de configuración
retraso_deteccion = 0
tiempo_medidas = 0
distancia_deteccion = 0

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
        ui["pages"].set_current_page(1)
        # Reiniciar la cámara si es necesario
        if hasattr(ui["page_1"]["Webcam_4"], 'start'):
            ui["page_1"]["Webcam_4"].start()
    
    ui["page_0"]["Button_0"].on_click = start_sequence
    
    # Botón "CONFIGURACION" lleva a la página 2
    ui["page_0"]["Button_1"].on_click = lambda btn: ui["pages"].set_current_page(2)
    
    # Iconos de página 1 y 2 vuelven a la página 0
    ui["page_1"]["Icon_2"].on_click = lambda icon: ui["pages"].set_current_page(0)
    ui["page_2"]["Icon_1"].on_click = lambda icon: ui["pages"].set_current_page(0)
    
    # Controles de retraso de detección
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
    
    # Controles de tiempo de medidas
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
    
    # Controles de distancia de detección
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

# ===================================================
# ============== 3. MAIN FUNCTION ==================
# ===================================================


def main():
    app = pv.PvApp()
    ui = create_ui()
    attach_events(ui)
    ui["window"].show()
    app.run()


if __name__ == '__main__':
    main()
