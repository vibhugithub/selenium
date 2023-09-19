import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

def flight_time(timeob):
    timeing=''
    for arr in timeob:
        temp=arr.find_all('span')
        timeing=temp[0].text
    return timeing

def miles_price(miles_st):
    temp=''
    for arr in miles_st:
        temp= arr
    try:
        temp=miles_st[0].text
    except:
        print([mil.text for mil in miles_st])
    return temp


chrome_options = Options()
# chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage");
# chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')

# chrome_options.add_argument("--window-size=1920x1080")
#driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chrome.exe",options=chrome_options)
# go to Indeed.com
driver  = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.united.com/en/us/")

# Wait for initialize, in seconds
wait = WebDriverWait(driver, 10)

#Logic to check if flight search form is there on the page
wait.until(EC.visibility_of_element_located((By.ID, "bookFlightForm")))


# one way radio button click
driver.find_element(By.XPATH,"//form[@id='bookFlightForm']/div/fieldset/div/label[2]/span[2]").click()

# # Book with miles  checkbox  click
driver.find_element(By.XPATH,"//form[@id='bookFlightForm']/div/div/label").click()

# flexible date check box click
driver.find_element(By.ID,"flexDatesLabel").click()

# clear source, enter sourse ita, click on the first matching data
driver.find_element(By.ID,"bookFlightOriginInput").click()
driver.find_element(By.ID,"bookFlightOriginInput").clear()
driver.find_element(By.ID,"bookFlightOriginInput").send_keys("LAX")
time.sleep(3)
driver.find_element(By.XPATH,"//li[@id='autocomplete-item-0']/button/span").click()

# clik on the search flights button
driver.find_element(By.XPATH,"//button[@type='submit']").click()

time.sleep(3)
# click on the drop down

wait.until(EC.visibility_of_element_located((By.XPATH,"//form[@id='mapSearchForm']/div[2]/div[3]/div/button")))
driver.find_element(By.XPATH,"//form[@id='mapSearchForm']/div[2]/div[3]/div/button").click()

time.sleep(3)
#Logic to check if flight search form is there on the page
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".app-components-PlacesFilters-HorizontalMapSearchForm-styles__active--3WvrY")))
driver.find_element(By.ID,"awards").click()

#
# driver.find_element(By.XPATH,"//div[@id='advanceFilterSection']/div/div/label/div[2]").click()
time.sleep(3)
#driver.find_element(By.XPATH,"//button[@type='submit']").click()
driver.find_element(By.XPATH,"//div[@class='app-components-PlacesFilters-HorizontalMapSearchForm-styles__actions--1BuhX']/button").click()
time.sleep(3)
driver.find_element(By.XPATH,"//div[@class='app-components-PlacesFilters-HorizontalMapSearchForm-styles__actions--1BuhX']/button").click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@class="atm-c-accordion-panel__button atm-js-accordion-btn"]').click()
time.sleep(10)
li=len(driver.find_elements(By.XPATH,'//*[@class="atm-c-accordion-panel__body"]/div/div/div/ul/li'))-1
print(li)
i=1
datalist=[]
while i is not li:
    print(i)
    if i > 1:
        wait.until(EC.element_to_be_clickable((By.XPATH,"//form[@id='mapSearchForm']/div[2]/div[3]/div/button"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".app-components-PlacesFilters-HorizontalMapSearchForm-styles__active--3WvrY")))
        driver.find_element(By.ID,"awards").click()
        #wait.until(EC.element_to_be_clickable((By.ID,"awards"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='app-components-PlacesFilters-HorizontalMapSearchForm-styles__actions--1BuhX']/button"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='app-components-PlacesFilters-HorizontalMapSearchForm-styles__actions--1BuhX']/button"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@class="atm-c-accordion-panel__button atm-js-accordion-btn"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@class="atm-c-accordion-panel__body"]/div/div/div/ul/li[{i}]/button[2]'))).click()
    #driver.find_element(By.XPATH,f'//*[@class="atm-c-accordion-panel__body"]/div/div/div/ul/li[{i}]/button[2]').click()
    time.sleep(10)
    try:
        driver.find_element(By.ID,"closeBtn").click()
        #wait.until(EC.element_to_be_clickable((By.ID,"closeBtn"))).click()
    except:
        pass
    #driver.find_element(By.ID,"closeBtn").click()
    time.sleep(10)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    results = soup.find_all('div',{'class':'app-components-Shopping-ResultRow-styles__resultRow--1WfbI','role':'row'})
    j=0
    print(len(results))
    flightlist=[]
    for result in results:
        tempdict={}
        #print(j)
        j+=1
        if j==1 :
            continue
        time.sleep(2)
        depart_st=result.find_all('div',{'class':'app-components-Shopping-FlightInfoBlock-styles__departTime--oRDUv'})
        arrival_st=result.find_all('div',{'class':'app-components-Shopping-FlightInfoBlock-styles__arrivalTime--1V4Lg'})
        departplace_st=result.find_all('div',{'class':'app-components-Shopping-FlightInfoBlock-styles__airport--1VYmb app-components-Shopping-FlightInfoBlock-styles__departAirport--1V3Dd'})
        arrivalplace_st=result.find_all('div',{'class':'app-components-Shopping-FlightInfoBlock-styles__airport--1VYmb app-components-Shopping-FlightInfoBlock-styles__arrivalAirport--2976a'})
        miles_st=result.find_all('div',{'class':'app-components-Shopping-Miles-styles__fontStyle--3swxB'})
        tempdict["depart_time"]=flight_time(depart_st)
        tempdict["depart_place"]=flight_time(departplace_st)
        tempdict["arrival_time"]=flight_time(arrival_st)
        tempdict["arrival_place"]=flight_time(arrivalplace_st)
        tempdict["miles_cost"]=miles_price(miles_st)
        
        #print(tempdict["depart_time"]," depart_time ",tempdict["depart_place"]," depart_place ",tempdict["arrival_time"]," arrival_time ",tempdict["arrival_place"]," arrival_place ",tempdict["miles_cost"]," miles_cost ")
        
        flightlist.append(tempdict)
        
        
        
        


    datalist.append({"flightlist":flightlist})    
    soup.prettify()
    """
    with open('dumping.html', "w", encoding='utf-8') as file:
        file.write(str(soup))
    """
    driver.back()
    time.sleep(10)
    i+=1
    #break
print(datalist)

with open('data.json', 'w') as f:
    json.dump({"datalist":datalist}, f)
time.sleep(10)

driver.back()

time.sleep(10)
#//*[@id="3u7Xa2Lfy6"]/div/div/div/ul/li[2]/button[2]
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
results = soup.find_all('ul',{'aria-label':True})

soup.prettify()
with open('dump.html', "w", encoding='utf-8') as file:
    file.write(str(soup))
temp=""
for ul in results:
    if ul['aria-label']=="search results":
        with open("output.txt", 'w') as file:
            for li in ul.find_all("li"):
                button = li.find_all('button')[1]
                divs = button.find_all('div')
                for div in divs:
                    if div.text != temp:
                        file.write(str(div.text)+"\n\n")
                        temp=div.text

print("hello")




