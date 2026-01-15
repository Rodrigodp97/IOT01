# Comunicación simple con Arduino
$port = new-Object System.IO.Ports.SerialPort COM15,9600,None,8,one
$port.Open()
Start-Sleep -Seconds 2

Write-Host "Puerto COM15 abierto" -ForegroundColor Green
Write-Host "Enviando: MENU CONFIGURACIONES" -ForegroundColor Yellow
$port.WriteLine("MENU CONFIGURACIONES")
Start-Sleep -Seconds 1

# Leer respuestas
for($i=0; $i -lt 30; $i++) {
    if($port.BytesToRead -gt 0) {
        $line = $port.ReadLine()
        Write-Host "Arduino: $line" -ForegroundColor Cyan
    }
    Start-Sleep -Milliseconds 100
}

$port.Close()
Write-Host "`nPuerto cerrado" -ForegroundColor Green
