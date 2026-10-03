from experiments.reproduce_r12_radix_spectra import calculate_radix_summary


def test_small_radix_reproduction_summary():
    summary = calculate_radix_summary(2, 2, 10)

    assert summary.radix == 2
    assert summary.max_position == 3
    assert summary.moduli_examined == 9
    assert summary.substitution_classes == 4
    assert summary.transposition_classes == 4
    assert summary.joint_classes == 4
    assert summary.zero_joint_moduli == 6
