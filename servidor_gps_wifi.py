"""
Servidor Flask para recibir ubicacion GPS desde Android via WiFi
Escucha en puerto 5000 en localhost
Endpoint: POST /gps con JSON {"lat": latitud, "lon": longitud}
"""

from flask import Flask, request, jsonify
from pathlib import Path
import json
import threading
import time
from datetime import datetime

# Crear aplicacion Flask
app = Flask(__name__)

# Archivo donde guardar la ultima ubicacion GPS
SCRIPT_DIR = Path(__file__).parent
GPS_FILE = SCRIPT_DIR / "gps_actual.json"
LOG_FILE = SCRIPT_DIR / "servidor_gps_log.txt"

# Asegurar que el archivo existe
if not GPS_FILE.exists():
    with open(GPS_FILE, 'w') as f:
        json.dump({"lat": 0.0, "lon": 0.0}, f)


def registrar_log(mensaje):
    """Registra mensajes en archivo de log con timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] {mensaje}"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(linea + "\n")
        print(linea, flush=True)  # Tambien imprimir en consola con flush
    except Exception as e:
        print(f"Error escribiendo log: {e}", flush=True)


def _parsear_gps_entrada():
    """
    Intenta extraer lat/lon desde JSON, form-data, query params o texto plano.
    Retorna tuple (lat, lon) o (None, None) si no se puede parsear.
    """
    print(f"[DEBUG] Iniciando parseo de GPS...", flush=True)
    print(f"[DEBUG] Content-Type: {request.content_type}", flush=True)
    print(f"[DEBUG] request.data: {request.data[:200]}", flush=True)
    
    # 1) JSON (dict o lista)
    print(f"[DEBUG] Intentando JSON...", flush=True)
    data = request.get_json(force=True, silent=True)
    print(f"[DEBUG] JSON resultado: {data}", flush=True)
    print(f"[DEBUG] Data es dict? {isinstance(data, dict)}, es list? {isinstance(data, list)}", flush=True)
    
    if isinstance(data, dict):
        print(f"[DEBUG] Procesando como dict", flush=True)
        lat = data.get('lat', data.get('latitude'))
        lon = data.get('lon', data.get('lng', data.get('longitude')))
        print(f"[DEBUG] Dict: lat={lat}, lon={lon}", flush=True)
        if lat is not None and lon is not None:
            return lat, lon
    elif isinstance(data, list) and len(data) >= 2:
        print(f"[DEBUG] Procesando como list: {data}", flush=True)
        return data[0], data[1]

    # 2) Form data o query params
    print(f"[DEBUG] Intentando form/query params...", flush=True)
    lat = request.form.get('lat') or request.args.get('lat')
    lon = request.form.get('lon') or request.args.get('lon')
    print(f"[DEBUG] Form/Query: lat={lat}, lon={lon}", flush=True)
    if lat is not None and lon is not None:
        return lat, lon

    # 3) Texto plano: "lat,lon" o "lat lon" o "lat;lon"
    print(f"[DEBUG] Intentando texto plano...", flush=True)
    texto = request.data.decode('utf-8', errors='replace').strip()
    print(f"[DEBUG] Texto plano: '{texto}'", flush=True)
    
    if texto:
        for sep in [',', ';', ' ']:
            print(f"[DEBUG]   Probando separador: '{sep}'", flush=True)
            partes = texto.split(sep)
            print(f"[DEBUG]   Split resultado: {partes}", flush=True)
            partes = [p.strip() for p in partes if p.strip()]
            print(f"[DEBUG]   Limpiado: {partes}", flush=True)
            
            if len(partes) == 2:
                print(f"[DEBUG]   OK Encontrado: {partes[0]}, {partes[1]}", flush=True)
                return partes[0], partes[1]

    print(f"[DEBUG] No se pudo extraer lat/lon", flush=True)
    return None, None


@app.route('/gps', methods=['POST'])
def recibir_gps():
    """
    Endpoint para recibir ubicacion GPS desde Android
    
    Request body esperado:
    {
        "lat": latitud (float),
        "lon": longitud (float)
    }
    
    Returns:
        JSON con estado de la operacion
    """
    try:
        # LOGGING DE DEBUG: Mostrar todo lo que llega
        registrar_log(f"[POST /gps] Nueva peticion recibida")
        registrar_log(f"   Content-Type: {request.content_type}")
        registrar_log(f"   Body RAW: {request.data.decode('utf-8', errors='replace')[:500]}")
        
        # Obtener datos del request (JSON, form, query o texto plano)
        lat, lon = _parsear_gps_entrada()
        registrar_log(f"   Parseo resultado: lat={lat}, lon={lon}")
        
        # Validar que existan lat y lon
        if lat is None or lon is None:
            registrar_log("[ERROR] POST /gps - No se pudo extraer lat/lon")
            return jsonify({
                'error': 'Missing or invalid lat/lon data',
                'status': 'error'
            }), 400
        
        # Validar que sean numeros validos
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            registrar_log(f"[ERROR] POST /gps - Valores lat/lon no son numeros: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'lat and lon must be valid numbers',
                'status': 'error'
            }), 400
        
        # Validar rango de coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            registrar_log(f"[ERROR] POST /gps - Rango invalido: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'Invalid coordinate range (lat: -90 to 90, lon: -180 to 180)',
                'status': 'error'
            }), 400
        
        # Guardar en archivo
        gps_data = {
            "lat": lat,
            "lon": lon,
            "timestamp": time.time()  # Agregar marca de tiempo
        }
        
        with open(GPS_FILE, 'w') as f:
            json.dump(gps_data, f)
        
        registrar_log(f"[OK] GPS RECIBIDO: lat={lat:.6f}, lon={lon:.6f}")
        
        return jsonify({
            'status': 'success',
            'lat': lat,
            'lon': lon,
            'message': 'GPS updated successfully'
        }), 200
    
    except Exception as e:
        registrar_log(f"[ERROR] Error en /gps: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/update_gps', methods=['GET'])
def update_gps_get():
    """
    Endpoint GET para actualizar GPS (compatible con Tasker)
    Uso: /update_gps?lat=38.635896&lon=-2.915610
    """
    try:
        # LOGGING DE DEBUG: Mostrar peticion GET
        registrar_log(f"[GET /update_gps] Nueva peticion recibida")
        registrar_log(f"   URL completa: {request.url}")
        registrar_log(f"   Parametros: {dict(request.args)}")
        
        # Obtener parametros de la URL
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if lat is None or lon is None:
            registrar_log(f"[ERROR] GET /update_gps - Faltan parametros lat/lon")
            return jsonify({
                'error': 'Missing "lat" or "lon" parameters',
                'status': 'error',
                'usage': '/update_gps?lat=38.635896&lon=-2.915610'
            }), 400
        
        # Validar que sean numeros validos
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            registrar_log(f"[ERROR] GET /update_gps - Valores no numericos: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'lat and lon must be valid numbers',
                'status': 'error'
            }), 400
        
        # Validar rango de coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            registrar_log(f"[ERROR] GET /update_gps - Rango invalido: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'Invalid coordinate range (lat: -90 to 90, lon: -180 to 180)',
                'status': 'error'
            }), 400
        
        # Guardar en archivo
        gps_data = {
            "lat": lat,
            "lon": lon,
            "timestamp": time.time()
        }
        
        with open(GPS_FILE, 'w') as f:
            json.dump(gps_data, f)
        
        registrar_log(f"[OK] GPS RECIBIDO (GET): lat={lat:.6f}, lon={lon:.6f}")
        
        return jsonify({
            'status': 'success',
            'lat': lat,
            'lon': lon,
            'message': 'GPS updated successfully'
        }), 200
    
    except Exception as e:
        registrar_log(f"[ERROR] Error en /update_gps: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/test', methods=['POST', 'GET'])
def test():
    """
    Endpoint de prueba simple
    Usalo para verificar conectividad basica
    """
    registrar_log(f"[OK] TEST - Solicitud recibida ({request.method})")
    return jsonify({
        'status': 'ok',
        'message': 'Servidor esta respondiendo correctamente'
    }), 200


@app.route('/status', methods=['GET'])
def status():
    """
    Endpoint para verificar si el servidor esta activo
    y obtener la ultima ubicacion GPS conocida
    """
    try:
        if GPS_FILE.exists():
            with open(GPS_FILE, 'r') as f:
                gps_data = json.load(f)
        else:
            gps_data = {"lat": 0.0, "lon": 0.0}
        
        registrar_log(f"[STATUS] GPS actual: {gps_data}")
        
        return jsonify({
            'status': 'online',
            'server': 'WiFi GPS Server',
            'gps_data': gps_data
        }), 200
    
    except Exception as e:
        registrar_log(f"[ERROR] Error en /status: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


def iniciar_servidor(puerto=5000, debug=False):
    """
    Inicia el servidor Flask
    
    Args:
        puerto: Puerto en el que escuchar (default 5000)
        debug: Activar modo debug (default False)
    """
    registrar_log("=" * 60)
    registrar_log(f"[INICIO] Iniciando servidor GPS WiFi en puerto {puerto}")
    registrar_log(f"[INFO] Archivo GPS: {GPS_FILE}")
    registrar_log(f"[INFO] Log: {LOG_FILE}")
    registrar_log(f"[INFO] Endpoint POST: http://localhost:{puerto}/gps")
    registrar_log(f"[INFO] Endpoint GET: http://localhost:{puerto}/update_gps?lat=X&lon=Y")
    registrar_log(f"[INFO] Endpoint TEST: http://localhost:{puerto}/test")
    registrar_log(f"[INFO] Endpoint STATUS: http://localhost:{puerto}/status")
    registrar_log("=" * 60)
    
    app.run(host='0.0.0.0', port=puerto, debug=debug, use_reloader=False)


def iniciar_servidor_thread(puerto=5000):
    """
    Inicia el servidor en un thread independiente
    Util para integracion en la aplicacion principal
    
    Returns:
        thread: El thread en el que corre el servidor
    """
    thread = threading.Thread(
        target=iniciar_servidor,
        args=(puerto, False),
        daemon=True
    )
    thread.start()
    registrar_log(f"[OK] Servidor GPS en thread background (puerto {puerto})")
    return thread


if __name__ == "__main__":
    # Ejecutar directamente
    iniciar_servidor()

