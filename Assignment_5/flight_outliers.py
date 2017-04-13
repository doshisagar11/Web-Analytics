import bs4
import time
from collections import OrderedDict
import unidecode
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import scatter
from matplotlib.pyplot import subplots
import datetime
from dateutil.parser import parse
import time
import os
from datetime import datetime
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean

driver = webdriver.Chrome("C:/Users/Sagar Doshi/Downloads/chromedriver")
driver.get('https://www.google.com/flights/explore/')

from datetime import date


class DataFrame(object):
    def __init__(self, list_of_list, header=True):
        if header:
            self.header = list_of_list[0]
            self.data = list_of_list[1:]
        else:
            self.header = list_of_list[0]
            self.data = list_of_list[1:]
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]


def scrape_data(start_date, from_place, to_place, city_name):

    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.20)
    # The place we want to fly to, that location is shown by the xpath below
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.50)
    curr_url = driver.current_url
    changed_url = curr_url + 'd=' + str(start_date.year) + '-0' + str(start_date.month) + '-' + str(start_date.day)

    driver.close()
    up_driver = webdriver.Chrome("C:/Users/Sagar Doshi/Downloads/chromedriver")
    up_driver.get(changed_url)
    time.sleep(0.50)

    results = up_driver.find_elements_by_class_name('LJTSM3-v-d')
    time.sleep(0.50)
    j=0
    x = []
    y = []
    i=0
    while i < len(results):
        print(len(results))
        print(i)
        city = results[i].find_element_by_class_name('LJTSM3-v-c').text
        time.sleep(0.50)

        cityname = city.split(',')[0].strip().lower()

        if cityname == city_name.lower():
            bars = results[i].find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(0.50)
            for bar in bars:
                ActionChains(up_driver).move_to_element(bar).perform()
                time.sleep(0.50)
                x.append(
                    (results[i].find_element_by_class_name('LJTSM3-w-w').text,
                     results[i].find_element_by_class_name('LJTSM3-w-h').text))
                j += 1
            break
        else:
            print(cityname)
            print('else chal raha hai')
            i = i + 1
            continue
    for dum in x:
        print(dum[0])
        price = float(dum[0].replace('$', '').replace(',', ''))
        date = parse(dum[1].split('-')[0].strip())
        y.append((price, date))

    df = pd.DataFrame(y, columns=['Price', 'Date'])
    print(df)

def scrape_data_90(start_date, from_place, to_place, city_name):
    driver = webdriver.Chrome("C:/Users/Sagar Doshi/Downloads/chromedriver")
    driver.get('https://www.google.com/flights/explore/')
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.20)
    # The place we want to fly to, that location is shown by the xpath below
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.50)
    curr_url = driver.current_url
    changed_url = curr_url + 'd=' + str(start_date.year) + '-0' + str(start_date.month) + '-' + str(start_date.day)

    driver.close()
    up_driver = webdriver.Chrome("C:/Users/Sagar Doshi/Downloads/chromedriver")
    up_driver.get(changed_url)
    time.sleep(0.50)

    results = up_driver.find_elements_by_class_name('LJTSM3-v-d')
    time.sleep(0.50)
    j = 0
    x = []
    y = []
    i = 0
    while i < len(results):
        print(len(results))
        print(i)
        city = results[i].find_element_by_class_name('LJTSM3-v-c').text
        time.sleep(0.50)

        cityname = city.split(',')[0].strip().lower()

        if cityname == city_name.lower():
            bars = results[i].find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(0.50)
            for bar in bars:
                ActionChains(up_driver).move_to_element(bar).perform()
                time.sleep(0.50)
                x.append(
                    (results[i].find_element_by_class_name('LJTSM3-w-w').text,
                     results[i].find_element_by_class_name('LJTSM3-w-h').text))
                j += 1
            break
        else:
            print(cityname)
            print('else chal raha hai')
            i = i + 1
            continue

    up_driver.find_element_by_class_name('LJTSM3-w-C').click()

    time.sleep(0.9)
    results = up_driver.find_elements_by_class_name('LJTSM3-v-d')
    time.sleep(0.9)

    i = 0
    while i < len(results):
        print(len(results))
        city = results[i].find_element_by_class_name('LJTSM3-v-c').text
        time.sleep(0.50)

        cityname = city.split(',')[0].strip().lower()

        if cityname == city_name.lower():
            bars = results[i].find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(0.50)
            for bar in bars:
                if j == 90:
                    break

                else:
                    ActionChains(up_driver).move_to_element(bar).perform()
                    time.sleep(0.50)
                    if (results[i].find_element_by_class_name('LJTSM3-w-w').text,
                        results[i].find_element_by_class_name('LJTSM3-w-h').text) in x:
                        continue
                    else:
                        x.append(
                            (results[i].find_element_by_class_name('LJTSM3-w-w').text,
                             results[i].find_element_by_class_name('LJTSM3-w-h').text))
                        j += 1

            break
        else:
            print(cityname)
            print('else chal raha hai')
            i += 1
            continue

    for dum in x:
        price = float(dum[0].replace('$', '').replace(',', ''))
        date = parse(dum[1].split('-')[0].strip())
        y.append((price, date))

    df = pd.DataFrame(y, columns=['Price', 'Date'])
    print (df)




