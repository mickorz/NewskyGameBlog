# Animancer Events - Usage 官方文档

## 📋 目录
- [概述](#概述)
- [三种配置方法](#三种配置方法)
- [方法1：Transitions（Inspector配置）](#方法1transitions配置)
- [方法2：Code（代码配置）](#方法2code代码配置)
- [方法3：Hybrid（混合模式）](#方法3hybrid混合模式)
- [高级特性](#高级特性)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

Animancer Events 提供**三种主要配置方法**，每种方法都有其独特的优势和适用场景。

### 🎯 三种配置方法对比

| 方法 | 配置位置 | 回调位置 | 优点 | 适用场景 |
|------|---------|---------|------|---------|
| **Transitions** | Inspector | Inspector | 可视化预览，易调整 | 简单事件，设计师友好 |
| **Code** | 代码 | 代码 | 完全可控，易维护 | 复杂逻辑，程序员友好 |
| **Hybrid** | Inspector时间 + 代码回调 | 代码 | 兼顾可视化和灵活性 | 团队协作，最佳实践 |

---

## 三种配置方法

### 方法对比图

```
┌─────────────────────────────────────────────────────────┐
│                   Transitions 方法                       │
│  ┌──────────────┐        ┌──────────────┐              │
│  │  Inspector   │  配置  │  Inspector   │              │
│  │  (时间+回调) │ ────> │  (UnityEvent)│              │
│  └──────────────┘        └──────────────┘              │
│  优点: 可视化预览，设计师友好                           │
│  缺点: 不易维护，回调分散                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     Code 方法                            │
│  ┌──────────────┐        ┌──────────────┐              │
│  │    代码      │  配置  │    代码      │              │
│  │  (时间+回调) │ ────> │  (方法/Lambda)│             │
│  └──────────────┘        └──────────────┘              │
│  优点: 易维护，集中管理                                 │
│  缺点: 调整时间需重新编译                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Hybrid 方法 (推荐)                    │
│  ┌──────────────┐        ┌──────────────┐              │
│  │  Inspector   │  配置  │    代码      │              │
│  │   (时间)     │ ────> │  (命名回调)   │              │
│  └──────────────┘        └──────────────┘              │
│  优点: 兼顾可视化和灵活性                               │
│  缺点: 需要理解命名事件机制                             │
└─────────────────────────────────────────────────────────┘
```

---

## 方法1：Transitions配置

### 📝 核心理念

> **"Easily adjust the event times in the Inspector and using the Transition Preview Window to align them correctly with the animation's visuals."**
>
> 在 Inspector 中轻松调整事件时间，使用 Transition Preview Window 与动画视觉对齐。

### 🎨 配置步骤

#### 步骤1：创建 Transition

```csharp
[SerializeField] private ClipTransition _AttackTransition;
```

#### 步骤2：在 Inspector 中添加事件

1. 选中 Transition
2. 展开 "Events" 面板
3. **双击时间轴添加事件**
4. 设置事件时间（归一化时间 0-1）
5. 配置 UnityEvent 回调

#### 步骤3：调整事件时间（快捷键）

| 快捷键 | 功能 |
|--------|------|
| **双击时间轴** | 添加新事件 |
| **← →** | 微调时间（小步长） |
| **Shift + ← →** | 粗调时间（大步长） |
| **Space** | 四舍五入时间值 |

#### 步骤4：使用 Transition Preview Window

打开预览窗口（Window > Animancer > Transition Preview），可以：
- 实时预览动画
- 可视化查看事件标记
- 精确对齐事件与动画帧

#### 步骤5：播放动画

```csharp
_Animancer.Play(_AttackTransition); // 自动应用Inspector配置的事件
```

### 📊 完整示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Transitions方法示例
/// 所有配置在Inspector中完成
/// </summary>
public class TransitionsMethodExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 在Inspector中配置事件：
    // - Event 1: Time=0.3, Callback=OnAttackStart
    // - Event 2: Time=0.5, Callback=OnAttackHit
    // - OnEnd: Callback=OnAttackEnd
    [SerializeField] private ClipTransition _AttackTransition;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            // 播放时自动应用Inspector配置的事件
            _Animancer.Play(_AttackTransition);
        }
    }

    // 这些方法由Inspector中的UnityEvents调用
    public void OnAttackStart()
    {
        Debug.Log("攻击开始");
    }

    public void OnAttackHit()
    {
        Debug.Log("攻击命中判定");
    }

    public void OnAttackEnd()
    {
        Debug.Log("攻击结束");
        _Animancer.Play(_IdleClip);
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### ✅ 优点

- **可视化预览**：实时查看事件标记
- **易于调整**：快捷键快速微调时间
- **设计师友好**：无需编程知识
- **快速迭代**：无需重新编译

### ❌ 缺点

- **难以维护**：事件回调分散在Inspector中
- **不易重构**：修改方法名需要更新所有Inspector引用
- **难以复用**：每个Transition都需要单独配置
- **无法传参**：UnityEvent参数支持有限

---

## 方法2：Code代码配置

### 💻 核心理念

使用纯代码配置事件，提供完全的程序化控制。

### 🎯 基础模式

```csharp
AnimancerState state = _Animancer.Play(_Animation);

// 获取事件序列
if (state.Events(this, out AnimancerEvent.Sequence events))
{
    // 添加事件
    events.Add(0.4f, OnHitStart);
    events.OnEnd = EnterIdleState;
}
```

### 📚 详细步骤

#### 步骤1：播放动画获取状态

```csharp
AnimancerState state = _Animancer.Play(_AttackClip);
```

#### 步骤2：获取事件序列

```csharp
// 方法A：使用out参数
if (state.Events(this, out AnimancerEvent.Sequence events))
{
    // events可用
}

// 方法B：直接获取
var events = state.Events(this);
```

#### 步骤3：添加事件

```csharp
// 使用方法引用
events.Add(0.5f, OnAttackHit);

// 使用Lambda表达式
events.Add(0.5f, () => {
    Debug.Log("攻击命中！");
    DealDamage(50);
});

// 添加结束事件
events.OnEnd = () => {
    _Animancer.Play(_IdleClip);
};
```

### 📊 完整示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Code方法示例
/// 所有配置在代码中完成
/// </summary>
public class CodeMethodExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private WeaponCollider _Weapon;

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

        // 获取事件序列
        if (state.Events(this, out var events))
        {
            // 清除旧事件
            events.Clear();

            // 添加事件（使用方法引用）
            events.Add(0.3f, OnAttackStart);
            events.Add(0.5f, OnAttackHit);

            // 添加事件（使用Lambda）
            events.Add(0.7f, () => {
                Debug.Log("攻击后摇开始");
                _Weapon.DisableCollider();
            });

            // 结束事件
            events.OnEnd = () => {
                Debug.Log("攻击结束");
                _Animancer.Play(_IdleClip);
            };
        }
    }

    void OnAttackStart()
    {
        Debug.Log("攻击前摇");
        _Weapon.EnableCollider();
    }

    void OnAttackHit()
    {
        Debug.Log("攻击判定");
        _Weapon.CheckHit(50);
    }
}

public class WeaponCollider : MonoBehaviour
{
    public void EnableCollider() { }
    public void DisableCollider() { }
    public void CheckHit(int damage) { }
}
```

### ✅ 优点

- **易于维护**：所有逻辑集中在代码中
- **易于重构**：方法名修改自动同步
- **支持Lambda**：内联回调，无需单独方法
- **完全可控**：运行时动态修改
- **易于复用**：封装为方法即可

### ❌ 缺点

- **调整不便**：修改时间需要重新编译
- **无可视化**：难以直观查看事件分布
- **设计师不友好**：需要编程知识

---

## 方法3：Hybrid混合模式

### 🔀 核心理念

**在 Inspector 中配置事件时间，在代码中注册回调**，结合了两者的优势。

### 🎯 三种实现策略

#### 策略1：Central Events（中央事件）

为所有动画注册命名事件的回调：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 中央事件模式
/// 在一个地方注册所有命名事件的回调
/// </summary>
public class CentralEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Awake()
    {
        // 注册全局命名事件回调
        _Animancer.Events.Add("Footstep", OnFootstep);
        _Animancer.Events.Add("AttackHit", OnAttackHit);
        _Animancer.Events.Add("SpawnEffect", OnSpawnEffect);
    }

    void OnFootstep()
    {
        Debug.Log("脚步声");
    }

    void OnAttackHit()
    {
        Debug.Log("攻击命中");
    }

    void OnSpawnEffect()
    {
        Debug.Log("生成特效");
    }
}

/*
Inspector配置：
- WalkTransition: Event Name="Footstep" @ 0.3, 0.7
- AttackTransition: Event Name="AttackHit" @ 0.5
- SkillTransition: Event Name="SpawnEffect" @ 0.6
*/
```

#### 策略2：Transition Events（Transition事件）

为特定 Transition 添加命名事件回调：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Transition事件模式
/// 为特定Transition注册回调
/// </summary>
public class TransitionEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackTransition;

    void Start()
    {
        // 为Transition的命名事件注册回调
        _AttackTransition.Events.Add("WindUp", OnAttackWindUp);
        _AttackTransition.Events.Add("Hit", OnAttackHit);
        _AttackTransition.Events.OnEnd = OnAttackEnd;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            // 播放时自动触发注册的回调
            _Animancer.Play(_AttackTransition);
        }
    }

    void OnAttackWindUp()
    {
        Debug.Log("攻击前摇");
    }

    void OnAttackHit()
    {
        Debug.Log("攻击命中判定");
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击结束");
    }
}

/*
Inspector配置（在_AttackTransition中）：
- Event 1: Time=0.3, Name="WindUp"
- Event 2: Time=0.5, Name="Hit"
*/
```

#### 策略3：State Events（状态事件）

直接在动画状态上添加命名事件回调：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// State事件模式
/// 在动画状态上注册回调
/// </summary>
public class StateEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _AttackTransition;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformAttack();
        }
    }

    void PerformAttack()
    {
        var state = _Animancer.Play(_AttackTransition);

        // 为状态的命名事件注册回调
        state.Events.Add("Hit", OnAttackHit);
        state.Events.OnEnd = OnAttackEnd;
    }

    void OnAttackHit()
    {
        Debug.Log("攻击命中判定");
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击结束");
    }
}

/*
Inspector配置（在_AttackTransition中）：
- Event: Time=0.5, Name="Hit"
*/
```

### 📊 混合模式对比

| 策略 | 注册位置 | 适用场景 | 优点 | 缺点 |
|------|---------|---------|------|------|
| **Central Events** | Awake/Start | 全局通用事件 | 集中管理 | 命名冲突风险 |
| **Transition Events** | Start | 特定Transition | 模块化 | 每个Transition单独配置 |
| **State Events** | 播放时 | 动态事件 | 最灵活 | 每次播放都注册 |

### ✅ 优点

- **可视化时间调整**：在Inspector中调整
- **代码管理回调**：易于维护和重构
- **团队协作友好**：设计师调时间，程序员写逻辑
- **最佳实践**：推荐用于生产项目

### ❌ 缺点

- **需要命名约定**：事件名需要统一管理
- **学习曲线**：需要理解命名事件机制

---

## 高级特性

### 🎯 AnimancerEvent.Current

> **"AnimancerEvent.Current allows you to access event details"**
>
> 在事件回调中访问事件详细信息。

```csharp
void OnAttackHit()
{
    // 访问当前触发的事件
    var currentEvent = AnimancerEvent.Current;

    Debug.Log($"事件时间: {currentEvent.normalizedTime}");
    Debug.Log($"事件名称: {currentEvent.name}");

    // 访问触发的动画状态
    var state = currentEvent.state;
    Debug.Log($"动画名称: {state.Clip.name}");
    Debug.Log($"动画速度: {state.Speed}");
}
```

### 🔄 Shared State Events（共享状态事件）

避免多个脚本重复初始化同一动画的事件：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 共享状态事件示例
/// 多个脚本共享同一动画状态的事件
/// </summary>
public class SharedStateEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _WalkClip;

    void Start()
    {
        var state = _Animancer.States.GetOrCreate(_WalkClip);

        // 检查是否已经初始化过
        if (state.Events.Count == 0)
        {
            // 首次初始化
            state.Events.AddNormalized(0.3f, OnFootstep);
            state.Events.AddNormalized(0.7f, OnFootstep);
            Debug.Log("初始化共享事件");
        }
        else
        {
            Debug.Log("共享事件已存在，跳过初始化");
        }
    }

    void OnFootstep()
    {
        Debug.Log("脚步声");
    }
}

