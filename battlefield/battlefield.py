from kivy.app import App
from kivy.uix.widget import Widget


class BattlefieldGame(Widget):
    pass


class BattlefieldApp(App):
    def build(self):
        return BattlefieldGame()


if __name__ == "__main__":
    BattlefieldApp().run()
