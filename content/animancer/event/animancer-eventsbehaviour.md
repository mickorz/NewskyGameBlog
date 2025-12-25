---
title: "Animancer Events - Behaviour"
date: 2025-12-25
draft: false
---

# Animancer Events - Behaviour 官方文档

## 📋 目录
- [概述](#概述)
- [核心行为机制](#核心行为机制)
- [循环动画中的事件](#循环动画中的事件)
- [End Events行为](#end-events行为)
- [高级特性](#高级特性)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

本文档详细解释 Animancer Events 的工作原理和触发机制，特别是在不同动画状态（循环/非循环）下的行为差异。

---

## 核心行为机制

### 🎯 触发时机

事件触发取决于动画类型：

| 动画类型 | 触发行为 |
|---------|---------|
| **非循环动画** | "Once on the frame when the animation passes the specified time"<br>动画通过指定时间点时触发**一次** |
| **循环动画** | "Every loop on the frame when the animation passes the specified time"<br>**每次循环**通过指定时间点时都触发 |

### 📊 触发机制图解

#### 非循环动画

```
时间轴: 0 ───────────→ 0.5 ───────────→ 1.0 (结束)
               ↑ 事件触发 1次

动画播放: ▬▬▬▬▬▬▬▬→ ⚡ ▬▬▬▬▬▬▬▬→ ⏹️
```

#### 循环动画

```
循环1: 0 → 0.5 → 1.0 → (重新开始)
          ↑ 事件触发

循环2: 0 → 0.5 → 1.0 → (重新开始)
          ↑ 事件再次触发

循环3: 0 → 0.5 → 1.0 → (重新开始)
          ↑ 事件再次触发

动画播放: 🔄▬▬→ ⚡ ▬▬→ 🔄▬▬→ ⚡ ▬▬→ 🔄▬▬→ ⚡ ▬▬→
```

---

## 循环动画中的事件

### 🔗 归一化时间约束

> **重要约束**：循环动画中的事件必须满足 `0 <= normalizedTime < 1`

```csharp
// ✅ 有效的归一化时间
state.Events.AddNormalized(0.0f, Callback);  // 循环开始
state.Events.AddNormalized(0.5f, Callback);  // 循环中间
state.Events.AddNormalized(0.99f, Callback); // 接近结束

// ❌ 无效的归一化时间（抛出 ArgumentOutOfRangeException）
state.Events.AddNormalized(1.0f, Callback);  // 超出范围
state.Events.AddNormalized(1.5f, Callback);  // 超出范围
```

### ⚠️ 异常处理

```csharp
// 超出范围会在更新时抛出异常
try
{
    state.Events.AddNormalized(1.0f, MyCallback);
}
catch (ArgumentOutOfRangeException ex)
{
    Debug.LogError($"事件时间超出循环范围: {ex.Message}");
}
```

### 🎯 AlmostOne 常量

对于需要在循环结束时触发的事件，使用 `AnimancerEvent.AlmostOne`：

```csharp
// 使用AlmostOne表示接近1但小于1的最大float值
state.Events.AddNormalized(AnimancerEvent.AlmostOne, OnLoopEnd);

// 等效于
state.Events.AddNormalized(0.999999f, OnLoopEnd);
```

### 🔄 快速循环行为

> **特性**：如果动画在一帧内播放多个循环，事件会按比例触发。

```csharp
// 示例：动画速度非常快，1帧播放3次循环
state.Speed = 100f;

// 如果在0.5处有事件
state.Events.AddNormalized(0.5f, OnMidLoop);

// 那么该帧会触发3次OnMidLoop回调！
```

---

## End Events行为

### 🎯 End Events 特殊机制

> **"End Events trigger on every frame when the animation has passed the specified time"**
>
> End Events 在动画通过指定时间后的**每一帧**都触发，独立于循环状态。

### 📊 End Events vs 普通Events

| 特性 | 普通Events | End Events |
|------|-----------|------------|
| **触发次数** | 通过时间点时触发一次 | 通过后每帧都触发 |
| **循环依赖** | 受循环影响 | 不受循环影响 |
| **典型用途** | 特定时刻的事件 | 动画结束后的持续检测 |

### 📝 End Events 示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// End Events 行为示例
/// </summary>
public class EndEventsBehaviourExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    void Start()
    {
        var state = _Animancer.Play(_AttackClip);
        state.IsLooping = false;

        // OnEnd 会在动画结束后的每一帧调用
        state.Events.OnEnd = OnAttackEnd;
    }

    int _endCallCount = 0;

    void OnAttackEnd()
    {
        _endCallCount++;
        Debug.Log($"OnEnd触发第 {_endCallCount} 次");

        // 通常在第一次触发时切换动画
        if (_endCallCount == 1)
        {
            _Animancer.Play(_IdleClip);
        }
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

---

## 高级特性

### ⏱️ 时间修改（Time Modification）

> **重要**：修改 `AnimancerState.Time` 会阻止该帧的后续事件触发。

```csharp
void OnEventA()
{
    var state = AnimancerEvent.Current.State;

    // 直接修改Time会跳过中间的事件
    state.Time = 2.0f; // 阻止该帧其他事件触发
}
```

### 🎯 MoveTime 方法

使用 `MoveTime` 方法触发中间事件：

```csharp
void OnEventA()
{
    var state = AnimancerEvent.Current.State;

    // MoveTime 会触发中间的所有事件
    state.MoveTime(2.0f, true); // ✅ 触发中间事件
}
```

### 🚫 事件序列修改限制

> **约束**：事件序列不能被自己的回调修改。

```csharp
void OnEvent()
{
    var state = AnimancerEvent.Current.State;

    // ❌ 错误：不能在回调中修改事件序列
    // state.Events.Add(0.8f, AnotherCallback); // 会抛出异常

    // ✅ 正确：延迟到下一帧修改
    UnityEngine.Coroutines.StartCoroutine(ModifyEventsNextFrame(state));
}

IEnumerator ModifyEventsNextFrame(AnimancerState state)
{
    yield return null;
    state.Events.Add(0.8f, AnotherCallback); // ✅ 安全
}
```

### 🎚️ Mixer 上的事件

事件可以附加到 Mixer 或其子动画：

```csharp
// 附加到Mixer：根据加权平均时间触发
mixerState.Events.Add(0.5f, OnMixerEvent);

// 附加到子动画：根据子动画自身时间触发
mixerState.GetChild(0).Events.Add(0.5f, OnChildEvent);
```

### 🎮 Controller State 兼容性

> **限制**：事件技术上支持 Controller States，但在检测内部 Animator 行为方面有限制。

```csharp
// Controller State 的事件支持有限
var controllerState = _Animancer.Play(animatorController);
controllerState.Events.Add(0.5f, Callback); // 可能不可靠
```

### 🔄 IUpdatable 接口替代方案

对于自定义动画驱动逻辑，推荐实现 `IUpdatable` 接口：

```csharp
public class CustomAnimationLogic : MonoBehaviour, IUpdatable
{
    public void Update()
    {
        // 自定义更新逻辑
        CheckCustomConditions();
    }

    void CheckCustomConditions()
    {
        // 根据动画状态执行逻辑
    }
}
```

---

## 代码示例

### 示例1：循环 vs 非循环事件

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 循环和非循环事件对比示例
/// </summary>
public class LoopingBehaviourExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _AttackClip;

    void Start()
    {
        TestLoopingAnimation();
        TestNonLoopingAnimation();
    }

    void TestLoopingAnimation()
    {
        var walkState = _Animancer.Play(_WalkClip);
        walkState.IsLooping = true;

        // 事件会在每次循环时触发
        walkState.Events.AddNormalized(0.3f, () => {
            Debug.Log($"[循环] 左脚触地 @ 时间={walkState.Time}");
        });

        walkState.Events.AddNormalized(0.7f, () => {
            Debug.Log($"[循环] 右脚触地 @ 时间={walkState.Time}");
        });

        // 使用AlmostOne在循环结束时触发
        walkState.Events.AddNormalized(AnimancerEvent.AlmostOne, () => {
            Debug.Log($"[循环] 循环结束 @ 时间={walkState.Time}");
        });
    }

    void TestNonLoopingAnimation()
    {
        var attackState = _Animancer.Play(_AttackClip);
        attackState.IsLooping = false;

        // 事件只触发一次
        attackState.Events.AddNormalized(0.5f, () => {
            Debug.Log($"[非循环] 攻击判定 @ 时间={attackState.Time}");
        });

        // End Event 在动画结束后每帧触发
        attackState.Events.OnEnd = () => {
            Debug.Log("[非循环] 动画结束 (每帧触发)");

            // 通常在第一次触发时切换动画
            if (!_hasTransitioned)
            {
                _Animancer.Play(_WalkClip);
                _hasTransitioned = true;
            }
        };
    }

    private bool _hasTransitioned = false;
}
```

### 示例2：快速循环事件触发

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 快速循环事件触发示例
/// 演示高速播放时事件的多次触发
/// </summary>
public class FastLoopingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _SpinClip;

    void Start()
    {
        var state = _Animancer.Play(_SpinClip);
        state.IsLooping = true;

        // 正常速度
        state.Speed = 1f;

        // 在中点添加事件
        int triggerCount = 0;
        state.Events.AddNormalized(0.5f, () => {
            triggerCount++;
            Debug.Log($"事件触发 #{triggerCount}");
        });

        // 2秒后加速
        StartCoroutine(SpeedUpAfterDelay());
    }

    System.Collections.IEnumerator SpeedUpAfterDelay()
    {
        yield return new WaitForSeconds(2f);

        Debug.Log("加速到10倍速度！");
        var state = _Animancer.States.Current;
        state.Speed = 10f;

        // 现在事件会在单帧内多次触发
        yield return new WaitForSeconds(2f);

        Debug.Log("加速到100倍速度！");
        state.Speed = 100f;

        // 可能在一帧内触发多次
    }
}
```

### 示例3：Time vs MoveTime

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Time vs MoveTime 对比示例
/// 演示两种时间修改方式的区别
/// </summary>
public class TimeMoveTimeExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _TestClip;

    void Start()
    {
        TestDirectTimeModification();
        TestMoveTimeMethod();
    }

    void TestDirectTimeModification()
    {
        var state = _Animancer.Play(_TestClip);

        // 添加多个事件
        state.Events.Add(0.5f, OnEvent1);
        state.Events.Add(1.0f, OnEvent2);
        state.Events.Add(1.5f, OnEvent3);
        state.Events.Add(2.0f, OnEvent4);

        // 在Event1中直接修改Time
        void OnEvent1()
        {
            Debug.Log("Event1触发");

            // 直接跳到2.0s，跳过Event2和Event3
            state.Time = 2.0f;

            Debug.Log("跳到2.0s，Event2和Event3被跳过");
        }
    }

    void TestMoveTimeMethod()
    {
        var state = _Animancer.Play(_TestClip);

        state.Events.Add(0.5f, OnEventA);
        state.Events.Add(1.0f, OnEventB);
        state.Events.Add(1.5f, OnEventC);
        state.Events.Add(2.0f, OnEventD);

        void OnEventA()
        {
            Debug.Log("EventA触发");

            // 使用MoveTime移动到2.0s，触发中间事件
            state.MoveTime(2.0f, fireEvents: true);

            Debug.Log("移动到2.0s，EventB和EventC也被触发");
        }
    }

    void OnEvent2() => Debug.Log("Event2触发");
    void OnEvent3() => Debug.Log("Event3触发");
    void OnEvent4() => Debug.Log("Event4触发");

    void OnEventB() => Debug.Log("EventB触发");
    void OnEventC() => Debug.Log("EventC触发");
    void OnEventD() => Debug.Log("EventD触发");
}
```

### 示例4：Mixer上的事件

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Mixer事件示例
/// 演示在Mixer和子动画上附加事件的区别
/// </summary>
public class MixerEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;
    [SerializeField] private AnimationClip _RunClip;

    void Start()
    {
        // 创建Mixer
        var mixer = new LinearMixerState(_Animancer.Graph)
        {
            { _IdleClip, 0.0f },
            { _WalkClip, 0.5f },
            { _RunClip, 1.0f }
        };

        _Animancer.Play(mixer);

        // 在Mixer上添加事件：根据加权平均时间触发
        mixer.Events.AddNormalized(0.5f, () => {
            Debug.Log($"Mixer事件触发 @ 加权平均时间50%");
        });

        // 在子动画上添加事件：根据子动画自身时间触发
        mixer.GetChild(1).Events.AddNormalized(0.5f, () => {
            Debug.Log("Walk子动画事件触发 @ Walk时间50%");
        });

        mixer.GetChild(2).Events.AddNormalized(0.5f, () => {
            Debug.Log("Run子动画事件触发 @ Run时间50%");
        });

        // 调整Mixer参数
        mixer.Parameter = 0.5f; // Walk
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **循环动画使用合法范围**
```csharp
// ✅ 好：归一化时间在[0, 1)范围内
state.Events.AddNormalized(0.5f, Callback);
state.Events.AddNormalized(AnimancerEvent.AlmostOne, OnLoopEnd);
```

2. **End Event 中检查是否首次触发**
```csharp
// ✅ 好：避免重复处理
bool _hasEnded = false;
state.Events.OnEnd = () => {
    if (!_hasEnded)
    {
        _hasEnded = true;
        HandleAnimationEnd();
    }
};
```

3. **使用 MoveTime 触发中间事件**
```csharp
// ✅ 好：使用MoveTime
state.MoveTime(targetTime, fireEvents: true);
```

4. **延迟修改事件序列**
```csharp
// ✅ 好：下一帧修改
StartCoroutine(ModifyEventsNextFrame());
```

### ❌ DON'T（避免做法）

1. **循环动画使用 1.0 或更大的归一化时间**
```csharp
// ❌ 差：超出范围
state.Events.AddNormalized(1.0f, Callback); // 抛出异常
```

2. **忘记处理 End Event 的重复触发**
```csharp
// ❌ 差：每帧都会切换动画
state.Events.OnEnd = () => {
    _Animancer.Play(_NextClip); // 重复执行！
};
```

3. **直接修改 Time 期望触发中间事件**
```csharp
// ❌ 差：中间事件不会触发
state.Time = 2.0f; // 跳过中间事件
```

4. **在事件回调中修改事件序列**
```csharp
// ❌ 差：抛出异常
void OnEvent()
{
    state.Events.Add(0.8f, AnotherCallback); // 错误！
}
```

---

## FAQ常见问题

### Q1: 为什么循环动画不能使用 1.0 作为归一化时间？

**A:** 循环动画的时间范围是 `[0, 1)`（左闭右开区间），1.0 表示下一次循环的开始（等同于 0.0）。如果允许 1.0，会导致歧义。使用 `AnimancerEvent.AlmostOne` 代替。

### Q2: End Event 为什么每帧都触发？

**A:** End Event 的设计目的是检测"动画是否已结束"的状态，而不是"动画刚刚结束"的事件。因此只要动画时间 >= End Time，每帧都会触发。

**解决方案：**
```csharp
bool _hasHandledEnd = false;
state.Events.OnEnd = () => {
    if (!_hasHandledEnd)
    {
        _hasHandledEnd = true;
        // 只执行一次
    }
};
```

### Q3: 如何在事件中跳转到另一个时间点？

**A:** 根据需求选择：

```csharp
// 方法1：跳过中间事件
state.Time = 2.0f;

// 方法2：触发中间事件
state.MoveTime(2.0f, fireEvents: true);
```

### Q4: 快速播放时事件触发多次怎么办？

**A:** 这是正常行为。如果只想触发一次，使用标志位：

```csharp
bool _hasTriggered = false;

state.Events.AddNormalized(0.5f, () => {
    if (!_hasTriggered)
    {
        _hasTriggered = true;
        HandleEvent();
    }
});
```

### Q5: 可以在事件回调中添加新事件吗？

**A:** 不能直接添加，需要延迟到下一帧：

```csharp
void OnEvent()
{
    StartCoroutine(AddEventNextFrame());
}

IEnumerator AddEventNextFrame()
{
    yield return null;
    state.Events.Add(0.8f, NewCallback);
}
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events 主页](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Animancer Events - Usage](https://kybernetik.com.au/animancer/docs/manual/events/animancer/usage)
- [End Events](https://kybernetik.com.au/animancer/docs/manual/events/end/)

### 🔗 API 参考
- `AnimancerEvent.AlmostOne`
- `AnimancerState.MoveTime()`
- `AnimancerState.Time`
- `IUpdatable` 接口

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
