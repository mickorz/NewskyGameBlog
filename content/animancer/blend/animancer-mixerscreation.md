# Animancer Mixers Creation 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/creation/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

Animancer 提供两种主要方法来创建 Mixers：通过 **Inspector 配置的 Transition** 或 **手动代码创建**。两种方法都支持嵌套 Mixers。

---

## 创建方法对比

| 方法 | 优势 | 适用场景 |
|------|------|---------|
| **Transition-Based** | 可视化配置,非程序员友好 | 固定配置,Inspector 管理 |
| **Manual Code** | 完全代码控制,动态生成 | 运行时动态创建,复杂逻辑 |

---

## 方法一：基于 Transition 创建

### 概述

> **Mixers 通常在 Inspector 中使用 Mixer Transitions 配置。**

**工作流程**：
1. 创建 Mixer Transition（Inline 或 Asset）
2. 在 Inspector 中配置子动画和参数
3. 在代码中播放并访问 Mixer 状态

---

### 配置步骤

#### 步骤1：创建 Transition

**Inline Transition（内联）**：
```csharp
using Animancer;
using UnityEngine;

public class InlineTransitionExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 在 Inspector 中直接配置
    [SerializeField] private LinearMixerTransition _MovementMixer;

    void Start()
    {
        // 播放 Mixer
        var mixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;
    }
}
```

**Transition Asset（资源文件）**：
```
1. 右键 → Create → Animancer → Linear Mixer Transition
2. 配置子动画和阈值
3. 在脚本中引用
```

---

#### 步骤2：Inspector 配置

**Linear Mixer Transition Inspector**：
```
LinearMixerTransition:
┌─────────────────────────────┐
│ Fade Duration: 0.25         │
│ Speed: 1.0                  │
│ Parameter: SpeedValue.asset │
│                             │
│ Children (3):               │
│ ├─ [0] Idle                 │
│ │   Threshold: 0.0          │
│ ├─ [1] Walk                 │
│ │   Threshold: 0.5          │
│ └─ [2] Run                  │
│     Threshold: 1.0          │
│                             │
│ ☑ Synchronize Children      │
└─────────────────────────────┘
```

---

#### 步骤3：代码访问

```csharp
using Animancer;
using UnityEngine;

public class TransitionBasedMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private LinearMixerTransition _MovementMixer;
    [SerializeField] private StringAsset _SpeedParameter;

    private LinearMixerState _MixerState;

    void Start()
    {
        // 播放 Mixer Transition
        _MixerState = _Animancer.Play(_MovementMixer) as LinearMixerState;

        // 访问 Mixer 状态参数
        Debug.Log($"Initial Parameter: {_MixerState.Parameter}");
    }

    void Update()
    {
        // 控制参数
        float speed = GetCurrentSpeed();
        _MixerState.Parameter = speed;

        // 或通过参数系统
        _Animancer.Parameters.SetValue(_SpeedParameter, speed);
    }

    float GetCurrentSpeed()
    {
        return Mathf.Abs(Input.GetAxis("Vertical"));
    }
}
```

---

### Transition 配置选项

**主要配置项**：
- **Fade Duration**：淡入持续时间
- **Speed**：播放速度
- **Parameter**：参数绑定（StringAsset）
- **Children**：子动画列表
- **Thresholds**：每个子动画的阈值
- **Synchronize Children**：是否同步子动画

---

## 方法二：手动代码创建

### 四步流程

1. **引用子动画**：获取 `AnimationClip` 引用或 Transition 对象
2. **实例化 Mixer**：创建 Mixer 实例（如 `LinearMixerState`）
3. **添加子状态**：通过集合初始化器或 `Add()` 方法
4. **存储引用**：保持 Mixer 引用以便参数控制

---

### 示例1：集合初始化器方式

