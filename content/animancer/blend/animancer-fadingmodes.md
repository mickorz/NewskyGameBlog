---
title: "Animancer Fading Modes"
date: 2025-12-25
draft: false
---

# Animancer Fading Modes 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/fading/modes/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**FadeMode（淡入模式）** 是 Animancer 中控制淡入淡出行为的重要参数。它决定了淡入持续时间如何被解释和应用。

`Play` 方法接受一个可选的 `FadeMode` 参数，如果不指定则默认使用 `FadeMode.FixedSpeed`。

---

## 基础用法 (Basic Usage)

```csharp
// 方式1：使用默认模式（FixedSpeed）
_Animancer.Play(clip, 0.25f);

// 方式2：显式指定模式（等价于方式1）
_Animancer.Play(clip, 0.25f, FadeMode.FixedSpeed);

// 方式3：使用其他模式
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);
```

---

## 淡入模式分类 (Fade Mode Categories)

### 1. **Fixed Modes（固定模式）**

**定义**：淡入持续时间**独立于**动画长度。

**特点**：
- ✅ 时长固定，不受动画长度影响
- ⚠️ 如果淡入时长超过动画长度，可能导致淡入未完成
- 💡 适合淡入时长已知且稳定的场景

**示例**：
```csharp
// 固定 0.25 秒淡入，无论动画长度
_Animancer.Play(clip, 0.25f, FadeMode.FixedSpeed);

// 动画长度 = 0.5 秒
// 实际淡入时长 = 0.25 秒 ✅

// 动画长度 = 0.1 秒
// 实际淡入时长 = 0.25 秒 ⚠️（超过动画长度！）
```

---

### 2. **Normalized Modes（归一化模式）**

**定义**：淡入持续时间**基于**动画长度计算。

**特点**：
- ✅ 自动适应动画长度
- ✅ 确保淡入在动画播放期间完成
- 💡 适合不同长度动画使用统一比例的场景

**时长范围**：通常在 **0-1** 之间（代表动画长度的百分比）

**示例**：
```csharp
// 淡入时长 = 动画长度 × 0.2（20%）
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);

// 动画长度 = 2 秒
// 实际淡入时长 = 2 × 0.2 = 0.4 秒 ✅

// 动画长度 = 0.5 秒
// 实际淡入时长 = 0.5 × 0.2 = 0.1 秒 ✅
```

---

## 主要淡入模式详解 (Main Fade Modes)

### 1. **FadeMode.FixedSpeed**（默认）

**定义**：固定速度淡入，时长不受动画长度影响。

**公式**：
```
实际淡入时长 = 指定的 fadeDuration（秒）
```

**代码示例**：
```csharp
// 固定 0.3 秒淡入
_Animancer.Play(clip, 0.3f, FadeMode.FixedSpeed);
// 或省略模式参数（默认）
_Animancer.Play(clip, 0.3f);
```

**适用场景**：
- ✅ 已知合适的淡入时长
- ✅ 所有动画长度相似
- ✅ 需要统一的淡入体验

**注意事项**：
```csharp
// ⚠️ 问题：淡入时长可能超过动画长度
AnimationClip shortClip; // 长度 0.2 秒
_Animancer.Play(shortClip, 0.5f, FadeMode.FixedSpeed);
// 淡入时长 0.5 秒 > 动画长度 0.2 秒
// 结果：动画播放完毕，淡入仍未完成
```

---

### 2. **FadeMode.NormalizedSpeed**

**定义**：淡入时长基于**新动画的长度**计算。

**公式**：
```
实际淡入时长 = 新动画长度 × fadeDuration
```

**代码示例**：
```csharp
// 淡入时长 = 新动画长度的 20%
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);

// 示例1：新动画长度 = 3 秒
// 实际淡入时长 = 3 × 0.2 = 0.6 秒

// 示例2：新动画长度 = 1 秒
// 实际淡入时长 = 1 × 0.2 = 0.2 秒
```

**适用场景**：
- ✅ 动画长度差异较大
- ✅ 希望淡入时长与动画长度成比例
- ✅ 长动画使用长淡入，短动画使用短淡入