// 另一个脚本可以复用同一状态
public class AnotherScript : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _WalkClip;

    void Start()
    {
        var state = _Animancer.States.GetOrCreate(_WalkClip);

        // 使用已存在的事件，无需重新初始化
        _Animancer.Play(state);
    }
}
```

---

## 代码示例

### 示例1：完整的混合模式实战

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 战斗系统 - 混合模式完整示例
/// Inspector配置时间，代码注册回调
/// </summary>
public class CombatSystemHybrid : MonoBehaviour
{
    [Header("组件")]
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private WeaponController _Weapon;
    [SerializeField] private AudioSource _AudioSource;
    [SerializeField] private ParticleSystem _SlashEffect;

    [Header("动画 - Inspector中配置命名事件")]
    // Attack1: "WindUp"@0.2, "Hit"@0.5, "Recovery"@0.7
    [SerializeField] private ClipTransition _Attack1;

    // Attack2: "WindUp"@0.3, "Hit"@0.6, "Recovery"@0.8
    [SerializeField] private ClipTransition _Attack2;

    // Attack3: "WindUp"@0.25, "Hit"@0.55, "Impact"@0.6, "Recovery"@0.9
    [SerializeField] private ClipTransition _Attack3;

    [Header("音效")]
    [SerializeField] private AudioClip _SwingSound;
    [SerializeField] private AudioClip _HitSound;

    private int _comboCount = 0;

    void Start()
    {
        // 中央注册所有命名事件
        RegisterNamedEvents();
    }

    void RegisterNamedEvents()
    {
        // 为所有攻击动画注册通用回调
        _Animancer.Events.Add("WindUp", OnWindUp);
        _Animancer.Events.Add("Hit", OnHit);
        _Animancer.Events.Add("Impact", OnImpact);
        _Animancer.Events.Add("Recovery", OnRecovery);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformComboAttack();
        }
    }

    void PerformComboAttack()
    {
        _comboCount++;

        AnimancerState state = _comboCount switch
        {
            1 => _Animancer.Play(_Attack1),
            2 => _Animancer.Play(_Attack2),
            _ => _Animancer.Play(_Attack3)
        };

        // 添加结束事件
        state.Events.OnEnd = () => {
            if (_comboCount >= 3)
            {
                _comboCount = 0;
                Debug.Log("连击结束");
            }
        };
    }

    // 命名事件回调
    void OnWindUp()
    {
        Debug.Log($"攻击{_comboCount}前摇");
        _AudioSource.PlayOneShot(_SwingSound);
        _Weapon.EnableCollider();
    }

    void OnHit()
    {
        Debug.Log($"攻击{_comboCount}判定");
        int damage = _comboCount * 30; // 连击伤害递增
        _Weapon.CheckHit(damage);
        _AudioSource.PlayOneShot(_HitSound);
    }

    void OnImpact()
    {
        Debug.Log("重击冲击");
        _SlashEffect.Play();
    }

    void OnRecovery()
    {
        Debug.Log($"攻击{_comboCount}后摇");
        _Weapon.DisableCollider();
    }
}

public class WeaponController : MonoBehaviour
{
    public void EnableCollider() { }
    public void DisableCollider() { }
    public void CheckHit(int damage) { }
}
```

