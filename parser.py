import json
import sys

# значения рамок и звезд для определения уровня
level_borders = {
    # Base level Bronze = 0
    "1055f5ae3a84b7bd8afa9fcbd2baaf9a412c63e8fe5411025b3264db12927771": 0,  # Bronze Lv 1
    "69c2c1aff0db8429a980bad7db76a3388003e43f0034097dc4cfa7f13c5de7d7": 0,  # Bronze Lv 11
    "4d63c2aadf536e87c84bdb7157c7b688cffb286e17a5362d2fa5c5281f4fc2a2": 0,  # Bronze Lv 21
    "78ebb45dd26b0050404305fdc1cb9ddc311d2c7e62400fd6348a3a488c69eee7": 0,  # Bronze Lv 31
    "888c84f2dfd211cde0c595036574040ca96b1698578daab90ce6822d89f7fe0e": 0,  # Bronze Lv 41
    "3fdfdd16c34ab7cdc9b7be3c04197e900928b368285ce639c1d3e1c0619eea6d": 0,  # Bronze Lv 51
    "e8b7df4b88998380658d49d00e7bc483c740432ac417218e94fab4137bec4ae0": 0,  # Bronze Lv 61
    "45cc69ca29f3981fa085b5337d2303a4eb555853daae1c29351b7ba46b27bbcd": 0,  # Bronze Lv 71
    "8b4be1017beff0bcd1f7a48d8cdf7faf9f22c1ffd2bdeaaff2684da5cddeaa76": 0,  # Bronze Lv 81
    "1b00b8cab530e98c378de2f3e8834d92ee41b4cd7b118179a8ecbccee83c8104": 0,  # Bronze Lv 91

    # Base level Silver = 6
    "f5d80c8b7370cda9a491bdf89e02bcd8c6ba1708189d907c7e4f55a719030264": 6,  # Silver Lv 1
    "ddb6f3f79241b8af2fa77b52910f60a2332db5d8347b3039d1328ae6d1272a59": 6,  # Silver Lv 11
    "c59072a340e6187116f5ae7456674dd6e1cba4b15781922d63fb94f56d9539c0": 6,  # Silver Lv 21
    "624461e537900ce98e3178d1a298cba4830c14f6a81a8b36319da6273bed255a": 6,  # Silver Lv 31
    "ba68d2c0f1b55e1991161cb1f88f369b97311452564b200ea1da226eb493e2e8": 6,  # Silver Lv 41
    "3c078f588353feeb3f52b0198fade12a78573a01c53050aca890969a395ff66a": 6,  # Silver Lv 51
    "f9bc9c6bb95f07f4e882b9e003ba7fa5ca6552fb8e0c27473a8b031714670116": 6,  # Silver Lv 61
    "8aa9f56cdd250579dd8b0ce6bd835934fffe8c27b9ce609f046c19a4a81591f8": 6,  # Silver Lv 71
    "32f84a58719318fa0aeee530ed3240952ba9945b998cd9e8150ebb583db0d4f6": 6,  # Silver Lv 81
    "c95fa44c02a1eae89a7c8d503026f181f1cc565da93d47c6254fab2c3d8793ef": 6,  # Silver Lv 91

    # Base level Gold = 12
    "5ab5c29e0e1e33f338ae9afc37f51917b151016aef42d10d361baac3e0965df1": 12,     # Gold Lv 1
    "7fd73e680007054dbb8ac5ea8757a565858b9d7dba19f389228101bda18f36b0": 12,     # Gold Lv 11
    "0ada1b8721830853d3fbcfabf616e1841f2100279cff15b386093f69cc6c09ad": 12,     # Gold Lv 21
    "7095ee84fc0a3aaac172120ffe0daa0d9abca33112e878cd863cd925cd8404b6": 12,     # Gold Lv 31
    "fa410247dd3f5b7bf2eb1a65583f3b0a3c8800bcd6b512ab1c1c4d9dd81675ae": 12,     # Gold Lv 41
    "a938ef37b673a240c4ade00d5a95f330b1e1ba93da9f0d3754bdb8a77bbbd7a1": 12,     # Gold Lv 51
    "49afee29dc05547ceebe6c1f61a54f7105a0e1b7f2c8509ff2b4aeaf4d384c8e": 12,     # Gold Lv 61
    "2c1464fb96d38839281c0bdb6e1a0cd06769782a5130609c13f6ca76fa358bcf": 12,     # Gold Lv 71
    "98f6eea1a2a10576251d6c690c13d52aaac19b06811ed2b684b43e7a9318f622": 12,     # Gold Lv 81
    "6e1036eab98de41694d785e076c32dbabe66962d38325117436b31210b003ad4": 12,     # Gold Lv 91

    # Base level Platinum = 18
    "69fde7abebb0bb5aa870e62362e84984cae13e441aec931a5e2c9dc5d22a56dc": 18,     # Platinum Lv 1
    "9c84055f9d91a297ccd1bac163c144e52bcce981dc385ff9e2957c5bd4433452": 18,     # Platinum Lv 11
    "97c803711cddc691bc458ec83dec73c570b0cc07219632c274bb5c5534786984": 18,     # Platinum Lv 21
    "c562ec882ababf2030e40ad3ce27e38176899f732166a1b335fd8f83735261f3": 18,     # Platinum Lv 31
    "da2cb4ab3281329c367cea51f9438c3d20d29ee07f55fa65762481777663f7f9": 18,     # Platinum Lv 41
    "460670e4d61b9bf0bcde6d93a52e50f01541177a20aaf69bbda91fe4353ed2b0": 18,     # Platinum Lv 51
    "5a019024b384de73f4348ed981ae58ec458a7ae6db68e0c44cda4d7062521b04": 18,     # Platinum Lv 61
    "1d5a458ecaf00fe0ef494b4159412d30a4b58ee76b9f0ff44b1db14ed211273c": 18,     # Platinum Lv 71
    "f1d43d87bbe5868cb99062ac02099001dd9f8215831347d8978e895468e81ef6": 18,     # Platinum Lv 81
    "27b2d05f97179aae72c8f72b69978777e1c5022f77e84f28e5943be8e9cd1d49": 18,     # Platinum Lv 91

    # Base level Diamond = 24
    "5c83959aa079f9ed9fd633411289920568e616c5117b2a7bb280dd8c857f8406": 24,     # Diamond Lv 1
    "ac14208753baf77110880020450fa4aa0121df0c344c32a2d20f77c18ba75db5": 24,     # Diamond Lv 11
    "a42bcb3339e1b3c999fc2799b0787fd862e163ec504d7541fa3ea8893b83957a": 24,     # Diamond Lv 21
    "7f1cc30ed6981974b6950666bb8236a6aa7b5a8579b14969394212dd7fa2951d": 24,     # Diamond Lv 31
    "efe3ab1c85c6266199ac7539566d4c811b0ee17bc5fb3e3e7a48e9bc2473cf50": 24,     # Diamond Lv 41
    "c7b9df20c91b10dc25bfdc847d069318ed9e8e69c5cad760803470caa9576e48": 24,     # Diamond Lv 51
    "413bdc1e11f9b190ed2c6257a9f7ea021fd9fcef577d50efcf30a5ea8df989a4": 24,     # Diamond Lv 61
    "625645c3c9af49eb315b504dba32137bb4081d348ec5b9750196b0ec0c9bb6a6": 24,     # Diamond Lv 71
    "f9813603e19350bb6d458bbee3c8c2a177b6503e6ff54868e8d176fa424a0191": 24,     # Diamond Lv 81
    "9e8600f97ea4a84d822d8b336f2b1dbfe7372fb9f2b6bf1d0336193567f6f943": 24,     # Diamond Lv 91 / Max
}

