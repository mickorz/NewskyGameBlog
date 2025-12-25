---
title: "Animancer Mixers"
date: 2025-12-25
draft: false
---

# Animancer Mixers 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Mixers（混合器）** 是 Animancer 中基于参数混合多个动画的系统,功能类似于 Mecanim 的 Blend Trees。它们能够实现平滑的动画过渡——例如,根据移动速度在 Idle、Walk 和 Run 状态之间混合,而不是使用离散的动画状态。

---

## 核心概念 (Core Concept)

> **Mixers 基于参数混合多个动画,实现连续的动画过渡谱,而不是离散的状态切换。**

**示例**：
```
传统状态机:
Idle → Walk → Run
(离散切换)

Mixer:
Idle ←━━━━━━━━━━━━━━━━━━━━━━━━━━→ Run
      Walk
(连续混合,参数 = 速度)
```

---

## Blend Trees vs. Mixers

### Blend Trees（Unity 内置）

**特点**：
- 在 Unity Editor 中手动创建
- 固定配置
- 运行时访问受限
- 强制统一的脚步同步

**限制**：
- ❌ 配置不灵活
- ❌ 运行时无法修改
- ❌ 所有状态强制同步

---

### Mixers（Animancer）

**特点**：
- 运行时动态生成
- 完全可修改
- 直接访问内部状态
- 可自定义同步选项

**优势**：
- ✅ 灵活配置
- ✅ 运行时可修改
- ✅ 可选择性同步
- ✅ 完全代码控制

---

## Mixer 类型对照表

| 类型 | 参数 | 算法 | Blend Tree 等价 | 用途 |
|------|------|------|----------------|------|
| **ManualMixerState** | 无 | 手动权重 | Direct Blending | 手动控制混合权重 |
| **LinearMixerState** | Float | 线性 O(n) | 1D Blending | 单参数混合（速度）|
| **CartesianMixerState** | Vector2 | 梯度带 O(n²) | 2D Freeform Cartesian | 笛卡尔坐标混合 |
| **DirectionalMixerState** | Vector2 | 极坐标梯度带 O(n²) | 2D Freeform Directional | 方向混合 |

---

## 参数系统 (Parameter System)

### 工作原理

**参数自动根据阈值（Thresholds）计算状态权重。**

```csharp
// 示例：Linear Mixer
// Threshold: [0, 0.5, 1.0]
// Animations: [Idle, Walk, Run]

parameter = 0.0  → Idle: 100%, Walk: 0%, Run: 0%
parameter = 0.25 → Idle: 50%, Walk: 50%, Run: 0%
parameter = 0.5  → Idle: 0%, Walk: 100%, Run: 0%
parameter = 0.75 → Idle: 0%, Walk: 50%, Run: 50%
parameter = 1.0  → Idle: 0%, Walk: 0%, Run: 100%
```

---

### 参数绑定

**参数可以绑定到 Animancer Parameters** 以便在不直接访问状态的情况下动态控制。

```csharp
using Animancer;
using UnityEngine;

public class ParameterBindingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;
    [SerializeField] private StringAsset _SpeedParameter;

    private LinearMixerState _MixerState;

    void Start()
    {
        // 播放 Mixer
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;

        // 绑定参数
        _MixerState.Parameter = 0; // 初始值
    }

    void Update()
    {
        // 通过参数控制
        float speed = GetCurrentSpeed();
        _Animancer.Parameters.SetValue(_SpeedParameter, speed);

        // Mixer 自动根据参数值调整权重
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

## Manual Mixers（手动混合器）

### 定义

**ManualMixerState** 提供直接的权重控制,绕过自动计算。

**用途**：
- ✅ 叠加动画
- ✅ 面部表情混合
- ✅ 复杂的权重控制逻辑

---

### 代码示例

```csharp
using Animancer;
using UnityEngine;

