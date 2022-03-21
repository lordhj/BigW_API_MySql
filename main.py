print("hi")
import requests
import mysql.connector
from urllib3 import connection_from_url


#Creating empty lists for all fields
id_list=[]
store_list = []
phone_list=[]
street_list=[]
suburb_list=[]
state_list=[]
postcode_list=[]
lat_list=[]
long_list=[]

#Retrieving DATA from API
api_endpoint = "https://api.bigw.com.au/api/stores/v0/list"
response = requests.get(api_endpoint)
data=response.json()
data_list = [value for (key,value) in data.items()]
len_list = len(data_list)
for _ in range(len_list):
    item_data = data_list[_]
    id_list.append(item_data['id'])
    store_list.append(item_data['name'])
    phone_list.append(item_data['phoneNumber'])
    street_list.append(item_data['address']['street'])
    suburb_list.append(item_data['address']['suburb'])
    state_list.append(item_data['address']['state'])
    postcode_list.append(item_data['address']['postcode'])
    lat_list.append(item_data['location']['lat'])
    long_list.append(item_data['location']['lng'])
print("API task successful")

#Integrating Data in SQL
connection = mysql.connector.connect(host='localhost',
                                    database='Store',
                                    user='Harshit',
                                    password='Harshit@123')
mySql_Create_Table_Query = """CREATE TABLE Store_Info ( 
    Id int(11) NOT NULL, 
    StoreName varchar(250) NOT NULL, 
    PhoneNumber int(12) NOT NULL,
    Street varchar(250) NOT NULL,
    Suburb varchar(250) NOT NULL,
    State varchar(250) NOT NULL,
    Postcode varchar(250) NOT NULL,
    Lat float NOT NULL,
    Lng float NOT NULL,
    PRIMARY KEY (Id))"""
cursor = connection.cursor()
result = cursor.execute(mySql_Create_Table_Query)
print("Table created")
add_StoreInfo = ("INSERT INTO Store_Info"
                "(Id, StoreName, PhoneNumber, Street, Suburb, State, Postcode, Lat, Lng)"
                "VALUES(%d, %s, %d, %s, %s, %s, %s, %f, %f)")
for  i in range(len_list):
    data_Store = (id_list[i], store_list[i], phone_list[i], street_list[i], suburb_list[i], state_list[i], postcode_list[i], lat_list[i], long_list[i])
    cursor.execute(add_StoreInfo, data_Store)
connection.commit()




cursor.close()
connection.close()