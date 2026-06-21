from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def filter():
    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://www.behance.net/joblist?tracking_source=nav20"
    driver.get(url)

    time.sleep(7)  
    
    try:
        view_all_button = driver.find_element(By.XPATH, "//*[text()='View All Categories']")
        view_all_button.click()
        time.sleep(5)  
    except Exception as e:
        print(f"Error clicking 'View All Categories' button: {e}")

    # To get subcategories of categories, including nested ones
    def get_subcategories(fieldset):
        subcategories = []
        try:
            # Finding the subcategories
            radio_buttons = fieldset.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            for radio_button in radio_buttons:
                # Extract the label text for each subcategory
                label_element = radio_button.find_element(By.XPATH, "..//label")
                label = label_element.text if label_element else "Unnamed Subcategory"
                subcategories.append(label)

                # If the subcategory has its own subcategories, recursing into it
                nested_fieldsets = radio_button.find_elements(By.XPATH, "..//fieldset")
                for nested_fieldset in nested_fieldsets:
                    nested_subcategories = get_subcategories(nested_fieldset)
                    if nested_subcategories:
                        subcategories.append(nested_subcategories)
        except Exception as e:
            print(f"Error getting subcategories: {e}")
        return subcategories

    # Finding all <fieldset> elements containing categories
    category_fieldsets = driver.find_elements(By.CSS_SELECTOR, "fieldset.CategoryFilter-fieldset-o7r")
    print(f"Found {len(category_fieldsets)} category fieldsets.")

    # Initializing a dictionary to store categories and their respective subcategories
    categories = {}

    # Iterating through each category section
    for fieldset in category_fieldsets:
        try:
            # Finding the category name 
            category_name_element = fieldset.find_element(By.CSS_SELECTOR, "legend.CategoryFilter-sectionSubheading-VsL")
            category_name = category_name_element.text if category_name_element else "Unknown Category"
            print(f"Processing category: {category_name}")

            # Getting the subcategories (Recursive for nested ones)
            subcategories = get_subcategories(fieldset)

            # Only adding a category if it has subcategories
            if subcategories:
                categories[category_name] = subcategories
            else:
                print(f"Warning: No subcategories found for {category_name}")
        except Exception as e:
            print(f"Error processing a category: {e}")
            continue

    # Output the scraped categories and subcategories
    print("Scraped Categories and Subcategories:")
    for category, subcategories in categories.items():
        print(f"Category: {category}")
        for subcategory in subcategories:
            if isinstance(subcategory, list):  # Nested subcategories
                print(f"  - Nested Subcategories: {subcategory}")
            else:
                print(f"  - {subcategory}")

    driver.quit()
    
    return categories