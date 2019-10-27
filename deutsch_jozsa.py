from pyquil import Program, get_qc
from pyquil.gates import *
from pyquil.api import local_forest_runtime
from pyquil.quil import DefGate

from arrays import uf_00, uf_01, uf_10, uf_11


def ghz_state(qubits):
    """
    Produces a generalized GHZ state on the given qubits by
    applying a Hadamard and CNOT gates.
    :param qubits: qubits to transform
    :return: GHZ state
    """
    program = Program()
    program += H(qubits[0])
    for q1, q2 in zip(qubits, qubits[1:]):
        program += CNOT(q1, q2)
    return program


def init_qubits(bits):
    """
    Initializes the QVM with the given states.

    `bits` is an array of classical values, where
    0 are qubits that should be left in the ground
    state, and 1 are qubits that should be excited.
    :param bits: the initialization pattern
    :return: init program
    """
    program = Program()
    for i, b in enumerate(bits):
        if b == 1:
            # excite the qubit
            program += X(i)
        # else leave it in ground

    return program


def Uf(uf_matrix):
    """
    Returns the U_f gate for a given function f.
    :param f: matrix repr
    :return: the gate representation of f
    """
    uf_definition = DefGate("UF-GATE", uf_matrix)
    UF_GATE = uf_definition.get_constructor()
    return uf_definition, UF_GATE


# Define size of algorithm
n = 4

uf_definition, UF_GATE = Uf(uf_01)

# construct a (0*n, 1) state
zeros = [0] * n
zeros.append(1)
p = init_qubits(zeros)
p += uf_definition
# apply Hadamards
for i in range(len(zeros)):
    p += H(i)
# apply Uf gate
p += UF_GATE()
# apply final Hadamards
for i in range(len(zeros) - 1):
    p += H(i)

with local_forest_runtime():
    qvm = get_qc('9q-square-qvm')
    results = qvm.run_and_measure(p, trials=10)
    print(results[0])
    print(results[1])
