---
title: "Animancer - End Events Alternatives"
date: 2025-12-25
draft: false
---

# Animancer - End Events Alternatives 官方文档

## 📋 目录
- [概述](#概述)
- [方案对比](#方案对比)
- [方案1：协程（Coroutines）](#方案1协程coroutines)
- [方案2：手动轮询（Manual Polling）](#方案2手动轮询manual-polling)
- [性能对比](#性能对比)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

虽然 **End Events 通常是最简单且高效的方式**，但 Animancer 还提供了两种替代方案来检测动画结束：

1. **协程（Coroutines）**：使用 `yield return` 等待动画完成
2. **手动轮询（Manual Polling）**：在 Update 中检查动画状态

---

## 方案对比

### 📊 三种方案对比表

| 特性 | End Events | Coroutines | Manual Polling |
|------|-----------|------------|----------------|
| **性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **GC分配** | 无 | 启动协程时 | 无 |
| **代码简洁** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **适用场景** | 通用 | 顺序逻辑 | 条件检测 |

### 🎯 选择建议

```csharp
// ✅ 默认使用 End Events
state.Events.OnEnd = OnComplete;

// ✅ 顺序逻辑使用 Coroutines
yield return state;
DoSomething();

// ✅ 复杂条件使用 Manual Polling
if (state.NormalizedTime >= 1 && someCondition)
{
    HandleCompletion();
}
```

---

## 方案1：协程（Coroutines）

### 🎯 核心机制

> **"可以在协程中使用 `yield return` 等待任何 AnimancerState 完成"**

**状态完成的定义：** 停止播放 **或** 超过其结束时间

### 📝 基础用法

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 协程方案基础示例
/// </summary>
public class CoroutineBasicExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;
    [SerializeField] private AnimationClip _IdleClip;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            StartCoroutine(AttackSequence());
        }
    }

    IEnumerator AttackSequence()
    {
        // 播放攻击动画
        var state = _Animancer.Play(_AttackClip);

        // 等待动画完成
        yield return state;

        // 动画完成后继续执行
        Debug.Log("攻击完成");

        // 播放Idle动画
        _Animancer.Play(_IdleClip);
    }
}
```

### 🔄 等待多个动画

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 等待多个动画示例
/// </summary>
public class WaitMultipleAnimations : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Attack1;
    [SerializeField] private AnimationClip _Attack2;
    [SerializeField] private AnimationClip _Attack3;

    void Start()
    {
        StartCoroutine(ComboSequence());
    }

    IEnumerator ComboSequence()
    {
        Debug.Log("开始连击");

        // 第一段攻击
        var state1 = _Animancer.Play(_Attack1);
        yield return state1;
        Debug.Log("第一段完成");

        // 第二段攻击
        var state2 = _Animancer.Play(_Attack2);
        yield return state2;
        Debug.Log("第二段完成");

        // 第三段攻击
        var state3 = _Animancer.Play(_Attack3);
        yield return state3;
        Debug.Log("第三段完成");

        Debug.Log("连击结束");
    }
}
```

### 🎚️ 等待 Layer 或 AnimancerComponent

> **扩展用途**：可以 yield 整个 Layer 或 AnimancerComponent 以等待所有状态完成

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 等待Layer或Component示例
/// </summary>
public class WaitLayerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Start()
    {
        StartCoroutine(WaitForAllAnimations());
    }

    IEnumerator WaitForAllAnimations()
    {
        // 播放多个动画
        _Animancer.Layers[0].Play(_Animation1);
        _Animancer.Layers[1].Play(_Animation2);
        _Animancer.Layers[2].Play(_Animation3);

        // 等待特定Layer的所有动画完成
        yield return _Animancer.Layers[0];
        Debug.Log("Layer 0 的动画完成");

        // 或等待整个AnimancerComponent的所有动画完成
        yield return _Animancer;
        Debug.Log("所有动画完成");
    }

    [SerializeField] private AnimationClip _Animation1;
    [SerializeField] private AnimationClip _Animation2;
    [SerializeField] private AnimationClip _Animation3;
}
```

### ⚠️ GC 注意事项

> **重要**：yield 状态本身不产生垃圾回收，但**启动协程会产生 GC**

```csharp
// ✅ yield状态：无GC
yield return state;

// ❌ StartCoroutine：有GC（分配协程对象）
StartCoroutine(MyCoroutine());
```

### 📊 协程完整示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 协程方案完整示例
/// 演示复杂的动画序列控制
/// </summary>
public class CoroutineCompleteExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [Header("技能动画")]
    [SerializeField] private AnimationClip _CastStart;
    [SerializeField] private AnimationClip _CastLoop;
    [SerializeField] private AnimationClip _CastEnd;
    [SerializeField] private AnimationClip _Idle;

    [Header("特效")]
    [SerializeField] private ParticleSystem _ChargeEffect;
    [SerializeField] private ParticleSystem _ReleaseEffect;

    private bool _isCharging = false;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            StartCoroutine(CastSkill());
        }
    }

    IEnumerator CastSkill()
    {
        Debug.Log("开始施法");

        // 1. 播放施法开始动画
        var startState = _Animancer.Play(_CastStart);
        yield return startState;
        Debug.Log("施法准备完成");

        // 2. 启动蓄力特效
        _ChargeEffect.Play();

        // 3. 播放循环蓄力动画
        var loopState = _Animancer.Play(_CastLoop);
        loopState.IsLooping = true;

        _isCharging = true;

        // 4. 等待2秒或玩家松开按键
        float chargeTime = 0f;
        while (_isCharging && chargeTime < 2f)
        {
            chargeTime += Time.deltaTime;
            yield return null;
        }

        Debug.Log($"蓄力时间: {chargeTime:F2}秒");

        // 5. 停止蓄力特效
        _ChargeEffect.Stop();

        // 6. 播放释放动画
        var endState = _Animancer.Play(_CastEnd);
        yield return endState;

        // 7. 触发释放特效
        _ReleaseEffect.Play();

        Debug.Log("技能释放完成");

        // 8. 返回Idle
        _Animancer.Play(_Idle);
    }

    void OnGUI()
    {
        if (_isCharging && GUI.Button(new Rect(10, 10, 100, 30), "释放技能"))
        {
            _isCharging = false;
        }
    }
}
```

---

## 方案2：手动轮询（Manual Polling）

### 🎯 核心机制

保存 `Play()` 返回的状态引用，每帧检查 `NormalizedTime` 属性。

**完成判断：** `NormalizedTime >= 1` 表示动画完成

### 📝 基础用法

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 手动轮询基础示例
/// </summary>
public class PollingBasicExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;
    [SerializeField] private AnimationClip _IdleClip;

    private AnimancerState _currentState;
    private bool _isAttacking = false;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0) && !_isAttacking)
        {
            StartAttack();
        }

        // 轮询检测动画完成
        if (_isAttacking)
        {
            CheckAttackCompletion();
        }
    }

    void StartAttack()
    {
        _isAttacking = true;
        _currentState = _Animancer.Play(_AttackClip);
        Debug.Log("开始攻击");
    }

    void CheckAttackCompletion()
    {
        // 检查归一化时间
        if (_currentState.NormalizedTime >= 1)
        {
            OnAttackComplete();
        }
    }

    void OnAttackComplete()
    {
        _isAttacking = false;
        Debug.Log("攻击完成");
        _Animancer.Play(_IdleClip);
    }
}
```

### 🛡️ 安全获取状态

使用 `TryGet()` 或 `GetOrCreate()` 避免状态未创建的错误：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 安全状态获取示例
/// </summary>
public class SafeStateAccessExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    void Update()
    {
        // 方法1：TryGet（推荐）
        if (_Animancer.States.TryGet(_AttackClip, out AnimancerState state))
        {
            if (state.NormalizedTime >= 1)
            {
                Debug.Log("攻击完成");
            }
        }

        // 方法2：GetOrCreate（确保状态存在）
        var safeState = _Animancer.States.GetOrCreate(_AttackClip);
        if (safeState.NormalizedTime >= 1)
        {
            Debug.Log("攻击完成");
        }

        // ❌ 错误：直接访问可能抛出异常
        // var dangerousState = _Animancer.States[_AttackClip]; // 状态不存在时报错
    }
}
```

