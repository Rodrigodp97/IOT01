# Script para probar comunicación serial con Arduino
# Puerto COM15 a 9600 baudios

$port = new-Object System.IO.Ports.SerialPort COM15,9600,None,8,one
$port.Open()
Start-Sleep -Milliseconds 2000  # Esperar a que Arduino se reinicie

Write-Host "`n=== PRUEBA DE COMUNICACION SERIAL ===" -ForegroundColor Green
Write-Host "Puerto: COM15 @ 9600 baud`n" -ForegroundColor Cyan

# Función para enviar comando y esperar respuesta
function Send-Command {
    param($cmd)
    Write-Host "`n>>> Enviando: $cmd" -ForegroundColor Yellow
    $port.WriteLine($cmd)
    Start-Sleep -Milliseconds 500
    
    # Leer respuestas
    $timeout = 0
    while($timeout -lt 20) {
        if($port.BytesToRead -gt 0) {
            try {
                $response = $port.ReadLine()
                Write-Host "<<< Arduino: $response" -ForegroundColor Green
            } catch {}
        }
        Start-Sleep -Milliseconds 100
        $timeout++
    }
}

# Prueba 1: Entrar en configuraciones
Write-Host "`n--- PRUEBA 1: Menu Configuraciones ---" -ForegroundColor Magenta
Send-Command "MENU CONFIGURACIONES"

# Prueba 2: Cambiar valores
Write-Host "`n--- PRUEBA 2: Cambiar Retraso a 180 ---" -ForegroundColor Magenta
Send-Command "CONFIG_RETRASO:180"

Write-Host "`n--- PRUEBA 3: Cambiar Tiempo a 80 ---" -ForegroundColor Magenta
Send-Command "CONFIG_TIEMPO:80"

Write-Host "`n--- PRUEBA 4: Cambiar Distancia a 90 ---" -ForegroundColor Magenta
Send-Command "CONFIG_DISTANCIA:90"

# Prueba 5: Volver a inicio
Write-Host "`n--- PRUEBA 5: Volver a Menu Inicio ---" -ForegroundColor Magenta
Send-Command "MENU INICIO"

# Prueba 6: Entrar en prueba sensor
Write-Host "`n--- PRUEBA 6: Menu Prueba Sensor ---" -ForegroundColor Magenta
Send-Command "MENU PRUEBA SENSOR"

Write-Host "`n--- Leyendo valores del sensor (5 segundos) ---" -ForegroundColor Magenta
$timeout = 0
while($timeout -lt 50) {
    if($port.BytesToRead -gt 0) {
        try {
            $response = $port.ReadLine()
            if($response -match '^\d+$') {
                Write-Host "Distancia: $response cm" -ForegroundColor Cyan
            } else {
                Write-Host "<<< $response" -ForegroundColor Green
            }
        } catch {}
    }
    Start-Sleep -Milliseconds 100
    $timeout++
}

# Prueba 6: Menu Secuencia
Write-Host "`n--- PRUEBA 7: Menu Secuencia ---" -ForegroundColor Magenta
Send-Command "MENU SECUENCIA"

Write-Host "`n=== PRUEBAS COMPLETADAS ===" -ForegroundColor Green
$port.Close()
Write-Host "Puerto cerrado.`n" -ForegroundColor Yellow
