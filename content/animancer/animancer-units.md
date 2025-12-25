# Animancer - Units 官方文档

## 📋 目录
- [概述](#概述)
- [Units 特性](#units-特性)
- [内置单位类型](#内置单位类型)
- [自定义单位](#自定义单位)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [参考资料](#参考资料)

---

## 概述

**Units 特性**用于在 Unity Inspector 中为数值字段添加单位后缀，提升可读性和直观性。

### 🎯 核心优势

| 特性 | 说明 |
|------|------|
| **可读性** | 清晰显示数值的单位（秒、米、度等） |
| **直观性** | 无需注释即可理解字段含义 |
| **一致性** | 统一的单位显示规范 |

### 基本用法

```csharp
using Animancer;
using UnityEngine;

public class UnitsExample : MonoBehaviour
{
    // ❌ 没有单位：不清楚是什么单位
    [SerializeField] private float _duration = 2.5f;

    // ✅ 有单位：清楚地显示为秒
    [SerializeField, Units("秒")]
    private float _duration = 2.5f;
}
```

### Inspector 显示效果

```
Without Units:
Duration: 2.5

With Units:
Duration: 2.5 秒
```

---

## Units 特性

### 基本语法

```csharp
[Units(string suffix)]
```

### 参数说明

- **suffix** - 显示在数值后的单位字符串

### 完整示例

```csharp
using Animancer;
using UnityEngine;

public class MovementController : MonoBehaviour
{
    [Header("速度设置")]
    [SerializeField, Units("m/s")]
    private float _moveSpeed = 5f;

    [SerializeField, Units("m/s")]
    private float _sprintSpeed = 8f;

    [Header("旋转设置")]
    [SerializeField, Units("度/秒")]
    private float _turnRate = 180f;

    [Header("跳跃设置")]
    [SerializeField, Units("米")]
    private float _jumpHeight = 2f;

    [SerializeField, Units("秒")]
    private float _jumpCooldown = 0.5f;

    [Header("重力设置")]
    [SerializeField, Units("m/s²")]
    private float _gravity = 9.81f;
}
```

---

## 内置单位类型

Animancer 提供了一些常用的单位特性：

### 时间单位

```csharp
using Animancer;
using UnityEngine;

public class TimeUnits : MonoBehaviour
{
    [SerializeField, Seconds]
    private float _duration = 2.5f;  // 显示: 2.5 x

    [SerializeField, Seconds(Rule = Validate.Value.IsNotNegative)]
    private float _delay = 1f;  // 非负验证

    [SerializeField, Units("毫秒")]
    private float _cooldown = 500f;  // 显示: 500 毫秒
}
```

### 角度单位

```csharp
using Animancer;
using UnityEngine;

public class AngleUnits : MonoBehaviour
{
    [SerializeField, Degrees]
    private float _rotationAngle = 90f;  // 显示: 90°

    [SerializeField, Units("弧度")]
    private float _angleInRadians = 1.57f;  // 显示: 1.57 弧度
}
```

### 距离单位

```csharp
using Animancer;
using UnityEngine;

public class DistanceUnits : MonoBehaviour
{
    [SerializeField, Meters]
    private float _distance = 10f;  // 显示: 10m

    [SerializeField, Units("厘米")]
    private float _offset = 5f;  // 显示: 5 厘米

    [SerializeField, Units("公里")]
    private float _viewDistance = 2f;  // 显示: 2 公里
}
```

### 百分比单位

```csharp
using Animancer;
using UnityEngine;

public class PercentageUnits : MonoBehaviour
{
    [SerializeField, Units("%")]
    private float _damageMultiplier = 150f;  // 显示: 150%

    [SerializeField, Units("%", Rule = Validate.Value.IsFinite)]
    private float _speedBoost = 25f;  // 显示: 25%，有限值验证
}
```

---

## 自定义单位

### 创建自定义单位特性

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 自定义单位特性：力 (牛顿)
/// </summary>
public class NewtonsAttribute : UnitsAttribute
{
    public NewtonsAttribute() : base("N") { }
}

/// <summary>
/// 自定义单位特性：质量 (千克)
/// </summary>
public class KilogramsAttribute : UnitsAttribute
{
    public KilogramsAttribute() : base("kg") { }
}

/// <summary>
/// 自定义单位特性：频率 (Hz)
/// </summary>
public class HertzAttribute : UnitsAttribute
{
    public HertzAttribute() : base("Hz") { }
}

// 使用自定义单位
public class PhysicsController : MonoBehaviour
{
    [SerializeField, Newtons]
    private float _pushForce = 500f;  // 显示: 500N

    [SerializeField, Kilograms]
    private float _mass = 70f;  // 显示: 70kg

    [SerializeField, Hertz]
    private float _frequency = 60f;  // 显示: 60Hz
}
```

### 带验证规则的自定义单位

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 自定义单位：速度（m/s），仅允许正值
/// </summary>
public class SpeedAttribute : UnitsAttribute
{
    public SpeedAttribute() : base("m/s")
    {
        Rule = Validate.Value.IsNotNegative;
    }
}

/// <summary>
/// 自定义单位：角速度（度/秒），限制范围
/// </summary>
public class AngularSpeedAttribute : UnitsAttribute
{
    public AngularSpeedAttribute(float min = 0, float max = 360)
        : base("°/s")
    {
        Rule = Validate.Value.InRange(min, max);
    }
}

// 使用带验证的单位
public class ValidatedUnits : MonoBehaviour
{
    [SerializeField, Speed]
    private float _velocity = 10f;  // 只能为非负值

    [SerializeField, AngularSpeed(0, 180)]
    private float _turnSpeed = 90f;  // 限制在0-180范围
}
```

---

## 代码示例

### 示例1：角色控制器单位标注

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 完整的角色控制器单位标注
/// </summary>
public class CharacterController : MonoBehaviour
{
    [Header("移动")]
    [SerializeField, Units("m/s"), Tooltip("行走速度")]
    private float _walkSpeed = 3f;

    [SerializeField, Units("m/s"), Tooltip("奔跑速度")]
    private float _runSpeed = 6f;

    [SerializeField, Units("m/s"), Tooltip("冲刺速度")]
    private float _sprintSpeed = 10f;

    [Header("旋转")]
    [SerializeField, Degrees, Tooltip("转身速度")]
    private float _rotationSpeed = 720f;

    [SerializeField, Degrees, Tooltip("最大仰角")]
    private float _maxPitchAngle = 80f;

    [Header("跳跃")]
    [SerializeField, Meters, Tooltip("跳跃高度")]
    private float _jumpHeight = 2f;

    [SerializeField, Seconds, Tooltip("跳跃冷却")]
    private float _jumpCooldown = 0.2f;

    [SerializeField, Units("次"), Tooltip("空中最大跳跃次数")]
    private int _maxAirJumps = 1;

    [Header("物理")]
    [SerializeField, Units("m/s²"), Tooltip("重力加速度")]
    private float _gravity = 20f;

    [SerializeField, Units("kg"), Tooltip("角色质量")]
    private float _mass = 70f;

    [Header("动画")]
    [SerializeField, Seconds, Tooltip("动画混合时间")]
    private float _blendDuration = 0.2f;

    [SerializeField, Units("%"), Tooltip("动画速度倍率")]
    private float _animationSpeed = 100f;
}
```

### 示例2：战斗系统单位标注

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 战斗系统参数单位标注
/// </summary>
public class CombatSystem : MonoBehaviour
{
    [Header("伤害")]
    [SerializeField, Units("点"), Tooltip("基础伤害")]
    private float _baseDamage = 10f;

    [SerializeField, Units("%"), Tooltip("暴击伤害加成")]
    private float _criticalDamageMultiplier = 200f;

    [SerializeField, Units("%"), Tooltip("暴击几率")]
    [Range(0, 100)]
    private float _criticalChance = 15f;

    [Header("攻击")]
    [SerializeField, Seconds, Tooltip("攻击间隔")]
    private float _attackInterval = 1.5f;

    [SerializeField, Meters, Tooltip("攻击范围")]
    private float _attackRange = 2f;

    [SerializeField, Degrees, Tooltip("攻击角度")]
    [Range(0, 180)]
    private float _attackAngle = 90f;

    [Header("防御")]
    [SerializeField, Units("点"), Tooltip("防御值")]
    private float _defense = 50f;

    [SerializeField, Units("%"), Tooltip("伤害减免")]
    [Range(0, 100)]
    private float _damageReduction = 25f;

    [SerializeField, Seconds, Tooltip("格挡持续时间")]
    private float _blockDuration = 2f;

    [Header("连击")]
    [SerializeField, Seconds, Tooltip("连击窗口")]
    private float _comboWindow = 0.5f;

    [SerializeField, Units("次"), Tooltip("最大连击数")]
    private int _maxComboCount = 3;

    [SerializeField, Units("%"), Tooltip("连击伤害加成/每击")]
    private float _comboDamageBonus = 10f;
}
```

### 示例3：动画系统单位标注

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 动画系统参数单位标注
/// </summary>
public class AnimationSystem : MonoBehaviour
{
    [Header("混合设置")]
    [SerializeField, Seconds, Tooltip("默认淡入时间")]
    private float _defaultFadeIn = 0.25f;

    [SerializeField, Seconds, Tooltip("默认淡出时间")]
    private float _defaultFadeOut = 0.25f;

    [SerializeField, Seconds, Tooltip("快速混合时间")]
    private float _quickBlend = 0.1f;

    [Header("动画速度")]
    [SerializeField, Units("%"), Tooltip("全局动画速度")]
    [Range(50, 200)]
    private float _globalSpeed = 100f;

    [SerializeField, Units("x"), Tooltip("慢动作倍率")]
    [Range(0.1f, 1f)]
    private float _slowMotionScale = 0.5f;

    [Header("IK设置")]
    [SerializeField, Units("%"), Tooltip("手部IK权重")]
    [Range(0, 100)]
    private float _handIKWeight = 100f;

    [SerializeField, Units("%"), Tooltip("脚部IK权重")]
    [Range(0, 100)]
    private float _footIKWeight = 80f;

    [SerializeField, Meters, Tooltip("脚步射线长度")]
    private float _footRayDistance = 1f;

    [Header("根运动")]
    [SerializeField, Units("%"), Tooltip("位置根运动权重")]
    [Range(0, 100)]
    private float _positionRootMotion = 100f;

    [SerializeField, Units("%"), Tooltip("旋转根运动权重")]
    [Range(0, 100)]
    private float _rotationRootMotion = 100f;
}
```

### 示例4：自定义单位库

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 游戏专用单位库
/// </summary>
namespace MyGame.Units
{
    // 货币单位
    public class GoldAttribute : UnitsAttribute
    {
        public GoldAttribute() : base("金币") { }
    }

    public class GemsAttribute : UnitsAttribute
    {
        public GemsAttribute() : base("宝石") { }
    }

    // 经验单位
    public class ExperienceAttribute : UnitsAttribute
    {
        public ExperienceAttribute() : base("经验") { }
    }

    // 等级单位
    public class LevelAttribute : UnitsAttribute
    {
        public LevelAttribute() : base("级") { }
    }

    // 耐力单位
    public class StaminaAttribute : UnitsAttribute
    {
        public StaminaAttribute() : base("点") { }
    }
}

// 使用自定义单位
using MyGame.Units;

public class PlayerStats : MonoBehaviour
{
    [Header("货币")]
    [SerializeField, Gold]
    private int _gold = 100;

    [SerializeField, Gems]
    private int _gems = 10;

    [Header("等级")]
    [SerializeField, Level]
    private int _level = 1;

    [SerializeField, Experience]
    private int _experience = 0;

    [SerializeField, Experience]
    private int _experienceToNextLevel = 100;

    [Header("耐力")]
    [SerializeField, Stamina]
    private float _maxStamina = 100f;

    [SerializeField, Stamina]
    private float _currentStamina = 100f;

    [SerializeField, Units("点/秒")]
    private float _staminaRegenRate = 10f;
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

#### 1. 为所有数值字段添加单位

```csharp
// ✅ 好：清晰的单位标注
[SerializeField, Seconds]
private float _duration = 2f;

[SerializeField, Meters]
private float _distance = 10f;
```

#### 2. 使用语义化的单位

```csharp
// ✅ 好：使用通用单位
[SerializeField, Units("m/s")]  // 米/秒
[SerializeField, Units("°")]    // 度
[SerializeField, Units("%")]    // 百分比
```

#### 3. 创建项目专用单位库

```csharp
// ✅ 好：统一的单位管理
namespace MyGame.Units
{
    public class DamageAttribute : UnitsAttribute
    {
        public DamageAttribute() : base("伤害") { }
    }
}
```

### ❌ DON'T（避免做法）

#### 1. 省略明显的单位

```csharp
// ❌ 差：不清楚是秒还是帧
[SerializeField]
private float _delay = 0.5f;

// ✅ 好
[SerializeField, Seconds]
private float _delay = 0.5f;
```

#### 2. 使用不一致的单位表示

```csharp
// ❌ 差：混乱的单位表示
[SerializeField, Units("s")]
private float _time1;

[SerializeField, Units("秒")]
private float _time2;

[SerializeField, Units("sec")]
private float _time3;

// ✅ 好：统一使用 Seconds 或中文
[SerializeField, Seconds]
private float _time;
```

#### 3. 忽略验证规则

```csharp
// ❌ 差：没有验证
[SerializeField, Seconds]
private float _cooldown; // 可能为负值！

// ✅ 好：添加验证
[SerializeField, Seconds(Rule = Validate.Value.IsNotNegative)]
private float _cooldown;
```

---

## FAQ

### Q1: Units 特性会影响运行时性能吗？

**A:** 不会。Units 是编辑器专用特性，仅影响 Inspector 显示，不会进入构建版本。

### Q2: 如何创建复合单位（如 m/s²）？

**A:** 直接在字符串中使用：

```csharp
[SerializeField, Units("m/s²")]
private float _acceleration = 10f;
```

### Q3: 能否动态更改单位显示？

**A:** Units 特性是编译时确定的，不支持运行时更改。如需动态单位，考虑使用自定义 PropertyDrawer。

### Q4: 内置的 Seconds/Meters/Degrees 从何而来？

**A:** Animancer 提供了这些常用单位特性：

```csharp
// Animancer 内置
public class SecondsAttribute : UnitsAttribute
{
    public SecondsAttribute() : base("x") { }
}

public class DegreesAttribute : UnitsAttribute
{
    public DegreesAttribute() : base("°") { }
}

public class MetersAttribute : UnitsAttribute
{
    public MetersAttribute() : base("m") { }
}
```

### Q5: 可以为 Vector2/Vector3 添加单位吗？

**A:** 可以，但单位会应用于整个向量：

```csharp
[SerializeField, Units("m")]
private Vector3 _position; // 显示: X:10m Y:5m Z:0m
```

---

## 参考资料

### 📚 相关文档
- [Animancer Units API](https://kybernetik.com.au/animancer/api/Animancer.Units/)
- [Unity Custom Attributes](https://docs.unity3d.com/Manual/Attributes.html)

### 💡 相关类型
- `UnitsAttribute` - 基础单位特性
- `SecondsAttribute` - 时间单位
- `DegreesAttribute` - 角度单位
- `MetersAttribute` - 距离单位

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
