"""
BB84 Quantum Key Distribution - Simulation Engine
Part 1.4 Support Module

Provides the core simulation function that runs the full BB84 protocol
including optional Eve interception. Used to generate data for all visualizations.

Compatible with the team's Qiskit code (qiskit_aer backend, same gate conventions).
"""

import random
from qiskit import QuantumCircuit


def alice_bit_generator(n):
    """Generate n random classical bits for Alice."""
    return [random.randint(0, 1) for _ in range(n)]


def alice_bases_generator(n):
    """Generate n random bases for Alice (0=Z, 1=X)."""
    return [random.randint(0, 1) for _ in range(n)]


def bob_bases_generator(n):
    """Generate n random bases for Bob (0=Z, 1=X)."""
    return [random.randint(0, 1) for _ in range(n)]


def eve_bases_generator(n):
    """Generate n random bases for Eve (0=Z, 1=X)."""
    return [random.randint(0, 1) for _ in range(n)]


def simulate_bb84(n_qubits, eve_present=False, eve_attack_prob=1.0):
    """
    Run a complete BB84 simulation.

    Parameters
    ----------
    n_qubits : int
        Number of qubits Alice sends.
    eve_present : bool
        Whether Eve is intercepting.
    eve_attack_prob : float
        Probability (0-1) that Eve intercepts each individual qubit.

    Returns
    -------
    dict with keys:
        'alice_bits'      : list of Alice's original bits
        'alice_bases'     : list of Alice's bases
        'bob_bases'       : list of Bob's bases
        'bob_results'     : list of Bob's measurement results
        'sifted_alice'    : Alice's sifted key
        'sifted_bob'      : Bob's sifted key
        'sifted_length'   : length of sifted key
        'qber'            : quantum bit error rate in sifted key
        'eve_intercepted' : list of bools indicating which qubits Eve intercepted
    """
    alice_bits = alice_bit_generator(n_qubits)
    alice_bases = alice_bases_generator(n_qubits)
    bob_bases = bob_bases_generator(n_qubits)

    eve_intercepted = [False] * n_qubits
    eve_bases = [None] * n_qubits
    eve_results = [None] * n_qubits

    # --- Eve's interception (classical simulation for speed) ---
    # When Eve intercepts, she measures in a random basis, collapsing the state.
    # If her basis matches Alice's, she gets the correct bit and resends it.
    # If her basis doesn't match, she gets a random result and resends that.
    actual_bits = list(alice_bits)  # bits that Bob will "receive"

    if eve_present:
        eve_bases_list = eve_bases_generator(n_qubits)
        for i in range(n_qubits):
            if random.random() < eve_attack_prob:
                eve_intercepted[i] = True
                eve_bases[i] = eve_bases_list[i]

                # Eve measures
                if eve_bases[i] == alice_bases[i]:
                    # Same basis -> Eve gets correct bit
                    eve_results[i] = alice_bits[i]
                else:
                    # Different basis -> random result
                    eve_results[i] = random.randint(0, 1)

                # Eve resends her result (this is what Bob receives)
                actual_bits[i] = eve_results[i]

    # --- Bob's measurement (classical simulation for speed) ---
    # Simulates the quantum measurement without building a full circuit
    # for each qubit (much faster for 1000-10000 qubits).
    bob_results = []
    for i in range(n_qubits):
        if bob_bases[i] == alice_bases[i]:
            # Matching basis with the "sender" (Alice or Eve's resent qubit)
            # If Eve intercepted and had wrong basis, actual_bits[i] may differ
            # But Bob measures in Alice's basis, so if the qubit was disturbed
            # by Eve, Bob might get a wrong result.
            #
            # Classical model: if Bob's basis matches Alice's basis:
            #   - Bob gets actual_bits[i] (which may be Eve's corrupted bit)
            bob_results.append(actual_bits[i])
        else:
            # Different basis -> random outcome
            bob_results.append(random.randint(0, 1))

    # --- Key sifting ---
    sifted_alice = []
    sifted_bob = []
    for i in range(n_qubits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_results[i])

    # --- QBER calculation ---
    sifted_length = len(sifted_alice)
    if sifted_length > 0:
        errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
        qber = errors / sifted_length
    else:
        qber = 0.0

    return {
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'bob_bases': bob_bases,
        'bob_results': bob_results,
        'sifted_alice': sifted_alice,
        'sifted_bob': sifted_bob,
        'sifted_length': sifted_length,
        'qber': qber,
        'eve_intercepted': eve_intercepted,
    }


def build_bb84_circuit_example(alice_bit, alice_basis, bob_basis,
                                eve_present=False, eve_basis=None):
    """
    Build a single-qubit Qiskit circuit demonstrating one round of BB84.
    Used for circuit visualization (Part 1.4).

    Returns a QuantumCircuit.
    """
    if eve_present:
        # 3 classical bits: Eve's measurement, Bob's measurement, extra
        qc = QuantumCircuit(1, 2)
        qc.name = f"BB84 | Alice({alice_bit},{['Z','X'][alice_basis]}) " \
                   f"Eve({['Z','X'][eve_basis]}) Bob({['Z','X'][bob_basis]})"
    else:
        qc = QuantumCircuit(1, 1)
        qc.name = f"BB84 | Alice({alice_bit},{['Z','X'][alice_basis]}) " \
                   f"Bob({['Z','X'][bob_basis]})"

    # --- Alice encodes ---
    if alice_basis == 0:  # Z basis
        if alice_bit == 1:
            qc.x(0)
    else:  # X basis
        if alice_bit == 0:
            qc.h(0)
        else:
            qc.x(0)
            qc.h(0)

    qc.barrier(label='Send')

    if eve_present and eve_basis is not None:
        # Eve measures
        if eve_basis == 1:
            qc.h(0)
        qc.measure(0, 0)
        qc.barrier(label='Eve')

        # Eve re-prepares (reset + encode based on her result)
        qc.reset(0)
        # We use an if_test to conditionally apply X if Eve measured 1
        # For visualization, we show the general structure
        qc.x(0)  # placeholder: Eve re-encodes
        if eve_basis == 1:
            qc.h(0)
        qc.barrier(label='Resend')

    # --- Bob measures ---
    if bob_basis == 1:  # X basis
        qc.h(0)

    if eve_present:
        qc.measure(0, 1)
    else:
        qc.measure(0, 0)

    return qc


if __name__ == '__main__':
    # Quick test
    result = simulate_bb84(1000, eve_present=False)
    print(f"No Eve  -> Sifted key length: {result['sifted_length']}, QBER: {result['qber']:.4f}")

    result = simulate_bb84(1000, eve_present=True, eve_attack_prob=1.0)
    print(f"Eve 100% -> Sifted key length: {result['sifted_length']}, QBER: {result['qber']:.4f}")

    result = simulate_bb84(1000, eve_present=True, eve_attack_prob=0.5)
    print(f"Eve 50%  -> Sifted key length: {result['sifted_length']}, QBER: {result['qber']:.4f}")
