from vision import Vision
from controller import Controller
from bot import Game
from window import Window

window = Window()
vision = Vision(window)
controller = Controller(window)
game = Game(vision, controller, window)

game.run()
