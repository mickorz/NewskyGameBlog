---
title: "Animancer Blending"
date: 2025-12-25
draft: false
---

# Animancer Blending 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Blending（混合）** 是在多个动画之间进行插值以将它们组合成单一输出的过程。

虽然动画通常像**有限状态机（Finite State Machine）**一样工作，但混合允许多个动画同时进行插值，而不是在状态之间进行排他性切换。

---

## 核心概念 (Key Concept)

> **混合是在多个动画之间进行插值，将它们组合成单一输出的过程。**

这意味着角色可以同时：
- 在 Walk 和 Run 之间混合
- 在单独的图层上播放挥手动画（上半身）
- 淡入到 Standing 状态
- 所有这些都同时发生，而不是互斥的状态

---

## 三种主要混合类型 (Three Main Blending Types)

### 1. **Fading（淡入淡出）**

**定义**：在一段时间内平滑过渡到另一个动画，而不是瞬间切换。

**用途**：
- 当动画在连接点没有完美对齐时
- 需要平滑过渡效果
- 避免动作突兀切换

**示例场景**：
```csharp
// 从 Idle 平滑过渡到 Walk
_Animancer.Play(_WalkAnimation, fadeDuration: 0.25f);
```

**关键特性**：
- 基于时间的渐变
- 可控制的淡入持续时间
- 避免动画切换时的跳跃感

---

### 2. **Layers（图层）**

**定义**：允许多个动画同时播放，实现身体不同部位的独立控制。

**用途**：
- 上半身和下半身独立动画
- 叠加特殊效果动画
- 局部动画覆盖

**示例场景**：
```csharp
// Layer 0: 下半身行走
_Animancer.Layers[0].Play(_WalkAnimation);

// Layer 1: 上半身挥手
_Animancer.Layers[1].Play(_WaveAnimation);
```

**关键特性**：
- 多层并行播放
- 独立权重控制
- Avatar Mask 支持（部分身体控制）

---

### 3. **Mixers（混合器）**

**定义**：基于参数在多个动画之间进行插值，实现中间状态。

**用途**：
- 速度混合（Walk ↔ Run）
- 方向混合（8方向移动）
- 瞄准角度混合

**示例场景**：
```csharp
// 1D Mixer: 根据速度混合 Walk 和 Run
LinearMixerState mixer = _Animancer.Play(_SpeedMixer);
mixer.Parameter = currentSpeed; // 0-1 之间的值
```

**关键特性**：
- 参数驱动的动画混合
- 支持 1D 和 2D 混合
- 平滑的中间状态

---

## 权重系统 (Weight System)

**所有动画和图层都使用 `AnimancerNode.Weight` 属性**（范围 0-1）来决定它们对最终混合结果的贡献。

### 权重计算示例

**单个动画**：
```csharp
state.Weight = 1.0f; // 100% 影响
state.Weight = 0.5f; // 50% 影响
state.Weight = 0.0f; // 无影响
```

**两个动画混合**：
```csharp
// 各占 50% 权重时，精确混合 50%
idleState.Weight = 0.5f;
walkState.Weight = 0.5f;
// 最终结果 = 50% Idle + 50% Walk
```

**三个动画混合**：
```csharp
// 权重会自动归一化
idleState.Weight = 0.2f;  // 20%
walkState.Weight = 0.3f;  // 30%
runState.Weight = 0.5f;   // 50%
// 最终结果 = 20% Idle + 30% Walk + 50% Run
```

---

## 组合使用示例 (Combined Usage Example)

一个角色可以同时执行多种混合操作：

```csharp
public class CharacterBlendingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // Mixers
    [SerializeField] private LinearMixerTransition _MovementMixer; // Walk ↔ Run

    // Layers
    [SerializeField] private ClipTransition _UpperBodyWave;

    // Fading
    [SerializeField] private ClipTransition _Standing;

    void Update()
    {
        // Layer 0: 使用 Mixer 混合 Walk 和 Run
        var movementState = _Animancer.Layers[0].Play(_MovementMixer);
        movementState.Parameter = GetCurrentSpeed(); // 0-1

        // Layer 1: 上半身挥手（独立图层）
        if (Input.GetKeyDown(KeyCode.Space))
        {
            _Animancer.Layers[1].Play(_UpperBodyWave);
        }

        // Fading: 当停止移动时，淡入到 Standing
        if (Input.GetKeyDown(KeyCode.S))
        {
            _Animancer.Play(_Standing, fadeDuration: 0.5f);
        }
    }

    float GetCurrentSpeed()
    {
        // 返回 0-1 之间的速度值
        return Mathf.Clamp01(GetComponent<Rigidbody>().velocity.magnitude / maxSpeed);
    }
}
```

**这个例子同时使用了三种混合类型**：
1. **Mixer**：下半身 Walk ↔ Run 动态混合
2. **Layer**：上半身独立播放挥手动画
3. **Fading**：平滑过渡到 Standing 状态

---

## 混合类型对比表

