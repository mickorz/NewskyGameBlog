---
title: "Animancer Custom Fading"
date: 2025-12-25
draft: false
---

# Animancer Custom Fading 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/blending/fading/custom/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Custom Easing（自定义缓动）** 是 Animancer 的高级功能，允许开发者修改淡入淡出动画，使其超越默认的线性渐变。系统使用标准缓动函数或自定义委托来控制动画权重的过渡方式。

> ⚠️ **重要**：这是 **Animancer Pro 专属功能**

---

## 核心概念 (Core Concept)

### 默认线性淡入淡出

默认情况下，交叉淡入淡出会以**恒定速度**将 `AnimancerNode.Weight` 移动到 `AnimancerNode.TargetWeight`。

```
线性淡入淡出（默认）:
Weight
  1.0 ┤           ╱
      │         ╱
      │       ╱
      │     ╱
  0.0 ┤───╱─────────> Time
      0            1
      匀速上升
```

**公式**：
```csharp
Weight = Mathf.Lerp(startWeight, targetWeight, t);
// t = 线性时间进度（0-1）
```

---

### 自定义缓动淡入淡出

自定义缓动通过数学曲线控制这个过渡过程，实现更平滑的过渡效果。

```
缓动淡入淡出（例如 EaseInOut）:
Weight
  1.0 ┤        ╱──
      │      ╱
      │    ╱
      │  ╱
  0.0 ┤─╱────────────> Time
      0            1
      慢-快-慢
```

**公式**：
```csharp
Weight = Mathf.Lerp(startWeight, targetWeight, easingFunction(t));
// easingFunction(t) = 应用缓动曲线后的时间进度
```

---

## 实现方法 (Implementation Methods)

### 方法1：使用自定义委托

**定义**：直接传递一个 `Func<float, float>` 委托函数。

**代码示例**：
```csharp
// 平方缓动（加速）
state.FadeGroup.SetEasing(t => t * t);

// 立方缓动（更快加速）
state.FadeGroup.SetEasing(t => t * t * t);

// 平方根缓动（减速）
state.FadeGroup.SetEasing(t => Mathf.Sqrt(t));

// 自定义复杂曲线
state.FadeGroup.SetEasing(t => {
    if (t < 0.5f)
        return 2 * t * t; // 前半段加速
    else
        return 1 - 2 * (1 - t) * (1 - t); // 后半段减速
});
```

**参数说明**：
- `t`：淡入淡出的标准化时间进度（0-1）
- 返回值：经过缓动处理的进度值（通常也是 0-1）

---

### 方法2：使用标准缓动类

**定义**：Animancer 提供了 `Easing` 类，包含多种标准数学曲线函数。

**代码示例**：
```csharp
// Sine 曲线（InOut 模式）
state.FadeGroup.SetEasing(Easing.Sine.InOut);

// Quad 二次曲线（In 模式）
state.FadeGroup.SetEasing(Easing.Quad.In);

// Cubic 三次曲线（Out 模式）
state.FadeGroup.SetEasing(Easing.Cubic.Out);

// Elastic 弹性曲线
state.FadeGroup.SetEasing(Easing.Elastic.InOut);

// Back 回弹曲线
state.FadeGroup.SetEasing(Easing.Back.InOut);

// Bounce 反弹曲线
state.FadeGroup.SetEasing(Easing.Bounce.Out);
```

**常用缓动类型**：

| 缓动类型 | In | Out | InOut | 特性 |
|---------|----|----|-------|------|
| **Sine** | ✅ | ✅ | ✅ | 平滑正弦曲线 |
| **Quad** | ✅ | ✅ | ✅ | 二次方（x²） |
| **Cubic** | ✅ | ✅ | ✅ | 三次方（x³） |
| **Quart** | ✅ | ✅ | ✅ | 四次方（x⁴） |
| **Quint** | ✅ | ✅ | ✅ | 五次方（x⁵） |
| **Expo** | ✅ | ✅ | ✅ | 指数曲线 |
| **Circ** | ✅ | ✅ | ✅ | 圆形曲线 |
| **Back** | ✅ | ✅ | ✅ | 回弹效果 |
| **Elastic** | ✅ | ✅ | ✅ | 弹性效果 |
| **Bounce** | ✅ | ✅ | ✅ | 反弹效果 |

---

### 方法3：使用缓动函数枚举

**定义**：通过 `Easing.Function` 枚举选择缓动类型。

