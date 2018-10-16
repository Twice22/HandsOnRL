import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable


# We want to plot
# V[(current_sum, dealer_card, usableAce)] = value
# we can thus plot a 3D plot (x, y, z) = (current_sum, dealer_card, value)
# and we need to plot 2 differents plot 
# (one if we have an usableAce and one when we don't have)
def plot_state_values(V, iterations):
	x_range = np.arange(12, 22) # if < 11 we are not dumb and we pick another card
	y_range = np.arange(1, 11) # dealer's face up card
	X, Y = np.meshgrid(x_range, y_range)

	fig = plt.figure(figsize=(15,20))

	aces = [(True, "Usable ace"), (False, "No usable ace")]

	for i, (usableAce, title) in enumerate(aces, 1):
		ax = fig.add_subplot(int("21" + str(i)), projection='3d')
		Z = np.array([V[x, y, usableAce] if (x, y, usableAce) in V else 0 for y in Y[:,0] for x in X[0] ]).reshape(X.shape)

		surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, vmin=-1.0, vmax=1.0,
							   edgecolor='w', linewidth=0.5)
		ax.set_xlabel("Player's Current Sum")
		ax.set_ylabel("Dealer's Showing Card")
		ax.set_zlabel("Value")
		ax.view_init(ax.elev, -120)
		ax.set_title(title, fontsize=14)

	fig.suptitle("Value after %i iterations" % iterations, fontsize=20)
	plt.show()


def plot_policy(pi, headline):
    def draw(pi, ax, aceValue):
        rows, cols = 11, 10
        image = np.zeros((rows, cols))

        for state, val in pi.items():
            player_sum, dealer_card, usableAce = state
            if usableAce != aceValue or player_sum < 11:
                continue

            image[player_sum-11, dealer_card-1] = 1-val
            
        row_labels = np.arange(11, 22)
        col_labels = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        surf = ax.matshow(image, cmap=plt.get_cmap('Pastel1', 2),
                          extent=[-1, 9, 10, -1])
        plt.gca().invert_yaxis()
        plt.xticks(range(cols), col_labels)
        plt.yticks(range(rows), row_labels)
        ax.grid(color='white', linestyle='--', linewidth=1)
        ax.set_title("%s ace" % ("Usable" if aceValue else "No usable"),
                     fontsize=16)
        
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.2)
        cbar = plt.colorbar(surf, ticks=[0.25,0.75], cax=cax, )
        cbar.ax.set_yticklabels(['HIT','STICK'])
        


    f = plt.figure(figsize=(15,8))

    aces = [(True, "Usable ace"), (False, "No usable ace")]

    for i, (usableAce, title) in enumerate(aces, 1):
        ax = f.add_subplot(int("12" + str(i)))
        draw(pi, ax, usableAce)
    
    f.suptitle(headline, fontsize=20)
    plt.show()