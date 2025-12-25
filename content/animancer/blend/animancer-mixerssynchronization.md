# Animancer Mixer Synchronization 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/synchronization/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Mixer Synchronization（混合器同步）** 解决了动画混合中的一个关键问题：当混合不同长度的动画时,如果不进行同步,它们会逐渐失去相位,导致不自然的结果——例如在 Walk 到 Run 过渡时出现尴尬的拖步。

---

## 核心问题 (The Problem)

> **当混合不同长度的动画时,如果让它们正常播放,它们会失去同步。**

### 问题示例

```
场景：混合 Walk 和 Run 动画

Walk 循环: 1.2 秒/循环
Run 循环:  0.8 秒/循环

时间 0.0s:
  Walk: 左脚着地
  Run:  左脚着地
  混合结果: ✅ 左脚着地

时间 0.4s:
  Walk: 右脚着地
  Run:  左脚着地（已完成半个循环）
  混合结果: ❌ 拖步、滑步

时间 0.8s:
  Walk: 仍在第一个循环
  Run:  完成一个完整循环
  混合结果: ❌ 更严重的不同步
```

**视觉效果**：
- 左右脚不协调
- 出现滑步
- 移动看起来不自然

---

## Animancer 的解决方案

### 可选同步 (Optional Synchronization)

**核心理念**：与 Blend Trees 不同（总是同步所有动画）,Mixers 允许开发者**选择性地为每个状态启用同步**。

> **关键原则**：**同步对移动动画有利,但通常应该禁用 Idle 动画的同步。**

---

### 为什么 Idle 不应该同步？

```
场景：Idle 和 Walk 混合

Idle 循环: 2.0 秒
Walk 循环: 1.0 秒

如果强制同步：
  Idle 会被加速到 1.0 秒/循环
  结果: ❌ Idle 动画播放速度不自然（过快）

如果不同步：
  Idle 保持 2.0 秒/循环
  Walk 保持 1.0 秒/循环
  结果: ✅ 两个动画都以自然速度播放
```

---

## 代码配置 (Code Configuration)

### 全局配置

```csharp
using Animancer;
using UnityEngine;

public class GlobalSynchronizationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Start()
    {
        // 禁用全局自动同步（默认是启用的）
        MixerState.AutoSynchronizeChildren = false;
    }
}
```

---

### Per-Mixer 配置

```csharp
public static void OptionalSynchronizationExample(MixerState mixer)
{
    // 方法1：禁用整个 Mixer 的同步
    mixer.DontSynchronizeChildren();

    // 方法2：为特定子状态禁用同步
    mixer.DontSynchronize(mixer.GetChild(0)); // 禁用第一个子状态（通常是 Idle）

    // 方法3：为特定子状态启用同步
    mixer.Synchronize(mixer.GetChild(1)); // 启用第二个子状态
}
```

---

### 实际应用示例

```csharp
using Animancer;
using UnityEngine;

public class MixerSynchronizationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;

    private LinearMixerState _MixerState;

    void Start()
    {
        CreateAndConfigureMixer();
    }

    void CreateAndConfigureMixer()
    {
        // 创建 Mixer
        _MixerState = new LinearMixerState(_Animancer.Graph)
        {
            { _IdleClip, 0.0f },   // Child 0
            { _WalkClip, 0.5f },   // Child 1
            { _RunClip, 1.0f }     // Child 2
        };

        // 配置同步：
        // - Idle: 不同步（保持自然速度）
        // - Walk & Run: 同步（避免脚步不协调）

        _MixerState.DontSynchronize(_MixerState.GetChild(0)); // Idle

        _MixerState.Synchronize(_MixerState.GetChild(1)); // Walk
        _MixerState.Synchronize(_MixerState.GetChild(2)); // Run

        _MixerState.Play(_Animancer);
    }

    void Update()
    {
        float speed = GetCurrentSpeed();
        _MixerState.Parameter = speed;
    }

    float GetCurrentSpeed()
    {
        return Mathf.Abs(Input.GetAxis("Vertical"));
    }
}
```

