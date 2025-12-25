# Animancer Transitions 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/transitions/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

Animancer 区分了动画控制中的两个核心概念：

- **State（状态）**：包含当前动画信息，如 `Time`（时间）和 `Speed`（速度）
- **Transition（过渡/转换）**：持有可序列化的数据，定义如何创建和播放状态，包括 `AnimationClip` 和淡入持续时间

## 关键概念 (Key Concept)

> **Transition 包含可序列化的数据，这些数据定义了如何创建和播放一个状态，例如它的 `AnimationClip` 和用于混合的淡入持续时间。**

Animancer 中的每种状态类型都有对应的过渡类型。当传递给 `AnimancerComponent.Play(ITransition)` 时，它会创建相应的状态类型——例如，`ClipTransition` 创建一个 `ClipState` 来播放单个动画片段。

---

## Transition 字段参考 (Transition Field Reference)

| 字段名称 | 代码属性 | 用途说明 |
|---------|----------|---------|
| **Animation（动画）** | `Clip` | 要播放的 AnimationClip（动画片段） |
| **Fade Duration（淡入时长）** | `FadeDuration` | 从上一个动画交叉淡入的时间（0 表示立即播放） |
| **Speed（播放速度）** | `Speed` | 播放速度倍率；负值表示倒放 |
| **Start Time（起始时间）** | `NormalizedStartTime` | 播放时的初始动画时间位置 |
| **End Time（结束时间）** | `Events.NormalizedEndTime` | 决定何时触发结束事件 |
| **Events（事件）** | `Events` | 过渡细节的时间轴可视化 |

---

## 时间字段单位 (Time Field Units)

提供三种测量系统：

### 1. **Normalized（归一化，x）**
- 动画长度的倍数
- 示例：`0.5x` = 动画播放到一半的位置
- 用途：与动画实际长度无关的相对时间

### 2. **Seconds（秒，s）**
- 实际时间持续时间
- 示例：`0.5s` = 半秒
- 用途：精确的时间控制

### 3. **Frames（帧，f）**
- 基于动画帧的计数
- 示例：`1f` = 一帧
- 用途：逐帧精确控制

**注意**：不同字段的底层存储格式可能不同，具体请参考字段参考表。

---

## 显示近似值 (Display Approximations)

> **这些字段会自动缩写它们的值以适应可用区域，并使用 `~` 符号来表示显示的值只是实际值的近似值。**

**示例**：
- `0~` - 非常接近 0 的值
- `1.2345~` - 显示了部分小数位
- `1.23e+7` - 科学计数法表示

这在 Inspector 窗口空间有限时很有用。

---

## 默认值 (Default Values)

**中键点击**时间字段可以将其设置为默认值：

| 字段 | 主要默认值 | 次要默认值 |
|------|-----------|-----------|
| **Fade Duration**（淡入时长） | 0.25s | 0s（立即切换） |
| **Speed**（播放速度） | 1x（正常速度） | -1x（倒放） |
| **Start Time**（起始时间） | Auto（自动） | Auto |
| **End Time**（结束时间） | Auto（自动） | Auto |

**操作提示**：
- **单次中键点击**：设置为主要默认值（如 0.25s）
- **连续中键点击**：切换到次要默认值（如 0s）

---

## 实现示例 (Implementation Example)

### 基础用法

```csharp
using Animancer;
using UnityEngine;

public class TransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private ClipTransition _Animation;

    protected virtual void OnEnable()
    {
        // 播放 Transition，自动创建对应的 State
        _Animancer.Play(_Animation);
    }
}
```

### 工作流程解析

1. **序列化**：`ClipTransition` 在 Inspector 中配置
2. **播放**：调用 `_Animancer.Play(_Animation)`
3. **创建状态**：Animancer 内部创建 `ClipState`
4. **应用设置**：应用 Fade Duration、Speed 等配置
5. **开始播放**：动画开始播放并混合

---

## Transition 存储方法 (Transition Storage Methods)

### 方法一：内联 Transitions (Inline Transitions)

**定义**：直接存储在脚本中的 Transition

**优点**：
- 简单直接
- 适合单一脚本使用
- 配置集中在一个地方