**实际应用**：
```csharp
public class NormalizedSpeedExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _ShortClip;  // 1 秒
    [SerializeField] private AnimationClip _LongClip;   // 5 秒

    void PlayWithProportionalFade()
    {
        // 两个动画都使用 15% 的淡入时长
        float fadeRatio = 0.15f;

        // 短动画：淡入 0.15 秒（1 × 0.15）
        _Animancer.Play(_ShortClip, fadeRatio, FadeMode.NormalizedSpeed);

        // 长动画：淡入 0.75 秒（5 × 0.15）
        _Animancer.Play(_LongClip, fadeRatio, FadeMode.NormalizedSpeed);
    }
}
```

---

### 3. **FadeMode.NormalizedDuration**

**定义**：淡入时长基于**新动画的长度和速度**计算。

**公式**：
```
实际淡入时长 = (新动画长度 × fadeDuration) / 播放速度
```

**代码示例**：
```csharp
// 淡入时长 = 新动画长度的 10% ÷ 播放速度
_Animancer.Play(clip, 0.1f, FadeMode.NormalizedDuration);

// 示例1：新动画长度 = 2 秒，速度 = 1x
// 实际淡入时长 = (2 × 0.1) / 1 = 0.2 秒

// 示例2：新动画长度 = 2 秒，速度 = 2x（加速）
// 实际淡入时长 = (2 × 0.1) / 2 = 0.1 秒

// 示例3：新动画长度 = 2 秒，速度 = 0.5x（减速）
// 实际淡入时长 = (2 × 0.1) / 0.5 = 0.4 秒
```

**适用场景**：
- ✅ 动画播放速度经常变化
- ✅ 希望淡入时长适应速度变化
- ✅ 慢动作或快动作效果

**实际应用**：
```csharp
public class NormalizedDurationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackAnimation;

    void PlayAttackWithSpeed(float speedMultiplier)
    {
        _AttackAnimation.Speed = speedMultiplier;

        // 淡入时长会根据速度自动调整
        _Animancer.Play(_AttackAnimation, 0.1f, FadeMode.NormalizedDuration);

        // 速度 = 2x（快速攻击）
        // 淡入时长会减半

        // 速度 = 0.5x（慢动作攻击）
        // 淡入时长会加倍
    }
}
```

---

### 4. **FadeMode.FromStart**

**定义**：从头开始重新播放动画，通过**克隆状态**实现新旧动画的交叉淡入淡出。

**工作原理**：
```
旧状态：|=============> (从当前时间继续播放并淡出)
新状态：|=============> (从 0 开始播放并淡入)
        ↑
    创建克隆
```

**代码示例**：
```csharp
// 从头开始播放，创建克隆状态
_Animancer.Play(clip, 0.25f, FadeMode.FromStart);
```

**重要特性**：

1. **克隆创建条件**：
   ```csharp
   // 当现有状态的权重超过阈值时才克隆
   if (existingState.Weight > AnimancerLayer.WeightlessThreshold)
   {
       // 创建克隆（默认阈值 = 0.1）
   }
   ```

2. **最大克隆数量**：
   ```csharp
   // 默认最多 3 个克隆
   AnimancerLayer.MaxCloneCount = 3;

   // 超过限制时，复用权重最低的克隆
   ```

3. **非 ClipState 警告**：
   ```csharp
   // 克隆复杂状态（如 Mixer）会生成警告
   // OptionalWarning.CloneComplexState
   ```

**适用场景**：
- ✅ 需要从头重新播放动画
- ✅ 当前动画播放到一半，但需要重新开始
- ✅ 连续触发相同动画（如连续攻击）

**实际应用**：
```csharp
public class FromStartExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _PunchClip;

    void OnPunchInput()
    {
        // 每次按下都从头开始播放攻击动画
        // 即使上一次攻击还没播放完
        _Animancer.Play(_PunchClip, 0.15f, FadeMode.FromStart);
    }
}
```

**克隆管理示例**：
```csharp
public class CloneManagementExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Start()
    {
        // 调整克隆阈值（更敏感）
        _Animancer.Layers[0].WeightlessThreshold = 0.05f;

        // 调整最大克隆数量
        _Animancer.Layers[0].MaxCloneCount = 5;
    }

    void PlayFromStart(AnimationClip clip)
    {
        _Animancer.Play(clip, 0.2f, FadeMode.FromStart);

        // 检查克隆数量
        int cloneCount = 0;
        foreach (var state in _Animancer.States)
        {
            if (state.Clip == clip)
            {
                cloneCount++;
            }
        }
        Debug.Log($"克隆数量: {cloneCount}");
    }
}
```

---

## Transition 默认模式 (Transition Defaults)