---

## Inspector 控制

### Mixer Transition 中的 Sync 开关

**在 Inspector 中配置同步**：

```
LinearMixerTransition:
┌─────────────────────────────┐
│ Children (3):               │
│ ├─ [0] Idle                 │
│ │   ☐ Sync                  │ ← 不勾选（不同步）
│ ├─ [1] Walk                 │
│ │   ☑ Sync                  │ ← 勾选（同步）
│ └─ [2] Run                  │
│     ☑ Sync                  │ ← 勾选（同步）
└─────────────────────────────┘
```

**操作**：
- ✅ **勾选 Sync**：启用该子动画的同步
- ☐ **不勾选 Sync**：禁用该子动画的同步

---

## Foot Phase Synchronization（脚步相位同步）

### 高级同步技术

Unity 的 Humanoid 系统支持基于相位的复杂同步,用于不规则的行走循环（如跛行,具有多种行走循环变化）。

**特点**：
- 支持复杂的相位匹配
- 适合不规则的移动循环
- 需要 Humanoid Avatar

**当前状态**：
- Animancer **目前未暴露**此功能
- 实现复杂,依赖未公开的 Unity API
- 如果有足够需求,未来可能添加支持

---

## Real Speed（实际速度）

### Inspector 字段

当同步状态的内部 Playable 速度与其基础 `AnimancerState.Speed` 不同时,Inspector 中会显示 **"Real Speed"** 字段。

```
Inspector 显示:
┌────────────────────────────┐
│ State: Walk                │
│ Speed: 1.0                 │ ← 基础速度
│ Real Speed: 1.25           │ ← 实际播放速度（同步调整后）
│ Weight: 0.5                │
└────────────────────────────┘
```

**含义**：
- **Speed**：用户设置的速度
- **Real Speed**：同步系统调整后的实际速度

---

### 为什么会不同？

```
场景：同步 Idle（2.0s）和 Walk（1.0s）

同步目标：统一循环时长为 1.5s（平均值）

Idle:
  原始速度: 1.0
  原始时长: 2.0s
  实际速度: 1.33（加速以匹配 1.5s）

Walk:
  原始速度: 1.0
  原始时长: 1.0s
  实际速度: 0.67（减速以匹配 1.5s）
```

---

## 代码示例集合

### 示例1：基础同步配置

```csharp
using Animancer;
using UnityEngine;

public class BasicSynchronizationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;

    private LinearMixerState _MixerState;

    void Start()
    {
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;

        // 配置同步
        ConfigureSynchronization();
    }

    void ConfigureSynchronization()
    {
        // Child 0: Idle - 不同步
        _MixerState.DontSynchronize(_MixerState.GetChild(0));

        // Child 1, 2, 3: Walk, Run, Sprint - 同步
        for (int i = 1; i < _MixerState.ChildCount; i++)
        {
            _MixerState.Synchronize(_MixerState.GetChild(i));
        }

        Debug.Log("同步配置完成");
    }

    void Update()
    {
        float speed = GetCurrentSpeed();
        _MixerState.Parameter = speed;
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

### 示例2：条件同步

```csharp
using Animancer;
using UnityEngine;

