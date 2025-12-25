# Animancer Weighted Mask Layers 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/layers/weighted/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**WeightedMaskLayers** 是 Animancer Pro 的高级功能,扩展了 Unity 的 `AvatarMask` 系统。它允许开发者**控制每个单独骨骼的权重**,包括随时间淡入淡出,而不是简单地启用或禁用整个骨骼组。

> ⚠️ **重要**：这是 **Animancer Pro 专属功能**

---

## 核心概念 (Core Concept)

**标准 Avatar Mask**：
- 骨骼要么完全启用（1.0）
- 要么完全禁用（0.0）
- 只有二元选择

**Weighted Mask Layers**：
- 每个骨骼可以有 **0.0 - 1.0** 的权重
- 支持骨骼权重的平滑过渡
- 可以随时间淡入淡出骨骼影响

---

## 设置流程 (Setup Process)

### 步骤1：添加组件

**操作**：
1. 选择带有 `AnimancerComponent` 的 GameObject
2. Add Component → Animancer → Weighted Mask Layers

```csharp
// 或通过代码添加
var weightedLayers = gameObject.AddComponent<WeightedMaskLayers>();
```

---

### 步骤2：配置骨骼和组

**操作**：
1. 在 Inspector 中找到 `WeightedMaskLayers` 组件
2. 点击 **Edit** 按钮打开编辑器窗口
3. 配置骨骼权重组

**Inspector 界面示例**：
```
WeightedMaskLayers 组件:
┌────────────────────────────┐
│ ☑ Enabled                  │
│ Animancer: [AnimancerComp] │
│                            │
│ [Edit] 按钮 ← 点击打开编辑器 │
└────────────────────────────┘
```

---

### 步骤3：添加权重组

**编辑器窗口操作**：
1. 点击 **"Add Group"** 创建新的权重组
2. 为每个骨骼设置权重值（0.0 - 1.0）
3. 保存配置

**示例配置**：
```
Weight Group 0: "Upper Body Only"
├─ Head: 1.0
├─ Spine: 1.0
├─ Left Arm: 1.0
├─ Right Arm: 1.0
├─ Pelvis: 0.0
├─ Left Leg: 0.0
└─ Right Leg: 0.0

Weight Group 1: "Partial Upper Body"
├─ Head: 0.5
├─ Spine: 0.7
├─ Left Arm: 0.8
├─ Right Arm: 0.8
├─ Pelvis: 0.2
├─ Left Leg: 0.0
└─ Right Leg: 0.0
```

---

## 权重值系统 (Weight Value System)

### 权重范围和含义

**权重值范围**：**0.0 - 1.0**

| 权重值 | 含义 | 效果 |
|--------|------|------|
| **1.0** | 完全由高层控制 | 等同于 AvatarMask 中包含该骨骼 |
| **0.0** | 完全由低层控制 | 等同于 AvatarMask 中排除该骨骼 |
| **0.0-1.0** | 两层之间插值 | 按权重混合两个图层的骨骼变换 |

---

### 权重计算公式

```csharp
// 最终骨骼变换计算
Transform finalBone = Lerp(
    lowerLayerBone,    // 下层图层的骨骼变换
    upperLayerBone,    // 上层图层的骨骼变换
    boneWeight         // 骨骼权重（0-1）
);
```

**示例**：
```csharp
// 权重 = 0.3
// 最终变换 = 70% 下层 + 30% 上层

// 权重 = 0.7
// 最终变换 = 30% 下层 + 70% 上层
```

---

## 运行时控制 (Runtime Control)

### 方法1：SetWeights（立即切换）

**定义**：立即将图层设置为指定权重组。

```csharp
using Animancer;
using UnityEngine;

public class SetWeightsExample : MonoBehaviour
{
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    void SwitchToUpperBodyOnly()
    {
        // 立即切换到权重组 0（上半身）
        _WeightedLayers.SetWeights(groupIndex: 0);
    }

    void SwitchToPartialUpperBody()
    {
        // 立即切换到权重组 1（部分上半身）
        _WeightedLayers.SetWeights(groupIndex: 1);
    }

    void SwitchToFullBody()
    {
        // 立即切换到权重组 2（全身）
        _WeightedLayers.SetWeights(groupIndex: 2);
    }
}
```

---

### 方法2：FadeWeights（渐变过渡）

**定义**：在指定时间内平滑过渡到目标权重组。

