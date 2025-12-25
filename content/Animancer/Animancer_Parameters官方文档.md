# Animancer Parameters 官方文档

## 概述

**Animancer Parameters** 是强类型的命名值，存储在中央字典中，用于跨多个动画状态共享数据。

## 核心特性

- **类型安全**：一旦为特定类型创建，只接受该类型
- **集中管理**：所有参数存储在 `AnimancerComponent.Parameters` 字典中
- **监听变化**：支持值变化回调

## 使用方式

### 方式1：缓存访问（推荐）

```csharp
public class ParameterExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private StringReference _speedParam = "Speed";

    private Parameter<float> _speedParameter;

    void Awake()
    {
        // 缓存参数引用
        _speedParameter = _animancer.Parameters.GetOrCreate<float>(_speedParam);

        // 监听值变化
        _speedParameter.OnValueChanged += OnSpeedChanged;
    }

    void Update()
    {
        // 设置值
        _speedParameter.Value = CalculateSpeed();
    }

    void OnSpeedChanged(float newSpeed)
    {
        Debug.Log($"速度改变: {newSpeed}");
    }
}
```

### 方式2：直接访问

```csharp
// 设置值
_animancer.Parameters.SetValue("Speed", 5.0f);

// 获取值
float speed = _animancer.Parameters.GetValue<float>("Speed");

// 监听变化
_animancer.Parameters.AddOnValueChanged<float>("Speed", OnSpeedChanged);
```

## 高级特性

### 平滑参数

```csharp
// 平滑Float参数
var smoothSpeed = new SmoothedFloatParameter(_animancer, "Speed");
smoothSpeed.SmoothTime = 0.25f;
smoothSpeed.Value = targetSpeed; // 平滑过渡

// 平滑Vector2参数
var smoothMove = new SmoothedVector2Parameter(_animancer, "Movement");
smoothMove.Value = targetMovement;
```

### 与Mixer状态集成

```csharp
// Mixer的参数可链接到Animancer Parameters
var mixer = new LinearMixerState(_animancer.Graph);
mixer.Parameter = _animancer.Parameters.GetOrCreate<float>("Speed");
```

## 调试

```csharp
// 启用日志
_animancer.Parameters.LogContext = LogContext.Everything;

// 或通过Inspector右键菜单启用
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
