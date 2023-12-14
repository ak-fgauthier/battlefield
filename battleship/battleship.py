import ctypes
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import randint


wwise = None
game_instance = None


class BattleshipGame(GridLayout):
    WWISE_GAME_ID = 42
    SHIPS = [2, 3, 3, 4, 4, 5]

    def __init__(self, **kwargs):
        super(BattleshipGame, self).__init__(**kwargs)
        self.cols = 11  # 10 for the board and an extra for labels

        self.board_size = 10
        self.board_player = [[0] * self.board_size for _ in range(self.board_size)]  # 0 represents an empty cell
        self.board_opponent = [[0] * self.board_size for _ in range(self.board_size)]

        self.buttons = []

        # Create labels for row and column headers
        self.add_widget(Label(text=''))
        for i in range(1, self.board_size + 1):
            self.add_widget(Label(text=str(i)))

        # Create buttons for the game board
        for row in range(1, self.board_size + 1):
            self.add_widget(Label(text=chr(ord('A') + row - 1)))
            for col in range(1, self.board_size + 1):
                button = Button(
                    text=' ',
                    font_size=20,
                    size_hint=(None, None),
                    width=40,
                    height=40,
                    on_press=self.cell_pressed
                )
                button.row = row - 1
                button.col = col - 1
                self.add_widget(button)
                self.buttons.append(button)

        self.place_ships(self.board_player, BattleshipGame.SHIPS)
        self.place_ships(self.board_opponent, BattleshipGame.SHIPS)

        self.player_ships = set((row, col)
                                for row in range(self.board_size)
                                for col in range(self.board_size)
                                if self.board_player[row][col] == 1)

        self.opponent_ships = set((row, col)
                                  for row in range(self.board_size)
                                  for col in range(self.board_size)
                                  if self.board_opponent[row][col] == 1)
        
        self.player_missiles = set()
        self.opponent_missiles = set()

    def place_ships(self, board, ships):
        # Place multiple ships on the board
        for length in ships:
            while True:
                orientation = randint(0, 1)  # 0 for horizontal, 1 for vertical
                if orientation == 0:  # Horizontal
                    ship_row = randint(0, self.board_size - 1)
                    ship_col = randint(0, self.board_size - length)
                    if all(board[ship_row][col] == 0 for col in range(ship_col, ship_col + length)):
                        for col in range(ship_col, ship_col + length):
                            board[ship_row][col] = 1
                        break
                else:  # Vertical
                    ship_row = randint(0, self.board_size - length)
                    ship_col = randint(0, self.board_size - 1)
                    if all(board[row][ship_col] == 0 for row in range(ship_row, ship_row + length)):
                        for row in range(ship_row, ship_row + length):
                            board[row][ship_col] = 1
                        break

    def cell_pressed(self, instance):
        row, col = instance.row, instance.col
        self.disable_buttons(True)

        self.player_missiles.add((row, col))
        if self.board_opponent[row][col] == 1:
            instance.text = 'X'  # Hit
            instance.background_color = (255, 0, 0, 1)
            self.opponent_ships.discard((row, col))
            print(f"opponent ships: {len(self.opponent_ships)}")
            if not self.opponent_ships:
                self.produce_sound("win")
                exit()
            else:
                self.produce_sound("hit")
                pass
        else:
            instance.text = 'O'  # Miss
            instance.background_color = (0, 255, 0, 1)
            self.produce_sound("miss")

        Clock.schedule_once(callback_to_opponent, 0.15)

    def opponent_move(self):
        while True:
            # find an unhit zone
            row = randint(0, self.board_size - 1)
            col = randint(0, self.board_size - 1)
            if (row, col) not in self.opponent_missiles:
                break

        self.opponent_missiles.add((row, col))

        if (row, col) in self.player_ships:
            self.player_ships.discard((row, col))
            if not self.player_ships:
                self.produce_sound("lose")
                exit()
            else:
                self.produce_sound("hit")
                pass
        else:
            self.produce_sound("miss")

        if self.board_player[row][col] == 0:
            self.board_player[row][col] = 1  # Mark the move on the player's board

    def produce_sound(self, sound_name):
        global wwise
        print(sound_name)  # Show name to be played
        wwise.AK_SE_PostEvent(sound_name, BattleshipGame.WWISE_GAME_ID)

    def disable_buttons(self, disabled):
        for button in self.buttons:
            button.disabled = disabled

    def __del__(self):
        global wwise
        wwise.AK_SE_Term()

class BattleshipApp(App):
    def build(self):
        global game_instance
        Clock.schedule_interval(callback, 0)
        game_instance = BattleshipGame()
        return game_instance


def load_dll():
    global wwise
    wwise = ctypes.cdll.LoadLibrary("lib/libAkSoundEngineDLL.so")


def callback(dt):
    wwise.AK_SE_Tick()


def callback_to_opponent(dt):
    global game_instance
    game_instance.opponent_move()
    game_instance.disable_buttons(False)


if __name__ == '__main__':
    remove_env = False
    if not os.environ.get("WWISE_SOUNDBANK_DIR"):
        remove_env = True
        os.environ["WWISE_SOUNDBANK_DIR"] = os.getcwd() + "/data/soundbanks"
    load_dll()
    wwise.AK_SE_Init()
    BattleshipApp().run()
    if remove_env:
        del os.environ["WWISE_SOUNDBANK_DIR"]
