import pygame
import sys
import os
import threading
import time
import requests
import subprocess
import tkinter as tk
from functools import partial
from config.socket_client import sio, game_handler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from pieces import King
from config.matchmaking import SERVER_URL

BOARD_WIDTH = 640
SIDE_PANEL = 100
WIDTH = BOARD_WIDTH + 2 * SIDE_PANEL
HEIGHT = 700
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS
BOARD_TOP = 30

WHITE = (245, 245, 245)
LIGHT_GRAY = (220, 220, 220)
GRAY = (100, 100, 100)
DARK = (50, 50, 50)
HIGHLIGHT = (106, 168, 79)
SELECTED = (255, 255, 0)
TARGET = (255, 0, 0)

IMAGES = {}

def load_images():
    pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for piece in pieces:
            path = f"assets/{color}_{piece}.png"
            IMAGES[f"{color}_{piece}"] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(win):
    pygame.draw.rect(win, LIGHT_GRAY, (0, 0, SIDE_PANEL, HEIGHT))
    pygame.draw.rect(win, LIGHT_GRAY, (WIDTH - SIDE_PANEL, 0, SIDE_PANEL, HEIGHT))

    for row in range(ROWS):
        for col in range(COLS):
            color = GRAY if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(win, color, (
                SIDE_PANEL + col * SQUARE_SIZE,
                BOARD_TOP + row * SQUARE_SIZE,
                SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board, player_color):
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = row if player_color == "white" else ROWS - 1 - row
            draw_col = col if player_color == "white" else COLS - 1 - col
            piece = board.get_piece(draw_row, draw_col)
            if piece:
                name = piece.__class__.__name__.lower()
                key = f"{piece.color}_{name}"
                x = SIDE_PANEL + col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                win.blit(IMAGES[key], (x, BOARD_TOP + y))

def draw_users(win, white_time, black_time, player_color, white_name="White", black_name="Black"):
    font = pygame.font.SysFont("arial", 20, True)

    w_min, w_sec = divmod(int(white_time), 60)
    b_min, b_sec = divmod(int(black_time), 60)

    white_label = font.render(f"{white_name}", True, (255, 255, 255))
    black_label = font.render(f"{black_name}", True, (255, 255, 255))

    white_time_label = font.render(f"{w_min:02}:{w_sec:02}", True, (255, 255, 255))
    black_time_label = font.render(f"{b_min:02}:{b_sec:02}", True, (255, 255, 255))

    pygame.draw.rect(win, (30, 30, 30), (0, 0, WIDTH, 30))
    pygame.draw.rect(win, (30, 30, 30), (0, HEIGHT - 30, WIDTH, 30))

    if player_color == "white":
        win.blit(black_label, (10, 5))
        win.blit(black_time_label, (WIDTH - 70, 5))
        win.blit(white_label, (10, HEIGHT - 25))
        win.blit(white_time_label, (WIDTH - 70, HEIGHT - 25))
    else:
        win.blit(white_label, (10, 5))
        win.blit(white_time_label, (WIDTH - 70, 5))
        win.blit(black_label, (10, HEIGHT - 25))
        win.blit(black_time_label, (WIDTH - 70, HEIGHT - 25))

def highlight_squares(win, selected_square, moves, player_color):
    if selected_square:
        row, col = selected_square
        draw_row = row if player_color == "white" else ROWS - 1 - row
        draw_col = col if player_color == "white" else COLS - 1 - col
        pygame.draw.rect(win, SELECTED, (
            SIDE_PANEL + draw_col * SQUARE_SIZE,
            BOARD_TOP + draw_row * SQUARE_SIZE,
            SQUARE_SIZE, SQUARE_SIZE), 4)

    for row, col in moves:
        draw_row = row if player_color == "white" else ROWS - 1 - row
        draw_col = col if player_color == "white" else COLS - 1 - col
        pygame.draw.circle(win, TARGET, (
            SIDE_PANEL + draw_col * SQUARE_SIZE + SQUARE_SIZE // 2,
            BOARD_TOP + draw_row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

def ask_promotion_gui(color):
    choice = []
    root = tk.Tk()
    root.title("Choisir une pièce pour la promotion")
    root.geometry("300x80")

    def choose(piece):
        choice.append(piece)
        root.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    for piece in ["queen", "rook", "bishop", "knight"]:
        icon_path = os.path.join("assets", f"{color}_{piece}.png")
        image = tk.PhotoImage(file=icon_path).subsample(2, 2)
        button = tk.Button(frame, image=image, command=partial(choose, piece))
        button.image = image
        button.pack(side=tk.LEFT, padx=5)

    root.mainloop()
    return choice[0] if choice else "queen"

def display_winner(win, winner):
    font = pygame.font.SysFont("arial", 32, True)
    text = f"Échec et mat : {winner} gagne !" if winner in ["white", "black"] else "Match nul !"
    label = font.render(text, True, (255, 0, 0))
    win.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(4000)

def draw_timers(win, font, white_time, black_time, usernames):
    white_label = usernames.get("white", "Invité")
    black_label = usernames.get("black", "Invité")

    wt_min, wt_sec = divmod(int(white_time), 60)
    bt_min, bt_sec = divmod(int(black_time), 60)

    white_text = font.render(f"{white_label}: {wt_min:02}:{wt_sec:02}", True, (0, 0, 0))
    black_text = font.render(f"{black_label}: {bt_min:02}:{bt_sec:02}", True, (0, 0, 0))

    win.blit(white_text, (20, 10))  # timer du joueur en bas à gauche
    win.blit(black_text, (WIDTH - black_text.get_width() - 20, 10))  # timer du joueur en haut à droite


def draw_captured_pieces(win, gs):
    spacing = 36
    icon_size = 32
    y_start = 80

    for i, piece in enumerate(gs.captured["black"]):
        img = IMAGES.get(f"black_{piece}")
        if img:
            scaled = pygame.transform.scale(img, (icon_size, icon_size))
            win.blit(scaled, (WIDTH - SIDE_PANEL + 10, y_start + i * spacing))

    for i, piece in enumerate(gs.captured["white"]):
        img = IMAGES.get(f"white_{piece}")
        if img:
            scaled = pygame.transform.scale(img, (icon_size, icon_size))
            win.blit(scaled, (10, y_start + i * spacing))

def show_end_window(winner, player_color, playerId):
    import tkinter as tk
    import requests

    root = tk.Tk()
    root.title("Fin de partie")

    window_width = 350
    window_height = 180

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#2c3e50")

    if winner == "draw":
        result = "Match nul"
    elif winner == player_color:
        result = "Victoire !"
    else:
        result = "Défaite..."

    elo_msg = ""
    if playerId:
        try:
            res = requests.get(f"{SERVER_URL}/api/user/{playerId}")
            if res.status_code == 200:
                data = res.json()
                elo_msg = f"Votre nouvel ELO : {data['elo']}"
        except:
            elo_msg = ""

    tk.Label(root, text=result, font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
    tk.Label(root, text=elo_msg, font=("Helvetica", 12), bg="#2c3e50", fg="white").pack(pady=5)

    def restart():
        root.destroy()
        pygame.quit()
        subprocess.Popen([sys.executable, "-m", "main"])
        sys.exit()

    def quit_all():
        root.destroy()
        pygame.quit()
        sys.exit()

    tk.Button(root, text="Rejouer", command=restart, bg="#27ae60", fg="white", font=("Helvetica", 12)).pack(pady=5)
    tk.Button(root, text="Quitter", command=quit_all, bg="#c0392b", fg="white", font=("Helvetica", 12)).pack(pady=5)

    root.mainloop()

def main(color="white"):
    global gs, is_my_turn
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu d'échecs")

    pygame.mixer.init()
    sound_move = pygame.mixer.Sound("assets/sounds/move-self.wav")
    sound_move_opponent = pygame.mixer.Sound("assets/sounds/move-opponent.wav")
    sound_capture = pygame.mixer.Sound("assets/sounds/capture.wav")
    sound_check = pygame.mixer.Sound("assets/sounds/move-check.wav")
    sound_castle = pygame.mixer.Sound("assets/sounds/castle.wav")
    sound_promote = pygame.mixer.Sound("assets/sounds/promote.wav")
    sound_game_start = pygame.mixer.Sound("assets/sounds/game-start.wav")
    sound_game_end = pygame.mixer.Sound("assets/sounds/game-end.wav")

    sound_game_start.play()

    load_images()
    clock = pygame.time.Clock()
    gs = GameState()
    selected_square = None
    valid_moves = []
    player_color = color
    is_my_turn = (color == "white")

    gameId = sys.argv[2] if len(sys.argv) > 2 else ""
    playerId = sys.argv[3] if len(sys.argv) > 3 else ""

    white_name = "White"
    black_name = "Black"

    if len(sys.argv) >= 7:
        my_name = sys.argv[4]
        my_elo = sys.argv[5]
        opponent_info = sys.argv[6]

        full_name = f"{my_name} ({my_elo})"
        if color == "white":
            white_name = full_name
            black_name = opponent_info
        else:
            white_name = opponent_info
            black_name = full_name

    white_time = 600
    black_time = 600

    running = True

    def sync_timer_loop():
        nonlocal white_time, black_time, running
        while running:
            try:
                response = requests.get(f"{SERVER_URL}/api/game_time/{gameId}/{player_color}")
                if response.status_code == 200:
                    data = response.json()
                    white_time = data["white"]
                    black_time = data["black"]
            except Exception as e:
                print(f"[ERROR] timer sync: {e}")
            time.sleep(1)

    threading.Thread(target=sync_timer_loop, daemon=True).start()

    from config.socket_client import sio
    sio.emit("register_socket", {
        "gameId": gameId,
        "playerColor": color
    })

    def handle_opponent_move(data):
        start = tuple(data["start"])
        end = tuple(data["end"])

        target_piece = gs.board.get_piece(*end)
        moving_piece = gs.board.get_piece(*start)

        moved, promotion_pos = gs.play_move(start, end)

        if moved:
            if data.get("promotion"):
                gs.promote_pawn(end, data["promotion"])

            if gs.board.is_in_check(player_color):
                sound_check.play()
            elif data.get("promotion"):
                sound_promote.play()
            elif data.get("is_castling") and isinstance(moving_piece, King):
                sound_castle.play()
            elif target_piece:
                sound_capture.play()
            else:
                sound_move_opponent.play()

        globals().__setitem__('is_my_turn', True)

    game_handler["on_opponent_move"] = handle_opponent_move


    while running:
        pygame.display.set_caption(f"{'À VOUS DE JOUER' if is_my_turn else 'Attente adversaire'} ({player_color})")
        clock.tick(60)
        draw_board(win)
        draw_pieces(win, gs.board, player_color)
        draw_captured_pieces(win, gs)
        highlight_squares(win, selected_square, valid_moves, player_color)
        draw_users(win, white_time, black_time, player_color, white_name, black_name)
        pygame.display.flip()

        if gs.is_game_over():
            sound_game_end.play()
            display_winner(win, gs.winner)
            sio.emit("end_game", {
                "gameId": gameId,
                "winner": gs.winner
            })
            show_end_window(gs.winner, player_color, playerId)
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and is_my_turn:
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pos

                if mouse_y < BOARD_TOP or mouse_x < SIDE_PANEL or mouse_x > SIDE_PANEL + BOARD_WIDTH:
                    continue

                row = (mouse_y - BOARD_TOP) // SQUARE_SIZE
                col = (mouse_x - SIDE_PANEL) // SQUARE_SIZE

                if row < 0 or row >= 8 or col < 0 or col >= 8:
                    continue

                actual_row = row if player_color == "white" else ROWS - 1 - row
                actual_col = col if player_color == "white" else COLS - 1 - col

                if selected_square:
                    target_piece = gs.board.get_piece(actual_row, actual_col)
                    moving_piece = gs.board.get_piece(*selected_square)

                    moved, promotion_pos = gs.play_move(selected_square, (actual_row, actual_col))

                    if moved:
                        promotion_choice = None
                        if promotion_pos:
                            promotion_choice = ask_promotion_gui(gs.board.get_piece(*promotion_pos).color)
                            gs.promote_pawn(promotion_pos, promotion_choice)

                        enemy_color = "black" if player_color == "white" else "white"
                        if gs.board.is_in_check(enemy_color):
                            sound_check.play()
                        elif promotion_pos:
                            sound_promote.play()
                        elif isinstance(moving_piece, King) and abs(selected_square[1] - actual_col) == 2:
                            sound_castle.play()
                        elif target_piece:
                            sound_capture.play()
                        else:
                            sound_move.play()

                        is_castling = isinstance(moving_piece, King) and abs(selected_square[1] - actual_col) == 2
                        is_my_turn = False
                        
                        sio.emit("move", {
                            "start": selected_square,
                            "end": (actual_row, actual_col),
                            "gameId": gameId,
                            "playerId": playerId,
                            "promotion": promotion_choice,
                            "is_castling": is_castling
                        })

                    selected_square = None
                    valid_moves = []
                    if not moved:
                        piece = gs.board.get_piece(actual_row, actual_col)
                        if piece and piece.color == gs.current_turn:
                            selected_square = (actual_row, actual_col)
                            valid_moves = gs.get_valid_moves(actual_row, actual_col)
                else:
                    piece = gs.board.get_piece(actual_row, actual_col)
                    if piece and piece.color == gs.current_turn:
                        selected_square = (actual_row, actual_col)
                        valid_moves = gs.get_valid_moves(actual_row, actual_col)

    pygame.quit()

if __name__ == "__main__":
    color = sys.argv[1] if len(sys.argv) > 1 else "white"
    main(color)