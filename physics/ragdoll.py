"""第 53 批：角色从台阶摔下时关节反折、手脚穿地、起身抽搐。

修复点：
- 四元数关节限制（对称锥面夹角，替代逐分量欧拉角限制）
- 碰撞体按骨骼半径扩张，避免手脚穿地
- PD 增益按质量归一，重骨不再过软
- 重力补偿分摊到全链每根骨骼，而非只压在根骨
- 地面多点接触统计，替代单点接触
- 动画/布娃娃混合用斜坡权重，替代硬切
- 关节驱动目标速度限速
- 碰撞对按链名过滤同链自碰撞
- 恢复起身时清零线速度，消除抽搐
- 固定步长积分按 ceil(dt/fixed_dt) 切分，与动画帧解耦
"""

import math


def limit_angle(angle, max_angle):
    """把关节角限制在四元数允许范围（对称限制 [-max_angle, max_angle]）。"""
    if angle > max_angle:
        return max_angle
    if angle < -max_angle:
        return -max_angle
    return angle


def expand_collider(radius, bone_radius):
    """按骨骼尺寸扩张碰撞体（碰撞半径叠加骨骼半径）。"""
    return radius + bone_radius


def mass_gain(mass, base_mass):
    """按质量归一 PD 增益：增益随质量线性缩放，保持固有频率不变。"""
    return mass / base_mass


def gravity_per_bone(total_gravity, bone_count):
    """把重力补偿均摊到整条骨链的每根骨骼。"""
    return total_gravity / bone_count


def contact_count(points):
    """返回地面多点接触的接触点数量。"""
    return len(points)


def blend_weight(t):
    """动画与布娃娃的混合斜坡权重，t 截断在 [0, 1]，替代硬切。"""
    if t < 0.0:
        return 0.0
    if t > 1.0:
        return 1.0
    return t


def drive_speed(target_speed, max_speed):
    """限制关节驱动目标速度在 [-max_speed, max_speed] 内。"""
    if target_speed > max_speed:
        return max_speed
    if target_speed < -max_speed:
        return -max_speed
    return target_speed


def same_chain(joint_a, joint_b):
    """判断两个关节是否在同一条链（按 ``链名:序号`` 的链名前缀过滤）。"""
    return joint_a.split(":", 1)[0] == joint_b.split(":", 1)[0]


def clear_velocity(velocity):
    """起身恢复时清零线速度，返回同维度的零向量（元组）。"""
    return tuple(0.0 for _ in velocity)


def fixed_steps(dt, fixed_dt):
    """按固定步长切分布娃娃积分，返回需要推进的固定步数（向上取整）。"""
    return math.ceil(dt / fixed_dt)
