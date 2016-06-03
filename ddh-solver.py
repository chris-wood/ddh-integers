from sage.all import *

numbits = int(sys.argv[1])
maxp = 2 ** numbits
p = random_prime(maxp)

k = GF(p)
g = k.multiplicative_generator()

print p, k, g

def _jacobi(a, b):
    if a == 1:
        return 1
    if a == 0:
        return -1

    # 1. Reduce the numerator modulo the denominator
    if a > b:
        return _jacobi(a % b, b)

    # 2. Extract factors of two from the numerator and evaluate them
    # (ab | n) = (a | n)(b | n)
    # (2 | n) -> rule 8
    if a % 2 == 0:
        w = 1 if (b % 8 == 1 or b % 8 == 7) else -1
        return w * _jacobi(a / 2, b) # extract a factor of two from the numerator

    # 3. Law of quadratic reciprocity
    if a % 2 == 1:
        if (b % 4 == 1) or (a % 4 == 1):
            return _jacobi(b, a)
        else:
            return -1 * _jacobi(b, a)

def distinguish(X, Y, Z, p):
    X = int(X)
    Y = int(Y)
    Z = int(Z)
    p = int(p)

    s = -1
    if _jacobi(X, p) == 1 or _jacobi(Y, p) == 1:
        s = 1

    if _jacobi(Z, p) == s:
        return 1
    else:
        return 0

def random_distinguish(k):
    a = k.random_element()
    b = k.random_element()
    r = k.random_element()

    ga = g ** a
    gb = g ** b
    s = gb ** a

    random = distinguish(ga, gb, r, p)
    real = distinguish(ga, gb, s, p)

    return (random, real)

N = 1000
values = []
for i in range(N):
    values.append(random_distinguish(k))

mean_random = mean(map(lambda (x, y) : x, values))
mean_real = mean(map(lambda (x, y) : y, values))

print mean_random, mean_real, float(mean_random - mean_real)