level_stars = {
    # Prestige modifiers
    "8de2fe5d938256a5725abe4b3655ee5e9067b7a1f4d5ff637d974eb9c2e4a1ea": 1,  # 1 Bronze star
    "755825d4a6768a22de17b48cfbe66ad85a54310ba5a8f8ab1e9c9a606b389354": 2,  # 2 Bronze stars
    "4a2c852a16043f613b7bfac33c8536dd9f9621a3d567174cb4ad9a80e3b13102": 3,  # 3 Bronze stars
    "bc80149bbd78d2f940984712485bce23ddaa6f2bd0edd1c0494464ef55251eef": 4,  # 4 Bronze stars
    "d35d380b7594b8f6af2d01040d80a5bfb6621553406c0905d4764bdc92a4ede8": 5,  # 5 Bronze stars

    "426c754c76cd12e6aacd30293a67363571341eea37880df549d3e02015a588fe": 1,  # 1 Silver star
    "c137dd97008328ed94efc5a9ec446e024c9ac92fce89fa5b825c5b1d7ff8d807": 2,  # 2 Silver stars
    "9a7c57aee22733a47c2b562000861d687d0423a74eb5e609c425f10db5528ed9": 3,  # 3 Silver stars
    "b944cf1de6653b629c951fd14583069bc91b1f1b7efdb171203448b2dbc39917": 4,  # 4 Silver stars
    "9b838b75065248ec14360723e4caf523239128ff8c13bda36cfd0b59ef501c1e": 5,  # 5 Silver stars

    "1858704e180db3578839aefdb83b89054f380fbb3d4c46b3ee12d34ed8af8712": 1,  # 1 Gold/Platinum star
    "e8568b9f9f5cac7016955f57c7b192ccd70f7b38504c7849efa8b1e3f7a1b077": 2,  # 2 Gold/Platinum stars
    "a25388825a0e00c946a23f5dd74c5b63f77f564231e0fd01e42ff2d1c9f10d38": 3,  # 3 Gold/Platinum stars
    "cff520765f143c521b25ad19e560abde9a90eeae79890b14146a60753d7baff8": 4,  # 4 Gold/Platinum stars
    "35fd7b9b98f57389c43e5a8e7ca989ca593c9f530985adf4670845bb598e1a9d": 5,  # 5 Gold/Platinum stars

    "8033fa55e3de5e7655cd694340870da851cdef348d7dcb76411f3a9c2c93002c": 1,  # 1 Diamond star
    "605c201cf3f0d24b318f643acb812084ff284e660f2bb5d62b487847d33fad29": 2,  # 2 Diamond stars
    "1c8c752d0f2757dc0bcc9e3db76f81c3802c874164a3b661475e1c7bd67c571f": 3,  # 3 Diamond stars
    "58b1323ab2eb1298fa6be649a8d4d7f0e623523bd01964ed8fefd5175d9073c0": 4,  # 4 Diamond stars
    "cd877430ccc400c10e24507dba972e24a4543edc05628045300f1349cf003f3a": 5,  # 5 Diamond stars
}



