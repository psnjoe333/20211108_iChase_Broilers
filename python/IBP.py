import requests
import json
import datetime

### Upload_img_to_IBP
def upload_img_to_IBP(dataTime,dataName, url1):    
    #dataTime = time.strftime("%Y-%m-%d %H:%M:%S")
    query = {'dataTime' : dataTime.strftime("%Y-%m-%d %H:%M:%S")}
    files = {'file': open(dataName, 'rb')}
    try:
        print("Uploaded to: ", url1)
        res = requests.post(url1, files=files, data=query, timeout=5)
        print(res.text) 
        print('Uploaded Successed!!')     
    except:
        print(res.text)
        print('Uploaded Failed!!')  

### Upload_data_to_IBP
def upload_data_to_IBP(dataTime,dataName, data, url): 
    headers = {"Content-Type":"application/json"}    
    query = {'dataTime':dataTime.strftime("%Y-%m-%d %H:%M:%S"), dataName:"{:.2f}".format(data)}
    query_j = json.dumps(query)
    print(query_j)
    try:
        print("Uploaded to: ", url)
        res = requests.post(url, data=query_j,headers=headers)
        print(res.text) 
        print('Uploaded Successed!!')     
    except:
        print(res.text)
        print('Uploaded Failed!!')  
