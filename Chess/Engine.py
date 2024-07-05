"""
    This script is the backbone of our engine
    it stores all information about the current state of the game
    it determines valid moves including special moves and contains the logs
"""


class GameState():
    def __init__(self, board=None):
        # the board is a list of lists where each list represents a rank
        if board is None:
            self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["-", "-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-", "-"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        else:
            self.board = board

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.moveLog = []
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    """ 
    Method that takes a move as a param, checks for validity and executes 
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "-"  # emptying the starting square
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # logging da moves
        self.whiteToMove = not self.whiteToMove  # giving the right to move to the other player
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # En Passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "-"
        # update enpassantPossible var
        if (move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2):
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()
        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # move rook
                self.board[move.endRow][move.endCol + 1] = "-"  # remove old square rook
            else:  # queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move rook
                self.board[move.endRow][move.endCol - 2] = "-"  # remove rook from prev location

        self.enPassantPossibleLog.append(self.enPassantPossible)

        # update castling rights : rook or king moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    """
    Method that undoes the previous move
    """

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch back turns
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo en passant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = "-"
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]
            # undo castling move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "-"
                else:  # queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "-"
            # undoing castling rights
            self.castleRightsLog.pop()  # get rid of new castle rights from undone move
            self.currentCastlingRight = self.castleRightsLog[-1]  # set curr castling rights to most recent one
            self.checkMate = False
            self.staleMate = False

    """
    Helper method to update the castling rights after a move is made
    """

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    """ 
    Method to find all valid moves when there's a check,
    e.g: get all white's possible moves then generate 
    black's moves in the position, if any result in a 
    check, we unvalidate them
    """

    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible
        tempCastlingRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                          self.currentCastlingRight.wqs, self.currentCastlingRight.bqs, )
        moves = self.getAllMoves()  # all possible moves
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves) - 1, -1, -1):  # go backwards when removing from a list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  # not a valid move if the kings in check
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:  # checkmate / stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRight = tempCastlingRights
        return moves

    """ 
    Method to determine if a player in check
    """

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """ 
    Method to determine if the enemy can attack the square
    """

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    """ 
    Method to find all moves when there's no check
    """

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # know type of piece in X location
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  #
        return moves

    """
    Method to manage the pawn moves
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawns
            if self.board[r - 1][c] == "-":  # 1 square bawn move
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "-":  # 2 square bawn move
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # remove this if to make a funny bug
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnPassantMove=True))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnPassantMove=True))
        else:  # black pawns
            if self.board[r + 1][c] == "-":  # 1 square bawn move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "-":  # 2 square bawn move
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnPassantMove=True))

    """
    Method to manage the rook moves
    """

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "-":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # invalid piece
                        break
                else:  # off board
                    break

    """
    Method to manage the knight moves
    """

    def getKnightMoves(self, r, c, moves):

        knightDirections = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in knightDirections:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Method to manage the bishop moves
    """

    def getBishopMoves(self, r, c, moves):

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "-":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # invalid piece
                        break
                else:  # off board
                    break

    """
    Method to manage the queen moves
    """

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    """
    Method to manage the king moves
    """

    def getKingMoves(self, r, c, moves):

        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Method to generate all valid castle moves
    for the king in r,c and add them to his set of moves
    """

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    """
    Helper method to generate kingside castle moves
    """

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "-" and self.board[r][c + 2] == "-":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    """
    Helper method to generate queenside castle moves
    """

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "-" and self.board[r][c - 2] == "-" and self.board[r][c - 3] == "-":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # dictionaries to map keys to values (key: value)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board, isEnPassantMove=False,
                 isCastleMove=False):  # constructor definition
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (
                self.pieceMoved == 'bp' and self.endRow == 7)

        # en passeant
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        # castle move
        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '-'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # overriding the cast to string function
    def __str__(self):
        # castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        # pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        # remaining notations
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare