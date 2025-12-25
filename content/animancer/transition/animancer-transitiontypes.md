---
title: "Animancer Transition Types"
date: 2025-12-25
draft: false
---

# Animancer Transition Types 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/transitions/types/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

Animancer 中的**每个状态类型都对应一个转换类型**，用于在调用 `AnimancerComponent.Play(ITransition)` 时创建相应的状态。

### 核心机制

```
Transition Type（转换类型） → 创建 → State Type（状态类型）
        ↓                                    ↓
  ClipTransition                        ClipState
  LinearMixerTransition                 LinearMixerState
  MixerTransition2D                     Mixer2D
  ...等等
```

---

## 序列化引用机制 (Serialization Reference)

### 问题背景

Unity 通常**不支持序列化继承类型**。例如，如果你有一个 `ITransition` 接口，直接序列化会失败：

```csharp
// ❌ 这样不行，Unity 无法序列化接口
[SerializeField]
private ITransition _Animation; // 在 Inspector 中显示为空
```

### 解决方案：SerializeReference

使用 `[SerializeReference]` 属性可以解决这个问题：

```csharp
// ✅ 使用 SerializeReference 属性
[SerializeReference]
private ITransition _Animation;
```

**效果**：
- 在 Inspector 中会显示一个**下拉菜单**
- 可以选择任何实现了 `ITransition` 的类型
- 代码无需了解具体类型，保持了多态性

**可视化示例**：
```
Inspector 中的显示：
┌─────────────────────────────────┐
│ Animation                       │
│ ┌─────────────────────────────┐ │
│ │ ▼ ClipTransition            │ │  ← 下拉菜单
│ ├─────────────────────────────┤ │
│ │   Clip: [拖入动画片段]      │ │
│ │   Fade Duration: 0.25       │ │
│ │   Speed: 1                  │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

点击下拉菜单可以切换为：
- ClipTransition
- LinearMixerTransition
- MixerTransition2D
- ControllerTransition
- 等等...

---

## Transition 类型分类

### 一、剪辑转换 (Clip Transitions)

#### 1. ClipTransition（单个剪辑转换）

**功能**：创建 `ClipState` 以播放**单个 AnimationClip**

**适用场景**：
- ✅ 简单的单个动画播放（如死亡、受击、装弹）
- ✅ 不需要混合的动画
- ✅ 需要精确控制淡入、速度、起始时间的动画

**配置字段**：
```yaml
Clip（动画片段）
├─ Animation Clip: 要播放的动画片段
├─ Fade Duration: 淡入时长（默认 0.25s）
├─ Speed: 播放速度（默认 1）
├─ Start Time: 起始时间（默认 0）
├─ End Time: 结束时间（默认动画长度）
└─ Events: 动画事件列表
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class ClipTransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private ClipTransition _DeathAnimation;

    public void Die()
    {
        // 播放死亡动画
        AnimancerState state = _Animancer.Play(_DeathAnimation);

        // 可以访问状态进行进一步操作
        state.Events.OnEnd = OnDeathAnimationEnd;
    }

    private void OnDeathAnimationEnd()
    {
        Debug.Log("角色死亡动画播放完毕");
        // 执行死亡后的逻辑
    }
}
```

**Inspector 配置示例**：
```
ClipTransition
├─ Clip: Rifle_Death_R
├─ Fade Duration: 0.1
├─ Speed: 1
├─ Start Time: 0
└─ Events:
    └─ Normalized Time: 1.0 → OnDeathComplete