```csharp
using Animancer;
using UnityEngine;

public class ManualMixerCreationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 步骤1：引用子动画
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;

    private LinearMixerState _MixerState;

    void Start()
    {
        CreateMixerWithCollectionInitializer();
    }

    void CreateMixerWithCollectionInitializer()
    {
        // 步骤2 & 3：实例化 Mixer 并添加子状态
        _MixerState = new LinearMixerState(_Animancer.Graph)
        {
            // 使用集合初始化器添加子状态
            { _IdleClip, 0.0f },   // Clip, Threshold
            { _WalkClip, 0.5f },
            { _RunClip, 1.0f }
        };

        // 可选：设置调试名称
        _MixerState.SetDebugName("Movement Mixer");

        // 播放 Mixer
        _MixerState.Play(_Animancer);

        // 步骤4：存储引用（已在类成员中存储）
    }

    void Update()
    {
        // 控制参数
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

### 示例2：Add() 方法方式

```csharp
using Animancer;
using UnityEngine;

public class ManualMixerWithAddExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;

    private LinearMixerState _MixerState;

    void Start()
    {
        CreateMixerWithAddMethod();
    }

    void CreateMixerWithAddMethod()
    {
        // 步骤2：实例化 Mixer
        _MixerState = new LinearMixerState(_Animancer.Graph);

        // 步骤3：使用 Add() 方法添加子状态
        _MixerState.Add(_IdleClip, threshold: 0.0f);
        _MixerState.Add(_WalkClip, threshold: 0.5f);
        _MixerState.Add(_RunClip, threshold: 1.0f);

        // 设置调试名称
        _MixerState.SetDebugName("Movement Mixer");

        // 播放 Mixer
        _MixerState.Play(_Animancer);
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

### 方法对比

| 特性 | 集合初始化器 | Add() 方法 |
|------|------------|-----------|
| **代码简洁性** | ✅ 更简洁 | ⚠️ 较冗长 |
| **可读性** | ✅ 清晰 | ✅ 清晰 |
| **条件添加** | ❌ 不灵活 | ✅ 灵活 |
| **推荐度** | ✅ 通用推荐 | ✅ 条件逻辑 |

---

## 配置元素详解

### 1. Thresholds（阈值）

**定义**：决定每个子动画对应的参数值。

**手动指定**：
```csharp
_MixerState.Add(_IdleClip, threshold: 0.0f);
_MixerState.Add(_WalkClip, threshold: 2.5f);  // 实际速度值
_MixerState.Add(_RunClip, threshold: 5.0f);
```

---

**自动计算（Vector2）**：

使用自定义委托计算阈值。

```csharp
using Animancer;
using Animancer.Units;
using UnityEngine;

public class AutoThresholdExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _ForwardClip;
    [SerializeField] private AnimationClip _RightClip;
    [SerializeField] private AnimationClip _BackClip;
    [SerializeField] private AnimationClip _LeftClip;

    private DirectionalMixerState _MixerState;

    void Start()
    {
        _MixerState = new DirectionalMixerState(_Animancer.Graph);

        // 使用工具方法自动计算阈值
        _MixerState.Add(_ForwardClip);
        _MixerState.Add(_RightClip);
        _MixerState.Add(_BackClip);
        _MixerState.Add(_LeftClip);

        // 自动计算基于平均速度的阈值
        AnimancerUtilities.CalculateThresholdsFromAverageVelocityXZ(_MixerState);

        _MixerState.Play(_Animancer);
    }
}
```

**说明**：`AnimancerUtilities.CalculateThresholdsFromAverageVelocityXZ` 会分析动画的 Root Motion 速度并自动设置阈值。

---

### 2. Debug Naming（调试命名）

**目的**：在 Inspector 中更容易识别。

```csharp
_MixerState.SetDebugName("Movement Mixer");

// 在 Inspector 中显示为：
// "Movement Mixer" 而不是 "LinearMixerState"
```

---

### 3. Synchronization Control（同步控制）

**禁用同步**：

```csharp
// 禁用整个 Mixer 的同步
_MixerState.DontSynchronizeChildren();

// 禁用特定子状态的同步
_MixerState.DontSynchronize(_MixerState.GetChild(0));
```

**详细说明请参考**：**Mixer Synchronization** 专题文档

---

## 嵌套 Mixers

### 方法1：Transition 嵌套

**定义**：父 Mixer 通过 Transition 定义,子 Mixer 作为 Transition Assets 引用。

```csharp
using Animancer;
using UnityEngine;

public class NestedTransitionMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 子 Mixer Transitions（作为资源文件）
    [SerializeField] private LinearMixerTransition _IdleWalkMixer;
    [SerializeField] private LinearMixerTransition _WalkRunMixer;

    private ManualMixerState _ParentMixer;

    void Start()
    {
        // 创建父 Mixer,包含子 Mixer Transitions
        ManualMixerTransition parentMixer = new ManualMixerTransition
        {
            _IdleWalkMixer,  // Child 0（Transition）
            _WalkRunMixer    // Child 1（Transition）
        };

        _ParentMixer = _Animancer.Play(parentMixer) as ManualMixerState;
    }

    void Update()
    {
        float speed = GetCurrentSpeed();

        // 根据速度选择使用哪个子 Mixer
        if (speed < 0.5f)
        {
            _ParentMixer.SetChildWeight(0, 1.0f);
            _ParentMixer.SetChildWeight(1, 0.0f);

            // 控制 IdleWalk Mixer
            var childMixer = _ParentMixer.GetChild(0) as LinearMixerState;
            childMixer.Parameter = speed * 2; // 0-1
        }
        else
        {
            _ParentMixer.SetChildWeight(0, 0.0f);
            _ParentMixer.SetChildWeight(1, 1.0f);

            // 控制 WalkRun Mixer
            var childMixer = _ParentMixer.GetChild(1) as LinearMixerState;
            childMixer.Parameter = (speed - 0.5f) * 2; // 0-1
        }
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

### 方法2：手动嵌套

**定义**：通过集合初始化器或 `Add()` 方法添加子 Mixer。

```csharp
using Animancer;
using UnityEngine;

public class ManualNestedMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;
    [SerializeField] private AnimationClip _SprintClip;

    private ManualMixerState _ParentMixer;

    void Start()
    {
        // 创建子 Mixer 1: Idle → Walk
        var idleWalkMixer = new LinearMixerState(_Animancer.Graph)
        {
            { _IdleClip, 0.0f },
            { _WalkClip, 1.0f }
        };
        idleWalkMixer.SetDebugName("Idle-Walk Mixer");

        // 创建子 Mixer 2: Walk → Run → Sprint
        var runMixer = new LinearMixerState(_Animancer.Graph)
        {
            { _WalkClip, 0.0f },
            { _RunClip, 0.5f },
            { _SprintClip, 1.0f }
        };
        runMixer.SetDebugName("Run Mixer");

        // 创建父 Mixer,包含子 Mixers
        _ParentMixer = new ManualMixerState(_Animancer.Graph);
        _ParentMixer.Add(idleWalkMixer);
        _ParentMixer.Add(runMixer);
        _ParentMixer.SetDebugName("Parent Mixer");

        _ParentMixer.Play(_Animancer);
    }

    void Update()
    {
        float speed = GetCurrentSpeed();

        // 控制父 Mixer 权重
        if (speed < 0.3f)
        {
            // 低速：使用 Idle-Walk Mixer
            _ParentMixer.SetChildWeight(0, 1.0f);
            _ParentMixer.SetChildWeight(1, 0.0f);

            var childMixer = _ParentMixer.GetChild(0) as LinearMixerState;
            childMixer.Parameter = speed / 0.3f; // 归一化到 0-1
        }
        else
        {
            // 高速：使用 Run Mixer
            _ParentMixer.SetChildWeight(0, 0.0f);
            _ParentMixer.SetChildWeight(1, 1.0f);

            var childMixer = _ParentMixer.GetChild(1) as LinearMixerState;
            childMixer.Parameter = (speed - 0.3f) / 0.7f; // 归一化到 0-1
        }
    }

    float GetCurrentSpeed()
    {
        return Mathf.Clamp01(Input.GetAxis("Vertical"));
    }
}
```

---

## 完整创建示例

### 示例1：2D Directional Mixer 完整流程

```csharp
using Animancer;
using UnityEngine;

