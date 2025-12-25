---
title: "Animancer Fading"
date: 2025-12-25
draft: false
---

# Animancer Fading 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/fading/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Fading（淡入淡出）** 是 Animancer 中实现动画平滑过渡的核心功能。通过**交叉淡入淡出（Cross-Fading）**，可以在动画之间逐渐过渡，而前一个动画同时淡出。

这对于**骨骼动画**特别有价值，允许角色在不同姿势之间平滑过渡，而**不需要**结束姿势和开始姿势完全相同。

---

## 核心概念 (Key Concept)

> **淡入淡出允许角色模型从一个动画的结束姿势平滑过渡到另一个动画的开始姿势，而不需要两个姿势完全相同。**

### 工作原理

```
时间轴示例：
|---------- Animation A (100% → 0%) ----------|
            |---------- Animation B (0% → 100%) ----------|
            ↑
        开始淡入淡出
        持续时间: 0.25秒

最终输出 = A的权重 × A的姿势 + B的权重 × B的姿势
```

**关键特性**：
- ✅ 平滑的姿势插值
- ✅ 避免动画切换时的跳跃
- ✅ 自动权重管理
- ❌ 不适用于精灵动画（Sprite Animation）

---

## 适用范围 (Applicability)

### ✅ 支持：骨骼动画 (Skeletal Animation)

```csharp
// 骨骼动画可以完美混合
_Animancer.Play(_IdleClip, fadeDuration: 0.25f);
_Animancer.Play(_WalkClip, fadeDuration: 0.25f); // 平滑过渡
```

**原因**：骨骼动画基于骨骼变换（Transform），可以在任意姿势之间插值。

---

### ❌ 不支持：精灵动画 (Sprite Animation)

```csharp
// 精灵动画无法混合
// Sprite A 和 Sprite B 无法"插值"
```

**原因**：精灵动画是离散的图像序列，不能在两个不同的 Sprite 之间进行插值混合。

---

## 淡入持续时间 (Fade Durations)

### 1. **默认淡入时长**

```csharp
// 使用默认淡入时长（0.25 秒）
_Animancer.Play(clip, AnimancerGraph.DefaultFadeDuration);

// 等价于
_Animancer.Play(clip, 0.25f);
```

**配置默认值**：
```csharp
// 修改全局默认值
AnimancerGraph.DefaultFadeDuration = 0.3f; // 改为 0.3 秒
```

---

### 2. **自定义淡入时长**

```csharp
// 快速淡入（0.1 秒）- 用于快速反应动作
_Animancer.Play(hitClip, 0.1f);

// 标准淡入（0.25 秒）- 通用过渡
_Animancer.Play(walkClip, 0.25f);

// 慢速淡入（0.8 秒）- 缓慢平滑过渡
_Animancer.Play(restClip, 0.8f);
```

**推荐时长参考**：

| 场景 | 推荐时长 | 说明 |
|------|---------|------|
| 受击/死亡 | 0.05 - 0.1s | 需要立即反馈 |
| 移动切换 | 0.2 - 0.3s | 标准平滑过渡 |
| 姿态变化 | 0.3 - 0.5s | 需要更平滑的效果 |
| 休息/睡眠 | 0.5 - 1.0s | 缓慢自然过渡 |

---

### 3. **归一化到新动画时长**

```csharp
// 淡入时长 = 新动画时长的 20%
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);

// 示例：
// 新动画时长 = 2 秒
// 实际淡入时长 = 2 × 0.2 = 0.4 秒
```

**用途**：
- 根据动画长度自动调整淡入时长
- 短动画使用短淡入，长动画使用长淡入
- 保持视觉上的一致性

---

### 4. **相对于前一个动画时长**

```csharp
// 淡入时长 = 前一个动画时长的 10%
float fadeDuration = _Animancer.States.Current.Length * 0.1f;
_Animancer.Play(clip, fadeDuration);

// 示例：
// 当前动画时长 = 3 秒
// 淡入时长 = 3 × 0.1 = 0.3 秒
```

**用途**：
- 根据当前播放的动画调整过渡速度
- 从长动画过渡时使用更长的淡入
- 动态适应不同场景

---

## 授权说明 (Licensing Note)