**示例**：
```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    // 内联 Transition，直接在脚本中配置
    [SerializeField]
    private ClipTransition _IdleAnimation;

    [SerializeField]
    private ClipTransition _WalkAnimation;

    void Start()
    {
        _Animancer.Play(_IdleAnimation);
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.Play(_WalkAnimation);
        }
        else
        {
            _Animancer.Play(_IdleAnimation);
        }
    }
}
```

**适用场景**：
- 动画配置只在一个脚本中使用
- 不需要在多个地方共享配置
- 快速原型开发

---

### 方法二：Transition Assets (Transition 资源)

**定义**：存储在 ScriptableObject 资源文件中的 Transition，可以在多个脚本之间引用

**优点**：
- 可重用性高
- 多个脚本可以共享同一配置
- 便于统一管理和修改
- 支持运行时动态加载

**创建方法**：
```
右键 → Create → Animancer → Clip Transition
```

**示例代码**：
```csharp
public class CharacterAnimations : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    // 引用外部的 Transition Asset
    [SerializeField]
    private TransitionAsset _IdleTransition;

    [SerializeField]
    private TransitionAsset _WalkTransition;

    void Start()
    {
        _Animancer.Play(_IdleTransition);
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.Play(_WalkTransition);
        }
        else
        {
            _Animancer.Play(_IdleTransition);
        }
    }
}
```

**适用场景**：
- 同一动画配置需要在多个脚本中使用
- 需要统一管理所有动画配置
- 大型项目，需要良好的资源组织

**文件结构示例**：
```
Assets/
└── Animations/
    └── Transitions/
        ├── Idle.asset
        ├── Walk.asset
        ├── Run.asset
        └── Jump.asset
```

---

## Transition 类型对照表

| Transition 类型 | 创建的 State 类型 | 用途 |
|----------------|------------------|------|
| `ClipTransition` | `ClipState` | 播放单个动画片段 |
| `LinearMixerTransition` | `LinearMixerState` | 1D 混合（如速度混合） |
| `MixerTransition2D` | `Mixer2D` | 2D 混合（如方向混合） |
| `ManualMixerTransition` | `ManualMixerState` | 手动控制权重混合 |
| `ControllerTransition` | `ControllerState` | 包装 Animator Controller |

---

## 相关文档主题 (Related Documentation Topics)

### 1. **Transition Types（过渡类型）**
- 详细介绍各种 Transition 类型
- 每种类型的具体使用场景
- 高级配置选项

### 2. **Transition Assets（过渡资源）**
- 如何创建和管理 Transition Asset
- ScriptableObject 的优势
- 资源组织最佳实践

### 3. **Transition Libraries（过渡库）**
- 批量管理 Transition
- 创建动画库系统
- 运行时动态选择动画

### 4. **Transition Previews（过渡预览）**
- 在编辑器中预览动画
- 调试工具使用
- Inspector 窗口功能

---

## 最佳实践建议

### 1. **选择合适的存储方式**

**使用内联 Transition 的情况**：
- ✅ 动画配置只在一个脚本中使用
- ✅ 快速原型开发
- ✅ 简单的动画控制

**使用 Transition Asset 的情况**：
- ✅ 需要在多个脚本间共享配置
- ✅ 大型项目，需要统一管理
- ✅ 需要运行时动态加载动画

### 2. **Fade Duration 设置建议**

```csharp
// 不同场景的推荐值
Idle → Walk:     0.25s  // 平滑过渡
Walk → Run:      0.2s   // 较快过渡
任意 → Hit:      0.05s  // 立即反馈
任意 → Death:    0.1s   // 快速切换
```

### 3. **Speed 使用技巧**

```csharp
// 正常播放
transition.Speed = 1;

// 快速播放（如快速装弹）
transition.Speed = 1.5f;

// 慢动作效果
transition.Speed = 0.5f;

// 倒放动画
transition.Speed = -1;
```

### 4. **Start Time 应用场景**

```csharp
// 从头开始播放
transition.NormalizedStartTime = 0;

// 从中间开始（跳过前置动作）
transition.NormalizedStartTime = 0.3f;

// 从末尾开始倒放
transition.NormalizedStartTime = 1;
transition.Speed = -1;
```

---

## 代码示例集合

### 示例1：基础播放

