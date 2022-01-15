#@title Игра
import sys
import random
from string import Template


class Choice:

    def __init__(self, text, scene_name, action=None, additional_text=""):
        self.text = text
        self.scene_name = scene_name
        self.action = action  # это лямбда с действием
        self.additional_text_choice = additional_text


class Scene:

    def __init__(self, text="", choices=[], additional_text=""):
      self.text = text
      self.additional_text = additional_text
      self.choices = choices  # это массив экземляров выборов

    def display_info(self, state):
        print(Template(self.text).safe_substitute(state))
        for count, choice in enumerate(self.choices, start=1):
            # print("\t", count,". ", choice.text.format(name), sep='')
            # это более умный вариант строки выше, а ещё тут name выросло до всего словаря состояний (state)
            print(f"\t{count}. {Template(choice.text).safe_substitute(state)}")

    def continue_scene(self):
        while True:
            try:
                choose = int(input()) - 1
                # возвращает название следующей сцены и лямбду (действие)
                result = (self.choices[choose].scene_name,
                          self.choices[choose].action)
                if self.additional_text:
                    print(self.additional_text)
                if self.choices[choose].additional_text_choice:
                    print(self.choices[choose].additional_text_choice)
                return result
            except:
                print("Неверно введён выбор, try again")


class Ending(Scene):

    def __init__(self, condition=None, choices=[]):
        self.condition = condition
        self.choices = choices

    def display_info(self, state):
        self.choose = int(self.condition(state))

    def continue_scene(self):
        result = (self.choices[self.choose].scene_name,
                  self.choices[self.choose].action)
        return result


class Exit(Scene):

    # здесь он должен выйти вместо вывода текста, так как это сцена завершения
    def display_info(self, name):
      print("Выход")
      sys.exit()


class Game:

    def __init__(self, scenes):
        self.scenes = scenes
        self.current_scene = scenes["menu"]
        self.state = {}

    def run(self):
        while True:
            self.current_scene.display_info(self.state)
            print("")
            result = self.current_scene.continue_scene()
            # это наличие лямбды, т. е. действия  (если её нет, то значение None, тогда не выполняется)
            if result[1]:
                # здесь состояние (state) обновляется через лямбду
                self.state = {**self.state, **result[1](self.state)}

                # print(self.state.get("count")) # для проверки счёта
                # print(self.state.get("anticount"))

            # result[0] - название следующей сцены
            self.current_scene = self.scenes[result[0]]


action = {"name_first": lambda state: {"name": input("Введите имя персонажа:"), "count": 0, "anticount": 0, "max_count": 6, "max_anticount": 6},
          # можно использовать только в первой сцене, так как тут обнуляется счёт (на самом деле создаётся)

          "count": lambda state: {"count": state["count"] + 1},
          "anticount": lambda state: {"anticount": state["anticount"] + 1},
          "random_title_1": lambda state: {"title": random.choice(['рыбка', 'охушка', 'небесный меч', 'правитель морей'])},
          "random_title_2": lambda state: {"title": random.choice(['глупая картошка', 'большая картошка', 'тихая картошка', 'упавшая картошка'])},
          "conditions": lambda state: 0 if state["anticount"] >= state["max_anticount"] - 1 else (1 if state["count"] >= state["max_count"]
                                                                                                  else (2 if state["count"] >= 4 else (3 if state["count"] >= 2 else 4)))}