```

---

#### 2. ClipTransitionSequence（剪辑序列转换）

**功能**：继承自 `ClipTransition`，包含一个**转换数组**，按顺序播放多个动画剪辑

**适用场景**：
- ✅ 需要连续播放多个动画（如连续攻击：轻击→重击→收刀）
- ✅ 过场动画序列
- ✅ 技能释放的多段动画

**工作原理**：
1. 播放第一个动画
2. 第一个动画结束后自动播放第二个
3. 依次类推，直到所有动画播放完毕

**配置字段**：
```yaml
ClipTransitionSequence
├─ Transitions（转换数组）:
│  ├─ [0] 第一个动画配置
│  ├─ [1] 第二个动画配置
│  └─ [2] 第三个动画配置
└─ 其他字段继承自 ClipTransition
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class ComboAttackExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private ClipTransitionSequence _ComboAttack;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 播放连续攻击序列
            _Animancer.Play(_ComboAttack);
        }
    }
}
```

**Inspector 配置示例**：
```
ClipTransitionSequence "三连击"
├─ Transitions:
│  ├─ [0] 轻击1
│  │  ├─ Clip: Attack_Light_1
│  │  ├─ Fade Duration: 0.1
│  │  └─ Speed: 1
│  ├─ [1] 轻击2
│  │  ├─ Clip: Attack_Light_2
│  │  ├─ Fade Duration: 0.05
│  │  └─ Speed: 1.2
│  └─ [2] 重击
│     ├─ Clip: Attack_Heavy
│     ├─ Fade Duration: 0.05
│     └─ Speed: 1
```

**应用示例（连击系统）**：
```csharp
public class ComboSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 定义多个连击序列
    [SerializeField] private ClipTransitionSequence _LightCombo;  // 轻攻击3连
    [SerializeField] private ClipTransitionSequence _HeavyCombo;  // 重攻击2连

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0)) // 左键
        {
            _Animancer.Play(_LightCombo);
        }
        else if (Input.GetKeyDown(KeyCode.Mouse1)) // 右键
        {
            _Animancer.Play(_HeavyCombo);
        }
    }
}
```

---

### 二、混合器转换 (Mixer Transitions)

混合器转换用于创建各类**混合器状态**，可以在多个动画之间平滑混合。

**右键菜单功能**：
- 右键点击混合器转换可以打开上下文菜单
- 包含多个实用功能（如添加子动画、删除子动画、调整顺序等）

---

#### 1. ManualMixerTransition（手动混合器转换）

**功能**：创建 `ManualMixerState`，手动控制每个子动画的权重

**适用场景**：
- ✅ 需要精确控制每个动画的权重
- ✅ 自定义混合逻辑
- ✅ 动画权重需要根据复杂条件计算

**特点**：
- 不依赖参数自动混合
- 完全由代码控制权重
- 灵活度最高

**配置字段**：
```yaml
ManualMixerTransition
├─ Children（子动画列表）:
│  ├─ [0] 动画1
│  ├─ [1] 动画2
│  └─ [2] 动画3
├─ Fade Duration: 淡入时长
└─ Synchronize Children: 是否同步子动画
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class ManualMixerExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private ManualMixerTransition _IdleMixer;

    private ManualMixerState _IdleState;

    void Start()
    {
        // 播放手动混合器
        _IdleState = (ManualMixerState)_Animancer.Play(_IdleMixer);
    }

    void Update()
    {
        // 根据玩家状态手动设置权重
        float health = GetHealthPercentage();

        if (health > 0.7f)
        {
            // 健康状态：100% 正常待机
            _IdleState.SetChildWeight(0, 1); // 正常待机
            _IdleState.SetChildWeight(1, 0); // 疲惫待机
            _IdleState.SetChildWeight(2, 0); // 受伤待机
        }
        else if (health > 0.3f)
        {
            // 中等状态：混合正常和疲惫
            float tiredness = (0.7f - health) / 0.4f; // 0 到 1
            _IdleState.SetChildWeight(0, 1 - tiredness);
            _IdleState.SetChildWeight(1, tiredness);
            _IdleState.SetChildWeight(2, 0);
        }
        else
        {
            // 危险状态：混合疲惫和受伤
            float injury = (0.3f - health) / 0.3f; // 0 到 1
            _IdleState.SetChildWeight(0, 0);
            _IdleState.SetChildWeight(1, 1 - injury);
            _IdleState.SetChildWeight(2, injury);
        }
    }

    private float GetHealthPercentage()
    {
        // 返回当前生命值百分比（0-1）
        return 0.5f; // 示例值
    }
}
```

**Inspector 配置示例**：
```
ManualMixerTransition "生命值待机混合"
├─ Fade Duration: 0.25
├─ Synchronize Children: true
└─ Children:
    ├─ [0] Idle_Healthy（健康待机）
    ├─ [1] Idle_Tired（疲惫待机）
    └─ [2] Idle_Injured（受伤待机）
