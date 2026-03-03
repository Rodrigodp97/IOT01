"""
Script independiente para abrir mapas interactivos
Ejecutar con: python abrir_mapa_standalone.py <nombre_mapa>
"""
import sys
import tkinter as tk
import tkintermapview
from pathlib import Path
import json
import math
import socket

# Configuraciones de mapas
MAPAS = {
    'huertas_leon_1': {
        'titulo': 'Huertas de Leon 1',
        'latitud': 38.63589588416404,
        'longitud': -2.9156099448703148,
        'zoom': 19  # Zoom con tiles completos
    },
    'hoya_del_herrero': {
        'titulo': 'Hoya del Herrero',
        'latitud': 38.6400,
        'longitud': -2.9200,
        'zoom': 19
    },
    'manzanos': {
        'titulo': 'Manzanos',
        'latitud': 38.6300,
        'longitud': -2.9100,
        'zoom': 19
    },
    'huertas_leon_2': {
        'titulo': 'Huertas de Leon 2',
        'latitud': 38.63390691618973,
        'longitud': -2.915841447227996,
        'zoom': 19
    },
    'lanchar': {
        'titulo': 'Lanchar',
        'latitud': 38.63058602411473,
        'longitud': -2.9116130259917177,
        'zoom': 19
    },
    'burraquero': {
        'titulo': 'Burraquero',
        'latitud': 38.6380,
        'longitud': -2.9180,
        'zoom': 19
    }
}

