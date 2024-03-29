import poseidon

from poly_utils import PrimeField
from fft import fft

t ,full_round, partial_round, alpha, prime, input_rate, security_level, rc, mds = 3, 8, 57, 5, poseidon.prime_254, 2, 128, poseidon.round_constants_254, poseidon.matrix_254
instance = poseidon.FastPoseidon(prime, security_level, alpha, input_rate, t=t, full_round=full_round,
                                 partial_round=partial_round, rc_list=rc, mds_matrix=mds)


# BN128 curve order
assert prime == 21888242871839275222246405745257275088548364400416034343698204186575808495617

nelements = 4096
x = 123456

coeffs = []

pf = PrimeField(prime)
ru = pf.exp(5, (prime-1) // nelements)
print("ru = {}".format(ru))
ru_idx = 4095
encoding_key = 0x1234

modulusBn254 = 0x30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001
encoding_key = encoding_key % modulusBn254
print("encoding_key:{}".format(encoding_key))

for i in range(nelements // 2):
    inputs = [0, encoding_key + i, encoding_key + i + 1]
    outputs = instance.run_hash_state(inputs)
    coeffs.extend(outputs[0:2])

print("f({}) = {}".format(x, pf.eval_poly_at(coeffs, x)))
# print(coeffs)

for i in range(10):
    print("a_{} = {}".format(i, hex(coeffs[i])))

evals = fft(coeffs, prime, ru)
print("ru^{} = {}".format(ru_idx, pf.exp(ru, ru_idx)))
print("f(ru^{}) = {}".format(ru_idx, evals[ru_idx]))

for i in range(10):
    print("f(ru^{}) = {}".format(i, hex(evals[i])))