def task_3_dbscan(start_date, from_place, to_place, city_name):

    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.20)
    # The place we want to fly to, that location is shown by the xpath below
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.50)
    curr_url = driver.current_url
    changed_url = curr_url + 'd=' + str(start_date.year) + '-0' + str(start_date.month) + '-' + str(start_date.day)

    driver.close()
    up_driver = webdriver.Chrome("C:/Users/Sagar Doshi/Downloads/chromedriver")
    up_driver.get(changed_url)
    time.sleep(0.50)

    results = up_driver.find_elements_by_class_name('LJTSM3-v-d')
    time.sleep(0.50)
    j = 0
    x = []
    y = []
    i = 0
    while i < len(results):
        print(len(results))
        print(i)
        city = results[i].find_element_by_class_name('LJTSM3-v-c').text
        time.sleep(0.50)

        cityname = city.split(',')[0].strip().lower()

        if cityname == city_name.lower():
            bars = results[i].find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(0.50)
            for bar in bars:
                ActionChains(up_driver).move_to_element(bar).perform()
                time.sleep(0.50)
                x.append(
                    (results[i].find_element_by_class_name('LJTSM3-w-w').text,
                     results[i].find_element_by_class_name('LJTSM3-w-h').text))
                j += 1
            break
        else:
            print(cityname)
            print('else chal raha hai')
            i = i + 1
            continue
    for dum in x:
        print(dum[0])
        price = float(dum[0].replace('$', '').replace(',', ''))
        date = parse(dum[1].split('-')[0].strip())
        y.append((price, date))

    df = pd.DataFrame(y, columns=['Price', 'Date'])
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(np.arange(len(df['Date'])), df['Price'])
    #plt.show()
    #df.plot(x='Date', y='Price', style='o')
    #df.plot.show()
    px = [x for x in df['Price']]
    ff = pd.DataFrame(px, columns=['fare']).reset_index()
    X = StandardScaler().fit_transform(ff)
    db = DBSCAN(eps=1.0, min_samples=5).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(12, 8))

    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=14)

    plt.title("Total Clusters: {}".format(clusters), fontsize=14,y=1.01)
    #plt.show()
    # get the distances to each clusters
    lbls = np.unique(db.labels_)
    print "Cluster labels: {}".format(np.unique(lbls))

    cluster_means = [np.mean(X[labels == num, :], axis=0) for num in range(lbls[-1] + 1)]
    print "Cluster Means: {}".format(cluster_means)
    mistake_cluster = X[labels==-1]
    print mistake_cluster
    outlier = []
    # euclidean
    for mistake_point in mistake_cluster:
        dist = [euclidean(mistake_point, cm) for cm in cluster_means]
        print "Euclidean distance: {}".format(dist)

        nearest_cluster = min(dist)
        print nearest_cluster
        index = dist.index(min(dist))

        cluster_price = X[labels == index]
        print cluster_price
        price_nearby = [i[1] for i in cluster_price]
        cluster_2sd = np.std(np.array(price_nearby)) * 2

        print mistake_point[1], cluster_means[index][1]
        print abs((mistake_point[1] - (cluster_means[index][1]))), " > ", cluster_2sd
        print (mistake_point[1] - (cluster_means[index][1])) > cluster_2sd
        print abs((mistake_point[1] - cluster_means[index][1])), " >=", "1"
        print (mistake_point[1] - cluster_means[index][1]) >= 1
        if abs((mistake_point[1] - (cluster_means[index][1]))) > cluster_2sd and abs(
                (mistake_point[1] - cluster_means[index][1])) >= 1:
            outlier.append(mistake_point)

    print outlier
    plt.show()
today = date.today()
#scrape_data(today,'New York City', 'South America', 'Aruba')
#scrape_data_90(today,'New York City', 'South America', 'Aruba')
task_3_dbscan(today,'New York City', 'South America', 'Aruba')
