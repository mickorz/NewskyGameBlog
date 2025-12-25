---
title: "Animancer Layers"
date: 2025-12-25
draft: false
---

# Animancer Layers 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/layers/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Layers（图层）** 是 Animancer 中实现动画并行播放的核心机制。通过将动画隔离到不同的图层,可以同时播放多个动画而不会相互干扰。

**核心原理**：在某个图层上播放动画时,只会停止同一图层上的其他动画,而不会影响其他图层上的动画。

---

## 核心概念 (Core Concept)

> **当您在某个图层上播放动画时,它会停止该图层上的其他动画,但不会影响不同图层上的动画。**

**工作原理**:
```
Layer 0 (Base Layer):
├─ Walk Animation (Weight: 1.0) → 下半身移动

Layer 1 (Upper Body):
├─ Aim Animation (Weight: 1.0)  → 上半身瞄准

最终输出 = Layer 0 + Layer 1
```

---

## 图层访问和创建 (Layer Access and Creation)

### 基础访问

使用 `AnimancerComponent.Layers` 属性管理图层。

```csharp
using Animancer;
using UnityEngine;

public class LayerAccessExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    void Example()
    {
        // 默认 Layer 0（基础层）
        _Animancer.Play(_Clip);
        // 等价于
        _Animancer.Layers[0].Play(_Clip);

        // Layer 1（如果不存在会自动创建）
        _Animancer.Layers[1].Play(_Clip);

        // Layer 2（会自动创建 Layer 1 和 Layer 2）
        _Animancer.Layers[2].Play(_Clip);
    }
}
```

---

### 自动创建规则

> **重要**：如果指定的图层不存在,系统会自动创建该图层（以及之前的所有图层）。

```csharp
// 初始状态：只有 Layer 0 存在

// 访问 Layer 3
_Animancer.Layers[3].Play(_Clip);

// 结果：自动创建 Layer 0, 1, 2, 3
```

**图层数量管理**:
```csharp
// 手动设置图层数量
_Animancer.Layers.SetCount(4); // 创建 0-3 共 4 个图层

// 获取当前图层数量
int layerCount = _Animancer.Layers.Count;
Debug.Log($"当前图层数量: {layerCount}");
```

---

## 基础用法示例 (Basic Usage Example)

```csharp
using Animancer;
using UnityEngine;

public class LayerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    void ExampleMethod()
    {
        // Layer 0: 播放动画
        _Animancer.Play(_Clip);

        // Layer 1: 播放同一动画（会自动创建 Layer 1）
        _Animancer.Layers[1].Play(_Clip);

        // 淡出 Layer 1
        _Animancer.Layers[1].StartFade(targetWeight: 0, fadeDuration: 0.25f);
    }
}
```

**工作流程**:
1. `Play(_Clip)` → 在 Layer 0 播放
2. `Layers[1].Play(_Clip)` → 在 Layer 1 播放（自动创建）
3. `StartFade(0, 0.25f)` → Layer 1 在 0.25 秒内淡出

---

## 状态克隆 (State Cloning)

### 跨图层播放

> **重要**：如果 AnimancerState 已存在于某个图层,尝试在不同图层播放时,状态会被**克隆**到新图层。

```csharp
// 在 Layer 0 播放
var state0 = _Animancer.Layers[0].Play(_Clip);

// 在 Layer 1 播放同一 Clip
var state1 = _Animancer.Layers[1].Play(_Clip);

// state1 是 state0 的克隆
Debug.Log(state0 == state1); // False（不同的实例）
```

**克隆行为**:
- ✅ 创建独立的状态实例
- ✅ 每个图层可以独立控制同一动画
- ✅ 时间、速度、权重等属性独立

---

## 调试命名 (Debug Naming)

### 设置图层名称

图层支持通过 `SetDebugName()` 设置调试名称,用于 Inspector 显示。

```csharp
void SetupLayers()
{
    // 设置调试名称
    _Animancer.Layers[0].SetDebugName("Base Layer");
    _Animancer.Layers[1].SetDebugName("Upper Body");
    _Animancer.Layers[2].SetDebugName("Additive Effects");

    // 在 Inspector 中会显示这些名称
}
```

⚠️ **注意**：名称仅用于调试,不会在运行时持久化。

---

## 图层混合配置 (Blending Configuration)

### 权重管理 (Weight Management)

**默认权重**:
- 新创建的图层默认权重为 **0**
- 调用 `Play()` 会自动将权重设为 **1**

```csharp
// 创建 Layer 1（默认权重 = 0）
_Animancer.Layers.SetCount(2);
Debug.Log(_Animancer.Layers[1].Weight); // 输出: 0

// 播放动画后权重变为 1
_Animancer.Layers[1].Play(_Clip);
Debug.Log(_Animancer.Layers[1].Weight); // 输出: 1
```