```

---

#### 2. LinearMixerTransition（线性混合器转换）

**功能**：创建 `LinearMixerState`，根据**单个参数**在多个动画之间线性混合（1D 混合）

**适用场景**：
- ✅ 速度混合（慢走 → 快走 → 跑步）
- ✅ 根据单一数值的变化混合动画
- ✅ Animator BlendTree 1D 的替代

**配置字段**：
```yaml
LinearMixerTransition
├─ Children（子动画列表）:
│  ├─ [0] 动画1
│  ├─ [1] 动画2
│  └─ [2] 动画3
├─ Thresholds（阈值）:
│  ├─ [0] -1.0
│  ├─ [1] 0.0
│  └─ [2] 1.0
├─ Parameter（参数）: 控制混合的参数
├─ Fade Duration: 淡入时长
└─ Synchronize Children: 是否同步子动画
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class LinearMixerExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private LinearMixerTransition _MovementBlend;

    [SerializeField]
    private StringAsset _SpeedParameter;

    private LinearMixerState _MovementState;

    void Start()
    {
        // 播放线性混合器
        _MovementState = (LinearMixerState)_Animancer.Play(_MovementBlend);
    }

    void Update()
    {
        // 根据输入更新速度参数
        float inputMagnitude = Input.GetAxis("Vertical"); // -1 到 1
        float speed = inputMagnitude * 5f; // -5 到 5

        // 更新参数，混合器会自动混合动画
        _SpeedParameter.Value = speed;
    }
}
```

**Inspector 配置示例**：
```
LinearMixerTransition "移动速度混合"
├─ Fade Duration: 0.25
├─ Parameter: SpeedValue.asset
├─ Synchronize Children: true
├─ Children:
│  ├─ [0] Walk_Backward（后退）
│  ├─ [1] Idle（待机）
│  ├─ [2] Walk_Forward（前进）
│  └─ [3] Run_Forward（跑步）
└─ Thresholds:
    ├─ [0] -2.5
    ├─ [1] 0
    ├─ [2] 2.5
    └─ [3] 5.0
```

**工作原理**：
```
参数值 = -2.5 → 100% 后退
参数值 = -1.25 → 50% 后退 + 50% 待机
参数值 = 0    → 100% 待机
参数值 = 1.25 → 50% 待机 + 50% 前进
参数值 = 2.5  → 100% 前进
参数值 = 3.75 → 50% 前进 + 50% 跑步
参数值 = 5.0  → 100% 跑步
```

---

#### 3. MixerTransition2D（2D 混合器转换）

**功能**：创建笛卡尔或方向混合器状态，根据**两个参数**在多个动画之间混合（2D 混合）

**适用场景**：
- ✅ 8 方向移动混合（前后左右及对角线）
- ✅ 需要两个维度控制的动画混合
- ✅ Animator BlendTree 2D 的替代

**混合类型**：
1. **Freeform Cartesian（自由形式笛卡尔）**
   - 适合：自由移动的循环动画
   - 示例：8 方向行走

2. **Freeform Directional（自由形式方向性）**
   - 适合：方向性动画
   - 示例：起步动画、停止动画

3. **Simple Directional（简单方向性）**
   - 适合：简单的方向混合

**配置字段**：
```yaml
MixerTransition2D
├─ Type: 混合类型（Cartesian/Directional/Simple）
├─ Children（子动画列表）:
│  ├─ [0] 动画1
│  ├─ [1] 动画2
│  └─ ... (通常8个)
├─ Thresholds（2D坐标）:
│  ├─ [0] x: 0,   y: 1    (正前)
│  ├─ [1] x: 0.7, y: 0.7  (前右)
│  └─ ... (对应每个动画)
├─ Parameter X: X轴参数
├─ Parameter Y: Y轴参数
├─ Fade Duration: 淡入时长
└─ Synchronize Children: 是否同步子动画
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class Mixer2DExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private MixerTransition2D _WalkingBlend;

    [SerializeField]
    private StringAsset _HorizontalParameter;

    [SerializeField]
    private StringAsset _VerticalParameter;

    private Mixer2D _WalkingState;

    void Start()
    {
        // 播放2D混合器
        _WalkingState = (Mixer2D)_Animancer.Play(_WalkingBlend);
    }

    void Update()
    {
        // 获取输入
        float horizontal = Input.GetAxis("Horizontal"); // -1 到 1
        float vertical = Input.GetAxis("Vertical");     // -1 到 1

        // 更新参数，混合器会自动混合8个方向的动画
        _HorizontalParameter.Value = horizontal;
        _VerticalParameter.Value = vertical;
    }
}
```

**Inspector 配置示例**：
```
MixerTransition2D "8方向行走混合"
├─ Type: Freeform Cartesian
├─ Fade Duration: 0.25
├─ Parameter X: Horizontal.asset
├─ Parameter Y: Vertical.asset
├─ Synchronize Children: true
├─ Children (8个):
│  ├─ [0] Walk_Forward
│  ├─ [1] Walk_Forward_Right
│  ├─ [2] Walk_Right
│  ├─ [3] Walk_Backward_Right
│  ├─ [4] Walk_Backward
│  ├─ [5] Walk_Backward_Left
│  ├─ [6] Walk_Left
│  └─ [7] Walk_Forward_Left
└─ Thresholds (8组坐标):
    ├─ [0] x: 0,     y: 1
    ├─ [1] x: 0.707, y: 0.707
    ├─ [2] x: 1,     y: 0
    ├─ [3] x: 0.707, y: -0.707
    ├─ [4] x: 0,     y: -1
    ├─ [5] x: -0.707,y: -0.707
    ├─ [6] x: -1,    y: 0
    └─ [7] x: -0.707,y: 0.707
