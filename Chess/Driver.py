"""
    This is the driver for ChessAI
    It handles the user input, animations
    and displays the current Evaluation
    (GameState object)
"""

import pygame as pyg
import sys
from Chess import Engine, MoveAI, stock
from button import Button  # Assuming you have a Button class implemented

"""
CONSTANTS
"""

board_width = board_height = 512
move_log_panel_width = 256
move_log_panel_height = board_height
dimension = 8
max_fps = 15
squareSize = board_height // dimension
IMAGES = {}

# Initializing Pygame window
pyg.init()
screen = pyg.display.set_mode((768, 512))
clock = pyg.time.Clock()
pyg.display.set_caption("ChessAI")

"""
Helper method to load our images dictionary of pieces
"""


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (squareSize, squareSize))


"""
Helper method to load gamestate and valid moves
"""


def initialize_game():
    gamestate = Engine.GameState()
    validMoves = gamestate.getValidMoves()
    return gamestate, validMoves


"""
Method for displaying the game's current state :p
"""


def drawGameState(screen, gamestate, validMoves, squareSelected, moveLogFont):
    drawBoard(screen)  # draw Squares
    drawPieces(screen, gamestate.board)  # drawing the pieces
    highlightSquares(screen, gamestate, validMoves, squareSelected)
    drawMoveLog(screen, gamestate, moveLogFont)


"""
Method to draw the squares on the board
"""