public class Complete2DMixerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _ForwardClip;
    [SerializeField] private AnimationClip _BackClip;
    [SerializeField] private AnimationClip _LeftClip;
    [SerializeField] private AnimationClip _RightClip;
    [SerializeField] private AnimationClip _ForwardLeftClip;
    [SerializeField] private AnimationClip _ForwardRightClip;
    [SerializeField] private AnimationClip _BackLeftClip;
    [SerializeField] private AnimationClip _BackRightClip;

    private DirectionalMixerState _MixerState;

    void Start()
    {
        CreateDirectionalMixer();
    }

    void CreateDirectionalMixer()
    {
        // 创建 2D Directional Mixer
        _MixerState = new DirectionalMixerState(_Animancer.Graph)
        {
            // 中心：Idle
            { _IdleClip, Vector2.zero },

            // 4 主方向
            { _ForwardClip, new Vector2(0, 1) },
            { _RightClip, new Vector2(1, 0) },
            { _BackClip, new Vector2(0, -1) },
            { _LeftClip, new Vector2(-1, 0) },

            // 4 对角线方向
            { _ForwardRightClip, new Vector2(0.707f, 0.707f) },
            { _BackRightClip, new Vector2(0.707f, -0.707f) },
            { _BackLeftClip, new Vector2(-0.707f, -0.707f) },
            { _ForwardLeftClip, new Vector2(-0.707f, 0.707f) }
        };

        // 设置调试名称
        _MixerState.SetDebugName("8-Direction Movement");

        // 配置同步（仅同步移动动画,不同步 Idle）
        _MixerState.DontSynchronize(_MixerState.GetChild(0)); // Idle

        // 播放 Mixer
        _MixerState.Play(_Animancer);
    }

    void Update()
    {
        // 获取输入
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        // 设置参数
        _MixerState.Parameter = new Vector2(horizontal, vertical);
    }
}
```

---

### 示例2：动态 Mixer 创建

```csharp
using Animancer;
using UnityEngine;
using System.Collections.Generic;

