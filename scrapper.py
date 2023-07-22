#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from parsel import Selector
import urllib3
import pandas as pd
from time import sleep
from selenium.webdriver.support.select import Select
pd.options.mode.chained_assignment = None

driver = webdriver.Chrome()

def credentials():
         f = open("creds.txt", "r")
         creds = f.read()
         f.close()
         creds = creds.split('\n')
         username = creds[0]
         password = creds[1]
         return [username, password]

def login():
        #try:
            driver.get("https://mycpa.cpa.state.tx.us/cong/leaseNumberAction.do")
            # driver.find_element_by_xpath("/html/body/div[4]/table/tbody/tr/td[2]/div/a[2]").click()
            driver.find_element(By.XPATH, "//div[@class='container']/table/tbody/tr/td[2]/div/a[2]").click()
            creds = credentials()

            userId = driver.find_element_by_xpath('//*[@id="loginId"]')
            userId.send_keys(creds[0])

            password = driver.find_element_by_xpath('//*[@id="pin"]')
            password.send_keys(creds[1])

            button = driver.find_element_by_xpath("/html/body/div[4]/table/tbody/tr/td[2]/div/form/div[3]/input")
            button.click()

            leaseLink = driver.find_element_by_xpath("/html/body/div[4]/table/tbody/tr/td[1]/div/div[1]/ul[2]/li[3]/a")
            leaseLink.click()
        #except: print("Invalid Username")
def search( leaseIn, county, leaseTp):
        #login()
        sleep(5)
        leaseInput = driver.find_element_by_id('leaseNum')
        leaseInput.clear()
        leaseInput.send_keys(leaseIn)

        contList = Select(driver.find_element_by_id('county'))
        contList.select_by_visible_text(county)

        leaseType = Select(driver.find_element_by_id('leaseType'))
        leaseType.select_by_visible_text(leaseTp)
        sleep(5)

        searchButton = driver.find_element_by_xpath('/html/body/div[4]/table/tbody/tr/td[2]/div/div/form/p[6]/input')
        searchButton.click()


def entry( date, leaseIn, county, leaseTp):
        #try:
            search(leaseIn, county, leaseTp)
            sleep(5)
            someDict = {'11' : '',
                        '03' : '',
                        '05' : '',
                        'other' : ''}
            table_id = driver.find_element_by_xpath('/html/body/div[4]/table/tbody/tr/td[2]/div/table')
            rows = table_id.find_elements_by_tag_name("tr") # get all of the rows in the table
            #print(rows.text)
            for k in range(len(rows)):
                sleep(2)
                tbl_id = driver.find_element_by_tag_name('table')
                rws = tbl_id.find_elements_by_tag_name("tr") # get all of the rows in the table
                row = rws[k].find_elements_by_tag_name("td")
                if not len(row)==0:
                    try:
                        if row[-2].text != 'No':
                            href = row[-2].find_element_by_tag_name('a')
                            href.click()
                            window_before = driver.window_handles[0]
                            window_before_title = driver.title
                            #print(window_before_title)
                            sleep(4)
                            table_id_1 = driver.find_element_by_tag_name("table")
                            rows_1 = table_id_1.find_elements_by_tag_name("tr")
                            for i in rows_1:
                                    someList = []
                                    i = i.find_elements_by_tag_name("td")
                                    if not len(i) == 0:
                                        if i[3].text in['11', '03', '05']:
                                            key = i[3].text
                                            someList.append('Y')
                                            if len(i[7].text) != 0:
                                                someList.append(i[7].text)
                                            if i[3].text == '11':
                                                i[3].find_element_by_tag_name('a').click()
                                                window_after = driver.window_handles[1]
                                                driver.switch_to.window(window_after)
                                                window_after_title = driver.title
                                                print(window_after_title)
                                                if window_before_title != window_after_title:
                                                   # print("Everything is good")
                                                    driver.maximize_window()
                                                    sleep(2)
                                                    table_id_2 = driver.find_element_by_tag_name("table")
                                                    rows_2 = table_id_2.find_elements_by_tag_name('tr')
                                                    for j in rows_2:
                                                        j = j.find_elements_by_tag_name('td')
                                                        if len(j) != 0:
                                                            try:
                                                                if int(j[0].text) == date:
                                                                    someList.append(str(j[3].text))
                                                            except: pass
                                                driver.close()
                                                driver.switch_to.window(window_before)
                                            someDict[key] = someList
                                        else:
                                            someDict['other'] = i[3].text
                            driver.execute_script("history.back();")
                    except: pass
            return someDict
       # except: print("nothing found")



