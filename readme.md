
# ChessAI Engine Project

This project aims to create a complete chess engine capable of enjoying the beauty of the game of chess empowered with the advancement of AI.
using Pygame and stockfish, play against AI of varying difficulties or against another human player.


## Overview

The chess engine is developed in Python and uses the Pygame library for rendering the chessboard and pieces, handling user inputs, and visualizing the game state.

### Key Components

- **Engine.py**: Core script managing the game state.
  - Stores all information about the current game state.
  - Determines valid moves, including special moves, and maintains game logs.

- **MoveAI.py**: Script containing AI algorithms for gameplay.
  - Includes algorithms such as minmax, alpha-beta pruning, and negamax.

- **stock.py**: Script integrating the Stockfish engine into the game for AI opponents.
  - Provides harder chess difficulties by leveraging Stockfish.

- **button.py**: Python script defining a class for handling user input on buttons and updating the screen.

- **Driver.py**: Main driver script for the ChessAI game.
  - Handles user input, mouse events, animations, and displays the game state.
  - Implements the Pygame GUI for the chess game.

### Libraries Used

- Pygame: Used for implementing the graphical user interface.
- Python Standard Libraries: `random` and `time` for general functionalities.
- Stockfish: Chess engine integrated for AI gameplay.

### Features

- Rendering of chessboard and pieces using Pygame
- Handling user inputs to move pieces
- Determining all valid moves for the current game state
- Special moves: Pawn Promotion, En Passant, Castling
- Check, Checkmate and Stalemate detection
- Play against a human or AI opponents with 3 difficulties

### Algorithms

- Implement MinMax Algorithm (with and without recursion)
- Implement Alpha-Beta Pruning into NegaMax
- Advanced AI opponent of the stockfish Engine

## Getting Started

To run this chess engine on your local machine, ensure you have Python and Pygame installed. Clone the repository, navigate to the project directory, and run the driver script:

```bash
git clone <repository-url>
cd chess-engine
python Driver.py
```

## Contribution

Feel free to fork the repository and submit pull requests. Whether it's fixing bugs, adding new features, or improving the documentation, all contributions are welcome.