| 混合类型 | 用途 | 参数控制 | 时间控制 | 并行播放 |
|---------|------|---------|---------|---------|
| **Fading** | 平滑过渡 | ❌ | ✅ | ❌ |
| **Layers** | 局部动画 | ❌ | ❌ | ✅ |
| **Mixers** | 参数插值 | ✅ | ❌ | ❌ |

---

## 相关文档主题 (Related Documentation Topics)

### 1. **Fading（淡入淡出）**
- 详细介绍淡入淡出机制
- Fade Modes（淡入模式）
- Custom Fading（自定义淡入）
- Fading Sequences（淡入序列）

### 2. **Layers（图层）**
- 图层系统详解
- Avatar Mask 使用
- Weighted Layers（加权图层）

### 3. **Mixers（混合器）**
- Linear Mixer（1D 混合）
- 2D Mixer（2D 混合）
- Mixer Creation（混合器创建）
- Mixer Synchronization（混合器同步）

### 4. **Finite State Machines（有限状态机）**
- 状态机模式
- 与混合的结合使用

---

## 最佳实践建议

### 1. **选择合适的混合类型**

**使用 Fading 的情况**：
- ✅ 动画切换需要平滑过渡
- ✅ 避免动作突兀
- ✅ 连接点不完美对齐

**使用 Layers 的情况**：
- ✅ 上下半身独立控制
- ✅ 叠加特效动画
- ✅ 局部动画覆盖

**使用 Mixers 的情况**：
- ✅ 基于参数的动态混合
- ✅ 需要中间状态
- ✅ 连续变化的动画（如速度）

---

### 2. **权重管理技巧**

```csharp
// ❌ 错误：权重超过 1 会导致不正确的混合
state.Weight = 1.5f;

// ✅ 正确：保持权重在 0-1 范围
state.Weight = Mathf.Clamp01(calculatedWeight);

// ✅ 推荐：使用归一化权重
float totalWeight = state1.Weight + state2.Weight;
state1.Weight /= totalWeight;
state2.Weight /= totalWeight;
```

---

### 3. **性能优化建议**

**避免过多混合**：
```csharp
// ❌ 不推荐：同时混合过多动画
for (int i = 0; i < 10; i++)
{
    states[i].Weight = 0.1f; // 10 个动画同时混合
}

// ✅ 推荐：限制同时活跃的动画数量
int maxActiveStates = 3;
// 只混合最重要的 3 个动画
```

**及时停止不需要的动画**：
```csharp
// ✅ 权重为 0 时停止播放
if (state.Weight <= 0.01f)
{
    state.Stop();
}
```

---

### 4. **调试混合问题**

**可视化权重**：
```csharp
void OnGUI()
{
    foreach (var state in _Animancer.States)
    {
        GUILayout.Label($"{state.Clip.name}: Weight = {state.Weight:F2}");
    }
}
```

**检查总权重**：
```csharp
float totalWeight = 0;
foreach (var state in _Animancer.States)
{
    totalWeight += state.Weight;
}
Debug.Log($"Total Weight: {totalWeight}"); // 应该接近 1.0
```

---

## 代码示例集合

### 示例1：基础淡入淡出

```csharp
using Animancer;
using UnityEngine;

public class BasicFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Idle;
    [SerializeField] private ClipTransition _Walk;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.W))
        {
            // 0.25 秒淡入到 Walk
            _Animancer.Play(_Walk, fadeDuration: 0.25f);
        }
        else if (Input.GetKeyDown(KeyCode.I))
        {
            // 0.25 秒淡入到 Idle
            _Animancer.Play(_Idle, fadeDuration: 0.25f);
        }
    }
}
```

---

### 示例2：图层独立控制

```csharp
using Animancer;
using UnityEngine;

public class LayerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // Layer 0: 下半身
    [SerializeField] private ClipTransition _Run;

    // Layer 1: 上半身
    [SerializeField] private ClipTransition _Shoot;

    void Start()
    {
        // 设置 Layer 1 使用 Avatar Mask（只影响上半身）
        // 这需要在 Inspector 中配置 Avatar Mask
    }

    void Update()
    {
        // Layer 0: 下半身奔跑
        _Animancer.Layers[0].Play(_Run);

        // Layer 1: 上半身射击
        if (Input.GetMouseButton(0))
        {
            _Animancer.Layers[1].Play(_Shoot);
        }
    }
}
```

---

### 示例3：Mixer 参数控制

```csharp
using Animancer;
using UnityEngine;

public class MixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;

    private LinearMixerState _MixerState;

    void Start()
    {
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;
    }

    void Update()
    {
        // 根据移动速度动态调整混合参数
        float speed = GetMovementSpeed();
        _MixerState.Parameter = speed; // 0 = Walk, 1 = Run
    }

    float GetMovementSpeed()
    {
        // 返回 0-1 之间的标准化速度
        Vector3 velocity = GetComponent<Rigidbody>().velocity;
        float currentSpeed = velocity.magnitude;
        float maxSpeed = 10f;
        return Mathf.Clamp01(currentSpeed / maxSpeed);
    }
}
```

