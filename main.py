from playwright.sync_api import sync_playwright

import time
from cookies import GOOGLE_COOKIES
import random
import pandas as pd


def scrapeGoogleMaps(input_phrase,language,headless=False):
    with sync_playwright() as p:
        url = 'https://www.google.pl/maps/'
        browser = p.chromium.launch(headless=headless,slow_mo=500)
        context = browser.new_context(locale=language)
        context.add_cookies(GOOGLE_COOKIES)
        page = context.new_page()
        page.goto(url)
        page.fill('xpath=//input[@id="searchboxinput"]',input_phrase)
        page.click('xpath=//button[@id="searchbox-searchbutton"]')
        page.click('xpath=//div[@class="L1xEbb"]')
        run = True
        while(run==True):
            
            

            page.keyboard.press('PageDown')
            time.sleep(random.uniform(1.945,2.534))

            status = page.is_visible('xpath=//span[@class="HlvSq"]')
            if status is True:
                print("End of google search list")
                run = False
        listings = page.locator('xpath=//a[@class="hfpxzc"]').all()
        columns = ['Company name','Rating','Votes','Address','Phone number','Website link']
        df = pd.DataFrame(columns=columns)
        
        for listing in listings:
            listing.click()

            #data
            name = page.locator('//h1[@class="DUwDvf lfPIob"]').inner_text()
            rating = page.locator('//div[@class="F7nice "]/span/span[@aria-hidden="true"]')
            if rating.count()>0:
                rating = page.locator('//div[@class="F7nice "]/span/span[@aria-hidden="true"]').inner_text()
                rating = rating.replace('.',',')
            else:
                rating = None

            votes = page.locator('//div[@class="F7nice "]/span/span/span[@aria-label]')
            if votes.count()>0:
                votes = page.locator('//div[@class="F7nice "]/span/span/span[@aria-label]').inner_text()
                votes = votes.replace(' ','')
                votes = votes.replace('(','')
                votes = votes.replace(')','')
                votes = votes.replace(',','')
            else:
                votes = None


            phone_number = page.locator('//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]/button[contains(@data-item-id,"phone")]/div/div[@class="rogA2c "]/div[@class="Io6YTe fontBodyMedium kR99db "]')
            if phone_number.count()>0:
                phone_number = page.locator('//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]/button[contains(@data-item-id,"phone")]/div/div[@class="rogA2c "]/div[@class="Io6YTe fontBodyMedium kR99db "]').inner_text()
            else:
                phone_number = None
            address = page.locator('//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]/button[@data-item-id="address"]/div/div[@class="rogA2c "]/div[@class="Io6YTe fontBodyMedium kR99db "]').inner_text()
            website = page.locator('//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]/a[@data-item-id="authority"]')
            if website.count() > 0:         
                website = page.locator('//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]/a[@data-item-id="authority"]').get_attribute('href')
            else:
                website = None
            new_row = {'Company name':name,
                       'Rating':rating,
                       'Votes':votes,
                       'Address':address,
                       'Phone number':phone_number,
                       'Website link':website}
            df.loc[len(df)] = new_row 
            time.sleep(random.uniform(1.455,1.987))
        df.to_csv(f'{input_phrase}.csv',index=False)
if __name__ == '__main__':
    # 'en-GB'
    scrapeGoogleMaps('Burger Poznań','en-GB',headless=True)
