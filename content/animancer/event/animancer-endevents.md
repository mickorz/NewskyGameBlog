# Animancer - End Events 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [End Events vs 其他事件](#end-events-vs-其他事件)
- [使用方法](#使用方法)
- [时间机制](#时间机制)
- [共享状态处理](#共享状态处理)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

**End Events** 是 Animancer 中用于处理动画结束的特殊事件系统，具有独特的触发机制。

### 🎯 核心定义

> **End Events 在指定点之后每帧触发，只要动画继续播放**

### 🔑 关键特性

- **Lite 版本可用**：End Events 在 Animancer Lite 和 Pro 中都完全可用
- **持续触发**：不同于一次性事件，End Events 在动画结束后每帧都会触发
- **确保执行**：即使动画已经经过结束点，事件仍会触发

---

## 核心概念

### 🔄 触发机制对比

```
常规 Animancer Events:
时间轴: 0 ──→ 0.5 ──→ 1.0
              ↑
           触发 1 次

End Events:
时间轴: 0 ──→ 1.0 ──→ 1.1 ──→ 1.2 ──→ ...
              ↑      ↑      ↑
           触发   触发   触发   (持续触发)
```

### 📊 触发行为

| 事件类型 | 触发时机 | 触发次数 | 典型用途 |
|---------|---------|---------|---------|
| **Animancer Events** | 通过特定时间点的那一帧 | 1次 | 特定时刻的事件 |
| **End Events** | 到达指定点后的每一帧 | 持续 | 动画结束后的处理 |
| **Exit Events** | 动画被中断时 | 1次 | 清理/过渡 |

---

## End Events vs 其他事件

### 📋 详细对比

#### 1. Animancer Events（常规事件）

```csharp
// 仅在动画时间经过0.5s的那一帧触发
state.Events.Add(0.5f, OnEvent);

// 触发后即使时间倒回再经过，也不会再次触发（同一帧内）
```

**适用场景：**
- 攻击判定
- 脚步声
- 特效触发
- 任何需要精确时刻触发的事件

#### 2. End Events（结束事件）

```csharp
// 动画到达结束点后，每帧都触发
state.Events.OnEnd = OnAnimationEnd;

// 即使动画已经结束，只要还在播放，每帧都会调用OnAnimationEnd
```

**适用场景：**
- 动画完成后自动播放其他动画
- 确保不会遗漏事件触发
- 需要保证回调执行的场景

#### 3. Exit Events（退出事件）

```csharp
// 动画被中断时触发
state.Events.OnExit = OnAnimationExit;

// 例如：正在播放攻击动画，突然切换到受击动画
```

**适用场景：**
- 清理资源
- 重置状态
- 过渡处理

### 🎯 选择建议

```csharp
// ✅ 使用 End Events
if (needsToTriggerAfterCompletion)
{
    state.Events.OnEnd = OnComplete;
}

// ✅ 使用 Animancer Events
if (needsToTriggerAtSpecificTime)
{
    state.Events.Add(0.5f, OnEvent);
}

// ✅ 使用 Exit Events
if (needsToTriggerWhenInterrupted)
{
    state.Events.OnExit = OnExit;
}
```

---

## 使用方法

### 方法1：在 Transitions 中设置

> **推荐**：在 Awake() 期间分配回调

```csharp
using Animancer;
using UnityEngine;

public class TransitionEndEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackTransition;

    void Awake()
    {
        // 在Awake中为Transition设置End Event
        _AttackTransition.Events.OnEnd = OnAttackEnd;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            // 播放时自动应用End Event
            _Animancer.Play(_AttackTransition);
        }
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击动画结束");
        _Animancer.Play(_IdleClip);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### 方法2：在 States 中设置

> **播放后立即分配**

```csharp
using Animancer;
using UnityEngine;

public class StateEndEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformAttack();
        }
    }

    void PerformAttack()
    {
        // 播放动画
        var state = _Animancer.Play(_AttackClip);

        // 使用 ??= 避免覆盖已存在的回调
        state.Events(this).OnEnd ??= OnAttackEnd;
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击结束");
        _Animancer.Play(_IdleClip);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### ⚠️ 使用 ??= 的重要性

```csharp
// ✅ 好：使用 ??= 避免覆盖
state.Events(this).OnEnd ??= OnAttackEnd;

// ❌ 差：使用 = 会覆盖已存在的回调
state.Events(this).OnEnd = OnAttackEnd;
```

---

## 时间机制

### ⏱️ End Time 计算规则

End Event 的触发时间基于动画速度：

| 动画速度 | End Time（归一化时间） | 说明 |
|---------|----------------------|------|
| **正速度** (Speed > 0) | 1.0 | 动画结束点 |
| **负速度** (Speed < 0) | 0.0 | 动画开始点 |
| **自定义** | 手动指定值 | 任意时间点 |

### 📝 代码示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// End Time 机制示例
/// </summary>
public class EndTimeExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    void Start()
    {
        TestPositiveSpeed();
        TestNegativeSpeed();
        TestCustomEndTime();
    }

    void TestPositiveSpeed()
    {
        var state = _Animancer.Play(_Clip);
        state.Speed = 1.0f; // 正速度

        // End Time 自动设置为 1.0（归一化时间）
        Debug.Log($"End Time: {state.Events.NormalizedEndTime}"); // 1.0

        state.Events.OnEnd = () => {
            Debug.Log($"[正速度] 动画结束 @ 时间={state.NormalizedTime}");
        };
    }

    void TestNegativeSpeed()
    {
        var state = _Animancer.Play(_Clip);
        state.Speed = -1.0f; // 负速度（倒播）

        // End Time 自动设置为 0.0（归一化时间）
        Debug.Log($"End Time: {state.Events.NormalizedEndTime}"); // 0.0

        state.Events.OnEnd = () => {
            Debug.Log($"[负速度] 动画结束 @ 时间={state.NormalizedTime}");
        };
    }

    void TestCustomEndTime()
    {
        var state = _Animancer.Play(_Clip);

        // 手动指定 End Time
        state.Events.NormalizedEndTime = 0.8f; // 80%时触发

        state.Events.OnEnd = () => {
            Debug.Log($"[自定义] 动画到达80% @ 时间={state.NormalizedTime}");
        };
    }
}
```

### 🔍 默认值

```csharp
// 默认值为 float.NaN（未设置）
if (float.IsNaN(state.Events.NormalizedEndTime))
{
    Debug.Log("End Time 未设置，将自动根据速度计算");
}
```

---

## 共享状态处理

### 🔀 多脚本共享状态问题

当多个脚本使用同一 AnimationClip 时，它们共享同一个 AnimancerState：

```csharp
// ScriptA.cs
var state1 = _Animancer.Play(_SharedClip);
state1.Events.OnEnd = ScriptA_OnEnd;

// ScriptB.cs
var state2 = _Animancer.Play(_SharedClip);
state2.Events.OnEnd = ScriptB_OnEnd; // 覆盖了ScriptA的回调！

// state1 和 state2 是同一个对象
Debug.Log(state1 == state2); // True
```

### 🛡️ 使用 SharedOwner 避免冲突

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 共享状态所有权示例
/// 使用SharedOwner避免多个脚本的事件冲突
/// </summary>
public class SharedOwnerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _SharedClip;

    // 使用object作为所有权标识
    private readonly object _myOwner = new object();

    void Start()
    {
        var state = _Animancer.Play(_SharedClip);

        // 检查是否已有其他脚本设置了End Event
        if (state.Events.SharedOwner == null)
        {
            // 我是第一个，设置所有权
            state.Events.SharedOwner = _myOwner;
            state.Events.OnEnd = OnMyEnd;

            Debug.Log("我获得了所有权");
        }
        else if (state.Events.SharedOwner == _myOwner)
        {
            // 我已经拥有所有权
            Debug.Log("我已经拥有所有权");
        }
        else
        {
            // 其他脚本拥有所有权
            Debug.Log("其他脚本拥有所有权，我不能修改End Event");
        }
    }

    void OnMyEnd()
    {
        Debug.Log("我的End Event触发");
    }
}
```

### 📚 所有权模式对比

```csharp
// 模式1：使用MonoBehaviour作为Owner（推荐）
state.Events.SharedOwner = this;
state.Events.OnEnd = OnEnd;

// 模式2：使用自定义对象
private readonly object _owner = new object();
state.Events.SharedOwner = _owner;

// 模式3：使用字符串（不推荐）
state.Events.SharedOwner = "MyScript";
```

---

## 代码示例

### 示例1：动画链播放

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 动画链播放示例
/// 使用End Events实现顺序播放
/// </summary>
public class AnimationChainExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Animation1;
    [SerializeField] private ClipTransition _Animation2;
    [SerializeField] private ClipTransition _Animation3;

    void Start()
    {
        // 设置动画链
        _Animation1.Events.OnEnd = () => _Animancer.Play(_Animation2);
        _Animation2.Events.OnEnd = () => _Animancer.Play(_Animation3);
        _Animation3.Events.OnEnd = () => Debug.Log("动画链完成");

        // 开始播放
        _Animancer.Play(_Animation1);
    }
}
```

### 示例2：防止重复触发

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 防止End Event重复触发示例
/// </summary>
public class PreventDuplicateExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    private bool _hasEnded = false;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformAttack();
        }
    }

    void PerformAttack()
    {
        _hasEnded = false; // 重置标志

        var state = _Animancer.Play(_AttackClip);

        state.Events.OnEnd = () => {
            // 使用标志避免重复处理
            if (!_hasEnded)
            {
                _hasEnded = true;
                OnAttackEnd();
            }
        };
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击结束（只执行一次）");
        _Animancer.Play(_IdleClip);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### 示例3：条件性切换

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 条件性动画切换示例
/// 根据状态决定下一个动画
/// </summary>
public class ConditionalSwitchExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Attack1;
    [SerializeField] private ClipTransition _Attack2;
    [SerializeField] private ClipTransition _Attack3;
    [SerializeField] private ClipTransition _Idle;

    private int _comboCount = 0;
    private bool _inputReceived = false;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            if (_comboCount == 0)
            {
                StartCombo();
            }
            else
            {
                _inputReceived = true;
            }
        }
    }

    void StartCombo()
    {
        _comboCount = 1;
        _inputReceived = false;

        PlayAttack(_Attack1);
    }

    void PlayAttack(ClipTransition attack)
    {
        var state = _Animancer.Play(attack);

        state.Events.OnEnd = () => {
            if (_inputReceived && _comboCount < 3)
            {
                // 玩家输入了下一次攻击
                _comboCount++;
                _inputReceived = false;

                var nextAttack = _comboCount switch
                {
                    2 => _Attack2,
                    3 => _Attack3,
                    _ => _Idle
                };

                PlayAttack(nextAttack);
            }
            else
            {
                // 连击结束
                _comboCount = 0;
                _Animancer.Play(_Idle);
                Debug.Log("连击结束");
            }
        };
    }
}
```

