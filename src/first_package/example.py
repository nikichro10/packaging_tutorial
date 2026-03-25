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
    
    plt.rcParams['animation.embed_limit'] = 300

    n = None
    d = None
    v = None
    dt = None
    eta = None

    r = None
    theta = None
    counter = 0


def distance(p1, p2):
    return np.sqrt(((p1 - p2) ** 2).sum())


def update_model():
    
    for i in range(MyAnimate.n):
        sum_sin = 0
        sum_cos = 0
        neighbours = 0

        for j in range(MyAnimate.n):
            if i != j:
                if distance(MyAnimate.r[i], MyAnimate.r[j]) < MyAnimate.d:
                    theta_j = 2 * np.pi * MyAnimate.theta[j]
                    sum_sin = sum_sin + np.sin(theta_j)
                    sum_cos = sum_cos + np.cos(theta_j)
                    neighbours = neighbours + 1

        if neighbours > 0:
            avg_theta = np.arctan2(sum_sin / neighbours, sum_cos / neighbours)
            MyAnimate.theta[i] = (avg_theta / (2 * np.pi)) + MyAnimate.eta * (np.random.rand() - 0.5)

        dx = MyAnimate.v * MyAnimate.dt * np.cos(2 * np.pi * MyAnimate.theta[i])
        dy = MyAnimate.v * MyAnimate.dt * np.sin(2 * np.pi * MyAnimate.theta[i])

        MyAnimate.r[i, 0] = MyAnimate.r[i, 0] + dx
        MyAnimate.r[i, 1] = MyAnimate.r[i, 1] + dy

        if MyAnimate.r[i, 0] > 1:
            MyAnimate.r[i, 0] = 0
        if MyAnimate.r[i, 1] > 1:
            MyAnimate.r[i, 1] = 0
        if MyAnimate.r[i, 0] < 0:
            MyAnimate.r[i, 0] = 1
        if MyAnimate.r[i, 1] < 0:
            MyAnimate.r[i, 1] = 1

        MyAnimate.counter = MyAnimate.counter + 1


def animate(frame):

    update_model()

    x = []
    y = []
    u = []
    vv = []

    for i in range(MyAnimate.n):
        x.append(MyAnimate.r[i, 0])
        y.append(MyAnimate.r[i, 1])
        u.append(np.cos(2 * np.pi * MyAnimate.theta[i]))
        vv.append(np.sin(2 * np.pi * MyAnimate.theta[i]))

    MyAnimate.q.set_offsets(np.c_[x, y])
    MyAnimate.q.set_UVC(u, vv)

    logging.info("frame: %d, counter: %d", frame, MyAnimate.counter)

    return MyAnimate.q,

@click.command()
@click.option("--n", default=200)
@click.option("--d", default=0.01)
@click.option("--v", default=0.01)
@click.option("--dt", default=1)
@click.option("--eta", default=0.1)
def main(n, d, v, dt, eta):

    # Parameter setzen
    MyAnimate.n = n
    MyAnimate.d = d
    MyAnimate.v = v
    MyAnimate.dt = dt
    MyAnimate.eta = eta
    #pdb.set_trace()
    #breakpoint()

    MyAnimate.r = np.random.random((MyAnimate.n, 2))
    MyAnimate.theta = np.random.random(MyAnimate.n)

    MyAnimate.fig, MyAnimate.ax = plt.subplots(figsize=(6, 6))

    MyAnimate.q = MyAnimate.ax.quiver(
        MyAnimate.r[:, 0],
        MyAnimate.r[:, 1],
        np.cos(2 * np.pi * MyAnimate.theta),
        np.sin(2 * np.pi * MyAnimate.theta),
        angles='xy'
    )

    MyAnimate.ax.set_xlim(0, 1)
    MyAnimate.ax.set_ylim(0, 1)
    MyAnimate.ax.set_title("Vicsek Model")

    ani = FuncAnimation(MyAnimate.fig, animate, frames=200, interval=50, blit=True)
    plt.show()


if __name__ == "__main__":
    main()