public class ManualMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ManualMixerTransition _FacialMixer;

    private ManualMixerState _MixerState;

    void Start()
    {
        // Mixer 子动画：
        // [0] Neutral（中性）
        // [1] Happy（快乐）
        // [2] Sad（悲伤）
        // [3] Angry（愤怒）

        _MixerState = _Animancer.Play(_FacialMixer) as ManualMixerState;
    }

    void SetEmotion(float happiness, float sadness, float anger)
    {
        // 中性表情作为基础
        float neutralWeight = 1.0f - (happiness + sadness + anger);

        // 手动设置每个表情的权重
        _MixerState.SetChildWeight(0, neutralWeight);
        _MixerState.SetChildWeight(1, happiness);
        _MixerState.SetChildWeight(2, sadness);
        _MixerState.SetChildWeight(3, anger);
    }

    [ContextMenu("Test: Happy")]
    void TestHappy() => SetEmotion(happiness: 1f, sadness: 0f, anger: 0f);

    [ContextMenu("Test: Mixed")]
    void TestMixed() => SetEmotion(happiness: 0.5f, sadness: 0.3f, anger: 0.2f);
}
```

---

## 2D Mixers（二维混合器）

### Cartesian vs. Directional

**CartesianMixerState（笛卡尔混合器）**：
- 使用直角坐标系（X, Y）
- 适合：位置相关的混合

**DirectionalMixerState（方向混合器）**：
- 使用极坐标系（角度,距离）
- 适合：方向相关的混合（前/后/左/右）
- **通常表现更好**

---

### 方向混合器建议

```csharp
// ✅ 推荐：使用 DirectionalMixer 处理移动方向
DirectionalMixerTransition movementMixer = new DirectionalMixerTransition
{
    // 8 方向动画
    new ClipTransition { Clip = forward, Position = new Vector2(0, 1) },
    new ClipTransition { Clip = forwardRight, Position = new Vector2(0.707f, 0.707f) },
    new ClipTransition { Clip = right, Position = new Vector2(1, 0) },
    // ... 其他方向
};
```

---

### 死区问题（Dead Zones）

> **重要**：当状态之间相隔 180+ 度时,会出现死区,产生不可预测的结果。

```
问题示例：
Forward (0°)
  │
  │  ← 超过 180° 的间隙
  │
Backward (180°)

解决方案：添加更多方向
Forward (0°)
Left (270°) ─┼─ Right (90°)
Backward (180°)
```

---

### 中心空闲动画

> **建议**：包含中心的空闲动画可以优化低参数值时的插值。

```csharp
// ✅ 推荐配置
DirectionalMixerTransition mixer = new DirectionalMixerTransition
{
    // 中心：Idle（参数接近 0 时）
    new ClipTransition { Clip = idle, Position = Vector2.zero },

    // 外围：8 方向移动
    new ClipTransition { Clip = forward, Position = new Vector2(0, 1) },
    new ClipTransition { Clip = forwardRight, Position = new Vector2(0.707f, 0.707f) },
    // ...
};
```

---

## Mixer 特定细节 (Mixer-Specific Details)

### Clip 属性

```csharp
var mixer = _Animancer.Play(_MixerTransition) as LinearMixerState;

Debug.Log(mixer.Clip); // 输出: null
// Mixer 不是单个 Clip,所以返回 null
```

---

### Length, Time, NormalizedTime

这些属性反映**加权平均值**。

```csharp
// 示例：
// Child 0: Length = 1.0s, Weight = 0.7
// Child 1: Length = 2.0s, Weight = 0.3

// Mixer.Length = (1.0 × 0.7) + (2.0 × 0.3) = 1.3s
```

---

### Keys（关键帧）

**子状态不会自动获得 Keys**,除非手动分配。

```csharp
// 手动分配 Keys
foreach (var child in mixer.Children)
{
    child.Key = child.Clip; // 使用 Clip 作为 Key
}
```

---

### 事件（Events）

事件基于**加权平均的 NormalizedTime** 触发。

```csharp
// Mixer 的 NormalizedTime 是所有子状态的加权平均
// 事件在该平均值达到触发点时触发
```

---

## 代码示例集合

### 示例1：Linear Mixer（1D 混合）

```csharp
using Animancer;
using UnityEngine;

public class LinearMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;

    private LinearMixerState _MixerState;

    void Start()
    {
        // 创建 Linear Mixer
        LinearMixerTransition mixer = new LinearMixerTransition
        {
            FadeDuration = 0.25f,

            // 子动画和阈值
            new ClipTransition { Clip = _IdleClip, Threshold = 0.0f },
            new ClipTransition { Clip = _WalkClip, Threshold = 0.5f },
            new ClipTransition { Clip = _RunClip, Threshold = 1.0f }
        };

        _MixerState = _Animancer.Play(mixer) as LinearMixerState;
    }

    void Update()
    {
        // 根据输入调整参数
        float speed = Input.GetAxis("Vertical"); // -1 到 1
        _MixerState.Parameter = Mathf.Abs(speed); // 0 到 1

        // 参数 = 0: Idle
        // 参数 = 0.5: Walk
        // 参数 = 1: Run
        // 中间值会自动混合
    }
}
```

---

### 示例2：2D Directional Mixer（方向混合）

```csharp
using Animancer;
using UnityEngine;

