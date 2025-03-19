import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import logging
import pickle
import os

# Настройка логирования
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

print = logging.info  # Перенаправление print в логирование

print("Скрипт запущен")

# Функция для сохранения cookies
def save_cookies(driver, path="cookies.pkl"):
    print("Сохраняем cookies")
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    print(f"Cookies сохранены в {path}")

# Функция для загрузки cookies
def load_cookies(driver, path="cookies.pkl"):
    if not os.path.exists(path):
        print(f"Файл cookies ({path}) не найден. Сначала выполните авторизацию.")
        return False
    
    print("Загружаем cookies")
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
    
    # Переходим на домен Ozon, чтобы cookies были применимы
    driver.get("https://www.ozon.ru")
    time.sleep(2)
    
    # Добавляем cookies в браузер
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("Cookies успешно загружены")
    return True

# Функция для ручной авторизации и сохранения cookies
def manual_login_and_save_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.ozon.ru/my/auth")  # Страница входа
    
    print("Пожалуйста, войдите в аккаунт вручную в открывшемся окне браузера.")
    input("Нажмите Enter после успешного входа в аккаунт...")  # Ожидание ручного входа
    
    # Проверка успешного входа
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/my/")]'))
        )
        print("Успешный вход обнаружен")
        save_cookies(driver)  # Сохраняем cookies
    except Exception as e:
        print(f"Ошибка при входе: {str(e)}")
    
    driver.quit()
    return True

# Прокрутка страницы до конца
def scroll_to_bottom(driver, step=300, delay=0.2):
    """
    Очень медленная прокрутка страницы до конца.
    :param driver: объект WebDriver
    :param step: количество пикселей для прокрутки за один шаг
    :param delay: задержка между шагами прокрутки в секундах
    """
    start_time = time.time()
    cycle_count = 0  # Счетчик циклов прокрутки

    while True:
        # Прокручиваем страницу на шаг
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(delay)
        cycle_count += 1
        print(f"Прокрутка: цикл {cycle_count}")

        # Получаем текущую позицию прокрутки и высоту страницы
        scroll_position = driver.execute_script("return window.scrollY + window.innerHeight;")
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        # Проверяем, достигли ли конца страницы
        if scroll_position >= scroll_height:
            print("Достигнута нижняя часть страницы.")
            break

# Функция для создания экземпляра браузера
def create_browser(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-webgl")  # Отключение WebGL
    options.add_argument("--disable-gpu")  # Отключение GPU
    options.add_argument("--disable-software-rasterizer")  # Отключение программного растеризатора
    if headless: 
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Основная функция парсинга отзывов
def parse_reviews(urls, output_file="output.xlsx"):
    print("Запускаем Chrome")
    headless = os.path.exists("cookies.pkl")  # Если cookies есть, запускаем в headless-режиме
    driver = create_browser(headless=headless)
    print("Chrome открыт")
    
    # Загружаем cookies, если они есть, иначе выполняем ручную авторизацию
    if not load_cookies(driver, "cookies.pkl"):
        print("Cookies не найдены, требуется ручная авторизация")
        driver.quit()  # Закрываем браузер с интерфейсом
        driver = create_browser(headless=False)  # Открываем браузер с интерфейсом
        manual_login_and_save_cookies()
        driver.quit()  # Закрываем браузер после авторизации
        driver = create_browser(headless=True)  # Перезапускаем браузер в headless-режиме
        load_cookies(driver, "cookies.pkl")
    
    # Проверяем, что авторизация прошла успешно
    driver.get("https://www.ozon.ru/my")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/my/")]'))
        )
        print("Авторизация через cookies подтверждена")
    except Exception as e:
        print(f"Ошибка авторизации через cookies: {str(e)}")
        driver.quit()
        sys.exit(1)
    
    reviews_list = []  # Список для хранения отзывов

    for url in urls:
        try:
            driver.get(url)
            time.sleep(20)
            scroll_to_bottom(driver)  # Прокрутка страницы
            print("Прокрутка страницы завершена.")
            
            # Сбор всех отзывов
            try:
                review_blocks_container = driver.find_element(By.XPATH, '//*[@data-widget="webReviewTabs"]')
                review_blocks = review_blocks_container.find_elements(By.CLASS_NAME, "r9u_32")
                
                if not review_blocks:
                    print("Блоки отзывов не найдены.")
                    continue
                print(f"Найдено блоков отзывов на текущей странице: {len(review_blocks)}")
            except Exception as e:
                print(f"Не удалось найти блоки отзывов: {e}")
                continue
            
            for block in review_blocks:
                try:
                    review_text_element = block.find_elements(By.CLASS_NAME, "y4p_32")
                    date_element = block.find_elements(By.CLASS_NAME, "p3y_32")
                    
                    if not review_text_element or not date_element:
                        continue  # Пропускаем блок, если элементы отсутствуют
                    
                    review_text = review_text_element[0].text.strip()
                    date = date_element[0].text.strip()
                    reviews_list.append({'Дата отзыва': date, 'Текст отзыва': review_text})
                    collected_reviews += 1
                except Exception:
                    continue  # Пропускаем блок при любой ошибке

        except Exception as e:
            print(f"Ошибка при обработке {url}: {str(e)}")
            continue
            
        time.sleep(5)

    driver.quit()
    print("Chrome закрыт")

    # Сохранение результатов в Excel
    if reviews_list:
        df = pd.DataFrame(reviews_list, columns=['Дата отзыва', 'Текст отзыва'])
        df.to_excel(output_file, index=False)
        print(f"Данные экспортированы в файл: {output_file}")
    else:
        print("Нет данных для сохранения.")

# Основная функция
if __name__ == "__main__":
    url = input("Введите ссылку на товар: ").strip()
    if not url:
        print("Ошибка: Ссылка не может быть пустой.")
        sys.exit(1)
    
    output_file_name = input("Введите имя выходного файла: ").strip()
    if not output_file_name:
        print("Ошибка: Имя файла не может быть пустым.")
        sys.exit(1)
    
    output_file = f"{output_file_name}.xlsx"
    print(f"Получена ссылка: {url}")
    parse_reviews([url], output_file=output_file)  # Парсинг и сохранение в Excel