"""
Servidor Flask para recibir ubicación GPS desde Android via WiFi
Escucha en puerto 5000 en localhost
Endpoint: POST /gps con JSON {"lat": latitud, "lon": longitud}
"""

from flask import Flask, request, jsonify
from pathlib import Path
import json
import threading
import time
from datetime import datetime

# Crear aplicación Flask
app = Flask(__name__)

# Archivo donde guardar la última ubicación GPS
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
        print(linea, flush=True)  # También imprimir en consola con flush
    except Exception as e:
        print(f"Error escribiendo log: {e}", flush=True)


@app.route('/gps', methods=['POST'])
def recibir_gps():
    """
    Endpoint para recibir ubicación GPS desde Android
    
    Request body esperado:
    {
        "lat": latitud (float),
        "lon": longitud (float)
    }
    
    Returns:
        JSON con estado de la operación
    """
    try:
        # LOGGING DE DEBUG: Mostrar todo lo que llega
        registrar_log(f"📥 POST /gps - Nueva petición recibida")
        registrar_log(f"   Content-Type: {request.content_type}")
        registrar_log(f"   Body RAW: {request.data.decode('utf-8', errors='replace')[:500]}")
        
        # Obtener datos del request
        data = request.get_json(force=True, silent=True)
        
        if data is None:
            registrar_log(f"⚠️  POST /gps - No es JSON, intentando parsear como texto plano...")
            # Intentar obtener como texto con formato "lat,lon"
            texto = request.data.decode('utf-8', errors='replace').strip()
            registrar_log(f"   Texto recibido: {texto}")
            
            # Parsear formato "latitud,longitud" (como envía Tasker)
            try:
                partes = texto.split(',')
                if len(partes) == 2:
                    lat = float(partes[0].strip())
                    lon = float(partes[1].strip())
                    registrar_log(f"   ✅ Parseado correctamente: lat={lat}, lon={lon}")
                    # Continuar con validación normal
                    data = {'lat': lat, 'lon': lon}
                else:
                    registrar_log(f"   ❌ Formato inválido: esperaba 'lat,lon', recibió {len(partes)} partes")
                    return jsonify({
                        'error': 'Invalid format. Expected "lat,lon" or JSON {"lat":X,"lon":Y}',
                        'received': texto[:200],
                        'status': 'error'
                    }), 400
            except (ValueError, IndexError) as e:
                registrar_log(f"   ❌ Error parseando coordenadas: {e}")
                return jsonify({
                    'error': 'Invalid coordinate format',
                    'received': texto[:200],
                    'status': 'error'
                }), 400
        
        # Validar que existan lat y lon
        lat = data.get('lat')
        lon = data.get('lon')
        
        if lat is None or lon is None:
            registrar_log(f"❌ POST /gps - Faltan campos lat/lon. Recibido: {data}")
            return jsonify({
                'error': 'Missing "lat" or "lon" fields',
                'status': 'error'
            }), 400
        
        # Validar que sean números válidos
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            registrar_log(f"❌ POST /gps - Valores lat/lon no son números: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'lat and lon must be valid numbers',
                'status': 'error'
            }), 400
        
        # Validar rango de coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            registrar_log(f"❌ POST /gps - Rango inválido: lat={lat}, lon={lon}")
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
        
        registrar_log(f"✅ GPS RECIBIDO: lat={lat:.6f}, lon={lon:.6f}")
        
        return jsonify({
            'status': 'success',
            'lat': lat,
            'lon': lon,
            'message': 'GPS updated successfully'
        }), 200
    
    except Exception as e:
        registrar_log(f"❌ Error en /gps: {str(e)}")
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
        # LOGGING DE DEBUG: Mostrar petición GET
        registrar_log(f"📥 GET /update_gps - Nueva petición recibida")
        registrar_log(f"   URL completa: {request.url}")
        registrar_log(f"   Parámetros: {dict(request.args)}")
        
        # Obtener parámetros de la URL
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if lat is None or lon is None:
            registrar_log(f"❌ GET /update_gps - Faltan parámetros lat/lon")
            return jsonify({
                'error': 'Missing "lat" or "lon" parameters',
                'status': 'error',
                'usage': '/update_gps?lat=38.635896&lon=-2.915610'
            }), 400
        
        # Validar que sean números válidos
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            registrar_log(f"❌ GET /update_gps - Valores no numéricos: lat={lat}, lon={lon}")
            return jsonify({
                'error': 'lat and lon must be valid numbers',
                'status': 'error'
            }), 400
        
        # Validar rango de coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            registrar_log(f"❌ GET /update_gps - Rango inválido: lat={lat}, lon={lon}")
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
        
        registrar_log(f"✅ GPS RECIBIDO (GET): lat={lat:.6f}, lon={lon:.6f}")
        
        return jsonify({
            'status': 'success',
            'lat': lat,
            'lon': lon,
            'message': 'GPS updated successfully'
        }), 200
    
    except Exception as e:
        registrar_log(f"❌ Error en /update_gps: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/test', methods=['POST', 'GET'])
def test():
    """
    Endpoint de prueba simple
    Úsalo para verificar conectividad básica
    """
    registrar_log(f"✅ TEST - Solicitud recibida ({request.method})")
    return jsonify({
        'status': 'ok',
        'message': 'Servidor está respondiendo correctamente'
    }), 200


@app.route('/status', methods=['GET'])
def status():
    """
    Endpoint para verificar si el servidor está activo
    y obtener la última ubicación GPS conocida
    """
    try:
        if GPS_FILE.exists():
            with open(GPS_FILE, 'r') as f:
                gps_data = json.load(f)
        else:
            gps_data = {"lat": 0.0, "lon": 0.0}
        
        registrar_log(f"📊 STATUS - GPS actual: {gps_data}")
        
        return jsonify({
            'status': 'online',
            'server': 'WiFi GPS Server',
            'gps_data': gps_data
        }), 200
    
    except Exception as e:
        registrar_log(f"❌ Error en /status: {str(e)}")
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
    registrar_log(f"🚀 Iniciando servidor GPS WiFi en puerto {puerto}")
    registrar_log(f"📍 Archivo GPS: {GPS_FILE}")
    registrar_log(f"📝 Log: {LOG_FILE}")
    registrar_log(f"📝 Endpoint POST: http://localhost:{puerto}/gps")
    registrar_log(f"📝 Endpoint GET: http://localhost:{puerto}/update_gps?lat=X&lon=Y")
    registrar_log(f"📝 Endpoint TEST: http://localhost:{puerto}/test")
    registrar_log(f"📊 Endpoint STATUS: http://localhost:{puerto}/status")
    registrar_log("=" * 60)
    
    app.run(host='0.0.0.0', port=puerto, debug=debug, use_reloader=False)


def iniciar_servidor_thread(puerto=5000):
    """
    Inicia el servidor en un thread independiente
    Útil para integración en la aplicación principal
    
    Returns:
        thread: El thread en el que corre el servidor
    """
    thread = threading.Thread(
        target=iniciar_servidor,
        args=(puerto, False),
        daemon=True
    )
    thread.start()
    registrar_log(f"✅ Servidor GPS en thread background (puerto {puerto})")
    return thread


if __name__ == "__main__":
    # Ejecutar directamente
    iniciar_servidor()

