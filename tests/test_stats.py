from calculadora_completa import compute_statistics


def test_compute_statistics_basic():
    data = [12, 7.5, 3, 9.25, 14]
    stats = compute_statistics(data)
    assert stats['n'] == 5
    assert abs(stats['mean'] - 9.15) < 1e-8
    assert stats['q2'] == 9.25
