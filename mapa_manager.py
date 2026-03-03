"""
Módulo para gestionar ventanas de mapas interactivos
Usa subprocess para abrir mapas en procesos separados
"""
import subprocess
import sys
import os


def abrir_mapa(nombre_mapa):
    """
    Abre un mapa en un proceso separado usando subprocess
    
    Args:
        nombre_mapa: Nombre del mapa (huertas_leon_1, manzanos, etc.)
    
    Returns:
        True si se pudo iniciar el proceso, False en caso contrario
    """
    print(f">>> abrir_mapa() llamado con: '{nombre_mapa}'")
    print(f">>> Tipo: {type(nombre_mapa)}")
    
    try:
        # Obtener la ruta del script standalone
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "abrir_mapa_standalone.py")
        
        print(f">>> script_dir: {script_dir}")
        print(f">>> script_path: {script_path}")
        print(f">>> Existe? {os.path.exists(script_path)}")
        
        # Verificar que el script existe
        if not os.path.exists(script_path):
            print(f"✗ Error: No se encuentra {script_path}")
            return False
        
        # Usar python.exe actual
        python_exe = sys.executable
        
        print(f"Ejecutando mapa: {nombre_mapa}")
        print(f"  Python: {python_exe}")
        print(f"  Script: {script_path}")
        
        # Crear proceso y ESPERAR a que termine (bloqueante)
        proceso = subprocess.Popen(
            [python_exe, script_path, nombre_mapa],
            cwd=script_dir
        )
        
        print(f"✓ Mapa '{nombre_mapa}' iniciado (PID: {proceso.pid})")
        
        # ESPERAR a que el usuario cierre el mapa
        proceso.wait()
        print(f"✓ Mapa '{nombre_mapa}' cerrado")
        
        return True
        return True
        
    except Exception as e:
        print(f"✗ Error al abrir mapa: {e}")
        import traceback
        traceback.print_exc()
        return False
