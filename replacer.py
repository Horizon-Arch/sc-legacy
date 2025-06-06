import re
import sys
import os

ignore_keys = [
    "clans.tournament.tournament_roza_vetrov2.name",
    "battlefield.id.peklo.name",
    "clans.tournament.tournament_roza_vetrov.name",
    "clans.tournament.tournament_roza_vetrov2_2x6.name",
    "clans.tournament.tournament_roza_vetrov2_2x4.name",
    "clans.tournament.tournament_roza_vetrov2_1x4.name",
    "checkpoints.dungeon_sub_merc_03.control_point",
    "cnps.availability.desc.barter.trader_lodochnaya.bolota_safezone_3",
    "cnps.faction.settlement_bandits_lodochnaya.relation.2",
    "map.global.region.tournament_roza_vetrov.name",
    "stalker.quickcommands.bandits.hello.6",
    "location.battlefield_peklo_open.name",
    "battlefield.id.krot2.name",
    "ejection.stage.notf.storm_14",
    "ejection.stage.notf.ending_4",
    "ejection.stage.notf.ending_8",
    "ejection.stage.notf.ending_18",
    "ejection.stage.notf.ending_23"
]

replacements = {
            "Рубеж": "Долг",
            "Заря": "Свобода",
            "Шепот": "Монолит",
            "Рубежом": "Долгом",
            "Зарёй": "Свободой",
            "Шепотом": "Монолитом",
            "Рубежа": "Долга",
            "Зари": "Свободы",
            "Шепота": "Монолита",
            "Зарю": "Свободу",
            "Крыса": "Тушкан",
            "Хрюша": "Плоть",
            "Шавка": "Слепой пес",
            "Пси-гончая": "Пси-собака",
            "Дикая гончая": "Псевдособака",
            "Шнырь": "Снорк",
            "Упырь": "Кровосос",
            "Бурелом": "Псевдогигант",
            "Бестия": "Химера",
            "Крысы": "Тушканы",
            "Хрюши": "Плоти",
            "Шавки": "Слепые псы",
            "Пси-гончие": "Пси-собаки",
            "Дикие гончие": "Псевдособаки",
            "Шныри": "Снорки",
            "Упыри": "Кровососы",
            "Буреломы": "Псевдогиганты",
            "Бестии": "Химеры",
            "хрюшки": "плоти",
            "Крысы": "Тушкана",
            "Хрюши": "Плоти",
            "Шавки": "Слепого пса",
            "Пси-гончей": "Пси-собаки",
            "Дикой гончей": "Псевдособаки",
            "Шныря": "Снорка",
            "Упыря": "Кровососа",
            "Бурелома": "Псевдогиганта",
            "Бестии": "Химеры",  
            "Крыс": "Тушканов", 
            "Хрюш": "Плотей", 
            "Шавок": "Слепых псов", 
            "Пси-гончих": "Пси-собак", 
            "Диких гончих": "Псевдособак", 
            "Шнырей": "Снорков", 
            "Упырей": "Кровососов", 
            "Буреломов": "Псевдогигантов", 
            "Бестий": "Химер",
            "Обочина": "Кордон",
            "Свалка техники": "Свалка",
            "Черные Ивы": "Темная долина",
            "Завод «Первомайский»": "Завод Росток",
            "Бар «Пьяный Гейгер»": "Бар «100 Рентген»",
            "Агрокомплекс «Колос»": "Агропром",
            "Полесское": "Армейские склады",
            "Любеч-3": "Лиманск",
            "Тихая заводь": "Затон",
            "Волчок": "Карусель",
            "Омут": "Воронка",
            "нора": "Пространственный пузырь",
            "Зажигалка": "Жарка",
            "Чайник": "Пар",
            "Пекло": "Цирк",
            "Разряд": "Электра",
            "Холодец": "Кисель",
            "Студень": "Ведьмин студень",
            "Пух": "Жгучий пух",
            "Волчка": "Карусели",
            "Омута": "Воронки",
            "Норы": "Пространственного пузыря",
            "Зажигалки": "Жарки",
            "Чайника": "Пара",
            "Пекла": "Цирка",
            "Разряда": "Электры",
            "Холодца": "Киселя",
            "Студня": "Ведьминого студня",
            "Пуха": "Жгучего пуха",
            "Аптечка ученых": "Аптечка научная",
            "Военная аптечка": "Аптечка армейская",
            "«Гемостат»": "«Барвинок»",
            "Антирад Б-191": "Антирад первого класса",
            "Антирад Б-29": "Антирад второго класса",
            "Антирад Б-393": "Антирад третьего класса",
            "Тоник «Арни»": "«Геркулес»",
            "Пси-блок «Нейрон-11»": "«Пси-блокада» первого класса",
            "Пси-блок «Нейрон-22»": "«Пси-блокада» второго класса",
            "Пси-блок «Нейрон-33»": "«Пси-блокада» третьего класса",
            "Лимб": "Лим",
            "Темный Лимб": "Черный Лим",
            "«Комбат» Оракула": "«Берилл» Оракула",
            "Бандитский кожак": "Бандитская куртка",
            "Бронекостюм «Комбат-5M»": "Бронекостюм «Берилл-5M»",
            "Бронекостюм «Скиф-5»": "Бронекостюм «СКАТ-10»",
            "Бронекостюм «Скиф-4Б»": "Бронекостюм «СКАТ-9Б»",
            "Бронекостюм «Скиф-4»": "Бронекостюм «СКАТ-9м»",
            "Бронекостюм «Скиф-2м»": "Бронекостюм ПСЗ-",
            "Сталкерская кожанка": "Кожаная куртка",
            "Комбинезон «Аврора»": "Комбинезон «Заря»",
            "Комбинезон «Аврора» c противогазом": "Комбинезон «Заря» c противогазом",
            "Комбинезон «Аврора-Б»": "Комбинезон «Заря-Б»",
            "Комбинезон «Уран»": "Комбинезон «СЕВА»",
            "Экзоскелет «Гектор»": "Модифицированный экзоскелет",
            "Экзоскелет": "Экзоскелет «Самсон»",
            "Комбинезон «Грибник»": "Комбинезон «Турист»",
            "«Лягуха»": "«Гадюка»",
            "«Волна»": "«Лавина»",
            "Винтовка Гаусса": "Гаусс-пушка",
            "Винтовки Гаусса": "Гаусс-пушки",
            "ОЦ-14M «Ураган»": "ОЦ-14M «Шторм»",
            "«Шлёпа»": "Рысь",
            "«Большой Билл»": "Большой Бэн",
            "«Уравнитель»": "L85A1 «Баланс»",
            "Сиг «Шепота»": "Монолитовский Сиг",
            "Глок «Шепота»": "Глок Монолита",
            "Трещотка": "Бенгальский огонь",
            "Комета": "Вспышка",
            "Вехотка": "Выверт",
            "Гребешок": "Глаз",
            "Прима": "Грави",
            "Сердце": "Душа",
            "Креветка": "Золотая рыбка",
            "Золотистая Прима": "Золотистый грави",
            "Роза": "Каменный цветок",
            "Пиявка": "Капля",
            "Кислотный кристалл": "Кислый кристалл",
            "Ежик": "Колобок",
            "Репях": "Колючка",
            "Красный кристалл": "Кристалл",
            "Липкий репях": "Кристальная колючка",
            "Ягодка": "Кровь камня",
            "Сало": "Ломоть мяса",
            "Лампочка Ильича": "Лунный свет",
            "Ветка Калины": "Мамины бусы",
            "Цибуля": "Медуза",
            "Ершик": "Морской еж",
            "Белая роза": "Ночная звезда",
            "Огонек": "Огненный шар",
            "Жар-птица": "Пламя",
            "Ряска": "Пленка",
            "Протоцибуля": "Протомедуза",
            "Гантель": "Пружина",
            "Жвачка": "Пузырь",
            "Гиря": "Пустышка",
            "Змеиный глаз": "Светляк",
            "Скорлупа": "Слизняк",
            "Флегма": "Слизь",
            "Чернильница": "Слюда",
            "Ледяной ежик": "Снежинка",
            "Стальной ежик": "Стальной колобок",
            "Проклятая роза": "Темная медуза",
            "Призрачный кристалл": "Частотный кристалл",
            "Рубежники": "Долговцы",
            "Зорьки": "Свободовцы",
            "Сельская школа": "Фотон-2",
            "Пожарная часть": "АТП",
            "База «Зари»": "База «Свободы»",
            "Трещоткой": "Бенгальским огнём",
            "Кометой": "Вспышкой",
            "Вехоткой": "Вывертом",
            "Гребешком": "Глазом",
            "Примой": "Грави",
            "Сердцем": "Душой",
            "Креветкой": "Золотой рыбкой",
            "Золотистой Примой": "Золотистым грави",
            "Розой": "Каменным цветком",
            "Пиявкой": "Каплей",
            "Кислотным кристаллом": "Кислым кристаллом",
            "Ёжиком": "Колобком",
            "Репяхом": "Колючкой",
            "Красным кристаллом": "Кристаллом",
            "Липким репяхом": "Кристальной колючкой",
            "Ягодкой": "Кровью камня",
            "Салом": "Ломтем мяса",
            "Лампочкой Ильича": "Лунным светом",
            "Веткой Калины": "Мамиными бусами",
            "Цибулей": "Медузой",
            "Ёршиком": "Морским ежом",
            "Белой розой": "Ночной звездой",
            "Огоньком": "Огненным шаром",
            "Жар-птицей": "Пламенем",
            "Ряской": "Плёнкой",
            "Протоцибулей": "Протомедузой",
            "Гантелью": "Пружиной",
            "Жвачкой": "Пузырём",
            "Гирей": "Пустышкой",
            "Змеиным глазом": "Светляком",
            "Скорлупой": "Слизняком",
            "Флегмой": "Слизью",
            "Чернильницей": "Слюдой",
            "Ледяным ёжиком": "Снежинкой",
            "Стальным ёжиком": "Стальным колобком",
            "Проклятой розой": "Тёмной медузой",
            "Призрачным кристаллом": "Частотным кристаллом",
            "Тёмным кристаллом": "Чёрным кристаллом",
            "Трещотки": "Бенгальского огня",
            "Кометы": "Вспышки",
            "Вехотки": "Выверта",
            "Гребешка": "Глаза",
            "Примы": "Грави",
            "Сердца": "Души",
            "Креветки": "Золотой рыбки",
            "Золотистой Примы": "Золотистого грави",
            "Розы": "Каменного цветка",
            "Пиявки": "Капли",
            "Кислотного кристалла": "Кислого кристалла",
            "Ёжика": "Колобка",
            "Репяха": "Колючки",
            "Красного кристалла": "Кристалла",
            "Липкого репяха": "Кристальной колючки",
            "Ягодки": "Крови камня",
            "Сала": "Ломтя мяса",
            "Лампочки Ильича": "Лунного света",
            "Ветки Калины": "Маминых 6yc",
            "Цибули": "Медузы",
            "Ёршика": "Морского ежа",
            "Белой розы": "Ночной звезды",
            "Огонька": "Огненного шара",
            "Жар-птицы": "Пламени",
            "Ряски": "Плёнки",
            "Протоцибули": "Протомедузы",
            "Гантели": "Пружины",
            "Жвачки": "Пузыря",
            "Гири": "Пустышки",
            "Змеиного глаза": "Светляка",
            "Скорлупы": "Слизняка",
            "Флегмы": "Слизи",
            "Чернильницы": "Слюды",
            "Ледяного ёжика": "Снежинки",
            "Стального ёжика": "Стального колобка",
            "Проклятой розы": "Тёмной медузы",
            "Призрачного кристалла": "Частотного кристалла",
            "Тёмного кристалла": "Чёрного кристалла",
            "Трещотку": "Бенгальский огонь",
            "Комету": "Вспышку",
            "Вехотку": "Выверт",
            "Приму": "Грави",
            "Креветку": "Золотую рыбку",
            "Золотистую Приму": "Золотистый грави",
            "Розу": "Каменный цветок",
            "Пиявку": "Каплю",
            "Ягодку": "Кровь камня",
            "Лампочку Ильича": "Лунный свет",
            "Ветку Калины": "Мамины бусы",
            "Цибулю": "Медузу",
            "Белую розу": "Ночную звезду",
            "Огонёк": "Огненный шар",
            "Жар-птицу": "Пламя",
            "Ряску": "Плёнку",
            "Протоцибулю": "Протомедузу",
            "Жвачку": "Пузырь",
            "Гирю": "Пустышку",
            "Скорлупу": "Слизняка",
            "Флегму": "Слизь",
            "Чернильницу": "Слюду",
            "Проклятую розу": "Тёмную медузу",
            "Тёмный кристалл": "Чёрный кристалл",
            "Обочина переполнена": "Кордон переполнен",
            "зорьки": "свободовцы",
            "рубежник": "долговец",
            "Любечские": "Лиманские",
            "нор": "Пузырей",
            "завода «Первомайский»": "Завода Росток",
            "Тихой Заводи": "Затоне",
            "Первомайском": "Ростке",
            "Зажигалок": "Жарок",
            "Тихой Заводью": "Затоном",
            "шепчущих": "монолитовцев"
}

