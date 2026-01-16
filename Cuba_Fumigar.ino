//Librerias incluidas
#include "LiquidCrystal.h"
#include <EEPROM.h>

//Definimos los estados de la maquina de estados
#define MenuPrincipal 0
#define ModoConfiguracion 1
#define ModoFuncionamiento 2
#define TiempoDeteccion 3
#define TiempoMedidas 4
#define FuncionamientoAut 5
#define FuncionamientoMan 6
#define UmbralDeteccion 7
#define PruebaSensor 8
#define EstadoConfiguraciones 9
#define ResultadosUso 10
#define VersionMaqueta 11

//Definimos los estados en el modo automatico
#define ArbolDetectado 1
#define ArbolDejadoDetectar 2
#define Desconocido 0

#define FALSE 0
#define TRUE 1

// Comentado para evitar interferencia con comunicación Python
//#define TRAZAS

// Se definen los pines de entradas y salidas que se van a usar
int botonArriba = 0;
int botonAbajo = 1;
int botonOK = 2;
int botonESC = 4;
int botonManual = 5;
int echo=7;
int trigg=8;
int Rele = 9;
int LED = 6;
int RW = 12;
int sincronizacion = 11;
int d4 = 5;
int d5 = 4;
int d6 = 3;
int d7 = 2;

//Se definen variables guardan las lecturas botones
bool LecturaBotonArriba = FALSE;
bool LecturaBotonAbajo = FALSE;
bool LecturaBotonOK = FALSE;
bool LecturaBotonESC = FALSE;
bool LecturaBotonManual = FALSE;

bool auxBotonArriba = FALSE;
bool auxBotonAbajo = FALSE;
bool auxBotonOK = FALSE;
bool auxBotonESC = FALSE;

//Se definen las variables auxiliares
int tiempoRetrasoDeteccion = 50;
int auxtiempoRetrasoDeteccion;
int periodoMedidas = 10;
int auxperiodoMedidas;
int distanciaDeteccion = 200;
int auxdistanciaDeteccion;
unsigned long auxinicioTiempo;
unsigned long auxactualTiempo;
int umbral = 200;
int estado = MenuPrincipal;
//int estado = FuncionamientoAut;
int estadoModoAut = Desconocido;
int cursor = 1;
bool flgSecPausado = 0;
bool ReleEncendido = false;
int contadorArbolDetectado = 0;
int contadorArbolNODetectado = 0;
int maxContador = 15;
int contadorDetectadoPrueba = 0;

// Variable para comandos seriales
String comandoSerial = "";
bool enviarDatosSensor = false;  // Controla cuándo enviar datos del sensor por serial

// Caracteristicas Electrovalvula
float CaudalElecValvula = 2; // En litros/segundos
//2 l/seg para la electrovalvula 40 Bar M-2010 SIRFRAN

//Variables estadisticas
int cntArbolesDia = 0;
float litrosUsoTotal = 0;
unsigned long auxUsoInicio;
unsigned long auxUsoFin;
unsigned long auxUsoTotal;
unsigned long tiempoEncendido = 0;
unsigned long tiempoInicio = 0;

//Se definen las direcciones en EEPROM de las variables
int addr_tiempoRetrasoDeteccion = 0;
int addr_periodoMedidas = sizeof(tiempoRetrasoDeteccion);
int addr_distanciaDeteccion = addr_periodoMedidas + sizeof(periodoMedidas);

//Se define el nombre version
String version = "bA01";

//Se definen columnas y filas de la pantalla LCD
#define COLS 16
#define ROWS 2

//Se inicializa la pantalla lcd
LiquidCrystal lcd(RW, sincronizacion, d4, d5, d6, d7);

void inicioConfiguraciones(void){
  tiempoRetrasoDeteccion = 500;
  periodoMedidas = 10;
  distanciaDeteccion = 40;
}

