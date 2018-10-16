import requests
import json
from datetime import datetime



class OWStats():
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {'stats': [], 'heroes': []}
        self.previous_data = {'stats': [], 'heroes': []}
        # проверка файла с датой последнего обновления
        try:
            self.lats_update_time = open('text_files/last_update' + self.user_id + '.txt', 'r').read()
            if self.lats_update_time == '':
                self.lats_update_time = 0
        except:
            self.lats_update_time = 0
        # при запуске программа открывает файлы и читает их
        try:
            profile_file_stats = open('profiles/' + self.user_id + '_stats.txt').read()
            json_data = json.loads(profile_file_stats)
            self.data['stats'] = json_data
        except FileNotFoundError:
            print('Данных нет, нужно обновить')
        try:
            profile_file_stats = open('profiles/' + self.user_id + '_previous_stats.txt').read()
            json_data = json.loads(profile_file_stats)
            self.previous_data['stats'] = json_data
        except FileNotFoundError:
            print('Старых данных нет')
        try:
            profile_file_heroes = open('profiles/' + self.user_id + '_heroes.txt').read()
            json_data = json.loads(profile_file_heroes)
            self.data['heroes'] = json_data
        except FileNotFoundError:
            print('Данных нет, нужно обновить')
        try:
            profile_file_heroes = open('profiles/' + self.user_id + '_previous_heroes.txt').read()
            json_data = json.loads(profile_file_heroes)
            self.previous_data['heroes'] = json_data
        except FileNotFoundError:
            print('Старых данных нет')

        self.get_request()

    def get_request(self):
        # проверка последнего обновления
        if int(datetime.timestamp(datetime.now())) - int(self.lats_update_time) > 300:
            # записываем дату последнего обновления информации
            with open('text_files/last_update' + self.user_id + '.txt', 'w') as file_update:
                file_update.write(str(int(datetime.timestamp(datetime.now()))))
                self.lats_update_time = int(datetime.timestamp(datetime.now()))
            # запрос для stats
            url = 'https://owapi.net/api/v3/u/' + (self.user_id) + '/stats'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            try:
                r = requests.get(url, headers=headers)
            except :
                if not self.data['stats']:
                    return None
                else:
                    return self.data

            response_text = str(r.text)
            json_data = json.loads(response_text)

            if not self.data['stats'] or not self.previous_data['stats']:
                self.data['stats'] = json_data
                self.previous_data['stats'] = json_data
                with open('profiles/' + self.user_id + '_stats.txt', 'w') as profile:
                    profile.write(response_text)
                with open('profiles/' + self.user_id + '_previous_stats.txt', 'w') as profile:
                    profile.write(response_text)
            else:
                changed_data = self.data['stats']['eu']['stats']['competitive']['game_stats']['games_played'] != json_data['eu']['stats']['competitive']['game_stats']['games_played']
                if changed_data:
                    old_stats = open('profiles/' + self.user_id + '_stats.txt').read()
                    with open('profiles/' + self.user_id + '_previous_stats.txt', 'w') as profile:
                        profile.write(old_stats)
                    with open('profiles/' + self.user_id + '_stats.txt', 'w') as profile:
                        profile.write(response_text)
                    self.previous_data['stats'] = self.data['stats']
                    self.data['stats'] = json.loads(response_text)


            # запрос для heroes
            url = 'https://owapi.net/api/v3/u/' + (self.user_id) + '/heroes'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            try:
                r = requests.get(url, headers=headers)
            except:
                if not self.data['heroes']:
                    return 123
                else:
                    return self.data

            response_text = str(r.text)
            json_data = json.loads(response_text)
            if not self.data['heroes'] or not self.previous_data['heroes']:
                self.data['heroes'] = json_data
                self.previous_data['heroes'] = json_data
                with open('profiles/' + self.user_id + '_heroes.txt', 'w') as profile:
                    profile.write(response_text)
                with open('profiles/' + self.user_id + '_previous_heroes.txt', 'w') as profile:
                    profile.write(response_text)
            else:
                if changed_data:
                    old_stats = open('profiles/' + self.user_id + '_heroes.txt').read()
                    with open('profiles/' + self.user_id + '_previous_heroes.txt', 'w') as profile:
                        profile.write(old_stats)
                    with open('profiles/' + self.user_id + '_heroes.txt', 'w') as profile:
                        profile.write(response_text)
                    self.previous_data['heroes'] = self.data['heroes']
                    self.data['heroes'] = json.loads(response_text)
            return self.data
        else:
            return self.data

    def get_stats(self):
        return self.get_request()['stats']

    def get_heroes(self):
        return self.get_request()['heroes']

    def get_previous_stats(self):
        return self.previous_data['stats']

    def get_previous_heroes(self):
        return self.previous_data['heroes']

    # получение текущего ранга и запись в файл
    def get_current_rank(self):
        current_rank = self.get_stats()['eu']['stats']['competitive']['overall_stats']['comprank']
        #записывает в файл текущий ранк
        with open('text_files/' + self.user_id + '_rank.txt', 'a') as file_rank:
            file_rank.write(str(current_rank) + '\n')
        with open('text_files/' + self.user_id + '_rank.txt', 'r') as file_rank:
            file_rank_text = file_rank.read()
            parts = file_rank_text.split('\n')
            # чистка строк если больше 7
            if len(parts) > 7:
                del parts[0]
                with open('text_files/' + self.user_id + '_rank.txt', 'w') as file_rank_new:
                    file_rank_new.write('\n'.join(parts))
        return current_rank
    # получение текущего уровня и запись в файл
    def get_current_level(self):
        try:
            user_level = self.get_stats()['eu']['stats']['competitive']['overall_stats']['prestige']*100 + self.get_stats()['eu']['stats']['competitive']['overall_stats']['level']
            with open('text_files/' + self.user_id + '_level.txt', 'a') as file_level:
                file_level.write(str(user_level) + '\n')
            with open('text_files/' + self.user_id + '_level.txt', 'r') as file_level:
                file_level_text = file_level.read()
                parts = file_level_text.split('\n')
                # чистка строк если больше 7
                if len(parts) > 7:
                    del parts[0]
                    with open('text_files/' + self.user_id + '_level.txt', 'w') as file_level_new:
                        file_level_new.write('\n'.join(parts))
            return user_level
        except:
            user_level_err = 'No info'
            return user_level_err
    # уровень репутации
    def get_current_reputation(self):
        user_reputation = self.get_stats()['eu']['stats']['competitive']['overall_stats']['endorsement_level']
        return user_reputation

    # вывод последних изменений ранговых поинтов
    def get_change_rank(self):
        return self.get_stats()['eu']['stats']['competitive']['overall_stats']['comprank'] - self.get_previous_stats()['eu']['stats']['competitive']['overall_stats']['comprank']


    def get_change_games_played(self):
        match_stats = {'wins': 0, 'loses': 0, 'tied': 0}
        match_stats['wins'] = int(self.get_stats()['eu']['stats']['competitive']['game_stats']['games_won'] - self.get_previous_stats()['eu']['stats']['competitive']['game_stats']['games_won'])
        match_stats['loses'] = int(self.get_stats()['eu']['stats']['competitive']['game_stats']['games_lost'] - self.get_previous_stats()['eu']['stats']['competitive']['game_stats']['games_lost'])
        match_stats['tied'] = int(self.get_stats()['eu']['stats']['competitive']['game_stats']['games_tied'] - self.get_previous_stats()['eu']['stats']['competitive']['game_stats']['games_tied'])
        return match_stats





    def get_hero_stats(self, dps_hero_name):
        information_hero = self.get_heroes()['eu']['heroes']['stats']['competitive'][dps_hero_name]
        return information_hero

    def get_matches_stats(self):
        matches_stats = self.get_stats()['eu']['stats']['competitive']['game_stats']
        return matches_stats





# советы типа кого лучше тренить и на ком сливаться
# примерный ранк на героях
# вкладки с несколькими аккаунтами
# сохранять настройки
# проверка на запросы данных к апи код ответа 200