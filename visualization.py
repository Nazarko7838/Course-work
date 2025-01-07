import matplotlib.pyplot as plt


def plot_scores(rounds, scores1, scores2, player1_name="Player 1", player2_name="Player 2"):
    plt.plot(rounds, scores1, label=player1_name)
    plt.plot(rounds, scores2, label=player2_name)
    plt.xlabel("Раунд")
    plt.ylabel("Рахунок")
    plt.title("Прогрес гри")
    plt.legend()
    plt.grid()
    plt.show()
