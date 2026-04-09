"""
BB84 Quantum Key Distribution - Key Length Graph
Part 1.4 Deliverable #3

Plots sifted key length vs number of qubits sent.
- Compares: No Eve vs Eve (full attack) vs Eve (50% attack)
- Shows theoretical ~50% sifting ratio
- Demonstrates how eavesdropping doesn't significantly change key LENGTH
  (only QBER changes — key length is determined by basis matching)

Output: key_length_vs_qubits.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from bb84_simulation import simulate_bb84


def plot_key_length(n_trials=15, save=True):
    """
    Generate key length vs number of qubits plot.

    Parameters
    ----------
    n_trials : int
        Number of trials to average at each qubit count.
    save : bool
        Whether to save the plot to a file.
    """
    qubit_counts = [100, 250, 500, 1000, 2000, 3000, 5000, 7500, 10000]

    scenarios = [
        {'label': 'No Eavesdropper', 'eve': False, 'prob': 0.0,
         'color': '#4CAF50', 'marker': 'o'},
        {'label': 'Eve (50% attack)', 'eve': True, 'prob': 0.5,
         'color': '#FF9800', 'marker': 's'},
        {'label': 'Eve (100% attack)', 'eve': True, 'prob': 1.0,
         'color': '#F44336', 'marker': '^'},
    ]

    print(f"\n[KEY LENGTH] Generating Key Length vs Qubits Sent ({n_trials} trials each)...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("BB84 Protocol: Sifted Key Length & Efficiency",
                 fontsize=15, fontweight='bold', y=1.02)

    for scenario in scenarios:
        mean_lengths = []
        std_lengths = []
        mean_ratios = []

        for n in qubit_counts:
            lengths = []
            for _ in range(n_trials):
                result = simulate_bb84(n, eve_present=scenario['eve'],
                                       eve_attack_prob=scenario['prob'])
                lengths.append(result['sifted_length'])
            mean_lengths.append(np.mean(lengths))
            std_lengths.append(np.std(lengths))
            mean_ratios.append(np.mean(lengths) / n)

            if n in [100, 1000, 10000]:
                print(f"  {scenario['label']:20s} | n={n:5d} -> "
                      f"key length = {np.mean(lengths):.0f} +/- {np.std(lengths):.0f} "
                      f"(ratio: {np.mean(lengths)/n:.3f})")

        # Key length plot
        ax1.errorbar(qubit_counts, mean_lengths, yerr=std_lengths,
                     fmt=f"{scenario['marker']}-", color=scenario['color'],
                     linewidth=2, markersize=7, capsize=4, capthick=1.5,
                     label=scenario['label'])

        # Sifting ratio plot
        ax2.plot(qubit_counts, mean_ratios,
                 f"{scenario['marker']}-", color=scenario['color'],
                 linewidth=2, markersize=7, label=scenario['label'])

    # Theoretical line on key length plot
    ax1.plot(qubit_counts, [n * 0.5 for n in qubit_counts], '--',
             color='gray', linewidth=1.5, alpha=0.7,
             label='Theoretical (50% sifting)')

    # Theoretical line on ratio plot
    ax2.axhline(y=0.5, color='gray', linestyle='--', linewidth=1.5,
                alpha=0.7, label='Expected ratio (0.50)')

    # Styling for key length plot
    ax1.set_xlabel("Number of Qubits Sent", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Sifted Key Length (bits)", fontsize=12, fontweight='bold')
    ax1.set_title("Sifted Key Length vs Qubits Sent", fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_facecolor('#FAFAFA')

    # Styling for ratio plot
    ax2.set_xlabel("Number of Qubits Sent", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Sifting Ratio (key length / qubits sent)", fontsize=12, fontweight='bold')
    ax2.set_title("Sifting Efficiency vs Qubits Sent", fontsize=13, fontweight='bold')
    ax2.legend(fontsize=9, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0.35, 0.65)
    ax2.set_facecolor('#FAFAFA')

    # Explain box
    textstr = ("Key length ≈ 50% of qubits sent\n"
               "(Alice & Bob bases match ~half the time).\n"
               "Eve doesn't change key length,\n"
               "only the error rate (QBER).")
    props = dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', alpha=0.8, edgecolor='#A5D6A7')
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', bbox=props)

    fig.patch.set_facecolor('white')
    plt.tight_layout()
    if save:
        plt.savefig('key_length_vs_qubits.png', dpi=200, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print("  [OK] Saved key_length_vs_qubits.png\n")
    plt.close()


if __name__ == '__main__':
    plot_key_length()
