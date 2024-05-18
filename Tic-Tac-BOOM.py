import tkinter as tk
from tkinter import PhotoImage
import random

# Places a bomb in one of the 3x3 grid cells
def place_bomb():
    global bomb_count, bomb_row, bomb_column, bomb_touched, player
    if bomb_count == 0 and bomb_touched == 0 and not check_winner():
        # Randomly selects a row and column to place the bomb 
        bomb_row = random.randint(0, 2)
        bomb_column = random.randint(0, 2)

        # Ensures the bomb is placed on an empty cell 
        while buttons[bomb_row][bomb_column]['text'] != " ":
            bomb_row = random.randint(0, 2)
            bomb_column = random.randint(0, 2)
        
        # Sets the button text to "Bomb", and make it invisible by matching text color with bg color
        buttons[bomb_row][bomb_column]['text'] = "Bomb"
        buttons[bomb_row][bomb_column].config(fg=default_grid_color)
        
        # Changes bomb count to 1 to indicate a bomb has been placed 
        bomb_count = 1 
        
        # Records the move for the undo button
        moves.append((bomb_row, bomb_column))  

        # Switches turn to the next player
        player = players[1] if player == players[0] else players[0]
        label_turn.config(text=player+"'s turn")
        change_bg()


# Checks if there is a winner 
def check_winner():
    # Checks if there are 3 matching symbols in a row   
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != " ": 
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    # Checks if there are 3 matching symbols in a column
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != " ":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    # Checks for 3 matching symbols in a diagonal
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != " ":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != " ":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True
    
    # Checks if the game is a tie [No bombs placed and No empty cells]
    elif bomb_count == 0 and not empty_space():
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "TIE"

    # No winner or tie
    else:
        return False

# Ends the game and displays the result
def end_game(result):
    global player_scores, bomb_count, bomb_row, bomb_column, bomb_touched

    # Tie condition
    if result == "TIE":
        for row in range(3):
            for column in range(3):
                if buttons[row][column]['text'] == " ":
                    buttons[row][column].config(bg="yellow")          
        label.config(text="TIE!", bg="yellow")
    else:
        # Bomb Touched Condition
        if bomb_touched == 1:
            enemy = players[1] if player == players[0] else players[0]
            label.config(text=enemy + " Wins")
            player_scores[enemy] += 1  
            update_scoreboard()
            label.config(fg = "yellow", bg = "black")  
        
        # Normal win / 3 matching symbols Condition
        else:
            label.config(text=player + " Wins")
            player_scores[player] += 1 
            update_scoreboard()
            if player == players[0]:
                label.config(bg = "#00DEDE")  
            elif player == players[1]:
                label.config(bg = "red")  

    # Resets bomb location
    bomb_row = None
    bomb_column = None


# Updates the scoreboard
def update_scoreboard():
    scoreboard_label.config(text="Scoreboard:\n" + players[0] + ": " + str(player_scores[players[0]]) + "\n" + players[1] + ": " + str(player_scores[players[1]]))

# Proceeds to next turn 
def next_turn(row, column):
    global player, bomb_touched

    # If a bomb was planted, check if the player touched it
    if bomb_count == 1 and bomb_touched == 0 and not check_winner():
        if buttons[row][column]['text'] == "Bomb":
            buttons[row][column].config(bg="black", fg="yellow")
            label_turn.config(text = player + " touched a bomb", bg = "black", fg = "yellow")
            bomb_touched = 1
            end_game("loses")
            return
        
    # Check if the clicked button is empty, and the game is still ongoing.
    if buttons[row][column]['text'] == " " and bomb_touched == 0 and not check_winner():
        # Puts the player's symbol on the clicked button
        if player == players[0]:
            buttons[row][column]['text'] = "X"
            buttons[row][column].config(bg="blue", fg="black")  
        else:
            buttons[row][column]['text'] = "O"
            buttons[row][column].config(bg="red", fg="black")
        
        # Records the player's move for the undo button
        moves.append((row, column)) 
        
        # Checks for a winner after each move
        if check_winner():
            end_game(check_winner())

        else:
            # Switches players and updates the turn label
            player = players[1] if player == players[0] else players[0]
            label_turn.config(text=player + "'s turn")
            change_bg()