public class ConditionalSynchronizationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;

    private LinearMixerState _MixerState;
    private bool _enableSynchronization = true;

    void Start()
    {
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;
    }

    void Update()
    {
        // 根据条件启用/禁用同步
        if (Input.GetKeyDown(KeyCode.S))
        {
            ToggleSynchronization();
        }

        float speed = GetCurrentSpeed();
        _MixerState.Parameter = speed;
    }

    void ToggleSynchronization()
    {
        _enableSynchronization = !_enableSynchronization;

        if (_enableSynchronization)
        {
            // 启用同步（除了 Idle）
            for (int i = 1; i < _MixerState.ChildCount; i++)
            {
                _MixerState.Synchronize(_MixerState.GetChild(i));
            }
            Debug.Log("同步已启用");
        }
        else
        {
            // 禁用所有同步
            _MixerState.DontSynchronizeChildren();
            Debug.Log("同步已禁用");
        }
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

### 示例3：2D Mixer 同步配置

```csharp
using Animancer;
using UnityEngine;

public class DirectionalMixerSyncExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _ForwardClip;
    [SerializeField] private AnimationClip _BackClip;
    [SerializeField] private AnimationClip _LeftClip;
    [SerializeField] private AnimationClip _RightClip;

    private DirectionalMixerState _MixerState;

    void Start()
    {
        CreateMixerWithSynchronization();
    }

    void CreateMixerWithSynchronization()
    {
        _MixerState = new DirectionalMixerState(_Animancer.Graph)
        {
            // Child 0: Idle（中心）
            { _IdleClip, Vector2.zero },

            // Child 1-4: 四方向移动
            { _ForwardClip, new Vector2(0, 1) },
            { _RightClip, new Vector2(1, 0) },
            { _BackClip, new Vector2(0, -1) },
            { _LeftClip, new Vector2(-1, 0) }
        };

        // 配置同步：
        // Idle（Child 0）不同步
        _MixerState.DontSynchronize(_MixerState.GetChild(0));

        // 所有移动动画（Child 1-4）同步
        for (int i = 1; i < _MixerState.ChildCount; i++)
        {
            _MixerState.Synchronize(_MixerState.GetChild(i));
        }

        _MixerState.Play(_Animancer);
    }

    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        _MixerState.Parameter = new Vector2(horizontal, vertical);
    }
}
```

---

### 示例4：监控实际速度

```csharp
using Animancer;
using UnityEngine;

public class RealSpeedMonitorExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;

    private LinearMixerState _MixerState;

    void Start()
    {
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;

        // 配置同步
        _MixerState.DontSynchronize(_MixerState.GetChild(0)); // Idle
        for (int i = 1; i < _MixerState.ChildCount; i++)
        {
            _MixerState.Synchronize(_MixerState.GetChild(i));
        }
    }

    void Update()
    {
        float speed = GetCurrentSpeed();
        _MixerState.Parameter = speed;

        // 监控每个子状态的实际速度
        MonitorChildSpeeds();
    }

    void MonitorChildSpeeds()
    {
        for (int i = 0; i < _MixerState.ChildCount; i++)
        {
            var child = _MixerState.GetChild(i);
            if (child.Weight > 0.01f) // 只显示有权重的状态
            {
                // 注意：实际速度可能与 child.Speed 不同
                Debug.Log($"Child {i} ({child.Clip.name}): " +
                          $"Speed = {child.Speed:F2}, " +
                          $"Weight = {child.Weight:F2}");
            }
        }
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

## 最佳实践建议

### 1. **Idle 动画不同步**

```csharp
// ✅ 推荐：Idle 不同步
_MixerState.DontSynchronize(_MixerState.GetChild(0)); // Idle

// ❌ 不推荐：所有动画都同步
_MixerState.SynchronizeChildren(); // Idle 会被加速/减速
```

---

### 2. **移动动画应同步**

```csharp
// ✅ 推荐：所有移动动画同步
for (int i = 1; i < _MixerState.ChildCount; i++)
{
    _MixerState.Synchronize(_MixerState.GetChild(i));
}
```

**原因**：避免脚步不协调、滑步等问题。

---

### 3. **使用 Inspector 配置**

```csharp
// ✅ 推荐：在 Transition 中配置同步
// 通过 Inspector 的 Sync 复选框
// 更直观,不需要代码

// ⚠️ 代码配置：灵活,但需要维护
_MixerState.Synchronize(child);
```

---

### 4. **监控同步效果**

```csharp
// ✅ 在开发时检查同步是否生效
void OnGUI()
{
    for (int i = 0; i < _MixerState.ChildCount; i++)
    {
        var child = _MixerState.GetChild(i);
        GUILayout.Label($"{child.Clip.name}: " +
                       $"Weight = {child.Weight:F2}, " +
                       $"Speed = {child.Speed:F2}");
    }
}
```

---

## 同步算法详解

### 基础同步机制

**目标**：使所有同步的动画以相同的相对速度播放。

```
示例：
  Walk: 1.0s/循环, Weight = 0.3
  Run:  0.8s/循环, Weight = 0.7

目标循环时长 = (1.0 × 0.3) + (0.8 × 0.7) = 0.86s

Walk 调整后速度 = 1.0 / 0.86 = 1.16x
Run 调整后速度 = 0.8 / 0.86 = 0.93x

结果：两个动画以相同的相对速度播放
```

---

### 非同步动画的行为

```csharp
// 非同步动画保持原始速度
_MixerState.DontSynchronize(_IdleClip);

// Idle 以 Speed = 1.0 播放,不受其他动画影响
```

---

## 常见问题 FAQ

### Q1: Blend Tree 和 Mixer 的同步有什么区别？

**A**:

| 特性 | Blend Tree | Mixer |
|------|-----------|-------|
| **同步方式** | 所有动画强制同步 | 可选择性同步 |
| **Idle 处理** | 也会被同步（不自然） | 可以不同步 |
| **灵活性** | 低 | 高 |

---

### Q2: 为什么 Idle 被同步后看起来不自然？

**A**: 因为 Idle 通常比移动动画慢。

```
Walk: 1.0s/循环
Idle: 3.0s/循环

如果同步：
  Idle 会被加速 3 倍,看起来很急促
```

---

### Q3: 所有移动动画都应该同步吗？

**A**: 通常是的,但有例外。

```csharp
// ✅ 同步：常规移动动画
Walk, Run, Sprint

// ⚠️ 可能不同步：特殊移动
Sneak（潜行）: 可能速度差异很大
Limp（跛行）: 不规则循环,可能需要特殊处理
```

---

### Q4: 如何判断同步是否生效？

**A**:

```csharp
// 方法1：Inspector 查看 Real Speed
// Real Speed ≠ Speed → 同步生效

// 方法2：运行时检查
void CheckSynchronization(AnimancerState state)
{
    // 如果 Playable 速度与 State 速度不同,说明同步生效
    Debug.Log($"State Speed: {state.Speed}");
    // Real Speed 需要通过 Playable API 获取（高级）
}
```

---

### Q5: 可以动态切换同步吗？

**A**: 可以！

```csharp
void ToggleSynchronization(bool enable)
{
    if (enable)
    {
        _MixerState.Synchronize(_MixerState.GetChild(1));
    }
    else
    {
        _MixerState.DontSynchronize(_MixerState.GetChild(1));
    }
}
```

---

### Q6: Foot Phase Synchronization 什么时候会支持？

**A**: 当前未确定。

- 依赖未公开的 Unity API
- 实现复杂
- 如果有足够需求,可能在未来版本添加

**替代方案**：
- 使用标准同步
- 确保动画循环对齐
- 使用 IK 系统辅助

---

## 总结

### 核心要点

1. **同步的目的**
   - 避免不同长度动画失去相位
   - 防止脚步不协调、滑步等问题

2. **可选同步机制**
   - Idle：不同步（保持自然速度）
   - 移动动画：同步（避免脚步问题）
   - 完全由开发者控制

3. **配置方式**
   - **Inspector**：Sync 复选框（推荐）
   - **代码**：`Synchronize()` 和 `DontSynchronize()`

4. **Real Speed**
   - 显示同步调整后的实际速度
   - 与用户设置的 Speed 可能不同

### 下一步学习

- 📖 深入学习 **Mixer Creation**（创建方法）
- 🎨 探索 **IK 系统**与同步的结合
- 📚 了解 **Root Motion** 在同步中的作用
- 🔍 查看实际项目中的同步配置案例

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/synchronization/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
