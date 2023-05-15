import cv2
import time
import serial
import struct

# seri = serial.Serial("COM3",9600)   
# time.sleep(2)                       

Algorithms = {            "Boosting"  : cv2.TrackerBoosting_create,
                          "CSRT"      : cv2.TrackerCSRT_create,
		                  "KCF"       : cv2.TrackerKCF_create,
                          "Mil"       : cv2.TrackerMIL_create,
                          "MedianFlow": cv2.TrackerMedianFlow_create,
		                  "Mosse"     : cv2.TrackerMOSSE_create,
		                  "TLD"       : cv2.TrackerTLD_create}             
		              	                  
NumAlgorithms = { "1"    : "Boosting",
                  "2"    : "CSRT",
                  "3"    : "KCF",
                  "4"    : "Mil",
                  "5"    : "MedianFlow",
                  "6"    : "Mosse",
                  "7"    : "TLD"}

NameAlgorithm = ["Boosting"]
RunAlgorithm = Algorithms[NameAlgorithm[0]]() 
choice = 0

print('''
      1. Boosting
      2. CSRT
      3. KCF
      4. Mil
      5. MedianFlow
      6. Mosse
      7. TLD
   ''')

choice = input("Choose an Algorithm  : ")
keys = NumAlgorithms.keys() 
if choice in keys: 
    NameAlgorithm.append(NumAlgorithms[choice]) 
    NameAlgorithm.remove(NameAlgorithm[0]) 
    print(choice, NameAlgorithm) 
    RunAlgorithm = Algorithms[NameAlgorithm[len(NameAlgorithm)-1]]() 
        
else: 
    print("Invalid Input Value {}".format(NameAlgorithm))

cap = cv2.VideoCapture(0) 

xloc=[90] 
yloc=[90] 

rsuc, img = cap.read() 

while True:
    timer = cv2.getTickCount()
    rsuc, img = cap.read()
    rsuc, coorpln = RunAlgorithm.update(img)
    
    if rsuc: 
        x, y, w, h = int(coorpln[0]),int(coorpln[1]),int(coorpln[2]),int(coorpln[3])
        mid_x = int(x+w/2)
        mid_y = int(y+h/2)
        
        print(" ")
        print(coorpln)
        cv2.rectangle(img, (x,y), ((x+w), (y+h)), (0,255,0), 5, 1) 
        cv2.putText(img,"Object At :",(10,15),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2) 
        cv2.putText(img,"X ="+str(mid_x),(140,15),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2) 
        cv2.putText(img,"Y ="+str(mid_y),(240,15),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2)
        cv2.putText(img,"Algorithm : "+NameAlgorithm[0],(10,450),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2)
    
        if mid_x > 300 and mid_x < 340: 
            print("locked_x")
            xloc.append(xloc[len(xloc)-1]) 
            xloc.remove(xloc[0]) 

        elif mid_x > 340:
            print("right")
            xloc.append(xloc[len(xloc)-1]-1) 
            xloc.remove(xloc[0])

        elif mid_x < 300: 
            print("left")
            xloc.append(xloc[len(xloc)-1]+1) 
            xloc.remove(xloc[0])

        xpos=xloc[len(xloc)-1] 
    
        if mid_y > 220 and mid_y < 260:
            print("locked_y")
            yloc.append(yloc[len(yloc)-1])
            yloc.remove(yloc[0])

        elif mid_y > 260:
            print("down")
            yloc.append(yloc[len(yloc)-1]+1)
            yloc.remove(yloc[0])

        elif mid_y < 220:
            print("up")
            yloc.append(yloc[len(yloc)-1]-1)
            yloc.remove(yloc[0])

        ypos=yloc[len(yloc)-1]
    
        if xpos >= 180:
            xloc.append(xloc[len(xloc)-1]-1)
            xloc.remove(xloc[0])
            print("x max 180")
            
        elif xpos <= 0:
            xloc.append(xloc[len(xloc)-1]+1)
            xloc.remove(xloc[0])
            print("x min 0")
        
        if ypos >= 180:
            yloc.append(yloc[len(yloc)-1]-1)
            yloc.remove(yloc[0])
            print("y max 180")
        
        elif ypos <= 0:
            yloc.append(yloc[len(yloc)-1]+1)
            yloc.remove(yloc[0])
            print("y min 0")
    
        print(xpos,ypos) 
        # seri.write(struct.pack('>BB', xpos,ypos)) 

    else: 
        cv2.putText(img,"Press : X",(10,5),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2)
    
    cv2.imshow("Tracking",img) 
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("x"):
        bbox = cv2.selectROI("Tracking", img, False)
        RunAlgorithm.init(img,bbox) 
        
    elif key == ord("q"): 
        break

cap.release()
cv2.destroyAllWindows()         