---

### 淡入淡出控制

**手动控制图层权重**:

```csharp
using Animancer;
using UnityEngine;

public class LayerWeightExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _UpperBodyClip;

    void StartUpperBodyAnimation()
    {
        // 播放动画并淡入图层
        _Animancer.Layers[1].Play(_UpperBodyClip);
        _Animancer.Layers[1].StartFade(targetWeight: 1.0f, fadeDuration: 0.3f);
    }

    void StopUpperBodyAnimation()
    {
        // 淡出图层
        _Animancer.Layers[1].StartFade(targetWeight: 0.0f, fadeDuration: 0.3f);
    }
}
```

---

### 重要警告

> ⚠️ **务必淡出图层,而不是状态。否则混合效果不正确。**

```csharp
// ❌ 错误：淡出状态
var state = _Animancer.Layers[1].CurrentState;
state.StartFade(0, 0.25f); // 图层权重仍然是 1

// ✅ 正确：淡出图层
_Animancer.Layers[1].StartFade(0, 0.25f); // 整个图层淡出
```

**原因**：
- 状态权重只控制在该图层内的混合
- 图层权重控制整个图层对最终输出的贡献
- 需要淡出图层才能真正减少该图层的影响

---

## Avatar Mask（头像遮罩）

### 概念说明

**Avatar Mask** 用于控制每个图层影响哪些骨骼。

```
示例配置：
Layer 0 (Full Body):
├─ Mask: None（影响所有骨骼）

Layer 1 (Upper Body):
├─ Mask: UpperBodyMask
│   ├─ ✅ Head, Chest, Arms
│   └─ ❌ Pelvis, Legs
```

---

### 设置 Avatar Mask

```csharp
using Animancer;
using UnityEngine;

public class AvatarMaskExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AvatarMask _UpperBodyMask;
    [SerializeField] private AnimationClip _AimClip;
    [SerializeField] private AnimationClip _WalkClip;

    void Start()
    {
        // Layer 0: 全身行走
        _Animancer.Layers[0].Play(_WalkClip);

        // Layer 1: 只影响上半身（瞄准）
        _Animancer.Layers[1].Mask = _UpperBodyMask;
        _Animancer.Layers[1].Play(_AimClip);
    }
}
```

**最终效果**：
```
骨骼         Layer 0 (Walk)  Layer 1 (Aim)  最终输出
Head         ✅              ✅ (覆盖)      Aim
Chest        ✅              ✅ (覆盖)      Aim
Left Arm     ✅              ✅ (覆盖)      Aim
Right Arm    ✅              ✅ (覆盖)      Aim
Pelvis       ✅              ❌             Walk
Left Leg     ✅              ❌             Walk
Right Leg    ✅              ❌             Walk
```

---

### 创建 Avatar Mask

**步骤**：
1. 右键 → Create → Avatar Mask
2. 在 Inspector 中选择影响的骨骼
3. 在代码中分配给图层

**Inspector 配置示例**：
```
AvatarMask: UpperBody
┌────────────────────┐
│ ☑ Head             │
│ ☑ Body             │
│ ☑ Left Arm         │
│ ☑ Right Arm        │
│ ☐ Left Leg         │
│ ☐ Right Leg        │
│ ☐ Root             │
└────────────────────┘
```

---

## 混合模式 (Blending Modes)

### 覆盖混合（默认）

**默认情况下,每个图层会完全替代前一个图层的输出。**

```csharp
// Layer 0: Walk（全身）
_Animancer.Layers[0].Play(_WalkClip);

// Layer 1: Aim（没有 Mask,会完全覆盖 Layer 0）
_Animancer.Layers[1].Play(_AimClip);

// 结果：只看到 Aim 动画
```

**使用 Avatar Mask 实现部分覆盖**:
```csharp
// Layer 1: 使用 Mask 只覆盖上半身
_Animancer.Layers[1].Mask = _UpperBodyMask;
_Animancer.Layers[1].Play(_AimClip);

// 结果：
// - 上半身：Aim
// - 下半身：Walk
```

---

### 叠加混合（Additive Blending）

**启用叠加模式**:

```csharp
_Animancer.Layers[1].IsAdditive = true;
```

**叠加模式特性**：
- ✅ 不替代下层,而是叠加效果
- ✅ 适合呼吸、受伤效果等
- ⚠️ 需要使用 Additive 类型的动画

```csharp
using Animancer;
using UnityEngine;

public class AdditiveLayerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _BreathingClip; // Additive 动画

    void Start()
    {
        // Layer 0: 基础待机
        _Animancer.Layers[0].Play(_IdleClip);

        // Layer 1: 呼吸效果（叠加）
        _Animancer.Layers[1].IsAdditive = true;
        _Animancer.Layers[1].Play(_BreathingClip);
    }
}
```

