"""
This script contains the AI algorithms used in this engine
"""

import random
import time

"""
CONSTANTS
"""

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knightScore = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

bishopScore = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4]
]

rookScore = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4]
]
queenScore = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
]
whitePawnScore = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
blackPawnScore = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
]

piecePositionScores = {"Q": queenScore,
                       "N": knightScore,
                       "B": bishopScore,
                       "R": rookScore,
                       "bp": blackPawnScore,
                       "wp": whitePawnScore}
CHECKMATE = 9999
STALEMATE = 0
DEPTH = 2
MAX_TIME = 15.0

"""
Method to generate random moves 
"""


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


"""
Method to find best move based on material only, iterative minmax depth 2 lolz
"""


def findGreedyMove(gamestate, validMoves):  # iterative minmax depth 2 lolz
    turnMultiplier = 1 if gamestate.whiteToMove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gamestate.makeMove(playerMove)
        oppMoves = gamestate.getValidMoves()
        if gamestate.staleMate:
            oppMaxScore = STALEMATE
        elif gamestate.checkMate:
            oppMaxScore = -CHECKMATE
        else:
            oppMaxScore = -CHECKMATE
            for oppMove in oppMoves:
                gamestate.makeMove(oppMove)
                gamestate.getValidMoves()
                if gamestate.checkMate:
                    score = CHECKMATE
                elif gamestate.staleMate:
                    score = STALEMATE
                else:
                    score = - turnMultiplier * scoreMaterial(gamestate.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gamestate.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gamestate.undoMove()  # comment this out it's so funny

    return bestPlayerMove


"""
Method to find best move using a naive recursive minmax algorithm
"""


def findMinMaxMove(gamestate, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gamestate.board)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gamestate.makeMove(move)
            nextMoves = gamestate.getValidMoves()
            score = findMinMaxMove(gamestate, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gamestate.undoMove()

        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gamestate.makeMove(move)
            nextMoves = gamestate.getValidMoves()
            score = findMinMaxMove(gamestate, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gamestate.undoMove()
        return minScore


"""
Method to implement the Nega Max algorithm 
"""


def findNegaMaxMove(gamestate, validMoves, depth, turnMultuplier):
    global nextMove
    if depth == 0:
        return turnMultuplier * scoreBoard(gamestate)
    maxScore = -CHECKMATE
    for move in validMoves:
        gamestate.makeMove(move)
        nextMoves = gamestate.getValidMoves()
        score = -findNegaMaxMove(gamestate, nextMoves, depth - 1, -turnMultuplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gamestate.undoMove()
    return maxScore


"""
Method to implement NegaMax with Alpha beta pruning
"""


def findNegaMaxAlphaBeta(gamestate, validMoves, depth, alpha, beta, turnMultuplier):
    global nextMove
    if depth == 0:
        return quiescenceSearch(gamestate, alpha, beta, turnMultuplier)
    maxScore = -CHECKMATE
    for move in validMoves:
        gamestate.makeMove(move)
        nextMoves = gamestate.getValidMoves()
        score = -findNegaMaxAlphaBeta(gamestate, nextMoves, depth - 1, -beta, -alpha, -turnMultuplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gamestate.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


"""
Helper method to implement Quiescence search to help NegaMax
"""


def quiescenceSearch(gamestate, alpha, beta, turnMultuplier):
    stand_pat = turnMultuplier * scoreBoard(gamestate)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    validMoves = gamestate.getValidMoves()
    for move in validMoves:
        if move.isCapture:
            gamestate.makeMove(move)
            score = -quiescenceSearch(gamestate, -beta, -alpha, -turnMultuplier)
            gamestate.undoMove()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


"""
Method to make first recursive call to algorithm (difficulty: 1)
"""


def findBestMove(gamestate, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMinMaxMove(gamestate, validMoves, DEPTH, 1 if gamestate.whiteToMove else - 1)
    return nextMove


"""
Method to make first recursive call to algorithm (difficulty: 2)
"""


def findBestMove2(gamestate, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findNegaMaxAlphaBeta(gamestate, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gamestate.whiteToMove else - 1)
    return nextMove


"""
Helper method to Evaluate king safety
"""


def kingSafety(gamestate):
    safetyScore = 0
    if gamestate.whiteToMove:
        kingRow, kingCol = gamestate.whiteKingLocation
    else:
        kingRow, kingCol = gamestate.blackKingLocation

    # Evaluate pawn shield
    safetyScore += pawnShield(gamestate, kingRow, kingCol, gamestate.whiteToMove)

    # Evaluate enemy attacks
    safetyScore -= enemyAttacks(gamestate, kingRow, kingCol, gamestate.whiteToMove)

    return safetyScore if gamestate.whiteToMove else -safetyScore


"""
Helper method to Evaluate the pawn shield
around the king.
"""


def pawnShield(gamestate, kingRow, kingCol, isWhite):
    shieldScore = 0
    if gamestate.whiteToMove:
        pawnColor = 'w'
        direction = -1  # pawns move up the board
    else:
        pawnColor = 'b'
        direction = 1  # pawns move down the board

    # Check the three squares in front of the king
    for col in range(max(0, kingCol - 1), min(7, kingCol + 1) + 1):
        row = kingRow + direction
        if 0 <= row <= 7:
            piece = gamestate.board[row][col]
            if piece == pawnColor + 'p':
                shieldScore += 1

    return shieldScore * 5  # weight of pawn shield


"""
Method to Evaluate the number of 
enemy attacks on squares around the king.
"""


def enemyAttacks(gamestate, kingRow, kingCol, isWhite):
    attackScore = 0
    enemyColor = 'b' if gamestate.whiteToMove else 'w'
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for direction in directions:
        for i in range(1, 8):
            endRow = kingRow + direction[0] * i
            endCol = kingCol + direction[1] * i
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = gamestate.board[endRow][endCol]
                if piece[0] == enemyColor:
                    attackScore += 1
                    break
                elif piece != "--":
                    break
            else:
                break

    return attackScore * 2  # weighting factor for enemy attacks


"""
Helper method to help the scoring method  
number of valid moves to evaluate mobility
"""


def mobility(gamestate):
    mobilityScore = len(gamestate.getValidMoves())
    return mobilityScore if gamestate.whiteToMove else -mobilityScore


"""
Helper method to help the scoring method  
with controlled squares of the center
"""


def controlofCenter(gamestate):
    score = 0
    centerSquares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for (r, c) in centerSquares:
        piece = gamestate.board[r][c]
        if piece[0] == 'w':
            score += 1
        if piece[0] == 'b':
            score -= 1

    return score


"""
Helper method for Evaluating the board
- positive score means White winning 
- negative score means Black winning
"""


def scoreBoard(gamestate):
    if gamestate.checkMate:
        if gamestate.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gamestate.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gamestate.board)):
        for col in range(len(gamestate.board[row])):
            square = gamestate.board[row][col]
            if square != "-":
                # positional scoring
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p":  # pawn score
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:  # other pieces score
                        piecePositionScore = piecePositionScores[square[1]][row][col]
            if square[0] == 'w':
                score += pieceScore[square[1]] + piecePositionScore
            if square[0] == 'b':
                score -= pieceScore[square[1]] + piecePositionScore

    score += kingSafety(gamestate)
    score += mobility(gamestate)
    score += controlofCenter(gamestate)

    return score


"""
Helper Method to Find board score based on material 
"""


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