### 🔍 高级条件检测

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 高级条件检测示例
/// 结合多个条件判断动画完成
/// </summary>
public class AdvancedPollingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _ChargeClip;

    private AnimancerState _chargeState;
    private bool _isCharging = false;
    private float _chargeStartTime;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            StartCharge();
        }

        if (Input.GetKeyUp(KeyCode.Space))
        {
            StopCharge();
        }

        if (_isCharging)
        {
            CheckChargeConditions();
        }
    }

    void StartCharge()
    {
        _isCharging = true;
        _chargeStartTime = Time.time;
        _chargeState = _Animancer.Play(_ChargeClip);
        _chargeState.IsLooping = true;

        Debug.Log("开始蓄力");
    }

    void CheckChargeConditions()
    {
        float chargeTime = Time.time - _chargeStartTime;

        // 条件1：动画播放超过50%
        bool animationCondition = _chargeState.NormalizedTime >= 0.5f;

        // 条件2：蓄力时间超过1秒
        bool timeCondition = chargeTime >= 1f;

        // 条件3：角色在地面上
        bool groundCondition = IsGrounded();

        // 组合条件判断
        if (animationCondition && timeCondition && groundCondition)
        {
            Debug.Log("蓄力完成，可以释放技能");
            // 显示UI提示
        }

        // 条件4：强制最大蓄力时间
        if (chargeTime >= 3f)
        {
            Debug.Log("达到最大蓄力时间");
            AutoRelease();
        }
    }

    void StopCharge()
    {
        if (_isCharging)
        {
            _isCharging = false;
            float chargeTime = Time.time - _chargeStartTime;
            Debug.Log($"释放技能（蓄力{chargeTime:F2}秒）");
            // 执行技能释放逻辑
        }
    }

    void AutoRelease()
    {
        _isCharging = false;
        Debug.Log("自动释放技能");
        // 执行技能释放逻辑
    }

    bool IsGrounded()
    {
        // 实际项目中的地面检测逻辑
        return true;
    }
}
```

### 📊 状态字典优化

> **优化方式**：通过内部字典高效获取状态

```csharp
// Animancer内部使用字典存储状态
// 查找效率: O(1)

