# ===================================================
#
# File Name: viewer.py
#
# Purpose: To replay bot save files
#
# Creation Date: 25-06-2017
#
# Last Modified: Thu 17 Aug 2017 04:41:58 PM PDT
#
# Created by: Jed Rembold
#
# ===================================================

import pickle, time, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk

pingrng = 8

p = argparse.ArgumentParser()
p.add_argument(
    "-i", "--input", default="lastgame.pickle", help="Saved replay file to load"
)
p.add_argument("-d", "--delay", default=1, help="Delay scaling factor. >1 speeds up")
args = p.parse_args()


with open(args.input, "rb") as f:
    mapstate = pickle.load(f)


def getPlayerDirSym(player):
    if player["face"] == 0:
        return "▲"
    if player["face"] == 1:
        return "▶"
    if player["face"] == 2:
        return "▼"
    if player["face"] == 3:
        return "◀"
    return "o"


def getBallColor(ball_activity):
    if ball_activity:
        return "red"
    return "gray"


def getPlayerColor(player):
    player_colors = [
            'firebrick1', 'goldenrod1', 'spring green', 'turquoise1', 'purple1',
            'deep pink', 'gold', 'deep sky blue', 'aquamarine', 'medium orchid'
            ]
    return player_colors[(player % 50) % len(player_colors)]


class Application(tk.Frame):
    @classmethod
    def main(cls):
        root = tk.Tk()
        app = cls(root)
        app.pack()
        root.mainloop()

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.size = 600
        self.initCanvas()
        self.round = 0
        self.maxround = max([x for x in mapstate if isinstance(x,int)])
        self.drawround()
        # self.playForward()

    def computePixel(self, p):
        return (p + 0.5) * self.bs

    def initCanvas(self):
        self.field = tk.Canvas(self, width=self.size, height=self.size, bg="#202020")
        self.bs = np.floor(self.size / mapstate["Map"].shape[0])
        self.field.pack()

    def drawround(self):
        self.field.delete('all')
        self.drawpings()
        self.drawmap()
        self.drawplayers()
        self.drawballs()

        self.round += 1
        if self.round <= self.maxround:
            self.after(100, self.drawround)
        else:
            if len(mapstate[self.round-1]['players'])>0:
                (winner_id, winner_data), = mapstate[self.round-1]['players'].items()
                self.field.create_text(
                        300, 300,
                        text = f'{winner_data["name"][:-3]} wins!',
                        fill = getPlayerColor(winner_id),
                        font = ('Purisa', 24),
                        )
            else:
                self.field.create_text(
                        300, 300,
                        text = f'There were no winners!',
                        fill = 'gray',
                        font = ('Purisa', 24),
                        )

            self.after(5000, self.root.destroy)

    def drawmap(self):
        for j, row in enumerate(mapstate[self.round]["map"]):
            for i, col in enumerate(row):
                if col == 1:
                    self.field.create_rectangle(
                        i * self.bs,
                        j * self.bs,
                        (i + 1) * self.bs,
                        (j + 1) * self.bs,
                        fill="black",
                        outline="green",
                    )

    def drawplayers(self):
        for idx, player in mapstate[self.round]["players"].items():
            self.field.create_text(
                self.computePixel(player["x"]),
                self.computePixel(player["y"]),
                # text="↑",
                text = getPlayerDirSym(player),
                fill = getPlayerColor(idx),
                font = ('Purisa', player['balls']*2 + 8),
            )

    def drawpings(self):
        for idx, player in mapstate[self.round]["players"].items():
            if player['pinging']:
                self.field.create_oval(
                        self.computePixel(player["x"]-pingrng),
                        self.computePixel(player["y"]+pingrng),
                        self.computePixel(player["x"]+pingrng),
                        self.computePixel(player["y"]-pingrng),
                        outline = getPlayerColor(idx),
                        # stipple="gray12",
                        )

    def drawballs(self):
        for ball in mapstate[self.round]["balls"]:
            self.field.create_oval(
                self.computePixel(ball[0])-5,
                self.computePixel(ball[1])-5,
                self.computePixel(ball[0])+5,
                self.computePixel(ball[1])+5,
                fill = getBallColor(ball[3]),
            )


if __name__ == "__main__":
    Application.main()

