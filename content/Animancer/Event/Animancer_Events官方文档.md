# Animancer Events 官方文档

## 📋 目录
- [概述](#概述)
- [两种事件系统对比](#两种事件系统对比)
- [核心概念](#核心概念)
- [基础使用方法](#基础使用方法)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

**Animancer Events** 是一个强大的事件系统，允许你在动画播放过程中的**特定时刻触发回调函数**。

### 🎯 典型应用场景

| 场景 | 说明 | 事件触发时机 |
|------|------|--------------|
| **高尔夫挥杆** | 击打球的精确时刻 | 挥杆到达最低点时 |
| **脚步声** | 行走时播放脚步音效 | 脚触地时刻 |
| **攻击检测** | 武器伤害判定 | 武器挥舞到攻击范围时 |
| **特效触发** | 播放视觉特效 | 动画关键帧时刻 |
| **动画切换** | 连击系统、动画序列 | 当前动画结束时 |

---

## 两种事件系统对比

Animancer 支持**两种事件系统**，各有优缺点：

### 📊 对比表

| 特性 | Animation Events<br>(Unity内置) | Animancer Events<br>(自定义系统) |
|------|--------------------------------|--------------------------------|
| **定义位置** | AnimationClip内部 | 独立于AnimationClip |
| **灵活性** | 所有使用该clip的状态共享事件 | 同一动画可使用不同事件集 |
| **回调位置** | 必须在同一GameObject的MonoBehaviour | 可从任何位置注册 |
| **性能** | 效率较低，可能产生GC | 使用C#委托，性能更优 |
| **配置方式** | 仅在AnimationClip中配置 | 检查器+代码 |
| **运行时修改** | 不支持 | 支持动态添加 |
| **兼容性** | 与Unity Animator完全相同 | Animancer专属 |

### ✅ Animation Events（Unity内置）

```csharp
// Animation Events 需要在同一GameObject的MonoBehaviour中定义方法
public class CharacterController : MonoBehaviour
{
    // 这个方法名必须与AnimationClip中的Event Name完全一致
    public void PlayFootstepSound()
    {
        Debug.Log("脚步声触发");
    }

    // Animation Events可以接收参数
    public void OnAttackHit(int damage)
    {
        Debug.Log($"攻击伤害: {damage}");
    }
}
```

**优点：**
- Unity原生支持，与Animator完全兼容
- 在Animation窗口中可视化编辑
- 无需额外学习成本

**缺点：**
- 必须在同一GameObject上
- 所有使用该clip的地方共享相同事件
- 运行时无法修改
- 性能开销较大

### ✅ Animancer Events（推荐）

```csharp
public class CharacterController : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _WalkTransition;

    void Start()
    {
        // 可以从任何位置注册回调
        var state = _Animancer.Play(_WalkTransition);

        // 添加事件（使用时间）
        state.Events(this).Add(0.3f, PlayFootstep);
        state.Events(this).Add(0.7f, PlayFootstep);

        // 添加结束事件
        state.Events(this).OnEnd = OnWalkEnd;
    }

    void PlayFootstep()
    {
        Debug.Log("脚步声");
    }

    void OnWalkEnd()
    {
        Debug.Log("行走动画结束");
    }
}
```

**优点：**
- 完全灵活的回调注册位置
- 同一动画可以有不同事件配置
- 支持运行时动态添加/移除
- 性能优异（C#委托）
- 支持Lambda表达式

**缺点：**
- Animancer专属API
- 需要学习新的事件系统

---

## 核心概念

### 🎬 事件时间表示方式

Animancer Events 支持**两种时间表示**：

```csharp
// 1. 绝对时间（秒）
state.Events(this).Add(1.5f, MyCallback); // 在1.5秒时触发

// 2. 归一化时间（0-1）
state.Events(this).AddNormalized(0.5f, MyCallback); // 在动画50%时触发
```

### 📦 事件序列结构

```
AnimancerState
    └── AnimancerEvent.Sequence（事件序列）
            ├── Event 1（时间: 0.3s, 回调: PlayFootstep）
            ├── Event 2（时间: 0.7s, 回调: PlayFootstep）
            └── End Event（时间: NormalizedEndTime, 回调: OnAnimationEnd）
```

### 🔄 事件触发逻辑
git remote add origin https://github.com/mickorz/NewskyGameBlog.git
```
播放动画 → 时间推进 → 检查事件 → 触发回调 → 继续播放
     ↓
  时间 >= 事件时间？
     ├─ 是 → 调用事件回调
     └─ 否 → 跳过
```

---

## 基础使用方法

### 方法1：Inspector配置（推荐新手）

**步骤：**

1. **创建 Transition**
```csharp
[SerializeField] private ClipTransition _AttackTransition;
```

2. **在Inspector中配置事件**
   - 选中Transition
   - 展开 "Events" 面板
   - 点击 "+" 添加事件
   - 设置时间和回调

3. **设置回调**
```csharp
void Start()
{
    // 自动应用Inspector中配置的事件
    _Animancer.Play(_AttackTransition);
}
```

### 方法2：代码配置（推荐高级用户）

```csharp
public class WeaponController : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AttackClip;

    void PerformAttack()
    {
        var state = _Animancer.Play(_AttackClip);

        // 添加攻击检测事件（归一化时间）
        state.Events(this).AddNormalized(0.6f, CheckHit);

        // 添加结束事件
        state.Events(this).OnEnd = OnAttackEnd;
    }

    void CheckHit()
    {
        Debug.Log("检测攻击命中");
        // 执行伤害判定逻辑
    }

    void OnAttackEnd()
    {
        Debug.Log("攻击动画结束，返回Idle");
        _Animancer.Play(_IdleClip);
    }
}
```

---

## 代码示例

### 示例1：脚步声系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 脚步声系统示例
/// 在行走/跑步动画中播放脚步音效
/// </summary>
public class FootstepSoundSystem : MonoBehaviour
{
    [Header("组件引用")]
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AudioSource _AudioSource;

    [Header("动画配置")]
    [SerializeField] private ClipTransition _WalkTransition;
    [SerializeField] private ClipTransition _RunTransition;

    [Header("音效配置")]
    [SerializeField] private AudioClip[] _FootstepSounds;

    void Update()
    {
        float speed = Input.GetAxis("Vertical");

        if (speed > 0.5f)
        {
            PlayRunWithFootsteps();
        }
        else if (speed > 0.1f)
        {
            PlayWalkWithFootsteps();
        }
    }

    void PlayWalkWithFootsteps()
    {
        var state = _Animancer.Play(_WalkTransition);

        // 清除之前的事件
        state.Events(this).Clear();

        // 行走动画通常有2个脚步点
        state.Events(this).AddNormalized(0.2f, PlayFootstepSound); // 左脚
        state.Events(this).AddNormalized(0.7f, PlayFootstepSound); // 右脚
    }

    void PlayRunWithFootsteps()
    {
        var state = _Animancer.Play(_RunTransition);

        state.Events(this).Clear();

        // 跑步动画脚步更快
        state.Events(this).AddNormalized(0.25f, PlayFootstepSound);
        state.Events(this).AddNormalized(0.75f, PlayFootstepSound);
    }

    void PlayFootstepSound()
    {
        if (_FootstepSounds.Length == 0) return;

        // 随机播放一个脚步声
        var clip = _FootstepSounds[Random.Range(0, _FootstepSounds.Length)];
        _AudioSource.PlayOneShot(clip);
    }
}
```

### 示例2：攻击连击系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 攻击连击系统
/// 使用Animancer Events实现连击窗口检测
/// </summary>
public class ComboAttackSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [SerializeField] private ClipTransition _Attack1;
    [SerializeField] private ClipTransition _Attack2;
    [SerializeField] private ClipTransition _Attack3;
    [SerializeField] private ClipTransition _Idle;

    private int _currentCombo = 0;
    private bool _canCombo = false;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            if (_currentCombo == 0 || _canCombo)
            {
                PerformNextAttack();
            }
        }
    }

    void PerformNextAttack()
    {
        _currentCombo++;
        _canCombo = false;

        AnimancerState state = null;

        switch (_currentCombo)
        {
            case 1:
                state = _Animancer.Play(_Attack1);
                break;
            case 2:
                state = _Animancer.Play(_Attack2);
                break;
            case 3:
                state = _Animancer.Play(_Attack3);
                break;
        }

        if (state != null)
        {
            // 连击窗口：在动画60%-90%之间可以进行下一次攻击
            state.Events(this).AddNormalized(0.6f, OpenComboWindow);
            state.Events(this).AddNormalized(0.9f, CloseComboWindow);

            // 攻击判定点：在动画50%时检测命中
            state.Events(this).AddNormalized(0.5f, CheckHit);

            // 结束事件
            state.Events(this).OnEnd = OnAttackEnd;
        }
    }

    void OpenComboWindow()
    {
        _canCombo = true;
        Debug.Log("连击窗口打开");
    }

    void CloseComboWindow()
    {
        _canCombo = false;
        Debug.Log("连击窗口关闭");
    }

    void CheckHit()
    {
        Debug.Log($"执行攻击 {_currentCombo} 的伤害判定");
        // 实际项目中这里执行碰撞检测、伤害计算等
    }

    void OnAttackEnd()
    {
        if (!_canCombo || _currentCombo >= 3)
        {
            // 连击结束，返回Idle
            _currentCombo = 0;
            _Animancer.Play(_Idle);
            Debug.Log("连击结束");
        }
    }
}
```

### 示例3：技能特效触发

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 技能特效系统
/// 在技能动画的关键帧触发粒子特效
/// </summary>
public class SkillEffectSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _FireballSkill;
    [SerializeField] private ClipTransition _IceSpellSkill;

    [SerializeField] private ParticleSystem _FireballEffect;
    [SerializeField] private ParticleSystem _IceEffect;
    [SerializeField] private Transform _CastPoint;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            CastFireball();
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            CastIceSpell();
        }
    }

    void CastFireball()
    {
        var state = _Animancer.Play(_FireballSkill);

        // 事件序列：准备 → 施法 → 发射
        state.Events(this).Clear();

        // 0.3s: 手部开始聚集火焰
        state.Events(this).Add(0.3f, () => {
            Debug.Log("开始聚集火焰能量");
            // 播放聚集特效
        });

        // 0.8s: 发射火球
        state.Events(this).Add(0.8f, () => {
            Debug.Log("发射火球！");
            Instantiate(_FireballEffect, _CastPoint.position, _CastPoint.rotation);
        });

        // 结束事件
        state.Events(this).OnEnd = () => {
            Debug.Log("施法完成");
            _Animancer.Play(_IdleClip);
        };
    }

    void CastIceSpell()
    {
        var state = _Animancer.Play(_IceSpellSkill);

        state.Events(this).Clear();

        // 使用归一化时间（更稳定）
        state.Events(this).AddNormalized(0.5f, () => {
            Debug.Log("冰霜爆发！");
            _IceEffect.transform.position = transform.position;
            _IceEffect.Play();
        });

        state.Events(this).OnEnd = () => {
            _Animancer.Play(_IdleClip);
        };
    }

    [SerializeField] private AnimationClip _IdleClip;
}
```

### 示例4：事件参数传递

```csharp
using Animancer;
using UnityEngine;
using System;

/// <summary>
/// 事件参数传递示例
/// 演示如何在事件中传递数据
/// </summary>
public class EventParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _Attack;

    void PerformAttack(int damage, string attackType)
    {
        var state = _Animancer.Play(_Attack);

        // 方法1：使用Lambda捕获变量
        state.Events(this).AddNormalized(0.5f, () => {
            OnAttackHit(damage, attackType);
        });

        // 方法2：使用闭包
        float criticalChance = 0.2f;
        state.Events(this).AddNormalized(0.5f, () => {
            bool isCritical = UnityEngine.Random.value < criticalChance;
            int finalDamage = isCritical ? damage * 2 : damage;
            OnAttackHit(finalDamage, attackType + (isCritical ? " (暴击!)" : ""));
        });
    }

    void OnAttackHit(int damage, string attackType)
    {
        Debug.Log($"攻击类型: {attackType}, 伤害: {damage}");
    }

    // 示例调用
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            PerformAttack(50, "轻攻击");
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            PerformAttack(100, "重攻击");
        }
    }
}
```

### 示例5：事件管理器（高级）

```csharp
using Animancer;
using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// 动画事件管理器
/// 集中管理所有动画事件，方便维护和扩展
/// </summary>
public class AnimationEventManager : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 事件配置数据
    [System.Serializable]
    public class AnimEventConfig
    {
        public string AnimationName;
        public List<EventPoint> Events;
    }

    [System.Serializable]
    public class EventPoint
    {
        public float NormalizedTime;
        public string EventName;
    }

    [SerializeField] private List<AnimEventConfig> _EventConfigs;

    private Dictionary<string, System.Action> _eventCallbacks;

    void Awake()
    {
        // 注册所有事件回调
        _eventCallbacks = new Dictionary<string, System.Action>
        {
            { "PlayFootstep", PlayFootstep },
            { "CheckHit", CheckHit },
            { "SpawnEffect", SpawnEffect },
            // 更多事件...
        };
    }

    /// <summary>
    /// 播放动画并自动应用配置的事件
    /// </summary>
    public AnimancerState PlayWithEvents(AnimationClip clip)
    {
        var state = _Animancer.Play(clip);
        ApplyEvents(state, clip.name);
        return state;
    }

    void ApplyEvents(AnimancerState state, string animName)
    {
        var config = _EventConfigs.Find(c => c.AnimationName == animName);
        if (config == null) return;

        state.Events(this).Clear();

        foreach (var eventPoint in config.Events)
        {
            if (_eventCallbacks.TryGetValue(eventPoint.EventName, out var callback))
            {
                state.Events(this).AddNormalized(eventPoint.NormalizedTime, callback);
                Debug.Log($"添加事件: {eventPoint.EventName} @ {eventPoint.NormalizedTime:P0}");
            }
            else
            {
                Debug.LogWarning($"未找到事件回调: {eventPoint.EventName}");
            }
        }
    }

    // 事件回调实现
    void PlayFootstep() => Debug.Log("脚步声");
    void CheckHit() => Debug.Log("攻击检测");
    void SpawnEffect() => Debug.Log("生成特效");
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **使用 Transition 播放动画**
```csharp
// ✅ 好：使用Transition，自动应用Inspector配置的事件
var state = _Animancer.Play(_AttackTransition);
```

