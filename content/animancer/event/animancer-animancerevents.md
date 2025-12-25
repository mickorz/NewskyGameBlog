---
title: "Animancer Events"
date: 2025-12-25
draft: false
---

# Animancer Events 官方文档

## 📋 目录
- [概述](#概述)
- [核心特性](#核心特性)
- [文档结构](#文档结构)
- [配置方式](#配置方式)
- [快速开始](#快速开始)
- [代码示例](#代码示例)
- [与其他事件系统的区别](#与其他事件系统的区别)
- [参考资料](#参考资料)

---

## 概述

**Animancer Events** 是 Animancer Pro 独有的强大事件系统，允许你注册函数在动画通过特定时间点时执行。

### 🎯 核心定义

> **"Animancer Events allow you to register a function to be executed when an animation passes a specific point in time."**
>
> 动画通过特定时间点时执行注册的函数。

---

## 核心特性

### ⭐ 专业版功能

| 特性 | Lite 版 | Pro 版 |
|------|---------|--------|
| **Animancer Events** | ❌ 不支持 | ✅ 完整支持 |
| **End Events** | ✅ 支持 | ✅ 支持 |
| **自定义淡入时长** | ❌ | ✅ |
| **运行时配置** | ❌ | ✅ |

### 🛠️ 配置方式

Animancer Events 提供**两种配置方式**：

#### 1. Inspector 配置（推荐）

```csharp
[SerializeField] private ClipTransition _AttackTransition;

void Start()
{
    // Inspector中配置的事件会自动应用
    _Animancer.Play(_AttackTransition);
}
```

**优点：**
- 可视化配置
- 易于调整时间点
- 支持 UnityEvents
- 无需编写代码

#### 2. 代码配置（灵活）

```csharp
void Start()
{
    var state = _Animancer.Play(_AttackClip);

    // 代码中添加事件
    state.Events(this).Add(0.5f, OnAttackHit);
    state.Events(this).OnEnd = OnAttackEnd;
}
```

**优点：**
- 运行时动态修改
- 支持 Lambda 表达式
- 完全程序化控制
- 可传递参数

---

## 文档结构

Animancer Events 系统包含以下子模块：

### 1. Usage（使用方法）

**内容：** 如何实现和使用 Animancer Events
- Inspector 配置步骤
- 代码配置方法
- 事件添加/移除
- 时间表示方式

### 2. Behaviour（行为机制）

**内容：** Events 的工作原理
- 事件触发时机
- 事件序列管理
- 循环动画中的事件
- 事件生命周期

### 3. Parameters（参数）

**内容：** 在 Events 中使用参数的方法
- Lambda 表达式传参
- 闭包捕获变量
- 上下文对象传递
- 参数化回调

### 4. Event Utilities（事件工具函数）

**内容：** 代码片段示例展示各类行为实现
- 常用工具方法
- 事件序列操作
- 批量事件管理
- 高级技巧

---

## 配置方式

### 方式1：Inspector 配置

**步骤：**

1. **创建 Transition**
```csharp
[SerializeField] private ClipTransition _AttackTransition;
```

2. **在 Inspector 中配置事件**
   - 选中 Transition
   - 展开 "Events" 面板
   - 点击 "+" 添加事件
   - 设置时间点（归一化时间 0-1）
   - 配置 UnityEvent 回调

3. **播放动画**
```csharp
_Animancer.Play(_AttackTransition); // 自动应用事件
```

### 方式2：代码配置

**步骤：**

1. **播放动画获取状态**
```csharp
var state = _Animancer.Play(_AttackClip);
```

2. **添加事件**
```csharp
// 使用绝对时间（秒）
state.Events(this).Add(0.5f, OnAttackHit);

// 使用归一化时间（0-1）
state.Events(this).AddNormalized(0.5f, OnAttackHit);
```

3. **实现回调**
```csharp
void OnAttackHit()
{
    Debug.Log("攻击命中！");
}
```

---

## 快速开始

### 示例1：简单的攻击事件

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 攻击事件示例
/// 演示如何在攻击动画中添加伤害判定事件
/// </summary>
public class AttackEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackTransition;
    [SerializeField] private WeaponCollider _WeaponCollider;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformAttack();
        }
    }

    void PerformAttack()
    {
        var state = _Animancer.Play(_AttackTransition);

        // 在动画50%时检测命中
        state.Events(this).AddNormalized(0.5f, OnAttackHit);

        // 动画结束时返回Idle
        state.Events(this).OnEnd = OnAttackEnd;
    }

    void OnAttackHit()
    {
        Debug.Log("执行攻击判定");
        _WeaponCollider.CheckHit();
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击结束");
        _Animancer.Play(_IdleClip);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### 示例2：Inspector 配置示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Inspector事件配置示例
/// 在Inspector中配置事件，代码中响应
/// </summary>
public class InspectorEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 在Inspector中为这个Transition配置事件
    [SerializeField] private ClipTransition _SkillTransition;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            // 播放时自动应用Inspector配置的事件
            _Animancer.Play(_SkillTransition);
        }
    }

    // 这些方法由Inspector配置的UnityEvents调用
    public void OnSkillCast()
    {
        Debug.Log("技能释放！");
    }

    public void OnSkillHit()
    {
        Debug.Log("技能命中！");
    }

    public void OnSkillEnd()
    {
        Debug.Log("技能结束！");
    }
}
```

---

## 代码示例

### 示例1：多事件组合

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 多事件组合示例
/// 在一个动画中添加多个事件
/// </summary>
public class MultipleEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _ComboAttack;

    [SerializeField] private AudioSource _AudioSource;
    [SerializeField] private ParticleSystem _SlashEffect;
    [SerializeField] private WeaponCollider _Weapon;

    void PerformComboAttack()
    {
        var state = _Animancer.Play(_ComboAttack);

        // 清除之前的事件
        state.Events(this).Clear();

        // 第一段攻击：0.3s
        state.Events(this).Add(0.3f, () => {
            _AudioSource.Play();
            _Weapon.EnableCollider();
        });

        // 命中判定：0.5s
        state.Events(this).Add(0.5f, () => {
            _Weapon.CheckHit(50); // 50点伤害
            _SlashEffect.Play();
        });

        // 禁用武器碰撞器：0.7s
        state.Events(this).Add(0.7f, () => {
            _Weapon.DisableCollider();
        });

        // 第二段攻击：1.2s
        state.Events(this).Add(1.2f, () => {
            _AudioSource.Play();
            _Weapon.EnableCollider();
        });

        // 第二段命中：1.4s
        state.Events(this).Add(1.4f, () => {
            _Weapon.CheckHit(80); // 80点伤害
            _SlashEffect.Play();
        });

        // 第二段结束：1.6s
        state.Events(this).Add(1.6f, () => {
            _Weapon.DisableCollider();
        });

        // 动画结束事件
        state.Events(this).OnEnd = () => {
            Debug.Log("连击结束");
            _Animancer.Play(_IdleClip);
        };
    }

    [SerializeField] private AnimationClip _IdleClip;
}

public class WeaponCollider : MonoBehaviour
{
    [SerializeField] private Collider _collider;

    public void EnableCollider() => _collider.enabled = true;
    public void DisableCollider() => _collider.enabled = false;

    public void CheckHit(int damage)
    {
        Debug.Log($"检测攻击命中，伤害: {damage}");
    }
}
```

### 示例2：事件参数传递

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 事件参数传递示例
/// 使用Lambda表达式传递参数
/// </summary>
public class EventParametersExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    void PerformAttack(string attackType, int damage, float critChance)
    {
        var state = _Animancer.Play(_AttackClip);

        // 使用Lambda捕获变量
        state.Events(this).AddNormalized(0.5f, () => {
            bool isCritical = Random.value < critChance;
            int finalDamage = isCritical ? damage * 2 : damage;

            OnAttackHit(attackType, finalDamage, isCritical);
        });
    }

    void OnAttackHit(string type, int damage, bool isCrit)
    {
        string critText = isCrit ? " (暴击!)" : "";
        Debug.Log($"{type}攻击: {damage}点伤害{critText}");
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            PerformAttack("轻攻击", 50, 0.2f);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            PerformAttack("重攻击", 100, 0.3f);
        }
    }
}
```

### 示例3：动态事件管理

```csharp
using Animancer;
using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// 动态事件管理示例
/// 根据游戏状态动态添加/移除事件
/// </summary>
public class DynamicEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _WalkTransition;

    private bool _enableFootsteps = true;
    private bool _enableDust = true;

    void Update()
    {
        // 切换脚步声
        if (Input.GetKeyDown(KeyCode.F))
        {
            _enableFootsteps = !_enableFootsteps;
            Debug.Log($"脚步声: {(_enableFootsteps ? "开启" : "关闭")}");
        }

        // 切换粉尘特效
        if (Input.GetKeyDown(KeyCode.D))
        {
            _enableDust = !_enableDust;
            Debug.Log($"粉尘特效: {(_enableDust ? "开启" : "关闭")}");
        }

        // 播放行走动画
        if (Input.GetKey(KeyCode.W))
        {
            PlayWalkWithDynamicEvents();
        }
    }

    void PlayWalkWithDynamicEvents()
    {
        var state = _Animancer.Play(_WalkTransition);

        // 清除旧事件
        state.Events(this).Clear();

        // 根据配置动态添加事件
        if (_enableFootsteps)
        {
            state.Events(this).AddNormalized(0.3f, PlayFootstepSound);
            state.Events(this).AddNormalized(0.7f, PlayFootstepSound);
        }

        if (_enableDust)
        {
            state.Events(this).AddNormalized(0.3f, SpawnDustEffect);
            state.Events(this).AddNormalized(0.7f, SpawnDustEffect);
        }
    }

    void PlayFootstepSound()
    {
        Debug.Log("播放脚步声");
    }

    void SpawnDustEffect()
    {
        Debug.Log("生成粉尘特效");
    }
}
```

---

## 与其他事件系统的区别

### 📊 Animancer Events vs End Events

| 特性 | Animancer Events | End Events |
|------|------------------|------------|
| **授权要求** | 需要 Pro 版本 | Lite/Pro 都支持 |
| **事件数量** | 无限制 | 仅1个（结束事件） |
| **时间点** | 任意时间点 | 仅动画结束时 |
| **运行时修改** | 支持 | 支持 |
| **配置方式** | Inspector + 代码 | Inspector + 代码 |

### 📊 Animancer Events vs Animation Events

| 特性 | Animancer Events | Animation Events |
|------|------------------|------------------|
| **系统来源** | Animancer 自定义 | Unity 内置 |
| **定义位置** | 独立于 Clip | AnimationClip 内部 |
| **灵活性** | 同一动画可有不同事件 | 所有使用该Clip共享事件 |
| **回调位置** | 任何位置 | 同一GameObject |
| **性能** | 高（无GC） | 较低（有GC） |
| **运行时修改** | 支持 | 不支持 |

---

## 参考资料

### 📚 详细文档（子章节）
1. **[Usage（使用方法）](https://kybernetik.com.au/animancer/docs/manual/events/animancer/usage)** - 如何实现 Animancer Events
2. **[Behaviour（行为机制）](https://kybernetik.com.au/animancer/docs/manual/events/animancer/behaviour)** - Events 的工作原理
3. **[Parameters（参数）](https://kybernetik.com.au/animancer/docs/manual/events/animancer/parameters/)** - 在 Events 中使用参数
4. **[Event Utilities（工具函数）](https://kybernetik.com.au/animancer/docs/manual/events/animancer/utilities)** - 代码片段和高级技巧

### 🔗 相关文档
- [Animancer Events 主页](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Animation Events](https://kybernetik.com.au/animancer/docs/manual/events/animation/)
- [End Events](https://kybernetik.com.au/animancer/docs/manual/events/end/)

### 💡 官方资源
- [Animancer 官方网站](https://kybernetik.com.au/animancer/)
- [Asset Store](https://assetstore.unity.com/packages/tools/animation/animancer-pro-116514)
- [Events 示例](https://kybernetik.com.au/animancer/docs/samples/)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+（需要 Pro 版本）
