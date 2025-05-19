
import pygame
import sys
import os
import time
import requests
import threading
import tkinter as tk
from functools import partial
from config.socket_client import sio, game_handler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from config.matchmaking import SERVER_URL

WIDTH, HEIGHT = 640, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (245, 245, 245)
GRAY = (100, 100, 100)
DARK = (50, 50, 50)
HIGHLIGHT = (106, 168, 79)
SELECTED = (255, 255, 0)
TARGET = (255, 0, 0)

# Chargement des images
IMAGES = {}

def load_images():
    pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for piece in pieces:
            path = f"assets/{color}_{piece}.png"
            IMAGES[f"{color}_{piece}"] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = GRAY if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(
                win, color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE + 30, SQUARE_SIZE, SQUARE_SIZE)
            )


def draw_pieces(win, board, player_color):
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = row if player_color == "white" else ROWS - 1 - row
            draw_col = col if player_color == "white" else COLS - 1 - col
            piece = board.get_piece(draw_row, draw_col)
            if piece:
                name = piece.__class__.__name__.lower()
                key = f"{piece.color}_{name}"
                win.blit(IMAGES[key], (col * SQUARE_SIZE, row * SQUARE_SIZE + 30))

def draw_timers(win, white_time, black_time, player_color):
        font = pygame.font.SysFont("arial", 20, True)
        w_min, w_sec = divmod(int(white_time), 60)
        b_min, b_sec = divmod(int(black_time), 60)

        white_text = f"Blanc: {w_min:02}:{w_sec:02}"
        black_text = f"Noir : {b_min:02}:{b_sec:02}"

        white_label = font.render(white_text, True, (255, 255, 255))
        black_label = font.render(black_text, True, (255, 255, 255))

        pygame.draw.rect(win, (30, 30, 30), (0, 0, WIDTH, 30))
        pygame.draw.rect(win, (30, 30, 30), (0, HEIGHT - 30, WIDTH, 30))

        if player_color == "white":
            win.blit(white_label, (10, HEIGHT - 25))
            win.blit(black_label, (10, 5))
        else:
            win.blit(black_label, (10, HEIGHT - 25))
            win.blit(white_label, (10, 5))

def highlight_squares(win, selected_square, moves, player_color):
    if selected_square:
        row, col = selected_square
        draw_row = row if player_color == "white" else ROWS - 1 - row
        draw_col = col if player_color == "white" else COLS - 1 - col
        pygame.draw.rect(win, SELECTED, (draw_col * SQUARE_SIZE, draw_row * SQUARE_SIZE + 30, SQUARE_SIZE, SQUARE_SIZE), 4)

    for row, col in moves:
        draw_row = row if player_color == "white" else ROWS - 1 - row
        draw_col = col if player_color == "white" else COLS - 1 - col
        pygame.draw.circle(win, TARGET,
            (draw_col * SQUARE_SIZE + SQUARE_SIZE // 2, draw_row * SQUARE_SIZE + 30 + SQUARE_SIZE // 2), 10)

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

def main(color="white"):
    global gs, is_my_turn
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu d'échecs")

    load_images()
    clock = pygame.time.Clock()
    gs = GameState()
    selected_square = None
    valid_moves = []
    player_color = color
    is_my_turn = (color == "white")

    gameId = sys.argv[2] if len(sys.argv) > 2 else ""
    playerId = sys.argv[3] if len(sys.argv) > 3 else ""

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
        print(f"[DEBUG] Reçu coup de l’adversaire : {data}")
        moved, promotion_pos = gs.play_move(tuple(data["start"]), tuple(data["end"]))

        if data.get("promotion"):
            gs.promote_pawn(tuple(data["end"]), data["promotion"])
            print(f"[PROMOTION] Promotion reçue : {data['promotion']} pour {gs.board.get_piece(*tuple(data['end'])).color}")

        globals().__setitem__('is_my_turn', True)
        print("[DEBUG] C’est à moi de jouer.")

    game_handler["on_opponent_move"] = handle_opponent_move

    while running:
        pygame.display.set_caption(f"{'À VOUS DE JOUER' if is_my_turn else 'Attente adversaire'} ({player_color})")
        clock.tick(60)
        draw_board(win)
        draw_pieces(win, gs.board, player_color)
        highlight_squares(win, selected_square, valid_moves, player_color)
        draw_timers(win, white_time, black_time, player_color)
        pygame.display.flip()

        if gs.is_game_over():
            display_winner(win, gs.winner)
            sio.emit("end_game", {
                "gameId": gameId,
                "winner": gs.winner
            })
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and is_my_turn:
                pos = pygame.mouse.get_pos()
                row = (pos[1] - 30) // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                if row < 0 or row >= 8 or col < 0 or col >= 8:
                    continue
                actual_row = row if player_color == "white" else ROWS - 1 - row
                actual_col = col if player_color == "white" else COLS - 1 - col

                if selected_square:
                    moved, promotion_pos = gs.play_move(selected_square, (actual_row, actual_col))
                    if moved:
                        
                        promotion_choice = None
                        if promotion_pos:
                            promotion_choice = ask_promotion_gui(gs.board.get_piece(*promotion_pos).color)
                            gs.promote_pawn(promotion_pos, promotion_choice)

                        is_my_turn = False
                        
                        sio.emit("move", {
                            "start": selected_square,
                            "end": (actual_row, actual_col),
                            "gameId": gameId,
                            "playerId": playerId,
                            "promotion": promotion_choice
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