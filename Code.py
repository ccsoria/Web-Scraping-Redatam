
#El Redatam cuenta con multiples cuadros y en este codigo unicamente se busca descargar el cuadro 26,
#el cual hace referencia a cultivos transitorios.

import os
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(service=Service("C:/Program Files/Chromedriver/chromedriver.exe"))

driver.get('https://censos.inei.gob.pe/bcoCuadros/IIIcenagro.htm')

#Nuevo frame
frame1 = driver.find_element('xpath','/html/frameset/frame')
driver.switch_to.frame(frame1)

#Nuevo frame
frame2 = driver.find_element('xpath','/html/body/form/div[2]/div/iframe')
driver.switch_to.frame(frame2)

#Departamento
conteo_dpto = driver.find_element('id','cmbDepartamento')
n_dpto = conteo_dpto.find_elements(By.TAG_NAME,'option')
selec_dpto = Select(driver.find_element('id','cmbDepartamento'))
for dpto in range(1,len(n_dpto)):
	selec_dpto.select_by_index(dpto)
	v_dpto = selec_dpto.options[dpto].text

	#Base de dato
	base_dato = []

	#Provincia
	time.sleep(2)
	conteo_prov = driver.find_element('id','cmbProvincia')
	n_prov = conteo_prov.find_elements(By.TAG_NAME,'option')
	selec_prov = Select(driver.find_element('id','cmbProvincia'))
	for prov in range(1,len(n_prov)):
		selec_prov.select_by_index(prov)
		v_prov = selec_prov.options[prov].text

		#Distrito
		time.sleep(2)
		conteo_dist = driver.find_element('id','cmbDistrito')
		n_dist = conteo_dist.find_elements(By.TAG_NAME,'option')
		selec_dist = Select(driver.find_element('id','cmbDistrito'))
		for dist in range(1,len(n_dist)):
			selec_dist.select_by_index(dist)
			v_dist = selec_dist.options[dist].text

			#Ver tablas
			driver.find_element('id','btnVer').click()

			#Nuevo frame
			frame3 = driver.find_element('id','frmResultado')
			driver.switch_to.frame(frame3)
			time.sleep(1)

			#Conteo de cuadros
			conteo_cuadro = driver.find_element('xpath','/html/body')
			n_cuadro = conteo_cuadro.find_elements(By.TAG_NAME,'ul')
			for cuadro in range(1,len(n_cuadro)):
				str_cuadro = driver.find_element('xpath','/html/body/ul[' + str(cuadro) + ']/li/font/a').text

				#Cultivo transitorio - Cuadro 26
				if "CUADRO Nº 26" in str_cuadro:
					print(str_cuadro)
					driver.find_element('xpath','/html/body/ul[' + str(cuadro) + ']/li/font/a').click()
					time.sleep(2)

					#Extraer. Algunos cuadros no tienen el mismo formato y es necesario 
					#revisar la base despues de que se ha extraido la informacion
					try:
						v_ua = driver.find_element('xpath','/html/body/table/tbody/tr[10]/td[3]').text
						v_sa = driver.find_element('xpath','/html/body/table/tbody/tr[11]/td[3]').text

					except:
						v_ua = "Ver pagina"
						v_sa = "Ver pagina"

					#Descargar
					base_dato.append([dpto,v_dpto,prov,v_prov,dist,v_dist,v_ua,v_sa])
					df = pd.DataFrame(base_dato,columns=['dpto','dpto_valor','prov','prov_valor','dist','dist_valor','ua','sa'])
					df.to_csv('A_' + str(dpto) + '.csv',encoding='utf-8-sig',index=False)

					#Regresar
					driver.find_element('xpath','/html/body/div[1]/input').click()
					time.sleep(1)

					break

				else:
					pass

			#Frame anterior
			driver.switch_to.parent_frame()
