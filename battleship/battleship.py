from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import randint


class BattleshipGame(GridLayout):
    SHIPS = [2, 3, 3, 4, 4, 5]

    def __init__(self, **kwargs):
        super(BattleshipGame, self).__init__(**kwargs)
        self.cols = 11  # 10 for the board and an extra for labels

        self.board_size = 10
        self.board_player = [[0] * self.board_size for _ in range(self.board_size)]  # 0 represents an empty cell
        self.board_opponent = [[0] * self.board_size for _ in range(self.board_size)]

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
        if (row, col) in self.player_missiles:
            return  # already hit this zone

        self.player_missiles.add((row, col))
        if self.board_opponent[row][col] == 1:
            instance.text = 'X'  # Hit
            instance.background_color = (255, 0, 0, 1)
            self.opponent_ships.discard((row, col))
            print(f"opponent ships: {len(self.opponent_ships)}")
            if not self.opponent_ships:
                # Player Won!!! (sound - win)
                print("you win!")
                exit()
            else:
                # (sound - player hit)
                pass
        else:
            instance.text = 'O'  # Miss
            instance.background_color = (0, 255, 0, 1)
            # (sound - player miss)

        self.opponent_move()

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
            print('Computer hits!')
            if not self.player_ships:
                # Computer Won!!! (sound - loss)
                print("you lose!")
                exit()
            else:
                # Computer Won!!! (sound - computer hit)
                pass
        else:
            # computer miss
            print('Computer misses!')

        if self.board_player[row][col] == 0:
            self.board_player[row][col] = 1  # Mark the move on the player's board
        


class BattleshipApp(App):
    def build(self):
        return BattleshipGame()


if __name__ == '__main__':
    BattleshipApp().run()