**最终效果**:
```
最终姿势 = Layer 0 姿势 + (Layer 1 姿势 - T-Pose) × Layer 1 权重
```

---

## 代码示例集合

### 示例1：上下半身分离控制

```csharp
using Animancer;
using UnityEngine;

public class UpperLowerBodyExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // Layer 0: 下半身
    [SerializeField] private AnimationClip _RunClip;

    // Layer 1: 上半身
    [SerializeField] private AvatarMask _UpperBodyMask;
    [SerializeField] private AnimationClip _ShootClip;
    [SerializeField] private AnimationClip _ReloadClip;

    void Start()
    {
        // 设置 Layer 1 为上半身层
        _Animancer.Layers[1].Mask = _UpperBodyMask;
    }

    void Update()
    {
        // Layer 0: 下半身始终奔跑
        _Animancer.Layers[0].Play(_RunClip);

        // Layer 1: 上半身根据输入切换
        if (Input.GetMouseButton(0))
        {
            _Animancer.Layers[1].Play(_ShootClip);
        }
        else if (Input.GetKeyDown(KeyCode.R))
        {
            _Animancer.Layers[1].Play(_ReloadClip);
        }
    }
}
```

---

### 示例2：淡入淡出图层

```csharp
using Animancer;
using UnityEngine;

public class LayerFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _InjuredWalkClip;

    private bool _isInjured = false;

    void Start()
    {
        // 创建图层并设置初始权重为 0
        _Animancer.Layers.SetCount(2);
        _Animancer.Layers[1].Weight = 0;
    }

    void Update()
    {
        // Layer 1: 受伤行走（始终播放,通过权重控制）
        if (_Animancer.Layers[1].CurrentState == null)
        {
            _Animancer.Layers[1].Play(_InjuredWalkClip);
        }

        // 根据受伤状态调整权重
        float targetWeight = _isInjured ? 1.0f : 0.0f;
        _Animancer.Layers[1].StartFade(targetWeight, fadeDuration: 0.5f);
    }

    [ContextMenu("Toggle Injured")]
    void ToggleInjured()
    {
        _isInjured = !_isInjured;
    }
}
```

---

### 示例3：多图层管理器

```csharp
using Animancer;
using UnityEngine;
using System.Collections.Generic;

public class MultiLayerManager : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    private Dictionary<string, int> _layerIndices = new Dictionary<string, int>
    {
        { "Base", 0 },
        { "UpperBody", 1 },
        { "Additive", 2 },
        { "Override", 3 }
    };

    void Start()
    {
        SetupLayers();
    }

    void SetupLayers()
    {
        // 创建所有图层
        _Animancer.Layers.SetCount(_layerIndices.Count);

        // 设置调试名称
        foreach (var kvp in _layerIndices)
        {
            _Animancer.Layers[kvp.Value].SetDebugName(kvp.Key);
        }

        // 配置特殊图层
        _Animancer.Layers[_layerIndices["Additive"]].IsAdditive = true;
    }

    public void PlayOnLayer(string layerName, AnimationClip clip, float fadeDuration = 0.25f)
    {
        if (_layerIndices.TryGetValue(layerName, out int index))
        {
            _Animancer.Layers[index].Play(clip, fadeDuration);
            Debug.Log($"在图层 '{layerName}' 播放: {clip.name}");
        }
        else
        {
            Debug.LogWarning($"图层 '{layerName}' 不存在");
        }
    }

    public void FadeOutLayer(string layerName, float fadeDuration = 0.25f)
    {
        if (_layerIndices.TryGetValue(layerName, out int index))
        {
            _Animancer.Layers[index].StartFade(0, fadeDuration);
        }
    }
}
```

---

### 示例4：动态图层权重

```csharp
using Animancer;
using UnityEngine;

public class DynamicLayerWeightExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _TiredClip;

    [SerializeField, Range(0f, 100f)]
    private float _stamina = 100f;

    void Start()
    {
        _Animancer.Layers.SetCount(2);
        _Animancer.Layers[1].Play(_TiredClip);
    }

    void Update()
    {
        // 根据体力动态调整疲劳图层权重
        float tiredWeight = 1.0f - (_stamina / 100f);
        _Animancer.Layers[1].Weight = tiredWeight;

        // 模拟体力消耗
        if (Input.GetKey(KeyCode.W))
        {
            _stamina = Mathf.Max(0, _stamina - 10 * Time.deltaTime);
        }
        else
        {
            _stamina = Mathf.Min(100, _stamina + 5 * Time.deltaTime);
        }
    }
}
```

---

## 最佳实践建议

### 1. **合理使用图层数量**

