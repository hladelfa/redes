from scapy.all import *
from thompsonValues import thompsonValues

def calculaMedia(valores):

    sum=0.0
    for valor in valores:
        sum += valor
        
    return sum / float(len(valores))

def calcularStandardDeviation(valores):

    media = calculaMedia(valores)
    diferencia = 0.0
    
    for valor in valores:
        diferencia += pow(valor - media, 2)

    diferencia = diferencia / float(len(valores)-1)
    return math.sqrt(diferencia)

def calcularOutliers(muestra_rtt, outliers):
    media = calculaMedia(muestra_rtt)
    print ("-------Media-----------")
    print (media)
    print ("-------Desvio Estandar-----------")
    dstandar = calcularStandardDeviation(muestra_rtt)
    print (dstandar)
    print ("-------absolute value of the deviation-----------")
    adeviation = abs(max(muestra_rtt) - media)
    print (adeviation)
    print ("-------modifiedThompson-----------")
    thompsonValue = thompsonValues[len(muestra_rtt)]
    modifiedThompson = thompsonValue * dstandar
    print (modifiedThompson)

    if adeviation > modifiedThompson:
        msg = "DRTT: "+str(max(muestra_rtt))+" es el enlace transatlantico"
        print msg 
        outliers.append(str(max(muestra_rtt)))
        muestra_rtt.pop()
        print (muestra_rtt)
        calcularOutliers(muestra_rtt, outliers)
    

def negativeFilter(muestra_rtt):
 muestra_rtt_copy = []
 index = 0
 for drtt in muestra_rtt:
   if(drtt >= 0.0):
     muestra_rtt_copy.append(drtt)
 media = calculaMedia(muestra_rtt_copy)
 while(len(muestra_rtt_copy) < len(muestra_rtt)): 
   muestra_rtt_copy.append(media);

 return muestra_rtt_copy

QUANTITY_ATTEMPTS = 30
LIMITE_TTL = 40

ip = sys.argv[1]
file_prefix = sys.argv[2]

text_file = open(file_prefix+"_output.txt", "w")
text_file.write("Saltos  Ip             rtt              DRTT     Intentos\n")

resp = ""
timeout=1
ttl = 1
muestra_rtt = []
ultimo_rtt_prom = 0.0
rtt_prom_list = []

while(resp != 0 and LIMITE_TTL > ttl): #"Echo Reply"
    #Paquete: ICMP Echo Request, destino IP y TTL.    
    packet = IP(dst=ip, ttl=ttl) / ICMP()
    res_ip = None
    res_ip_list = []
    cant_timeouts = 0
    intentos = 1
    rtt_sum = 0.0
    cant_exitos = 0
    while intentos <= QUANTITY_ATTEMPTS:    
	print ("TTL: ", ttl)
	print ("Intentos: ", intentos)
        rtt = int(round(time.time() * 1000))
        res = sr1(packet, timeout=timeout)
        rtt = int(round(time.time() * 1000)) - rtt
        
        if res != None:

            if res.type == 0: #ECHO_REPLY
                 resp = 0
            
            if res_ip == None:
               res_ip = res[IP].src
               res_ip_list.append(res_ip)   
            elif res_ip != res[IP].src: # Cambio la IP
                 res_ip = res[IP].src
                 res_ip_list.append(res_ip)
            #    if intentos <= 3: # no tenemos suficientes RTTs para promediar
            #       res_ip = res[IP].src
            #       intentos = 2
            #       rtt_sum = rtt
            #       cant_exitos = 1
            #       rtts = [rtt]
            #       continue
            #    else: # Seguimos al proximo ttl
            #       break  
            rtt_sum += rtt
            cant_exitos += 1  
        
        #else:
        #    cant_timeouts += 1

        #    if cant_timeouts >= 3:
        #        timeout += 1
        #        break

        intentos += 1
    
    #print(res)
    print ("----------------------")
    #print (res[0][ICMP].display())
    print ("TTL: ", ttl)
    print ("**********************")   

    text_file.write(str(ttl))
    text_file.write("       ") 

    if(rtt_sum > 0):

        rtt_prom = rtt_sum / cant_exitos

        #deltaRTTi = abs(rtt_prom - ultimo_rtt_prom)
	deltaRTTi = rtt_prom - ultimo_rtt_prom
	#if( deltaRTTi < 0.0):
	#    deltaRTTi = 0.0;


        ultimo_rtt_prom = rtt_prom

        muestra_rtt.append(deltaRTTi)

        
        #text_file.write(res_ip)
        text_file.write(str(res_ip_list))        
        text_file.write("   ")
        text_file.write(str(rtt_prom))
        text_file.write("         ")
        text_file.write(str(deltaRTTi))
        text_file.write("   ")
	text_file.write(str(cant_exitos))
        text_file.write("\n")
    else:
        #En otro caso, marcar como desconocido (*) 
        text_file.write("*****\n")
        
    ttl += 1

text_file.close()

print ("-------DRTTS-----------")
muestra_rtt.pop(0)
muestra_rtt = negativeFilter(muestra_rtt)
muestra_rtt.sort()
print (muestra_rtt)

outliers = []
calcularOutliers(muestra_rtt, outliers)

outliers_file = open(file_prefix+"_outliers.txt", "w")
#outliers_file.write("Media: ")
#outliers_file.write(str(media))
#outliers_file.write(" Desvio Estandar: ")
#outliers_file.write(str(dstandar))
#outliers_file.write(" modifiedThompson: ")
#outliers_file.write(str(modifiedThompson))
#outliers_file.write("\n")
#outliers_file.write("\n")


outliers_file.write("DRTT    outliers\n")

for dato in outliers:
    outliers_file.write(dato)
    outliers_file.write("\n")
    
outliers_file.close()

