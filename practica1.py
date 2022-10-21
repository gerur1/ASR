import time
from getSNMP_P1 import consultaSNMP
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

print("Sistema de administración de red\n Práctica 1 -Adquisición de Información"
      "\nOlivares López Gerson Uriel \tBoleta: 2017631151\t Grupo: 4CM16")
f = open('bd.txt', 'w')
f.close()


def elegirOpcion():
    correcto = False  # Validar opción correcta
    num = 0
    while (not correcto):
        try:
            num = int(input("Elige una opción: "))
            correcto = True
        except ValueError:
            print('Error, introduce una opción válida')

    return num


def agregarAgente():
    comunidad = str(input("Escribe el nombre de la comunidad: "))
    version = str(input("Escribe la versión de SNMP(v1/v2): "))
    puerto = int(input("Ingresa el puerto del agente: "))
    host = str(input("Ingresa IP o hostname del agente: "))
    SysOp = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.1.0', puerto))  # Extrae sistema operativo
    nomDisp = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.5.0', puerto)).split()  # nombre del dispositivo
    contacto = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.4.0', puerto)).split()  # contacto
    numInterfaz = int(consultaSNMP(comunidad, host, '1.3.6.1.2.1.2.1.0', puerto).split()[2])

    #############Nombre del equipo######
    print(nomDisp[2])
    ##########Systema Operativo###########
    if "Linux" in SysOp:
        Sistema = 'Linux'
    if "Windows" in SysOp:
        Sistema = 'Windows'

    ###########Estado de las interfaces#####
    OIDifIndex = '1.3.6.1.2.1.2.2.1.1.'
    OIDifDescr = '1.3.6.1.2.1.2.2.1.2.'
    OIDifAdminStatus = '1.3.6.1.2.1.2.2.1.7.'

    f = open('bd.txt', 'a')
    f.write('*')
    f.write(nomDisp[2] + '\n')
    f.write(comunidad + '\n')
    f.write(str(puerto) + '\n')
    f.write(version + '\n')
    f.write(host+ '\n')
    #f.write('\n')
    '''
    f.write(Sistema + '\n')
    f.write(str(numInterfaz) + '\n')  ###########NumInterfacez###############
    f.write(contacto[2] + '\n')  ###########Info de contacto########
    for i in range(numInterfaz + 1):
        if i > 0:
            index = OIDifIndex + str(i)
            Descrip = OIDifDescr + str(i)
            indice = consultaSNMP(comunidad, host, index, puerto).split()[2]
            Descripcion = consultaSNMP(comunidad, host, Descrip, puerto)[29:]
            Status = OIDifAdminStatus + str(i)
            Estatus = consultaSNMP(comunidad, host, Status, puerto).split()[2]
            f.write(indice + ',' + Descripcion + ',' + Estatus)
            f.write('\n')'''
    f.close()





def reporte(indexagente):
    print(indexagente)
    f = open('bd.txt', 'r')

    escribir = f.readlines()
    contador = 0
    contador_l=0

    for linea in escribir:
        contador_l+=1
        if '*' in linea:
            #1print(str(contador) + '.- ' + linea.strip('*'))
            contador += 1
            if (contador) == int(indexagente):
                print(contador)
                print('Lo encontré:')
                comunidad = str(escribir[contador_l].strip())
                puerto = int(escribir[contador_l + 1].strip())
                version = str(escribir[contador_l + 2].strip())
                host = str(escribir[contador_l + 3].strip())
                print(host)
                f.close()
                break
    w, h = A4
    c = canvas.Canvas("reporte.pdf", pagesize=A4)
    text = c.beginText(50, h - 50)
    text.setFont("Times-Roman", 12)
    text.textLine("Administración de servicios en red")
    text.textLine("Practica 1")
    text.textLine("Alumno:Olivares López Gerson Uriel Grupo:4CM16")
    SysOp = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.1.0',puerto))  # Extrae sistema operativo
    text.textLine(escribir[contador_l-1])
    contacto = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.4.0', puerto).split()[2])  # contacto

    numInterfaz = int(consultaSNMP(comunidad, host, '1.3.6.1.2.1.2.1.0', puerto).split()[2])
    if "Linux" in SysOp:
        Sistema = 'Linux'
    if "Windows" in SysOp:
        Sistema = 'Windows'
    text.textLine(Sistema)
    text.textLine(comunidad)
    text.textLine(host)
    text.textLine(contacto)
    ########### OID's  #####
    OIDifIndex = '1.3.6.1.2.1.2.2.1.1.'
    OIDifDescr = '1.3.6.1.2.1.2.2.1.2.'
    OIDifAdminStatus = '1.3.6.1.2.1.2.2.1.7.'
    text.textLine('Numero de interfaces: '+str(numInterfaz))
    for i in range(numInterfaz + 1):
        if i > 0:
            index = OIDifIndex + str(i)
            Descrip = OIDifDescr + str(i)
            indice = consultaSNMP(comunidad, host, index, puerto).split()[2]
            Descripcion = consultaSNMP(comunidad, host, Descrip, puerto)[29:]
            Status = OIDifAdminStatus + str(i)
            Estatus = consultaSNMP(comunidad, host, Status, puerto).split()[2]
            text.textLine(indice + ',' + Descripcion + ',' + Estatus)
    c.drawText(text)
    c.save()


def seleccionar():
    f = open('bd.txt', 'r')
    agentes = f.readlines()
    contador = 1
    for linea in agentes:
        if '*' in linea:
            print(str(contador)+'.- '+linea.strip('*'))
            contador += 1
    f.close()
    agenteSelect = input("Selecciona un agente: ")
    return agenteSelect


opcion = 0
while True:

    print("1. Agregar dispositivo")
    print("2. Cambiar información de dispositivo")
    print("3. Eliminar dispositivo")
    print("4. Generar Reporte")

    opcion = elegirOpcion()

    if opcion == 1:
        agregarAgente()
    elif opcion == 2:
        modificar()
    elif opcion == 3:
        print("Opcion 3")
    elif opcion == 4:
        reporte(seleccionar())

    else:
        print("Introduce un número entre 1 y 4")

print("Fin")
