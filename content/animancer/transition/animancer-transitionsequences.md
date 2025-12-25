# Animancer Transition Sequences 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/fading/sequences/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Transition Sequences（过渡序列）** 允许您定义一系列 Transition 或 State，并将它们作为一个组进行管理和播放。它们的工作方式类似于标准的 Transition，在运行时会创建一个 `SequenceState`。

---

## 核心概念 (Core Concept)

> **TransitionSequences 允许您定义一系列 Transitions 或 States，并将它们作为一个组进行处理。**

**工作原理**：
```
TransitionSequence:
├─ Child Transition 1 (Attack1) → 播放完成
├─ Child Transition 2 (Attack2) → 播放完成
└─ Child Transition 3 (Attack3) → 播放完成

整个序列作为一个统一的 State 进行管理
```

**关键特性**：
- ✅ 将多个动画组合成一个序列
- ✅ 自动按顺序播放
- ✅ 可以作为单一 State 使用
- ✅ 支持事件管理

---

## 序列结构 (Sequence Structure)

### 基础结构

```csharp
TransitionSequence sequence = new TransitionSequence
{
    // 子过渡数组（通常是 ClipTransition）
    new ClipTransition { Clip = attack1Clip },
    new ClipTransition { Clip = attack2Clip },
    new ClipTransition { Clip = attack3Clip }
};
```

### 支持的 Transition 类型

**常用类型**：
- `ClipTransition`：单个动画片段
- `LinearMixerTransition`：1D 混合
- `MixerTransition2D`：2D 混合
- 其他任何 `ITransition` 类型

**混合类型示例**：
```csharp
TransitionSequence mixedSequence = new TransitionSequence
{
    new ClipTransition { Clip = prepareClip },      // 准备动作
    new LinearMixerTransition { /* 配置 */ },       // 混合移动
    new ClipTransition { Clip = finishClip }        // 结束动作
};
```

---

## 配置说明 (Configuration Notes)

### 1. **Fade Duration 覆盖**

**规则**：第一个子过渡的淡入持续时间会被序列自身的淡入设置覆盖。

```csharp
TransitionSequence sequence = new TransitionSequence
{
    FadeDuration = 0.2f, // ← 序列的淡入时长

    // 第一个子过渡
    new ClipTransition
    {
        Clip = clip1,
        FadeDuration = 0.5f // ← 这个值会被忽略，使用 0.2f
    },

    // 后续子过渡
    new ClipTransition
    {
        Clip = clip2,
        FadeDuration = 0.3f // ← 这个值有效
    }
};
```

**重要提示**：
- ✅ 序列的 `FadeDuration` 控制整个序列的淡入
- ⚠️ 第一个子过渡的 `FadeDuration` 被覆盖
- ✅ 后续子过渡的 `FadeDuration` 正常工作

---

### 2. **Start Time 管理**

**规则**：起始时间由序列管理，而不是单个子过渡。

```csharp
TransitionSequence sequence = new TransitionSequence
{
    NormalizedStartTime = 0.5f, // ← 序列从 50% 开始

    new ClipTransition
    {
        Clip = clip1,
        NormalizedStartTime = 0.2f // ← 这个值会被忽略
    },
    new ClipTransition { Clip = clip2 },
    new ClipTransition { Clip = clip3 }
};

// 播放序列
_Animancer.Play(sequence);
// 结果：序列会从整体进度的 50% 开始播放
// 可能直接从 clip2 或 clip3 开始（取决于各自的长度）
```

---

### 3. **其他属性正常工作**

以下属性在子过渡中正常生效：
- ✅ `Speed`（播放速度）
- ✅ `Events`（事件配置）
- ✅ `EndTime`（结束时间）
- ✅ 其他自定义属性

```csharp
TransitionSequence sequence = new TransitionSequence
{
    new ClipTransition
    {
        Clip = clip1,
        Speed = 1.5f, // ✅ 有效：加速播放
        Events = new AnimancerEvent.Sequence // ✅ 有效
        {
            // 事件配置
        }
    },
    new ClipTransition
    {
        Clip = clip2,
        Speed = 0.8f // ✅ 有效：减速播放
    }
};
```

---

## 实现示例 (Implementation Example)

### 基础用法

```csharp
using Animancer;
using UnityEngine;

public class TransitionSequenceExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionSequence _ActionSequence;
    [SerializeField] private ClipTransition _Idle;

    protected virtual void Update()
    {
        // 检测鼠标左键点击
        if (Input.GetMouseButtonDown(0))
        {
            // 播放动作序列
            AnimancerState state = _Animancer.Play(_ActionSequence);

            // 序列播放完成后返回待机
            state.Events(this).OnEnd ??= () => _Animancer.Play(_Idle);
        }
    }
}
```

