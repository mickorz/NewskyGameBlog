# Animancer Events - Parameters 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [使用带参数的回调](#使用带参数的回调)
- [内置参数类型](#内置参数类型)
- [自定义参数类型](#自定义参数类型)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

Animancer Events 默认使用无参数回调，但支持通过 `AnimancerEvent.Parameter` 系统传递参数值给事件回调。

### 🎯 核心特性

> **"事件回调默认为无参数，但可以通过设置 AnimancerEvent.Parameter 选项来传递参数值"**

---

## 核心概念

### 📦 参数系统架构

```
AnimancerEvent
    ├── 无参数回调 (默认)
    │   └── Action callback
    │
    └── 带参数回调
            ├── AnimancerEvent.Parameter<T> (引用类型)
            └── AnimancerEvent.ParameterBoxed<T> (值类型)
```

### 🔍 参数类型分类

| 参数类型 | 基类 | 适用于 | 示例 |
|---------|------|--------|------|
| **引用类型** | `AnimancerEvent.Parameter<T>` | class | AudioSource, GameObject |
| **值类型** | `AnimancerEvent.ParameterBoxed<T>` | struct, enum | Vector3, int, SoundType |

---

## 使用带参数的回调

### 🎯 基础语法

使用泛型方法注册带参数的回调：

```csharp
// 泛型语法指定参数类型
_Animancer.Events.AddTo<AudioSource>(_EventName, PlaySound);
_Animation.Events.AddCallback<AudioSource>(_EventName, PlaySound);
```

### 📚 三种配置方式

所有三种事件配置方式都支持参数：

#### 1. Central Events（中央事件）

```csharp
void Awake()
{
    // 注册带参数的全局事件
    _Animancer.Events.AddTo<AudioSource>("PlaySound", PlaySound);
}

void PlaySound(AudioSource audioSource)
{
    audioSource.Play();
}
```

#### 2. Transition Events（Transition事件）

```csharp
void Start()
{
    // 为Transition注册带参数回调
    _AttackTransition.Events.AddCallback<int>("Hit", OnHit);
}

void OnHit(int damage)
{
    Debug.Log($"造成 {damage} 点伤害");
}
```

#### 3. State Events（状态事件）

```csharp
void PerformAttack()
{
    var state = _Animancer.Play(_AttackClip);

    // 在状态上注册带参数回调
    state.Events.AddCallback<Vector3>("SpawnEffect", SpawnEffect);
}

void SpawnEffect(Vector3 position)
{
    Instantiate(_EffectPrefab, position, Quaternion.identity);
}
```

---

## 内置参数类型

Animancer 内置支持常见参数类型：

### 📝 常用类型

```csharp
// Unity常用类型（引用类型）
AudioSource
GameObject
Transform
ParticleSystem
AudioClip

// 值类型
int
float
bool
Vector3
Quaternion
```

### 📊 使用示例

```csharp
using Animancer;
using UnityEngine;

public class BuiltInParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    void Awake()
    {
        // AudioSource参数
        _Animancer.Events.AddTo<AudioSource>("PlaySound", PlaySound);

        // int参数
        _Animancer.Events.AddTo<int>("Damage", ApplyDamage);

        // Vector3参数
        _Animancer.Events.AddTo<Vector3>("SpawnAt", SpawnEffect);

        // bool参数
        _Animancer.Events.AddTo<bool>("SetActive", SetWeaponActive);
    }

    void PlaySound(AudioSource source) => source.Play();
    void ApplyDamage(int damage) => Debug.Log($"伤害: {damage}");
    void SpawnEffect(Vector3 pos) => Debug.Log($"生成特效 @ {pos}");
    void SetWeaponActive(bool active) => Debug.Log($"武器激活: {active}");
}
```

---

## 自定义参数类型

### 🎨 创建自定义参数类型

根据类型分类选择基类：

#### 引用类型（class）

```csharp
[System.Serializable]
public class ParameterAudioSource :
    Animancer.AnimancerEvent.Parameter<AudioSource>
{ }
```

#### 值类型（struct/enum）

```csharp
[System.Serializable]
public class ParameterVector3 :
    Animancer.AnimancerEvent.ParameterBoxed<Vector3>
{ }

[System.Serializable]
public class ParameterSoundType :
    Animancer.AnimancerEvent.ParameterBoxed<SoundType>
{ }
```

### 📚 完整示例

```csharp
using Animancer;
using UnityEngine;

// 定义枚举
public enum SoundType
{
    Footstep,
    Jump,
    Land,
    Attack
}

// 创建参数类型
[System.Serializable]
public class ParameterSoundType :
    AnimancerEvent.ParameterBoxed<SoundType>
{ }

/// <summary>
/// 自定义参数类型示例
/// </summary>
public class CustomParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _WalkTransition;

    void Awake()
    {
        // 注册带自定义参数的事件
        _Animancer.Events.AddTo<SoundType>("PlaySound", PlaySound);
    }

    void PlaySound(SoundType soundType)
    {
        Debug.Log($"播放音效: {soundType}");

        switch (soundType)
        {
            case SoundType.Footstep:
                // 播放脚步声
                break;
            case SoundType.Jump:
                // 播放跳跃音效
                break;
            // ...
        }
    }
}
```

### 🔧 高级：实现 IInvokable 接口

对于更复杂的需求，可以直接实现 `IInvokable` 接口：

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 自定义可调用事件
/// </summary>
[System.Serializable]
public class CustomInvokable : IInvokable
{
    public string EventName;
    public int Damage;
    public float Multiplier;

    public void Invoke(AnimancerState state)
    {
        Debug.Log($"事件: {EventName}");
        Debug.Log($"伤害: {Damage * Multiplier}");
    }
}
```

---

## 代码示例

### 示例1：Footstep Events（脚步声事件）

> **官方示例**："Footstep Events示例演示了如何用参数区分左右脚事件"

```csharp
using Animancer;
using UnityEngine;

// 定义脚步类型枚举
public enum FootType
{
    Left,
    Right
}

// 创建参数类型
[System.Serializable]
public class ParameterFootType :
    AnimancerEvent.ParameterBoxed<FootType>
{ }

/// <summary>
/// 脚步声事件参数示例
/// 使用参数区分左右脚，避免创建重复的事件名称
/// </summary>
public class FootstepEventsExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _WalkTransition;

    [Header("音效")]
    [SerializeField] private AudioSource _AudioSource;
    [SerializeField] private AudioClip[] _LeftFootSounds;
    [SerializeField] private AudioClip[] _RightFootSounds;

    [Header("粒子特效")]
    [SerializeField] private ParticleSystem _DustEffect;
    [SerializeField] private Transform _LeftFoot;
    [SerializeField] private Transform _RightFoot;

    void Awake()
    {
        // 注册单个事件名，使用参数区分左右脚
        _Animancer.Events.AddTo<FootType>("Footstep", OnFootstep);
    }

    void OnFootstep(FootType footType)
    {
        // 根据脚步类型播放不同音效
        AudioClip[] sounds = footType == FootType.Left
            ? _LeftFootSounds
            : _RightFootSounds;

        if (sounds.Length > 0)
        {
            var clip = sounds[Random.Range(0, sounds.Length)];
            _AudioSource.PlayOneShot(clip);
        }

        // 在对应脚的位置生成粉尘特效
        Transform foot = footType == FootType.Left
            ? _LeftFoot
            : _RightFoot;

        _DustEffect.transform.position = foot.position;
        _DustEffect.Play();

        Debug.Log($"{footType}脚触地");
    }
}

/*
Inspector配置（在_WalkTransition中）：
- Event 1: Time=0.3, Name="Footstep", Parameter=FootType.Left
- Event 2: Time=0.7, Name="Footstep", Parameter=FootType.Right
*/
```

### 示例2：武器系统参数

```csharp
using Animancer;
using UnityEngine;

// 武器配置
[System.Serializable]
public class WeaponConfig
{
    public string Name;
    public int Damage;
    public float Range;
    public ParticleSystem HitEffect;
}

// 参数类型
[System.Serializable]
public class ParameterWeaponConfig :
    AnimancerEvent.Parameter<WeaponConfig>
{ }

/// <summary>
/// 武器系统参数示例
/// 使用参数传递武器配置
/// </summary>
public class WeaponSystemExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [Header("武器配置")]
    [SerializeField] private WeaponConfig _SwordConfig;
    [SerializeField] private WeaponConfig _AxeConfig;
    [SerializeField] private WeaponConfig _SpearConfig;

    void Awake()
    {
        // 注册带武器配置参数的事件
        _Animancer.Events.AddTo<WeaponConfig>("Attack", OnAttack);
    }

    void OnAttack(WeaponConfig weapon)
    {
        Debug.Log($"攻击: {weapon.Name}");
        Debug.Log($"伤害: {weapon.Damage}");
        Debug.Log($"范围: {weapon.Range}");

        // 检测命中
        CheckHit(weapon);

        // 播放特效
        if (weapon.HitEffect != null)
        {
            weapon.HitEffect.Play();
        }
    }

    void CheckHit(WeaponConfig weapon)
    {
        Collider[] hits = Physics.OverlapSphere(
            transform.position,
            weapon.Range
        );

        foreach (var hit in hits)
        {
            if (hit.CompareTag("Enemy"))
            {
                hit.GetComponent<Enemy>()?.TakeDamage(weapon.Damage);
            }
        }
    }
}