```csharp
using Animancer;
using UnityEngine;

public class FadeWeightsExample : MonoBehaviour
{
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    void SmoothSwitchToUpperBody()
    {
        // 在 0.5 秒内平滑过渡到上半身权重组
        _WeightedLayers.FadeWeights(groupIndex: 0, fadeDuration: 0.5f);
    }

    void QuickSwitchToFullBody()
    {
        // 在 0.2 秒内快速过渡到全身
        _WeightedLayers.FadeWeights(groupIndex: 2, fadeDuration: 0.2f);
    }

    void OnDamaged()
    {
        // 受伤时,在 0.3 秒内过渡到部分上半身控制
        _WeightedLayers.FadeWeights(groupIndex: 1, fadeDuration: 0.3f);
    }
}
```

---

## 实际应用场景

### 场景1：受伤状态过渡

```csharp
using Animancer;
using UnityEngine;

public class InjurySystemExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    [SerializeField] private AnimationClip _NormalWalkClip;
    [SerializeField] private AnimationClip _InjuredWalkClip;

    // 权重组配置：
    // Group 0: 全身正常（所有骨骼 = 0.0）
    // Group 1: 轻伤（上半身 = 0.3）
    // Group 2: 重伤（上半身 = 0.7）

    void Start()
    {
        // Layer 0: 正常行走
        _Animancer.Layers[0].Play(_NormalWalkClip);

        // Layer 1: 受伤行走
        _Animancer.Layers[1].Play(_InjuredWalkClip);

        // 初始状态：全身正常
        _WeightedLayers.SetWeights(0);
    }

    void TakeDamage(float severity)
    {
        if (severity > 0.7f)
        {
            // 重伤：大部分骨骼使用受伤动画
            _WeightedLayers.FadeWeights(groupIndex: 2, fadeDuration: 0.5f);
        }
        else if (severity > 0.3f)
        {
            // 轻伤：部分骨骼使用受伤动画
            _WeightedLayers.FadeWeights(groupIndex: 1, fadeDuration: 0.5f);
        }
    }

    void Heal()
    {
        // 治疗后恢复正常
        _WeightedLayers.FadeWeights(groupIndex: 0, fadeDuration: 1.0f);
    }
}
```

---

### 场景2：疲劳系统

```csharp
using Animancer;
using UnityEngine;

public class FatigueSystemExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    [SerializeField] private AnimationClip _FreshRunClip;
    [SerializeField] private AnimationClip _TiredRunClip;

    // 权重组：
    // Group 0: 精力充沛（所有骨骼 = 0.0）
    // Group 1: 疲劳开始（上半身 = 0.4）
    // Group 2: 非常疲劳（上半身 = 0.8）

    [SerializeField, Range(0f, 100f)]
    private float _stamina = 100f;

    void Start()
    {
        _Animancer.Layers[0].Play(_FreshRunClip);
        _Animancer.Layers[1].Play(_TiredRunClip);
    }

    void Update()
    {
        // 根据体力动态调整权重组
        if (_stamina > 70f)
        {
            _WeightedLayers.FadeWeights(0, 0.3f); // 精力充沛
        }
        else if (_stamina > 30f)
        {
            _WeightedLayers.FadeWeights(1, 0.3f); // 开始疲劳
        }
        else
        {
            _WeightedLayers.FadeWeights(2, 0.3f); // 非常疲劳
        }

        // 模拟体力消耗
        if (Input.GetKey(KeyCode.W))
        {
            _stamina -= 10 * Time.deltaTime;
        }
        else
        {
            _stamina += 5 * Time.deltaTime;
        }
        _stamina = Mathf.Clamp(_stamina, 0, 100);
    }
}
```

---

### 场景3：环境影响（寒冷、醉酒）

```csharp
using Animancer;
using UnityEngine;

public class EnvironmentEffectExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    [SerializeField] private AnimationClip _NormalIdleClip;
    [SerializeField] private AnimationClip _ShiveringIdleClip; // 发抖

    // 权重组：
    // Group 0: 正常（所有 = 0.0）
    // Group 1: 轻微发抖（上半身 = 0.3）
    // Group 2: 严重发抖（上半身 = 0.7）

    void Start()
    {
        _Animancer.Layers[0].Play(_NormalIdleClip);
        _Animancer.Layers[1].Play(_ShiveringIdleClip);
    }

    void OnEnterColdArea()
    {
        // 进入寒冷区域,开始发抖
        _WeightedLayers.FadeWeights(groupIndex: 1, fadeDuration: 2.0f);
    }

    void OnStayInCold(float duration)
    {
        if (duration > 10f)
        {
            // 停留过久,发抖加剧
            _WeightedLayers.FadeWeights(groupIndex: 2, fadeDuration: 1.0f);
        }
    }

    void OnExitColdArea()
    {
        // 离开寒冷区域,逐渐恢复
        _WeightedLayers.FadeWeights(groupIndex: 0, fadeDuration: 3.0f);
    }
}
```