**工作流程**：
```
1. 玩家点击鼠标左键
2. 播放完整的动作序列（例如：攻击1 → 攻击2 → 攻击3）
3. 序列播放完成
4. 自动返回待机动画
```

---

## 事件管理 (Event Management)

### 使用 Central Event System

**推荐方式**：使用集中式事件系统，这样脚本不需要了解序列的具体设置。

```csharp
using Animancer;
using UnityEngine;

public class CentralEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionSequence _AttackSequence;
    [SerializeField] private ClipTransition _Idle;

    void PerformAttack()
    {
        var state = _Animancer.Play(_AttackSequence);

        // 使用 Central Event System
        state.Events(this).OnEnd ??= OnAttackSequenceEnd;
    }

    void OnAttackSequenceEnd()
    {
        Debug.Log("攻击序列完成");
        _Animancer.Play(_Idle);
    }
}
```

---

### 为子过渡添加事件

**方法1：在序列配置中添加事件**

```csharp
TransitionSequence sequence = new TransitionSequence
{
    new ClipTransition
    {
        Clip = attack1Clip,
        Events = new AnimancerEvent.Sequence
        {
            OnEnd = () => Debug.Log("攻击1完成")
        }
    },
    new ClipTransition
    {
        Clip = attack2Clip,
        Events = new AnimancerEvent.Sequence
        {
            OnEnd = () => Debug.Log("攻击2完成")
        }
    },
    new ClipTransition
    {
        Clip = attack3Clip,
        Events = new AnimancerEvent.Sequence
        {
            OnEnd = () => Debug.Log("攻击3完成")
        }
    }
};
```

---

**方法2：运行时添加事件**

```csharp
void PlaySequenceWithEvents()
{
    var state = _Animancer.Play(_AttackSequence) as SequenceState;

    // 为每个子状态添加事件
    for (int i = 0; i < state.ChildCount; i++)
    {
        var childState = state.GetChild(i);
        int index = i; // 捕获循环变量

        childState.Events(this).OnEnd = () =>
        {
            Debug.Log($"子动画 {index} 完成");
        };
    }
}
```

---

## Transition Assets 集成

**序列也可以保存为 Transition Assets**，实现跨脚本重用。

### 创建 TransitionSequence Asset

**步骤**：
1. 右键 → Create → Animancer → Transition Sequence
2. 配置子过渡数组
3. 在脚本中引用

**示例**：
```csharp
using Animancer;
using UnityEngine;

public class SequenceAssetExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 引用外部的 TransitionSequence Asset
    [SerializeField] private TransitionAssetBase _ComboSequenceAsset;

    void PlayCombo()
    {
        _Animancer.Play(_ComboSequenceAsset);
    }
}
```

**Asset 配置示例**：
```
ComboSequence.asset:
├─ Fade Duration: 0.2
├─ Speed: 1.0
└─ Children:
    ├─ [0] Attack1.asset (ClipTransition)
    ├─ [1] Attack2.asset (ClipTransition)
    └─ [2] Attack3.asset (ClipTransition)
```

---

## 与 Timeline 对比

**相似功能**：Unity 的 Timeline 也提供了类似的序列功能。

**对比表**：

| 特性 | TransitionSequence | Timeline |
|------|-------------------|----------|
| **易用性** | ✅ 简单直接 | ⚠️ 较复杂 |
| **性能** | ✅ 轻量级 | ⚠️ 较重 |
| **灵活性** | ✅ 代码优先 | ✅ 可视化编辑 |
| **事件系统** | ✅ 集成 Animancer Events | ✅ Markers |
| **适用场景** | 游戏玩法动画 | 过场动画 |

**选择建议**：
- ✅ **TransitionSequence**：游戏玩法中的动作序列（攻击连击、技能释放）
- ✅ **Timeline**：复杂的过场动画、多轨道同步

---

## 代码示例集合

### 示例1：三段攻击连击

```csharp
using Animancer;
using UnityEngine;

public class ThreeHitComboExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Attack1;
    [SerializeField] private AnimationClip _Attack2;
    [SerializeField] private AnimationClip _Attack3;
    [SerializeField] private ClipTransition _Idle;

    private TransitionSequence _ComboSequence;

    void Start()
    {
        // 创建三段攻击序列
        _ComboSequence = new TransitionSequence
        {
            FadeDuration = 0.15f,

            new ClipTransition { Clip = _Attack1, Speed = 1.2f },
            new ClipTransition { Clip = _Attack2, Speed = 1.0f },
            new ClipTransition { Clip = _Attack3, Speed = 0.9f }
        };
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            PerformCombo();
        }
    }

    void PerformCombo()
    {
        var state = _Animancer.Play(_ComboSequence);
        state.Events(this).OnEnd = () => _Animancer.Play(_Idle);

        Debug.Log("执行三段连击");
    }
}
```