void setup(){

  pinMode(botonArriba, INPUT);
  pinMode(botonAbajo, INPUT);
  pinMode(botonOK, INPUT);
  pinMode(botonESC, INPUT);
  pinMode(botonManual, INPUT);
  
  pinMode(Rele, OUTPUT);
  pinMode(LED, OUTPUT);

  pinMode(trigg, OUTPUT);
  pinMode(echo, INPUT);

  lcd.begin(COLS, ROWS);
  lcd.clear();

  Serial.begin(9600);
  leerEEPROM();
  // inicioConfiguraciones(); // Comentado para no sobreescribir valores de EEPROM
}

// Cabeceras funciones utilizadas
long ping(int TriggerPin, int EchoPin);
void encenderLED(void);
void apagarLED(void);
void encenderRELE(void);
void apagarRELE(void);
void Toggleflg(void);
float contadorLitrosFumigar(unsigned long tiempoEncendido);
void procesarComandoSerial(String comando);

void loop(){

  // Procesar comandos seriales de Python
  if (Serial.available() > 0) {
    comandoSerial = Serial.readStringUntil('\n');
    comandoSerial.trim(); // Eliminar espacios y saltos de línea
    procesarComandoSerial(comandoSerial);
  }

  // Desactivar lectura de botones físicos temporalmente
  // LecturaBotonAbajo = leerEntradaAnalogica(botonAbajo);
  // LecturaBotonArriba = leerEntradaAnalogica(botonArriba);
  // LecturaBotonOK = leerEntradaAnalogica(botonOK);
  // LecturaBotonESC = leerEntradaAnalogica(botonESC);
  // LecturaBotonManual = leerEntradaAnalogica(botonManual);
  
  // Poner todas las lecturas en TRUE (no presionado)
  LecturaBotonAbajo = TRUE;
  LecturaBotonArriba = TRUE;
  LecturaBotonOK = TRUE;
  LecturaBotonESC = TRUE;
  LecturaBotonManual = TRUE;
  
  delay(10);
  
  switch(estado){

  case MenuPrincipal:
    if (cursor == 1){
      lcd.setCursor(0,0);
      lcd.print("->Configuracion");
      lcd.setCursor(0,1);
      lcd.print("Inicio Sec.");
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 2;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = ModoConfiguracion;
        lcd.clear();
      }
    }else if(cursor==2){
      lcd.setCursor(0,0);
      lcd.print("Configuracion");
      lcd.setCursor(0,1);
      lcd.print("->Inicio Sec.");
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 1;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = ModoFuncionamiento;
        cursor = 1;
        lcd.clear();
      }
    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 3;
        lcd.clear();
      }
    }else if(cursor==3){
      lcd.setCursor(0,0);
      lcd.print("->Prueba Sensor");
      lcd.setCursor(0,1);
      lcd.print("Estado Config");   
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 2;
        lcd.clear();
      }
    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 4;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = PruebaSensor;
        contadorDetectadoPrueba = 0;
        cursor = 1;
        lcd.clear();
      }
  }else if(cursor==4){
      lcd.setCursor(0,0);
      lcd.print("Prueba Sensor");
      lcd.setCursor(0,1);
      lcd.print("->Estado Config");   
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 3;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = EstadoConfiguraciones;
        cursor = 1;
        lcd.clear();
      }
    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 5;
        lcd.clear();
      }
  }else if(cursor==5){
      lcd.setCursor(0,0);
      lcd.print("->Resultados Uso");
      lcd.setCursor(0,1);
      lcd.print("Version SW");    
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
      cursor = 4;
      lcd.clear();
    }
    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
      cursor = 6;
      lcd.clear();
    }
    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      estado = ResultadosUso;
      cursor = 1;
      lcd.clear();
    }
  }else if(cursor==6){
      lcd.setCursor(0,0);
      lcd.print("Resultados Uso"); 
      lcd.setCursor(0,1);
      lcd.print("->Version SW");       
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
      cursor = 5;
      lcd.clear();
    }
    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      estado = VersionMaqueta;
      cursor = 1;
      lcd.clear();
    }
  }
    break;

  case ModoConfiguracion:
    if (cursor == 1){
      lcd.setCursor(0,0);
      lcd.print("->Retraso Detec");
      lcd.setCursor(0,1);
      lcd.print("Tiempo Medidas");
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 2;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = TiempoDeteccion;
        auxtiempoRetrasoDeteccion = tiempoRetrasoDeteccion;
        lcd.clear();
      }
    }else if(cursor==2){
      lcd.setCursor(0,0);
      lcd.print("Retraso Detec");
      lcd.setCursor(0,1);
      lcd.print("->Tiempo Medidas");
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 1;
        lcd.clear();
      }
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 3;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = TiempoMedidas;
        auxperiodoMedidas = periodoMedidas;
        cursor = 1;
        lcd.clear();
      }
    }else if(cursor==3){
      lcd.setCursor(0,0);
      lcd.print("->Distancia Det");
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 2;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = UmbralDeteccion;
        auxdistanciaDeteccion = distanciaDeteccion;
        cursor = 1;
        lcd.clear();
      }
    }
    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      cursor = 1;
      lcd.clear();
    }
    break;

  case ModoFuncionamiento:

    if (cursor == 1){
      lcd.setCursor(0,0);
      lcd.print("->Modo Automat");
      lcd.setCursor(0,1);
      lcd.print("Modo Manual");
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 2;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = FuncionamientoAut;
        lcd.clear();
      }
    }else if(cursor==2){
      lcd.setCursor(0,0);
      lcd.print("Modo Automat");
      lcd.setCursor(0,1);
      lcd.print("->Modo Manual");
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 1;
        lcd.clear();
      }
      if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
        estado = FuncionamientoMan;
        cursor = 1;
        lcd.clear();
      }
    }
    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      lcd.clear();
    }

    break;

  case TiempoDeteccion:
    lcd.setCursor(0,0);
    lcd.print("Retraso Detecc");
    lcd.setCursor(0,1);
    lcd.print(auxtiempoRetrasoDeteccion);
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
      auxtiempoRetrasoDeteccion = auxtiempoRetrasoDeteccion + 100;
      lcd.clear();
    }

    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
      auxtiempoRetrasoDeteccion = auxtiempoRetrasoDeteccion - 100;
      if(auxtiempoRetrasoDeteccion<100){
        auxtiempoRetrasoDeteccion = 100;
      }
      lcd.clear();
    }

    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      lcd.clear();
      tiempoRetrasoDeteccion = auxtiempoRetrasoDeteccion;
      EEPROM.put(addr_tiempoRetrasoDeteccion, tiempoRetrasoDeteccion);
      lcd.setCursor(0,0);
      lcd.print("Configuracion");
      lcd.setCursor(0,1);
      lcd.print("Guardada");
      delay(1000);
      lcd.clear();
    }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = ModoConfiguracion;
      lcd.clear();
    }

    break;

  case TiempoMedidas:
    lcd.setCursor(0,0);
    lcd.print("Tiempo Medidas");
    lcd.setCursor(0,1);
    lcd.print(auxperiodoMedidas);
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
      auxperiodoMedidas = auxperiodoMedidas + 10;
    }

    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
      auxperiodoMedidas = auxperiodoMedidas - 10;

      if(auxperiodoMedidas<10){
        auxperiodoMedidas = 10;
      }
      lcd.clear();
    }

    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      lcd.clear();
      periodoMedidas = auxperiodoMedidas;
      EEPROM.put(addr_periodoMedidas, periodoMedidas);
      lcd.setCursor(0,0);
      lcd.print("Configuracion");
      lcd.setCursor(0,1);
      lcd.print("Guardada");
      delay(1000);
      lcd.clear();
    }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = ModoConfiguracion;
      lcd.clear();
    }

    break;

  case UmbralDeteccion:
    lcd.setCursor(0,0);
    lcd.print("Limite Detecc");
    lcd.setCursor(0,1);
    lcd.print(auxdistanciaDeteccion);
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
      auxdistanciaDeteccion = auxdistanciaDeteccion + 20;
    }

    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
      auxdistanciaDeteccion = auxdistanciaDeteccion - 20;

      if(auxdistanciaDeteccion<20){
        auxdistanciaDeteccion = 20;
      }
      lcd.clear();
    }

    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      lcd.clear();
      distanciaDeteccion = auxdistanciaDeteccion;
      EEPROM.put(addr_distanciaDeteccion, distanciaDeteccion);
      lcd.setCursor(0,0);
      lcd.print("Configuracion");
      lcd.setCursor(0,1);
      lcd.print("Guardada");
      delay(1000);
      lcd.clear();
    }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = ModoConfiguracion;
      lcd.clear();
    }

    break;

  case FuncionamientoAut:
    if ((LecturaBotonOK == FALSE) && (auxBotonOK == TRUE)){
      Toggleflg();
    }
    if(flgSecPausado == FALSE){
      lcd.setCursor(0,0);
      lcd.print("Modo Funcionam");
      lcd.setCursor(0,1);
      lcd.print("Automatico");
    
      long cm;
      cm = ping(trigg, echo);

      switch(estadoModoAut){
        case Desconocido:
          if(cm < distanciaDeteccion){
            contadorArbolDetectado++;
          }

          if(contadorArbolDetectado>=maxContador){
            delay(tiempoRetrasoDeteccion);
            estadoModoAut = ArbolDetectado;
            // Encender el Rele
            encenderRELE();
            encenderLED();
            // Guardar el tiempo de inicio
            tiempoInicio = millis();
            cntArbolesDia++;

            contadorArbolDetectado=0;
            contadorArbolNODetectado=0;         
          }
          break;

        case ArbolDetectado:
          if(cm > distanciaDeteccion){
            contadorArbolNODetectado++;
          }

          if(contadorArbolNODetectado>=maxContador){
            estadoModoAut = ArbolDejadoDetectar;                    
          // Apagar el Rele
          apagarRELE();
          apagarLED();
          // Calcular el tiempo que estuvo encendido
          tiempoEncendido += millis() - tiempoInicio;        
            contadorArbolDetectado=0;
            contadorArbolNODetectado=0;    
          }
          break;

        case ArbolDejadoDetectar:
          estadoModoAut = Desconocido;            
          break;
      }
  }else{
    lcd.setCursor(0,0);
    lcd.print("Modo Funcionam");
    lcd.setCursor(0,1);
    lcd.print("PAUSADO");  
    apagarRELE();
    ReleEncendido = FALSE;
    apagarLED();
  }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = ModoFuncionamiento;
      apagarRELE();
      ReleEncendido = FALSE;
      apagarLED();
      lcd.clear();
    }
    break;

  case FuncionamientoMan:
    lcd.setCursor(0,0);
    lcd.print("Modo Funcionam");
    lcd.setCursor(0,1);
    lcd.print("Manual");
    if (LecturaBotonManual == FALSE){
      if (!ReleEncendido) {
        // Encender el Rele
        encenderRELE();
        encenderLED();
        // Guardar el tiempo de inicio
        tiempoInicio = millis();
        // Cambiar el estado del Rele a encendido
        ReleEncendido = true;
      }      
    }else{
      if (ReleEncendido) {
        // Encender el Rele
        apagarRELE();
        apagarLED();
        // Calcular el tiempo que estuvo encendido en esta pulsación
        tiempoEncendido += millis() - tiempoInicio;
        // Cambiar el estado del LED a apagado
        ReleEncendido = false;
      }
    }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = ModoFuncionamiento;
      apagarRELE();
      ReleEncendido = FALSE;
      apagarLED();
      lcd.clear();
    }
    break;
  
  case PruebaSensor:
    lcd.setCursor(0,0);
    lcd.print("Distancia: (cm)");

    long distancia;
  
    distancia=ping(trigg,echo);
    
    // Enviar valor del sensor vía serial solo si estamos en modo prueba
    Serial.println(distancia);

    lcd.setCursor(0,1);
    lcd.print("                ");

    lcd.setCursor(0,1);
    lcd.print(distancia);

    if(distancia < distanciaDeteccion){
      if(contadorDetectadoPrueba>maxContador){
        encenderLED();
      }else{
        contadorDetectadoPrueba++;
      }
    }else{
      contadorDetectadoPrueba = 0;
      apagarLED();
    }

    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      cursor = 1;
      lcd.clear();
    }
    delay(tiempoRetrasoDeteccion);
  
    break;
  
  case EstadoConfiguraciones:
    if (cursor == 1){
      lcd.setCursor(0,0);
      lcd.print("Retraso Detecc");
      lcd.setCursor(0,1);
      lcd.print(tiempoRetrasoDeteccion);
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 2;
        lcd.clear();
      }
    }else if(cursor==2){
      lcd.setCursor(0,0);
      lcd.print("Tiempo Medidas");
      lcd.setCursor(0,1);
      lcd.print(periodoMedidas);
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 1;
        lcd.clear();
      }
    if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 3;
        lcd.clear();
      }
    }else if(cursor==3){
    lcd.setCursor(0,0);
      lcd.print("Limite Detecc");
      lcd.setCursor(0,1);
      lcd.print(distanciaDeteccion);    
    if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 2;
        lcd.clear();
      }
  }
    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      cursor = 1;
      lcd.clear();
    } 
    break;  
  
  case ResultadosUso:
    if (cursor == 1){
    lcd.setCursor(0,0);
      lcd.print("Arboles Fumig");
      lcd.setCursor(0,1);
      lcd.print(cntArbolesDia);
      if ((LecturaBotonAbajo == FALSE) && (auxBotonAbajo == TRUE)){
        cursor = 2;
        lcd.clear();
      }
    }else if(cursor==2){
      litrosUsoTotal = contadorLitrosFumigar(tiempoEncendido);
      lcd.setCursor(0,0);
      lcd.print("Litros Fumig");
      lcd.setCursor(0,1);
      lcd.print(litrosUsoTotal);
      if ((LecturaBotonArriba == FALSE) && (auxBotonArriba == TRUE)){
        cursor = 1;
        lcd.clear();
      }
    } 
    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      cursor = 1;
      lcd.clear();
    }
    break;

  case VersionMaqueta:
    lcd.setCursor(0,0);
    lcd.print("Version SW");
    lcd.setCursor(0,1);
    lcd.print(version);
    if ((LecturaBotonESC == FALSE) && (auxBotonESC == TRUE)){
      estado = MenuPrincipal;
      cursor = 1;
      lcd.clear();
    }
    break;
  }

  //Se actualizan las variables auxiliares
  auxBotonArriba = LecturaBotonArriba;
  auxBotonAbajo = LecturaBotonAbajo;
  auxBotonOK = LecturaBotonOK;
  auxBotonESC = LecturaBotonESC;
}