**代码示例**：
```csharp
// 使用枚举
state.FadeGroup.SetEasing(Easing.Function.SineInOut);
state.FadeGroup.SetEasing(Easing.Function.QuadIn);
state.FadeGroup.SetEasing(Easing.Function.CubicOut);
state.FadeGroup.SetEasing(Easing.Function.ElasticInOut);
```

**动态选择示例**：
```csharp
public class DynamicEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;
    [SerializeField] private Easing.Function _EasingType = Easing.Function.SineInOut;

    void PlayWithEasing()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);
        state.FadeGroup.SetEasing(_EasingType);
    }
}
```

---

### 方法4：使用 AnimationCurve

**定义**：通过 Unity 的 `AnimationCurve` 在 Inspector 中手动配置缓动曲线。

**代码示例**：
```csharp
using Animancer;
using UnityEngine;

public class AnimationCurveEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    // 在 Inspector 中可视化配置的曲线
    [SerializeField] private AnimationCurve _FadeCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

    void PlayWithCustomCurve()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);

        // 使用曲线的 Evaluate 方法作为缓动函数
        state.FadeGroup.SetEasing(_FadeCurve.Evaluate);
    }
}
```

**Inspector 配置**：
```
Inspector:
┌─────────────────────────────────┐
│ Fade Curve                      │
│ ┌───────────────────────────┐   │
│ │    ╱─────                 │   │
│ │  ╱                        │   │
│ │╱                          │   │
│ └───────────────────────────┘   │
│ 可以通过点击编辑关键帧          │
└─────────────────────────────────┘
```

**内置曲线预设**：
```csharp
// Unity 提供的内置曲线
AnimationCurve.EaseInOut(0, 0, 1, 1);  // 慢-快-慢
AnimationCurve.Linear(0, 0, 1, 1);     // 线性
AnimationCurve.Constant(0, 1, 0.5f);   // 恒定值
```

---

## 缓动曲线详解 (Easing Curve Details)

### In / Out / InOut 模式

**In（缓入）**：
- 开始慢，结束快
- 适合：物体加速进入

```
In 模式:
  1.0 ┤          ╱
      │        ╱
      │     ╱
      │  ╱
  0.0 ┤─╱──────────> Time
      慢启动，快结束
```

---

**Out（缓出）**：
- 开始快，结束慢
- 适合：物体减速停止

```
Out 模式:
  1.0 ┤───╱
      │  ╱
      │ ╱
      │╱
  0.0 ┤─────────────> Time
      快启动，慢结束
```

---

**InOut（缓入缓出）**：
- 开始慢，中间快，结束慢
- 适合：平滑自然过渡

```
InOut 模式:
  1.0 ┤      ╱──
      │    ╱
      │  ╱
      │╱
  0.0 ┤──────────────> Time
      慢-快-慢
```

---

### 常用缓动类型对比

#### 1. **Sine（正弦曲线）**

```csharp
state.FadeGroup.SetEasing(Easing.Sine.InOut);
```

**特性**：
- 最平滑的曲线
- 自然的加速/减速
- 推荐用于大多数场景

**公式**：
```csharp
// Sine InOut
float SineInOut(float t)
{
    return -(Mathf.Cos(Mathf.PI * t) - 1) / 2;
}
```

---

#### 2. **Quad（二次曲线）**

```csharp
state.FadeGroup.SetEasing(Easing.Quad.In);   // t²
state.FadeGroup.SetEasing(Easing.Quad.Out);  // 1 - (1-t)²
```

**特性**：
- 适度的加速效果
- 比线性平滑，比三次方缓和

**公式**：
```csharp
// Quad In
float QuadIn(float t)
{
    return t * t;
}
```

---

#### 3. **Elastic（弹性曲线）**

```csharp
state.FadeGroup.SetEasing(Easing.Elastic.Out);
```

**特性**：
- 有弹性效果
- 会超出目标值再回弹
- 适合：弹簧效果、卡通风格

**效果**：
```
Elastic Out:
  1.0 ┤─╱╲─╱─
      │╱  ╲╱
      │
  0.0 ┤───────────> Time
      超出后回弹
```

---

#### 4. **Back（回弹曲线）**

```csharp
state.FadeGroup.SetEasing(Easing.Back.InOut);
```

**特性**：
- 轻微回弹效果
- 比 Elastic 温和
- 适合：UI 动画、按钮效果

---

#### 5. **Bounce（反弹曲线）**