> ⚠️ **重要**：自定义淡入持续时间是 **Animancer Pro** 的专属功能。

### Animancer Lite 限制

```csharp
// ✅ Lite 版本在编辑器中可以使用自定义时长
_Animancer.Play(clip, 0.5f); // 编辑器中有效

// ❌ Lite 版本在运行时构建（Build）中强制使用默认值
_Animancer.Play(clip, 0.5f); // 运行时会变成 0.25f
```

### Animancer Pro 完整功能

```csharp
// ✅ Pro 版本在编辑器和运行时都支持自定义时长
_Animancer.Play(clip, 0.8f); // 编辑器和运行时都是 0.8 秒
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed); // 完全支持
```

**版本对比**：

| 功能 | Animancer Lite | Animancer Pro |
|------|---------------|---------------|
| 默认淡入（0.25s） | ✅ | ✅ |
| 自定义淡入（编辑器） | ✅ | ✅ |
| 自定义淡入（运行时） | ❌ | ✅ |
| FadeMode 参数 | ❌ | ✅ |

---

## 独立淡入淡出 (Individual Fading)

**`AnimancerNode.StartFade` 方法**允许独立控制单个状态或图层的淡入淡出，这在游戏中的图层管理非常有用。

### 基础用法

```csharp
// 获取特定状态
AnimancerState state = _Animancer.States.GetOrCreate(clip);

// 手动启动淡入
state.StartFade(targetWeight: 1.0f, fadeDuration: 0.5f);

// 手动启动淡出
state.StartFade(targetWeight: 0.0f, fadeDuration: 0.5f);
```

---

### 实际应用场景

#### 场景1：图层独立淡入淡出

```csharp
public class LayerFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _UpperBodyAim;

    void StartAiming()
    {
        // 上半身图层淡入瞄准动画
        var aimState = _Animancer.Layers[1].Play(_UpperBodyAim);
        aimState.StartFade(targetWeight: 1.0f, fadeDuration: 0.3f);
    }

    void StopAiming()
    {
        // 上半身图层淡出瞄准动画
        var aimState = _Animancer.Layers[1].CurrentState;
        aimState.StartFade(targetWeight: 0.0f, fadeDuration: 0.3f);
    }
}
```

---

#### 场景2：动态权重控制

```csharp
public class DynamicWeightExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _InjuredWalk;

    private AnimancerState _InjuredState;

    void Start()
    {
        _InjuredState = _Animancer.States.GetOrCreate(_InjuredWalk);
    }

    void Update()
    {
        float healthPercent = GetHealthPercent();

        // 根据血量动态调整受伤动画权重
        if (healthPercent < 0.3f)
        {
            // 血量低于 30%，淡入受伤动画
            _InjuredState.StartFade(targetWeight: 1.0f - healthPercent, fadeDuration: 0.5f);
        }
        else
        {
            // 血量高于 30%，淡出受伤动画
            _InjuredState.StartFade(targetWeight: 0.0f, fadeDuration: 0.5f);
        }
    }

    float GetHealthPercent()
    {
        // 返回 0-1 的血量百分比
        return 0.5f; // 示例值
    }
}
```

---

#### 场景3：环境效果叠加

```csharp
public class EnvironmentEffectExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private ClipTransition _ShiverAnimation; // 发抖动画

    private AnimancerState _ShiverState;

    void Start()
    {
        _ShiverState = _Animancer.States.GetOrCreate(_ShiverAnimation);
    }

    void OnEnterColdArea()
    {
        // 进入寒冷区域，淡入发抖动画
        _ShiverState.StartFade(targetWeight: 0.5f, fadeDuration: 2.0f);
    }

    void OnExitColdArea()
    {
        // 离开寒冷区域，淡出发抖动画
        _ShiverState.StartFade(targetWeight: 0.0f, fadeDuration: 2.0f);
    }
}
```

---

## 淡入淡出模式 (Fade Modes)

Animancer 支持多种淡入淡出模式，提供不同的时长解释方式。

### 常用模式

