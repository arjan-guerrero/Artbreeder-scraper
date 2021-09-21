import sys
import os
from PIL import Image
from os import name
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# extract IDs

input_folder = 'imgs/'

if not os.path.exists(input_folder):
    os.makedirs(input_folder)

imgs_IDs = []

for filename in os.listdir(input_folder):
    clean_name = os.path.splitext(filename)[0]
    imgs_IDs.append(clean_name)


# open site + login

driver = webdriver.Chrome('./chromedriver')

driver.maximize_window()

login_url = 'https://www.artbreeder.com/login'

driver.get(login_url)

email_add = driver.find_element_by_class_name('email')
email_add.clear()
email_add.send_keys('arjan.guerrero@gmail.com')

pass_add = driver.find_element_by_class_name('password')
pass_add.clear()
pass_add.send_keys('venadoartificial')

button = driver.find_element_by_class_name('submit')
button.click()

time.sleep(1)


# EXTRACT GEN PROFILE


def ex_profile(id):
    xo_url = f'https://www.artbreeder.com/i?k={id}'
    driver.get(xo_url)
    time.sleep(2)
    genes = driver.find_elements_by_class_name('gene_controller')
    gen_profile = []
    for gene in genes:
        name = gene.get_attribute('data-name')
        value = gene.get_attribute('data-original_value')
        gene_item = {
            'name': name,
            'value': value
        }
        gen_profile.append(gene_item)
    df = pd.DataFrame(gen_profile)
    print(f'Genetic profile of {id}:')
    print(df)
    print('\n')
    df.to_csv(f'GP-{id}.csv', index=False)


for id in imgs_IDs:
    ex_profile(id)

driver.close()
# driver.quit()

# NEXT
# save dataframes into one single 3D (3 axis) file?
# scraper ref: https://github.com/4m4n5/fifa18-all-player-statistics/tree/master/2019
