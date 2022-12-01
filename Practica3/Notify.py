import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
COMMASPACE = ', '
# Define params
rrdpath = '/home/gerur/Documentos/ASR/Practicas/Introduccion_SNMP/6-AdministraciónDeRendimiento/RRD/'
imgpath = '/home/gerur/Documentos/ASR/Practicas/Introduccion_SNMP/6-AdministraciónDeRendimiento/IMG'
fname = 'trend.rrd'

mailsender = "dummycuenta3@gmail.com"
mailreceip = "dummycuenta3@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'dvduuffmlhspbmjj'

def send_alert_attached(subject,imagen,host):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """

    msg = MIMEMultipart()
    msg['Subject'] = 'GERSON ' + subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imagen, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(MIMEText(host, 'plain'))
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()