```csharp
// 1. 固定时长（默认）
_Animancer.Play(clip, 0.25f);

// 2. 归一化到速度（Normalized Speed）
_Animancer.Play(clip, 0.2f, FadeMode.NormalizedSpeed);
// 淡入时长 = 新动画时长 × 0.2

// 3. 归一化到持续时间（Normalized Duration）
_Animancer.Play(clip, 0.1f, FadeMode.NormalizedDuration);
// 淡入时长 = 新动画时长 × 0.1 / 速度
```

**详细说明**请参考：**Fade Modes** 专题文档

---

## 自定义缓动 (Custom Easing)

Animancer 允许使用非线性插值替代默认的线性淡入淡出。

### 缓动曲线示例

```csharp
// 使用 AnimationCurve 自定义缓动
AnimationCurve easeCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

AnimancerState state = _Animancer.Play(clip);
state.StartFade(
    targetWeight: 1.0f,
    fadeDuration: 0.5f,
    easingFunction: easeCurve.Evaluate
);
```

**常见缓动类型**：
- **Ease In**：慢启动，快结束
- **Ease Out**：快启动，慢结束
- **Ease In-Out**：慢启动，慢结束

**详细说明**请参考：**Custom Easing** 专题文档

---

## 淡入淡出序列 (Sequences)

**Sequences（序列）** 允许将多个动画作为统一的状态播放，支持复杂的动画组合。

### 基础序列示例

```csharp
// 创建序列：攻击动画 1 → 攻击动画 2 → 攻击动画 3
ClipTransitionSequence attackCombo = new ClipTransitionSequence
{
    new ClipTransition { Clip = attack1Clip },
    new ClipTransition { Clip = attack2Clip },
    new ClipTransition { Clip = attack3Clip }
};

// 播放整个序列
_Animancer.Play(attackCombo);
```

**详细说明**请参考：**Sequences** 专题文档

---

## 代码示例集合

### 示例1：基础淡入淡出

```csharp
using Animancer;
using UnityEngine;

public class BasicFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.W))
        {
            // 0.25 秒淡入到 Walk
            _Animancer.Play(_WalkClip, fadeDuration: 0.25f);
        }
        else if (Input.GetKeyDown(KeyCode.S))
        {
            // 0.25 秒淡入到 Idle
            _Animancer.Play(_IdleClip, fadeDuration: 0.25f);
        }
    }
}
```

---

### 示例2：动态淡入时长

```csharp
using Animancer;
using UnityEngine;

public class DynamicFadeDurationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _RunClip;

    void PlayWithDynamicFade()
    {
        // 根据当前动画的长度动态调整淡入时长
        float currentLength = _Animancer.States.Current?.Length ?? 1.0f;
        float fadeDuration = currentLength * 0.15f; // 当前动画长度的 15%

        _Animancer.Play(_RunClip, fadeDuration);

        Debug.Log($"淡入时长: {fadeDuration} 秒");
    }
}
```

---

### 示例3：条件性淡入

```csharp
using Animancer;
using UnityEngine;

public class ConditionalFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _CombatIdleClip;
    [SerializeField] private AnimationClip _RelaxedIdleClip;

    private bool _isInCombat = false;

    void SwitchCombatState(bool inCombat)
    {
        _isInCombat = inCombat;

        if (_isInCombat)
        {
            // 进入战斗：快速切换（0.1 秒）
            _Animancer.Play(_CombatIdleClip, fadeDuration: 0.1f);
        }
        else
        {
            // 退出战斗：慢速放松（0.8 秒）
            _Animancer.Play(_RelaxedIdleClip, fadeDuration: 0.8f);
        }
    }
}
```

---

### 示例4：图层独立淡入淡出

```csharp
using Animancer;
using UnityEngine;

public class LayerIndependentFadingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _AimClip;
    [SerializeField] private AnimationClip _ReloadClip;

    void Start()
    {
        // 确保有两个图层
        _Animancer.Layers.SetCount(2);

        // 设置 Layer 1 的初始权重
        _Animancer.Layers[1].Weight = 0;
    }

    void StartAiming()
    {
        // Layer 1 淡入瞄准动画
        var aimState = _Animancer.Layers[1].Play(_AimClip);
        aimState.StartFade(targetWeight: 1.0f, fadeDuration: 0.3f);

        // 同时淡入图层本身
        _Animancer.Layers[1].StartFade(targetWeight: 1.0f, fadeDuration: 0.3f);
    }

    void StopAiming()
    {
        // Layer 1 淡出
        _Animancer.Layers[1].StartFade(targetWeight: 0.0f, fadeDuration: 0.3f);
    }

    void Reload()
    {
        // 在 Layer 1 播放装填动画（替换瞄准）
        _Animancer.Layers[1].Play(_ReloadClip, fadeDuration: 0.2f);
    }
}
```

