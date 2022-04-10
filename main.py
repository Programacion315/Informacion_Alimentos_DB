from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
#Nuevas
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
#Fin nuevas
import os
import time

import requests
from bs4 import BeautifulSoup

#Conexion base de datos
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="admin",
    db="comida"
)

cursor = connection.cursor()


#EDITAR
#Cambiar ruta donde se instalo el selenium en tu maquina!
from selenium.webdriver.support.wait import WebDriverWait
chromePath= Service(r'C:\Users\jluiso315\Documents\driver\chromedriver.exe')
driver=webdriver.Chrome(service = chromePath)


#Entramos a la pagina web deseada
search_URL = "https://www.tabladecalorias.net/"
driver.get(search_URL)


time.sleep(2)

#Guardamos todos los links dentro de un arreglo

#Me devuelve todos los elementos con tag a.


tag_a = driver.find_elements(by=By.TAG_NAME,value="a")


nombre = []
counter = 0
for con in tag_a:
    if counter > 9 and counter < 54:
        nombre.append(con.get_attribute('href'))
    counter += 1
print(nombre)

for link in nombre:
    #driver.find_element(By.LINK_TEXT, link).click()
    driver.get(link)

    #Cuando entre queremos usar beautiful soup para
    #robarnos los datos de las tablas
    url = link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    league_table = soup.find('table', class_ = 'table')


    for team in league_table.find_all('tbody'):
        rows = team.find_all('tr')
        for row in rows:
            nombreComida = row.find('td', class_= 'food').text
            cantidad = row.find('td', class_='serving 100g').text
            calorias = row.find('td', class_='kcal').text

            #Instruccion sql para llenar nuestra base de datos.
            #print(f"{nombreComida} - {cantidad} - {calorias}")
            sql = f"INSERT INTO alimento(nombre, cantidad, calorias) VALUES('{nombreComida}', '{cantidad}', '{calorias}')"
            cursor.execute(sql)
            connection.commit()

    time.sleep(2)