```csharp
// ❌ 不推荐：过多图层
_Animancer.Layers.SetCount(10); // 通常不需要这么多

// ✅ 推荐：2-4 个图层通常足够
_Animancer.Layers.SetCount(3);
// Layer 0: 基础全身动画
// Layer 1: 上半身覆盖
// Layer 2: 叠加效果
```

---

### 2. **始终淡出图层,不是状态**

```csharp
// ❌ 错误
var state = _Animancer.Layers[1].CurrentState;
state.StartFade(0, 0.25f);

// ✅ 正确
_Animancer.Layers[1].StartFade(0, 0.25f);
```

---

### 3. **使用 Avatar Mask 优化性能**

```csharp
// ✅ 推荐：为上半身图层设置 Mask
_Animancer.Layers[1].Mask = _UpperBodyMask;

// 优势：
// - 只计算需要的骨骼
// - 避免不必要的混合计算
```

---

### 4. **管理图层权重**

```csharp
// ✅ 推荐：不使用时将图层权重设为 0
void DisableUpperBodyLayer()
{
    _Animancer.Layers[1].StartFade(0, 0.3f);
    // 权重为 0 时,该图层不参与最终计算
}
```

---

## 常见问题 FAQ

### Q1: 最多可以有多少个图层？

**A**: Animancer 默认支持 **4 个图层**（与 Unity Animator 相同）。

```csharp
// 可以增加图层数量
_Animancer.Layers.SetCount(8); // 增加到 8 个

// ⚠️ 注意：图层越多,性能开销越大
```

---

### Q2: 图层权重为 0 时还会播放动画吗？

**A**: 会播放,但不会影响最终输出。

```csharp
_Animancer.Layers[1].Weight = 0;
_Animancer.Layers[1].Play(_Clip); // ✅ 播放,但不可见

// 建议：权重为 0 时停止播放以节省性能
if (_Animancer.Layers[1].Weight <= 0.01f)
{
    _Animancer.Layers[1].Stop();
}
```

---

### Q3: 如何实现面部表情和身体动画分离？

**A**: 使用 Avatar Mask：

```csharp
// 创建面部 Mask（只包含头部骨骼）
_Animancer.Layers[1].Mask = _FacialMask;
_Animancer.Layers[1].Play(_SmileClip);

// Layer 0: 身体动画
// Layer 1: 面部表情
```

---

### Q4: Additive 图层需要特殊的动画吗？

**A**: 是的,需要使用 **Additive 类型**的动画。

在 Unity 中创建 Additive 动画：
1. 选择 AnimationClip
2. Inspector → Animation → Clip Settings
3. Animation Type → Additive

```csharp
_Animancer.Layers[1].IsAdditive = true;
_Animancer.Layers[1].Play(_AdditiveClip); // 必须是 Additive 类型
```

---

### Q5: 如何调试图层混合问题？

**A**:

```csharp
// 方法1：设置调试名称
_Animancer.Layers[0].SetDebugName("Base");
_Animancer.Layers[1].SetDebugName("UpperBody");

// 方法2：运行时检查权重
void OnGUI()
{
    for (int i = 0; i < _Animancer.Layers.Count; i++)
    {
        var layer = _Animancer.Layers[i];
        GUILayout.Label($"Layer {i}: Weight = {layer.Weight:F2}");
    }
}

// 方法3：Inspector 实时查看
// 运行时在 Inspector 中展开 AnimancerComponent → Layers
```

---

### Q6: 克隆状态会影响性能吗？

**A**: 轻微影响,但通常可以忽略。

```csharp
// 克隆发生：
_Animancer.Layers[0].Play(_Clip); // 创建 State A
_Animancer.Layers[1].Play(_Clip); // 克隆 State A → State B

// 优化建议：
// - 避免在多个图层频繁播放同一动画
// - 使用不同的动画片段
```

---

## 总结

### 核心要点

1. **图层基础**
   - 图层隔离动画,实现并行播放
   - 自动创建机制
   - 独立的权重控制

2. **混合模式**
   - **覆盖模式**（默认）：替代下层
   - **叠加模式**：叠加效果
   - Avatar Mask 控制骨骼影响

3. **权重管理**
   - 新图层默认权重 0
   - `Play()` 自动设为 1
   - 使用 `StartFade()` 平滑过渡

4. **最佳实践**
   - 淡出图层而不是状态
   - 使用 Avatar Mask 优化性能
   - 合理控制图层数量（2-4 个）

### 下一步学习

- 📖 深入学习 **Weighted Layers**（加权图层）
- 🎨 探索 **Additive Blending** 的高级用法
- 📚 了解 **Avatar Mask** 的详细配置
- 🔍 查看实际项目中的图层管理模式

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/layers/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