public class DirectionalMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _ForwardClip;
    [SerializeField] private AnimationClip _BackwardClip;
    [SerializeField] private AnimationClip _LeftClip;
    [SerializeField] private AnimationClip _RightClip;

    private DirectionalMixerState _MixerState;

    void Start()
    {
        DirectionalMixerTransition mixer = new DirectionalMixerTransition
        {
            FadeDuration = 0.25f,

            // 中心：Idle
            new ClipTransition { Clip = _IdleClip, Position = Vector2.zero },

            // 四方向
            new ClipTransition { Clip = _ForwardClip, Position = new Vector2(0, 1) },
            new ClipTransition { Clip = _BackwardClip, Position = new Vector2(0, -1) },
            new ClipTransition { Clip = _LeftClip, Position = new Vector2(-1, 0) },
            new ClipTransition { Clip = _RightClip, Position = new Vector2(1, 0) }
        };

        _MixerState = _Animancer.Play(mixer) as DirectionalMixerState;
    }

    void Update()
    {
        // 获取输入
        float horizontal = Input.GetAxis("Horizontal"); // -1 到 1
        float vertical = Input.GetAxis("Vertical");     // -1 到 1

        // 设置参数（Vector2）
        _MixerState.Parameter = new Vector2(horizontal, vertical);

        // 例如：
        // (0, 1): Forward
        // (1, 0): Right
        // (0.707, 0.707): Forward-Right（自动混合）
    }
}
```

---

### 示例3：Manual Mixer（手动权重）

```csharp
using Animancer;
using UnityEngine;

public class HealthBasedMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _HealthyWalkClip;
    [SerializeField] private AnimationClip _TiredWalkClip;
    [SerializeField] private AnimationClip _InjuredWalkClip;

    private ManualMixerState _MixerState;

    [SerializeField, Range(0f, 100f)]
    private float _health = 100f;

    void Start()
    {
        ManualMixerTransition mixer = new ManualMixerTransition
        {
            new ClipTransition { Clip = _HealthyWalkClip },
            new ClipTransition { Clip = _TiredWalkClip },
            new ClipTransition { Clip = _InjuredWalkClip }
        };

        _MixerState = _Animancer.Play(mixer) as ManualMixerState;
    }

    void Update()
    {
        UpdateWeightsBasedOnHealth();
    }

    void UpdateWeightsBasedOnHealth()
    {
        if (_health > 70f)
        {
            // 健康：只使用健康行走
            _MixerState.SetChildWeight(0, 1.0f);
            _MixerState.SetChildWeight(1, 0.0f);
            _MixerState.SetChildWeight(2, 0.0f);
        }
        else if (_health > 30f)
        {
            // 疲劳：混合健康和疲劳
            float healthRatio = (_health - 30f) / 40f; // 0-1
            _MixerState.SetChildWeight(0, healthRatio);
            _MixerState.SetChildWeight(1, 1.0f - healthRatio);
            _MixerState.SetChildWeight(2, 0.0f);
        }
        else
        {
            // 受伤：混合疲劳和受伤
            float tiredRatio = _health / 30f; // 0-1
            _MixerState.SetChildWeight(0, 0.0f);
            _MixerState.SetChildWeight(1, tiredRatio);
            _MixerState.SetChildWeight(2, 1.0f - tiredRatio);
        }
    }
}
```

---

### 示例4：嵌套 Mixer

```csharp
using Animancer;
using UnityEngine;

