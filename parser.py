import json
import sys

# тут заходим на сайт (пока что читаем инфу с сохраненной страницы) и получаем ее в текстовом виде
with open('bannannza old acc private profile.html', 'r') as testfile:
    text = testfile.read()
# получение текста html с кодами героев
heroes_list = {}
profile_type = text.split('<p class="masthead-permission-level-text">', 1)[1]
profile_type = profile_type.split('</p>', 1)[0]
if profile_type == 'Public Profile':
    profile_type = 1
elif profile_type == 'Private Profile':
    profile_type = 0
heroes_list['profile_type'] = profile_type
if heroes_list['profile_type'] == 0:
    with open('stats_test.txt', 'w') as file_obj:
        json.dump(heroes_list, file_obj)
    sys.exit()
else:
    # считываем текущий рейтинг и пишем в словарь
    current_sr = text.split('<div class="u-align-center h5">', 1)[1]
    current_sr = current_sr.split('</div></div>', 1)[0]
    heroes_list['current_rank'] = current_sr
    # сразу отделяем соревновательную статистику
    competitive_stats_html_code = text.split('<div id="competitive" data-js="career-category" data-mode="competitive"', 1)[1]
    competitive_stats_html_code = competitive_stats_html_code.split('<section id="achievements-section" class="content-box u-max-width-container">', 1)[0]
    heroes_list_text = competitive_stats_html_code.split('<select data-js="career-select" data-group-id="stats" class="dropdown-select-element"', 1)[1]
    heroes_list_text = heroes_list_text.split('</select>')[0]
    heroes_list_text = heroes_list_text.split('>', 1)[1]

    #разбиение на список героев и их id

    heroes_id_for_list = []
    heroes_list_array = heroes_list_text.split('</option>')
    for element in heroes_list_array:
        if len(element) > 0:
            id_hero = element.split('value="', 1)[1]
            id_hero = id_hero.split('" option-id="', 1)[0]
            name_hero = element.split('option-id="', 1)[1]
            name_hero = name_hero.split('">', 1)[0]
            heroes_list[id_hero] = {'name': name_hero, 'stats': {}}
            heroes_id_for_list.append(id_hero)
        else:
            pass


    # тут было отделение соревновательной статистики

    # разделение табличек с соревновательной статистикой на элементы
    # ВСЕ таблички со статами
    tables = '<div data-group-id="stats" data-category-id="' + competitive_stats_html_code.split('<div data-group-id="stats" data-category-id="', 1)[1]
    tables = tables.split('</div></section></div>', 1)[0]
    # тут таблички уже заносятся в массив каждая отдельно
    tables_array = tables.split('</table></div></div></div>')

    # тут делаем так, чтобы для каждого героя (по айди) записались статы все какие есть и приравниваем их к None
    # отделяем таблицы
    all_id_tables = '<div data-group-id="stats"' + competitive_stats_html_code.split('</option></select></div></div></div><hr><div data-group-id="stats"', 1)[1]
    # отделяем таблицы со статками
    all_id_tables = all_id_tables.split('</tbody></table></div></div>')
    id_tables_stats = []
    # через For делаем каждый элемент массива просто табличкой в которой есть айдишники и тд
    for table_id in all_id_tables:
        if len(table_id) > 0:
            if table_id.find('<tbody class="DataTable-tableBody">') > -1:
                table_stat = table_id.split('<tbody class="DataTable-tableBody">', 1)[1]
                stats_tables = table_stat.split('</td></tr>')
                for stat_table in stats_tables:
                    id_tables_stats.append(stat_table)
            else:
                pass
        else:
            pass

    # выделяем статки героев, айдишники и пишем в словарь
    for id_table_stats in id_tables_stats:
        if len(id_table_stats) > 0:
            stat_id = id_table_stats.split('<tr data-stat-id="', 1)[1]
            stat_id = stat_id.split('" class="DataTable-tableRow">', 1)[0]
            stat_name = id_table_stats.split('<td class="DataTable-tableColumn">', 1)[1]
            stat_name = stat_name.split('</td>', 1)[0]
            # записываем все статки для героев в список
            for id_hero in heroes_id_for_list:
                heroes_list[id_hero]['stats'][stat_id] = {'name': stat_name, 'value': None}
        else:
            pass




    # для каждой таблички
    for table in tables_array:
        if len(table) > 0:
            # выделяем айди героя
            hero_id = table.split('<div data-group-id="stats" data-category-id="', 1)[1]
            hero_id = hero_id.split('" class="row js-stats toggle-display', 1)[0]
            # сплитуем все статки по отдельности и они заносятся в массив
            stats_html_element = table.split('</td></tr>')
            # тут уже из элементов массива достаем айди статки, ее название и значение
            for stat in stats_html_element:
                if stat.find('<tr data-stat-id="') > -1:
                    stat_id = stat.split('<tr data-stat-id="', 1)[1]
                    stat_id = stat_id.split('" class="DataTable-tableRow">', 1)[0]
                    stat_name = stat.split('<td class="DataTable-tableColumn">', 1)[1]
                    stat_name = stat_name.split('</td>', 1)[0]
                    stat_value = stat.split('</td><td class="DataTable-tableColumn">', 1)[1]
                    stat_value = stat_value.split('</td>', 1)[0]
                    # записываем все статки для героев в список
                    heroes_list[hero_id]['stats'][stat_id] = {'name': stat_name, 'value': stat_value}
                else:
                    pass
        else:
            pass


    with open('stats_test.txt', 'w') as file_obj:
        json.dump(heroes_list, file_obj)