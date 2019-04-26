import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
plt.style.use('dark_background')

class SpiralAnimator:
    def __init__(self):
        self.fig = plt.figure()
        self.coords = []
        self.ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
        self.img, = self.ax.plot([], [], lw=2)

    def _animate(self, i):
        print("Frame number :: {}".format(i))

        t = 0.1*i
        # x, y values to be plotted
        x, y = t*np.sin(t), t*np.cos(t)

        # appending new points to x, y axes points list
        self.coords.append((x, y))
        X, Y = zip(*self.coords)
        self.img.set_data(X, Y)
        return[self.img]

    def animate(self, num_frames=1000):
        plt.axis('off')
        self.anim = animation.FuncAnimation(self.fig, self._animate,
                               frames=num_frames, interval=5, blit=True,
                               repeat=False)
        # plt.show()

    def save(self, filename="animation.mp4"):
        self.anim.save(filename, writer='imagemagick')



def main():
    animator = SpiralAnimator()
    animator.animate(100)
    animator.save("out/spiral.mp4")

if __name__ == "__main__":
    main()