```

**坐标布局可视化**：
```
           (0, 1)
        正前 Forward
           ↑
   (-0.707, 0.707) | (0.707, 0.707)
      前左  \   |   /  前右
             \ | /
  (-1, 0) ----●---- (1, 0)
    正左       |       正右
             / | \
      后左  /   |   \  后右
(-0.707, -0.707) | (0.707, -0.707)
           ↓
        (0, -1)
       正后 Back
```

---

### 三、其他转换 (Other Transitions)

#### 1. ControllerTransition（控制器转换）

**功能**：创建 `ControllerState`，包装 Unity 的 **Animator Controller**

**适用场景**：
- ✅ 需要使用现有的 Animator Controller
- ✅ 渐进式迁移到 Animancer（保留部分 Animator 功能）
- ✅ 复杂的状态机逻辑暂时不想用代码重写

**配置字段**：
```yaml
ControllerTransition
├─ Controller: Animator Controller 资源
├─ Fade Duration: 淡入时长
└─ Keep State On Stop: 停止时保持状态
```

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class ControllerTransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private ControllerTransition _LegacyController;

    void Start()
    {
        // 播放 Animator Controller
        ControllerState state = (ControllerState)_Animancer.Play(_LegacyController);

        // 可以访问底层的 Animator
        Animator animator = state.Playable.GetAnimator();
        animator.SetBool("IsRunning", true);
    }
}
```

**使用建议**：
- ⚠️ 主要用于迁移过程
- ⚠️ 长期使用建议完全转换为 Animancer 状态
- ✅ 可以访问 Animator 的参数和功能

---

#### 2. PlayableAssetTransition（可播放资源转换）

**功能**：创建 `PlayableAssetState`，支持 Unity 的 **Timeline** 系统

**适用场景**：
- ✅ 使用 Timeline 制作的过场动画
- ✅ 复杂的多轨道动画序列
- ✅ 需要与 Timeline 绑定的对象交互

**配置字段**：
```yaml
PlayableAssetTransition
├─ Asset: PlayableAsset（Timeline资源）
├─ Bindings: 时间轴绑定数组
├─ Fade Duration: 淡入时长
└─ Speed: 播放速度
```

**时间轴绑定数组**：
- 用于绑定 Timeline 中的轨道到场景中的对象
- 例如：角色轨道绑定到玩家对象

**代码示例**：

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

