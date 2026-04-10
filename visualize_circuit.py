import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit

from bb import encode_qubits
from bb84_simulation import build_bb84_circuit_example


def create_alice_encoding_circuits():
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Alice's Qubit Encoding in BB84", fontsize=16, fontweight='bold', y=0.98)

    configs = [
        (0, 0, "Bit=0, Z-basis -> |0>"),
        (1, 0, "Bit=1, Z-basis -> |1>"),
        (0, 1, "Bit=0, X-basis -> |+>"),
        (1, 1, "Bit=1, X-basis -> |->"),
    ]

    for idx, (bit, basis, title) in enumerate(configs):
        qc = QuantumCircuit(1)
        qc.name = title

        if basis == 0:
            if bit == 1:
                qc.x(0)
        else:
            if bit == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)

        ax = axes[idx // 2][idx % 2]
        qc.draw('mpl', ax=ax)
        ax.set_title(title, fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('circuit_alice_encoding.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("  [OK] Saved circuit_alice_encoding.png")


def create_bob_measurement_circuits():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Bob's Measurement in BB84", fontsize=16, fontweight='bold', y=1.02)

    qc1 = QuantumCircuit(1, 1)
    qc1.x(0)
    qc1.barrier(label='Channel')
    qc1.measure(0, 0)
    qc1.draw('mpl', ax=axes[0])
    axes[0].set_title("Matching Basis (Z->Z): Correct Result", fontsize=11, fontweight='bold')

    qc2 = QuantumCircuit(1, 1)
    qc2.x(0)
    qc2.barrier(label='Channel')
    qc2.h(0)
    qc2.measure(0, 0)
    qc2.draw('mpl', ax=axes[1])
    axes[1].set_title("Mismatching Basis (Z->X): Random Result", fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('circuit_bob_measurement.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("  [OK] Saved circuit_bob_measurement.png")


def create_eve_interception_circuit():
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle("BB84 Protocol: Without vs With Eavesdropper (Eve)",
                 fontsize=16, fontweight='bold', y=1.02)

    qc_no_eve = build_bb84_circuit_example(
        alice_bit=1, alice_basis=0, bob_basis=0,
        eve_present=False
    )
    qc_no_eve.draw('mpl', ax=axes[0])
    axes[0].set_title("Normal: Alice(1,Z) -> Bob(Z) OK", fontsize=11, fontweight='bold')

    qc_eve = build_bb84_circuit_example(
        alice_bit=1, alice_basis=0, bob_basis=0,
        eve_present=True, eve_basis=1
    )
    qc_eve.draw('mpl', ax=axes[1])
    axes[1].set_title("Eve Attack: Alice(1,Z) -> Eve(X) -> Bob(Z) X", fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('circuit_eve_attack.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("  [OK] Saved circuit_eve_attack.png")


def create_full_protocol_circuit():
    n = 4
    alice_bits =  [1, 0, 1, 0]
    alice_bases = [0, 1, 1, 0]
    bob_bases =   [0, 0, 1, 1]

    import bb
    original_n = bb.n
    bb.n = n
    qc = encode_qubits(alice_bits, alice_bases)
    bb.n = original_n

    qc.barrier(label='Quantum Channel')

    for i in range(n):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)

    fig, ax = plt.subplots(figsize=(14, 6))
    qc.draw('mpl', ax=ax)

    title = "Full BB84 Protocol Example (4 qubits)\n"
    title += "Alice bits: [1,0,1,0]  |  Alice bases: [Z,X,X,Z]  |  Bob bases: [Z,Z,X,X]\n"
    title += "Matching bases at q0(Z=Z) and q2(X=X) -> sifted key from these positions"
    ax.set_title(title, fontsize=12, fontweight='bold', linespacing=1.5)

    plt.tight_layout()
    plt.savefig('circuit_full_protocol.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("  [OK] Saved circuit_full_protocol.png")


def run_all():
    print("\n[CIRCUITS] Generating Circuit Visualizations...")
    create_alice_encoding_circuits()
    create_bob_measurement_circuits()
    create_eve_interception_circuit()
    create_full_protocol_circuit()
    print("  Done!\n")


if __name__ == '__main__':
    run_all()