public class DynamicMixerCreationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip[] _AnimationClips;

    private LinearMixerState _MixerState;

    void Start()
    {
        CreateDynamicMixer();
    }

    void CreateDynamicMixer()
    {
        _MixerState = new LinearMixerState(_Animancer.Graph);

        // 动态添加所有动画
        for (int i = 0; i < _AnimationClips.Length; i++)
        {
            // 阈值均匀分布在 0-1 之间
            float threshold = (float)i / (_AnimationClips.Length - 1);
            _MixerState.Add(_AnimationClips[i], threshold);

            Debug.Log($"Added {_AnimationClips[i].name} at threshold {threshold:F2}");
        }

        _MixerState.SetDebugName("Dynamic Mixer");
        _MixerState.Play(_Animancer);
    }

    void Update()
    {
        float parameter = Mathf.Abs(Input.GetAxis("Vertical"));
        _MixerState.Parameter = parameter;
    }
}
```

---

## 最佳实践建议

### 1. **选择合适的创建方法**

```csharp
// ✅ 固定配置：使用 Transition（Inspector 配置）
[SerializeField] private LinearMixerTransition _FixedMixer;

// ✅ 动态创建：使用代码
void CreateDynamicMixer(AnimationClip[] clips)
{
    var mixer = new LinearMixerState(_Animancer.Graph);
    foreach (var clip in clips)
    {
        mixer.Add(clip, CalculateThreshold(clip));
    }
}
```

---

### 2. **使用调试名称**

```csharp
// ✅ 推荐：始终设置调试名称
_MixerState.SetDebugName("Movement Mixer");