2. **使用归一化时间（0-1）**
```csharp
// ✅ 好：归一化时间不受动画长度影响
state.Events(this).AddNormalized(0.5f, Callback);
```

3. **清除旧事件避免重复触发**
```csharp
// ✅ 好：每次播放前清除旧事件
state.Events(this).Clear();
state.Events(this).Add(0.5f, NewCallback);
```

4. **使用 End Event 而非手动计算**
```csharp
// ✅ 好：使用OnEnd
state.Events(this).OnEnd = OnAnimationEnd;
```

5. **使用 Lambda 传递参数**
```csharp
// ✅ 好：清晰的参数传递
int damage = 50;
state.Events(this).Add(0.5f, () => DealDamage(damage));
```

### ❌ DON'T（避免做法）

1. **直接播放 AnimationClip**
```csharp
// ❌ 差：直接播放Clip，无法使用Inspector配置的事件
var state = _Animancer.Play(_AttackClip);
```

2. **硬编码绝对时间**
```csharp
// ❌ 差：如果动画长度改变，时间点就不对了
state.Events(this).Add(1.5f, Callback);
```

3. **忘记清除事件**
```csharp
// ❌ 差：重复播放会累积事件
state.Events(this).Add(0.5f, Callback); // 可能被多次添加
```

4. **使用 Update 轮询动画时间**
```csharp
// ❌ 差：性能低且不精确
void Update()
{
    if (state.Time >= 0.5f && !hasTriggered)
    {
        Callback();
        hasTriggered = true;
    }
}
```

