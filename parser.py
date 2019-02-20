import json

with open('test.html', 'r') as testfile:
    text = testfile.read()
# получение текста html с кодами героев
# сразу отделяем соревновательную статистику
competitive_stats_html_code = text.split('<div id="competitive" data-js="career-category" data-mode="competitive"', 1)[1]
competitive_stats_html_code = competitive_stats_html_code.split('<section id="achievements-section" class="content-box u-max-width-container">', 1)[0]
heroes_list_text = competitive_stats_html_code.split('<select data-js="career-select" data-group-id="stats" class="dropdown-select-element"', 1)[1]
heroes_list_text = heroes_list_text.split('</select>')[0]
heroes_list_text = heroes_list_text.split('>', 1)[1]

#разбиение на список героев и их id
heroes_list = {}
heroes_list_array = heroes_list_text.split('</option>')
for element in heroes_list_array:
    if len(element) > 0:
        id_hero = element.split('value="', 1)[1]
        id_hero = id_hero.split('" option-id="', 1)[0]
        name_hero = element.split('option-id="', 1)[1]
        name_hero = name_hero.split('">', 1)[0]
        heroes_list[id_hero] = {'name': name_hero, 'stats': {}}
    else:
        pass
print(heroes_list)

# тут было отделение соревновательной статистики

# разделение табличек с соревновательной статистикой на элементы
# ВСЕ таблички со статами
tables = '<div data-group-id="stats" data-category-id="' + competitive_stats_html_code.split('<div data-group-id="stats" data-category-id="', 1)[1]
tables = tables.split('</div></section></div>', 1)[0]
# тут таблички уже заносятся в массив каждая отдельно
tables_array = tables.split('</table></div></div></div>')
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
                heroes_list[hero_id]['stats'][stat_id] = {'name': stat_name, 'value': stat_value}
            else:
                pass
    else:
        pass
print(heroes_list)
with open('stats_test.txt', 'w') as file_obj:
    json.dump(heroes_list, file_obj)
# Парсинг id и названий всех стат

