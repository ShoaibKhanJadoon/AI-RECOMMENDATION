import requests


data= None

def Fetch_Data():
    global data
    url ="https://shopping-website-admin-eta.vercel.app/api/7541d19c-cab8-465c-a897-d01587954f8f/products"

    if data is None:               
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            data=None
        finally:
            return data
       
    return data
    

if __name__=="__main__":    
    data=Fetch_Data()
    print(data)