// ✅ 高效：直接从字典获取
var state = _Animancer.States.TryGet(_Clip, out var result);

// ❌ 低效：遍历所有状态
foreach (var state in _Animancer.States)
{
    if (state.Clip == _Clip) { }
}
```

---

## 性能对比

### 📊 性能测试结果

| 方案 | CPU开销 | GC分配 | 代码行数 | 适用场景 |
|------|---------|--------|---------|---------|
| **End Events** | 最低 | 0 | 最少 | 通用推荐 |
| **Coroutines** | 低 | StartCoroutine时 | 少 | 顺序逻辑 |
| **Manual Polling** | 中 | 0 | 较多 | 复杂条件 |

### 🎯 性能优化建议

```csharp
// ✅ 最佳：End Events（零开销）
state.Events.OnEnd = OnComplete;

// ✅ 良好：Coroutines（协程复用）
private Coroutine _currentCoroutine;

void Play()
{
    if (_currentCoroutine != null)
        StopCoroutine(_currentCoroutine);

    _currentCoroutine = StartCoroutine(PlaySequence());
}

// ⚠️ 注意：Manual Polling（每帧检查）
void Update()
{
    // 只在必要时检查
    if (_needsCheck && _state.NormalizedTime >= 1)
    {
        OnComplete();
        _needsCheck = false;
    }
}
```

---

## 代码示例

### 示例1：三种方案对比

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 三种方案对比示例
/// </summary>
public class ThreeApproachesExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;
    [SerializeField] private AnimationClip _IdleClip;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            UseEndEvents();
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            StartCoroutine(UseCoroutines());
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            UseManualPolling();
        }
    }

    // 方法1：End Events（推荐）
    void UseEndEvents()
    {
        Debug.Log("[End Events] 开始攻击");
        var state = _Animancer.Play(_AttackClip);
        state.Events.OnEnd = () => {
            Debug.Log("[End Events] 攻击完成");
            _Animancer.Play(_IdleClip);
        };
    }

    // 方法2：Coroutines
    IEnumerator UseCoroutines()
    {
        Debug.Log("[Coroutines] 开始攻击");
        var state = _Animancer.Play(_AttackClip);
        yield return state;
        Debug.Log("[Coroutines] 攻击完成");
        _Animancer.Play(_IdleClip);
    }

    // 方法3：Manual Polling
    private AnimancerState _pollingState;
    private bool _isPolling = false;

    void UseManualPolling()
    {
        Debug.Log("[Manual Polling] 开始攻击");
        _pollingState = _Animancer.Play(_AttackClip);
        _isPolling = true;
    }

    void LateUpdate()
    {
        if (_isPolling && _pollingState.NormalizedTime >= 1)
        {
            Debug.Log("[Manual Polling] 攻击完成");
            _isPolling = false;
            _Animancer.Play(_IdleClip);
        }
    }
}
```

