from csv import DictWriter
import os
from datetime import datetime

def check_os_dir_exist(filepath):
    path_split = filepath.split('/')
    Cur_Check_Path = ''
    for path_section_num in path_split:
        if(path_section_num) == '.':
            Cur_Check_Path = '.'
        else:
            Cur_Check_Path = Cur_Check_Path +'/'+ path_section_num

        if not os.path.exists(Cur_Check_Path):
            print("Dir is not existed, create a new dir : " + os.path.abspath(Cur_Check_Path))
            os.mkdir(Cur_Check_Path)
    return Cur_Check_Path

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    is_firstfile = not os.path.isfile(file_name)
    with open(file_name, 'a+', newline='') as write_obj:        
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)        
        if is_firstfile:
            print("csv file is not exist, create new one and add header.")
            dict_writer.writeheader()
            # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

def readInfo(filename):
    Info = dict()
    with open(filename,'r') as file:
        line = file.readline()
        while line:
            line = file.readline()
            print(line.strip())
            if  '<Information>' in line:
                info=readinfo_2dict(file)
                Info.update({'information': info})
            elif '<Algorithm>' in line:
                info=readinfo_2dict(file)
                Info.update({'algorithm info': info})
            elif '<Hardware>' in line:
                info=readinfo_2dict(file)
                Info.update({'hardware info': info})
            elif  '<YoloFile>' in line:
                info=readinfo_2dict(file)
                Info.update({'yolo info' : info})
            elif  '<FilePath>' in line:
                info=readinfo_2dict(file)
                Info.update({'path info': info})
            elif  '<URL>' in line:
                info=readinfo_2dict(file)
                Info.update({'url info': info})
    Info_verified=version_check(Info)
    print(Info_verified) 
    return Info_verified

def readinfo_2dict(file):
        line = file.readline()
        print(line.strip())  
        dic_temp = dict()
        while line:
            if not '##' in line:
                str_split= line.strip().split('=')
                item = str_split[0].strip()
                config = str_split[1].strip()   
                dic_temp.update({item:config}) 
                line = file.readline()
                print(line.strip())                    
            else:
                break 
        return dic_temp  

def version_check(info):
    CurFileName = os.path.basename(__file__)
    CfgFileName = info['algorithm info']['main_filename']
    #print("CurFileName: ", CurFileName)
    if not CurFileName ==  CfgFileName:
        print("Error!! File Version is Not Matched")
        quit()
    else:
        return info   

if __name__ == "__main__":

    try : 
        ## Read configuration and imformation
        info = readInfo('./ichase.cfg')   
        ## Definition of the variables
        filepath = info['path info']['Original'] ###original picture
        filepath_temp = info['path info']['Temporary'] ### temporary picture
        filepath_final = info['path info']['Final'] ### final picture
        filepath_noflash = info['path info']['Noflash'] 
        filepath_data_csv = info['path info']['Data_Csv'] 
        filepath_yolo_cfg = info['yolo info']['yolov4_cfg']
        filepath_coco_data = info['yolo info']['coco_data']
        filepath_weight = info['yolo info']['weight']
        url = info['url info']['url_data_weight']   
        url1 = info['url info']['url_image_original'] 
        url2 = info['url info']['url_data_AVGweight']
        url3 = info['url info']['url_image_noflash']
        url_image_detection = info['url info']['url_image_detection']
        LED_Count = int(info['hardware info']['LED_count'])
        board_dia_ratio = float(info['hardware info']['Board_Dia_Ratio'])  
        drift_x_ratio = float(info['hardware info']['Cen_Drift_X_Ratio']) 
        drift_y_ratio = float(info['hardware info']['Cen_Drift_Y_Ratio']) 
        EntryDate = datetime.strptime(info['information']['EntryDate'], "%Y-%m-%d")

    except KeyboardInterrupt:
        print("Exiting Program")