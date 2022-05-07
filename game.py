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
            if result[1]: # это наличие лямбды, т. е. действия  (если её нет, то значение None, тогда не выполняется)
                self.state = {**self.state, **result[1](self.state)} # здесь состояние (state) обновляется через лямбду

                # print(self.state.get("count")) # для проверки счёта
                # print(self.state.get("anticount"))

            self.current_scene = self.scenes[result[0]] # result[0] - название следующей сцены