public class NestedMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // Linear Mixer 1: Idle → Walk
    [SerializeField] private LinearMixerTransition _IdleWalkMixer;

    // Linear Mixer 2: Walk → Run
    [SerializeField] private LinearMixerTransition _WalkRunMixer;

    // Parent Mixer: 根据速度选择子 Mixer
    private ManualMixerState _ParentMixer;

    void Start()
    {
        ManualMixerTransition parentMixer = new ManualMixerTransition
        {
            _IdleWalkMixer,  // Child 0
            _WalkRunMixer    // Child 1
        };

        _ParentMixer = _Animancer.Play(parentMixer) as ManualMixerState;
    }

    void Update()
    {
        float speed = GetCurrentSpeed(); // 0-1

        // 根据速度调整父 Mixer 权重
        if (speed < 0.5f)
        {
            // 低速：使用 IdleWalk Mixer
            _ParentMixer.SetChildWeight(0, 1.0f);
            _ParentMixer.SetChildWeight(1, 0.0f);

            // 控制 IdleWalk Mixer 的参数
            var idleWalkMixer = _ParentMixer.GetChild(0) as LinearMixerState;
            idleWalkMixer.Parameter = speed * 2; // 0-1
        }
        else
        {
            // 高速：使用 WalkRun Mixer
            _ParentMixer.SetChildWeight(0, 0.0f);
            _ParentMixer.SetChildWeight(1, 1.0f);

            // 控制 WalkRun Mixer 的参数
            var walkRunMixer = _ParentMixer.GetChild(1) as LinearMixerState;
            walkRunMixer.Parameter = (speed - 0.5f) * 2; // 0-1
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

### 1. **选择合适的 Mixer 类型**

```csharp
// ✅ 单参数（速度）：Linear Mixer
LinearMixerTransition speedMixer;

// ✅ 方向移动：Directional Mixer
DirectionalMixerTransition movementMixer;

// ✅ 复杂权重控制：Manual Mixer
ManualMixerTransition facialMixer;
```

---

### 2. **方向混合避免死区**

```csharp
// ❌ 不推荐：只有前后（180° 间隙）
DirectionalMixerTransition badMixer = new DirectionalMixerTransition
{
    new ClipTransition { Clip = forward, Position = new Vector2(0, 1) },
    new ClipTransition { Clip = backward, Position = new Vector2(0, -1) }
};

// ✅ 推荐：8 方向覆盖
DirectionalMixerTransition goodMixer = new DirectionalMixerTransition
{
    // Forward, ForwardRight, Right, BackRight,
    // Back, BackLeft, Left, ForwardLeft
};
```

---

### 3. **包含中心 Idle 动画**

```csharp
// ✅ 推荐
DirectionalMixerTransition mixer = new DirectionalMixerTransition
{
    new ClipTransition { Clip = idle, Position = Vector2.zero }, // 中心
    // ... 其他方向
};
```

---

### 4. **合理设置阈值**

```csharp
// ✅ 推荐：基于实际需求设置阈值
LinearMixerTransition mixer = new LinearMixerTransition
{
    new ClipTransition { Clip = idle, Threshold = 0.0f },
    new ClipTransition { Clip = walk, Threshold = 2.5f },  // 实际速度值
    new ClipTransition { Clip = run, Threshold = 5.0f }
};

// 参数 = 实际速度（m/s）
_MixerState.Parameter = GetActualSpeed();
```

---

## 常见问题 FAQ

### Q1: Mixer 和 Blend Tree 应该如何选择？

**A**:

| 场景 | 推荐方案 |
|------|---------|
| 需要运行时修改 | Mixer |
| 需要代码完全控制 | Mixer |
| 需要可选同步 | Mixer |
| 简单场景,不需要代码 | Blend Tree |
| 已有 Animator Controller | Blend Tree |

---

### Q2: 如何调试 Mixer 权重？

**A**:

```csharp
void OnGUI()
{
    if (_MixerState != null)
    {
        GUILayout.Label($"Mixer Parameter: {_MixerState.Parameter}");

        for (int i = 0; i < _MixerState.ChildCount; i++)
        {
            var child = _MixerState.GetChild(i);
            GUILayout.Label($"Child {i}: Weight = {child.Weight:F2}");
        }
    }
}
```

---

### Q3: Mixer 可以包含其他类型的 Transition 吗？

**A**: 可以！

```csharp
LinearMixerTransition mixer = new LinearMixerTransition
{
    new ClipTransition { Clip = idle },
    new ClipTransitionSequence { /* 序列 */ },
    new LinearMixerTransition { /* 嵌套 Mixer */ }
};
```

---

### Q4: 为什么我的 Mixer Events 没有触发？

**A**: Mixer 的事件基于加权平均的 NormalizedTime。

```csharp
// 解决方案：为每个子动画单独添加事件
for (int i = 0; i < _MixerState.ChildCount; i++)
{
    var child = _MixerState.GetChild(i);
    child.Events(this).OnEnd = () => Debug.Log($"Child {i} ended");
}
```

---

### Q5: Manual Mixer 的权重总和必须是 1 吗？

**A**: 不强制要求,但建议归一化。

```csharp
// ✅ 推荐：归一化权重
void SetNormalizedWeights(params float[] weights)
{
    float total = 0;
    foreach (float w in weights) total += w;

    for (int i = 0; i < weights.Length; i++)
    {
        _MixerState.SetChildWeight(i, weights[i] / total);
    }
}
```

---

## 总结

### 核心要点

1. **四种 Mixer 类型**
   - **Linear**：单参数混合
   - **Cartesian**：2D 笛卡尔混合
   - **Directional**：2D 方向混合
   - **Manual**：手动权重控制

2. **参数系统**
   - 自动计算权重
   - 支持参数绑定
   - 实时动态调整

3. **vs. Blend Trees**
   - Mixers：动态、灵活、代码控制
   - Blend Trees：静态、Editor 配置

4. **最佳实践**
   - 方向混合避免死区
   - 包含中心 Idle 动画
   - 选择性同步子状态

### 下一步学习

- 📖 深入学习 **Mixer Creation**（创建方法）
- 🎨 探索 **Mixer Synchronization**（同步机制）
- 📚 了解参数绑定的高级用法
- 🔍 查看实际项目中的 Mixer 应用

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
