from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


from time import sleep
import string
import random
import argparse

def main(args):
    print(args)
    seed = random.randint(0, 1000000)
    if args.seed is not None:
        seed = args.seed
    random.seed(args.seed)
    print(f"seed: {seed}")

    random.seed(seed)
    driver = webdriver.Chrome()
    driver.set_window_size(1400, 900)
    delay = args.delay or 1.5

    def xpath(text):
        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(delay)
        print('xpath', element)
        return element

    def id(text):
        return driver.find_element(By.ID, text)

    def fuzzyid(text):
        return driver.find_element(By.XPATH, f"//*[contains(@id, '{text}')]")

    def randomText(multiplier=1):
        length = random.randint(5, 30*multiplier)
        # characters = string.printable
        characters = string.ascii_letters + string.digits + string.punctuation
        # characters.replace('\t', '')
        return ''.join(random.choice(characters) for _ in range(length))


    try:
        driver.implicitly_wait(10)
        # Login
        def login(username, password):
            driver.get("http://bubblebarter.herokuapp.com/admin")
            username_input = driver.find_element(By.NAME, "username")
            username_input.send_keys(username)
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            driver.find_element(By.XPATH, '//input[@value="Log in"]').click()
            sleep(delay)
            print("LOGGED IN")
        
        def login1():
            login('luke', 'adminslay1')
        
        def login2():
            login('sarah', 'password')
        
        def logout():
            driver.get("http://bubblebarter.herokuapp.com/admin/logout")
            sleep(delay*2)
            print("LOGGED OUT")
        
        # def logoutin(username, password):
        #     driver.get("http://bubblebarter.herokuapp.com/admin")
        #     xpath('LOG OUT')
        #     username_input = driver.find_element(By.NAME, "username")
        #     username_input.send_keys(username)
        #     password_input = driver.find_element(By.NAME, "password")
        #     password_input.send_keys(password)
        #     driver.find_element(By.XPATH, '//input[@value="Log in"]').click()
        #     sleep(delay)
        #     print("LOGGED IN")

        def post_item():
            # # Post item
            driver.get("http://bubblebarter.herokuapp.com/")
            xpath("Post Item").click()
            sleep(delay)
            title = f"selenium-{randomText()}"
            id('title').send_keys(title)
            id('description').send_keys(randomText(5))
            id('wants').send_keys(randomText(5))

            # for _ in range(random.randint(0, 5)):
                # random_by_class("col-md-2 col-4").click()
                # all_buttons = ['art','food','clothing','trasnport','fun','weird','event','ticket','misc','free','room','help']
                # button = random.choice(all_buttons)
                # print(button)
                # sleep(1)
                # xpath(button).click()

            xpath("Post item").click()
            try:
                alert =  WebDriverWait(driver, 5).until(EC.alert_is_present())
                sleep(delay)
                alert.accept()
            except TimeoutException:
                print("Alert not found. Move on...")
            sleep(delay)
            driver.get("http://bubblebarter.herokuapp.com/")

            sleep(delay)
            print("POSTED ITEM")

        # # Search and edit
        def edit_item():
            driver.get("http://bubblebarter.herokuapp.com/")
            sleep(delay)
            xpath("selenium").click()
            xpath("Edit Item").click()

            fuzzyid('item-title').send_keys('selenium-edited-'+randomText())
            sleep(delay)
            # try:
            # xpath('Save changes').click()
            # driver.find_element(By.XPATH, "//input[@type='submit']").click()

            # except UnexpectedAlertPresentException:
            #     alert = driver.switch_to.alert
            #     sleep(delay)
            #     # alert.accept()
            #     alert.dismiss()
            #     xpath('OK').click()
            print('SAVE CHANGES')
            sleep(delay*4)
            print("EDITED ITEM")

            # Search and make offer
        def propose():
            driver.get("http://bubblebarter.herokuapp.com/")
            sleep(delay)
            xpath("selenium").click()
            # button = xpath("Make a Proposal")
            sleep(delay*4)


        def accept():
            driver.get("http://bubblebarter.herokuapp.com/account")
            xpath("Accept Proposal").click()
            sleep(delay)
            # try:
            #     alert =  WebDriverWait(driver, 5).until(EC.alert_is_present())
            #     sleep(delay)
            #     alert.accept()
            # except TimeoutException:
            #     print("Alert not found. Move on...")
            sleep(delay*2)
            print("ACCEPTED PROPOSAL")

        def execute_function(func_name):
            function_map = {
                'login': login1,
                'login2': login2,
                'post': post_item,
                'edit': edit_item,
                'accept': accept,
                'logout': logout,
                'propose': propose,
            }
            func = function_map.get(func_name)
            if func:
                func()
            else:
                print(f"Function '{func_name}' not found")

        if args.functions is None:
            args.functions = ['login', 'post', 'edit', 'logout']

        for func_name in args.functions:
            execute_function(func_name)

        # sleep(delay*3)
        print('done')

    finally:
        driver.quit()

parser = argparse.ArgumentParser(description='Execute a sequence of functions')
parser.add_argument('--functions', metavar='function', type=str, nargs='+', help='a function to execute')
parser.add_argument('--seed', type=int, help='random seed (default: None)')
parser.add_argument('--delay', type=int, help='delay in seconds (default: 1.5)')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