def should_ignore(key):
    return any(ignore_key in key for ignore_key in ignore_keys)

def replace_text(text, replacements):
    for old, new in replacements.items():
        text = re.sub(r'\b' + re.escape(old) + r'\b', new, text, flags=re.IGNORECASE)
    return text

if __name__ == "__main__":
    input_file = input("Вставьте путь к файлу, затем нажмите Enter: ").strip().strip('"')

    if not os.path.exists(input_file):
        print(f"Ошибка: Файл '{input_file}' не найден. Убедитесь, что путь верен.")
        input("Нажмите Enter для выхода...")
        sys.exit()

    file_dir, file_name = os.path.split(input_file)
    file_base, file_ext = os.path.splitext(file_name)
    output_file = os.path.join(file_dir, f"{file_base}_modified{file_ext}")

    try:
        with open(input_file, "r", encoding="utf-8") as f_in, \
             open(output_file, "w", encoding="utf-8") as f_out:
            for line in f_in:
                line = line.rstrip("\n")
                if "=" not in line:
                    f_out.write(line + "\n")
                    continue

                key, val = line.split("=", 1)
                if should_ignore(key):
                    f_out.write(line + "\n")
                else:
                    new_val = replace_text(val, replacements)
                    f_out.write(f"{key}={new_val}\n")
        print(f"Файл обработан. Результат сохранен в: {output_file}")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

    input("Enter для выхода...")
