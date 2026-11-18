import pytest
from physics import ragdoll as mod

CASES = [
    ("limit_over", "m.limit_angle(2.0, 1.0) == approx(1.0)"),
    ("limit_inside", "m.limit_angle(0.5, 1.0) == approx(0.5)"),
    ("limit_negative", "m.limit_angle(-2.0, 1.0) == approx(-1.0)"),
    ("collider_grow", "m.expand_collider(0.2, 0.1) == approx(0.3)"),
    ("gain_half", "m.mass_gain(2.0, 4.0) == approx(0.5)"),
    ("gravity_split", "m.gravity_per_bone(10.0, 2) == approx(5.0)"),
    ("contacts_two", "m.contact_count([(0, 0), (1, 1)]) == 2"),
    ("blend_start", "m.blend_weight(0.0) == approx(0.0)"),
    ("blend_end", "m.blend_weight(1.0) == approx(1.0)"),
    ("drive_clamp", "m.drive_speed(10.0, 3.0) == approx(3.0)"),
    ("drive_inside", "m.drive_speed(2.0, 3.0) == approx(2.0)"),
    ("chain_true", "m.same_chain('arm:1', 'arm:2') is True"),
    ("chain_false", "m.same_chain('arm:1', 'leg:1') is False"),
    ("clear_zero", "m.clear_velocity((1.0, 2.0)) == (0.0, 0.0)"),
    ("steps_two", "m.fixed_steps(0.033, 0.016) == 3")
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
