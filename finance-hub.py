#IMPORTS
import requests
import json
import os
import csv

#VARIABLES
name = ""
id = 0
email = ""
price = 1
quantity = 1
cost = 1

#SETUP
API_ENDPOINT = "https://api.notion.com/v1/pages"
NOTION_TOKEN = os.environ.get("NOTION")
DATABASE_ID = "16a656910f9041f3beb889ddd3a9bb0c"
headers = {"Authorization": "Bearer " + NOTION_TOKEN,"Content-Type": "application/json","Notion-Version": "2021-08-16"}
num = 0
with open("num.txt","r") as f:
    num = int(f.read())
    f.close()
with open("num.txt","w") as f:
    num = num + 1
    f.write(str(num))

#FUNCTIONS
def setvariables(data_):
    global name, id, email, price, quantity, cost
    try:
        name = str(data_[0])
        id = int(data_[1])
        email = str(data_[2])
        price = float(data_[3])
        quantity = int(data_[4])
        cost = float(data_[5])
        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "ID": {"number": id},
                "Customer": {"email": email},
                "Price": {"number": price},
                "Quantity": {"number": quantity},
                "Cost": {"number": cost},
            }
        }
        return data
    except Exception as e:
        print("Error: Wrong Format\nname: text\nid: number\nemail: text\nprice: number\nquantity: number\ncost: number")
        print(f"Error Message: {e}")
        
def addproduct(data_):
    data = setvariables(data_)
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    if "error" in str(response.json()):
        return "Notion API Error"
    else:
        return "Product Added to Notion Successfully"

def run(path):
    with open(path) as csvfile:
        reader_ = list(csv.reader(csvfile))[1:]
        for lst in reader_:
            lst.insert(1,num)
            print(f"Product Data: {lst}")
            print(addproduct(lst))
    f = open(path,"w")
    f.write("Product,Email,Price,Quantity,Cost\n")
#RUN
run("product.csv")