Transition 的默认 `FadeMode` 取决于 **"Start Time"** 切换按钮的设置：

### 配置对照表

| Start Time 设置 | 默认 FadeMode | 行为说明 |
|----------------|---------------|---------|
| **启用（Enabled）** | `FadeMode.FromStart` | 总是从指定时间开始播放 |
| **禁用（Disabled）** | `FadeMode.FixedSpeed` | 从当前播放位置继续 |

### Inspector 配置

```
TransitionAsset Inspector:
┌─────────────────────────┐
│ Start Time: ☑ Enabled   │ ← 勾选
│ → Default: FromStart     │
└─────────────────────────┘

┌─────────────────────────┐
│ Start Time: ☐ Disabled  │ ← 未勾选
│ → Default: FixedSpeed    │
└─────────────────────────┘
```

### 代码覆盖默认值

```csharp
// 即使 Transition 默认是 FromStart，也可以覆盖
_Animancer.Play(_Transition, fadeDuration: 0.3f, FadeMode.FixedSpeed);
```

---

## 模式对比表 (Mode Comparison Table)

| FadeMode | 时长计算 | 受速度影响 | 克隆状态 | 适用场景 |
|----------|---------|-----------|---------|---------|
| **FixedSpeed** | 固定值 | ❌ | ❌ | 标准过渡 |
| **NormalizedSpeed** | 动画长度 × 比例 | ❌ | ❌ | 不同长度动画 |
| **NormalizedDuration** | 动画长度 × 比例 / 速度 | ✅ | ❌ | 速度变化场景 |
| **FromStart** | 固定值 | ❌ | ✅ | 从头重播 |

---

## 代码示例集合

### 示例1：对比不同模式

```csharp
using Animancer;
using UnityEngine;

public class FadeModeComparisonExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _TestClip; // 长度 2 秒

    void TestFixedSpeed()
    {
        // 固定 0.5 秒淡入
        _Animancer.Play(_TestClip, 0.5f, FadeMode.FixedSpeed);
        Debug.Log("淡入时长: 0.5 秒");
    }

    void TestNormalizedSpeed()
    {
        // 淡入时长 = 2 × 0.25 = 0.5 秒
        _Animancer.Play(_TestClip, 0.25f, FadeMode.NormalizedSpeed);
        Debug.Log("淡入时长: " + (2 * 0.25f) + " 秒");
    }

    void TestNormalizedDuration()
    {
        // 假设速度 = 1x
        // 淡入时长 = (2 × 0.25) / 1 = 0.5 秒
        _Animancer.Play(_TestClip, 0.25f, FadeMode.NormalizedDuration);
        Debug.Log("淡入时长: " + ((2 * 0.25f) / 1) + " 秒");
    }

    void TestFromStart()
    {
        // 从头开始，淡入 0.5 秒
        _Animancer.Play(_TestClip, 0.5f, FadeMode.FromStart);
        Debug.Log("从头开始播放，淡入时长: 0.5 秒");
    }
}
```

---

### 示例2：动态选择模式

```csharp
using Animancer;
using UnityEngine;

public class DynamicModeSelectionExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    void PlayWithAdaptiveMode(bool shouldRestart, float speed)
    {
        float fadeDuration = 0.25f;
        FadeMode mode;

        if (shouldRestart)
        {
            // 需要重新开始
            mode = FadeMode.FromStart;
        }
        else if (speed != 1.0f)
        {
            // 速度变化，使用 NormalizedDuration
            mode = FadeMode.NormalizedDuration;
        }
        else
        {
            // 标准情况
            mode = FadeMode.FixedSpeed;
        }

        _Animancer.Play(_Clip, fadeDuration, mode);
        Debug.Log($"使用模式: {mode}");
    }
}
```

---

### 示例3：FromStart 连续攻击

```csharp
using Animancer;
using UnityEngine;

public class ContinuousAttackExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    private int _attackCount = 0;

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            PerformAttack();
        }
    }

    void PerformAttack()
    {
        _attackCount++;

        // 每次攻击都从头开始，即使上次还没播完
        _Animancer.Play(_AttackClip, 0.1f, FadeMode.FromStart);

        Debug.Log($"攻击 #{_attackCount} - 从头开始播放");
    }
}
```

---

### 示例4：基于动画长度的自适应淡入