```csharp
state.FadeGroup.SetEasing(Easing.Bounce.Out);
```

**特性**：
- 模拟物理反弹
- 多次小幅震荡
- 适合：着陆动画、掉落效果

---

## 曲线预设 (Curve Presets)

Animancer 提供可下载的曲线预设文件，用于 `AnimationCurve` 配置。

**使用方法**：
1. 下载官方预设文件
2. 在 Inspector 中加载预设
3. 微调关键帧

**优势**：
- ✅ 手动配置的高效曲线
- ✅ 最小化关键帧数量
- ⚠️ 可能与 `Easing` 类不完全匹配

**注意**：
- 预设文件是手动配置的近似曲线
- 为了效率使用最少的关键帧
- 如果需要精确曲线，建议使用 `Easing` 类

---

## 代码示例集合

### 示例1：基础自定义缓动

```csharp
using Animancer;
using UnityEngine;

public class BasicCustomEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleClip;
    [SerializeField] private AnimationClip _WalkClip;

    void SwitchToWalkWithEasing()
    {
        // 播放动画并应用缓动
        var state = _Animancer.Play(_WalkClip, fadeDuration: 0.5f);

        // 使用 Sine InOut 曲线（平滑过渡）
        state.FadeGroup.SetEasing(Easing.Sine.InOut);
    }
}
```

---

### 示例2：对比不同缓动效果

```csharp
using Animancer;
using UnityEngine;

public class EasingComparisonExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    [ContextMenu("Test Linear")]
    void TestLinear()
    {
        // 默认线性（无缓动）
        _Animancer.Play(_Clip, fadeDuration: 1.0f);
        Debug.Log("线性淡入");
    }

    [ContextMenu("Test Sine InOut")]
    void TestSineInOut()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 1.0f);
        state.FadeGroup.SetEasing(Easing.Sine.InOut);
        Debug.Log("Sine InOut 淡入（慢-快-慢）");
    }

    [ContextMenu("Test Quad In")]
    void TestQuadIn()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 1.0f);
        state.FadeGroup.SetEasing(Easing.Quad.In);
        Debug.Log("Quad In 淡入（加速）");
    }

    [ContextMenu("Test Elastic Out")]
    void TestElasticOut()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 1.0f);
        state.FadeGroup.SetEasing(Easing.Elastic.Out);
        Debug.Log("Elastic Out 淡入（弹性效果）");
    }
}
```

---

### 示例3：AnimationCurve 可视化配置

```csharp
using Animancer;
using UnityEngine;

public class AnimationCurveEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    // 在 Inspector 中可视化编辑
    [SerializeField] private AnimationCurve _CustomFadeCurve = new AnimationCurve(
        new Keyframe(0, 0, 0, 2),
        new Keyframe(1, 1, 2, 0)
    );

    void PlayWithCustomCurve()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);
        state.FadeGroup.SetEasing(_CustomFadeCurve.Evaluate);

        Debug.Log("使用自定义 AnimationCurve 淡入");
    }
}
```

---

### 示例4：基于场景选择缓动

```csharp
using Animancer;
using UnityEngine;

public class ContextBasedEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    public enum TransitionType
    {
        Smooth,      // 平滑过渡
        Quick,       // 快速过渡
        Energetic,   // 有活力的过渡
        Bouncy       // 弹性过渡
    }

    void PlayWithEasing(AnimationClip clip, TransitionType type)
    {
        float fadeDuration = GetFadeDuration(type);
        var state = _Animancer.Play(clip, fadeDuration);

        // 根据类型选择缓动
        switch (type)
        {
            case TransitionType.Smooth:
                state.FadeGroup.SetEasing(Easing.Sine.InOut);
                break;

            case TransitionType.Quick:
                state.FadeGroup.SetEasing(Easing.Quad.In);
                break;

            case TransitionType.Energetic:
                state.FadeGroup.SetEasing(Easing.Back.Out);
                break;

            case TransitionType.Bouncy:
                state.FadeGroup.SetEasing(Easing.Bounce.Out);
                break;
        }

        Debug.Log($"应用 {type} 缓动");
    }

    float GetFadeDuration(TransitionType type)
    {
        switch (type)
        {
            case TransitionType.Quick: return 0.15f;
            case TransitionType.Smooth: return 0.3f;
            case TransitionType.Energetic: return 0.25f;
            case TransitionType.Bouncy: return 0.4f;
            default: return 0.25f;
        }
    }
}
```