class VentanaMapa:
    def __init__(self, titulo, latitud, longitud, zoom=17):
        self.titulo = titulo
        self.latitud = latitud
        self.longitud = longitud
        self.zoom = zoom
        self.puntos_marcados = []
        self.marcador_gps = None
        self.gps_file = Path(__file__).parent / "gps_actual.json"
        self.fumigacion_file = Path(__file__).parent / "fumigacion_trayectoria.json"
        self.zonas_fumigadas = []  # Lista de poligonos de zonas fumigadas

    def _hay_conectividad_tiles(self, timeout=1.5):
        """Verificar conectividad basica al servidor de tiles."""
        try:
            with socket.create_connection(("mt0.google.com", 443), timeout=timeout):
                return True
        except OSError:
            return False
        
    def abrir(self):
        # Crear ventana
        self.root = tk.Tk()
        self.root.title(self.titulo)
        self.root.geometry("1024x600")
        
        # Configurar modo de mapa (online/offline)
        db_path = Path(__file__).parent / "offline_map.db"
        tiene_db_offline = db_path.exists()
        online_disponible = self._hay_conectividad_tiles(timeout=1.5)
        use_offline = tiene_db_offline and not online_disponible

        if online_disponible:
            print("[OK] Modo ONLINE activado")
            if tiene_db_offline:
                print(f"  Base offline disponible como respaldo: {db_path}")
        elif use_offline:
            print(f"[OK] Modo OFFLINE activado")
            print(f"  Base de datos: {db_path}")
            print(f"  Tamano: {db_path.stat().st_size / 1024 / 1024:.2f} MB")
        else:
            print("[WARN] Sin conectividad al servidor de tiles y sin base offline")
            print(f"  Base no encontrada: {db_path}")
            print("  El mapa puede abrir, pero sin tiles visibles hasta recuperar conexion")
        
        # Crear widget de mapa con configuracion offline
        # Zoom maximo limitado a 19 (maximo nivel descargado en tiles offline)
        self.map_widget = tkintermapview.TkinterMapView(
            self.root, 
            width=1024, 
            height=600, 
            corner_radius=0,
            database_path=str(db_path) if use_offline else None,
            use_database_only=use_offline,  # CRITICO: Solo usar base de datos, no descargar
            max_zoom=19  # Zoom maximo de tiles descargados
        )
        
        # Limitar zoom minimo a 15 (nivel minimo descargado)
        self.min_zoom_permitido = 15
        
        # Sobrescribir metodo de zoom del mouse para controlar limites
        self._mouse_zoom_original = self.map_widget.mouse_zoom
        self.map_widget.mouse_zoom = self._mouse_zoom_limitado
        
        self.map_widget.pack(fill="both", expand=True)
        
        # Configurar servidor de tiles (para identificacion del formato)
        # Vista Satelite de Google
        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}",
            max_zoom=19  # Limitado al zoom maximo de tiles descargados
        )
        
        # Posicionar con zoom maximo disponible (19) para maximo detalle
        self.map_widget.set_position(self.latitud, self.longitud)
        self.map_widget.set_zoom(19)  # Zoom maximo de tiles descargados
        
        # Marcador central deshabilitado (no se necesita por ahora)
        # self.marker_centro = self.map_widget.set_marker(
        #     self.latitud, self.longitud,
        #     text=self.titulo,
        #     marker_color_circle="red",
        #     marker_color_outside="darkred"
        # )
        
        # Eventos
        # Click deshabilitado por ahora (se anadiran marcadores mas adelante)
        # self.map_widget.add_left_click_map_command(self._click_en_mapa)
        
        # Verificar limites de zoom continuamente
        self._verificar_limites_zoom()
        
        # Cargar y mostrar zonas fumigadas al inicio
        self._cargar_zonas_fumigadas()
        
        # Iniciar actualizacion de posicion GPS cada segundo
        self._actualizar_gps()
        
        # Panel de info
        self._crear_panel_info()
        
        # Al cerrar, limpiar archivo GPS
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Loop
        self.root.mainloop()
    
    def _mouse_zoom_limitado(self, event):
        """Interceptar zoom del mouse para aplicar limites"""
        # Calcular nuevo zoom antes de aplicarlo
        zoom_antes = self.map_widget.zoom
        
        # Llamar al zoom original
        self._mouse_zoom_original(event)
        
        # Verificar y corregir si se sale de limites
        zoom_despues = self.map_widget.zoom
        if zoom_despues < self.min_zoom_permitido:
            self.map_widget.set_zoom(self.min_zoom_permitido)
    
    def _verificar_limites_zoom(self):
        """Verificar y ajustar el zoom si esta fuera de limites continuamente"""
        try:
            zoom_actual = round(self.map_widget.zoom)
            if zoom_actual < self.min_zoom_permitido:
                self.map_widget.set_zoom(self.min_zoom_permitido)
            # Verificar cada 50ms (mas rapido)
            self.root.after(50, self._verificar_limites_zoom)
        except:
            # Si hay error (ventana cerrada), no continuar
            pass
    
    def _click_en_mapa(self, coords):
        lat, lon = coords
        print(f"Click: {lat:.6f}, {lon:.6f}")
        
        punto = self.map_widget.set_marker(
            lat, lon,
            text=f"P{len(self.puntos_marcados)+1}",
            marker_color_circle="blue",
            marker_color_outside="darkblue"
        )
        
        self.puntos_marcados.append({'lat': lat, 'lon': lon, 'marker': punto})
        self._actualizar_info()
    
    def _limpiar_puntos(self):
        for punto in self.puntos_marcados:
            punto['marker'].delete()
        self.puntos_marcados.clear()
        self._actualizar_info()
    
    def _actualizar_info(self):
        if hasattr(self, 'label_puntos'):
            self.label_puntos.config(text=f"Puntos: {len(self.puntos_marcados)}")
    
    def _crear_panel_info(self):
        info_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, borderwidth=2)
        info_frame.place(x=10, y=10, width=280, height=180)
        
        # Titulo
        tk.Label(info_frame, text=self.titulo, font=("Arial", 12, "bold"), bg="white").pack(pady=15)
        
        # Botones de zoom
        zoom_frame = tk.Frame(info_frame, bg="white")
        zoom_frame.pack(pady=10)
        
        tk.Button(zoom_frame, text="+", command=self._zoom_mas, 
                 bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), 
                 cursor="hand2", width=5, height=1).pack(side=tk.LEFT, padx=5)
        
        tk.Button(zoom_frame, text="-", command=self._zoom_menos, 
                 bg="#2196F3", fg="white", font=("Arial", 14, "bold"), 
                 cursor="hand2", width=5, height=1).pack(side=tk.LEFT, padx=5)
        
        # Boton de cerrar
        tk.Button(info_frame, text="<- CERRAR MAPA", command=self.root.destroy, 
                 bg="#424242", fg="white", font=("Arial", 10, "bold"), 
                 cursor="hand2", relief=tk.RAISED, bd=2).pack(pady=10, fill=tk.X, padx=10)
    
    def _zoom_mas(self):
        """Aumentar zoom (acercar)"""
        zoom_actual = self.map_widget.zoom
        if zoom_actual < 19:  # Zoom maximo descargado
            self.map_widget.set_zoom(zoom_actual + 1)
    
    def _zoom_menos(self):
        """Disminuir zoom (alejar)"""
        zoom_actual = self.map_widget.zoom
        if zoom_actual > self.min_zoom_permitido:
            self.map_widget.set_zoom(zoom_actual - 1)
    
    def _actualizar_gps(self):
        """Leer archivo GPS y actualizar circulo azul cada segundo"""
        try:
            if self.gps_file.exists():
                with open(self.gps_file, 'r') as f:
                    data = json.load(f)
                    lat = data.get('lat', 0.0)
                    lon = data.get('lon', 0.0)
                    
                    # Solo actualizar si hay coordenadas validas
                    if lat != 0.0 and lon != 0.0:
                        # Eliminar marcador anterior
                        if self.marcador_gps is not None:
                            self.marcador_gps.delete()
                        
                        # Crear circulo puro usando poligono
                        # Radio en grados (aprox. 1.5 metros en esta latitud)
                        radio = 0.000015
                        puntos_circulo = []
                        
                        # Generar puntos del circulo (36 puntos = cada 10 grados)
                        for i in range(36):
                            angulo = math.radians(i * 10)
                            lat_punto = lat + radio * math.sin(angulo)
                            lon_punto = lon + radio * math.cos(angulo)
                            puntos_circulo.append((lat_punto, lon_punto))
                        
                        # Dibujar circulo azul con borde claro
                        self.marcador_gps = self.map_widget.set_polygon(
                            puntos_circulo,
                            fill_color="#0099FF",      # Azul brillante solido
                            outline_color="#0066CC",   # Azul mas oscuro en borde
                            border_width=8,            # Borde grueso para mas visibilidad
                            name="gps_position"
                        )
        except Exception as e:
            pass  # Ignorar errores silenciosamente
        
        # Repetir en 1 segundo
        self.root.after(1000, self._actualizar_gps)
    
    def _cargar_zonas_fumigadas(self):
        """Cargar y mostrar zonas fumigadas desde el archivo"""
        try:
            if self.fumigacion_file.exists():
                with open(self.fumigacion_file, 'r') as f:
                    data = json.load(f)
                    puntos = data.get('puntos', [])
                    
                    if len(puntos) > 0:
                        print(f"[OK] Cargando {len(puntos)} puntos de fumigacion")
                        
                        # Crear circulos sombreados para cada punto fumigado
                        for lat, lon in puntos:
                            # Radio del area fumigada (~1.5 metros)
                            radio = 0.000015
                            puntos_circulo = []
                            
                            # Generar puntos del circulo
                            for i in range(24):  # 24 puntos = suficiente para circulo suave
                                angulo = math.radians(i * 15)
                                lat_punto = lat + radio * math.sin(angulo)
                                lon_punto = lon + radio * math.cos(angulo)
                                puntos_circulo.append((lat_punto, lon_punto))
                            
                            # Dibujar zona fumigada (verde translucido)
                            zona = self.map_widget.set_polygon(
                                puntos_circulo,
                                fill_color="#90EE90",      # Verde claro translucido
                                outline_color="#228B22",   # Verde oscuro borde
                                border_width=1,
                                name=f"fumigacion_{len(self.zonas_fumigadas)}"
                            )
                            self.zonas_fumigadas.append(zona)
                        
                        print(f"[OK] {len(self.zonas_fumigadas)} zonas fumigadas mostradas")
        except Exception as e:
            print(f"Error cargando zonas fumigadas: {e}")
    
    def _on_closing(self):
        """Limpiar archivo GPS y cerrar ventana"""
        try:
            if self.gps_file.exists():
                self.gps_file.unlink()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    # Obtener nombre del mapa desde argumentos
    if len(sys.argv) < 2:
        print("Uso: python abrir_mapa_standalone.py <nombre_mapa>")
        print(f"Mapas disponibles: {', '.join(MAPAS.keys())}, ubicacion_actual")
        sys.exit(1)
    
    nombre_mapa = sys.argv[1]
    
    # Caso especial: mapa en ubicacion actual (lectura de GPS en tiempo real)
    if nombre_mapa == 'ubicacion_actual':
        print("="*60)
        print("Abriendo mapa en ubicacion actual...")
        print("="*60)
        gps_file = Path(__file__).parent / "gps_actual.json"
        
        print(f"[INFO] Buscando archivo: {gps_file}")
        print(f"   Existe: {gps_file.exists()}")
        
        try:
            # Forzar lectura fresh del archivo
            with open(gps_file, 'r') as f:
                contenido_raw = f.read()
                print(f"   Contenido raw: {contenido_raw}")
                gps_data = json.loads(contenido_raw)
                
            lat = float(gps_data.get('lat', 38.6358))
            lon = float(gps_data.get('lon', -2.9156))
            
            print(f"[OK] Ubicacion GPS:")
            print(f"   Latitud:  {lat:.6f}")
            print(f"   Longitud: {lon:.6f}")
        except FileNotFoundError:
            print(f"[WARN] Archivo no encontrado, usando ubicacion por defecto")
            lat = 38.6358
            lon = -2.9156
        except Exception as e:
            print(f"[WARN] Error leyendo GPS: {e}")
            print(f"   Usando ubicacion por defecto: 38.6358, -2.9156")
            lat = 38.6358
            lon = -2.9156
        
        config = {
            'titulo': 'Mi Ubicacion Actual',
            'latitud': lat,
            'longitud': lon,
            'zoom': 19
        }
        print("="*60)
    elif nombre_mapa not in MAPAS:
        print(f"Error: Mapa '{nombre_mapa}' no encontrado")
        print(f"Mapas disponibles: {', '.join(MAPAS.keys())}, ubicacion_actual")
        sys.exit(1)
    else:
        config = MAPAS[nombre_mapa]
    
    print(f"Abriendo {config['titulo']}...")
    
    mapa = VentanaMapa(
        titulo=config['titulo'],
        latitud=config['latitud'],
        longitud=config['longitud'],
        zoom=config['zoom']
    )
    
    mapa.abrir()