5. **在事件中执行耗时操作**
```csharp
// ❌ 差：阻塞主线程
state.Events(this).Add(0.5f, () => {
    Thread.Sleep(100); // 卡顿！
});
```

---

## FAQ常见问题

### Q1: 如何在同一时间点添加多个事件？

**A:** 多次调用 Add 方法即可：

```csharp
var state = _Animancer.Play(_Attack);
state.Events(this).AddNormalized(0.5f, PlaySound);
state.Events(this).AddNormalized(0.5f, SpawnEffect);
state.Events(this).AddNormalized(0.5f, CheckHit);
```

### Q2: 事件会在循环动画中重复触发吗？

**A:** 是的，循环动画每次循环都会触发事件：

```csharp
// Loop动画会在每次循环时触发事件
var state = _Animancer.Play(_WalkClip);
state.IsLooping = true;
state.Events(this).AddNormalized(0.3f, PlayFootstep); // 每次循环都触发
```

### Q3: 如何临时禁用某个事件？

**A:** 方法1是移除事件，方法2是使用标志位：

```csharp
// 方法1：移除事件
state.Events(this).Clear();

// 方法2：使用标志位
bool enableEvent = false;
state.Events(this).Add(0.5f, () => {
    if (enableEvent) Callback();
});
```

### Q4: Animancer Events 和 Animation Events 可以混用吗？