---

### 示例2：技能释放序列

```csharp
using Animancer;
using UnityEngine;

public class SkillCastSequenceExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _PrepareClip;  // 准备动作
    [SerializeField] private AnimationClip _CastClip;     // 施法动作
    [SerializeField] private AnimationClip _RecoverClip;  // 恢复动作
    [SerializeField] private ClipTransition _Idle;

    private TransitionSequence _SkillSequence;

    void Start()
    {
        _SkillSequence = new TransitionSequence
        {
            FadeDuration = 0.2f,

            new ClipTransition
            {
                Clip = _PrepareClip,
                Events = new AnimancerEvent.Sequence
                {
                    OnEnd = OnPrepareComplete
                }
            },
            new ClipTransition
            {
                Clip = _CastClip,
                Events = new AnimancerEvent.Sequence
                {
                    new AnimancerEvent(0.5f, OnCastEffect) // 50% 时触发特效
                }
            },
            new ClipTransition { Clip = _RecoverClip }
        };
    }

    void CastSkill()
    {
        var state = _Animancer.Play(_SkillSequence);
        state.Events(this).OnEnd = () => _Animancer.Play(_Idle);
    }

    void OnPrepareComplete()
    {
        Debug.Log("准备完成，开始施法");
    }

    void OnCastEffect()
    {
        Debug.Log("触发技能特效");
        // 实例化特效、伤害判定等
    }
}
```

---

### 示例3：动态构建序列

```csharp
using Animancer;
using UnityEngine;
using System.Collections.Generic;

public class DynamicSequenceExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip[] _AttackClips;
    [SerializeField] private ClipTransition _Idle;

    void PerformRandomCombo(int attackCount)
    {
        // 动态创建序列
        List<ClipTransition> transitions = new List<ClipTransition>();

        for (int i = 0; i < attackCount; i++)
        {
            // 随机选择攻击动画
            AnimationClip randomClip = _AttackClips[Random.Range(0, _AttackClips.Length)];

            transitions.Add(new ClipTransition
            {
                Clip = randomClip,
                FadeDuration = 0.1f,
                Speed = Random.Range(0.9f, 1.2f) // 随机速度
            });
        }

        // 创建序列
        TransitionSequence sequence = new TransitionSequence();
        sequence.FadeDuration = 0.2f;
        foreach (var transition in transitions)
        {
            sequence.Add(transition);
        }

        // 播放序列
        var state = _Animancer.Play(sequence);
        state.Events(this).OnEnd = () => _Animancer.Play(_Idle);

        Debug.Log($"执行 {attackCount} 段随机连击");
    }
}
```

---

### 示例4：条件跳过子序列

```csharp
using Animancer;
using UnityEngine;

public class ConditionalSequenceExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _LongPrepare;  // 长准备动作
    [SerializeField] private AnimationClip _QuickPrepare; // 快速准备
    [SerializeField] private AnimationClip _Attack;
    [SerializeField] private ClipTransition _Idle;

    void PerformAttack(bool hasTime)
    {
        TransitionSequence sequence;

        if (hasTime)
        {
            // 有时间：使用长准备
            sequence = new TransitionSequence
            {
                new ClipTransition { Clip = _LongPrepare },
                new ClipTransition { Clip = _Attack }
            };
        }
        else
        {
            // 时间紧迫：使用快速准备
            sequence = new TransitionSequence
            {
                new ClipTransition { Clip = _QuickPrepare },
                new ClipTransition { Clip = _Attack }
            };
        }

        var state = _Animancer.Play(sequence);
        state.Events(this).OnEnd = () => _Animancer.Play(_Idle);
    }
}
```

---

### 示例5：嵌套序列（高级）

```csharp
using Animancer;
using UnityEngine;

public class NestedSequenceExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionSequence _IntroSequence;  // 前置序列
    [SerializeField] private TransitionSequence _MainSequence;   // 主要序列
    [SerializeField] private TransitionSequence _OutroSequence;  // 后续序列
    [SerializeField] private ClipTransition _Idle;

    void PerformFullSequence()
    {
        // 创建嵌套序列
        TransitionSequence fullSequence = new TransitionSequence
        {
            FadeDuration = 0.25f,

            _IntroSequence,  // 子序列1
            _MainSequence,   // 子序列2
            _OutroSequence   // 子序列3
        };

        var state = _Animancer.Play(fullSequence);
        state.Events(this).OnEnd = () => _Animancer.Play(_Idle);

        Debug.Log("播放完整嵌套序列");
    }
}
```

---

## 最佳实践建议

### 1. **使用 Central Event System**

