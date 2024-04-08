# Importing libraries
import os
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm


# Say hello
print(
    '\033[38;5;212m '
    '    ██╗ ██╗   ██╗ ████████╗ ███████╗ ██╗   ██╗\n'
    '     ██║ ██║   ██║ ╚══██╔══╝ ██╔════╝ ██║   ██║\n'
    '     ██║ ██║   ██║    ██║    ███████╗ ██║   ██║\n'
    '██   ██║ ██║   ██║    ██║    ╚════██║ ██║   ██║\n'
    '╚█████╔╝ ╚██████╔╝    ██║    ███████║ ╚██████╔╝\n'
    ' ╚════╝   ╚═════╝     ╚═╝    ╚══════╝  ╚═════╝\n'
    ' █████╗  ███╗   ██╗ ██╗ ███╗   ███╗ ███████╗\n'
    '██╔══██╗ ████╗  ██║ ██║ ████╗ ████║ ██╔════╝\n'
    '███████║ ██╔██╗ ██║ ██║ ██╔████╔██║ █████╗\n'
    '██╔══██║ ██║╚██╗██║ ██║ ██║╚██╔╝██║ ██╔══╝\n'
    '██║  ██║ ██║ ╚████║ ██║ ██║ ╚═╝ ██║ ███████╗\n'
    '╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝     ╚═╝ ╚══════╝\n'
    '██████╗   ██████╗  ██╗    ██╗ ███╗   ██╗  ██████╗  ██╗       █████╗   ██████╗  ██████╗  ███████╗ ██████╗\n'
    '██╔══██╗ ██╔═══██╗ ██║    ██║ ████╗  ██║ ██╔═══██╗ ██║      ██╔══██╗ ██╔═══██╗ ██╔══██╗ ██╔════╝ ██╔══██╗\n'
    '██║  ██║ ██║   ██║ ██║ █╗ ██║ ██╔██╗ ██║ ██║   ██║ ██║      ███████║ ██║   ██║ ██║  ██║ █████╗   ██████╔╝\n'
    '██║  ██║ ██║   ██║ ██║███╗██║ ██║╚██╗██║ ██║   ██║ ██║      ██╔══██║ ██║   ██║ ██║  ██║ ██╔══╝   ██╔══██╗\n'
    '██████╔╝ ╚██████╔╝ ╚███╔███╔╝ ██║ ╚████║ ╚██████╔╝ ███████╗ ██║  ██║ ╚██████╔╝ ██████╔╝ ███████╗ ██║  ██║\n'
    '╚═════╝   ╚═════╝   ╚══╝╚══╝  ╚═╝  ╚═══╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═╝\033[0m'
)

# Anime name
find_name = input('ВВЕДИТЕ НАЗВАНИЕ АНИМЕ: ')

# Anime quality
quality = input('РАЗРЕШЕНИЕ: ')

# Anime season
season = input('СЕЗОН: ')

# Anime episodes
from_episode = int(input('С КАКОЙ СЕРИИ: '))
to_episode = int(input('ПО КАКУЮ СЕРИЮ: '))

# Create Fake User Agent
ua = UserAgent().chrome

# Searching start
start_time = time.time()

if quality != '1080':
    if quality != '720':
        if quality != '480':
            if quality != '360':
                print('НЕПРАВИЛЬНОЕ РАЗРЕШЕНИЕ')
                quality = input('РАЗРЕШЕНИЕ: ')

def find_and_write(name, season, episode_number, ua):
    link = f"https://jut.su{name}/season-{season}/episode-{episode_number}.html"
    response = requests.get(link, headers={'User-Agent': ua})

    if response.status_code == 404:
        return 'no'

    # Getting url to episode
    soup = BeautifulSoup(response.text, 'lxml')
    src = soup.find('source', label=f'{quality}p')

    try:
        src = src.get('src')

        response = requests.get(src, headers={'User-Agent': ua})

        # Writing to folder
        with open(f'{name.replace("/", "").capitalize()} - {season}сезон/{episode_number} эпизод.mp4', 'wb') as file:
            file.write(response.content)

    except AttributeError:
        print('НЕЛЬЗЯ НА ТЕРРИТОРИИ РФ')
        return 'no'


for page in range(1, 100):
    page_number = page
    url = f"https://jut.su/anime/page-{page_number}"
    response = requests.get(url, headers={'User-Agent': ua})

    soup = BeautifulSoup(response.text, 'lxml')
    names_on_page = soup.find_all('div', class_='aaname')

    # Page checking
    if not names_on_page:
        break

    else:
        for name_on_page in names_on_page:
            if find_name.lower().strip() == name_on_page.text.lower().strip():
                a_tag = name_on_page.find_parent('a')
                name = a_tag.get('href')
                print(f'НАЙДЕНО: {name.replace("/", "").capitalize()}')
                break

        if 'name' in locals():
            # Create folder
            if os.path.exists(f'{name.replace("/", "").capitalize()} - {season}сезон'):
                pass
            else:
                os.mkdir(
                    f'{name.replace("/", "").capitalize()} - {season}сезон')

            print('\033[38;5;212m'
                  '███████╗ ████████╗  █████╗  ██████╗  ████████╗\n'
                  '██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔══██╗ ╚══██╔══╝\n'
                  '███████╗    ██║    ███████║ ██████╔╝    ██║\n'
                  '╚════██║    ██║    ██╔══██║ ██╔══██╗    ██║\n'
                  '███████║    ██║    ██║  ██║ ██║  ██║    ██║\n'
                  '╚══════╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═╝    ╚═╝\033[0m')

            # Some episodes
            if from_episode != to_episode:
                for episode in tqdm(range(from_episode, to_episode + 1), desc='СЕРИИ'):
                    episode_number = episode
                    a = find_and_write(name, season, episode_number, ua)
                    if a == 'no':
                        break
                    else:
                        pass

            # One episode
            else:
                print('СКАЧИВАТЕСЯ...')
                episode_number = from_episode
                find_and_write(name, season, episode_number, ua)

            # Searching end
            end_time = time.time()
            execution_time = end_time - start_time

            hours = int(execution_time // 3600)
            minutes = int((execution_time % 3600) // 60)
            seconds = int(execution_time % 60)

            print(' \033[38;5;212m'
                  '██████╗  ██████╗  ███╗   ███╗ ██████╗  ██╗      ███████╗ ████████╗ ███████╗\n'
                  '██╔════╝ ██╔═══██╗ ████╗ ████║ ██╔══██╗ ██║      ██╔════╝ ╚══██╔══╝ ██╔════╝\n'
                  '██║      ██║   ██║ ██╔████╔██║ ██████╔╝ ██║      █████╗      ██║    █████╗\n'
                  '██║      ██║   ██║ ██║╚██╔╝██║ ██╔═══╝  ██║      ██╔══╝      ██║    ██╔══╝\n'
                  '╚██████╗ ╚██████╔╝ ██║ ╚═╝ ██║ ██║      ███████╗ ███████╗    ██║    ███████╗\n'
                  ' ╚═════╝  ╚═════╝  ╚═╝     ╚═╝ ╚═╝      ╚══════╝ ╚══════╝    ╚═╝    ╚══════╝\033[0m')

            print(
                f"ЭТО ЗАНЯЛО:\n--- {hours} ЧАСОВ {minutes} МИНУТ {seconds} СЕКУНД ---")
            break

if 'name' not in locals():
    print('ЧТО-ТО НЕ ТАК')
