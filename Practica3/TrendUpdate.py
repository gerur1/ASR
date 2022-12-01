import time
import rrdtool
from getSNMP import consultaSNMP
#rrdpath = '../RRD/'
PromCPU = 0

while 1:
    carga_CPU1 = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
    carga_CPU2 = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.25.3.3.1.2.196609'))
    carga_CPU3 = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.25.3.3.1.2.196610'))
    carga_CPU4 = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.25.3.3.1.2.196611'))
    ram_l = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.4.1.2021.4.6.0'))  # Espacio libre
    redIn = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.10.3'))
    redOut = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.16.3'))
    ramDIsp = float(ram_l*100/7050120)
    PromCPU = float((carga_CPU1+carga_CPU2+carga_CPU3+carga_CPU4)/4)
    porcentajeRed = float(((redIn+redOut)/8)*100/100000000)
    valor = "N:" + str(PromCPU) + ':' + str(ramDIsp) + ':' + str(porcentajeRed)
    print(valor)
    rrdtool.update('trend.rrd', valor)
    rrdtool.dump('trend.rrd', 'trend.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)
