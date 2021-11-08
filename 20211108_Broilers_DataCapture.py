import sys
import os
from datetime import datetime
import time
import cv2

CurFileDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(CurFileDir)
print('CWD:      ', os.getcwd()) 
sys.path.append('./python')

import CSICAMERA as csicam
from ICHASEI2C import JoeI2C
import ICHASECFG as cfg
import IMGPROC as imgproc
from WS2812B import SPItoWS
import IBP as IBP

try:

    ## Read configuration and imformation
    info = cfg.readInfo('./ichase.cfg')        
    
    ## Definition of the variables
    filepath_withflash = info['path info']['Original'] ###original picture
    filepath_temp = info['path info']['Temporary'] ### temporary picture
    filepath_final = info['path info']['Final'] ### final picture
    filepath_noflash = info['path info']['Noflash'] 
    filepath_data_csv = info['path info']['Data_Csv'] 
    filepath_yolo_cfg = info['yolo info']['yolov4_cfg']
    filepath_coco_data = info['yolo info']['coco_data']
    filepath_weight = info['yolo info']['weight']
    url_data_weight = info['url info']['url_data_weight']   
    url_img_withflash = info['url info']['url_image_original'] 
    url_img_noflash = info['url info']['url_image_noflash']
    LED_Count = int(info['hardware info']['LED_count'])
    board_dia_ratio = float(info['hardware info']['Board_Dia_Ratio'])  
    drift_x_ratio = float(info['hardware info']['Cen_Drift_X_Ratio']) 
    drift_y_ratio = float(info['hardware info']['Cen_Drift_Y_Ratio']) 
    EntryDate = datetime.strptime(info['information']['EntryDate'], "%Y-%m-%d")
    print('Entry Date: ',EntryDate)

    CurDate = datetime.now()
    CurDate_str = CurDate.strftime("%Y-%m-%d %H:%M:%S")
    d_Date = CurDate-EntryDate
    CurWeek = int(d_Date.days/7) + 1
    sig = SPItoWS(LED_Count) 
    myI2C = JoeI2C()

    filepath_withflash_withweek = filepath_withflash + "/Week"+ str(CurWeek)
    filepath_noflash_withweek = filepath_noflash + "/Week"+ str(CurWeek)
    
    ### main program
    sig.Show_Color([0,0,0])
    sig.Show_Meteor(3)

    ### Capture the image
    ## No flash
    result_noflash = myI2C.readWeight()
    fig_noflash = csicam.show_camera()
    cv2.imwrite(cfg.check_os_dir_exist(filepath_noflash_withweek)+'/'+CurDate_str+ '.jpg',fig_noflash)

    sig.Show_Slowly(255,255,255)

    ## With flash
    result_withflash = myI2C.readWeight()
    fig_withflash = csicam.show_camera()
    cv2.imwrite(cfg.check_os_dir_exist(filepath_withflash_withweek)+'/'+CurDate_str+ '.jpg',fig_withflash)
    sig.Turn_off_slowly(255,255,255)

    ### Post-precessing
    ## Flash           
    pho = cv2.imread(filepath_withflash_withweek+'/'+CurDate_str+ '.jpg')
    width = pho.shape[1]
    height = pho.shape[0]
    cons = cv2.copyMakeBorder(pho, round(height*0.065), 0, 0, 0, cv2.BORDER_CONSTANT, value=0)
    font = cv2.FONT_HERSHEY_PLAIN
    text = CurDate_str +' With Flash '+'Total='+str(result_withflash) +'kg'
    img = cv2.putText(cons,text,(0,round(height*0.05)),font,4,(255,255,255),3,cv2.LINE_AA)         
    cv2.imwrite(cfg.check_os_dir_exist(filepath_withflash_withweek + '/AddComment')+'/'+CurDate_str+'.jpg',img) 

    ##No flash
    pho = cv2.imread(filepath_noflash_withweek+'/'+CurDate_str+ '.jpg')
    width = pho.shape[1]
    height = pho.shape[0]
    cons = cv2.copyMakeBorder(pho, round(height*0.065), 0, 0, 0, cv2.BORDER_CONSTANT, value=0)
    font = cv2.FONT_HERSHEY_PLAIN
    text = CurDate_str +' No Flash '+'Total='+str(result_noflash) +'kg'
    img = cv2.putText(cons,text,(0,round(height*0.05)),font,4,(255,255,255),3,cv2.LINE_AA)         
    cv2.imwrite(cfg.check_os_dir_exist(filepath_noflash_withweek + '/AddComment')+'/'+CurDate_str+'.jpg',img) 
    
    ## Save data to .csv file
    fieldnames = ['Date', 'Week', 'Total Weight(No Flash)','Total Weight(With Flash)']
    data = {
        'Date' : CurDate_str,
        'Week' : CurWeek,
        'Total Weight(No Flash)' : result_noflash,
        'Total Weight(With Flash)' : result_withflash
        }            
    cfg.append_dict_as_row(filepath_data_csv,data,fieldnames)

    ### Upload to IBP
    IBP.upload_data_to_IBP(CurDate,'weight_withflash', result_withflash , url_data_weight)
    IBP.upload_data_to_IBP(CurDate,'weight_noflash', result_noflash , url_data_weight)
    IBP.upload_img_to_IBP(CurDate, filepath_withflash_withweek + '/AddComment'+'/'+CurDate_str+'.jpg', url_img_withflash)
    IBP.upload_img_to_IBP(CurDate, filepath_noflash_withweek + '/AddComment'+'/'+CurDate_str+'.jpg' , url_img_noflash)
except KeyboardInterrupt:
    print("Exiting Program")