---

### 示例4：组合混合（完整示例）

```csharp
using Animancer;
using UnityEngine;

public class AdvancedBlendingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // Mixers
    [SerializeField] private LinearMixerTransition _LowerBodyMixer;

    // Upper Body Clips
    [SerializeField] private ClipTransition _Aim;
    [SerializeField] private ClipTransition _Reload;

    private LinearMixerState _LowerBodyState;

    void Start()
    {
        // Layer 0: 下半身移动混合
        _LowerBodyState = _Animancer.Layers[0].Play(_LowerBodyMixer) as LinearMixerState;

        // Layer 1: 上半身动作（需要配置 Avatar Mask）
        _Animancer.Layers[1].Weight = 1.0f;
    }

    void Update()
    {
        // 1. Mixer: 下半身速度混合
        UpdateLowerBodyMovement();

        // 2. Layer: 上半身独立动作
        UpdateUpperBodyActions();
    }

    void UpdateLowerBodyMovement()
    {
        float speed = GetCurrentSpeed();
        _LowerBodyState.Parameter = speed;
    }

    void UpdateUpperBodyActions()
    {
        // 瞄准
        if (Input.GetMouseButton(1))
        {
            _Animancer.Layers[1].Play(_Aim);
        }

        // 装填（带淡入）
        if (Input.GetKeyDown(KeyCode.R))
        {
            _Animancer.Layers[1].Play(_Reload, fadeDuration: 0.2f);
        }
    }

    float GetCurrentSpeed()
    {
        // 实际项目中的速度计算逻辑
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

## 常见问题 FAQ

### Q1: Blending 和 Transition 有什么区别？

**A**:
- **Transition（过渡）**：动画切换时的配置（如淡入时长、速度等）
- **Blending（混合）**：多个动画同时播放并插值的机制

Transition 是 Blending 的一种实现方式（Fading）。

---

### Q2: 为什么需要使用 Layers？

**A**: Layers 允许身体不同部位独立播放动画，例如：
- 下半身奔跑 + 上半身射击
- 全身跳跃 + 面部表情
- 基础动作 + 受伤效果叠加

使用 Avatar Mask 可以精确控制每个 Layer 影响的骨骼。

---

### Q3: Mixer 的 Parameter 范围是多少？

**A**:
- **Linear Mixer (1D)**：通常是 0-1，但可以自定义范围
- **2D Mixer**：X 和 Y 参数都可以自定义范围

在配置 Mixer 时，Threshold（阈值）定义了每个动画对应的参数值。

---

### Q4: 如何避免混合时的抖动？

**A**:
1. **使用足够的淡入时长**：
   ```csharp
   _Animancer.Play(_Animation, fadeDuration: 0.25f); // 推荐 0.2-0.5 秒
   ```

2. **确保动画帧率一致**：
   - 避免混合 30fps 和 60fps 动画

3. **检查骨骼对齐**：
   - 确保混合的动画使用相同的骨骼结构

---

### Q5: 可以同时使用多少个 Layers？

**A**:
- Animancer 默认支持 **4 个 Layers**（与 Unity Animator 相同）
- 可以通过代码增加：
  ```csharp
  _Animancer.Layers.SetCount(8); // 增加到 8 个图层
  ```
- **性能建议**：通常 2-4 个 Layers 足够，过多会影响性能

---

### Q6: 如何调试混合权重问题？

**A**: 使用 Animancer 的内置调试功能：

```csharp
// 1. Inspector 中实时查看
// 运行时在 Inspector 中展开 AnimancerComponent 可以看到所有 States 的 Weight

// 2. 代码输出
void OnGUI()
{
    foreach (var state in _Animancer.States)
    {
        if (state.Weight > 0)
        {
            GUILayout.Label($"{state.Clip.name}: {state.Weight:F2}");
        }
    }
}

// 3. 使用 Animancer Tools
// Window -> Animancer -> Inspector Settings -> Show Weight
```

---

## 总结

### 核心要点

1. **三种混合类型**
   - **Fading**：时间驱动的平滑过渡
   - **Layers**：并行播放，局部控制
   - **Mixers**：参数驱动的动态混合

2. **权重系统**
   - 所有混合基于 0-1 的权重值
   - 权重决定动画对最终结果的贡献
   - 可以组合使用多种混合类型

3. **灵活组合**
   - 可以同时使用 Fading + Layers + Mixers
   - 每个 Layer 可以独立使用 Mixer
   - 权重控制提供精确的混合效果

4. **性能考虑**
   - 限制同时活跃的动画数量
   - 及时停止权重为 0 的动画
   - 合理使用 Layers 数量

### 下一步学习

- 📖 深入学习 **Fading** 的各种模式和自定义方法
- 🎨 探索 **Layers** 的 Avatar Mask 配置
- 📚 了解 **Mixers** 的创建和同步机制
- 🔍 查看官方示例了解实际应用

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
