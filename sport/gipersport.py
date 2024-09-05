import csv
import json
import os
import bs4
import time
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

count = 1
while count <= 98:
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options) as driver:  # Открываем хром
        driver.get(f"https://samara.gipersport.ru/catalog/kardiotrenazhery/?PAGEN_1={count}")  # Открываем страницу
        time.sleep(5)  # Время на прогрузку страницы
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        heads = soup.find_all('div', {'class': 'product uk-panel'})
        category = soup.find('ul', {'class': 'uk-breadcrumb'}).find_all('li')
        print(category[2].text.strip())
        razdel = (category[2].text.strip())
        print(len(heads))
        for head in heads:
            name = head.find_next('a', {'class': 'product-name sc-name'}).text.strip()
            print(name)
            articul = head.find_next('span', {'class': 'badge sc-badge-article uk-text-muted'}).text.strip()
            print(articul)
            try:
                price = head.find_next('div', {'class': 'product-price'}).text.strip().replace('₽', '')
                print(price)
            except:
                price = 'None'
                print('None')
            try:
                params = head.find_next('table', {'class': 'uk-table uk-table-striped'}).find_all_next('tr')
                all_params = []
                for param in params:
                    terr = param.text.strip()
                    print(terr)
                    all_params.append(terr.replace('\n', '').replace('\t', '').strip())
            except:
                all_params = 'None'
                print('None')
            photo = head.find_next('div', {'class': 'uk-vertical-align-middle'}).find('img', src=True)
            print('https://samara.gipersport.ru' + photo['src'])
            pix = ('https://samara.gipersport.ru' + photo['src'])
            print('\n')

            storage = {'category': razdel, 'name': name, 'articul': articul, 'price': price,
                       'params': '; '.join(all_params), 'photo': pix}
            # fields = ['Category', 'Name', 'Articul', 'Price', 'Params', 'Photo']
            # with open(f'{razdel}.csv', 'a+', encoding='utf-16') as file:
            #     pisar = csv.writer(file, delimiter='$', lineterminator='\r')
            #     pisar.writerow(
            #         [storage['category'], storage['name'], storage['articul'], storage['price'], storage['params'],
            #          storage['photo']])
            # Задаем имя файла
            json_file = f'{razdel}.json'

            # Проверяем, существует ли файл
            if os.path.isfile(json_file):
                # Если файл существует, читаем и обновляем данные
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)  # Загружаем существующие данные
            else:
                data = []  # Если файла нет, создаем новый список

            # Добавляем новый элемент в список данных
            data.append(storage)

            # Записываем обновленный список в JSON файл
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)  # Запись с красивым форматом
    count += 1
    print(count)
