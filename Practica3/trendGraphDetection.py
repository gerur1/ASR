import sys
import pywhatkit
import rrdtool
import time
from Notify import send_alert_attached
import time
from getSNMPb import consultaSNMP

hostname = str(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.1.1.0')[2:]).replace(',',' ')

correo = str(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.1.4.0')[2])

ubicacion = str(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.1.6.0')[2:]).replace(',',' ')





def generarGraficaCPU(ultima_lectura):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 3500
    ret = rrdtool.graphv("deteccionCPU.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final+1),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del CPU del agente Usando SNMP y RRDtools \n Gerson Uriel Olivares López",
                    "DEF:cargaCPU=trend.rrd:CPUload:AVERAGE",
                    "LINE2:cargaCPU#FF0000:Carga de CPU",
                    "HRULE:89#04ff00:Umbral 89%",
                    "HRULE:60#FF8C00:Umbral 60%")
    print ('CPU')

def generarGraficaRam(ultima_lectura):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 3500
    ret = rrdtool.graphv("deteccionRAM.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final+1),
                     "--vertical-label=Ram disponible",
                    '--lower-limit', '0',
                    '--upper-limit', '30',
                    "--title=Espacio disponible en la RAM \nGerson Uriel Olivares López",
                    "DEF:cargaRAM=trend.rrd:RAM:AVERAGE",
                    "LINE2:cargaRAM#334cff:Carga de RAM",
                    "HRULE:20#00CED1:Umbral 20%",
                    "HRULE:10#FF8C00:Umbral 10%")
    print ('RAM')



def generarGraficaRed(ultima_lectura):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 3500
    ret = rrdtool.graphv("deteccionRed.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final+1),
                     "--vertical-label=Porcentaje de red ocupada",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Porcentaje de uso de la red \nGerson Uriel Olivares López ",
                    "DEF:cargaRed=trend.rrd:Red:MAX",
                    "LINE2:cargaRed#33fcff:Carga de Red",
                    "HRULE:20#04ff00:Umbral 20%",
                    "HRULE:45#FF8C00:Umbral 45%")
    print('Red')



while (1):

    ultima_actualizacion = rrdtool.lastupdate("trend.rrd")
    CPU=ultima_actualizacion['ds']['CPUload']
    RAM=ultima_actualizacion['ds']['RAM']
    RED=ultima_actualizacion['ds']['Red']
    tiempo=ultima_actualizacion['date'].timestamp()
    #print(promedio)
    '''if CPU > 60.0 and CPU < 89.0:
        generarGraficaCPU(tiempo)
        send_alert_attached("CPU está en el umbral precaución","deteccionCPU.png","Porcentaje: "+str(CPU)+"\nInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    if CPU > 89:
        generarGraficaCPU(tiempo)
        send_alert_attached("CPU Está en el umbral crítico","deteccionCPU.png","Porcentaje: "+str(CPU)+"\nInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    
    if RAM < 50 and RAM > 10 :
        generarGraficaRam(tiempo)
        send_alert_attached("RAM Está en el umbral crítico","deteccionRAM.png","Porcentaje libre: "+str(RAM)+"\nInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    if RAM < 10:
        generarGraficaRam(tiempo)
        send_alert_attached("RAM Está en el umbral precaución","deteccionRAM.png","Porcentaje libre: "+str(RAM)+"\nInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    
'''
    if RED > 20 and RED < 45:
        generarGraficaRed(tiempo)
        send_alert_attached("Red Rebasó umbral Correcto","deteccionRed.png","Porcentaje usado: "+str(RED)+"\nInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    if RED > 45:
        generarGraficaRed(tiempo)
        send_alert_attached("Red está en umbral Precaución","deteccionRed.png","Porcentaje usado: "+str(RED)+"\nxInfo del sistema: "+hostname+'\n' + "Contacto:" + correo + '\n' + "Ubicación: " + ubicacion)
    time.sleep(10)