import os
import json
import glob
import shutil
from colorama import init

init()

class Quiz:
    
    """
    Класс осуществляет поиск по указанному в запросе пути файлов `*.quiz`, заносит путь к файлам в список
        `self.quiz_list`, осуществляет просмотр сформированного списка путей.
    """
    
    def __init__(self, path):
        self.path = self.check_path(path)
        self.quiz_list = self.find_file()
    
    # __________ Функция проверки на существование, указанного пользователем, пути __________ #
    
        """
        Функция осуществляет проверку на существование, указанногопользователем, пути в файловой системе и того,
        что существующий путь, является директорией. Если, проверка не пройдена, то выведет сообщение в консоль об ошибке.
        """
        
    def check_path(self, p):
        if os.path.exists(p):
            if os.path.isdir(p):
                return p
            else:
                print('\033[31m' + "Указанный путь не является директорией:", p, '\033[39m')
        else:
            print('\n\033[31m' + "Такой файл или директория не существует:", p, '\033[39m')
        return 'Error'

    # __________ Функция выводит переменную self.path __________ #
    
    def get_path(self):
        return self.path

    # __________ Функция вывода в консоль пронумерованного списка найденных файлов __________ #

    def get_list(self):
        for n, elem in enumerate(self.quiz_list):
            print('\033[32m', n,'\033[36m', elem ,'\033[39m')

    # __________ Функция поиска файлов __________ #
    
        """
        Функция осуществляет рекурсивный поиск файлов `*.quiz` в указанной директории `self.path`, согласно выражению
        `'\**\*Тест\quiz\quiz[0-9].quiz'`, используя функцию glob одноимённого модуля.
        Если, в переменной  `self.path` значение "Error", то список заполняться не будет и `self.quiz_list` будет пуст.
        Если файл обнаружен, то добавляем в список `lst`, который в конструкторе будет присвоен списку `self.quiz_list`.
        """
    
    def find_file(self):
        lst = []
        if self.path != "Error":
            for elem in sorted(glob.glob(self.path + '/**/0_Тест/quiz/quiz[0-9].quiz', recursive=True)):
                lst.append(elem)
        return lst


def main():
    
    original_path = input("\nВведите начальный путь: ")     # Запрос пути где будет производиться поиск файла *.quiz
    copy_path = input("\nВведите конечный путь: ")      # Запрос пути куда будет скопирован файл *.quiz
    number_quarter = input("\nВведите номер квартала: ")       # Запрос номера квартала
    
    # __________ Путь до файла db.json, в котором хранится база __________ #
    
    # DB_DATA = "/home/itkachuk/my_project/File_Manipulator/data/db.json"         # Unix
    DB_DATA = "C:/Users/Ivan/my_project-master/File_Manipulator/data/db.json"   # Windows
        
    # __________ Функция загрузки месяцев указанного квартала из JSON файла __________ #
    
    def load_quarter():
        with open(DB_DATA, "r", encoding="utf-8") as quarter:
            data = json.load(quarter)
            return data[f'quarter {number_quarter}']

    # __________ Функция загрузки должностей из JSON файла __________ #
    
    def load_wagon_service_positions():
        with open(DB_DATA, "r", encoding="utf-8") as wagon_service_positions:
            data = json.load(wagon_service_positions)
            return data['wagon service positions']

    # __________ Функция копирования файла __________ #

    def copy_quiz():        
        for elem in q.quiz_list:
            sp = elem.split("/")    # для Unix
            # sp = elem.replace("\\", "/").split("/")     # для Windows
            topic_number = sp[-4]
            file = sp[-1]
            copy_file = file[:-5] + f"_{topic_number}" + file[-5:]
            
            SW_COPY = f"{copy_path}/Контрольные за {number_quarter}кв 2022/{sp[-5]}/kontrol04"
            
            if os.path.exists(SW_COPY) == False:
                os.makedirs(SW_COPY)
            
            if os.path.exists(f"{SW_COPY}/{copy_file}"):
                print(f"Файл {copy_file} существует в конечной папке!")
            else:
                shutil.copy2(elem, f"{SW_COPY}/{copy_file}")
                print(f"Файл {copy_file} скопирован!")
    
    month_list = load_quarter()        
    position_list = load_wagon_service_positions()
    
    for month in month_list:
        for position in position_list:
            SW_PATH = f"{original_path}/{month}/{position}"
            q = Quiz(SW_PATH)
            print("\nВывод рабочей директории:", q.get_path(), "\n")
            copy_quiz()
                   

if __name__ == '__main__':
    main()
    
# /home/itkachuk/Share/Техническая учёба/В/_2022    # Unix
# //192.168.103.156/9005/Техническая учёба/В/_2022  # Windows