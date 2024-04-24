import matplotlib.pyplot as plt

def plot_fa_profiles(fa_profiles):
    colors = ['r', 'g', 'b']  # colors for the FA profiles

    for i, fa_profile in enumerate(fa_profiles):
        plt.plot(fa_profile, color=colors[i], label=f'Centroid {i+1}')

    plt.xlabel('Point along centroid')
    plt.ylabel('FA value')
    plt.legend()
    plt.show()