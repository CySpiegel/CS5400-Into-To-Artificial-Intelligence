# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
from games.chess.functions import *
from games.chess.iddlmm import *
import random

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Matthew Stroble" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>
        fenSplit = self.game.fen.split(' ')
        fenBoard = fenSplit[0]
        fenNextTuenSide = fenSplit[1]
        fenCastlingAvailability = fenSplit[2]
        fenTurnsToDraw = fenSplit[4]
        fenTotalTurnsInGame = fenSplit[5]
        BoardList = fenBoard.split('/')

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Inferface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """

        #get move history list
        MoveHistory =  self.game.history
        #cul history list to last 8 moves
        if (len(MoveHistory) > 8):
            MoveHistory = MoveHistory[-8:]
        

        fenSplit = self.game.fen.split(' ')
        fenBoard = fenSplit[0]
        fenNextTuenSide = fenSplit[1]
        fenCastlingAvailability = fenSplit[2]
        fenTurnsToDraw = fenSplit[4]
        fenTotalTurnsInGame = fenSplit[5]
        BoardList = fenBoard.split('/')

        newChessBoard = parseFenBoardList(BoardList)
        # movementList = generateSelectedPeaceMoveList(self.player.color, newChessBoard, False)
        movePair = iddlmm(newChessBoard, self.player.color)

        print("")
        print("")

        print(self.game.print())

        print("")

        # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for makeMove
        return movePair[1]
        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