# тут заходим на сайт (пока что читаем инфу с сохраненной страницы) и получаем ее в текстовом виде
with open('bannannza_profile.html', 'r') as testfile:
    text = testfile.read()

# получение текста html с кодами героев
heroes_list = {}
profile_type = text.find('<div id="competitive"') > -1

# 1 - открытый профиль, 0 - закрытый
if profile_type == True:
    profile_type = 1
elif profile_type == False:
    profile_type = 0
heroes_list['profile_type'] = profile_type

# чекаем открыт или закрыт профиль
if heroes_list['profile_type'] == 0:
    with open('stats_test.txt', 'w') as file_obj:
        json.dump(heroes_list, file_obj)
    sys.exit()
else:
    # считываем текущий рейтинг и пишем в словарь
    current_sr = text.split('<div class="u-align-center h5">', 1)[1]
    current_sr = current_sr.split('</div></div>', 1)[0]
    heroes_list['current_rank'] = current_sr

    # считывание адреса аватарки
    avatar = text.split('<div class="masthead-player"><img src="', 1)[1]
    avatar = avatar.split('" class="player-portrait">', 1)[0]
    heroes_list['profile_avatar'] = avatar

    # считывание уровня репутации
    endorsement_level = text.split('<div class="endorsement-level">', 1)[1]
    endorsement_level = endorsement_level.split('<div class="u-center">', 1)[1]
    endorsement_level = endorsement_level.split('</div>', 1)[0]
    heroes_list['endorsement_level'] = endorsement_level

    # все для определения уровня аккаунта
    border_link = text.split('<div class="masthead-player-progression show-for-lg"><div style="background-image:url(', 1)[1]
    stars_link = border_link.split('</div><div style="background-image:url(', 1)[1]
    stars_link = stars_link.split(')" class="player-rank">', 1)[0]

    if len(stars_link) > 0:
        heroes_list['stars_link'] = stars_link
    else:
        heroes_list['stars_link'] = None

    acc_level = border_link.split('class="player-level"><div class="u-vertical-center">', 1)[1]
    acc_level = acc_level.split('</div>', 1)[0]
    border_link = border_link.split(')" class="player-level">', 1)[0]
    heroes_list['acc_level'] = acc_level
    heroes_list['border_link'] = border_link

    # вычисляем уровень и записываем
    border_hash = border_link.split('cloudfront.net/overwatch/', 1)[1]
    border_hash = border_hash.split('.png', 1)[0]
    if len(stars_link) > 0:
        stars_hash = stars_link.split('cloudfront.net/overwatch/', 1)[1]
        stars_hash = stars_hash.split('.png', 1)[0]
    else:
        stars_hash = 0

    if stars_hash != 0:
        profile_level = level_borders[border_hash] * 100 + level_stars[stars_hash] * 100 + int(acc_level)
    else:
        profile_level = level_borders[border_hash] * 100 + int(acc_level)
    heroes_list['profile_level'] = profile_level

    # отделяем соревновательную статистику
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