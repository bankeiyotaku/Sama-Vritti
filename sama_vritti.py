''' 
Copyright (c) 2021 Eugene Mesgar

'''


'''
Imported Librarries

'''

from gdx import gdx
from playsound import playsound
import math
import time
import statistics



breath_list = []
delta_list =  []

'''
Funcitons
'''



def breath_average( breath_val, count = 6 ):
    breath_list.append( round(breath_val,2) )
    list_size = len(breath_list)


    if list_size < count:
        return float('NaN')

    
    if list_size > count:
        breath_list.pop(0)


    return round(   statistics.median(breath_list.copy()) ,2)

        


'''

Main Code

'''



gdx = gdx.gdx()



'''GDX-RB 0K3003L6 BLE -45'''

gdx.open_ble("proximity_pairing")  


measurement_cycle = 10

pulse_bpm = 30
breath_bpm = 15
counter = 0



gdx.select_sensors([2])
gdx.start(measurement_cycle)


pulses_since_change=0

current=breath_bpm
last=current
last2=last
last3=last2


t0 = time.time()
t1 = t0



print(time.strftime("%H:%M:%S", time.localtime())," :Starting at default  breath rate ", breath_bpm, " (bpm) -- metronome at :", pulse_bpm, " (bpm)")

 
for i in range(0,100000000):
  
    
    beep_cycle = int(((60/pulse_bpm)*1000)) - 10

    t1 = t0
    t0 = time.time()
    
    measurement_cycle = int(float(t0 - t1)*1000) - 10
    counter += measurement_cycle
  

    
    if counter >= beep_cycle:
        playsound("beep.aiff")
        counter=0
    
    measurements = gdx.read()
    if measurements == None: 
        break
    
    if math.isnan(measurements[0]) == False and measurements[0] > 0:

        pulses_since_change += 1

        current = round(measurements[0],2)
        avg = breath_average( current )
        
        if math.isnan( avg ) == True:
            print(time.strftime("%H:%M:%S", time.localtime()),": No Average Yet: ", breath_list)
            continue
        

        delta = round  ( ((current - breath_bpm) / breath_bpm)*  100, 2)
        delta_list.append(delta)
        if( len(delta_list) > 5 ):
            delta_list.pop(0)
            


        delta_avg = round(sum(delta_list)/len(delta_list),2)
        delta_len = len(delta_list)
        

        print (time.strftime("%H:%M:%S", time.localtime()), ": Cur: ", current, " Avg: ", avg, " Delta: ", delta, "Delta Avg: ", delta_avg, "Delta Len: ", delta_len)
               


        if pulses_since_change < 5 or delta_len < 5:
            continue
        

        if avg <= breath_bpm:
            if delta_avg < -10:
                breath_bpm = round(avg,1)
                pulse_bpm = breath_bpm * 2
                pulses_since_change=0
                delta_list = []
                print(time.strftime("%H:%M:%S", time.localtime()), ":  LOWERING to", breath_bpm)
                continue
            elif abs(delta_avg) < 5:
                breath_bpm -= .2
                pulse_bpm = breath_bpm * 2
                pulses_since_change=0
                print(time.strftime("%H:%M:%S", time.localtime()), ": LOWERING to", breath_bpm)
                delta_list = []
                continue
      
                     
        if avg > breath_bpm:
            if delta_avg > 10:
                breath_bpm = round(avg,1)
                pulse_bpm = breath_bpm * 2
                pulses_since_change=0
                delta_list = []
                print(time.strftime("%H:%M:%S", time.localtime()), ": RAISING to", breath_bpm)
                continue
            '''elif abs(delta_avg) > 5:
                breath_bpm += .2
                pulse_bpm = breath_bpm * 2
                pulses_since_change=0
                delta_list = []
                print(time.strftime("%H:%M:%S", time.localtime()), ": RAISING to", breath_bpm)
                continue'''

           
        
        


gdx.stop()
gdx.close()