# Undo the last move
def undo_move():
    global player, bomb_count, bomb_row, bomb_column, bomb_touched


    # Disables undo button if the game is already finished
    if check_winner() or bomb_touched == 1:
        return
    
    # Undo the last move
    elif moves:
        # Removes the last move from the record
        row, column = moves.pop()
        
        # Checks if the last move was for placing a bomb
        if bomb_count == 1 and (row, column) == (bomb_row, bomb_column):
                #Resets bomb-related variables
                bomb_count = 0
                bomb_row = None
                bomb_column = None
            
        # Resets the button to its original state 
        buttons[row][column]['text'] = " "
        buttons[row][column].config(bg=default_grid_color)  
        
        
        # Switches player 
        player = players[1] if player == players[0] else players[0]
        label_turn.config(text=player + "'s turn")
        
        # Change background image depending on whose player turn it is
        change_bg()


# Checks if there are empty cells left in the 3x3 grid
def empty_space():
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == " ":
                return True
    return False


#Changes text, background, and button colors based on the player's turn
def change_bg():
        if player == players[0]:
            bg_image.config(image=plyr1bg_path)
            welcome_label.config(fg="#000000",bg="#00DEDE")
            label1.config(fg="#000000",bg="#00DEDE")
            label2.config(fg="#000000",bg="#00DEDE")
            start_button.config(fg="#000000",bg="#00DEDE")
            label_turn.config(bg="light blue", fg = "black")
            restart_button.config(fg="#000000",bg="#00DEDE")
            undo_button.config(fg="#000000",bg="#00DEDE")
            bomb_button.config(fg="#000000",bg="#00DEDE")
            scoreboard_label.config(bg="light blue")
            label.config(bg = "light blue")
        
        elif player == players[1]: 
            bg_image.config(image=plyr2bg_path)
            welcome_label.config(fg="#F0F0F0",bg="#7A0000")
            label1.config(fg="#F0F0F0",bg="#7A0000")
            label2.config(fg="#F0F0F0",bg="#7A0000")
            start_button.config(fg="#F0F0F0",bg="#7A0000")
            label_turn.config(bg="red", fg = "black")
            restart_button.config(fg="#F0F0F0",bg="#7A0000")
            undo_button.config(fg="#F0F0F0",bg="#7A0000")
            bomb_button.config(fg="#F0F0F0",bg="#7A0000")
            scoreboard_label.config(bg="red")
            label.config(bg = "red")

# Starts and initializes the game state
def start_game():
    global player, players, player_scores, moves, bomb_count, bomb_touched 

    # Gets players names, removes excess whitespace before and after name
    player1 = entry1.get().strip() 
    player2 = entry2.get().strip()

    # Stops the game from starting if both players have the same names
    if player1 == player2:
        label.config(text="Player names needs to be different!")
        return
    
    #Changes "Start" button text to "Reset"
    start_button.config(text="Reset")
    
    # Initializes Player Scores
    players = [player1, player2]
    player_scores = {player1: 0, player2: 0}
    
    # Determines the Player who goes first
    player = random.choice(players)
    
    # Initializes bomb counter and bomb touched variables
    bomb_count = 0
    bomb_touched = 0

    # Resets the 3x3 grid and Clears the grid of bombs
    for row in range(3):
        for column in range(3):
            buttons[row][column]['text'] = " "
            buttons[row][column].config(bg=default_grid_color)
    
    # Set up the game interface
    label_turn.config(text=player+"'s turn")
    change_bg()
    label.config(text="", fg  = "black")
    # Update and display the scoreboard after initializing players
    update_scoreboard()
    # Initialize moves list for undo button
    moves = []  
    
# Starts a new round of the game
def new_game():
    global player, moves, bomb_count, bomb_touched

    # Determine the player who goes first
    player = random.choice(players)
    label_turn.config(text=player+"'s turn")

    # Clear labels and the 3x3 Grids
    label.config(text="", fg  = "black")
    for row in range(3):
        for column in range(3):
            buttons[row][column]['text'] = " "
            buttons[row][column].config(bg=default_grid_color)
    
    #Clears the move list and resets the bomb counter and bomb touched status
    moves = []
    bomb_count = 0
    bomb_touched = 0

    #Changes background according to whos player turn is it
    change_bg()

