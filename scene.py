import sys
from string import Template


class Choice:

    def __init__(self, text, scene_name, action = None, additional_text=""):
        self.text = text
        self.scene_name = scene_name
        self.action = action # это лямбда с действием
        self.additional_text_choice = additional_text

class Scene:

    def __init__(self, text="", choices=[], additional_text=""):
      self.text = text
      self.additional_text = additional_text
      self.choices = choices  # это массив экземляров выборов

    def display_info(self, state):
        print(Template(self.text).safe_substitute(state))
        for count, choice in enumerate(self.choices, start = 1):
            # print("\t", count,". ", choice.text.format(name), sep='')
            print(f"\t{count}. {Template(choice.text).safe_substitute(state)}") # это более умный вариант строки выше, а ещё тут name выросло до всего словаря состояний (state)

    def continue_scene(self):
        while True:
            try:
                choose = int(input()) - 1
                result = (self.choices[choose].scene_name, self.choices[choose].action) #возвращает название следующей сцены и лямбду (действие)
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
        result = (self.choices[self.choose].scene_name, self.choices[self.choose].action)
        return result


class Exit(Scene):

    def display_info(self, name): # здесь он должен выйти вместо вывода текста, так как это сцена завершения
      print("Выход")
      sys.exit()