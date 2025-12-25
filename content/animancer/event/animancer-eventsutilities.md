---
title: "Animancer Events - Utilities"
date: 2025-12-25
draft: false
---

# Animancer Events - Utilities 官方文档

## 📋 目录
- [概述](#概述)
- [AnimancerEvent.Current](#animancereventcurrent)
- [三个实用工具](#三个实用工具)
- [Log Current Event](#log-current-event日志记录事件)
- [Restart Current State](#restart-current-state重启当前状态)
- [Pause At Current Event](#pause-at-current-event暂停于当前事件)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

本文档展示了利用 `AnimancerEvent.Current` 属性在事件触发时访问其详情，实现多种实用行为的代码片段。

### 🎯 核心概念

> **"AnimancerEvent.Current 属性允许在事件触发时访问事件详情"**

### 🔧 委托字段设计

> **关键设计**："方法声明为委托字段而非常规方法，避免创建垃圾回收对象"

```csharp
// ✅ 好：使用委托字段（无GC）
public static readonly Action LogEvent = () => {
    Debug.Log(AnimancerEvent.Current);
};

// ❌ 差：使用常规方法（每次调用分配GC）
public static void LogEvent()
{
    Debug.Log(AnimancerEvent.Current);
}
```

---

## AnimancerEvent.Current

### 🎯 访问当前事件

`AnimancerEvent.Current` 是一个静态属性，在事件回调执行期间可以访问当前触发的事件详情。

### 📊 可用信息

```csharp
void OnEvent()
{
    var evt = AnimancerEvent.Current;

    // 事件信息
    Debug.Log($"事件名称: {evt.name}");
    Debug.Log($"归一化时间: {evt.normalizedTime}");
    Debug.Log($"时间（秒）: {evt.time}");

    // 动画状态
    var state = evt.state;
    Debug.Log($"动画名称: {state.Clip.name}");
    Debug.Log($"动画速度: {state.Speed}");
    Debug.Log($"动画权重: {state.Weight}");

    // 事件序列
    var sequence = evt.sequence;
    Debug.Log($"事件总数: {sequence.Count}");
}
```

### ⚠️ 生命周期

```csharp
void OnEvent()
{
    // ✅ 可用：在回调函数内
    var evt = AnimancerEvent.Current;

    StartCoroutine(DelayedAccess());
}

IEnumerator DelayedAccess()
{
    yield return null;

    // ❌ 不可用：回调函数外（已过期）
    var evt = AnimancerEvent.Current; // null 或 旧值
}
```

---

## 三个实用工具

### 📋 工具概览

| 工具 | 功能 | 典型用途 |
|------|------|---------|
| **Log Current Event** | 记录事件详情 | 调试事件触发 |
| **Restart Current State** | 重启动画 | 强制循环播放 |
| **Pause At Current Event** | 暂停于事件点 | 精确控制动画流程 |

---

## Log Current Event（日志记录事件）

### 🎯 功能

记录事件触发的详细信息，方便调试和分析。

### 📝 实现代码

```csharp
using Animancer;
using UnityEngine;

public static class AnimancerEventUtilities
{
    /// <summary>
    /// 日志记录当前事件
    /// 委托字段设计避免GC分配
    /// </summary>
    public static readonly System.Action LogCurrentEvent = () =>
    {
        var evt = AnimancerEvent.Current;

        Debug.Log($"<b>Animancer Event 触发:</b>\n" +
                  $"- 事件名称: {evt.name}\n" +
                  $"- 归一化时间: {evt.normalizedTime:F3}\n" +
                  $"- 绝对时间: {evt.time:F3}s\n" +
                  $"- 动画: {evt.state.Clip.name}\n" +
                  $"- 状态: {evt.state}\n" +
                  $"- 权重: {evt.state.Weight:F2}",
                  evt.state.Graph.Component as Object);
    };
}
```

### 📚 使用方法

#### 方法1：批量添加到所有事件

```csharp
using Animancer;
using UnityEngine;

public class LogEventExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackTransition;

    void Start()
    {
        var state = _Animancer.Play(_AttackTransition);

        // 为所有事件添加日志回调
        foreach (var evt in state.Events)
        {
            evt.callback += AnimancerEventUtilities.LogCurrentEvent;
        }
    }
}
```

#### 方法2：为特定事件添加

```csharp
void Start()
{
    var state = _Animancer.Play(_AttackTransition);

    // 只为特定事件添加日志
    state.Events.Add(0.5f, AnimancerEventUtilities.LogCurrentEvent);
}
```

#### 方法3：组合其他回调

```csharp
void Start()
{
    var state = _Animancer.Play(_AttackTransition);

    state.Events.Add(0.5f, () =>
    {
        // 先记录日志
        AnimancerEventUtilities.LogCurrentEvent();

        // 再执行业务逻辑
        OnAttackHit();
    });
}

void OnAttackHit()
{
    Debug.Log("执行攻击判定");
}
```

### 🎯 Console高亮

日志中的对象引用可以在Console中直接点击高亮相关GameObject：

```csharp
Debug.Log("事件触发", evt.state.Graph.Component as Object);
//                    ↑ 点击可在Hierarchy中高亮
```

---

## Restart Current State（重启当前状态）

### 🎯 功能

将动画时间重置为0，强制重新开始播放。

### 📝 实现代码

```csharp
public static class AnimancerEventUtilities
{
    /// <summary>
    /// 重启当前动画状态
    /// 将时间重置为0
    /// </summary>
    public static readonly System.Action RestartCurrentState = () =>
    {
        var state = AnimancerEvent.Current.State;
        state.Time = 0;
        Debug.Log($"重启动画: {state.Clip.name}");
    };
}
```

### 📚 使用场景

#### 场景1：强制循环播放非循环动画

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 强制循环播放非循环动画
/// </summary>
public class ForceLoopExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip; // 非循环动画

    void Start()
    {
        var state = _Animancer.Play(_AttackClip);
        state.IsLooping = false;

        // 在结束事件中重启动画，实现手动循环
        state.Events.OnEnd = AnimancerEventUtilities.RestartCurrentState;

        Debug.Log("非循环动画将无限循环播放");
    }
}
```

#### 场景2：条件性重播

```csharp
public class ConditionalRestartExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _ChargeClip;

    private bool _isCharging = false;

    void Start()
    {
        var state = _Animancer.Play(_ChargeClip);
        state.IsLooping = false;

        // 如果还在蓄力，就重启动画
        state.Events.OnEnd = () =>
        {
            if (_isCharging)
            {
                AnimancerEventUtilities.RestartCurrentState();
            }
            else
            {
                _Animancer.Play(_IdleClip);
            }
        };
    }

    void Update()
    {
        // 按住按钮持续蓄力
        _isCharging = Input.GetKey(KeyCode.Space);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

---

## Pause At Current Event（暂停于当前事件）

### 🎯 功能

在特定事件处暂停动画播放，保持在事件的归一化时间。

### 🔑 关键特性

> **"停止播放但保持在事件的归一化时间"**
>
> **"无需将动画分割为多个片段"**
>
> **"支持按事件名称精准触发"**

### 📝 实现代码

```csharp
public static class AnimancerEventUtilities
{
    /// <summary>
    /// 暂停于当前事件
    /// </summary>
    public static readonly System.Action PauseAtCurrentEvent = () =>
    {
        var evt = AnimancerEvent.Current;
        var state = evt.State;

        // 设置时间为事件时间
        state.Time = evt.time;

        // 暂停播放
        state.IsPlaying = false;

        Debug.Log($"暂停于事件: {evt.name} @ {evt.normalizedTime:P0}");
    };

    /// <summary>
    /// 按事件名称暂停
    /// </summary>
    public static System.Action PauseAtEvent(string eventName)
    {
        return () =>
        {
            var evt = AnimancerEvent.Current;

            if (evt.name == eventName)
            {
                PauseAtCurrentEvent();
            }
        };
    }
}
```

### 📚 使用场景

#### 场景1：分段播放动画

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 分段播放动画示例
/// 在特定点暂停，等待输入后继续
/// </summary>
public class PausedAnimationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _ComboTransition;

    private AnimancerState _currentState;

    void Start()
    {
        _currentState = _Animancer.Play(_ComboTransition);

        // 在"ComboWindow"事件处暂停
        _currentState.Events.Add("ComboWindow",
            AnimancerEventUtilities.PauseAtEvent("ComboWindow"));
    }

    void Update()
    {
        // 按下按键继续播放
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            if (!_currentState.IsPlaying)
            {
                Debug.Log("继续播放动画");
                _currentState.IsPlaying = true;
            }
        }
    }
}
```

#### 场景2：QTE系统

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// QTE（Quick Time Event）系统
/// 在特定点暂停，等待玩家输入
/// </summary>
public class QTESystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _FinisherTransition;
    [SerializeField] private Text _QTEPrompt;

    private AnimancerState _currentState;
    private bool _waitingForInput = false;

    void Start()
    {
        _QTEPrompt.gameObject.SetActive(false);

        _currentState = _Animancer.Play(_FinisherTransition);

        // 在QTE点暂停
        _currentState.Events.Add("QTE", OnQTEPoint);
    }

    void OnQTEPoint()
    {
        var evt = AnimancerEvent.Current;
        var state = evt.State;

        // 暂停动画
        state.Time = evt.time;
        state.IsPlaying = false;

        // 显示提示
        _QTEPrompt.text = "按下 [Space] 完成终结技！";
        _QTEPrompt.gameObject.SetActive(true);

        _waitingForInput = true;

        // 启动超时检测
        StartCoroutine(QTETimeout());
    }

    void Update()
    {
        if (_waitingForInput && Input.GetKeyDown(KeyCode.Space))
        {
            OnQTESuccess();
        }
    }

    void OnQTESuccess()
    {
        _waitingForInput = false;
        _QTEPrompt.gameObject.SetActive(false);

        Debug.Log("QTE成功！");

        // 继续播放动画
        _currentState.IsPlaying = true;

        StopAllCoroutines();
    }

    System.Collections.IEnumerator QTETimeout()
    {
        yield return new WaitForSeconds(1.5f);

        if (_waitingForInput)
        {
            _waitingForInput = false;
            _QTEPrompt.gameObject.SetActive(false);

            Debug.Log("QTE失败！");

            // 播放失败动画
            _Animancer.Play(_FailClip);
        }
    }

    [SerializeField] private AnimationClip _FailClip;
}
```

#### 场景3：教学系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 教学系统
/// 在关键步骤暂停，显示提示
/// </summary>
public class TutorialSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _TutorialAnimation;

    private string[] _tutorialTexts = {
        "步骤1: 移动角色...",
        "步骤2: 瞄准目标...",
        "步骤3: 按下攻击键..."
    };

    private int _currentStep = 0;

    void Start()
    {
        var state = _Animancer.Play(_TutorialAnimation);

        // 在多个点暂停
        state.Events.Add("Step1", () => OnTutorialStep(0));
        state.Events.Add("Step2", () => OnTutorialStep(1));
        state.Events.Add("Step3", () => OnTutorialStep(2));
    }

    void OnTutorialStep(int stepIndex)
    {
        AnimancerEventUtilities.PauseAtCurrentEvent();

        _currentStep = stepIndex;
        Debug.Log(_tutorialTexts[stepIndex]);

        // 显示UI提示
        ShowTutorialPrompt(_tutorialTexts[stepIndex]);
    }

    void Update()
    {
        // 按任意键继续
        if (Input.anyKeyDown)
        {
            ContinueTutorial();
        }
    }

    void ContinueTutorial()
    {
        var state = _Animancer.States.Current;

        if (state != null && !state.IsPlaying)
        {
            Debug.Log("继续教学...");
            state.IsPlaying = true;
            HideTutorialPrompt();
        }
    }

    void ShowTutorialPrompt(string text) { /* UI逻辑 */ }
    void HideTutorialPrompt() { /* UI逻辑 */ }
}
```

---

## 代码示例

### 示例1：整合三个工具

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 整合所有事件工具的完整示例
/// </summary>
public class EventUtilitiesIntegration : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _ComboAttack;

    void Awake()
    {
        var state = _Animancer.Play(_ComboAttack);

        // 1. 为所有事件添加日志
        foreach (var evt in state.Events)
        {
            evt.callback += AnimancerEventUtilities.LogCurrentEvent;
        }

        // 2. 在连击窗口暂停
        state.Events.Add("ComboWindow",
            AnimancerEventUtilities.PauseAtEvent("ComboWindow"));

        // 3. 根据条件重启或结束
        state.Events.OnEnd = () =>
        {
            if (Input.GetKey(KeyCode.Mouse0))
            {
                // 玩家还在按攻击键，重启动画
                AnimancerEventUtilities.RestartCurrentState();
            }
            else
            {
                // 返回Idle
                _Animancer.Play(_IdleClip);
            }
        };
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### 示例2：自定义事件工具

```csharp
using Animancer;
using UnityEngine;

public static class CustomEventUtilities
{
    /// <summary>
    /// 减速播放当前动画
    /// </summary>
    public static readonly System.Action SlowDown = () =>
    {
        var state = AnimancerEvent.Current.State;
        state.Speed *= 0.5f;
        Debug.Log($"动画减速: {state.Speed}x");
    };

    /// <summary>
    /// 加速播放当前动画
    /// </summary>
    public static readonly System.Action SpeedUp = () =>
    {
        var state = AnimancerEvent.Current.State;
        state.Speed *= 2f;
        Debug.Log($"动画加速: {state.Speed}x");
    };

    /// <summary>
    /// 播放音效
    /// </summary>
    public static System.Action PlaySound(AudioClip clip, AudioSource source)
    {
        return () =>
        {
            if (clip != null && source != null)
            {
                source.PlayOneShot(clip);
                Debug.Log($"播放音效: {clip.name}");
            }
        };
    }

    /// <summary>
    /// 生成粒子特效
    /// </summary>
    public static System.Action SpawnParticle(ParticleSystem prefab, Transform spawnPoint)
    {
        return () =>
        {
            if (prefab != null && spawnPoint != null)
            {
                var particle = Object.Instantiate(prefab, spawnPoint.position, spawnPoint.rotation);
                particle.Play();
                Debug.Log($"生成特效: {prefab.name}");
            }
        };
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **使用委托字段避免GC**
```csharp
// ✅ 好：委托字段
public static readonly Action MyUtility = () => { };
```

2. **检查AnimancerEvent.Current的有效性**
```csharp
// ✅ 好：检查生命周期
void OnEvent()
{
    var evt = AnimancerEvent.Current;
    if (evt != null)
    {
        // 使用evt
    }
}
```

3. **组合多个工具**
```csharp
// ✅ 好：链式调用
state.Events.Add(0.5f, () => {
    AnimancerEventUtilities.LogCurrentEvent();
    OnAttackHit();
});
```

4. **为调试添加日志工具**
```csharp
// ✅ 好：开发阶段启用日志
#if UNITY_EDITOR
foreach (var evt in state.Events)
{
    evt.callback += AnimancerEventUtilities.LogCurrentEvent;
}
#endif
```

### ❌ DON'T（避免做法）

1. **不要在回调外使用AnimancerEvent.Current**
```csharp
// ❌ 差：生命周期外使用
IEnumerator DelayedUse()
{
    yield return null;
    var evt = AnimancerEvent.Current; // 无效
}
```

2. **不要使用常规方法（产生GC）**
```csharp
// ❌ 差：每次调用分配GC
public static void MyUtility() { }
```

3. **不要忘记恢复播放状态**
```csharp
// ❌ 差：暂停后忘记恢复
state.IsPlaying = false;
// 忘记在某个时机设置 state.IsPlaying = true;
```

---

## FAQ常见问题

### Q1: 为什么要使用委托字段而不是方法？

**A:** 性能优化，避免GC分配：

```csharp
// 委托字段：只分配一次
public static readonly Action LogEvent = () => { };

// 常规方法：每次创建新的委托对象
public static void LogEvent() { }

// 使用时：
state.Events.Add(0.5f, LogEvent); // 字段：无GC
state.Events.Add(0.5f, () => LogEvent()); // 方法：有GC
```

### Q2: AnimancerEvent.Current什么时候可用？

**A:** 仅在事件回调执行期间：

```
事件触发 → AnimancerEvent.Current 有效
    ↓
回调执行完毕 → AnimancerEvent.Current 无效
```

### Q3: 如何创建自己的事件工具？

**A:** 遵循委托字段模式：

```csharp
public static class MyUtilities
{
    public static readonly Action MyTool = () =>
    {
        var evt = AnimancerEvent.Current;
        // 使用evt实现功能
    };
}
```

### Q4: 暂停事件后如何恢复？

**A:** 手动设置IsPlaying：

```csharp
// 暂停
state.IsPlaying = false;

// 恢复
state.IsPlaying = true;
```

### Q5: 可以在暂停状态下修改动画吗？

**A:** 可以：

```csharp
// 暂停后可以修改
state.IsPlaying = false;
state.Time = 1.0f;  // 修改时间
state.Speed = 0.5f; // 修改速度
state.Weight = 0.5f; // 修改权重

// 然后恢复播放
state.IsPlaying = true;
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events - Behaviour](https://kybernetik.com.au/animancer/docs/manual/events/animancer/behaviour)
- [Animancer Events - Usage](https://kybernetik.com.au/animancer/docs/manual/events/animancer/usage)
- [AnimancerState API](https://kybernetik.com.au/animancer/api/Animancer/AnimancerState/)

### 🔗 API 参考
- `AnimancerEvent.Current`
- `AnimancerEvent.State`
- `AnimancerState.Time`
- `AnimancerState.IsPlaying`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