---

### 示例5：自定义数学曲线

```csharp
using Animancer;
using UnityEngine;

public class CustomMathEasingExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _Clip;

    void PlayWithCustomMath()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);

        // 自定义缓动：慢-快-慢（自定义曲线）
        state.FadeGroup.SetEasing(t =>
        {
            if (t < 0.5f)
            {
                // 前半段：二次加速
                return 2 * t * t;
            }
            else
            {
                // 后半段：二次减速
                float adjusted = 1 - t;
                return 1 - 2 * adjusted * adjusted;
            }
        });
    }

    void PlayWithSmoothStep()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);

        // 使用 Unity 的 SmoothStep
        state.FadeGroup.SetEasing(t => Mathf.SmoothStep(0, 1, t));
    }

    void PlayWithCustomBounce()
    {
        var state = _Animancer.Play(_Clip, fadeDuration: 0.5f);

        // 自定义反弹效果
        state.FadeGroup.SetEasing(t =>
        {
            float bounce = Mathf.Abs(Mathf.Sin(t * Mathf.PI * 3));
            return Mathf.Lerp(t, 1, bounce * 0.2f);
        });
    }
}
```

---

### 示例6：3D Game Kit 平滑待机过渡

**场景**：在 3D Game Kit 示例中，用于平滑不同待机动画之间的过渡。

```csharp
using Animancer;
using UnityEngine;

public class SmoothIdleTransitionExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationClip _IdleNormal;
    [SerializeField] private AnimationClip _IdleBored;
    [SerializeField] private AnimationClip _IdleTired;

    private float _idleTimer = 0f;
    private int _currentIdleIndex = 0;

    void Update()
    {
        _idleTimer += Time.deltaTime;

        // 每 5 秒切换一次待机动画
        if (_idleTimer >= 5.0f)
        {
            _idleTimer = 0f;
            SwitchToNextIdle();
        }
    }

    void SwitchToNextIdle()
    {
        _currentIdleIndex = (_currentIdleIndex + 1) % 3;

        AnimationClip targetIdle = GetIdleClip(_currentIdleIndex);
        var state = _Animancer.Play(targetIdle, fadeDuration: 0.5f);

        // 使用 Sine InOut 实现平滑过渡
        state.FadeGroup.SetEasing(Easing.Sine.InOut);

        Debug.Log($"切换到待机动画 {_currentIdleIndex}");
    }

    AnimationClip GetIdleClip(int index)
    {
        switch (index)
        {
            case 0: return _IdleNormal;
            case 1: return _IdleBored;
            case 2: return _IdleTired;
            default: return _IdleNormal;
        }
    }
}
```

---

## 最佳实践建议

### 1. **选择合适的缓动类型**

```csharp
// ✅ 推荐：根据动画类型选择缓动
void PlayAnimationWithAppropriatEasing(AnimationClip clip, AnimationType type)
{
    var state = _Animancer.Play(clip, 0.3f);

    switch (type)
    {
        case AnimationType.Idle:
            // 待机：平滑过渡
            state.FadeGroup.SetEasing(Easing.Sine.InOut);
            break;

        case AnimationType.Attack:
            // 攻击：快速启动
            state.FadeGroup.SetEasing(Easing.Quad.In);
            break;

        case AnimationType.Hit:
            // 受击：立即反应，无缓动
            // 不设置缓动，保持线性
            break;

        case AnimationType.UI:
            // UI：轻微回弹
            state.FadeGroup.SetEasing(Easing.Back.Out);
            break;
    }
}
```

---

### 2. **避免过度使用复杂缓动**

```csharp
// ❌ 不推荐：所有动画都使用弹性效果
state.FadeGroup.SetEasing(Easing.Elastic.InOut); // 过于夸张

// ✅ 推荐：大多数使用 Sine，特殊场景使用复杂缓动
state.FadeGroup.SetEasing(Easing.Sine.InOut); // 通用平滑
```

---

### 3. **性能考虑**

```csharp
// ✅ 简单数学函数性能更好
state.FadeGroup.SetEasing(t => t * t); // 简单快速

// ⚠️ 复杂计算可能影响性能
state.FadeGroup.SetEasing(t => {
    // 复杂的三角函数计算
    return Mathf.Sin(t * Mathf.PI * 10) * Mathf.Cos(t * Mathf.PI * 5);
}); // 避免过度复杂
```

