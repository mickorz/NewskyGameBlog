---
title: "Animancer - Strings"
date: 2025-12-25
draft: false
---

# Animancer - Strings 官方文档

## 📋 目录
- [概述](#概述)
- [StringReference](#stringreference)
- [StringAsset](#stringasset)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [参考资料](#参考资料)

---

## 概述

**Strings 系统**提供了两个工具来优化字符串处理性能：

- **StringReference** - 缓存字符串引用以避免重复的字符串比较
- **StringAsset** - 将字符串封装为 ScriptableObject 资产

### 🎯 核心优势

| 工具 | 用途 | 性能优化 |
|------|------|----------|
| **StringReference** | 缓存字符串引用 | 避免重复的字符串比较 |
| **StringAsset** | 字符串资产化 | 引用比较替代值比较 |

---

## StringReference

### 问题：重复的字符串查找

```csharp
// ❌ 每次调用都进行字符串比较
public void UpdateParameter()
{
    _animancer.Parameters.Get<float>("Speed"); // 字符串比较
    _animancer.Parameters.Get<float>("Speed"); // 再次比较
    _animancer.Parameters.Get<float>("Speed"); // 又一次比较
}
```

### 解决方案：StringReference

```csharp
using Animancer;

public class CharacterController : MonoBehaviour
{
    // ✅ 缓存 StringReference
    private static readonly StringReference SpeedParameter = "Speed";

    private AnimancerComponent _animancer;

    void Update()
    {
        // 使用缓存的引用（更快）
        var speed = _animancer.Parameters.Get<float>(SpeedParameter);
    }
}
```

### 工作原理

```csharp
/// <summary>
/// StringReference 内部结构
/// </summary>
public readonly struct StringReference
{
    private readonly string _string;
    private readonly int _hashCode;

    public StringReference(string value)
    {
        _string = value;
        _hashCode = value?.GetHashCode() ?? 0;
    }

    // 隐式转换
    public static implicit operator StringReference(string value)
        => new StringReference(value);
}
```

### 性能对比

```csharp
using UnityEngine;

public class StringPerformanceTest : MonoBehaviour
{
    private ParameterDictionary _parameters;
    private static readonly StringReference CachedKey = "TestParam";

    void TestPerformance()
    {
        // ❌ 方式1：原始字符串（较慢）
        for (int i = 0; i < 10000; i++)
        {
            _parameters.Get<float>("TestParam");
        }

        // ✅ 方式2：StringReference（更快）
        for (int i = 0; i < 10000; i++)
        {
            _parameters.Get<float>(CachedKey);
        }
    }
}
```

---

## StringAsset

### 概念

**StringAsset** 是一个 ScriptableObject 包装器，将字符串作为项目资产。

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 字符串资产
/// </summary>
[CreateAssetMenu(menuName = "Animancer/String Asset")]
public class StringAsset : ScriptableObject
{
    [SerializeField]
    private string _value;

    public string Value => _value;

    // 隐式转换为 string
    public static implicit operator string(StringAsset asset)
        => asset._value;

    // 隐式转换为 StringReference
    public static implicit operator StringReference(StringAsset asset)
        => new StringReference(asset._value);
}
```

### 使用场景

#### 场景1：共享参数名称

```csharp
using Animancer;
using UnityEngine;

public class SharedParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // 在 Inspector 中分配 StringAsset
    [SerializeField] private StringAsset _speedParameter;
    [SerializeField] private StringAsset _jumpParameter;

    void Update()
    {
        // 使用 StringAsset
        var speed = _animancer.Parameters.Get<float>(_speedParameter);
        var canJump = _animancer.Parameters.Get<bool>(_jumpParameter);

        Debug.Log($"Speed: {speed}, CanJump: {canJump}");
    }
}
```

#### 场景2：多个系统共享常量

```csharp
using UnityEngine;

/// <summary>
/// 创建共享的字符串常量资产
/// </summary>
public class AnimationParameters : ScriptableObject
{
    public static StringAsset Speed;
    public static StringAsset IsGrounded;
    public static StringAsset AttackTrigger;

    [RuntimeInitializeOnLoadMethod]
    static void Initialize()
    {
        // 加载资产
        Speed = Resources.Load<StringAsset>("Parameters/Speed");
        IsGrounded = Resources.Load<StringAsset>("Parameters/IsGrounded");
        AttackTrigger = Resources.Load<StringAsset>("Parameters/AttackTrigger");
    }
}

// 在多个脚本中使用
public class PlayerController : MonoBehaviour
{
    void Update()
    {
        _animancer.Parameters.Set(AnimationParameters.Speed, currentSpeed);
    }
}

public class CombatSystem : MonoBehaviour
{
    void Attack()
    {
        _animancer.Parameters.Set(AnimationParameters.AttackTrigger, true);
    }
}
```

---

## 代码示例

### 示例1：完整的 StringReference 使用

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 使用 StringReference 优化参数访问
/// </summary>
public class OptimizedParameterAccess : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // ✅ 静态缓存所有参数名称
    private static readonly StringReference Speed = "Speed";
    private static readonly StringReference TurnRate = "TurnRate";
    private static readonly StringReference IsGrounded = "IsGrounded";
    private static readonly StringReference IsAirborne = "IsAirborne";

    void Update()
    {
        // 高效的参数访问
        float speed = GetMovementSpeed();
        _animancer.Parameters.Set(Speed, speed);

        float turnRate = CalculateTurnRate();
        _animancer.Parameters.Set(TurnRate, turnRate);

        bool grounded = CheckGrounded();
        _animancer.Parameters.Set(IsGrounded, grounded);
        _animancer.Parameters.Set(IsAirborne, !grounded);
    }

    float GetMovementSpeed() => 5f;
    float CalculateTurnRate() => 180f;
    bool CheckGrounded() => true;
}
```

### 示例2：StringAsset 配置系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 使用 StringAsset 创建可配置的参数系统
/// </summary>
public class ConfigurableParameterSystem : MonoBehaviour
{
    [System.Serializable]
    public class ParameterConfig
    {
        public StringAsset ParameterName;
        public float DefaultValue;
        public float MinValue;
        public float MaxValue;
    }

    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private ParameterConfig[] _parameters;

    void Start()
    {
        // 初始化所有参数
        foreach (var config in _parameters)
        {
            _animancer.Parameters.Set(
                config.ParameterName,
                config.DefaultValue
            );
        }
    }

    public void SetParameter(StringAsset paramName, float value)
    {
        // 查找配置
        var config = System.Array.Find(
            _parameters,
            p => p.ParameterName == paramName
        );

        if (config != null)
        {
            // 应用范围限制
            value = Mathf.Clamp(value, config.MinValue, config.MaxValue);
            _animancer.Parameters.Set(paramName, value);
        }
    }
}
```

### 示例3：参数名称中心化管理

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 中心化管理所有动画参数
/// </summary>
public static class AnimParams
{
    // 移动参数
    public static readonly StringReference Speed = "Speed";
    public static readonly StringReference Direction = "Direction";
    public static readonly StringReference TurnRate = "TurnRate";

    // 状态参数
    public static readonly StringReference IsGrounded = "IsGrounded";
    public static readonly StringReference IsAirborne = "IsAirborne";
    public static readonly StringReference IsCrouching = "IsCrouching";

    // 战斗参数
    public static readonly StringReference AttackSpeed = "AttackSpeed";
    public static readonly StringReference WeaponType = "WeaponType";
    public static readonly StringReference IsBlocking = "IsBlocking";
}

/// <summary>
/// 使用中心化参数
/// </summary>
public class CentralizedParameterUsage : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    void Update()
    {
        // ✅ 使用中心化的参数名称
        _animancer.Parameters.Set(AnimParams.Speed, 5f);
        _animancer.Parameters.Set(AnimParams.IsGrounded, true);

        // 类型安全且易于重构
    }
}
```

### 示例4：创建 StringAsset 资产

```csharp
using Animancer;
using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;

/// <summary>
/// 编辑器工具：批量创建 StringAsset
/// </summary>
public static class StringAssetCreator
{
    [MenuItem("Assets/Create/Animancer/Batch Create String Assets")]
    static void CreateStringAssets()
    {
        string[] parameterNames = new[]
        {
            "Speed",
            "Direction",
            "IsGrounded",
            "AttackSpeed"
        };

        foreach (var paramName in parameterNames)
        {
            // 创建 StringAsset 实例
            var asset = ScriptableObject.CreateInstance<StringAsset>();

            // 设置值（需要反射或公开setter）
            var serializedObject = new SerializedObject(asset);
            serializedObject.FindProperty("_value").stringValue = paramName;
            serializedObject.ApplyModifiedProperties();

            // 保存资产
            string path = $"Assets/Parameters/{paramName}.asset";
            AssetDatabase.CreateAsset(asset, path);
        }

        AssetDatabase.SaveAssets();
        Debug.Log($"创建了 {parameterNames.Length} 个 StringAsset");
    }
}
#endif
```

---

## 最佳实践

### ✅ DO（推荐做法）

#### 1. 使用 static readonly 缓存 StringReference

```csharp
// ✅ 好：静态缓存
public class Controller : MonoBehaviour
{
    private static readonly StringReference SpeedParam = "Speed";

    void Update()
    {
        _animancer.Parameters.Set(SpeedParam, 5f);
    }
}
```

#### 2. 中心化管理参数名称

```csharp
// ✅ 好：统一管理
public static class AnimParams
{
    public static readonly StringReference Speed = "Speed";
    public static readonly StringReference Jump = "Jump";
}
```

#### 3. 使用 StringAsset 共享配置

```csharp
// ✅ 好：在多个脚本间共享
[SerializeField] private StringAsset _speedParameter;
```

### ❌ DON'T（避免做法）

#### 1. 重复使用原始字符串

```csharp
// ❌ 差：每次都创建新字符串
void Update()
{
    _animancer.Parameters.Set("Speed", 5f);
    _animancer.Parameters.Get<float>("Speed");
    _animancer.Parameters.Get<float>("Speed"); // 重复比较
}
```

#### 2. 在非静态字段中缓存

```csharp
// ❌ 差：实例字段浪费内存
public class Controller : MonoBehaviour
{
    private StringReference _speedParam = "Speed"; // 每个实例都有副本
}
```

#### 3. 硬编码字符串散落各处

```csharp
// ❌ 差：难以维护
void Update()
{
    _animancer.Parameters.Set("Speed", 5f);
}

void FixedUpdate()
{
    _animancer.Parameters.Set("Spead", 3f); // 拼写错误！
}
```

---

## FAQ

### Q1: StringReference 和 string 有什么区别？

**A:** StringReference 缓存了字符串的哈希码，避免重复的字符串比较操作。

```csharp
// 原始字符串：每次都比较字符内容
_parameters.Get<float>("Speed"); // O(n)

// StringReference：使用缓存的哈希码
_parameters.Get<float>(SpeedRef); // O(1)
```

### Q2: 什么时候使用 StringAsset？

**A:** 当需要在多个脚本或预制体间共享相同的参数名称时。

```csharp
// 场景1：多个系统使用相同参数
[SerializeField] private StringAsset _speedParam; // 在Inspector中分配

// 场景2：避免拼写错误
// StringAsset 提供资产引用，避免硬编码字符串
```

### Q3: 如何在Inspector中编辑 StringAsset？

**A:** 创建自定义编辑器或直接在 StringAsset 中公开字段：

```csharp
[CreateAssetMenu]
public class StringAsset : ScriptableObject
{
    [SerializeField]
    private string _value; // 在Inspector中可编辑

    public string Value => _value;
}
```

### Q4: 性能提升有多大？

**A:** 取决于调用频率：

- **低频调用**（每秒几次）：差异可忽略
- **高频调用**（每帧多次）：可提升 10-30%
- **极高频调用**（每帧数百次）：可提升 50%+

### Q5: 可以在运行时创建 StringReference 吗？

**A:** 可以，但推荐静态缓存：

```csharp
// ✅ 推荐：编译时创建
private static readonly StringReference Speed = "Speed";

// ⚠️ 可行但不推荐：运行时创建
void Start()
{
    StringReference speedRef = "Speed"; // 每次Start都创建
}
```

---

## 参考资料

### 📚 相关文档
- [Parameters](https://kybernetik.com.au/animancer/docs/manual/parameters/)
- [Animancer API](https://kybernetik.com.au/animancer/api/Animancer/)

### 💡 相关类型
- `StringReference` - 字符串引用结构体
- `StringAsset` - 字符串资产 ScriptableObject
- `ParameterDictionary` - 参数字典

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