# Create Main Application Window
window = tk.Tk()
window.title("Tic-Tac-BOOM")
icon_logo_image=PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Logo.png")
window.iconphoto(False, icon_logo_image)

# Default color for 3x3 grid
default_grid_color = "#F0F0F0"

# Load Background Images
image_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Main Menu.png")
plyr1bg_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Blue.png")
plyr2bg_path = PhotoImage(file=r"C:\Tic-Tac-BOOM Pack\Red.png")


# Set up background image and UI elements
bg_image = tk.Label(window, image=image_path)
bg_image.place(relheight=1, relwidth=1)

welcome_label = tk.Label(window, text="Welcome to Tic-Tac-BOOM!!! Have Fun!", font=('Press Start 2P', 22), bg="#00DEDE") 
welcome_label.pack(side ="top", padx = 9, pady = 10)

label1 = tk.Label(window, text="Enter Player 1 Name: ", font=('Press Start 2P', 18), bg="#00DEDE")
label1.pack(side="top", padx = 9, pady = 10)

entry1 = tk.Entry(window, font=('Pixelmix', 18))
entry1.pack(side="top", padx = 9, pady = 10)

label2 = tk.Label(window, text="Enter Player 2 Name: ", font=('Press Start 2P', 18), bg="#00DEDE")
label2.pack(side="top", padx = 9, pady = 10)

entry2 = tk.Entry(window, font=('Pixelmix', 18))
entry2.pack(side="top", padx = 9, pady = 10)

start_button = tk.Button(window, text="Start Game", font=('Press Start 2P', 15), command=start_game, width=10, bg = "#00DEDE")
start_button.pack(side="top", padx = 9, pady = 10)

label_turn = tk.Label(window, text="", font=('Press Start 2P', 18), bg="light blue")
label_turn.pack(side="top", padx = 9, pady = 10)

restart_button = tk.Button(text="Restart", font=('Press Start 2P', 15), command=new_game, width=10, bg = "#00DEDE")
restart_button.pack(side="top", padx = 9, pady = 10)

undo_button = tk.Button(text="Undo", font=('Press Start 2P', 15), command=undo_move, width=10, bg = "#00DEDE")
undo_button.pack(side="top", padx = 9, pady = 10)

bomb_button = tk.Button(text="Place Bomb", font=('Press Start 2P', 15), command=place_bomb, width=10, bg = "#00DEDE")
bomb_button.pack(side="top", padx = 9, pady = 10)

# Initializes buttons as an empty list
buttons = [] 
# Initializes moves list
moves = []  

# Creates 3 x 3 grid for the game
frame = tk.Frame(window, bg=default_grid_color)
frame.pack(side="top", padx = 9, pady = 10)

for row in range(3):
    # Create a list to hold buttons for this row
    button_row = []
    for column in range(3):
        # Create Button widget and append it to button_row
        button = tk.Button(frame, text=" ", font=('Pixelmix', 12), width=25, height=2, bg=default_grid_color, command=lambda row=row, column=column: next_turn(row, column))
        button.grid(row=row, column=column)
        button_row.append(button) 
    buttons.append(button_row)

label = tk.Label(window, text="", font=('Press Start 2P', 23))
label.pack(side="top", padx = 9, pady = 10)


# Display scoreboard on screen
scoreboard_label = tk.Label(window, text="Scoreboard:", font=('Pixelmix', 11), bg="light blue", width = 20)
scoreboard_label.pack(side="bottom", padx = 9, pady = 10)

window.mainloop()

#Acknowledgements:
#   FONTS:
#       Pixelmix - Andrew Tyler[@andrewtyler.net]
#       Press Start 2P - Cody Boisclair [cody@zone38.net]
#   Images:
#       3157822 - "Designed by Freepik" <a href="http://www.freepik.com">Designed by Freepik</a>
#       3203855 - "Designed by Freepik" <a href="http://www.freepik.com">Designed by Freepik</a>
#   References:
#        Python Tic Tac Toe game tutorial  by Bro Code  https://www.youtube.com/watch?v=V9MbQ2Xl4CE&t=181s