---
title: "Animancer - Controller States"
date: 2025-12-25
draft: false
---

# Animancer - Controller States 官方文档

## 📋 目录
- [概述](#概述)
- [ControllerState](#controllerstate)
- [使用方法](#使用方法)
- [参数化ControllerState](#参数化controllerstate)
- [高级工具](#高级工具)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [参考资料](#参考资料)

---

## 概述

**ControllerState** 是 Animancer 中的一种特殊状态类型，能够播放整个 Animator Controller 作为单个状态。

> **⚠️ 授权要求：此功能仅限 Pro 版本**

### 🎯 核心优势

| 特性 | 说明 |
|------|------|
| **播放整个Controller** | 将Controller作为一个Animancer状态 |
| **混合能力** | 可与其他动画混合 |
| **多Controller支持** | 同一角色可播放多个Controller |
| **参数控制** | 完整的Animator参数API支持 |

### 典型应用场景

```csharp
// 场景1：保留复杂的移动Controller，特殊动画用Animancer
_animancer.Play(_movementController); // Controller状态
_animancer.Play(_specialAttack);      // Clip状态

// 场景2：同一角色多个Controller
_animancer.Layers[0].Play(_baseController);
_animancer.Layers[1].Play(_weaponController);

// 场景3：渐进迁移
_animancer.Play(_legacyController); // 保留旧Controller
// 新功能逐步用Animancer实现
```

---

## ControllerState

### 核心类型

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// ControllerState 基本结构
/// </summary>
public class ControllerStateBasics : MonoBehaviour
{
    // Controller资产
    [SerializeField] private RuntimeAnimatorController _controller;

    // 方式1：使用ControllerTransition
    [SerializeField] private ControllerTransition _controllerTransition;

    // 方式2：手动创建ControllerState
    private ControllerState _controllerState;

    void Example()
    {
        // ControllerState 提供完整的 Animator API
        _controllerState.Play("Idle");
        _controllerState.CrossFade("Walk", 0.25f);
        _controllerState.SetFloat("Speed", 5f);
        _controllerState.SetBool("IsGrounded", true);
        _controllerState.SetTrigger("Jump");
    }
}
```

---

## 使用方法

### 方式1：使用 ControllerTransition（推荐）

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 通过 ControllerTransition 使用（推荐）
/// </summary>
public class ControllerTransitionUsage : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // 在 Inspector 中配置
    [SerializeField] private ControllerTransition _controller;

    void Start()
    {
        // 播放 Controller
        _animancer.Play(_controller);

        // 访问 ControllerState
        var state = _controller.State;

        // 设置参数
        state.SetFloat("MoveSpeed", 0.5f);
        state.SetBool("IsRunning", true);
    }

    void Update()
    {
        // 动态更新参数
        float speed = Input.GetAxis("Vertical");
        _controller.State.SetFloat("Speed", Mathf.Abs(speed));
    }
}
```

### 方式2：手动创建 ControllerState

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 手动创建 ControllerState
/// </summary>
public class ManualControllerState : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private RuntimeAnimatorController _controller;

    private ControllerState _controllerState;

    void Start()
    {
        // 手动创建 ControllerState
        _controllerState = new ControllerState(_controller);

        // 播放
        _animancer.Play(_controllerState);

        // 或使用淡入
        _animancer.Play(_controllerState, 0.25f);
    }

    void Update()
    {
        // 控制参数
        float speed = Input.GetAxis("Vertical");
        _controllerState.SetFloat("MoveSpeed", Mathf.Abs(speed));
    }
}
```

### 方式3：HybridAnimancerComponent

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 使用 HybridAnimancerComponent
/// </summary>
public class HybridControllerUsage : MonoBehaviour
{
    [SerializeField] private HybridAnimancerComponent _animancer;
    [SerializeField] private AnimationClip _specialAttack;

    void Start()
    {
        // 自动播放 Controller（如果已分配）
        _animancer.PlayController();
    }

    void SpecialAttack()
    {
        // 临时切换到特殊动画
        var state = _animancer.Play(_specialAttack);

        state.Events.OnEnd = () =>
        {
            // 返回 Controller
            _animancer.PlayController(0.25f);
        };
    }

    void UpdateMovement(float speed)
    {
        // 设置 Controller 参数
        _animancer.Playable.SetFloat("Speed", speed);
    }
}
```

---

## 参数化ControllerState

### Float1ControllerState

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 单参数 Controller State
/// </summary>
public class Float1ControllerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // Float1ControllerState 封装一个Float参数
    [SerializeField] private Float1ControllerTransition _movement;

    void Start()
    {
        // 播放
        _animancer.Play(_movement);

        // 设置参数（类型安全）
        _movement.State.Parameter = 0.5f;

        // 参数名称在Inspector中有下拉菜单
    }

    void Update()
    {
        float speed = Input.GetAxis("Vertical");
        _movement.State.Parameter = Mathf.Abs(speed);
    }
}
```

### Float2ControllerState

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 双参数 Controller State (如2D混合)
/// </summary>
public class Float2ControllerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // Float2ControllerState 封装两个Float参数
    [SerializeField] private Float2ControllerTransition _locomotion;

    void Start()
    {
        _animancer.Play(_locomotion);
    }

    void Update()
    {
        // 设置两个参数
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        _locomotion.State.ParameterX = horizontal; // MoveX
        _locomotion.State.ParameterY = vertical;   // MoveY

        // 或使用向量
        _locomotion.State.Parameter = new Vector2(horizontal, vertical);
    }
}
```

### Float3ControllerState

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 三参数 Controller State
/// </summary>
public class Float3ControllerExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // Float3ControllerState 封装三个Float参数
    [SerializeField] private Float3ControllerTransition _advanced;

    void Update()
    {
        float x = Input.GetAxis("Horizontal");
        float y = Input.GetAxis("Vertical");
        float z = Input.GetKey(KeyCode.LeftShift) ? 1f : 0f;

        // 设置三个参数
        _advanced.State.ParameterX = x;
        _advanced.State.ParameterY = y;
        _advanced.State.ParameterZ = z;

        // 或使用向量
        _advanced.State.Parameter = new Vector3(x, y, z);
    }
}
```

### 参数验证

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 参数化ControllerState的优势：编译时验证
/// </summary>
public class ParameterValidation : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // ❌ 普通 ControllerState: 运行时才发现错误
    [SerializeField] private ControllerTransition _normalController;

    // ✅ Float1ControllerState: Inspector中验证参数存在
    [SerializeField] private Float1ControllerTransition _validatedController;

    void NormalApproach()
    {
        _animancer.Play(_normalController);

        // ⚠️ 拼写错误，运行时才会发现
        _normalController.State.SetFloat("Spead", 5f); // 应该是"Speed"
    }

    void ValidatedApproach()
    {
        _animancer.Play(_validatedController);

        // ✅ 类型安全，编译时检查
        _validatedController.State.Parameter = 5f;

        // Inspector会显示参数名称下拉菜单
        // 避免拼写错误
    }
}
```

---

## 高级工具

### Controller State Generator（Weaver插件）

```csharp
// 1. 选择 Animator Controller 资产
// 2. 点击 Inspector 中的齿轮图标
// 3. 选择 "Generate Controller State"
// 4. 选择脚本保存位置

/// <summary>
/// 自动生成的专用 ControllerState 类
/// </summary>
public class GeneratedCharacterController : Float2ControllerState
{
    // 自动生成的参数属性
    public float MoveX
    {
        get => GetFloat("MoveX");
        set => SetFloat("MoveX", value);
    }

    public float MoveY
    {
        get => GetFloat("MoveY");
        set => SetFloat("MoveY", value);
    }

    public bool IsGrounded
    {
        get => GetBool("IsGrounded");
        set => SetBool("IsGrounded", value);
    }

    public void TriggerJump()
    {
        SetTrigger("Jump");
    }

    // 使用示例
    void UpdateMovement()
    {
        MoveX = Input.GetAxis("Horizontal");
        MoveY = Input.GetAxis("Vertical");
        IsGrounded = CheckGround();
    }
}
```

### Transition Asset 生成

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 从 Animator Controller 生成 Transition Assets
/// </summary>
public class TransitionGeneration : MonoBehaviour
{
    // Animator Controller 中的状态和BlendTree
    // 可以转换为对应的 Animancer Transition Assets

    // 示例：BlendTree → MixerTransition
    // - 1D Blend Tree → LinearMixerTransition
    // - 2D Blend Tree → CartesianMixerTransition
    // - Direct Blend Tree → ManualMixerTransition

    [SerializeField] private LinearMixerTransition _generatedMixer;

    void Example()
    {
        // 生成的 Mixer 包含原始 BlendTree 的配置
        _animancer.Play(_generatedMixer);
    }
}
```

---

## 代码示例

### 示例1：基础 ControllerState 使用

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 基础 ControllerState 使用示例
/// </summary>
public class BasicControllerStateUsage : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private ControllerTransition _controller;

    [Header("特殊动画")]
    [SerializeField] private AnimationClip _death;
    [SerializeField] private AnimationClip _victory;

    void Start()
    {
        // 播放 Controller
        _animancer.Play(_controller);
    }

    void Update()
    {
        // 更新 Controller 参数
        float speed = Input.GetAxis("Vertical");
        _controller.State.SetFloat("Speed", Mathf.Abs(speed));

        bool isRunning = Input.GetKey(KeyCode.LeftShift);
        _controller.State.SetBool("IsRunning", isRunning);

        // 特殊动画打断 Controller
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            PlayDeath();
        }
    }

    void PlayDeath()
    {
        // 切换到特殊动画
        var state = _animancer.Play(_death);

        // 死亡动画结束后不返回 Controller
        state.Events.OnEnd = () =>
        {
            Debug.Log("角色死亡");
            enabled = false;
        };
    }

    void PlayVictory()
    {
        var state = _animancer.Play(_victory);

        // 胜利动画结束后返回 Controller
        state.Events.OnEnd = () =>
        {
            _animancer.Play(_controller, 0.25f);
        };
    }
}
```

### 示例2：多 Controller 分层

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 多个 Controller 分层使用
/// </summary>
public class MultiControllerLayers : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [Header("Controllers")]
    [SerializeField] private ControllerTransition _baseController;
    [SerializeField] private ControllerTransition _upperBodyController;

    [Header("遮罩")]
    [SerializeField] private AvatarMask _upperBodyMask;

    void Start()
    {
        // Layer 0: 全身移动 Controller
        _animancer.Layers[0].Play(_baseController);

        // Layer 1: 上半身武器 Controller
        var upperBodyLayer = _animancer.Layers[1];
        upperBodyLayer.SetMask(_upperBodyMask);
        upperBodyLayer.Play(_upperBodyController);
        upperBodyLayer.Weight = 1f;
    }

    void Update()
    {
        // 更新基础移动参数
        float speed = Input.GetAxis("Vertical");
        _baseController.State.SetFloat("Speed", Mathf.Abs(speed));

        // 更新上半身武器参数
        bool isAiming = Input.GetButton("Fire2");
        _upperBodyController.State.SetBool("IsAiming", isAiming);

        if (Input.GetButtonDown("Fire1"))
        {
            _upperBodyController.State.SetTrigger("Fire");
        }
    }
}
```

### 示例3：参数化 Controller 完整示例

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 完整的参数化 ControllerState 示例
/// </summary>
public class ParameterizedControllerComplete : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // 使用 Float2ControllerState 管理移动
    [SerializeField] private Float2ControllerTransition _movement;

    [Header("移动设置")]
    [SerializeField] private float _walkSpeed = 3f;
    [SerializeField] private float _runSpeed = 6f;

    private CharacterController _controller;

    void Awake()
    {
        _controller = GetComponent<CharacterController>();
    }

    void Start()
    {
        // 播放移动 Controller
        _animancer.Play(_movement);
    }

    void Update()
    {
        UpdateMovement();
        UpdateAnimation();
    }

    void UpdateMovement()
    {
        // 获取输入
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        bool sprint = Input.GetKey(KeyCode.LeftShift);
        float speed = sprint ? _runSpeed : _walkSpeed;

        // 移动角色
        Vector3 direction = new Vector3(horizontal, 0, vertical).normalized;
        _controller.Move(direction * speed * Time.deltaTime);

        // 旋转朝向
        if (direction.magnitude > 0.1f)
        {
            Quaternion targetRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                targetRotation,
                Time.deltaTime * 10f
            );
        }
    }

    void UpdateAnimation()
    {
        // 更新 Controller 参数
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        // 方式1：分别设置
        _movement.State.ParameterX = horizontal;
        _movement.State.ParameterY = vertical;

        // 方式2：使用向量
        // _movement.State.Parameter = new Vector2(horizontal, vertical);

        // 可以访问底层 Animator 方法
        if (Input.GetKeyDown(KeyCode.Space))
        {
            _movement.State.SetTrigger("Jump");
        }
    }
}
```

### 示例4：Controller + Animancer 混合系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// Controller 处理基础动画，Animancer 处理特殊动画
/// </summary>
public class HybridAnimationSystem : MonoBehaviour
{
    [SerializeField] private HybridAnimancerComponent _animancer;

    [Header("特殊动画")]
    [SerializeField] private AnimationClip[] _attacks;
    [SerializeField] private AnimationClip _dodge;
    [SerializeField] private AnimationClip _parry;
    [SerializeField] private AnimationClip _death;

    private int _attackIndex = 0;
    private bool _isPerformingAction = false;

    void Start()
    {
        // Controller 处理 Idle, Walk, Run, Jump
        _animancer.PlayController();
    }

    void Update()
    {
        // 防止在特殊动画期间接受输入
        if (_isPerformingAction) return;

        HandleCombat();
    }

    void HandleCombat()
    {
        // 攻击
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            PerformAttack();
        }

        // 闪避
        if (Input.GetKeyDown(KeyCode.Space))
        {
            PerformDodge();
        }

        // 格挡
        if (Input.GetKeyDown(KeyCode.Mouse1))
        {
            PerformParry();
        }
    }

    void PerformAttack()
    {
        _isPerformingAction = true;

        var attackClip = _attacks[_attackIndex];
        var state = _animancer.Play(attackClip, 0.1f);

        // 循环攻击索引
        _attackIndex = (_attackIndex + 1) % _attacks.Length;

        state.Events.OnEnd = () =>
        {
            _isPerformingAction = false;
            _animancer.PlayController(0.25f);
        };
    }

    void PerformDodge()
    {
        _isPerformingAction = true;

        var state = _animancer.Play(_dodge, 0.1f);
        state.Events.OnEnd = () =>
        {
            _isPerformingAction = false;
            _animancer.PlayController(0.15f);
        };
    }

    void PerformParry()
    {
        _isPerformingAction = true;

        var state = _animancer.Play(_parry, 0.05f);

        // 格挡窗口事件
        state.Events.AddNormalized(0.2f, OnParryWindowStart);
        state.Events.AddNormalized(0.6f, OnParryWindowEnd);

        state.Events.OnEnd = () =>
        {
            _isPerformingAction = false;
            _animancer.PlayController(0.2f);
        };
    }

    void OnParryWindowStart()
    {
        Debug.Log("格挡窗口开启");
    }

    void OnParryWindowEnd()
    {
        Debug.Log("格挡窗口关闭");
    }

    public void Die()
    {
        _isPerformingAction = true;

        var state = _animancer.Play(_death);
        state.Events.OnEnd = () =>
        {
            Debug.Log("角色死亡");
            enabled = false;
        };
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

#### 1. 使用 ControllerTransition

```csharp
// ✅ 好：在Inspector中配置
[SerializeField] private ControllerTransition _controller;
_animancer.Play(_controller);
```

#### 2. 使用参数化 ControllerState

```csharp
// ✅ 好：类型安全
[SerializeField] private Float1ControllerTransition _movement;
_movement.State.Parameter = 0.5f;
```

#### 3. Controller 处理基础，Animancer 处理特殊

```csharp
// ✅ 好：职责分离
// Controller: Idle, Walk, Run, Jump
// Animancer: Attack, Skill, Death, Cutscene
```

### ❌ DON'T（避免做法）

#### 1. 过度使用 ControllerState

```csharp
// ❌ 差：简单动画不需要 Controller
_animancer.Play(_idleController); // 直接用 AnimationClip

// ✅ 好
_animancer.Play(_idleClip);
```

#### 2. 硬编码参数名称

```csharp
// ❌ 差：拼写错误风险
_controller.State.SetFloat("Spead", 5f);

// ✅ 好：使用常量
private const string SPEED_PARAM = "Speed";
_controller.State.SetFloat(SPEED_PARAM, 5f);
```

#### 3. 忽略 ControllerState 的性能开销

```csharp
// ❌ 差：ControllerState 比 ClipState 开销更大
// 仅在必要时使用
```

---

## FAQ

### Q1: ControllerState 和普通播放 Controller 有什么区别？

**A:**

| 特性 | 普通 Controller | ControllerState |
|------|----------------|----------------|
| **播放方式** | Animator.Play() | Animancer.Play() |
| **混合能力** | 有限 | 完全支持 |
| **多Controller** | 不支持 | 支持 |
| **与Animancer集成** | Native模式 | Hybrid模式 |

### Q2: 什么时候使用 ControllerState？

**A:**

| 场景 | 推荐方案 |
|------|---------|
| 复杂状态机 | ControllerState |
| 简单动画 | AnimationClip |
| 遗留项目 | ControllerState（渐进迁移） |
| 新项目 | 优先 AnimationClip |

### Q3: Float1/2/3ControllerState 有什么优势？

**A:**

- ✅ Inspector 中参数名称下拉菜单
- ✅ 编译时验证参数存在
- ✅ 类型安全的参数访问
- ✅ 更好的代码自动补全

### Q4: 可以在 ControllerState 中使用 Animancer Events 吗？

**A:** 可以，但有限制：

```csharp
var state = _animancer.Play(_controller);

// ✅ End Events 正常工作
state.Events.OnEnd = () => Debug.Log("Controller finished");

// ⚠️ 中间事件不推荐（Controller内部状态复杂）
```

### Q5: ControllerState 性能如何？

**A:** 比 ClipState 开销更大：

- **ClipState**: ~0.1ms
- **ControllerState**: ~0.3-0.5ms

仅在需要 Controller 逻辑时使用。

---

## 参考资料

### 📚 相关文档
- [Animator Controllers](https://kybernetik.com.au/animancer/docs/manual/animator-controllers/)
- [Conversion Guide](https://kybernetik.com.au/animancer/docs/manual/animator-controllers/conversion/)
- [HybridAnimancerComponent](https://kybernetik.com.au/animancer/api/Animancer/HybridAnimancerComponent/)

### 💡 相关类型
- `ControllerState` - Controller 状态
- `ControllerTransition` - Controller 转换
- `Float1/2/3ControllerState` - 参数化 Controller 状态
- `HybridAnimancerComponent` - 混合组件

### 🔧 工具
- Controller State Generator (Weaver插件)
- Transition Asset Generator

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+ (仅Pro版本)
