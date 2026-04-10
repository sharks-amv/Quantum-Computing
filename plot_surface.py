import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from bb84_simulation import simulate_bb84


def plot_qber_surface(n_trials=5, save=True):
    attack_probs = np.arange(0.0, 1.05, 0.1)
    qubit_counts = [100, 250, 500, 750, 1000, 1500, 2000, 3000, 5000]

    print(f"\n[SURFACE] Generating 3D QBER Surface ({n_trials} trials per point)...")
    total_points = len(attack_probs) * len(qubit_counts)
    print(f"  Grid: {len(attack_probs)} x {len(qubit_counts)} = {total_points} points")

    X, Y = np.meshgrid(attack_probs, qubit_counts)
    Z = np.zeros_like(X, dtype=float)

    count = 0
    for i, n_q in enumerate(qubit_counts):
        for j, prob in enumerate(attack_probs):
            qbers = []
            for _ in range(n_trials):
                result = simulate_bb84(n_q, eve_present=(prob > 0),
                                       eve_attack_prob=prob)
                qbers.append(result['qber'])
            Z[i, j] = np.mean(qbers)
            count += 1
            if count % 20 == 0:
                print(f"  Progress: {count}/{total_points} points computed...")

    print(f"  All {total_points} points computed.")

    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none',
                           alpha=0.85, antialiased=True)

    ax.plot_wireframe(X, Y, Z, color='black', alpha=0.1, linewidth=0.5)

    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=15, pad=0.1)
    cbar.set_label('QBER', fontsize=12, fontweight='bold')

    xx, yy = np.meshgrid(attack_probs, qubit_counts)
    zz = np.full_like(xx, 0.25, dtype=float)
    ax.plot_surface(xx, yy, zz, alpha=0.15, color='red')
    ax.text(0.5, 5000, 0.26, "QBER = 25% threshold", color='red',
            fontsize=9, fontweight='bold')

    ax.set_xlabel("\nEve's Attack Probability", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel("\nNumber of Qubits", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_zlabel("\nQBER", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_title("BB84 Simulation: QBER Surface\n(Attack Probability x Number of Qubits)",
                 fontsize=14, fontweight='bold', pad=20)

    ax.view_init(elev=25, azim=225)
    ax.set_zlim(0, 0.35)

    fig.patch.set_facecolor('white')
    plt.tight_layout()
    if save:
        plt.savefig('qber_surface_3d.png', dpi=200, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print("  [OK] Saved qber_surface_3d.png\n")
    plt.close()

    fig2, ax2 = plt.subplots(figsize=(12, 7))
    im = ax2.imshow(Z, aspect='auto', origin='lower', cmap='coolwarm',
                    extent=[attack_probs[0], attack_probs[-1], 0, len(qubit_counts)-1],
                    vmin=0, vmax=0.30)

    ax2.set_yticks(range(len(qubit_counts)))
    ax2.set_yticklabels(qubit_counts)
    ax2.set_xlabel("Eve's Attack Probability", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Number of Qubits", fontsize=12, fontweight='bold')
    ax2.set_title("BB84 Simulation: QBER Heatmap\n(Attack Probability x Number of Qubits)",
                  fontsize=14, fontweight='bold')

    cbar2 = fig2.colorbar(im, ax=ax2, shrink=0.8)
    cbar2.set_label('QBER', fontsize=12, fontweight='bold')

    cs = ax2.contour(np.linspace(attack_probs[0], attack_probs[-1], Z.shape[1]),
                      np.arange(Z.shape[0]),
                      Z, levels=[0.05, 0.10, 0.15, 0.20, 0.25],
                      colors='black', linewidths=0.8, alpha=0.5)
    ax2.clabel(cs, inline=True, fontsize=8, fmt='%.2f')

    fig2.patch.set_facecolor('white')
    plt.tight_layout()
    if save:
        plt.savefig('qber_heatmap.png', dpi=200, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print("  [OK] Saved qber_heatmap.png\n")
    plt.close()


if __name__ == '__main__':
    plot_qber_surface()