### 示例2：复杂协程序列

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 复杂协程序列示例
/// </summary>
public class ComplexCoroutineExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Start()
    {
        StartCoroutine(BossIntroSequence());
    }

    IEnumerator BossIntroSequence()
    {
        Debug.Log("=== BOSS登场序列开始 ===");

        // 1. 播放入场动画
        yield return _Animancer.Play(_BossEnter);
        Debug.Log("BOSS入场完成");

        // 2. 等待1秒
        yield return new WaitForSeconds(1f);

        // 3. 播放咆哮动画
        yield return _Animancer.Play(_BossRoar);
        Debug.Log("BOSS咆哮完成");

        // 4. 触发屏幕震动
        CameraShake();

        // 5. 等待0.5秒
        yield return new WaitForSeconds(0.5f);

        // 6. 播放战斗准备动画
        yield return _Animancer.Play(_BossBattleReady);
        Debug.Log("BOSS战斗准备完成");

        // 7. 进入Idle循环
        _Animancer.Play(_BossIdle);

        Debug.Log("=== BOSS登场序列结束，战斗开始 ===");

        // 8. 启用BOSS AI
        EnableBossAI();
    }

    void CameraShake() { Debug.Log("屏幕震动"); }
    void EnableBossAI() { Debug.Log("启用BOSS AI"); }

    [SerializeField] private AnimationClip _BossEnter;
    [SerializeField] private AnimationClip _BossRoar;
    [SerializeField] private AnimationClip _BossBattleReady;
    [SerializeField] private AnimationClip _BossIdle;
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **优先使用 End Events**
```csharp
// ✅ 默认选择
state.Events.OnEnd = OnComplete;
```

2. **顺序逻辑使用协程**
```csharp
// ✅ 适合多步骤序列
yield return state1;
yield return state2;
yield return state3;
```

3. **复杂条件使用轮询**
```csharp
// ✅ 适合多条件判断
if (state.NormalizedTime >= 1 && otherCondition)
{
    HandleCompletion();
}
```

4. **使用 TryGet 安全获取状态**
```csharp
// ✅ 避免异常
if (_Animancer.States.TryGet(_Clip, out var state))
{
    // 使用state
}
```

### ❌ DON'T（避免做法）

1. **不要过度使用协程**
```csharp
// ❌ 简单情况不要用协程
StartCoroutine(PlayAndThenIdle()); // 产生GC
```

2. **不要在轮询中做重复操作**
```csharp
// ❌ 每帧重复执行
void Update()
{
    if (state.NormalizedTime >= 1)
    {
        SomeExpensiveOperation(); // 没有标志位！
    }
}
```

3. **不要直接访问可能不存在的状态**
```csharp
// ❌ 可能抛出异常
var state = _Animancer.States[_Clip];
```

---

## FAQ常见问题

### Q1: 什么时候应该使用替代方案？

**A:**

- **End Events**: 95%的情况
- **Coroutines**: 需要顺序执行多个步骤时
- **Manual Polling**: 需要复杂条件判断时

### Q2: 协程的GC开销大吗？

**A:** 适中：

```csharp
// GC来源：
// 1. StartCoroutine() - 分配协程对象
// 2. yield return new WaitForSeconds() - 分配等待对象

// 优化：
// - 缓存WaitForSeconds对象
// - yield return state（无GC）
```

### Q3: 如何避免手动轮询的性能问题？

**A:** 使用标志位：

```csharp
private bool _needsCheck = false;

void Update()
{
    if (_needsCheck)
    {
        if (state.NormalizedTime >= 1)
        {
            OnComplete();
            _needsCheck = false; // 停止检查
        }
    }
}
```

### Q4: yield return Layer 是什么意思？

**A:** 等待该Layer的所有动画完成：

```csharp
// 等待Layer 0的所有动画
yield return _Animancer.Layers[0];

// 等待所有Layer的所有动画
yield return _Animancer;
```

### Q5: 三种方案可以混用吗？

**A:** 可以：

```csharp
IEnumerator MixedApproach()
{
    // 使用协程等待动画
    yield return _Animancer.Play(_Anim1);

    // 使用End Event处理完成
    var state = _Animancer.Play(_Anim2);
    state.Events.OnEnd = OnComplete;

    // 使用轮询检查条件
    _needsPolling = true;
}
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events - End Events](https://kybernetik.com.au/animancer/docs/manual/events/end/)
- [AnimancerState API](https://kybernetik.com.au/animancer/api/Animancer/AnimancerState/)
- [Unity Coroutines](https://docs.unity3d.com/Manual/Coroutines.html)

### 🔗 API 参考
- `AnimancerState.NormalizedTime`
- `AnimancerState.IsPlaying`
- `AnimancerComponent.States.TryGet()`
- `AnimancerComponent.States.GetOrCreate()`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
