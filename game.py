
import random
import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


class Demineur(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ecran_demarrage = ecranDemarrage(name='intro')
        self.ecran_de_jeu = ecranJeu(name='game')
        self.ecran_des_scores = ecranScore(name='score')

        self.add_widget(self.ecran_demarrage)
        self.add_widget(self.ecran_de_jeu)
        self.add_widget(self.ecran_des_scores)


class ecranDemarrage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.my_root_widget = BoxLayout(spacing=10, padding=100, orientation='vertical')
        self.button_play = Button(text="Jouer")
        self.button_play.bind(on_press=self.demarrer_Jeu)
        self.hauteur_label = Label(text="Hauteur")
        self.largeur_label = Label(text="Largeur")
        self.bombe_compteur_label = Label(text="Nombre de bombes")
        self.hauteur_input = TextInput(text='', multiline=False)
        self.largeur_input = TextInput(text='', multiline=False)
        self.bombs_count_input = TextInput(text='', multiline=False)
        self.my_root_widget.add_widget(self.hauteur_label)
        self.my_root_widget.add_widget(self.hauteur_input)
        self.my_root_widget.add_widget(self.largeur_label)
        self.my_root_widget.add_widget(self.largeur_input)
        self.my_root_widget.add_widget(self.bombe_compteur_label)
        self.my_root_widget.add_widget(self.bombs_count_input)
        self.my_root_widget.add_widget(self.button_play)
        self.add_widget(self.my_root_widget)

    def demarrer_Jeu(self, _):
        length = self.hauteur_input.text
        width = self.largeur_input.text
        bombs_count = self.bombs_count_input.text
        if not length.isnumeric() or not width.isnumeric() or not bombs_count.isnumeric() \
                or int(length) <= 0 or int(width) <= 0 or int(bombs_count) <= 0:
            return
        length = int(length)
        width = int(width)
        bombs_count = int(bombs_count)
        ecran_de_jeu_name = 'game'
        ecran_de_jeu = self.manager.get_screen(ecran_de_jeu_name)
        ecran_de_jeu.init(length, width, bombs_count)
        self.manager.current = ecran_de_jeu_name


class ecranJeu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.my_root_widget = None
        self.tile_list = None
        self.rows = None
        self.cols = None
        self.remaining_tiles_count = None
        self.bombs_count = None
        self.game_started = False
        self.start_time = None

    def init(self, length, width, bombs_count):
        self.rows = length
        self.cols = width
        self.remaining_tiles_count = self.cols * self.rows
        self.my_root_widget = GridLayout(cols=self.cols, rows=self.rows)
        # generer la position des bombes aléatoire
        self.bombs_count = bombs_count
        bombs = list(range(self.cols * self.rows))
        random.shuffle(bombs)
        bombs = bombs[:self.bombs_count]
        self.tile_list = [Tile(self, i) for i in range(self.cols * self.rows)]
        for bomb_index in bombs:
            self.tile_list[bomb_index].set_bomb()
            left, right, top, bottom = bomb_index-1, bomb_index+1, bomb_index-self.cols, bomb_index+self.cols
            if top >= 0:
                self.tile_list[top].number += 1
            if bottom <= len(self.tile_list) - 1:
                self.tile_list[bottom].number += 1
            if left >= 0 and left % self.cols != self.cols - 1:
                self.tile_list[left].number += 1
            if right <= len(self.tile_list) - 1 and right % self.cols != 0:
                self.tile_list[right].number += 1
        for tile in self.tile_list:
            self.my_root_widget.add_widget(tile)
        self.add_widget(self.my_root_widget)

    def on_press_callback(self, index):
        ecran_des_scores_name = 'score'
        # demarer le timer
        if not self.game_started:
            self.start_time = time.time()
            self.game_started = True

        if self.tile_list[index].is_bomb():
            # joueur perdant
            ecran_de_jeu = self.manager.get_screen(ecran_des_scores_name)
            ecran_de_jeu.init_lost_screen(int(time.time() - self.start_time))
            self.manager.current = ecran_des_scores_name
        else:
            self.expand(self.tile_list[index], root=True)
            if self.remaining_tiles_count == self.bombs_count:
                # joueur gagnant
                ecran_de_jeu = self.manager.get_screen(ecran_des_scores_name)
                ecran_de_jeu.init_win_screen(int(time.time() - self.start_time))
                self.manager.current = ecran_des_scores_name

    def expand(self, tile, root=False):
        if tile.is_visited():
            return
        elif tile.is_neighbour() and not root:
            tile.show_number()
            tile.set_visited()
            self.remaining_tiles_count -= 1
            return
        else:
            tile.show_number()
            tile.set_visited()
            self.remaining_tiles_count -= 1
            index = tile.get_tile_index()
            left, right, top, bottom = index-1, index+1, index-self.cols, index+self.cols
            if top >= 0 and not self.tile_list[top].is_bomb():
                self.expand(self.tile_list[top])
            if bottom <= len(self.tile_list) - 1 and not self.tile_list[bottom].is_bomb():
                self.expand(self.tile_list[bottom])
            if left >= 0 and left % self.cols != self.cols - 1 and not self.tile_list[left].is_bomb():
                self.expand(self.tile_list[left])
            if right <= len(self.tile_list) - 1 and right % self.cols != 0 and not self.tile_list[right].is_bomb():
                self.expand(self.tile_list[right])


class Tile(Button):
    def __init__(self, game, index, is_bomb_flag=False, number=0, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.tile_index = index
        self.is_bomb_flag = is_bomb_flag
        self.number = number
        self.text = ''
        self.visited = False

    def set_bomb(self):
        self.is_bomb_flag = True

    def is_bomb(self):
        return self.is_bomb_flag

    def on_press(self):
        self.game.on_press_callback(self.tile_index)

    def get_tile_index(self):
        return self.tile_index

    def show_number(self):
        self.text = '' if self.number == 0 else str(self.number)
        self.disabled = True

    def is_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True

    def is_neighbour(self):
        return True if self.number > 0 else False


class ecranScore(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def init_lost_screen(self, score):
        my_root_layout = BoxLayout(spacing=10, padding=200, orientation='vertical')
        my_root_layout.add_widget(Label(text="Vous avez Perdu"))
        my_root_layout.add_widget(Label(text="Votre score " + str(score) + " clic(s)"))
        button = Button(text='Rejouer')
        #button.bind(on_press=MineSweeperApp())
        my_root_layout.add_widget(button)
        self.add_widget(my_root_layout)

    def init_win_screen(self, score):
        my_root_layout = BoxLayout(spacing=10, padding=200, orientation='vertical')
        my_root_layout.add_widget(Label(text="Félicitation"))
        my_root_layout.add_widget(Label(text="Vous avez terminer en " + str(score) + " clic(s)"))
        button = Button(text='Rejouer')
        #button.bind(on_press=MineSweeperApp())
        my_root_layout.add_widget(button)
        self.add_widget(my_root_layout)



class MineSweeperApp(App):
    def build(self):
        return Demineur()


if __name__ == '__main__':
    MineSweeperApp().run()