---

### 示例5：健康状态权重控制

```csharp
using Animancer;
using UnityEngine;

public class HealthBasedAnimationExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _NormalWalkClip;
    [SerializeField] private AnimationClip _InjuredWalkClip;

    private AnimancerState _NormalWalkState;
    private AnimancerState _InjuredWalkState;

    [SerializeField] private float _currentHealth = 100f;
    [SerializeField] private float _maxHealth = 100f;

    void Start()
    {
        _NormalWalkState = _Animancer.States.GetOrCreate(_NormalWalkClip);
        _InjuredWalkState = _Animancer.States.GetOrCreate(_InjuredWalkClip);

        // 开始时播放正常行走
        _NormalWalkState.Play();
        _NormalWalkState.Weight = 1.0f;
        _InjuredWalkState.Weight = 0.0f;
    }

    void Update()
    {
        UpdateAnimationWeights();
    }

    void UpdateAnimationWeights()
    {
        float healthPercent = _currentHealth / _maxHealth;

        // 根据血量动态调整权重
        float normalWeight = healthPercent;
        float injuredWeight = 1.0f - healthPercent;

        // 平滑过渡
        _NormalWalkState.StartFade(normalWeight, fadeDuration: 0.5f);
        _InjuredWalkState.StartFade(injuredWeight, fadeDuration: 0.5f);
    }

    // 测试方法
    [ContextMenu("Damage")]
    void TakeDamage()
    {
        _currentHealth = Mathf.Max(0, _currentHealth - 20);
    }

    [ContextMenu("Heal")]
    void Heal()
    {
        _currentHealth = Mathf.Min(_maxHealth, _currentHealth + 20);
    }
}
```

---

## 最佳实践建议

### 1. **选择合适的淡入时长**

```csharp
// ❌ 不推荐：所有动画使用相同的淡入时长
_Animancer.Play(anyClip, 0.25f);

// ✅ 推荐：根据动画类型选择合适的时长
float fadeDuration = GetAppropriateFadeDuration(clipType);
_Animancer.Play(clip, fadeDuration);

float GetApproppriateFadeDuration(AnimationType type)
{
    switch (type)
    {
        case AnimationType.Hit:
            return 0.05f;  // 快速反应
        case AnimationType.Movement:
            return 0.25f;  // 标准过渡
        case AnimationType.Idle:
            return 0.5f;   // 慢速放松
        default:
            return 0.25f;
    }
}
```

---

### 2. **避免过短的淡入时长**

```csharp
// ❌ 不推荐：淡入时长过短可能导致抖动
_Animancer.Play(clip, 0.01f); // 过短

// ✅ 推荐：至少 0.05 秒（除非特殊需求）
_Animancer.Play(clip, 0.1f); // 合适
```

**经验法则**：
- 最小值：0.05 秒（快速反应）
- 标准值：0.2 - 0.3 秒（通用）
- 最大值：1.0 秒（缓慢过渡）

---

### 3. **图层淡入淡出注意事项**

```csharp
// ✅ 正确：同时淡入状态和图层
void StartUpperBodyAction()
{
    var state = _Animancer.Layers[1].Play(_ActionClip);
    state.StartFade(1.0f, 0.3f);           // 淡入状态
    _Animancer.Layers[1].StartFade(1.0f, 0.3f); // 淡入图层
}

// ❌ 错误：只淡入状态，图层权重为 0
void WrongApproach()
{
    var state = _Animancer.Layers[1].Play(_ActionClip);
    state.StartFade(1.0f, 0.3f);
    // 图层权重仍然是 0，动画不会显示
}
```

---

### 4. **性能优化**

```csharp
// ✅ 及时停止不需要的状态
void OnFadeOutComplete(AnimancerState state)
{
    if (state.Weight <= 0.01f)
    {
        state.Stop(); // 停止播放，节省性能
    }
}

// ✅ 监听淡入淡出完成事件
state.Events.OnEnd = () =>
{
    Debug.Log("淡入淡出完成");
    state.Stop();
};
```