---

### 4. **AnimationCurve 优化**

```csharp
// ✅ 推荐：最小化关键帧数量
AnimationCurve efficientCurve = new AnimationCurve(
    new Keyframe(0, 0),
    new Keyframe(1, 1)
); // 只有 2 个关键帧

// ❌ 避免：过多关键帧
AnimationCurve complexCurve = new AnimationCurve(
    // 100 个关键帧...
); // 影响性能
```

---

### 5. **调试和可视化**

```csharp
// ✅ 使用 Inspector 测试不同曲线
[SerializeField] private Easing.Function _TestEasingType = Easing.Function.SineInOut;

void TestEasing()
{
    var state = _Animancer.Play(_Clip, 1.0f);
    state.FadeGroup.SetEasing(_TestEasingType);

    // 在运行时调整 Inspector 中的枚举值，实时查看效果
}
```

---

## 常见问题 FAQ

### Q1: 什么时候应该使用自定义缓动？

**A**:
- ✅ 需要更平滑的过渡效果
- ✅ UI 动画需要特殊效果（回弹、弹性）
- ✅ 待机动画之间的切换
- ❌ 快速反应动作（受击、死亡）- 使用线性

---

### Q2: Sine InOut 和 Quad InOut 有什么区别？

**A**:

| 特性 | Sine InOut | Quad InOut |
|------|-----------|------------|
| **平滑度** | 非常平滑 | 适度平滑 |
| **性能** | 稍慢（三角函数） | 更快（简单乘法） |
| **视觉效果** | 更自然 | 稍微明显 |

**推荐**：
- 通用场景：`Sine.InOut`
- 性能敏感：`Quad.InOut`

---

### Q3: 如何在 Inspector 中预览缓动曲线？

**A**: 使用 `AnimationCurve`：

```csharp
[SerializeField] private AnimationCurve _PreviewCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

void ApplyPreview()
{
    state.FadeGroup.SetEasing(_PreviewCurve.Evaluate);
}
```

在 Inspector 中可以直接看到曲线形状并编辑。

---

### Q4: Custom Easing 是 Pro 专属功能吗？

**A**: 是的。

| 功能 | Animancer Lite | Animancer Pro |
|------|---------------|---------------|
| 线性淡入淡出 | ✅ | ✅ |
| 自定义缓动 | ❌ | ✅ |
| `SetEasing` 方法 | ❌ | ✅ |

---

### Q5: 可以对 Mixer 使用自定义缓动吗？

**A**: 可以！

```csharp
var mixerState = _Animancer.Play(_MixerTransition, 0.5f);
mixerState.FadeGroup.SetEasing(Easing.Sine.InOut);
```

所有 `AnimancerState` 类型都支持自定义缓动。

---

### Q6: 如何实现自定义的弹簧效果？

**A**:

```csharp
state.FadeGroup.SetEasing(t =>
{
    // 模拟阻尼弹簧
    float damping = 0.8f;
    float frequency = 5.0f;
    return 1 - Mathf.Exp(-t * damping) * Mathf.Cos(t * frequency);
});
```

---

## 总结

### 核心要点

1. **三种实现方法**
   - 自定义委托：灵活，代码控制
   - 标准缓动类：方便，预定义曲线
   - AnimationCurve：可视化，Inspector 配置

2. **常用缓动类型**
   - **Sine.InOut**：最平滑，通用
   - **Quad.In/Out**：适度加速/减速
   - **Elastic/Back**：特殊效果
   - **Bounce**：物理反弹

3. **In/Out/InOut 模式**
   - **In**：加速进入
   - **Out**：减速退出
   - **InOut**：平滑过渡

4. **Pro 专属功能**
   - Lite 版本不支持
   - Pro 版本完全支持
   - 可以显著提升动画质量

### 下一步学习

- 📖 深入学习 **Sequences** 组合多个动画
- 🎨 探索 **Layers** 的缓动应用
- 📚 了解 **FadeGroup** 的高级用法
- 🔍 查看 3D Game Kit 示例的实际应用

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/blending/fading/custom/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)

## 参考资源

- [Easing Functions Cheat Sheet](https://easings.net/) - 可视化各种缓动函数
- [Robert Penner's Easing Functions](http://robertpenner.com/easing/) - 经典缓动函数参考
- [Unity AnimationCurve Documentation](https://docs.unity3d.com/ScriptReference/AnimationCurve.html) - Unity 官方文档