long ping(int TriggerPin, int EchoPin) {
  long duration, distanceCm;

  digitalWrite(TriggerPin, LOW);  //para generar un pulso limpio ponemos a LOW 4us
  delayMicroseconds(4);
  digitalWrite(TriggerPin, HIGH);  //generamos Trigger (disparo) de 10us
  delayMicroseconds(10);
  digitalWrite(TriggerPin, LOW);
  
  duration = pulseIn(EchoPin, HIGH, 30000);  //timeout de 30ms para evitar bloqueos
  
  distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm

  delay(periodoMedidas);
  return distanceCm;
}

bool leerEntradaAnalogica (int pin){
  int valor;
  valor = analogRead(pin);   // realizar la lectura 
  if (valor > 900){
    return TRUE;
  }else{
    return FALSE;
  }
}

void encenderLED(void){
  digitalWrite(LED, HIGH);
}

void apagarLED(void){
  digitalWrite(LED, LOW);
}

void encenderRELE(void){
  digitalWrite(Rele, HIGH);
}

void apagarRELE(void){
  digitalWrite(Rele, LOW);
}

float contadorLitrosFumigar(unsigned long tiempoEncendido){
  float litrosFumigados;
  /*Serial.print(" Tiempo encendido es:");
  Serial.println(tiempoEncendido);
  Serial.print(" Caudal es:");
  Serial.println(CaudalElecValvula);*/
  litrosFumigados = (CaudalElecValvula * tiempoEncendido)/1000;
  /*Serial.print(" Resultado es:");
  Serial.println(litrosFumigados);*/ 
  return litrosFumigados;
}