### 示例4：循环动画的End Event

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 循环动画End Event示例
/// 演示循环动画的End Event行为
/// </summary>
public class LoopingEndEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _LoopClip;

    private int _loopCount = 0;
    private const int _maxLoops = 3;

    void Start()
    {
        var state = _Animancer.Play(_LoopClip);
        state.IsLooping = true;

        // 循环动画的End Event在每次循环结束时触发
        state.Events.OnEnd = OnLoopEnd;
    }

    void OnLoopEnd()
    {
        _loopCount++;
        Debug.Log($"循环次数: {_loopCount}");

        // 达到最大循环次数后停止
        if (_loopCount >= _maxLoops)
        {
            Debug.Log("停止循环");
            _Animancer.Stop();
        }
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **使用 ??= 避免覆盖**
```csharp
// ✅ 好：保留已存在的回调
state.Events.OnEnd ??= OnEnd;
```

2. **使用标志避免重复触发**
```csharp
// ✅ 好：防止重复处理
bool _hasEnded = false;
state.Events.OnEnd = () => {
    if (!_hasEnded)
    {
        _hasEnded = true;
        HandleEnd();
    }
};
```

3. **使用 SharedOwner 管理共享状态**
```csharp
// ✅ 好：声明所有权
if (state.Events.SharedOwner == null)
{
    state.Events.SharedOwner = this;
    state.Events.OnEnd = OnEnd;
}
```

4. **在Awake中为Transition设置End Event**
```csharp
// ✅ 好：配置一次，重复使用
void Awake()
{
    _Transition.Events.OnEnd = OnEnd;
}
```

### ❌ DON'T（避免做法）

1. **直接覆盖End Event**
```csharp
// ❌ 差：覆盖已存在的回调
state.Events.OnEnd = OnEnd;
```

2. **忘记处理重复触发**
```csharp
// ❌ 差：每帧都会切换动画
state.Events.OnEnd = () => {
    _Animancer.Play(_NextClip); // 重复执行！
};
```

3. **忽略共享状态问题**
```csharp
// ❌ 差：可能覆盖其他脚本的回调
var state = _Animancer.Play(_SharedClip);
state.Events.OnEnd = MyOnEnd; // 危险！
```

---

## FAQ常见问题

### Q1: End Event为什么每帧都触发？

**A:** 这是设计特性，确保回调不会被遗漏：

```csharp
// 即使动画已经超过结束点，End Event仍会触发
state.Time = 1.5f; // 超过结束点
// OnEnd 仍然会在下一帧触发
```

### Q2: 如何避免End Event重复执行逻辑？

**A:** 使用标志位：

```csharp
bool _hasHandled = false;

state.Events.OnEnd = () => {
    if (!_hasHandled)
    {
        _hasHandled = true;
        // 只执行一次
    }
};
```

### Q3: End Event 和常规事件的区别？

**A:**

| 特性 | End Event | 常规Event |
|------|-----------|----------|
| 触发时机 | ≥ End Time | = Event Time |
| 触发频率 | 每帧 | 一次 |
| 适用场景 | 动画结束处理 | 特定时刻事件 |

### Q4: 循环动画的End Event会触发吗？

**A:** 会，每次循环结束时触发：

```csharp
state.IsLooping = true;
state.Events.OnEnd = () => {
    Debug.Log("循环结束"); // 每次循环都触发
};
```

### Q5: 如何手动设置End Time？

**A:**

```csharp
// 设置归一化时间
state.Events.NormalizedEndTime = 0.8f;

// 或设置绝对时间
state.Events.EndTime = 2.0f; // 2秒时触发
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events 主页](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Animancer Events - Behaviour](https://kybernetik.com.au/animancer/docs/manual/events/animancer/behaviour)
- [End Events Alternatives](https://kybernetik.com.au/animancer/docs/manual/events/end/alternatives)

### 🔗 API 参考
- `AnimancerEvent.Sequence.OnEnd`
- `AnimancerEvent.Sequence.NormalizedEndTime`
- `AnimancerEvent.Sequence.SharedOwner`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+（Lite 和 Pro 均支持）
