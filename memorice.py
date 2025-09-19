import tkinter as tk
from tkinter import ttk
import random
import time

class Memorygame: 
    def __init__(self, master):
        self.master = master
        self.master.title("Memorice")
        self.master.geometry("900x700")
        self.master.configure(bg="#1a1a2e")
        #Timer
        self.timer_running = False
        self.start_time = None

        self.custom_font = ("Helvetica", 14, "bold") #defineción de fuente personalizada

        #Definición de colores de la interfaz
        self.colors = {
            'bg': "#1a1a2e",
            'sidebar_bg': "#16213e",
            'card_bg': "#0f3469",
            'card_fg': "#e94560",
            'text': "#ffffff",
            'button_bg': "#4caf50",
            'button_fg': "#ffffff",
            'combobox_bg': "#32734b",
            'combobox_fg': "#ffffff",
            'gameover_bg': "#0f3460",
        }

        #Definición de niveles de dificultad
        self.difficulty_levels = {
            'Estandar': {"grid": (6, 6), "symbols": ['🍎', '🍌', '🍇', '🍉', '🍓', '🍒', '🥝', '🍍', '🥥', '🍑', '🍋', '🍊', '🥭', '🍐', '🍏', '🥑', '🥕', '🌽']} #Tablero de 6x6 con 16 parejas de símbolos
        }

        self.current_difficulty = "Estandar"
        self.revealed = [] #Lista para almacenar las cartas reveladas
        self.matched_pairs = 0 #Contador de parejas encontradas
        self.matched_cards = [] #Lista para almacenar las cartas que ya han sido emparejadas
        self.moves = 0 #Contador de movimientos realizados
        self.start_time = None #Variable para almacenar el tiempo de inicio del juego
        self.game_solved = False #Variable para indicar si el juego ha sido resuelto

        self.input_locked = False #Variable para bloquear la entrada mientras se muestran las cartas
        self.pending_after = []

        self.create_widgets() #Llama al método para crear los widgets de la interfaz
        self.create_game_grid() #Llama al método para crear el grid del juego

    def create_widgets(self):
        #Marco principal
        self.main_frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        #Barra lateral
        self.sidebar = tk.Frame(self.main_frame, bg=self.colors['sidebar_bg'], width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        #Frame para el grid del juego
        self.game_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_sidebar()

    def create_sidebar(self):
        title_label = tk.Label(self.sidebar, text="Memorice", font=("Helvetica", 24, "bold"), bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        title_label.pack(pady=(30, 10))

        subtitle_label = tk.Label(self.sidebar, text = "Encuentra las parejas!", font=("Helvetica", 16, "italic"), bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        subtitle_label.pack(pady=(0, 30))

        self.IA_label = tk.Label(self.sidebar, text="Seleccion de IA", font=self.custom_font, bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.IA_label.pack(pady=(0, 5))

        '''self.style = ttk.Style()
        self.style.theme_create("modern", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": self.colors['combobox_bg'],
                    "fieldbackground": self.colors['combobox_bg'],    #COMBOBOX SELECTOR DE IA
                    "background": self.colors['button_bg'],
                    "foreground": self.colors['combobox_fg'],
                }
            }
        })

        self.style.theme_use("modern")
        
        self.difficulty_combobox = ttk.Combobox(self.sidebar, values=list(self.difficulty_levels.keys()), state="readonly", font=self.custom_font, width=10)

        self.difficulty_combobox.set(self.current_difficulty)
        self.difficulty_combobox.pack(pady=(0, 20))'''

        #numero de movimientos y tiempo
        self.moves_label = tk.Label(self.sidebar, text = "Movimientos: 0", font=self.custom_font, bg = self.colors['sidebar_bg'], fg=self.colors['text'])
        self.moves_label.pack(pady=10)

        self.time_label = tk.Label(self.sidebar, text="Tiempo: 00:00", font = self.custom_font, bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.time_label.pack(pady=10)

        #Botón para iniciar un nuevo juego
        self.new_game_button = tk.Button(self.sidebar, text="Nuevo juego", font=self.custom_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], relief=tk.FLAT, command=self.new_game)
        self.new_game_button.pack(pady=30)

        #Efecto hover para el botón
        self.new_game_button.bind("<Enter>", lambda e: e.widget.config(bg="#377038"))
        self.new_game_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))


    def create_game_grid(self):
        #crear el grid del juego
        self.cards_frame = tk.Frame(self.game_frame, bg=self.colors['bg'])
        self.cards_frame.pack(expand=True)

        #crea el grid y los pares de símbolos
        self.cards = []
        rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"] * 2 #duplica los símbolos para crear parejas
        random.shuffle(symbols)
        self.symbols = symbols

        #crea las cartas en el grid
        for i in range(rows):
            for j in range(cols):
                card_idx = i*cols+j
                card = tk.Canvas(self.cards_frame, width=80, height=100, bg=self.colors['card_bg'], highlightthickness=0)
                card.grid(row=i, column=j, padx=5, pady=5)
                card.bind("<Button-1>", lambda e, idx=card_idx: self.on_card_click(idx))
                card.create_rectangle(5, 5, 75, 95, fill=self.colors['card_bg'], outline=self.colors['card_fg'], width=2)
                card.create_text(40, 50, text="?", font=("Helvetica", 24, "bold"), fill=self.colors['card_fg'])
                card.create_rectangle(5, 5, 75, 95, fill=self.colors['card_bg'], width=2, state='hidden', tags=('front',))
                card.create_text(40, 50, text=self.symbols[card_idx], font=("Helvetica", 24, "bold"), fill=self.colors['card_fg'], state='hidden', tags=('symbol',))
                self.cards.append(card)

    # Método que se ejecuta al hacer clic en una carta
    def on_card_click(self, idx):
        if self.input_locked or idx in self.matched_cards or idx in self.revealed or len(self.revealed) >=2:
            return

        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.tick_timer()

        self.reveal_card(idx)
        self.revealed.append(idx)
        if len(self.revealed) == 2:
            self.input_locked = True
            self.moves += 1
            self.moves_label.config(text=f"Movimientos: {self.moves}")
            after_id = self.master.after(500, self.check_match)
            self.pending_after.append(after_id)

    def tick_timer(self):
        if not self.timer_running or self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        mm, ss = divmod(elapsed, 60)
        self.time_label.config(text=f"Tiempo: {mm:02d}:{ss:02d}")
        self.master.after(1000, self.tick_timer)

    # Método para revelar las cartas
    def reveal_card(self, idx):
        card = self.cards[idx]
        card.itemconfig('front', state='normal')
        card.itemconfig('symbol', state='normal')
        card.tag_raise('symbol')

    # Método para ocultar las cartas
    def hide_card(self, idx):
        card = self.cards[idx]
        card.itemconfig('front', state='hidden')
        card.itemconfig('symbol', state='hidden')

    def check_match(self):
        if len(self.revealed) < 2:
            self.input_locked = False
            return
        idx1, idx2 = self.revealed #Obtiene los índices de las cartas reveladas
        if self.symbols[idx1] == self.symbols[idx2]:
            self.matched_pairs += 1
            self.matched_cards.extend([idx1, idx2])
            for idx in [idx1, idx2]:
                card = self.cards[idx]
                card.itemconfig('front', fill="#8bc34a")
        else:
            self.hide_card(idx1)
            self.hide_card(idx2)
        del self.revealed[:2]
        self.input_locked = False
        self.check_win()

    def check_win(self):
        total_pairs = len(self.symbols) // 2
        if self.matched_pairs == total_pairs:
            self.timer_running = False
            self.show_game_over()

    def show_game_over(self):
        overlay = tk.Toplevel(self.master)
        overlay.title("Juego Terminado!")
        overlay.configure(bg=self.colors['gameover_bg'])
        overlay.transient(self.master)
        overlay.grab_set()

        if self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            mm, ss = divmod(elapsed, 60)
            final_time = f"{mm:02d}:{ss:02d}"
        else:
            final_time = "00:00"

        tk.Label(overlay, text="Juego Terminado!", font =("Helvetica", 20, "bold"), bg=self.colors['gameover_bg'], fg=self.colors['text']).pack(padx=20, pady=(20, 10))
        tk.Label(overlay, text=f"Movimientos: {self.moves}\nTiempo: {final_time}", font=self.custom_font, bg=self.colors['gameover_bg'], fg=self.colors['text']).pack(pady=5)

    # Método para iniciar un nuevo juego
    def new_game(self):

        for aid in self.pending_after:
            try:
                self.master.after_cancel(aid)
            except Exception:
                pass
        self.pending_after.clear()

        self.game_solved = False
        self.revealed.clear()
        self.matched_cards.clear()
        self.matched_pairs = 0
        self.moves = 0
        self.start_time = None
        self.moves_label.config(text="Movimientos: 0")
        self.time_label.config(text="Tiempo: 00:00")
        self.cards_frame.destroy()
        self.create_game_grid()


if __name__ == "__main__":
    root = tk.Tk() #Crea la ventana principal
    game = Memorygame(root) #Crea una instancia del juego
    root.mainloop() #Inicia el bucle principal de la interfaz gráfica