def drawBoard(screen):
    global colors
    colors = [pyg.Color("white"), pyg.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            pyg.draw.rect(screen, color, pyg.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


"""
Method for square highlighting and moves
"""


def highlightSquares(screen, gamestate, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        if gamestate.board[r][c][0] == ('w' if gamestate.whiteToMove else 'b'):  # square selected is right turn
            s = pyg.Surface((squareSize, squareSize))
            s.set_alpha(50)
            s.fill(pyg.Color('cyan'))
            screen.blit(s, (c * squareSize, r * squareSize))
            # highlight moves available from square
            s.fill(pyg.Color('cyan'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * squareSize, move.endRow * squareSize))


"""
Method to draw pieces on board :o
"""


def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece], pyg.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


"""
Method to draw move logs on screen
"""


def drawMoveLog(screen, gamestate, font):
    moveLogRect = pyg.Rect(board_width, 0, move_log_panel_width, move_log_panel_height)
    pyg.draw.rect(screen, pyg.Color("white"), moveLogRect)
    moveLog = gamestate.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1])
        moveTexts.append(moveString)
    movesPerRow = 3

    padding = 5
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j] + " "
        textObject = font.render(text, 1, pyg.Color("black"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + 15


"""
Method for animating pieces
"""


def animateMove(move, screen, board, clock):
    global colors
    cords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    fps = 10  # frames per square lol
    frameCount = (abs(dR) + abs(dC)) * fps
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # remove piece from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pyg.Rect(move.endCol * squareSize, move.endRow * squareSize, squareSize, squareSize)
        pyg.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "-":
            if move.isEnPassantMove:
                enPassantRow = (move.endRow + 1) if move.piececaptured[0] == 'b' else (move.endRow - 1)
                endSquare = pyg.Rect(move.endCol * squareSize, enPassantRow * squareSize, squareSize, squareSize)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pyg.Rect(c * squareSize, r * squareSize, squareSize, squareSize))
        pyg.display.flip()
        clock.tick(60)


"""
Method to display text when game is over
"""

def drawEndGameText(screen, text):
    font = pyg.font.SysFont('Press Start 2P', 20, False, False)  # Increased font size
    textObject = font.render(text, True, (80, 1, 0))  # White text color
    textRect = textObject.get_rect()
    textRect.center = ((screen.get_width() - 256 )// 2, screen.get_height() // 2)  # Center text on the screen

    # Draw semi-transparent background rectangle behind the text
    bgRect = pyg.Rect(0, 0, textRect.width + 40, textRect.height + 20)  # Adjust size as needed
    bgRect.center = textRect.center
    pyg.draw.rect(screen, (244,244,255, 50), bgRect)  # RGBA color for transparency

    screen.blit(textObject, textRect)




def get_font(size):  # Returns Press-Start-2P in the desired size
    return pyg.font.Font("assets/font.ttf", size)


"""
Method to draw the main menu
"""


def drawMainMenu(screen):
    # Load background image
    background = pyg.image.load("assets/board.jpg")
    screen.blit(background, (0, 0))

    # Menu buttons
    play_button = Button(image=pyg.image.load("assets/Play Rect.png"), pos=(384, 140),
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=pyg.image.load("assets/Quit Rect.png"), pos=(384, 380),
                         text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    # Update and draw buttons
    play_button.changeColor(pyg.mouse.get_pos())
    play_button.update(screen)

    quit_button.changeColor(pyg.mouse.get_pos())
    quit_button.update(screen)

    return play_button, quit_button


"""
Method to draw opponent and difficulty menu
"""


def drawOpponentMenu(screen):
    # Load background image
    background = pyg.image.load("assets/Background.png")
    screen.blit(background, (0, 0))

    # Opponent selection buttons
    human_button = Button(pos=(384, 100), text_input="HUMAN", font=get_font(30), base_color="#d7fcd4",
                          hovering_color="White")
    ai_easy_button = Button(pos=(384, 180), text_input="AI EASY", font=get_font(30), base_color="#d7fcd4",
                            hovering_color="White")
    ai_medium_button = Button(pos=(384, 260), text_input="AI MEDIUM", font=get_font(30), base_color="#d7fcd4",
                              hovering_color="White")
    ai_hard_button = Button(pos=(384, 340), text_input="AI HARD", font=get_font(30), base_color="#d7fcd4",
                            hovering_color="White")
    back_button = Button(pos=(384, 420), text_input="BACK", font=get_font(30), base_color="#d7fcd4",
                         hovering_color="White")

    # Update and draw buttons
    human_button.changeColor(pyg.mouse.get_pos())
    human_button.update(screen)

    ai_easy_button.changeColor(pyg.mouse.get_pos())
    ai_easy_button.update(screen)

    ai_medium_button.changeColor(pyg.mouse.get_pos())
    ai_medium_button.update(screen)

    ai_hard_button.changeColor(pyg.mouse.get_pos())
    ai_hard_button.update(screen)

    back_button.changeColor(pyg.mouse.get_pos())
    back_button.update(screen)
    pyg.display.flip()

    return human_button, ai_easy_button, ai_medium_button, ai_hard_button, back_button


"""
Method to draw Choose Color Menu
"""


def drawColorMenu(screen):
    background = pyg.image.load("assets/bobby.jpg")
    screen.blit(background, (0, 0))

    white_button = Button(image=pyg.image.load("assets/Play Rect.png"), pos=(384, 100),
                          text_input="WHITE", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
    black_button = Button(image=pyg.image.load("assets/Play Rect.png"), pos=(384, 250),
                          text_input="BLACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
    back_button = Button(image=pyg.image.load("assets/Quit Rect.png"), pos=(384, 400),
                         text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

    white_button.changeColor(pyg.mouse.get_pos())
    white_button.update(screen)

    black_button.changeColor(pyg.mouse.get_pos())
    black_button.update(screen)

    back_button.changeColor(pyg.mouse.get_pos())
    back_button.update(screen)

    pyg.display.flip()

    return white_button, black_button, back_button


"""
Method to handle events for which color to play with
"""


def handleColorMenuEvents(white_button, black_button, back_button):
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        elif event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            if white_button.checkForInput(mouse_pos):
                return 'white'
            elif black_button.checkForInput(mouse_pos):
                return 'black'
            elif back_button.checkForInput(mouse_pos):
                return 'back'
    return None


"""
Method to hand main menu events
"""


def handleMainMenuEvents(play_button, quit_button):
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        elif event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            if play_button.checkForInput(mouse_pos):
                return 'play'
            elif quit_button.checkForInput(mouse_pos):
                pyg.quit()
                sys.exit()
    return None


"""
Method to handle opponent options menu
"""


def handleOpponentMenuEvents(human_button, ai_easy_button, ai_medium_button, ai_hard_button, back_button):
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        elif event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            if human_button.checkForInput(mouse_pos):
                return 'human'
            elif ai_easy_button.checkForInput(mouse_pos):
                return 'ai_easy'
            elif ai_medium_button.checkForInput(mouse_pos):
                return 'ai_medium'
            elif ai_hard_button.checkForInput(mouse_pos):
                return 'ai_hard'
            elif back_button.checkForInput(mouse_pos):
                return 'back'
    return None


"""
Method to handle the playing loop
"""


def play_screen(playerOne, playerTwo, ai_level=None):
    pyg.init()
    screen = pyg.display.set_mode((board_width + move_log_panel_width, board_height), pyg.DOUBLEBUF)
    clock = pyg.time.Clock()
    screen.fill(pyg.Color("white"))
    moveLogFont = pyg.font.SysFont('Montserrat', 20, False, False)
    moveMade = False  # check if a move is made
    animate = False  # flag for animation
    loadImages()
    running = True
    squareSelected = ()  # initialize tuple to keep track of selected square
    playerClicks = []  # list of clicked on the two tuples that represent squares clicked on
    gameOver = False  # flag to check if gg
    # playerOne = True  # if human plays W this is true
    # playerTwo = False
    gamestate, validMoves = initialize_game()
    running = True
    while running:
        isHumanTurn = (gamestate.whiteToMove and playerOne) or (not gamestate.whiteToMove and playerTwo)
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                running = False
            # mouse events handling
            elif e.type == pyg.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pyg.mouse.get_pos()  # gets the x,y coordinates of our mouse
                    col = location[0] // squareSize
                    row = location[1] // squareSize
                    if squareSelected == (row, col) or col >= 8:
                        squareSelected = ()  # deselect a square
                        playerClicks = []
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                    if len(playerClicks) == 2 and isHumanTurn:  # checking if the user has clicked for a 2nd time to move a piece
                        move = Engine.Move(playerClicks[0], playerClicks[1], gamestate.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gamestate.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                squareSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [squareSelected]

            elif e.type == pyg.KEYDOWN:
                if e.key == pyg.K_z:
                    gamestate.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == pyg.K_r:  # reset board if r is pressed
                    gamestate = Engine.GameState()
                    validMoves = gamestate.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        # AI MOVES
        if not gameOver and not isHumanTurn:
            if ai_level == 'easy':
                AIMove = MoveAI.findBestMove(gamestate, validMoves)
            elif ai_level == 'medium':
                AIMove = MoveAI.findBestMove2(gamestate, validMoves)
            elif ai_level == 'hard':
                AIMove = stock.findStockfishMove(gamestate, validMoves)
            if AIMove is None:
                AIMove = MoveAI.findRandomMove(validMoves)
            gamestate.makeMove(AIMove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gamestate.moveLog[-1], screen, gamestate.board, clock)
            validMoves = gamestate.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gamestate, validMoves, squareSelected, moveLogFont)

        if gamestate.checkMate or gamestate.staleMate:
            gameOver = True
            drawEndGameText(screen,
                            'Stalemate !' if gamestate.staleMate else 'Black wins!, YOU DIED' if gamestate.whiteToMove else 'White wins!, YOU DIED')
        clock.tick(60)
        pyg.display.flip()


# Main menu loop
def main_menu():
    while True:
        play_button, quit_button = drawMainMenu(screen)
        option = handleMainMenuEvents(play_button, quit_button)
        if option == 'play':
            opponent_selected = False
            while not opponent_selected:
                human_button, ai_easy_button, ai_medium_button, ai_hard_button, back_button = drawOpponentMenu(screen)
                opponent_option = handleOpponentMenuEvents(human_button, ai_easy_button, ai_medium_button,
                                                           ai_hard_button, back_button)
                if opponent_option in ['human', 'ai_easy', 'ai_medium', 'ai_hard']:
                    color_selected = False
                    while not color_selected:
                        white_button, black_button, back_button = drawColorMenu(screen)
                        color_option = handleColorMenuEvents(white_button, black_button, back_button)
                        if color_option == 'white':
                            playerOne = True if opponent_option != 'human' else True
                            playerTwo = False if opponent_option != 'human' else False
                            if opponent_option == 'human':
                                play_screen(playerOne=True, playerTwo=True)
                            elif opponent_option == 'ai_easy':
                                play_screen(playerOne, playerTwo, ai_level='easy')
                            elif opponent_option == 'ai_medium':
                                play_screen(playerOne, playerTwo, ai_level='medium')
                            elif opponent_option == 'ai_hard':
                                play_screen(playerOne, playerTwo, ai_level='hard')
                            color_selected = True
                            opponent_selected = True
                        elif color_option == 'black':
                            playerOne = False if opponent_option != 'human' else False
                            playerTwo = True if opponent_option != 'human' else True
                            if opponent_option == 'human':
                                play_screen(playerOne=True, playerTwo=True)
                            elif opponent_option == 'ai_easy':
                                play_screen(playerOne, playerTwo, ai_level='easy')
                            elif opponent_option == 'ai_medium':
                                play_screen(playerOne, playerTwo, ai_level='medium')
                            elif opponent_option == 'ai_hard':
                                play_screen(playerOne, playerTwo, ai_level='hard')
                            color_selected = True
                            opponent_selected = True
                        elif color_option == 'back':
                            break
                elif opponent_option == 'back':
                    break
        pyg.display.flip()


if __name__ == "__main__":
    loadImages()
    main_menu()

pyg.quit()