### 示例2：动态事件管理

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 动态事件管理示例
/// 根据游戏状态动态修改事件行为
/// </summary>
public class DynamicEventManagement : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _RunTransition;

    private bool _isSprinting = false;
    private bool _isStealthy = false;

    void Update()
    {
        // 切换冲刺模式
        if (Input.GetKeyDown(KeyCode.LeftShift))
        {
            _isSprinting = !_isSprinting;
        }

        // 切换潜行模式
        if (Input.GetKeyDown(KeyCode.LeftControl))
        {
            _isStealthy = !_isStealthy;
        }

        // 播放跑步动画
        if (Input.GetKey(KeyCode.W))
        {
            PlayRunWithDynamicEvents();
        }
    }

    void PlayRunWithDynamicEvents()
    {
        var state = _Animancer.Play(_RunTransition);

        // 清除旧事件
        state.Events.Clear();

        // 根据状态添加不同的脚步声事件
        if (_isSprinting)
        {
            // 冲刺：脚步频率更快，音量更大
            state.Events.AddNormalized(0.25f, () => PlayFootstep(1.0f));
            state.Events.AddNormalized(0.5f, () => PlayFootstep(1.0f));
            state.Events.AddNormalized(0.75f, () => PlayFootstep(1.0f));
        }
        else if (_isStealthy)
        {
            // 潜行：脚步频率更慢，音量更小
            state.Events.AddNormalized(0.3f, () => PlayFootstep(0.3f));
            state.Events.AddNormalized(0.7f, () => PlayFootstep(0.3f));
        }
        else
        {
            // 普通跑步
            state.Events.AddNormalized(0.3f, () => PlayFootstep(0.7f));
            state.Events.AddNormalized(0.7f, () => PlayFootstep(0.7f));
        }
    }

    void PlayFootstep(float volume)
    {
        Debug.Log($"脚步声 (音量: {volume})");
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **生产项目使用混合模式**
```csharp
// ✅ 好：Inspector配置时间，代码管理回调
_Animancer.Events.Add("Hit", OnHit);
```

2. **使用命名约定**
```csharp
// ✅ 好：清晰的命名规范
"WindUp", "Hit", "Recovery", "Footstep_L", "Footstep_R"
```

3. **使用 AnimancerEvent.Current 获取上下文**
```csharp
// ✅ 好：访问事件详情
void OnEvent()
{
    var evt = AnimancerEvent.Current;
    Debug.Log($"时间: {evt.normalizedTime}");
}
```

4. **检查共享状态避免重复初始化**
```csharp
// ✅ 好：避免重复添加事件
if (state.Events.Count == 0)
{
    state.Events.Add(0.5f, OnHit);
}
```

5. **清除旧事件避免累积**
```csharp
// ✅ 好：每次播放前清除
state.Events.Clear();
state.Events.Add(0.5f, NewCallback);
```

### ❌ DON'T（避免做法）

1. **不要混用多种模式**
```csharp
// ❌ 差：混乱的配置方式
// 部分在Inspector，部分在代码，难以维护
```

2. **不要使用模糊的事件名**
```csharp
// ❌ 差：不清晰的命名
"Event1", "Event2", "DoSomething"
```

3. **不要忘记清除事件**
```csharp
// ❌ 差：事件累积
void Play()
{
    var state = _Animancer.Play(_Clip);
    state.Events.Add(0.5f, OnHit); // 重复添加！
}
```

4. **不要在事件中执行耗时操作**
```csharp
// ❌ 差：阻塞主线程
void OnEvent()
{
    Thread.Sleep(100); // 卡顿！
}
```

---

## FAQ常见问题

### Q1: 三种方法应该选哪个？

**A:** 根据项目需求：

- **小型项目/原型**：Transitions 方法（快速简单）
- **中型项目**：Code 方法（易维护）
- **大型项目/团队协作**：Hybrid 方法（推荐）

### Q2: 命名事件如何工作？

**A:**
1. Inspector 中配置事件，设置 Name 字段
2. 代码中使用 `Events.Add("Name", Callback)` 注册
3. 播放动画时，匹配 Name 触发回调

### Q3: AnimancerEvent.Current 什么时候可用？

**A:** 仅在事件回调函数执行期间可用：

```csharp
void OnHit()
{
    var evt = AnimancerEvent.Current; // ✅ 可用

    StartCoroutine(DelayedAccess());
}

IEnumerator DelayedAccess()
{
    yield return null;
    var evt = AnimancerEvent.Current; // ❌ 不可用（已过期）
}
```

### Q4: 如何避免共享状态事件重复初始化？

**A:** 检查事件数量：

```csharp
var state = _Animancer.States.GetOrCreate(_Clip);

if (state.Events.Count == 0)
{
    // 首次初始化
    state.Events.Add(0.5f, OnHit);
}
```

### Q5: 可以在运行时修改 Inspector 配置的事件吗？

**A:** 可以，但会覆盖 Inspector 配置：

```csharp
var state = _Animancer.Play(_Transition);

// 清除Inspector配置的事件
state.Events.Clear();

// 添加新的事件
state.Events.Add(0.5f, NewCallback);
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events 主页](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Animancer Events - Behaviour](https://kybernetik.com.au/animancer/docs/manual/events/animancer/behaviour)
- [Animancer Events - Parameters](https://kybernetik.com.au/animancer/docs/manual/events/animancer/parameters/)
- [Transition Preview Window](https://kybernetik.com.au/animancer/docs/manual/transitions/previews/)

### 🔗 官方资源
- [Animancer Events 示例](https://kybernetik.com.au/animancer/docs/samples/)
- [API 文档](https://kybernetik.com.au/animancer/api/)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+（需要 Pro 版本）
