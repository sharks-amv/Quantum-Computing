import time
from bb84_simulation import simulate_bb84


def main():
    print("=" * 60)
    print("  BB84 Quantum Key Distribution")
    print("  Part 1.4: Visualization and Results")
    print("=" * 60)

    start = time.time()

    print("\n[*] Running quick sanity check...")
    r1 = simulate_bb84(1000, eve_present=False)
    print(f"  No Eve:   sifted key = {r1['sifted_length']} bits, QBER = {r1['qber']:.4f}")
    r2 = simulate_bb84(1000, eve_present=True, eve_attack_prob=1.0)
    print(f"  Eve 100%: sifted key = {r2['sifted_length']} bits, QBER = {r2['qber']:.4f}")
    print("  Sanity check passed." if r1['qber'] < 0.05 and r2['qber'] > 0.15 else "  WARNING: Unexpected results")

    from visualize_circuit import run_all as run_circuits
    run_circuits()

    from plot_qber import plot_qber_vs_attack_probability
    plot_qber_vs_attack_probability(n_qubits=1000, n_trials=20)

    from plot_key_length import plot_key_length
    plot_key_length(n_trials=15)

    from plot_surface import plot_qber_surface
    plot_qber_surface(n_trials=5)

    elapsed = time.time() - start

    print("=" * 60)
    print(f"  All done! Total time: {elapsed:.1f} seconds")
    print("=" * 60)
    print("\nGenerated files:")
    print("  Circuit Diagrams:")
    print("    - circuit_alice_encoding.png")
    print("    - circuit_bob_measurement.png")
    print("    - circuit_eve_attack.png")
    print("    - circuit_full_protocol.png")
    print("  Graphs:")
    print("    - qber_vs_attack_prob.png")
    print("    - key_length_vs_qubits.png")
    print("    - qber_surface_3d.png")
    print("    - qber_heatmap.png")
    print()


if __name__ == '__main__':
    main()