---

## 已知约束 (Known Constraints)

### 仅支持覆盖混合

> **重要限制**：WeightedMaskLayers **仅支持覆盖混合（Override Blending）**,不支持叠加混合（Additive Blending）。

```csharp
// ✅ 支持：覆盖混合
_Animancer.Layers[1].IsAdditive = false; // 默认
_WeightedLayers.FadeWeights(0, 0.5f);

// ❌ 不支持：叠加混合
_Animancer.Layers[1].IsAdditive = true;
_WeightedLayers.FadeWeights(0, 0.5f); // 效果不正确
```

**官方说明**：
- 当前版本限制为覆盖混合
- 未来如果有需求可能会支持叠加混合
- 如果需要叠加混合,建议使用标准的 Layer 系统

---

## 代码示例集合

### 示例1：完整配置示例

```csharp
using Animancer;
using UnityEngine;

public class WeightedLayersSetupExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    [SerializeField] private AnimationClip _BaseAnimation;
    [SerializeField] private AnimationClip _OverrideAnimation;

    void Start()
    {
        SetupAnimations();
        SetupWeightGroups();
    }

    void SetupAnimations()
    {
        // Layer 0: 基础动画
        _Animancer.Layers[0].Play(_BaseAnimation);

        // Layer 1: 覆盖动画
        _Animancer.Layers[1].Play(_OverrideAnimation);
    }

    void SetupWeightGroups()
    {
        // 在 Inspector 中通过 Edit 按钮配置,或者通过代码：

        // 注意：实际配置通常在 Inspector 的编辑器窗口中完成
        // 这里只展示运行时切换的示例
    }

    [ContextMenu("Test: Full Override")]
    void TestFullOverride()
    {
        _WeightedLayers.SetWeights(0); // 假设 Group 0 = 全部覆盖
    }

    [ContextMenu("Test: Partial Override")]
    void TestPartialOverride()
    {
        _WeightedLayers.FadeWeights(1, 0.5f); // Group 1 = 部分覆盖
    }

    [ContextMenu("Test: No Override")]
    void TestNoOverride()
    {
        _WeightedLayers.FadeWeights(2, 0.5f); // Group 2 = 无覆盖
    }
}
```

---

### 示例2：动态权重插值

```csharp
using Animancer;
using UnityEngine;

public class DynamicWeightInterpolationExample : MonoBehaviour
{
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    [SerializeField, Range(0f, 1f)]
    private float _intensity = 0f;

    private int _previousGroupIndex = -1;

    void Update()
    {
        // 根据强度值选择权重组
        int targetGroupIndex = GetGroupIndexByIntensity(_intensity);

        // 只在组索引变化时切换
        if (targetGroupIndex != _previousGroupIndex)
        {
            _WeightedLayers.FadeWeights(targetGroupIndex, fadeDuration: 0.3f);
            _previousGroupIndex = targetGroupIndex;

            Debug.Log($"切换到权重组 {targetGroupIndex}（强度: {_intensity:F2}）");
        }
    }

    int GetGroupIndexByIntensity(float intensity)
    {
        // 0.0 - 0.33: Group 0
        // 0.33 - 0.66: Group 1
        // 0.66 - 1.0: Group 2

        if (intensity < 0.33f)
            return 0;
        else if (intensity < 0.66f)
            return 1;
        else
            return 2;
    }
}
```

---

### 示例3：条件权重切换

```csharp
using Animancer;
using UnityEngine;

public class ConditionalWeightSwitchExample : MonoBehaviour
{
    [SerializeField] private WeightedMaskLayers _WeightedLayers;

    private enum CharacterState
    {
        Healthy,    // Group 0
        Injured,    // Group 1
        Critical    // Group 2
    }

    private CharacterState _currentState = CharacterState.Healthy;

    void SwitchState(CharacterState newState)
    {
        if (_currentState == newState)
            return;

        _currentState = newState;

        // 根据状态切换权重组
        int groupIndex = (int)newState;
        float fadeDuration = GetFadeDuration(_currentState, newState);

        _WeightedLayers.FadeWeights(groupIndex, fadeDuration);

        Debug.Log($"状态切换: {newState}（权重组 {groupIndex}）");
    }

    float GetFadeDuration(CharacterState from, CharacterState to)
    {
        // 根据状态转换决定淡入时长
        if (from == CharacterState.Healthy && to == CharacterState.Critical)
        {
            return 0.2f; // 快速切换（突然重伤）
        }
        else if (from == CharacterState.Critical && to == CharacterState.Healthy)
        {
            return 2.0f; // 慢速切换（逐渐康复）
        }
        else
        {
            return 0.5f; // 标准切换
        }
    }

    // 测试方法
    [ContextMenu("Injure")]
    void Injure() => SwitchState(CharacterState.Injured);

    [ContextMenu("Critical")]
    void Critical() => SwitchState(CharacterState.Critical);

    [ContextMenu("Heal")]
    void Heal() => SwitchState(CharacterState.Healthy);
}
```