// 在 Inspector 中更容易识别
```

---

### 3. **合理组织嵌套结构**

```csharp
// ❌ 不推荐：过深的嵌套
Mixer
  └─ Mixer
      └─ Mixer
          └─ Mixer（过深）

// ✅ 推荐：2-3 层嵌套
Mixer
  ├─ Mixer（IdleWalk）
  └─ Mixer（RunSprint）
```

---

### 4. **验证配置**

```csharp
void ValidateMixer(LinearMixerState mixer)
{
    if (mixer.ChildCount < 2)
    {
        Debug.LogWarning("Mixer 至少需要 2 个子动画");
    }

    // 检查阈值是否递增
    for (int i = 1; i < mixer.ChildCount; i++)
    {
        if (mixer.GetThreshold(i) <= mixer.GetThreshold(i - 1))
        {
            Debug.LogWarning($"阈值未递增: {i}");
        }
    }
}
```

---

## 常见问题 FAQ

### Q1: Transition-Based 和 Manual 创建有什么区别？

**A**:

| 特性 | Transition-Based | Manual Code |
|------|-----------------|------------|
| **配置位置** | Inspector | 代码 |
| **灵活性** | 固定配置 | 完全动态 |
| **团队协作** | 设计师友好 | 需要编程 |
| **性能** | 相同 | 相同 |

---

### Q2: 可以在运行时修改 Transition-Based Mixer 吗？

**A**: 可以修改参数,但不能修改结构。

```csharp
// ✅ 可以：修改参数
_MixerState.Parameter = newValue;

// ❌ 不能：添加/删除子动画
// Transition-Based Mixer 的结构是固定的
```

---

### Q3: 如何实现条件子动画添加？

**A**: 使用 Manual 创建方法。

```csharp
var mixer = new LinearMixerState(_Animancer.Graph);

// 条件添加
if (hasIdleAnimation)
{
    mixer.Add(_IdleClip, 0.0f);
}

if (hasWalkAnimation)
{
    mixer.Add(_WalkClip, 0.5f);
}

if (hasRunAnimation && playerLevel > 10)
{
    mixer.Add(_RunClip, 1.0f);
}
```

---

### Q4: 嵌套 Mixer 的性能如何？

**A**: 轻微性能开销,但通常可以接受。

**优化建议**：
- 限制嵌套层级（2-3 层）
- 避免不必要的嵌套
- 使用 Profiler 监控性能

---

### Q5: 自动计算阈值适用于所有情况吗？

**A**: 主要适用于有 Root Motion 的动画。

```csharp
// ✅ 适合：有 Root Motion 的移动动画
AnimancerUtilities.CalculateThresholdsFromAverageVelocityXZ(_MixerState);

// ❌ 不适合：静态动画、面部表情等
// 需要手动指定阈值
```

---

## 总结

### 核心要点

1. **两种创建方法**
   - **Transition-Based**：Inspector 配置,适合固定配置
   - **Manual Code**：代码创建,适合动态生成

2. **手动创建四步骤**
   - 引用子动画
   - 实例化 Mixer
   - 添加子状态
   - 存储引用

3. **配置元素**
   - Thresholds（阈值）
   - Debug Naming（调试命名）
   - Synchronization Control（同步控制）

4. **嵌套 Mixers**
   - Transition 嵌套
   - 手动嵌套
   - 支持多层结构

### 下一步学习

- 📖 深入学习 **Mixer Synchronization**（同步机制）
- 🎨 探索 **参数系统**的高级用法
- 📚 了解 **嵌套 Mixer** 的实际应用
- 🔍 查看实际项目中的 Mixer 创建模式

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/mixers/creation/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