public class PlayableAssetExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private PlayableAssetTransition _Cutscene;

    public void PlayCutscene()
    {
        // 播放 Timeline 过场动画
        PlayableAssetState state = (PlayableAssetState)_Animancer.Play(_Cutscene);

        // 监听播放结束
        state.Events.OnEnd = OnCutsceneEnd;
    }

    private void OnCutsceneEnd()
    {
        Debug.Log("过场动画播放完毕");
        // 恢复游戏控制
    }
}
```

**Inspector 配置示例**：
```
PlayableAssetTransition "开场过场动画"
├─ Asset: OpeningCutscene.playable
├─ Bindings:
│  ├─ [0] PlayerTrack → Player GameObject
│  ├─ [1] CameraTrack → Main Camera
│  └─ [2] EnemyTrack → Boss GameObject
├─ Fade Duration: 0.5
└─ Speed: 1
```

---

## 自定义转换 (Custom Transitions)

### 创建自定义 Transition

开发者可以通过以下方式创建自定义转换：

#### 方法一：实现 ITransition 接口

```csharp
using Animancer;
using UnityEngine;

[System.Serializable]
public class MyCustomTransition : ITransition
{
    [SerializeField]
    private AnimationClip _Clip;

    [SerializeField]
    private float _CustomParameter;

    public float FadeDuration => 0.25f;

    public AnimancerState CreateState()
    {
        // 创建自定义状态
        return new ClipState();
    }

    public void Apply(AnimancerState state)
    {
        // 应用自定义逻辑
        ClipState clipState = (ClipState)state;
        clipState.Clip = _Clip;
        clipState.Speed = _CustomParameter;
    }
}
```

---

#### 方法二：继承 Transition<TState>

**推荐方式**，更简洁：

```csharp
using Animancer;
using UnityEngine;

[System.Serializable]
public class MyCustomTransition : Transition<ClipState>
{
    [SerializeField]
    private AnimationClip _Clip;

    [SerializeField]
    private float _CustomParameter;

    public override ClipState CreateState()
    {
        return new ClipState();
    }

    public override void Apply(ClipState state)
    {
        base.Apply(state);
        state.Clip = _Clip;
        state.Speed = _CustomParameter;
    }
}
```

---

#### 方法三：继承现有 Transition（最常用）

**示例：面部表情转换**

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 面部表情转换，添加了用户友好的名称字段
/// </summary>
[System.Serializable]
public class FacialExpressionTransition : ClipTransition
{
    // 添加自定义字段
    [SerializeField]
    private string _ExpressionName = "Neutral";

    [SerializeField]
    private float _Intensity = 1f;

    public string ExpressionName => _ExpressionName;
    public float Intensity => _Intensity;

    public override void Apply(AnimancerState state)
    {
        base.Apply(state);

        // 应用强度到动画速度
        state.Speed = _Intensity;

        Debug.Log($"播放表情: {_ExpressionName}, 强度: {_Intensity}");
    }
}
```

**使用示例**：

```csharp
public class FacialAnimationController : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    [SerializeField]
    private FacialExpressionTransition _Smile;

    [SerializeField]
    private FacialExpressionTransition _Angry;

    public void ShowExpression(string expressionName)
    {
        if (expressionName == "Smile")
            _Animancer.Play(_Smile);
        else if (expressionName == "Angry")
            _Animancer.Play(_Angry);
    }
}
```

---

### 自定义 Inspector 绘制器

可以创建继承 `Drawer` 类的自定义绘制器：

```csharp
#if UNITY_EDITOR
using UnityEditor;
using Animancer.Editor;

[CustomPropertyDrawer(typeof(FacialExpressionTransition), true)]
public class FacialExpressionDrawer : TransitionDrawer
{
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        base.OnGUI(position, property, label);

        // 添加自定义 GUI
        SerializedProperty expressionName = property.FindPropertyRelative("_ExpressionName");
        EditorGUILayout.PropertyField(expressionName, new GUIContent("表情名称"));
    }
}
#endif
```

---

## Transition 类型选择指南

### 决策树

```
需要播放什么？
├─ 单个动画 → ClipTransition
├─ 多个动画顺序播放 → ClipTransitionSequence
├─ 根据一个参数混合 → LinearMixerTransition
├─ 根据两个参数混合 → MixerTransition2D
├─ 手动控制权重 → ManualMixerTransition
├─ 使用 Animator Controller → ControllerTransition
├─ 使用 Timeline → PlayableAssetTransition
└─ 自定义需求 → 继承并创建自定义 Transition
```

### 常见场景推荐