---

## 最佳实践建议

### 1. **合理组织权重组**

```csharp
// ✅ 推荐：清晰的组织结构
// Group 0: Normal State（正常状态）
// Group 1: Light Effect（轻微效果）
// Group 2: Medium Effect（中等效果）
// Group 3: Heavy Effect（严重效果）
```

---

### 2. **使用渐变而不是突变**

```csharp
// ❌ 不推荐：突然切换
_WeightedLayers.SetWeights(1);

// ✅ 推荐：平滑过渡
_WeightedLayers.FadeWeights(1, fadeDuration: 0.5f);
```

---

### 3. **配合图层权重使用**

```csharp
// ✅ 推荐：同时控制图层权重和骨骼权重
void EnableUpperBodyAnimation()
{
    // 淡入图层
    _Animancer.Layers[1].StartFade(1.0f, 0.3f);

    // 同时调整骨骼权重
    _WeightedLayers.FadeWeights(groupIndex: 0, fadeDuration: 0.3f);
}
```

---

### 4. **在 Inspector 中预览权重**

在编辑器中配置权重组时：
- 使用 **Edit** 按钮打开编辑器
- 直接在编辑器中调整每个骨骼的权重
- 实时预览效果

---

## 常见问题 FAQ

### Q1: WeightedMaskLayers 和标准 AvatarMask 有什么区别？

**A**:

| 特性 | AvatarMask | WeightedMaskLayers |
|------|-----------|-------------------|
| **骨骼权重** | 0 或 1（二元） | 0.0 - 1.0（连续） |
| **淡入淡出** | ❌ | ✅ |
| **复杂度** | 简单 | 复杂 |
| **性能** | 更快 | 稍慢 |
| **叠加混合** | ✅ | ❌ |

---

### Q2: 为什么不支持叠加混合？

**A**: 这是当前版本的技术限制。官方表示如果有足够需求,可能在未来版本中添加支持。

**替代方案**：
- 使用标准的叠加图层
- 结合使用 WeightedMaskLayers（覆盖）和标准图层（叠加）

---

### Q3: 如何确定合适的权重值？

**A**: 通过实验和迭代：

```csharp
// 在 Inspector 中实时调整
[SerializeField, Range(0f, 1f)] private float _testWeight = 0.5f;

void Update()
{
    // 临时测试权重效果
    // 在编辑器中调整 _testWeight 观察效果
}
```

---

### Q4: 可以动态创建权重组吗？

**A**: 通常在 Inspector 中配置,运行时主要是切换已有的组。

如果需要运行时修改权重,建议：
- 预先配置多个权重组
- 运行时通过 `SetWeights()` 或 `FadeWeights()` 切换

---

### Q5: WeightedMaskLayers 会影响性能吗？

**A**: 有轻微的性能开销,但通常可以接受。

**优化建议**：
- 只在需要细粒度控制时使用
- 简单场景使用标准 AvatarMask
- 限制活跃的 WeightedMaskLayers 数量

---

## 总结

### 核心要点

1. **扩展功能**
   - 基于 AvatarMask 的增强版本
   - 支持 0.0-1.0 的连续权重值
   - 支持骨骼权重的淡入淡出

2. **三步设置**
   - 添加 WeightedMaskLayers 组件
   - 通过 Edit 按钮配置权重组
   - 运行时切换权重组

3. **运行时控制**
   - `SetWeights()`：立即切换
   - `FadeWeights()`：平滑过渡

4. **限制和约束**
   - 仅支持覆盖混合
   - 不支持叠加混合
   - Pro 专属功能

### 下一步学习

- 📖 深入学习 **Avatar Mask** 配置
- 🎨 探索结合 **Mixers** 的高级用法
- 📚 了解性能优化技巧
- 🔍 查看实际项目中的受伤系统实现

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/layers/weighted/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
