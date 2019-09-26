import math
import time
import cv2
import numpy as np
from dronekit import VehicleMode, connect

#stelan warna
hue_lower = 5
hue_upper = 130
saturation_lower = 5
saturation_upper = 40
value_lower = 60
value_upper = 180
min_contour_area = 500 # piksel terkecil pada kontur sebelum itu terdaftar sebagai target

#kamera
horizontal_resolution = 1280
vertical_resolution = 720

camera = cv2.VideoCapture(0)

#koneksi ke wahana
connection_string = "/dev/ttyS0"
baud_rate = 57600

print('connecting..')
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

print('start visual landing')

def send_land_message(x, y):
    msg = vehicle.message_factory.landing_target_encode(
        0,       
        0,       
        0,       
        (x-horizontal_resolution/2)*horizontal_fov/horizontal_resolution,
        (y-vertical_resolution/2)*vertical_fov/vertical_resolution,
        0,       
        0,0)     
    vehicle.send_mavlink(msg)
    vehicle.flush()

while(1):
    _,capture = camera.read()
    hsv = cv2.cvtColor(capture,cv2.COLOR_BGR2HSV)   
    inrangepixels = cv2.inRange(capture,np.array((hue_lower,saturation_lower,value_lower)),np.array((hue_upper,saturation_upper,value_upper)))#in opencv, HSV is 0-180,0-255,0-255
    tobecontourdetected = inrangepixels.copy()
    contours,hierarchy = cv2.findContours(tobecontourdetected,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    contour_sizes=[]
    contour_centroids = []
    for contour in contours:  
        real_area = cv2.contourArea(contour)
        if real_area > min_contour_area:
            M = cv2.moments(contour) #moment itu centroid
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            cv2.circle(capture,(cx,cy),5,(0,0,255),-1)
            contour_sizes.append(real_area)
            contour_centroids.append((cx,cy))
    
    #mendeeksi kontur terbesar (by area)    
    biggest_contour_index = 0
    for i in range(1,len(contour_sizes)):
        if contour_sizes[i] > contour_sizes[biggest_contour_index]:
            biggest_contour_index = i
    biggest_contour_centroid=None
    if len(contour_sizes)>0:
        biggest_contour_centroid=contour_centroids[biggest_contour_index]
    
    #jika kontur terbesar sudah ditemukan dan itu berwarna merah
    if biggest_contour_centroid is not None:
        cv2.circle(capture,biggest_contour_centroid,5,(0,0,255),-1)
        x,y = biggest_contour_centroid
        vehicle.mode = VehicleMode("LAND")
        send_land_message(x,y)

    
    cv2.imshow('capture',capture) 
        
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
camera.release()
