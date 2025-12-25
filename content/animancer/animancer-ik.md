---
title: "Animancer IK（逆向动力学）"
date: 2025-12-25
draft: false
---

# Animancer IK（逆向动力学）官方文档

## 概述

**IK（Inverse Kinematics）** 允许直接控制骨骼链的末端位置（如手、脚），系统自动计算中间骨骼的旋转。

## Forward vs Inverse Kinematics

| 类型 | 控制方式 | 适用场景 |
|------|---------|---------|
| **Forward Kinematics** | 旋转每个骨骼 | 预制动画 |
| **Inverse Kinematics** | 指定末端位置 | 动态交互（抓取、脚步对齐） |

## 启用IK Pass

### 三层级控制

```csharp
// 1. Graph级别（全局）
_animancer.Graph.ApplyAnimatorIK = true;

// 2. Layer级别
_animancer.Layers[0].ApplyAnimatorIK = true;

// 3. State级别
var state = _animancer.Play(clip);
state.ApplyAnimatorIK = true;
```

### Foot IK（减少脚部滑动）

```csharp
// 启用Foot IK
_animancer.Graph.ApplyFootIK = true;

// 或在特定Layer/State上启用
_animancer.Layers[0].ApplyFootIK = true;
state.ApplyFootIK = true;
```

## OnAnimatorIK 回调

```csharp
public class IKController : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private Transform _ikTarget;

    private Animator _animator;

    void Awake()
    {
        _animator = GetComponent<Animator>();
        _animancer.Graph.ApplyAnimatorIK = true;
    }

    void OnAnimatorIK(int layerIndex)
    {
        if (_animator == null) return;

        // 设置右手IK目标
        _animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1f);
        _animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1f);

        _animator.SetIKPosition(AvatarIKGoal.RightHand, _ikTarget.position);
        _animator.SetIKRotation(AvatarIKGoal.RightHand, _ikTarget.rotation);

        // 视线IK
        _animator.SetLookAtWeight(1f);
        _animator.SetLookAtPosition(_ikTarget.position);
    }
}
```

## 动画曲线控制IK权重

```csharp
// 使用动画曲线控制IK影响
var animatedWeight = new AnimatedFloat(_animancer, "IKWeight");

void OnAnimatorIK(int layerIndex)
{
    // 从动画曲线获取权重（0=完全动画，1=完全IK）
    float weight = animatedWeight.Value;

    _animator.SetIKPositionWeight(AvatarIKGoal.RightHand, weight);
    _animator.SetIKPosition(AvatarIKGoal.RightHand, _ikTarget.position);
}
```

## 完整示例

```csharp
using Animancer;
using UnityEngine;

public class SimpleIKExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _reachClip;
    [SerializeField] private Transform _target;

    private Animator _animator;

    void Awake()
    {
        _animator = GetComponent<Animator>();

        // 启用IK Pass
        _animancer.Graph.ApplyAnimatorIK = true;

        // 播放动画并启用IK
        var state = _animancer.Play(_reachClip);
        state.ApplyAnimatorIK = true;
    }

    void OnAnimatorIK(int layerIndex)
    {
        if (_target == null) return;

        // 右手抓取目标
        _animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1f);
        _animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1f);
        _animator.SetIKPosition(AvatarIKGoal.RightHand, _target.position);
        _animator.SetIKRotation(AvatarIKGoal.RightHand, _target.rotation);
    }
}
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