public class Enemy : MonoBehaviour
{
    public void TakeDamage(int damage) { }
}
```

### 示例3：技能特效参数

```csharp
using Animancer;
using UnityEngine;

// 特效配置
[System.Serializable]
public class EffectConfig
{
    public GameObject EffectPrefab;
    public Vector3 LocalOffset;
    public float Lifetime = 2f;
    public bool AttachToParent = false;
}

// 参数类型
[System.Serializable]
public class ParameterEffectConfig :
    AnimancerEvent.Parameter<EffectConfig>
{ }

/// <summary>
/// 技能特效参数示例
/// 使用参数配置特效生成
/// </summary>
public class SkillEffectExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _FireballSkill;
    [SerializeField] private ClipTransition _IceSpellSkill;

    [Header("特效配置")]
    [SerializeField] private EffectConfig _FireballEffect;
    [SerializeField] private EffectConfig _IceEffect;
    [SerializeField] private Transform _CastPoint;

    void Awake()
    {
        // 注册特效生成事件
        _Animancer.Events.AddTo<EffectConfig>("SpawnEffect", SpawnEffect);
    }

    void SpawnEffect(EffectConfig config)
    {
        if (config.EffectPrefab == null) return;

        // 计算生成位置
        Vector3 spawnPos = _CastPoint.position +
                          _CastPoint.TransformDirection(config.LocalOffset);

        // 生成特效
        GameObject effect = Instantiate(
            config.EffectPrefab,
            spawnPos,
            _CastPoint.rotation
        );

        // 是否附加到父物体
        if (config.AttachToParent)
        {
            effect.transform.SetParent(_CastPoint);
        }

        // 设置生命周期
        Destroy(effect, config.Lifetime);

        Debug.Log($"生成特效: {config.EffectPrefab.name}");
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            _Animancer.Play(_FireballSkill);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            _Animancer.Play(_IceSpellSkill);
        }
    }
}