scenes = {"menu": Scene(
    "Код: Saphielle Gilzeiros, текст: Saphielle Gilzeiros и Ирина Зайцева\n\n\
Каждый день человек принимает огромное количество решений. Мы делаем это так часто, что даже не подозреваем, куда нас может привести выбранный путь.\n\
Конечно, это всё очень серьёзно, но не стоит печалиться. Наша команда предлагает тебе немного расслабиться и отправить в маленькое путешествие.\n\
Вперед! \n\nЧтобы выбрать действие введите соответствующую цифру и нажмите [Enter]",

    [Choice("Начать игру", "start", action["name_first"]),
          Choice("Выйти", "exit_scene")]),

          "exit_scene": Exit(),

          "start": Scene(
    "Привет, $name. Так, что тут у нас? В самом начале тебе предстоит выбрать наиболее привлекательную дорожку. \n\
Не хотим мучать тебя нравоучениями о значении каждого действия (мы сделали это в начале), поэтому делай что хочешь.",

    [Choice("Назвать это дорогой нельзя... ЭТО ПУТЬ НИНДЗЯ.", "code"),
          Choice("go away", "bad_end_2")]),

    "code": Scene(
    "Коля, Гречка и Таня изучали примеры кода, где продемонстрирован один из основных принципов ООП. \n\
  — Это полиморфизм и код написан на C++ — сказала Гречка. \n\
  — Нет, здесь инкапсуляция, а написано всё на python, — возразил Коля. \n\
  — Это наследование, и написан код не на C++, - сказала Таня. \n\
Оказавшийся рядом программист сказал, что каждый из них прав только в одном из двух высказанных предположений. \n\
Что же там было показано?",
    [Choice("Python, наследование", "gift"),
     Choice("C++, инкапсуляция", "gift"),
     Choice("Python, полиморфизм", "gift", action["count"]),
     Choice("Haskell лучший", "gift", action["anticount"])]),

    "gift": Scene(
    "Наставнику пришли 3 коробки с подарками. В первой – финики, во второй – инжиры, а третья выдаёт случайным образом то финики, то инжиры.\n\
Чтобы получить подарок в одной из коробок, нужна 1 монета. \n\
Однако преподаватель перепутал надписи на коробках, поэтому на каждой из них оказалась неправильная наклейка. \n\
Сколько монет понадобится находчивому наставнику, чтобы понять, где какая коробка?",
   	[Choice("1 монетка", "winner", action["count"]),
            Choice("2 монетки", "winner"),
            Choice("3 монетки", "winner"),
            Choice("Лучше уволиться, чем работать в таких условиях.", "winner", action["anticount"])]),

    "winner": Scene(
    "Трое друзей, ребят из технокруга, спорили о результате предстоящего соревнования. \n\
  — Вот увидишь, Касперский не придет первым, — сказал Даниил. — Первым будет Эйджей. \n\
  — Да нет же, победителем будет, как всегда, Касперский! — воскликнула Кристина. — А о Снеже и говорить нечего, ей не быть первой. \n\
Денис возмутился: \n\
  — Эйджею не видать первого места, а вот Снежа считает на калькуляторе быстрее всех. \n\
По завершении сореванования оказалось, что каждое из двух предположений двоих друзей подтвердилось, а оба предположения третьего из друзей оказались неверны. \n\
Кто выиграл?",
    [Choice("Касперский", "mem", action["count"]),
     Choice("Снежа", "mem"),
     Choice("Эйджей", "mem"),
     Choice("Да кто этот ваш технокруг вообще такой?", "mem", action["anticount"])]),

    "mem": Scene(
    "Три подружки очень любили мемы. Однажды им попался очень хороший мем с котиком, но они забыли его сохранить. \n\
Рыбка утверждает, что это была серенькая сибирская кошка. \n\
Охушка сказала, что это был рыженький британец. \n\
Зачемушка, в свою очередь, сказала, что котик был точно не серый, и, вроде бы, это был мейн-кун. \n\
Когда удалось отыскать картинку, выяснилось, что каждая из подружек точно определила только одну характеристику кота, а в другой ошиблась. \n\
Что это был за котик?",
    [Choice("Рыженькая сибирская кошка", "bar", action["count"]),
     Choice("Серенький мейн-кун", "bar"),
     Choice("Серенький британец", "bar"),
     Choice("Рыженький мейн-кун", "bar"),
     Choice("Я тоже хочу посмотреть на котика", "bar", action["anticount"])]),

    "bar": Scene(
    "В Петербурге на улице Рубинштейна есть один бар, в который ходят лишь необщительные люди, назовём их интровертами. \n\
(На самом деле интроверты общительные, необщительность — это миф. Но это задачка, поэтому упростим.) \n\
\n\
Интроверты садятся вдоль барной стойки, где есть 25 мест. Когда входит новый посетитель, он всегда садится у стойки как можно дальше от остальных гостей. \n\
Никто не садится на соседнее место рядом с другим интровертом: если кто-то входит и видит, что свободных мест мало и надо сесть рядом с кем-то, то он уходит. \n\
\n\
Бармен хочет получить как можно больше клиентов. У него есть право посадить самого первого посетителя на любое место у стойки. \n\
Куда выгоднее посадить первого интроверта с точки зрения бармена?",
    [Choice("Место №1", "mandarin"),
     Choice("Место №9", "mandarin", action["count"]),
     Choice("Место №13", "mandarin"),
     Choice("Место №26", "mandarin", action["anticount"]),
     Choice("Прибыльнее будет закрыть бар.", "mandarin", action["anticount"])]),

    "mandarin": Scene(
    "Яна и Ира купили по 15 мандаринов для поднятия новогоднего настроения. \
Яна съела 7 мандаринов, а Ира съела столько мандаринов, сколько осталось у Иры. \
Сколько мандаринов на двоих осталось у девочек?",
    [Choice("0", "rain"),
     Choice("7", "rain"),
     Choice("8", "rain"),
     Choice("15", "rain", action["count"]),
     Choice("Мандариночки...", "rain", action["anticount"])]),


    "rain": Scene(
    "Если каждый день в 12 часов ночи идет дождь, то можно ли ожидать, что через 72 часа будет солнечная погода?",
    [Choice("Да", "meeting"),
     Choice("Возможно", "meeting"),
     Choice("Нет", "meeting", action["count"]),
     Choice("Вам следует обратиться к прогнозу погоды", "meeting", action["anticount"])]),

    "meeting": Scene(
    "Сергей и Оля переписывают старую библиотеку на разных языках программирования. \
Код Оли на Go выполняется на 2 миллисекунды быстрее, чем прошлая версия, \
но она считает, что на 3 миллисекунды медленннее. \
Код Сергея, написанный на Rust, на 3 миллисекунды медленнее, а ему кажется, что на 2 милисекунды быстрее. \
Сергей и Оля пытаются запустить программы так, чтобы они завершили выполнение одновременно.\
Чья программа закончит последней?",
    [Choice("Сергея", "bear", action["count"]),
     Choice("Выполнение завершится одновременно", "bear"),
     Choice("Оли", "bear"),
     Choice("А измерять время заранее они не умеют", "bear", action["anticount"])]),

    "bear": Scene(
    "Дом имеет четыре стены, причём все они смотрят на юг. Вокруг дома ходит медведь. Какого он цвета?",
   	[Choice("Бурый", "last_scene"),
            Choice("Чёрный", "last_scene"),
            Choice("Белый", "last_scene", action["count"]),
            Choice("Красно-чёрный", "last_scene", action["anticount"])]),

    "last_scene": Ending(action["conditions"],
                         [Choice("0", "anti_end"),
                          Choice("1", "good_end",
                                 action["random_title_1"]),
                          Choice("2", "neutral_end"),
                          Choice("3", "neutral_end_2"),
                          Choice("4", "bad_end", action["random_title_2"])]),

    "anti_end": Scene("ohhh did you import antigravity $name? $count$anticount$anticount$count$count$anticount",
                      [Choice("back home", "menu", None, "\tСпасибо за прохождение игры! ヽ(・∀・)ﾉ"),
                       Choice("Посмотреть ответы", "answers")]),

    "good_end": Scene("А вот и конец, ты умничка, $name! Звание: $title. Твой счёт — $count, а антисчёт — $anticount.",
                      [Choice("Меню", "menu", None, "\tСпасибо за прохождение игры! ヽ(・∀・)ﾉ"),
                       Choice("Посмотреть ответы", "answers")]),

    "neutral_end": Scene("Хорошая работа, $name! Твой счёт — $count, а антисчёт — $anticount.",
                         [Choice("Меню", "menu", None, "\tСпасибо за прохождение игры! ヽ(・∀・)ﾉ"),
                          Choice("Посмотреть ответы", "answers")]),

    "neutral_end_2": Scene("Может попробуешь ещё раз, $name? Твой счёт — $count, а антисчёт — $anticount.",
                           [Choice("Меню", "menu", None, "\tСпасибо за прохождение игры! ヽ(・∀・)ﾉ"),
                            Choice("Посмотреть ответы", "answers")]),

    "bad_end": Scene("Прости, но теперь ты $title! Твой счёт — $count, а антисчёт — $anticount.",
                     [Choice("Меню", "menu", None, "\tСпасибо за прохождение игры! ヽ(・∀・)ﾉ"),
                      Choice("Посмотреть ответы", "answers")]),

    "bad_end_2": Scene("okay",
                       [Choice("Меню", "menu")]),

    "answers": Scene(
    "Выбери интересующую задачу:",
    [Choice("Код", "answers", None, "\tПравильный ответ: python, полиморфизм.\n"),
     Choice("Монетки", "answers", None,
            "\t Правильный ответ: 1 монетка\n"),
     Choice("Победитель", "answers", None,
            "\t Правильный ответ: Касперский\n"),
     Choice("Котик", "answers", None,
            "\t Правильный ответ: рыженькая сибирская кошка\n"),
     Choice("Бар", "answers", None, "\t Правильный ответ: №9\n"),
     Choice("Мандарины", "answers", None,
            "\t Правильный ответ: 15 мандаринов\n"),
     Choice("Дождик", "answers", None, "\t Правильный ответ: нет\n"),
     Choice("Опоздавший", "answers", None,
            "\t Правильный ответ: Сергей\n"),
     Choice("Медведь", "answers", None, "\t Правильный ответ: белый\n"),

     Choice("Вернуться в меню", "menu")]),

    "scene_name_2": Scene(
    "описание сцены 2",
    [Choice("текст выбора 1", "scene_name_1"),
     Choice("текст выбора 2", "scene_name_1"),
     Choice("текст выбора 3", "scene_name_1"),
     Choice("текст выбора 4", "scene_name_1")]),
}

game = Game(scenes)
game.run()
