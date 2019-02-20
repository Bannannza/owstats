with open('test.html', 'r') as testfile:
    text = testfile.read()
# получение текста html с кодами героев
heroes_list_text = text.split('<select data-js="career-select" data-group-id="stats" class="dropdown-select-element"')[1]
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

# отделение соревновательной статистики
competitive_stats_html_code = text.split('<div id="competitive" data-js="career-category" data-mode="competitive"', 1)[1]
competitive_stats_html_code = competitive_stats_html_code.split('<section id="achievements-section" class="content-box u-max-width-container">', 1)[0]

# разделение табличек с соревновательной статистикой на элементы
tables = '<div data-group-id="stats" data-category-id="' + competitive_stats_html_code.split('<div data-group-id="stats" data-category-id="', 1)[1]
tables = tables.split('</div></section></div>', 1)[0]
tables_array = tables.split('</table></div></div></div>')
for table in tables_array:
    if len(table) > 0:
        hero_id = table.split('<div data-group-id="stats" data-category-id="', 1)[1]
        hero_id = hero_id.split('" class="row js-stats toggle-display',1)[0]

    else:
        pass
# Парсинг id и названий всех стат

