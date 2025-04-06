# Ozon Reviews Parser

## Description

This script is designed for automatically collecting reviews from products on the Ozon website. The program uses Selenium to interact with the web page and parse reviews.

## Features
- The code uses predefined classes to extract review data, so it may become outdated.
- Authorization via cookies.
- Manual login option if cookies are missing.
- Collects reviews by scrolling the page to the end.
- Saves data in Excel format.
- Supports headless mode for browserless operation.

## Keeping Up-to-Date
Go to the config and update the class names to the current ones.

## Requirements

- Installed Google Chrome.
- Python 3.9+
- Libraries:
  - pandas
  - selenium
  - webdriver_manager
  - openpyxl

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/baldiczxc/Ozon-parser-reviews.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Ozon-parser-reviews
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python parse_reviews.py
   ```
2. Follow the console instructions:
   - Enter the product link to collect reviews from.
   - Specify the output file name (without extension). The program will save the data in `.xlsx` format.
3. If cookies are missing, the program will open a browser for manual login. After successful authorization, cookies will be saved for future use.

## Example

1. When running the program:
   ```
   Enter the product link: https://www.ozon.ru/product/123456/
   Enter the output file name: reviews
   ```
2. After completion, the data will be saved to the file `reviews.xlsx`.

## Notes

- If the program is run for the first time, you need to manually log in to your Ozon account through the opened browser.
- Ensure you have the latest version of Google Chrome installed for proper operation.
- To reset cookies, delete the `cookies.pkl` file in the program folder.

---

# Парсер отзывов с Ozon

## Описание

Этот скрипт предназначен для автоматического сбора отзывов с товаров на сайте Ozon. Программа использует Selenium для взаимодействия с веб-страницей и парсинга отзывов.

## Особенности
- В коде прописанно что данные о отзыве он берет по классам, так что версия может быть не актуальной.
- Авторизация через cookies.
- Возможность ручного входа в аккаунт, если cookies отсутствуют.
- Сбор отзывов с прокруткой страницы до конца.
- Сохранение данных в формате Excel.
- Поддержка headless-режима для работы без интерфейса браузера.

## Подтержка актуальности
Зайдите в конфиг и поменяйте название классов на актуальный

## Требования

- Установленный Google Chrome.
- Python 3.9+
- Библиотеки:
  - pandas
  - selenium
  - webdriver_manager
  - openpyxl

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/baldiczxc/Ozon-parser-reviews.git
   ```
2. Перейдите в папку проекта:
   ```bash
   cd Ozon-parser-reviews
   ```
3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

1. Запустите скрипт:
   ```bash
   python parse_reviews.py
   ```
2. Следуйте инструкциям в консоли:
   - Введите ссылку на товар, с которого нужно собрать отзывы.
   - Укажите имя выходного файла (без расширения). Программа сохранит данные в формате `.xlsx`.
3. Если cookies отсутствуют, программа откроет браузер для ручного входа. После успешной авторизации cookies будут сохранены для последующего использования.

## Пример работы

1. При запуске программы:
   ```
   Введите ссылку на товар: https://www.ozon.ru/product/123456/
   Введите имя выходного файла: отзывы
   ```
2. После завершения работы данные будут сохранены в файл `отзывы.xlsx`.

## Примечания

- Если программа запускается впервые, необходимо вручную войти в аккаунт Ozon через открывшийся браузер.
- Для корректной работы убедитесь, что у вас установлен Google Chrome последней версии.
- Если вы хотите сбросить cookies, удалите файл `cookies.pkl` в папке с программой.