void leerEEPROM(void){
  //Direcciones de EEPROM:
  //tiempoRetrasoDeteccion -> 0
  //periodoMedidas -> 2
  //distanciaDeteccion -> 4
  EEPROM.get(addr_tiempoRetrasoDeteccion, tiempoRetrasoDeteccion);
  EEPROM.get(addr_periodoMedidas, periodoMedidas);
  EEPROM.get(addr_distanciaDeteccion, distanciaDeteccion);
}

void Toggleflg(void){
  lcd.clear();
  if(flgSecPausado == TRUE){
    flgSecPausado = FALSE;
  }else{
    flgSecPausado = TRUE;
  }
}

void procesarComandoSerial(String comando) {
  // Procesar comandos desde la interfaz Python
  if (comando == "MENU INICIO") {
    estado = MenuPrincipal;
    cursor = 1;
    lcd.clear();
    Serial.println("ESTADO:INICIO");
  }
  else if (comando == "MENU CONFIGURACIONES") {
    enviarDatosSensor = false;  // Desactivar envío de datos
    estado = ModoConfiguracion;
    lcd.clear();
    // Enviar confirmación y valores actuales
    Serial.println("ESTADO:CONFIGURACION");
    Serial.print("RETRASO:");
    Serial.println(tiempoRetrasoDeteccion);
    Serial.print("TIEMPO:");
    Serial.println(periodoMedidas);
    Serial.print("DISTANCIA:");
    Serial.println(distanciaDeteccion);
  }
  else if (comando == "MENU SECUENCIA") {
    enviarDatosSensor = false;  // Desactivar envío de datos
    estado = ModoFuncionamiento;
    lcd.clear();
    Serial.println("ESTADO:FUNCIONAMIENTO");
  }
  else if (comando == "MENU PRUEBA SENSOR") {
    estado = PruebaSensor;
    lcd.clear();
    Serial.println("ESTADO:PRUEBA_SENSOR");
    enviarDatosSensor = true;  // Activar envío de datos del sensor
  }
  // Comandos para recibir valores de configuración desde Python
  else if (comando.startsWith("CONFIG_RETRASO:")) {
    int valor = comando.substring(15).toInt();
    tiempoRetrasoDeteccion = valor;
    EEPROM.put(addr_tiempoRetrasoDeteccion, tiempoRetrasoDeteccion);
    Serial.print("RETRASO:");
    Serial.println(tiempoRetrasoDeteccion);
  }
  else if (comando.startsWith("CONFIG_TIEMPO:")) {
    int valor = comando.substring(14).toInt();
    periodoMedidas = valor;
    EEPROM.put(addr_periodoMedidas, periodoMedidas);
    Serial.print("TIEMPO:");
    Serial.println(periodoMedidas);
  }
  else if (comando.startsWith("CONFIG_DISTANCIA:")) {
    int valor = comando.substring(17).toInt();
    distanciaDeteccion = valor;
    EEPROM.put(addr_distanciaDeteccion, distanciaDeteccion);
    Serial.print("DISTANCIA:");
    Serial.println(distanciaDeteccion);
  }
}