```csharp
using Animancer;
using UnityEngine;

public class AdaptiveFadeExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip[] _Clips;

    [SerializeField, Range(0f, 1f)]
    private float _fadeRatio = 0.2f; // 20%

    void PlayRandomClipWithAdaptiveFade()
    {
        AnimationClip randomClip = _Clips[Random.Range(0, _Clips.Length)];

        // 使用 NormalizedSpeed 确保所有动画都使用相同比例的淡入
        _Animancer.Play(randomClip, _fadeRatio, FadeMode.NormalizedSpeed);

        float actualFadeDuration = randomClip.length * _fadeRatio;
        Debug.Log($"动画: {randomClip.name}, 长度: {randomClip.length:F2}s, 淡入: {actualFadeDuration:F2}s");
    }
}
```

---

### 示例5：速度变化场景

```csharp
using Animancer;
using UnityEngine;

public class SpeedBasedFadeExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Animation;

    void PlayWithSpeed(float speedMultiplier)
    {
        _Animation.Speed = speedMultiplier;

        // 使用 NormalizedDuration 适应速度变化
        _Animancer.Play(_Animation, 0.15f, FadeMode.NormalizedDuration);

        float clipLength = _Animation.Clip.length;
        float actualFade = (clipLength * 0.15f) / speedMultiplier;

        Debug.Log($"速度: {speedMultiplier}x, 淡入时长: {actualFade:F2}s");
    }

    // 测试方法
    [ContextMenu("Normal Speed")]
    void NormalSpeed() => PlayWithSpeed(1.0f); // 标准淡入

    [ContextMenu("Fast Speed")]
    void FastSpeed() => PlayWithSpeed(2.0f);   // 淡入减半

    [ContextMenu("Slow Speed")]
    void SlowSpeed() => PlayWithSpeed(0.5f);   // 淡入加倍
}
```

---

## 最佳实践建议

### 1. **选择合适的模式**

```csharp
// ✅ 推荐：根据场景选择模式
FadeMode GetAppropriateFadeMode(AnimationType type, float speed)
{
    switch (type)
    {
        case AnimationType.QuickAction:
            return FadeMode.FixedSpeed; // 固定快速过渡

        case AnimationType.Movement:
            if (speed != 1.0f)
                return FadeMode.NormalizedDuration; // 速度变化
            else
                return FadeMode.NormalizedSpeed; // 标准移动

        case AnimationType.Restart:
            return FadeMode.FromStart; // 需要重新开始

        default:
            return FadeMode.FixedSpeed;
    }
}
```

---

### 2. **避免常见错误**

```csharp
// ❌ 错误：FixedSpeed 时长超过动画长度
AnimationClip shortClip; // 长度 0.3 秒
_Animancer.Play(shortClip, 1.0f, FadeMode.FixedSpeed);
// 淡入时长 1 秒 > 动画长度 0.3 秒

// ✅ 正确：使用 NormalizedSpeed
_Animancer.Play(shortClip, 0.3f, FadeMode.NormalizedSpeed);
// 淡入时长 = 0.3 × 0.3 = 0.09 秒 ✅
```

---

### 3. **管理 FromStart 克隆**

```csharp
// ✅ 监控克隆数量
void MonitorClones(AnimationClip targetClip)
{
    int cloneCount = 0;
    foreach (var state in _Animancer.States)
    {
        if (state.Clip == targetClip)
        {
            cloneCount++;
        }
    }

    if (cloneCount > AnimancerLayer.MaxCloneCount)
    {
        Debug.LogWarning($"克隆数量过多: {cloneCount}");
    }
}

// ✅ 调整克隆限制
_Animancer.Layers[0].MaxCloneCount = 5; // 增加限制
```

---

### 4. **Normalized 模式的时长范围**

```csharp
// ✅ 推荐：Normalized 模式使用 0-1 范围
_Animancer.Play(clip, 0.25f, FadeMode.NormalizedSpeed); // 25%

// ❌ 不推荐：超过 1 会导致淡入时长过长
_Animancer.Play(clip, 2.0f, FadeMode.NormalizedSpeed); // 200%（过长）
```

---

## 常见问题 FAQ

### Q1: 什么时候应该使用 NormalizedSpeed 而不是 FixedSpeed？

**A**: 当动画长度差异较大时使用 `NormalizedSpeed`：

