"""
BB84 Quantum Key Distribution - QBER Graph
Part 1.4 Deliverable #2

Plots Quantum Bit Error Rate (QBER) vs Eve's attack probability.
- Sweeps attack probability from 0.0 to 1.0
- Runs multiple trials per point for statistical averaging
- Shows error bars and the theoretical 25% threshold

Output: qber_vs_attack_prob.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from bb84_simulation import simulate_bb84


def plot_qber_vs_attack_probability(n_qubits=1000, n_trials=20, save=True):
    """
    Generate QBER vs attack probability plot.

    Parameters
    ----------
    n_qubits : int
        Number of qubits per simulation run.
    n_trials : int
        Number of trials to average at each attack probability.
    save : bool
        Whether to save the plot to a file.
    """
    attack_probs = np.arange(0.0, 1.05, 0.05)
    mean_qbers = []
    std_qbers = []

    print(f"\n[QBER] Generating QBER vs Attack Probability (n={n_qubits}, {n_trials} trials each)...")

    for prob in attack_probs:
        qbers = []
        for _ in range(n_trials):
            result = simulate_bb84(n_qubits, eve_present=(prob > 0), eve_attack_prob=prob)
            qbers.append(result['qber'])
        mean_qbers.append(np.mean(qbers))
        std_qbers.append(np.std(qbers))
        print(f"  Attack prob = {prob:.2f} -> QBER = {np.mean(qbers):.4f} +/- {np.std(qbers):.4f}")

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Main data with error bars
    ax.errorbar(attack_probs, mean_qbers, yerr=std_qbers,
                fmt='o-', color='#2196F3', linewidth=2, markersize=6,
                capsize=4, capthick=1.5, ecolor='#90CAF9',
                label=f'Simulated QBER (n={n_qubits})')

    # Fill uncertainty region
    ax.fill_between(attack_probs,
                     np.array(mean_qbers) - np.array(std_qbers),
                     np.array(mean_qbers) + np.array(std_qbers),
                     alpha=0.15, color='#2196F3')

    # Theoretical line: QBER = 0.25 * attack_prob
    theoretical_qber = 0.25 * attack_probs
    ax.plot(attack_probs, theoretical_qber, '--', color='#F44336', linewidth=2,
            label='Theoretical QBER = 0.25 × P(attack)')

    # 25% threshold line
    ax.axhline(y=0.25, color='#FF9800', linestyle=':', linewidth=1.5,
               label='Maximum QBER threshold (25%)')

    # Annotations
    ax.annotate('No eavesdropping\nQBER ≈ 0%',
                xy=(0.0, 0.0), xytext=(0.12, 0.08),
                fontsize=10, fontweight='bold', color='#4CAF50',
                arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5))

    ax.annotate('Full attack\nQBER ≈ 25%',
                xy=(1.0, mean_qbers[-1]), xytext=(0.75, 0.32),
                fontsize=10, fontweight='bold', color='#F44336',
                arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.5))

    # Styling
    ax.set_xlabel("Eve's Attack Probability", fontsize=13, fontweight='bold')
    ax.set_ylabel("Quantum Bit Error Rate (QBER)", fontsize=13, fontweight='bold')
    ax.set_title("BB84 Protocol: QBER vs Eavesdropping Intensity",
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 0.40)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('white')

    # Add explanation text box
    textstr = ("Eve intercepts each qubit with probability P.\n"
               "Wrong basis (50%) × wrong result (50%) = 25% max QBER.\n"
               "If QBER > threshold → eavesdropping detected!")
    props = dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD', alpha=0.8, edgecolor='#90CAF9')
    ax.text(0.98, 0.65, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    if save:
        plt.savefig('qber_vs_attack_prob.png', dpi=200, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print("  [OK] Saved qber_vs_attack_prob.png\n")
    plt.close()


if __name__ == '__main__':
    plot_qber_vs_attack_probability()
