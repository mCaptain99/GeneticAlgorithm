import matplotlib.pyplot as plt


class Plots:

    @staticmethod
    def best_plot(bests):
        plt.ylabel('Results')
        plt.xlabel('Epochs')
        epochs_amount = len(bests) - 1
        epochs_counter = [i+1 for i in range(epochs_amount + 1)]
        plt.plot(epochs_counter, bests, 'b')
        plt.savefig('best_result_chart.png')
        plt.close()
        file = open("results.txt", "w")
        for i in range(epochs_amount):
            file.write(str(epochs_counter[i]) + "  " + str(bests[i]) + "\n")
        file.close()

    @staticmethod
    def average_plot(averages):
        plt.ylabel('Average result')
        plt.xlabel('Epochs')
        epochs_amount = len(averages) - 1
        epochs_counter = [i + 1 for i in range(epochs_amount + 1)]
        plt.plot(epochs_counter, averages, 'r')
        plt.savefig('average_result_chart.png')
        plt.close()

    @staticmethod
    def std_plot(stds):
        plt.ylabel('Std')
        plt.xlabel('Epochs')
        epochs_amount = len(stds) - 1
        epochs_counter = [i + 1 for i in range(epochs_amount + 1)]
        plt.plot(epochs_counter, stds, 'g')
        plt.savefig('std_chart.png')
        plt.close()