```csharp
// 场景：有短动画（0.5秒）和长动画（5秒）

// ❌ FixedSpeed：短动画淡入过长
_Animancer.Play(shortClip, 0.5f, FadeMode.FixedSpeed); // 淡入 = 动画长度

// ✅ NormalizedSpeed：比例一致
_Animancer.Play(shortClip, 0.2f, FadeMode.NormalizedSpeed); // 淡入 0.1s
_Animancer.Play(longClip, 0.2f, FadeMode.NormalizedSpeed);  // 淡入 1.0s
```

---

### Q2: FromStart 模式为什么需要克隆状态？

**A**: 因为需要同时播放两个相同动画的不同时间点：

```
旧状态：|====时间2.5s====> 继续播放并淡出
新状态：|====时间0.0s====> 从头开始并淡入
        ↑
    必须使用两个独立的状态实例
```

---

### Q3: 克隆复杂状态会有什么问题？

**A**: 克隆 `Mixer` 或 `Controller` 等复杂状态会：
- 增加内存使用
- 可能导致状态不同步
- 触发 `OptionalWarning.CloneComplexState` 警告

**建议**：
```csharp
// ❌ 避免对 Mixer 使用 FromStart
_Animancer.Play(_MixerTransition, 0.25f, FadeMode.FromStart);

// ✅ 对 ClipTransition 使用 FromStart
_Animancer.Play(_ClipTransition, 0.25f, FadeMode.FromStart);
```

---

### Q4: NormalizedDuration 和 NormalizedSpeed 有什么区别？

**A**:

| 特性 | NormalizedSpeed | NormalizedDuration |
|------|----------------|-------------------|
| **公式** | 长度 × 比例 | (长度 × 比例) / 速度 |
| **受速度影响** | ❌ | ✅ |
| **适用场景** | 标准动画 | 速度变化动画 |

**示例**：
```csharp
// 动画长度 2 秒，速度 2x，比例 0.2

// NormalizedSpeed: 2 × 0.2 = 0.4 秒
// NormalizedDuration: (2 × 0.2) / 2 = 0.2 秒
```

---

### Q5: 如何避免淡入时长超过动画长度？

**A**:

```csharp
// 方法1：使用 NormalizedSpeed
_Animancer.Play(clip, 0.3f, FadeMode.NormalizedSpeed); // 最多 30% 长度

// 方法2：动态计算
float safeFadeDuration = Mathf.Min(clip.length * 0.5f, 0.25f);
_Animancer.Play(clip, safeFadeDuration, FadeMode.FixedSpeed);

// 方法3：检查并警告
void SafePlay(AnimationClip clip, float fadeDuration)
{
    if (fadeDuration > clip.length)
    {
        Debug.LogWarning($"淡入时长 {fadeDuration} 超过动画长度 {clip.length}");
        fadeDuration = clip.length * 0.5f;
    }
    _Animancer.Play(clip, fadeDuration);
}
```

---

### Q6: 如何在 Inspector 中设置默认 FadeMode？

**A**: 通过 Transition 的 "Start Time" 设置：

```
Inspector:
┌─────────────────────────┐
│ ClipTransition          │
│ ├─ Clip: [...]          │
│ ├─ Fade Duration: 0.25  │
│ └─ Start Time: ☑        │ ← 勾选 = FromStart
└─────────────────────────┘
```

代码中可以覆盖：
```csharp
// 即使默认是 FromStart，也可以覆盖
_Animancer.Play(_Transition, 0.3f, FadeMode.FixedSpeed);
```

---

## 总结

### 核心要点

1. **四种主要模式**
   - **FixedSpeed**：固定时长，标准模式
   - **NormalizedSpeed**：基于动画长度
   - **NormalizedDuration**：考虑播放速度
   - **FromStart**：克隆状态，从头开始

2. **选择策略**
   - 标准场景：`FixedSpeed`
   - 不同长度动画：`NormalizedSpeed`
   - 速度变化：`NormalizedDuration`
   - 重新开始：`FromStart`

3. **Normalized 模式优势**
   - 自动适应动画长度
   - 避免淡入超出动画
   - 保持一致的视觉比例

4. **FromStart 注意事项**
   - 会创建状态克隆
   - 有最大克隆数量限制
   - 避免克隆复杂状态

### 下一步学习

- 📖 深入学习 **Custom Easing** 实现非线性淡入
- 🎨 探索 **Sequences** 组合多个动画
- 📚 了解克隆状态的内存管理
- 🔍 查看实际项目中的模式选择策略

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/fading/modes/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