/*
Inspector配置：
- FireballSkill: Event="SpawnEffect", Parameter=_FireballEffect @ 0.6
- IceSpellSkill: Event="SpawnEffect", Parameter=_IceEffect @ 0.5
*/
```

### 示例4：多参数组合

```csharp
using Animancer;
using UnityEngine;

// 复合参数配置
[System.Serializable]
public class AttackData
{
    public int Damage;
    public float KnockbackForce;
    public Vector3 HitDirection;
    public AudioClip HitSound;
    public ParticleSystem HitEffect;
}

// 参数类型
[System.Serializable]
public class ParameterAttackData :
    AnimancerEvent.Parameter<AttackData>
{ }

/// <summary>
/// 多参数组合示例
/// 使用复合参数传递多个配置
/// </summary>
public class MultiParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    [Header("攻击配置")]
    [SerializeField] private AttackData _LightAttackData;
    [SerializeField] private AttackData _HeavyAttackData;
    [SerializeField] private AttackData _SpecialAttackData;

    [SerializeField] private AudioSource _AudioSource;

    void Awake()
    {
        // 注册复合参数事件
        _Animancer.Events.AddTo<AttackData>("ExecuteAttack", ExecuteAttack);
    }

    void ExecuteAttack(AttackData data)
    {
        Debug.Log($"执行攻击:");
        Debug.Log($"- 伤害: {data.Damage}");
        Debug.Log($"- 击退: {data.KnockbackForce}");
        Debug.Log($"- 方向: {data.HitDirection}");

        // 播放音效
        if (data.HitSound != null)
        {
            _AudioSource.PlayOneShot(data.HitSound);
        }

        // 播放特效
        if (data.HitEffect != null)
        {
            data.HitEffect.Play();
        }

        // 执行攻击逻辑
        PerformAttackLogic(data);
    }

    void PerformAttackLogic(AttackData data)
    {
        // 检测敌人
        Collider[] enemies = Physics.OverlapSphere(transform.position, 2f);

        foreach (var enemy in enemies)
        {
            if (enemy.CompareTag("Enemy"))
            {
                // 造成伤害
                enemy.GetComponent<Enemy>()?.TakeDamage(data.Damage);

                // 应用击退
                Rigidbody rb = enemy.GetComponent<Rigidbody>();
                if (rb != null)
                {
                    rb.AddForce(data.HitDirection * data.KnockbackForce, ForceMode.Impulse);
                }
            }
        }
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **使用参数避免重复事件名**
```csharp
// ✅ 好：单个事件名，用参数区分
_Animancer.Events.AddTo<FootType>("Footstep", OnFootstep);

// ❌ 差：多个事件名
_Animancer.Events.Add("FootstepLeft", OnFootstepLeft);
_Animancer.Events.Add("FootstepRight", OnFootstepRight);
```

2. **为值类型使用 ParameterBoxed**
```csharp
// ✅ 好：值类型使用ParameterBoxed
[System.Serializable]
public class ParameterVector3 :
    AnimancerEvent.ParameterBoxed<Vector3> { }
```

3. **为引用类型使用 Parameter**
```csharp
// ✅ 好：引用类型使用Parameter
[System.Serializable]
public class ParameterAudioSource :
    AnimancerEvent.Parameter<AudioSource> { }
```

4. **使用配置对象传递多个参数**
```csharp
// ✅ 好：封装配置
public class AttackConfig
{
    public int Damage;
    public float Range;
    public AudioClip Sound;
}
```

### ❌ DON'T（避免做法）

1. **不要为每个参数值创建事件名**
```csharp
// ❌ 差：难以维护
"FootstepLeft", "FootstepRight", "FootstepLeftHeavy", ...
```

2. **不要混淆参数类型基类**
```csharp
// ❌ 差：Vector3是值类型，应该用ParameterBoxed
public class ParameterVector3 :
    AnimancerEvent.Parameter<Vector3> { } // 错误！
```

3. **不要在参数中存储状态**
```csharp
// ❌ 差：参数应该是数据，不是状态
public class BadParameter
{
    public bool hasTriggered; // 不应该有状态
}
```

---

## FAQ常见问题

### Q1: 什么时候应该使用参数？

**A:**

| 场景 | 是否使用参数 |
|------|------------|
| 多个事件只是参数不同 | ✅ 使用 |
| 需要传递配置数据 | ✅ 使用 |
| 事件逻辑完全不同 | ❌ 不使用，分开事件 |
| 简单的无数据事件 | ❌ 不使用 |

### Q2: Parameter 和 ParameterBoxed 有什么区别？

**A:**

```csharp
// Parameter: 用于引用类型（class）
public class ParameterAudioSource :
    AnimancerEvent.Parameter<AudioSource> { }

// ParameterBoxed: 用于值类型（struct, enum）
public class ParameterVector3 :
    AnimancerEvent.ParameterBoxed<Vector3> { }
```

### Q3: 如何在Inspector中设置参数值？

**A:** 创建参数类型后，会自动在Inspector的事件面板中显示参数字段：

```
Event:
  ├─ Name: "Footstep"
  ├─ Time: 0.3
  └─ Parameter: [FootType Dropdown]
                └─ Left / Right
```

### Q4: 可以传递多个参数吗？

**A:** 不能直接传递多个参数，但可以封装为配置对象：

```csharp
// ✅ 好：封装多个参数
public class EventData
{
    public int Param1;
    public string Param2;
    public Vector3 Param3;
}

_Animancer.Events.AddTo<EventData>("Event", OnEvent);
```

### Q5: 参数类型必须标记为 [Serializable] 吗？

**A:** 如果需要在Inspector中配置，必须标记：

```csharp
// ✅ 好：可以在Inspector中配置
[System.Serializable]
public class ParameterData :
    AnimancerEvent.Parameter<MyData> { }

// ❌ 差：无法在Inspector中配置
public class ParameterData :
    AnimancerEvent.Parameter<MyData> { }
```

---

## 参考资料

### 📚 相关文档
- [Animancer Events - Usage](https://kybernetik.com.au/animancer/docs/manual/events/animancer/usage)
- [Animancer Events - Behaviour](https://kybernetik.com.au/animancer/docs/manual/events/animancer/behaviour)
- [Footstep Events 示例](https://kybernetik.com.au/animancer/docs/samples/)

### 🔗 API 参考
- `AnimancerEvent.Parameter<T>`
- `AnimancerEvent.ParameterBoxed<T>`
- `IInvokable` 接口

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+（需要 Pro 版本）
