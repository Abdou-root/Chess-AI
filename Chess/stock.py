"""
This script contains a stockfish engine integration to our game
for harder chess difficulties :p
"""

import stockfish
from Chess import Engine

"""
Method to get the best move from the stockfish engine
"""

gamestate = Engine.GameState()


def getBestMove(fen_position, stockfish_path, validMoves, depth_value=15):
    # Stockfish init
    engine = stockfish.Stockfish(stockfish_path)
    # Set difficulty
    engine.set_depth(depth_value)
    # Set position
    engine.set_fen_position(fen_position)
    # Get best move
    best_move = engine.get_best_move()

    return best_move


"""
Method to convert our gamestate to an FEN string for stockfish evaluation
"""


def getFen(gamestate):
    pieceToFEN = {"bR": "r", "bN": "n", "bB": "b", "bQ": "q", "bK": "k", "bp": "p",
                  "wR": "R", "wN": "N", "wB": "B", "wQ": "Q", "wK": "K", "wp": "P",
                  "-": "8"}
    board = gamestate.board
    en_passant_possible = gamestate.enPassantPossible
    current_castling_rights = gamestate.currentCastlingRight

    # Convert board to FEN
    fen_board = []
    for row in board:
        empty_squares = 0
        fen_row = ""
        for square in row:
            if square == "-":
                empty_squares += 1
            else:
                if empty_squares > 0:
                    fen_row += str(empty_squares)
                    empty_squares = 0
                fen_row += pieceToFEN[square]
        if empty_squares > 0:
            fen_row += str(empty_squares)
        fen_board.append(fen_row)

    fen_board = "/".join(fen_board)

    # Determine turn
    active_color = "w" if gamestate.whiteToMove else "b"

    # Castling rights
    castling_rights = ""
    if current_castling_rights.wks:
        castling_rights += "K"
    if current_castling_rights.wqs:
        castling_rights += "Q"
    if current_castling_rights.bks:
        castling_rights += "k"
    if current_castling_rights.bqs:
        castling_rights += "q"
    if not castling_rights:
        castling_rights = "-"

    # En passant target square
    if en_passant_possible:
        en_passant_square = Engine.Move.colsToFiles[en_passant_possible[1]] + Engine.Move.rowsToRanks[
            en_passant_possible[0]]
    else:
        en_passant_square = "-"

    # Halfmove clock and fullmove number (for now, setting to 0)
    halfmove_clock = "0"
    fullmove_number = str(len(gamestate.moveLog) // 2 + 1)

    # Combine all parts to form FEN
    fen = f"{fen_board} {active_color} {castling_rights} {en_passant_square} {halfmove_clock} {fullmove_number}"
    return fen


"""
Method to convert to convert the stockfish best move to gamestate
"""


def algebraToMove(move_str, gamestate):
    # Parse the move string
    startSquare = move_str[:2]
    endSquare = move_str[2:]

    # Convert to row and column indices
    startRow = Engine.Move.ranksToRows[startSquare[1]]
    startCol = Engine.Move.filesToCols[startSquare[0]]
    endRow = Engine.Move.ranksToRows[endSquare[1]]
    endCol = Engine.Move.filesToCols[endSquare[0]]

    # Create the Move object
    move = Engine.Move((startRow, startCol), (endRow, endCol), gamestate.board)

    return move


"""
Method to call to get the best move according to stockfish
"""
def findStockfishMove(gamestate, validMoves):
    fen = getFen(gamestate)
    stockfish_path = '../stockfish/stockfish-windows-x86-64-avx2.exe'
    bestMoveStr = getBestMove(fen, stockfish_path, validMoves)
    bestMove = algebraToMove(bestMoveStr, gamestate)
    return bestMove
