import time
import random

from tqdm import tqdm  # Использую этот модуль, чтобы примерно понимать, сколько времени будет работать программа.
# Он рисует progress bar.


def elliptic_curve(x, y, p):
    """
    Проверяем, что точка (x, y) принадлежит эллиптической кривой y^2 = x^3 + ax + b в поле Z_p
    """
    return (y ** 2) % p == (x ** 3 + (a % p) * x + (b % p)) % p


def extended_euclidean_algorithm(a, b):
    """
    Возвращает (gcd, x, y): ax + by == gcd(a, b)
    Сложность: O(log b)
    Взято с https://habr.com/ru/post/335906/
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Возвращает m: (n * m) % p == 1
    Взято с https://habr.com/ru/post/335906/
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p


def points_sum(A, B, p):
    """
    Вычисляем алгебраическую сумму точек A, B в поле Z_p
    Алгоритм с https://habr.com/ru/post/335906/
    Возвращает R = (x_r, y_r) = A + B
    """
    if A == (0, 0):
        return B
    if B == (0, 0):
        return A
    if A[0] == B[0] and A[1] != B[1]:
       return 0, 0

    if A != B:
        m = ((A[1] - B[1]) * inverse_of(A[0] - B[0], p)) % p
    else:
        m = ((3 * A[0] ** 2 + a) * inverse_of(2 * A[1], p)) % p

    x_r = (m ** 2 - A[0] - A[1]) % p
    y_r = (A[1] + m * (x_r - A[0])) % p
    return x_r, -y_r % p


def get_point_order(point, p):
    """
    Вычисляем порядок точки point в поле Z_p
    """
    ans = 0
    found_point_order = False
    prev_point = point
    while not found_point_order:
        ans += 1
        point_sum = points_sum(point, prev_point, p)
        if point_sum == (0, 0):
            found_point_order = True
        else:
            prev_point = point
            point = point_sum
    return ans


if __name__ == '__main__':
    a = 0
    b = 7
    p = 31277

    start = time.time()
    points = []
    for x in tqdm(range(p)):
        for y in range(p):
            if elliptic_curve(x, y, p):
                points.append((x, y))

    curve_order = len(points)
    print('Curve order:', curve_order)

    point = random.choice(points)
    point_order = get_point_order(point, p)
    print('Point', point, 'order:', point_order)

    end = time.time()
    print('Time:', end - start, 's')

"""
100%|██████████| 31277/31277 [09:57<00:00, 52.36it/s]
Curve order: 31277
Point (12652, 1851) order: 96397
Time: 597.6167588233948 s
"""