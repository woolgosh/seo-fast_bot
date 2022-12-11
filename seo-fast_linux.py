from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time, os
import pickle

useragent = UserAgent()
login = 'woolgosh@mail.ru'
password = 'c8fbbc86ab'
options = Options()
options.set_preference('media.volume_scale', '0.0')
# options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("--headless")
driver_service = Service(executable_path='/home/seo-fast/geckodriver')
driver = webdriver.Firefox(service=driver_service, options=options)

def capcha_pictures(): #решаем купчу при входе на сайт
    driver.find_element(By.ID, 'capcha').screenshot('seo-fast/cacha_pic.png')
    time.sleep(2)
    os.startfile(os.getcwd()+r'\seo-fast\cacha_pic.png')
    print(f'{datetime.now().strftime("%H:%M:%S")}', end='')
    number = input('Введи порядковый номер подходящей картинки(если много, то числа через пробел): ')
    number = number.strip()
    if len(number) == '1':
        driver.find_elements(By.CSS_SELECTOR, 'form#capcha label')[int(number) - 1].click()
    else:
        all_numbers = number.split()
        for i in all_numbers:
            driver.find_elements(By.CSS_SELECTOR, 'form#capcha label')[int(i) - 1].click()

def capcha_chisla():
    time.sleep(9)
    if len(driver.find_elements(By.CSS_SELECTOR, 'div#echoall h1')) > 0:
        if driver.find_element(By.CSS_SELECTOR, 'div#echoall h1').text == 'Проверка':
            driver.find_element(By.ID, 'echoall').screenshot('seo-fast/cacha_numbers.png')
            time.sleep(2)
            os.startfile(os.getcwd() + r'\seo-fast\cacha_numbers.png')
            print(f'{datetime.now().strftime("%H:%M:%S")}', end='')
            chisla = input('Введите число с картинки: ')
            driver.find_element(By.ID, 'code').send_keys(chisla)
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, 'div#echoall a.sf_button').click()
            time.sleep(5)

def login_sf():
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(login)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password + Keys.ENTER)
    time.sleep(1)
    capcha_pictures()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'sf_button').click()
    time.sleep(5)
    pickle.dump(driver.get_cookies(), open(f'seofast_coockies', 'wb'))

def play_youtube(): #функция запускае воспроизведение ютуба
    print('Большую красную кнопку вижу')
    try:
        driver.find_element(By.CLASS_NAME, 'ytp-large-play-button').click()
        print(f'{datetime.now().strftime("%H:%M:%S")} Кликаем Play...')
        return True
    except:
        time.sleep(5)
        if len(driver.find_elements(By.CLASS_NAME, 'ytp-large-play-button')) > 0:
            try:
                driver.find_element(By.CLASS_NAME, 'ytp-large-play-button').click()
                print(f'{datetime.now().strftime("%H:%M:%S")} Кликаем Play...')
                return True
            except:
                print(f'{datetime.now().strftime("%H:%M:%S")} Нету кнопки play')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return False

def all_links():
    driver.refresh()
    time.sleep(5)
    capcha_chisla()
    driver.find_element(By.CSS_SELECTOR, 'a[href="/work_youtube?youtube_expensive"]').click()
    time.sleep(10)
    all_youtube = driver.find_elements(By.CSS_SELECTOR, 'tr td td div a.surf_ckick')
    print(len(all_youtube))
    if len(all_youtube) == 0:
        time.sleep(5)
        all_youtube = driver.find_elements(By.CSS_SELECTOR, 'tr td td div a.surf_ckick')


    for i in all_youtube[::-1]:
        # ActionChains.move_to_element(i).perform()
        driver.execute_script('arguments[0].click();', i)
        time.sleep(1)
        driver.get_screenshot_as_file('seo-fast/click_adv.png')
        time.sleep(9)

        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
        else:
            print(f'{datetime.now().strftime("%H:%M:%S")}Не открылось окно: ')
            all_links()
        time.sleep(2)

        if len(driver.find_elements(By.ID, 'tmr')) > 0:
            timer = int(driver.find_element(By.ID, 'tmr').text)
        else:
            time.sleep(10)

            if len(driver.find_elements(By.ID, 'tmr')) > 0:
                timer = int(driver.find_element(By.ID, 'tmr').text)
            else:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

        driver.switch_to.frame('video-start')
        driver.get_screenshot_as_file('seo-fast/before_youtube_click.png')

        if len(driver.find_elements(By.CLASS_NAME, 'ytp-large-play-button')) > 0: #Ищем кнопку Play
            if play_youtube() == False:
                continue
        else:
            time.sleep(5)
            driver.switch_to.frame('video-start')
            if play_youtube() == False:
                continue

        time.sleep(timer + 4)
        driver.switch_to.default_content()
        driver.get_screenshot_as_file('seo-fast/before_sf_button.png')
        if len(driver.find_elements(By.CLASS_NAME, 'sf_button')) > 0:
            driver.find_element(By.CLASS_NAME, 'sf_button').click()
            print(f'{datetime.now().strftime("%H:%M:%S")} Получаем деньги за просмотр...')
        else:
            time.sleep(7)

            if len(driver.find_elements(By.CLASS_NAME, 'sf_button')) > 0:
                driver.find_element(By.CLASS_NAME, 'sf_button').click()
                print(f'{datetime.now().strftime("%H:%M:%S")} Получаем деньги за просмотр...')
            else:
                time.sleep(1)
                print(f'{datetime.now().strftime("%H:%M:%S")} Не вижу кнопки Продолжить, переходим к следующей ссылке')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

        time.sleep(2)
        # input(':7')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

def to_youtube_links():
    time.sleep(8)
    driver.find_element(By.CLASS_NAME, 'fa-youtube').click()
    time.sleep(7)
    capcha_chisla()
    time.sleep(3)
    try:
        driver.find_element(By.CSS_SELECTOR, 'div.popup2 a').click()  # пробуем закрыть модальное окно
    except Exception as ex:
        print('Не ознакомился')
    # input(':3')
    driver.find_element(By.ID, 'sll_m_bl5').screenshot('seo-fast/screen.png')

    all_links()

def start_script():
    try:
        driver.get(url='https://seo-fast.ru/login')
        time.sleep(6)
        login_sf()

        to_youtube_links()

        input('_-_-')
    except Exception as ex:
        print(ex)
        to_youtube_links()
    finally:
        driver.close()
        driver.quit()

start_script()