import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import click
import math
import logging
import pdb
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MyAnimate:

    def __init__(self, n=200):
        self.n = n
        self.r = np.random.random((self.n, 2))
        self.theta = np.random.random(self.n)
        self.counter = 0

    
    @staticmethod
    def distance(p1, p2):
        return np.sqrt(((p1 - p2) ** 2).sum())
    
    plt.rcParams['animation.embed_limit'] = 300


    def update_model(self, d = 0.01, v=0.01, dt=1, eta=0.1):

        for i in range(self.n):
            sum_sin = 0
            sum_cos = 0
            neighbours = 0

            for j in range(self.n):
                if i != j:
                    if MyAnimate.distance(self.r[i], self.r[j]) < d:
                        theta_j = 2 * np.pi * self.theta[j]
                        sum_sin = sum_sin + np.sin(theta_j)
                        sum_cos = sum_cos + np.cos(theta_j)
                        neighbours = neighbours + 1

            if neighbours > 0:
                avg_theta = np.arctan2(sum_sin / neighbours, sum_cos / neighbours)
                self.theta[i] = (avg_theta / (2 * np.pi)) + eta * (np.random.rand() - 0.5)

            dx = v * dt * np.cos(2 * np.pi * self.theta[i])
            dy = v * dt * np.sin(2 * np.pi * self.theta[i])

            self.r[i, 0] = self.r[i, 0] + dx
            self.r[i, 1] = self.r[i, 1] + dy

            if self.r[i, 0] > 1:
                self.r[i, 0] = 0
            if self.r[i, 1] > 1:
                self.r[i, 1] = 0
            if self.r[i, 0] < 0:
                self.r[i, 0] = 1
            if self.r[i, 1] < 0:
                self.r[i, 1] = 1

            self.counter = self.counter + 1


def animate(frame, model, q):
    model.update_model()
    x = []
    y = []
    u = []
    vv = []
    for i in range(model.n):
        x.append(model.r[i, 0])
        y.append(model.r[i, 1])
        u.append(np.cos(2 * np.pi * model.theta[i]))
        vv.append(np.sin(2 * np.pi * model.theta[i]))
    q.set_offsets(np.c_[x, y])

    q.set_UVC(u, vv)
    #logging.info("frame: %d, counter: %d", frame, model.counter)
    return q,

@click.command()
@click.option("--n", default=200)
@click.option("--d", default=0.01)
@click.option("--v", default=0.01)
@click.option("--dt", default=1)
@click.option("--eta", default=0.1)
def main(n, d, v, dt, eta):

    fig, ax = plt.subplots(figsize=(6, 6))
    vicsek = MyAnimate(n)

    x = vicsek.r[:, 0]
    y = vicsek.r[:, 1]
    u = np.cos(2 * np.pi * vicsek.theta)
    vv = np.sin(2 * np.pi * vicsek.theta)
    q = ax.quiver(x, y, u, vv, angles='xy')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Vicsek Model")

    ani = FuncAnimation(fig, animate, fargs=(vicsek, q), frames=200, interval=50, blit=True)
    plt.show()


if __name__ == "__main__":
    main()