```csharp
using Animancer;
using UnityEngine;

public class BasicPlayExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Idle;
    [SerializeField] private ClipTransition _Walk;

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.Play(_Walk);
        }
        else
        {
            _Animancer.Play(_Idle);
        }
    }
}
```

### 示例2：获取播放后的状态

```csharp
using Animancer;
using UnityEngine;

public class StateAccessExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Animation;

    void Start()
    {
        // 播放并获取返回的状态
        AnimancerState state = _Animancer.Play(_Animation);

        // 可以进一步操作状态
        state.Speed = 2; // 加速播放
        state.Time = 0.5f; // 跳到特定时间
    }
}
```

### 示例3：动态修改 Transition

```csharp
using Animancer;
using UnityEngine;

public class DynamicTransitionExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Animation;

    void PlayWithCustomSettings()
    {
        // 临时修改 Transition 设置
        _Animation.FadeDuration = 0.5f;
        _Animation.Speed = 1.5f;
        _Animation.NormalizedStartTime = 0.2f;

        // 使用修改后的设置播放
        _Animancer.Play(_Animation);
    }
}
```

### 示例4：处理动画事件

```csharp
using Animancer;
using UnityEngine;

public class EventHandlingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Animation;

    void Start()
    {
        // 播放动画
        AnimancerState state = _Animancer.Play(_Animation);

        // 添加结束事件
        state.Events.OnEnd = OnAnimationEnd;
    }

    private void OnAnimationEnd()
    {
        Debug.Log("动画播放结束！");
    }
}
```

---

## 常见问题 FAQ

### Q1: Transition 和 State 有什么区别？

**A**:
- **Transition**：可序列化的配置数据，定义"如何"播放动画
- **State**：运行时的动画状态对象，包含当前播放信息

类比：Transition 是"食谱"，State 是"正在烹饪的菜"。

---

### Q2: 为什么要使用 Transition 而不是直接播放 AnimationClip？

**A**: Transition 提供了更多控制选项：
- ✅ 淡入时长（Fade Duration）
- ✅ 播放速度（Speed）
- ✅ 起始时间（Start Time）
- ✅ 事件配置（Events）
- ✅ 可序列化存储

---

### Q3: 何时应该使用 Transition Asset？

**A**: 当满足以下任一条件时：
- 需要在多个脚本中使用同一动画配置
- 需要统一管理所有动画资源
- 需要运行时动态加载动画
- 项目规模较大，需要良好的组织结构

---

### Q4: Fade Duration 设置为 0 会怎样？

**A**:
- 动画会**立即切换**，没有混合过渡
- 适用于需要快速反馈的场景（如受击、死亡）
- 不适合需要平滑过渡的场景（如待机到行走）

---

### Q5: 可以在运行时修改 Transition 的值吗？

**A**: 可以！Transition 的所有属性都可以在运行时修改：

```csharp
// 运行时修改
_Animation.FadeDuration = 0.5f;
_Animation.Speed = 2.0f;
_Animancer.Play(_Animation);
```

但要注意：如果使用 Transition Asset，修改会影响所有引用它的地方。

---

### Q6: 如何实现动画倒放？

**A**: 设置 Speed 为负值：

```csharp
_Animation.Speed = -1; // 正常速度倒放
_Animation.Speed = -2; // 双倍速度倒放
```

---

## 总结

### 核心要点

1. **Transition 是配置，State 是运行时对象**
   - Transition 定义"如何"播放
   - State 包含"当前"状态

2. **两种存储方式各有优势**
   - 内联：简单直接，适合单一使用
   - Asset：可重用，适合大型项目

3. **丰富的配置选项**
   - Fade Duration：控制混合时间
   - Speed：控制播放速度
   - Start/End Time：控制播放区间
   - Events：添加事件回调

4. **灵活的时间单位**
   - Normalized：相对时间
   - Seconds：绝对时间
   - Frames：逐帧控制

### 下一步学习

- 📖 学习不同的 **Transition Types**（Mixer、Controller 等）
- 🎨 探索 **Transition Assets** 的高级用法
- 📚 了解 **Transition Libraries** 管理大量动画
- 🔍 使用 **Transition Previews** 工具调试动画

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/transitions/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