def loading_df(dateEdit, fileName):
        with open('count.txt') as f:
            count = f.read()
        count = int(count)
        count = 0
        new_fileName = fileName.split('.')
        if len(new_fileName) > 2:
            new_fileName = new_fileName[0] +'.'+ new_fileName[1] + ' (Updated).xlsx'
        else:
            new_fileName = new_fileName[0] + ' (Updated).xlsx'
        df = pd.read_csv(fileName, sep=',', converters = {'RRC Lease#' : str, 'County Code' : str, 'Type 3 [Y/N]' : str, 'Other Exemption' : str})
    # try:
        login()
        for i in range(len(df)):
            code = str(df['County Code'][i])
            if len(code) == 2:
                    code = str('0' + code)
            elif len(code) == 1:
                    code = str('00' + code)
            county = str(df['County Name'][i]).upper() + ' - '+ code
            date = dateEdit
            leaseIn = str(df['Lease # RRC Format'][i])
            if len(leaseIn) == 4:
                leaseIn = '00' + leaseIn
            elif len(leaseIn) == 5:
                leaseIn = '0' + leaseIn
            leaseTp = str(df['Lease Type'][i]).title()
            obtained_dict = entry(date, leaseIn, county, leaseTp)
            print(obtained_dict)
            if obtained_dict['11'] != '':
                df.loc[i, 'Type 11 [Y/N]'] = obtained_dict['11'][0]
                try:
                    if leaseTp == 'Oil':
                        df.loc[i, 'Eligibility for Current Month [Y/N]'] = 'Oil Lease'
                    else:
                        df.loc[i, 'Eligibility for Current Month [Y/N]'] = obtained_dict['11'][1]
                except:
                    df.loc[i, 'Eligibility for Current Month [Y/N]'] = 'Input Date Not Found'
            if obtained_dict['03'] != '':
                df.loc[i, 'Type 3 [Y/N]'] = obtained_dict['03'][0]
                try:
                    df.loc[i, 'Expiration.1'] = obtained_dict['03'][1]
                except: pass
            if obtained_dict['05'] != '':
                df.loc[i, 'Type 5 [Y/N]'] = obtained_dict['05'][0]
                try:
                    df.loc[i, 'Expiration.2'] = obtained_dict['05'][1]
                except: pass
            if obtained_dict['other'] != 'NG':
                df.loc[i, 'Other Exemption'] = obtained_dict['other']
            count += 1
        df.to_excel(new_fileName, index=False)
        driver.close()
    # except:
    #     if '(Incomplete)' not in fileName:
    #         unComFile = fileName.split('.')
    #         if len(unComFile) > 2:
    #             unComFile = unComFile[0] + unComFile[1] + '(Incomplete).csv'
    #         else:
    #             unComFile = unComFile[0] +'(Incomplete).csv'
    #         df.to_csv(unComFile, sep=',', index=False)
    #     else:
    #         df.to_csv(fileName, sep=',', index=False)
    #     with open('count.txt', 'w') as f:
    #         count = str(count)
    #         f.write(count)

def resume_df(dateEdit, fileName):
    with open('count.txt') as f:
        count = f.read()
    count = int(count)
    new_fileName = fileName.split('.')
    if len(new_fileName) > 2:
        new_fileName = new_fileName[0] + new_fileName[1] + ' (Updated).xlsx'
    else:
        new_fileName = new_fileName[0] + ' (Updated).xlsx'
    df = pd.read_csv(fileName, sep=',', converters = {'RRC Lease#' : str, 'County Code' : str, 'Type 3 [Y/N]' : str, 'Other Exemption' : str})
    try:
        login()
        for i in range(len(df)):
            if i >= count:
                code = str(df['County Code'][i])
                if len(code) == 2:
                        code = str('0' + code)
                elif len(code) == 1:
                        code = str('00' + code)
                county = str(df['County Name'][i]).upper() + ' - '+ code
                date = dateEdit
                leaseIn = str(df['Lease # RRC Format'][i])
                if len(leaseIn) == 4:
                    leaseIn = '00' + leaseIn
                elif len(leaseIn) == 5:
                    leaseIn = '0' + leaseIn
                leaseTp = str(df['Lease Type'][i]).title()
                obtained_dict = entry(date, leaseIn, county, leaseTp)
                print(obtained_dict)
                if obtained_dict['11'] != '':
                    df.loc[i, 'Type 11 [Y/N]'] = obtained_dict['11'][0]
                    try:
                        df.loc[i, 'Eligibility for Current Month [Y/N]'] = obtained_dict['11'][1]
                    except: pass
                if obtained_dict['03'] != '':
                    df.loc[i, 'Type 3 [Y/N]'] = obtained_dict['03'][0]
                    try:
                        df.loc[i, 'Expiration.1'] = obtained_dict['03'][1]
                    except: pass
                if obtained_dict['05'] != '':
                    df.loc[i, 'Type 5 [Y/N]'] = obtained_dict['05'][0]
                    try:
                        df.loc[i, 'Expiration.2'] = obtained_dict['05'][1]
                    except: pass
                if obtained_dict['other'] != 'NG':
                    df.loc[i, 'Other Exemption'] = obtained_dict['other']
                count += 1
        df.to_excel(new_fileName, index=False)
        driver.close()
    except:
        if '(Incomplete)' not in fileName:
            unComFile = fileName.split('.')
            if len(unComFile) > 2:
                unComFile = unComFile[0] + unComFile[1] + '(Incomplete).csv'
            else:
                unComFile = unComFile[0] + '(Incomplete).csv'
            df.to_csv(unComFile, sep=',', index=False)
        else:
            df.to_csv(fileName, sep=',', index=False)
        with open('count.txt', 'w') as f:
            count = str(count)
            f.write(count)