```csharp
// ✅ 推荐：使用集中式事件系统
state.Events(this).OnEnd ??= OnSequenceEnd;

// ❌ 不推荐：直接在序列中硬编码
sequence.Events.OnEnd = () => { /* 特定逻辑 */ };
```

**优势**：
- 脚本不需要了解序列的内部结构
- 更容易维护和修改
- 更好的代码解耦

---

### 2. **合理设置淡入时长**

```csharp
// ✅ 推荐：序列设置较短的淡入时长
TransitionSequence sequence = new TransitionSequence
{
    FadeDuration = 0.15f, // 快速启动

    new ClipTransition { Clip = clip1 },
    new ClipTransition
    {
        Clip = clip2,
        FadeDuration = 0.25f // 子过渡之间可以更平滑
    }
};
```

---

### 3. **避免过长的序列**

```csharp
// ⚠️ 不推荐：序列过长
TransitionSequence tooLong = new TransitionSequence
{
    // 10+ 个子过渡...
};

// ✅ 推荐：拆分成多个短序列
void PlayAttackPhase1() { /* 序列1 */ }
void PlayAttackPhase2() { /* 序列2 */ }
```

**原因**：
- 更容易中断和控制
- 更好的调试体验
- 更灵活的游戏逻辑

---

### 4. **使用 TransitionAsset 重用**

```csharp
// ✅ 推荐：将常用序列保存为 Asset
[SerializeField] private TransitionAssetBase _ComboAsset;

void PerformCombo()
{
    _Animancer.Play(_ComboAsset);
}
```

---

## 常见问题 FAQ

### Q1: TransitionSequence 和手动切换动画有什么区别？

**A**:

**手动切换**：
```csharp
// 需要手动管理状态转换
state1.Events.OnEnd = () => {
    var state2 = _Animancer.Play(clip2);
    state2.Events.OnEnd = () => {
        var state3 = _Animancer.Play(clip3);
        // ...
    };
};
```

**TransitionSequence**：
```csharp
// 自动管理，简洁清晰
TransitionSequence sequence = new TransitionSequence
{
    new ClipTransition { Clip = clip1 },
    new ClipTransition { Clip = clip2 },
    new ClipTransition { Clip = clip3 }
};
_Animancer.Play(sequence);
```

---

### Q2: 为什么第一个子过渡的 FadeDuration 会被覆盖？

**A**: 因为序列作为一个整体进行淡入淡出。第一个子过渡是序列的起点，使用序列的淡入设置保证了一致性。

---

### Q3: 可以在序列播放过程中中断吗？

**A**: 可以！

```csharp
// 播放序列
var sequenceState = _Animancer.Play(_AttackSequence);

// 条件中断
if (shouldInterrupt)
{
    _Animancer.Play(_InterruptClip, fadeDuration: 0.1f);
}
```

---

### Q4: TransitionSequence 支持循环播放吗？

**A**: 可以通过事件实现循环：

```csharp
void PlayLoopingSequence()
{
    var state = _Animancer.Play(_Sequence);
    state.Events(this).OnEnd = () => PlayLoopingSequence(); // 递归调用
}
```

---

### Q5: 如何获取当前播放的是序列中的哪个子动画？

**A**:

```csharp
var sequenceState = _Animancer.Play(_Sequence) as SequenceState;

void Update()
{
    if (sequenceState != null)
    {
        int currentIndex = sequenceState.Index;
        Debug.Log($"当前播放子动画索引: {currentIndex}");
    }
}
```

---

### Q6: TransitionSequence 和 Timeline 应该如何选择？

**A**:

| 场景 | 推荐方案 |
|------|---------|
| 游戏玩法连击 | TransitionSequence |
| 过场动画 | Timeline |
| 多轨道同步 | Timeline |
| 简单动作序列 | TransitionSequence |
| 需要代码控制 | TransitionSequence |
| 需要可视化编辑 | Timeline |

---

## 总结

### 核心要点

1. **序列的本质**
   - 将多个 Transition 组合成一个统一的 State
   - 自动按顺序播放
   - 支持各种 Transition 类型

2. **配置规则**
   - 序列的 `FadeDuration` 覆盖第一个子过渡
   - `StartTime` 由序列管理
   - 其他属性正常工作

3. **事件管理**
   - 推荐使用 Central Event System
   - 可以为每个子过渡添加独立事件
   - 序列整体也支持事件

4. **与 Timeline 对比**
   - TransitionSequence：轻量级，适合游戏玩法
   - Timeline：功能强大，适合过场动画

### 下一步学习

- 📖 深入学习 **Layers** 的序列应用
- 🎨 探索 **Events** 系统的高级用法
- 📚 了解 **SequenceState** 的内部机制
- 🔍 查看实际项目中的连击系统实现

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/fading/sequences/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
