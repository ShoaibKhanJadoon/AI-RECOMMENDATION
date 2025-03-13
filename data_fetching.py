import requests




def Fetch_Data(url):
    
    response = requests.get(url)
    data = response.json()   
    return data
       
    
    

if __name__=="__main__":    
    data=Fetch_Data()
    print(data)

