import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import math

class MyAnimate:
    
    plt.rcParams['animation.embed_limit'] = 300

    n = 200
    d = 0.01
    v = 0.01
    dt = 1
    eta = 0.1

    r = np.random.random((n, 2))
    theta = np.random.random(n)

    fig, ax = plt.subplots(figsize=(6, 6))

    x = r[:, 0]
    y = r[:, 1]
    u = np.cos(2 * np.pi * theta)
    vv = np.sin(2 * np.pi * theta)

    q = ax.quiver(x, y, u, vv, angles='xy')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Vicsek Model")

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

    print("frame", frame, "counter", MyAnimate.counter)

    return MyAnimate.q,

if __name__ == "__main__":

    ani = FuncAnimation(MyAnimate.fig, animate, frames=200, interval=50, blit=True)
    plt.show()
