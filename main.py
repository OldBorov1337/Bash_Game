from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from bash import select_stones, get_boxes_and_stones


class SettingsScreen(Screen):
    pass

class GameScreen(Screen):
    stones_left = NumericProperty(11)

class ResultScreen(Screen):
    pass

class BashGameApp(App):
    def build(self):
        self.load_kv('kivy_design.kv')  # Явная загрузка kv файла
        self.sm = ScreenManager()
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(GameScreen(name="game"))
        self.sm.add_widget(ResultScreen(name="result"))
        return self.sm


    def start_game(self, difficulty, first_player):
        self.difficulty = difficulty
        self.current_player = 1 if first_player == "Player 1" else 2
        self.stones_left = 11
        self.training_set = []
        self.player_data = get_boxes_and_stones()

    def make_move(self, stones_taken):
        if self.stones_left <= 0:
            return
        self.stones_left -= stones_taken
        screen = self.sm.get_screen("game")
        screen.ids.stones_label.text = f"Stones remain: {self.stones_left}"
        if self.stones_left == 0:
            self.end_game()
            return
        self.current_player = 3 - self.current_player
        if self.current_player == 2:
            ai_move = select_stones(self.player_data, self.stones_left)
            self.make_move(ai_move)

    def end_game(self):
        winner = "Player 1" if self.current_player == 1 else "Player 2"
        result_screen = self.sm.get_screen("result")
        result_screen.ids.result_label.text = f"{winner} WINS!"
        self.sm.current = "result"


if __name__ == "__main__":
    BashGameApp().run()



        



