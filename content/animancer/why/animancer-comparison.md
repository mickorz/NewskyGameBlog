---
title: "Animancer - Comparison 对比总览"
date: 2025-12-25
draft: false
---

# Animancer - Comparison 对比总览

## 📋 目录
- [概述](#概述)
- [四大对比主题](#四大对比主题)
- [参考资料](#参考资料)

---

## 概述

本系列文档通过**实战场景**对比Mecanim和Animancer的实现方式，展示两者在实际开发中的差异。

---

## 四大对比主题

### 1. Playing（播放动画）

> **"How to play a single animation (with or without scripting)."**

**对比内容：**
- 无脚本播放方式
- 脚本控制播放
- 理解与维护
- 复用性

**核心差异：**
```csharp
// Mecanim: 需要Controller配置
_animator.Play("Walk");

// Animancer: 直接播放
_animancer.Play(_walk);
```

📖 [animancer-playing]({{< ref "animancer-playing.md" >}})

---

### 2. Waiting（等待动画）

> **"How to wait until an animation ends before running some code."**

**对比内容：**
- 状态信息检查
- NormalizedTime监控
- StateMachineBehaviour
- End Events
- Coroutines

**核心差异：**
```csharp
// Mecanim: 复杂的状态检查
while (true)
{
    var info = _animator.GetCurrentAnimatorStateInfo(0);
    if (info.IsName("Attack") && info.normalizedTime >= 1f)
        break;
    yield return null;
}

// Animancer: 简单的事件
var state = _animancer.Play(_attack);
state.Events.OnEnd = OnComplete;
```

📖 [animancer-waiting]({{< ref "animancer-waiting.md" >}})

---

### 3. Speed and Time（速度和时间）

> **"How to manipulate the speed and time of animations."**

**对比内容：**
- 固定速度设置
- 动态速度调整
- 时间控制
- 常量时间控制

**核心差异：**
```csharp
// Mecanim: 需要参数
_animator.SetFloat("SpeedMultiplier", 2f);

// Animancer: 直接设置
var state = _animancer.Play(_walk);
state.Speed = 2f;
```

📖 [animancer-speedandtime]({{< ref "animancer-speedandtime.md" >}})

---

### 4. Weapon Animations（武器动画）

> **"How to set up a system where each weapon has its own attack animations."**

**对比内容：**
- 武器系统架构
- 动画覆盖方式
- 武器切换实现
- 内存管理

**核心差异：**
```csharp
// Mecanim: AnimatorOverrideController
var overrideController = new AnimatorOverrideController(baseController);
overrideController["PlaceholderAttack"] = swordAttack;
_animator.runtimeAnimatorController = overrideController;

// Animancer: 直接播放
_animancer.Play(weapon.AttackClip);
```

📖 [animancer-weaponanimations]({{< ref "animancer-weaponanimations.md" >}})

---

## 对比总结表

| 场景 | Mecanim复杂度 | Animancer复杂度 | 优势方 |
|------|--------------|----------------|--------|
| **播放动画** | 高（需要Controller配置） | 低（1行代码） | Animancer |
| **等待结束** | 中（状态检查或Behaviour） | 低（End Events） | Animancer |
| **速度控制** | 中（需要参数） | 低（直接设置） | Animancer |
| **武器系统** | 高（Override Controller） | 低（直接播放） | Animancer |

---

## 快速决策

### 选择Mecanim的情况
- ✅ 已有大量Controller资产
- ✅ 团队不熟悉编程
- ✅ 简单固定的动画流程

### 选择Animancer的情况
- ✅ 需要灵活的动画控制
- ✅ 复杂的游戏逻辑
- ✅ 团队有编程能力
- ✅ 需要快速迭代

---

## 参考资料

### 📚 详细对比文档
- [animancer-playing]({{< ref "animancer-playing.md" >}})
- [animancer-waiting]({{< ref "animancer-waiting.md" >}})
- [animancer-speedandtime]({{< ref "animancer-speedandtime.md" >}})
- [animancer-weaponanimations]({{< ref "animancer-weaponanimations.md" >}})

### 🎯 Why系列
- [animancer-why]({{< ref "animancer-why.md" >}})
- [animancer-simplicity]({{< ref "animancer-simplicity.md" >}})
- [animancer-reliability]({{< ref "animancer-reliability.md" >}})

### ⚡ 性能分析
- [animancer-performance]({{< ref "animancer-performance.md" >}})

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