| 场景 | 推荐类型 |
|------|---------|
| 死亡动画 | ClipTransition |
| 装弹动画 | ClipTransition |
| 连续攻击 | ClipTransitionSequence |
| 速度混合（走→跑） | LinearMixerTransition |
| 8方向移动 | MixerTransition2D |
| 生命值影响待机 | ManualMixerTransition |
| 过场动画 | PlayableAssetTransition |
| 遗留系统迁移 | ControllerTransition |

---

## 最佳实践

### 1. 选择合适的 Transition 类型

**原则**：选择最简单能满足需求的类型

```
简单 → 复杂
ClipTransition → LinearMixer → Mixer2D → ManualMixer → Custom
```

### 2. 合理使用 Synchronize Children

**何时启用**：
- ✅ 循环动画（行走、跑步）
- ✅ 需要保持步调一致的动画

**何时禁用**：
- ❌ 不同时长的动画
- ❌ 单次播放的动画

### 3. 阈值设置技巧

**LinearMixer**：
- 均匀分布：`-1, 0, 1`
- 偏向某端：`-2, 0, 1`（更倾向负向）

**Mixer2D**：
- 使用 `0.707`（√2/2）保证对角线速度一致
- 避免使用 `(1, 1)` 导致速度√2倍

### 4. 性能优化

**避免过多子动画**：
- LinearMixer：≤ 5 个
- Mixer2D：≤ 16 个

**合理设置 Fade Duration**：
- 不要过长（> 0.5s）
- 根据动画类型调整

---

## 常见问题 FAQ

### Q1: 何时使用 ClipTransition vs ClipTransitionSequence？

**A**:
- **ClipTransition**：只需播放一个动画
- **ClipTransitionSequence**：需要连续播放多个动画

### Q2: LinearMixer 和 Mixer2D 有什么区别？

**A**:
- **LinearMixer**：1D 混合，用一个参数控制
- **Mixer2D**：2D 混合，用两个参数控制

### Q3: ManualMixer 适合什么场景？

**A**: 当你需要**完全自定义**权重计算逻辑时使用，如：
- 根据复杂公式计算权重
- 多个条件影响权重
- 动态调整权重

### Q4: ControllerTransition 的性能如何？

**A**:
- 比直接用 Animancer 慢
- 适合过渡期使用
- 建议最终迁移到纯 Animancer

### Q5: 如何创建自定义 Transition？

**A**: 三种方式：
1. 实现 `ITransition` 接口（最灵活）
2. 继承 `Transition<TState>`（推荐）
3. 继承现有类型（最简单，如继承 `ClipTransition`）

### Q6: Mixer2D 的三种类型有什么区别?

**A**:
- **Freeform Cartesian**：自由混合，适合循环动画
- **Freeform Directional**：方向性混合，适合起步/停止
- **Simple Directional**：简化版方向混合

---

## 总结

### 核心要点

1. **每种状态都有对应的 Transition**
   - ClipTransition → ClipState
   - LinearMixerTransition → LinearMixerState
   - 等等...

2. **选择合适的类型很重要**
   - 简单场景用简单类型
   - 复杂需求用高级类型
   - 必要时创建自定义类型

3. **Mixer 是强大的工具**
   - LinearMixer：1D 混合
   - Mixer2D：2D 混合
   - ManualMixer：完全控制

4. **可扩展性强**
   - 可以继承现有类型
   - 可以创建完全自定义的 Transition
   - 可以自定义 Inspector 显示

### Transition 类型速查表

| 类型 | 用途 | 子动画数 | 参数数 | 复杂度 |
|------|------|---------|--------|--------|
| ClipTransition | 单个动画 | 1 | 0 | ⭐ |
| ClipTransitionSequence | 多个顺序播放 | N | 0 | ⭐⭐ |
| LinearMixerTransition | 1D混合 | 2-5 | 1 | ⭐⭐⭐ |
| MixerTransition2D | 2D混合 | 4-16 | 2 | ⭐⭐⭐⭐ |
| ManualMixerTransition | 手动权重 | N | 0 | ⭐⭐⭐⭐ |
| ControllerTransition | 包装Controller | - | - | ⭐⭐⭐ |
| PlayableAssetTransition | Timeline | - | - | ⭐⭐⭐⭐ |

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/transitions/types/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