---

## 常见问题 FAQ

### Q1: 淡入淡出和直接切换有什么区别?

**A**:
- **直接切换**：
  ```csharp
  _Animancer.Play(clip, fadeDuration: 0); // 立即切换
  ```
  - 优点：响应速度快
  - 缺点：可能出现动作跳跃

- **淡入淡出**：
  ```csharp
  _Animancer.Play(clip, fadeDuration: 0.25f); // 平滑过渡
  ```
  - 优点：视觉平滑，无跳跃
  - 缺点：有轻微延迟

---

### Q2: 为什么精灵动画不支持淡入淡出?

**A**: 精灵动画是**离散的图像序列**，两个不同的 Sprite 无法进行像素级插值混合。

```
Sprite A: 😊  +  Sprite B: 😢  ≠  可混合的结果
```

骨骼动画基于**骨骼变换矩阵**，可以在任意姿势之间插值。

---

### Q3: Animancer Lite 和 Pro 在淡入淡出上有什么区别?

**A**:

| 功能 | Lite | Pro |
|------|------|-----|
| 默认淡入（0.25s） | ✅ | ✅ |
| 自定义淡入（编辑器） | ✅ | ✅ |
| 自定义淡入（运行时） | ❌ | ✅ |
| FadeMode | ❌ | ✅ |
| 自定义缓动 | ❌ | ✅ |

---

### Q4: 如何确定合适的淡入时长?

**A**: 使用以下方法测试：

```csharp
[SerializeField, Range(0f, 1f)] private float _testFadeDuration = 0.25f;

void Update()
{
    if (Input.GetKeyDown(KeyCode.Space))
    {
        _Animancer.Play(testClip, _testFadeDuration);
        Debug.Log($"Testing fade duration: {_testFadeDuration}");
    }
}
```

在 Inspector 中拖动滑块，实时测试不同的淡入时长。

---

### Q5: 淡入淡出会影响性能吗?

**A**:
- **轻微影响**：淡入淡出期间会同时播放两个动画
- **优化建议**：
  ```csharp
  // ✅ 淡入淡出完成后及时停止旧动画
  oldState.Events.OnEnd = () => oldState.Stop();
  ```

---

### Q6: 如何实现图层的独立淡入淡出?

**A**:

```csharp
// 方法1：使用 StartFade
_Animancer.Layers[1].StartFade(targetWeight: 1.0f, fadeDuration: 0.5f);

// 方法2：手动调整权重
void Update()
{
    _Animancer.Layers[1].Weight = Mathf.Lerp(
        _Animancer.Layers[1].Weight,
        targetWeight,
        Time.deltaTime / fadeDuration
    );
}
```

---

## 相关文档主题 (Related Documentation Topics)

### 1. **Fade Modes（淡入模式）**
- 不同的时长解释方式
- Normalized Speed vs Normalized Duration
- 自定义模式

### 2. **Custom Easing（自定义缓动）**
- 非线性插值
- AnimationCurve 应用
- 常见缓动函数

### 3. **Sequences（序列）**
- 多动画组合播放
- 序列创建和管理
- 复杂动画链

---

## 总结

### 核心要点

1. **淡入淡出的本质**
   - 权重从 0 → 1 的平滑过渡
   - 旧动画从 1 → 0 的平滑过渡
   - 两者同时进行，产生混合效果

2. **淡入时长选择**
   - 默认：0.25 秒
   - 快速：0.05 - 0.1 秒
   - 标准：0.2 - 0.3 秒
   - 慢速：0.5 - 1.0 秒

3. **适用范围**
   - ✅ 骨骼动画
   - ❌ 精灵动画

4. **高级功能**
   - Pro 版本支持自定义时长和模式
   - 独立淡入淡出（StartFade）
   - 自定义缓动曲线

### 下一步学习

- 📖 深入学习 **Fade Modes** 的不同模式
- 🎨 探索 **Custom Easing** 实现非线性过渡
- 📚 了解 **Sequences** 组合复杂动画
- 🔍 查看实际项目中的应用案例

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/fading/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
