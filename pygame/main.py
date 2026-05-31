from src.core.motorGame.motor import MotorGame
from src.core.settings.config import width, height
import sys

motorgame = MotorGame(width=width, height=height)

if __name__ == "__main__":
    motorgame.loop()
    sys.exit()
