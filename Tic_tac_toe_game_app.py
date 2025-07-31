from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.checkbox import CheckBox
import random

class TicTacToe(GridLayout):
    def __init__(self, player1, player2, ai_mode=False, ai_level="Normal", back_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 5
        self.padding = 5
        self.current_player = "X"
        self.player_names = {"X": player1, "O": player2}
        self.ai_mode = ai_mode
        self.ai_level = ai_level
        self.buttons = []
        self.scores = {"X": 0, "O": 0}
        self.back_callback = back_callback

        # Top bar (Back + Title)
        top_bar = BoxLayout(size_hint=(1, 0.1), padding=5, spacing=5)
        back_btn = Button(text="←", size_hint=(0.15, 1), font_size=28, background_normal='', background_color=(0.2, 0.5, 0.7, 1))
        back_btn.bind(on_press=lambda x: self.back_callback() if self.back_callback else None)
        title = Label(text="Tic Tac Toe", font_size=28, bold=True, halign="center", valign="middle")
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)
        self.add_widget(top_bar)

        # Game grid
        grid = GridLayout(cols=3, spacing=3, size_hint=(1, 0.9))
        with grid.canvas.before:
            Color(0.15, 0.2, 0.3, 1)
            self.bg_rect = Rectangle(size=grid.size, pos=grid.pos)
        grid.bind(size=self.update_bg, pos=self.update_bg)

        for i in range(9):
            btn = Button(
                font_size=40,
                on_press=self.on_button_press,
                background_normal='',
                background_color=(0.1, 0.4, 0.7, 1),
                color=(1, 1, 1, 1),
                border=(2, 2, 2, 2)
            )
            btn.bind(on_release=self.on_hover)
            grid.add_widget(btn)
            self.buttons.append(btn)

        self.add_widget(grid)

        # Load sounds (optional)
        self.win_sound = SoundLoader.load('win.wav') or None
        self.draw_sound = SoundLoader.load('draw.wav') or None
        self.click_sound = SoundLoader.load('click.wav') or None

    def update_bg(self, *args):
        self.bg_rect.size = self.children[0].size
        self.bg_rect.pos = self.children[0].pos

    def on_hover(self, instance, *args):
        anim = Animation(background_color=(0.2, 0.6, 0.3, 1), duration=0.2)
        anim.start(instance)

    def on_button_press(self, instance):
        from kivy.app import App
        if instance.text == "":
            if self.click_sound: self.click_sound.play()
            instance.text = self.current_player
            if self.check_winner():
                self.scores[self.current_player] += 1
                if self.win_sound: self.win_sound.play()
                App.get_running_app().update_score_label()
                self.show_popup(f"{self.player_names[self.current_player]} wins!\n\nScores:\n{self.player_names['X']} (X): {self.scores['X']}\n{self.player_names['O']} (O): {self.scores['O']}")
            elif all(b.text != "" for b in self.buttons):
                if self.draw_sound: self.draw_sound.play()
                self.show_popup("It's a Draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.ai_mode and self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        from kivy.app import App
        empty_buttons = [b for b in self.buttons if b.text == ""]
        if not empty_buttons: return

        if self.ai_level == "Normal":
            choice = random.choice(empty_buttons)
        elif self.ai_level == "Hard":
            choice = self.find_best_move() or random.choice(empty_buttons)
        elif self.ai_level == "Super Hard":
            choice = self.find_best_move(block=True) or random.choice(empty_buttons)
        else:
            choice = random.choice(empty_buttons)

        choice.text = "O"
        if self.check_winner():
            self.scores["O"] += 1
            if self.win_sound: self.win_sound.play()
            App.get_running_app().update_score_label()
            self.show_popup(f"{self.player_names['O']} wins!\n\nScores:\n{self.player_names['X']} (X): {self.scores['X']}\n{self.player_names['O']} (O): {self.scores['O']}")
        elif all(b.text != "" for b in self.buttons):
            if self.draw_sound: self.draw_sound.play()
            self.show_popup("It's a Draw!")
        else:
            self.current_player = "X"

    def find_best_move(self, block=False):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        target = "O" if not block else "X"
        for combo in combos:
            values = [self.buttons[i].text for i in combo]
            if values.count(target) == 2 and values.count("") == 1:
                return self.buttons[combo[values.index("")]]
        return None

    def check_winner(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for combo in combos:
            if self.buttons[combo[0]].text == self.buttons[combo[1]].text == self.buttons[combo[2]].text != "":
                for i in combo:
                    anim = Animation(background_color=(0, 1, 0, 1), duration=0.3)
                    anim.start(self.buttons[i])
                return True
        return False

    def reset_board(self):
        for btn in self.buttons:
            btn.text = ""
            btn.background_color = (0.1, 0.4, 0.7, 1)
        self.current_player = "X"

    def show_popup(self, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message, font_size=20))
        replay_btn = Button(text="Play Again", size_hint=(1, 0.3), background_color=(0.2, 0.6, 0.8, 1))
        layout.add_widget(replay_btn)
        popup = Popup(title="Game Over", content=layout, size_hint=(0.8,0.5))
        replay_btn.bind(on_press=lambda x: (popup.dismiss(), self.reset_board()))
        popup.open()

class PlayerInput(BoxLayout):
    def __init__(self, start_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(text="Enter Player Names", font_size=24))

        self.player1_input = TextInput(hint_text="Player 1 Name", multiline=False, font_size=18, size_hint=(None, None), height=40, width=200)
        self.player2_input = TextInput(hint_text="Player 2 Name", multiline=False, font_size=18, size_hint=(None, None), height=40, width=200)

        self.ai_checkbox = CheckBox(size_hint=(None, None), size=(30, 30))
        ai_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), height=40)
        ai_box.add_widget(self.ai_checkbox)
        ai_box.add_widget(Label(text="Play with AI", font_size=18, size_hint=(None, None), height=30, width=150))

        # Difficulty checkboxes in one row (center)
        self.difficulty_options = ["Normal", "Hard", "Super Hard"]
        self.difficulty_checkboxes = {}
        diff_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint=(None, None), height=40)
        for level in self.difficulty_options:
            box = BoxLayout(orientation='horizontal', spacing=4, size_hint=(None, None), width=120)
            cb = CheckBox(group="difficulty")
            self.difficulty_checkboxes[level] = cb
            box.add_widget(cb)
            box.add_widget(Label(text=level, font_size=16))
            diff_layout.add_widget(box)

        self.add_widget(self.player1_input)
        self.add_widget(self.player2_input)
        self.add_widget(ai_box)
        self.add_widget(Label(text="AI Difficulty:", font_size=18))
        self.add_widget(diff_layout)

        start_btn = Button(text="Start Game", size_hint=(None, None), height=45, width=200, background_color=(0.2, 0.7, 0.4, 1))
        start_btn.bind(on_press=lambda x: start_callback(self.player1_input.text or "Player 1",
                                                         self.player2_input.text or "Player 2",
                                                         self.ai_checkbox.active,
                                                         self.get_selected_difficulty()))
        self.add_widget(start_btn)

    def get_selected_difficulty(self):
        for level, cb in self.difficulty_checkboxes.items():
            if cb.active:
                return level
        return "Normal"

class TicTacToeApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation="vertical")
        self.score_bar = BoxLayout(size_hint=(1, 0.1), padding=10)
        self.score_label = Label(text="Welcome to Tic-Tac-Toe!", font_size=22, bold=True, color=(1,1,1,1))
        self.score_bar.add_widget(self.score_label)
        with self.score_bar.canvas.before:
            Color(0.1, 0.3, 0.5, 1)
            self.bar_bg = Rectangle(size=self.score_bar.size, pos=self.score_bar.pos)
        self.score_bar.bind(size=self.update_bar, pos=self.update_bar)

        self.input_screen = PlayerInput(self.start_game)
        self.root_layout.add_widget(self.score_bar)
        self.root_layout.add_widget(self.input_screen)
        return self.root_layout

    def update_bar(self, *args):
        self.bar_bg.size = self.score_bar.size
        self.bar_bg.pos = self.score_bar.pos

    def update_score_label(self):
        self.score_label.text = f"{self.game.player_names['X']} (X): {self.game.scores['X']}  |  {self.game.player_names['O']} (O): {self.game.scores['O']}"

    def start_game(self, p1, p2, ai_mode, ai_level):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.score_bar)
        self.game = TicTacToe(p1, p2 if not ai_mode else "AI", ai_mode=ai_mode, ai_level=ai_level, back_callback=self.show_menu)
        self.root_layout.add_widget(self.game)
        self.update_score_label()

    def show_menu(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.score_bar)
        self.input_screen = PlayerInput(self.start_game)
        self.root_layout.add_widget(self.input_screen)
        self.score_label.text = "Welcome to Tic-Tac-Toe!"

if __name__ == "__main__":
    TicTacToeApp().run()
