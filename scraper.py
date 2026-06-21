from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import sys

def scraper(job_title):
    print(f"Starting scraper for: {job_title}")
    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://www.behance.net/joblist?tracking_source=nav20"
    driver.get(url)
    time.sleep(3) 

    scroll_limit = 20
    scroll_count = 0
    job_found = False
    data = []
    specific_job_data = []

    while scroll_count < scroll_limit:
        job_cards = driver.find_elements(By.CLASS_NAME, "JobCard-jobCard-mzZ")
        
        for index, card in enumerate(job_cards):
            try:
                company = card.find_element(By.CLASS_NAME, "JobCard-company-GQS").text
                title = card.find_element(By.CLASS_NAME, "JobCard-jobTitle-LS4").text
                description = card.find_element(By.CLASS_NAME, "JobCard-jobDescription-SYp").text
                time_posted = card.find_element(By.CLASS_NAME, "JobCard-time-Cvz").text
                location = card.find_element(By.CLASS_NAME, "JobCard-jobLocation-sjd").text
                image_element = card.find_element(By.CLASS_NAME, 'JobLogo-logoButton-aes').find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src')
                
                data.append([company, title, description, time_posted, location, image_url])
                
                if title.lower() == job_title.lower() and not job_found:
                    job_found = True
                    specific_job_data.append([company, title, description, time_posted, location, image_url])
            except Exception:
                continue
                
        if job_found:
            break

        driver.execute_script("window.scrollBy(0, 1000);")
        scroll_count += 1
        time.sleep(2)

    with open("jobs.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Job Title", "Description", "Time Posted", "Location", "Image URL"])
        writer.writerows(data)

    if specific_job_data:
        with open("card.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Company", "Job Title", "Description", "Time Posted", "Location", "Image URL"])
            writer.writerows(specific_job_data)

    driver.quit()

if __name__ == "__main__":
    # Get the job title from command line arguments
    target = sys.argv[1] if len(sys.argv) > 1 else "UI/UX Designer"
    scraper(target)