**A:** 可以，两者完全独立：

```csharp
// Animation Events（在Clip中定义）
public void UnityEventCallback() { }

// Animancer Events（代码定义）
state.Events(this).Add(0.5f, AnimancerCallback);
```

### Q5: 事件回调的 `this` 参数是什么？

**A:** 这是用于自动清理的上下文对象：

```csharp
// this 是当前MonoBehaviour
// 当该对象被销毁时，事件会自动清理
state.Events(this).Add(0.5f, Callback);

// 不传this也可以，但需要手动管理生命周期
state.Events().Add(0.5f, Callback); // ⚠️ 需要手动清理
```

### Q6: 如何调试事件没有触发的问题？

**A:** 检查以下几点：

```csharp
// 1. 确认动画在播放
Debug.Log($"动画播放中: {state.IsPlaying}");

// 2. 确认时间有经过事件点
Debug.Log($"当前时间: {state.Time}, 事件时间: 0.5");

// 3. 检查事件是否被添加
var events = state.Events();
Debug.Log($"事件数量: {events.Count}");

// 4. 添加日志到回调中
state.Events(this).Add(0.5f, () => {
    Debug.Log("事件触发！");
    Callback();
});
```

### Q7: 为什么有时候事件触发两次？

**A:** 可能原因：

```csharp
// 原因1：没有清除旧事件
state.Events(this).Clear(); // 添加这行

// 原因2：重复播放动画
if (!state.IsPlaying) // 添加检查
{
    _Animancer.Play(_Clip);
}

// 原因3：动画循环
state.IsLooping = false; // 如果不需要循环
```

### Q8: 如何在事件中切换动画？

**A:** 直接调用 Play 即可：

```csharp
state.Events(this).OnEnd = () => {
    _Animancer.Play(_NextClip); // 安全
};
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events - Animation](https://kybernetik.com.au/animancer/docs/manual/events/animation/)
- [Animancer Events - Animancer Events](https://kybernetik.com.au/animancer/docs/manual/events/animancer/)
- [Animancer Events - Usage](https://kybernetik.com.au/animancer/docs/manual/events/animancer/usage)
- [Animancer Events - End Events](https://kybernetik.com.au/animancer/docs/manual/events/end/)

### 🔗 官方链接
- [Animancer 官方文档](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Unity Animation Events](https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
