import sys
from visual import *
from main import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import requests
from pathlib import Path
import json

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # пробуем открыть файл с настройками языка программы
        try:
            with open('text_files/settings.txt', 'r') as settings_read:
                settings_read_file = settings_read.read()
                self.settings = json.loads(settings_read_file)
        # если фала нет то ставим дефолт язык английский и создаем файл в котором это указываем
        except:
            self.settings = {"language": "en"}
            with open('text_files/settings.txt', 'w') as settings_write:
                settings_write.write(json.dumps(self.settings))
        self.render_language()
        self.accounts = []
        self.accs_choose = {}
        self.current_account = ''

        # подгрузка списка профилей из файла при запуске программы
        with open('text_files/profiles_list.txt', 'r') as profiles_list_read:
            profiles_list_text = profiles_list_read.read()
            parts = profiles_list_text.split('\n')
            for part in parts:
                if part == '':
                    pass
                else:
                    self.accounts.append(part)


        self.tableAccs_rendering()
        # Здесь прописываем событие нажатия на кнопку
        self.ui.add_profile_button.clicked.connect(self.AddProfile)
        self.ui.update_information_button.clicked.connect(self.UpdateInfo)
        # клик по ячейке таблицы (удаление профиля)
        self.ui.choose_acc_settings_listWidget.itemDoubleClicked.connect(self.AccsRemoveClicked)
        # выбор аккаунта
        self.ui.choose_acc_listWidget.itemClicked.connect(self.ChooseAcc)
        # выбор персонажа для вывода статистики
        self.ui.choose_hero_stats_listWidget.itemClicked.connect(self.render_heroes_tab_stats)
        # выбор языка через нажатие на кнопки
        self.ui.ru_lang_button.clicked.connect(self.set_language)
        self.ui.eng_lang_button.clicked.connect(self.set_language)


    # при нажатии на кнопку Добавить профиль
    def AddProfile(self):
        # проверка введенных данных
        if self.ui.add_profile_nickname_lineEdit.text() == '' or self.ui.add_profile_number_lineEdit.text() == '' or not self.ui.add_profile_number_lineEdit.text().isdecimal():
            self.error_message('Проверьте данные')
        else:
            battle_tag_part1 = self.ui.add_profile_nickname_lineEdit.text()
            battle_tag_part2 = self.ui.add_profile_number_lineEdit.text()
            battle_tag = battle_tag_part1 + '-' + battle_tag_part2
            # добавление профиля в таблицу
            item = Qt.QTableWidgetItem()
            item.setText(battle_tag)
            # проверка на количество профилей
            if len(self.accounts) >= 5:
                self.error_message('Список аккаунтов переполнен')
            else:
                self.accounts.append(battle_tag)
                self.rewriteProfileFile()
                self.tableAccs_rendering()


    def AccsRemoveClicked(self, item):
        reply = QMessageBox.question(self, 'Удаление аккаунта',
                                     "Вы точно хотите удалить этот аккаунт?", QMessageBox.Yes |
                                     QMessageBox.No)
        # при нажатии YES удаляется акк
        if reply == QMessageBox.Yes:
            self.accounts.remove(item.text())
            self.rewriteProfileFile()
            self.tableAccs_rendering()
        else:
            pass

    # сообщение об ошибке с параметром который выводит сообщение
    def error_message(self, type_error):
        QMessageBox.information(self, 'Ошибка', type_error, QMessageBox.Ok)


    # перерисовка таблиц со списком аккаунтов
    def tableAccs_rendering(self):
        # очищаем виджеты
        self.ui.choose_acc_settings_listWidget.clear()
        self.ui.choose_acc_listWidget.clear()

        for index in range(0, len(self.accounts)):
            if len(self.accounts) > 0:
                item = Qt.QListWidgetItem()
                item.setText(self.accounts[index])
                self.ui.choose_acc_settings_listWidget.insertItem(index, item)
                item_accs = Qt.QListWidgetItem()
                item_accs.setText(self.accounts[index])
                self.ui.choose_acc_listWidget.insertItem(index, item_accs)
            else:
                pass


    def rewriteProfileFile(self):
        with open('text_files/profiles_list.txt', 'w') as profiles_list:
            profiles_list.write('\n'.join(self.accounts))


    def ChooseAcc(self, item):
        self.accs_choose[item.text()] = OWStats(item.text())
        btag = item.text().replace('-', '#')
        self.ui.battle_tag_label.setText(btag)
        self.current_account = item.text()
        self.render_profile_tab(self.current_account)
        self.render_statistic_tab(self.current_account)
        self.render_heroes_tab_list(self.current_account)




    def render_profile_tab(self, item):
        current_level = str(self.accs_choose[item].get_current_level())
        current_rank = str(self.accs_choose[item].get_current_rank())
        current_reputation = str(self.accs_choose[item].get_current_reputation())
        time_played = int(self.accs_choose[item].get_matches_stats()['time_played'])
        games_won = int(self.accs_choose[item].get_matches_stats()['games_won'])
        games_lost = int(self.accs_choose[item].get_matches_stats()['games_lost'])
        games_tied = int(self.accs_choose[item].get_matches_stats()['games_tied'])
        total_matches_count = games_lost + games_won
        winrate = (games_won / total_matches_count) * 100

        # кэш данных побед лузов ранка и тд
        color = 'white'
        if self.accs_choose[item].get_change_rank() > 0:
            color = '#77f968'
        elif self.accs_choose[item].get_change_rank() < 0:
            color = 'red'

        self.ui.last_change_rank_label.setStyleSheet('color: ' + color)
        self.ui.last_change_rank_label.setText(str(self.accs_choose[item].get_change_rank()))
        self.ui.change_games_won_label.setText(str(self.accs_choose[item].get_change_games_played()['wins']))
        self.ui.change_games_lost_label.setText(str(self.accs_choose[item].get_change_games_played()['loses']))
        self.ui.change_games_tied_label.setText(str(self.accs_choose[item].get_change_games_played()['tied']))


        # загрузка аватара для профиля
        p = requests.get(self.accs_choose[item].get_stats()['eu']['stats']['competitive']['overall_stats']['avatar'])
        out = open("images/logoacc.png", "wb")
        out.write(p.content)
        out.close()
        pixmap = QPixmap('images/logoacc.png')

        # загрузка аватара лиги рейтинга
        rank_avatar = self.accs_choose[item].get_stats()['eu']['stats']['competitive']['overall_stats']['tier']
        pixmap_rank_avatar = QPixmap('images/' + rank_avatar + '.png')
        self.ui.rank_avatar_label.setPixmap(pixmap_rank_avatar)


        # обновление всей текущей информации
        self.ui.current_games_won_label.setText(str(games_won))
        self.ui.current_games_lost_label.setText(str(games_lost))
        self.ui.current_games_tied_label.setText(str(games_tied))
        self.ui.current_winrate_acc_label.setText(str(round(winrate, 2)) + '%')
        self.ui.current_hours_played_inrank_label.setText(str(time_played))
        self.ui.current_reputation_label.setText(current_reputation)

        self.ui.current_rank_label.setText(current_rank)
        self.ui.current_level_label.setText(current_level)
        self.ui.avatar_label.setPixmap(pixmap)

    # обновление информации при нажатии на кнопку обновить информацию
    def UpdateInfo(self):
        if self.current_account == '':
            pass
        else:
            btag = self.current_account.replace('-', '#')
            self.ui.battle_tag_label.setText(btag)
            self.render_profile_tab(self.current_account)
            self.render_statistic_tab(self.current_account)

    def render_statistic_tab(self, item):
        most_elims_in_match = str(int(self.accs_choose[item].get_matches_stats()['eliminations_most_in_game']))
        self.ui.most_elims_acc_label.setText(str(most_elims_in_match))
        total_elims = str(int(self.accs_choose[item].get_matches_stats()['eliminations']))
        self.ui.total_elims_acc_label.setText(str(total_elims))
        most_final_blows = str(int(self.accs_choose[item].get_matches_stats()['final_blows_most_in_game']))
        self.ui.most_final_blows_acc_label.setText(str(most_final_blows))
        total_final_blows = str(int(self.accs_choose[item].get_matches_stats()['final_blows']))
        self.ui.total_final_blows_acc_label.setText(str(total_final_blows))
        most_obj_elims = str(int(self.accs_choose[item].get_matches_stats()['objective_kills_most_in_game']))
        self.ui.most_obj_elims_acc_label.setText(str(most_obj_elims))
        total_obj_elims = str(int(self.accs_choose[item].get_matches_stats()['objective_kills']))
        self.ui.total_obj_elims_acc_label.setText(str(total_obj_elims))
        most_dmg_in_match = str(int(self.accs_choose[item].get_matches_stats()['hero_damage_done_most_in_game']))
        self.ui.most_heroes_dmg_acc_label.setText(str(most_dmg_in_match))
        total_dmg_done = str(int(self.accs_choose[item].get_matches_stats()['hero_damage_done']))
        self.ui.total_heroes_dmg_acc_label.setText(str(total_dmg_done))
        most_solo_elims_in_match = str(int(self.accs_choose[item].get_matches_stats()['solo_kills_most_in_game']))
        self.ui.most_solo_elims_acc_label.setText(str(most_solo_elims_in_match))
        total_solo_elims = str(int(self.accs_choose[item].get_matches_stats()['solo_kills']))
        self.ui.total_solo_elims_acc_label.setText(str(total_solo_elims))
        most_healing_in_match = str(int(self.accs_choose[item].get_matches_stats()['healing_done_most_in_game']))
        self.ui.most_healing_acc_label.setText(str(most_healing_in_match))
        total_healing_done = str(int(self.accs_choose[item].get_matches_stats()['healing_done']))
        self.ui.total_healing_acc_label.setText(str(total_healing_done))

        # время на объекте
        total_obj_time = self.accs_choose[item].get_matches_stats()['objective_time']
        obj_time_minutes = (total_obj_time - int(total_obj_time)) * 60
        if obj_time_minutes < 10:
            obj_time_minutes = '0' + str(int(obj_time_minutes))
            self.ui.total_obj_time_acc_label.setText(str(int(total_obj_time)) + ':' + obj_time_minutes)
        else:
            self.ui.total_obj_time_acc_label.setText(str(int(total_obj_time)) + ':' + str(int(obj_time_minutes)))

        most_obj_time_in_match = self.accs_choose[item].get_matches_stats()['objective_time_most_in_game']
        record_obj_time_match = most_obj_time_in_match * 60
        record_obj_time_match_mins = int(record_obj_time_match)
        record_obj_time_match_secs = record_obj_time_match - record_obj_time_match_mins
        if record_obj_time_match_secs < 10:
            record_obj_time_match_secs = '0' + str(int(record_obj_time_match_secs))
            self.ui.most_obj_time_acc_label.setText(str(record_obj_time_match_mins) + ':' + record_obj_time_match_secs)
        else:
            self.ui.most_obj_time_acc_label.setText(str(record_obj_time_match_mins) + ':' + str(int(record_obj_time_match_secs)))

        # время в ударе
        total_fire_time = self.accs_choose[item].get_matches_stats()['time_spent_on_fire']
        total_fire_time_hrs = int(total_fire_time)
        total_fire_time_mins = (total_fire_time - total_fire_time_hrs) * 60
        if total_fire_time_mins < 10:
            total_fire_time_mins = '0' + str(int(total_fire_time_mins))
            self.ui.total_fire_time_acc_label.setText(str(total_fire_time_hrs) + ':' + total_fire_time_mins)
        else:
            self.ui.total_fire_time_acc_label.setText(str(total_fire_time_hrs) + ':' + str(int(total_fire_time_mins)))

        most_fire_time = self.accs_choose[item].get_matches_stats()['time_spent_on_fire_most_in_game']
        most_fire_time_all = most_fire_time * 60
        most_fire_time_mins = int(most_fire_time_all)
        most_fire_time_secs = (most_fire_time_all - int(most_fire_time_all)) * 60
        if most_fire_time_secs < 10:
            most_fire_time_secs = '0' + str(int(most_fire_time_secs))
            self.ui.most_fire_time_acc_label.setText(str(most_fire_time_mins) + ':' + most_fire_time_secs)
        else:
            self.ui.most_fire_time_acc_label.setText(str(most_fire_time_mins)+ ':' + str(int(most_fire_time_secs)))


    def render_heroes_tab_list(self, item):
        heroes_list = self.accs_choose[item].get_heroes()['eu']['heroes']['stats']['competitive']
        heroes_list = sorted(heroes_list)
        self.ui.choose_hero_stats_listWidget.clear()
        index = 0
        for hero_name in heroes_list:
            item = Qt.QListWidgetItem()
            item.setText(hero_name.title())
            self.ui.choose_hero_stats_listWidget.insertItem(index, item)
            index += 1


    def render_heroes_tab_stats(self, item):
        hero_statistic = self.accs_choose[self.current_account].get_hero_stats(item.text().lower())
        try:
            games_played = int(hero_statistic['general_stats']['games_won']) + int(hero_statistic['general_stats']['games_lost'])
        except:
            games_played = 0

        elims = round(self.avg_stats_heroes(hero_statistic, 'eliminations', 'games_played'), 2)
        self.ui.avg_elims_hero_label.setText(str(elims))

        obj_elims = round(self.avg_stats_heroes(hero_statistic, 'objective_kills', 'games_played'), 2)
        self.ui.avg_obj_elims_hero_label.setText(str(obj_elims))

        damage_done = int(self.avg_stats_heroes(hero_statistic, 'hero_damage_done', 'games_played'))
        self.ui.avg_damage_done_hero_label.setText(str(damage_done))

        deaths = round(self.avg_stats_heroes(hero_statistic, 'deaths', 'games_played'), 2)
        self.ui.avg_deaths_hero_label.setText(str(deaths))

        healing_done = int(self.avg_stats_heroes(hero_statistic, 'healing_done', 'games_played'))
        self.ui.avg_healing_done_hero_label.setText(str(healing_done))
        try:
            time_played = hero_statistic['general_stats']['time_played']
            self.ui.time_played_hero_label.setText(str(int(time_played)) + ' ч')
        except:
            self.ui.time_played_hero_label.setText('0 ч')
        # винрейт
        try:
            winrate = round((hero_statistic['general_stats']['games_won'] / games_played) * 100, 2)
            self.ui.winrate_hero_label.setText(str(winrate) + '%')
        except:
            self.ui.winrate_hero_label.setText('-')

        final_blows = round(self.avg_stats_heroes(hero_statistic, 'final_blows', 'games_played'), 2)
        self.ui.final_blows_hero_label.setText(str(final_blows))
        # меткость только у некоторых героев
        try:
            accuracy = hero_statistic['general_stats']['weapon_accuracy'] * 100
            self.ui.accuracy_hero_label.setText(str(int(accuracy)) + '%')
        except:
            self.ui.accuracy_hero_label.setText('-')

        # крит меткость
        try:
            accuracy = hero_statistic['general_stats']['critical_hit_accuracy'] * 100
            self.ui.critical_accuracy_hero_label.setText(str(int(accuracy)) + '%')
        except:
            self.ui.critical_accuracy_hero_label.setText('-')

        # хил только у некоторых героев
        try:
            healing_done = int(hero_statistic['general_stats']['healing_done'] / hero_statistic['general_stats']['games_played'])
            self.ui.avg_healing_done_hero_label.setText(str(healing_done))
        except:
            self.ui.avg_healing_done_hero_label.setText('-')

        solo_elims = round(self.avg_stats_heroes(hero_statistic, 'solo_kills', 'games_played'), 2)
        self.ui.avg_solo_elims_hero_label.setText(str(solo_elims))

        # Время на объекте среднее
        try:
            obj_time_all = hero_statistic['general_stats']['objective_time']* 60 / hero_statistic['general_stats']['games_played']
            if hero_statistic['general_stats']['objective_time'] > hero_statistic['general_stats']['time_played']:
                if hero_statistic['general_stats']['objective_time'] < 10:
                    self.ui.avg_obj_time_hero_label.setText('0:0' + str(int(hero_statistic['general_stats']['objective_time'])))
                else:
                    self.ui.avg_obj_time_hero_label.setText('0:' + str(int(hero_statistic['general_stats']['objective_time'])))
            else:
                obj_time_secs = (obj_time_all - int(obj_time_all)) * 60
                if obj_time_secs < 10:
                    self.ui.avg_obj_time_hero_label.setText(str(int(obj_time_all)) + ':0' + str(int(obj_time_secs)))
                else:
                    self.ui.avg_obj_time_hero_label.setText(str(int(obj_time_all)) + ':' + str(int(obj_time_secs)))
        except:
            self.ui.avg_obj_time_hero_label.setText('-')
        # время в ударе в % от времени наигранном на персонаже
        try:
            fire_time = hero_statistic['general_stats']['time_spent_on_fire']
            if fire_time > hero_statistic['general_stats']['time_played']:
                fire_time = fire_time / 3600
            fire_time_percent = round((fire_time / hero_statistic['general_stats']['time_played']) * 100, 2)
            self.ui.avg_fire_time_hero_label.setText(str(fire_time_percent) + '%')
        except:
            self.ui.avg_fire_time_hero_label.setText('-')
        # количество матчей на персонаже побед поражений ничьих
        try:
            self.ui.games_won_hero_label.setText(str(int(hero_statistic['general_stats']['games_won'])))
        except:
            self.ui.games_won_hero_label.setText('0')

        try:
            self.ui.games_lost_hero_label.setText(str(int(hero_statistic['general_stats']['games_lost'])))
        except:
            self.ui.games_lost_hero_label.setText('0')

        try:
            self.ui.games_tied_hero_label.setText(str(int(hero_statistic['general_stats']['games_tied'])))
        except:
            self.ui.games_tied_hero_label.setText('0')

        # вставляем автар героя
        image = Path('heroes_avatars/' + item.text().lower() + '.png')
        if image.is_file():
            pixmap = QPixmap('heroes_avatars/' + item.text().lower() + '.png')
            self.ui.avatar_hero_label.setPixmap(pixmap)
        else:
            pixmap = QPixmap('heroes_avatars/unknownhero.png')
            self.ui.avatar_hero_label.setPixmap(pixmap)


    # на случай если один из параметров равен 0
    def avg_stats_heroes(self, hero_statistic, param1, param2):
        try:
            return hero_statistic['general_stats'][param1] / hero_statistic['general_stats'][param2]
        except:
            return 0


    def set_language(self, button):
        self.settings["language"] = self.sender().text().lower()
        with open('text_files/settings.txt', 'w') as settings_write:
            settings_write.write(json.dumps(self.settings))
        self.render_language()


    def render_language(self):
        with open('text_files/' + self.settings["language"] + '_settings.txt', 'r') as lang_read:
            settings_read_file = lang_read.read()
            lang_lines = settings_read_file.split('\n')
            for lang_line in lang_lines:
                tmp = lang_line.split('=')
                tmp2 = getattr(self.ui, tmp[0])
                tmp2.setText(tmp[1])
        if self.settings["language"] == "ru":
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.profile_tab), "Профиль")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.statistic_tab), "Статистика")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.heroes_tab), "Герои")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.settings_tab),"Настройки")
        else:
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.profile_tab), "Profile")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.statistic_tab), "Statistic")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.heroes_tab), "Heroes")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.settings_tab), "Settings")





if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())


