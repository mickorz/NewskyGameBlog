# Animancer - Animator Controllers Conversion 官方文档

## 📋 目录
- [概述](#概述)
- [核心转换概念](#核心转换概念)
- [功能对应关系](#功能对应关系)
- [转换指南](#转换指南)
- [API兼容性](#api兼容性)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [参考资料](#参考资料)

---

## 概述

Animancer 和 Mecanim (Animator Controller) 是**完全不同的系统**，无法直接转换，但功能可以映射对应。

> **"Direct conversion between them isn't possible, but their functionality can be mapped from one to the other."**

### 🎯 转换目标

| 转换方向 | 说明 |
|---------|------|
| **Mecanim → Animancer** | 将 Animator Controller 逻辑转换为脚本代码 |
| **逻辑迁移** | 参数、条件、状态机逻辑由脚本接管 |
| **资源复用** | AnimationClip 和 BlendTree 可直接使用 |

---

## 核心转换概念

### 哲学差异

```
Animator Controller（可视化，隐式逻辑）
         ↓
    状态 + 过渡 + 参数 + 条件
         ↓
    自动状态切换

VS

Animancer（代码驱动，显式逻辑）
         ↓
    AnimationClip + 脚本逻辑
         ↓
    手动状态切换
```

### 核心原则

> **"Animancer transitions don't define any conditions or logic - your scripts are responsible for all the logic."**

---

## 功能对应关系

### 完整对应表

| Mecanim 功能 | Animancer 替代方案 | 支持程度 |
|--------------|-------------------|---------|
| **AnimationClip** | 直接使用 | ✅ 完全支持 |
| **State** | AnimancerState（自动创建） | ✅ 完全支持 |
| **Transition** | Play() + FadeDuration | ✅ 完全支持 |
| **Parameters** | 脚本变量 | ✅ 完全替代 |
| **Conditions** | if 语句 | ✅ 完全替代 |
| **Blend Tree** | Mixer States | ✅ 完全支持 |
| **Layers** | AnimancerLayer | ✅ 运行时创建 |
| **State Machine Behaviour** | FSM 系统 | ✅ 更灵活 |
| **Sub-State Machine** | 脚本组织 | ⚠️ 手动实现 |
| **Animator.CrossFade()** | Play(clip, fade) | ✅ 完全支持 |

---

## 转换指南

### 1. 动画片段转换

**Mecanim:**
```
Animator Controller
  ├─ State: Idle (AnimationClip)
  ├─ State: Walk (AnimationClip)
  └─ State: Run (AnimationClip)
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

public class AnimationClipConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    void Start()
    {
        // 直接播放 AnimationClip
        _animancer.Play(_idle);
    }

    void PlayWalk()
    {
        _animancer.Play(_walk, 0.25f); // 淡入0.25秒
    }

    void PlayRun()
    {
        _animancer.Play(_run, 0.25f);
    }
}
```

### 2. 过渡转换

**Mecanim:**
```
Idle State
  ↓ (Transition)
  Condition: Speed > 0.1
  Duration: 0.25s
  ↓
Walk State
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

public class TransitionConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;

    private float _speed;

    void Update()
    {
        _speed = GetMovementSpeed();

        // ✅ 脚本负责所有逻辑
        if (_speed > 0.1f)
        {
            // 播放Walk，淡入0.25秒
            _animancer.Play(_walk, 0.25f);
        }
        else
        {
            _animancer.Play(_idle, 0.25f);
        }
    }

    float GetMovementSpeed()
    {
        // 获取移动速度
        return Input.GetAxis("Vertical");
    }
}
```

### 3. 参数转换

**Mecanim:**
```
Parameters:
  - Speed (Float)
  - IsGrounded (Bool)
  - Jump (Trigger)
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 用脚本变量替代 Animator Parameters
/// </summary>
public class ParameterConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [Header("动画")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _jump;

    // ✅ 参数转换为脚本变量
    private float _speed;
    private bool _isGrounded;
    private bool _jumpTriggered;

    void Update()
    {
        UpdateParameters();
        EvaluateAnimations();
    }

    void UpdateParameters()
    {
        // 更新变量（替代 Animator.SetFloat/SetBool/SetTrigger）
        _speed = Input.GetAxis("Vertical");
        _isGrounded = CheckGrounded();

        if (Input.GetKeyDown(KeyCode.Space))
            _jumpTriggered = true;
    }

    void EvaluateAnimations()
    {
        // 使用变量控制动画逻辑
        if (_jumpTriggered && _isGrounded)
        {
            _animancer.Play(_jump);
            _jumpTriggered = false; // 消耗Trigger
        }
        else if (_speed > 0.1f)
        {
            _animancer.Play(_walk, 0.25f);
        }
        else
        {
            _animancer.Play(_idle, 0.25f);
        }
    }

    bool CheckGrounded()
    {
        return Physics.Raycast(transform.position, Vector3.down, 1.1f);
    }
}
```

### 4. 条件转换

**Mecanim:**
```
Idle → Attack Transition
Conditions:
  - AttackTrigger == true
  - CanAttack == true
  - NormalizedTime > 0.16
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

public class ConditionConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _attack;

    private bool _attackTriggered;
    private bool _canAttack = true;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            _attackTriggered = true;
        }

        if (_attackTriggered)
        {
            TryAttack();
        }
    }

    void TryAttack()
    {
        // ✅ 所有条件检查在脚本中
        var currentState = _animancer.States.Current;
        float normalizedTime = currentState.NormalizedTime;

        // 条件1: AttackTrigger
        // 条件2: CanAttack
        // 条件3: NormalizedTime > 0.16
        if (_attackTriggered && _canAttack && normalizedTime > 0.16f)
        {
            PlayAttack();
            _attackTriggered = false;
        }
    }

    void PlayAttack()
    {
        var state = _animancer.Play(_attack);
        _canAttack = false;

        state.Events.OnEnd = () =>
        {
            _canAttack = true;
            _animancer.Play(_idle);
        };
    }
}
```

### 5. Blend Tree 转换

**Mecanim:**
```
Blend Tree (1D)
  ├─ Idle (0)
  ├─ Walk (0.5)
  └─ Run (1.0)
  Parameter: Speed
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

public class BlendTreeConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    private LinearMixerTransition _movementMixer;

    void Awake()
    {
        // 创建 Linear Mixer（1D Blend Tree）
        _movementMixer = new LinearMixerTransition
        {
            Clips = new[]
            {
                _idle,  // Parameter = 0
                _walk,  // Parameter = 0.5
                _run    // Parameter = 1.0
            }
        };
    }

    void Update()
    {
        // 播放 Mixer
        var state = _animancer.Play(_movementMixer);

        // 设置混合参数（0-1）
        float speed = Input.GetAxis("Vertical");
        state.Parameter = Mathf.Abs(speed);
    }
}
```

### 6. 分层转换

**Mecanim:**
```
Base Layer (Weight: 1.0)
  - Locomotion animations

Upper Body Layer (Weight: 0.5)
  - Aim animations
```

**Animancer:**
```csharp
using Animancer;
using UnityEngine;

public class LayerConversion : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [Header("Base Layer")]
    [SerializeField] private AnimationClip _walk;

    [Header("Upper Body Layer")]
    [SerializeField] private AnimationClip _aim;
    [SerializeField] private AvatarMask _upperBodyMask;

    void Start()
    {
        // Base Layer（默认Layer 0）
        _animancer.Play(_walk);

        // Upper Body Layer（Layer 1）
        var upperBodyLayer = _animancer.Layers[1];
        upperBodyLayer.SetMask(_upperBodyMask);
        upperBodyLayer.Play(_aim);

        // 设置权重
        upperBodyLayer.Weight = 0.5f;
    }
}
```

### 7. State Machine Behaviour 转换

**Mecanim:**
```csharp
public class AttackBehaviour : StateMachineBehaviour
{
    public override void OnStateEnter(Animator animator, ...)
    {
        // 进入攻击状态
    }

    public override void OnStateExit(Animator animator, ...)
    {
        // 退出攻击状态
    }
}
```

**Animancer:**
```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

// 使用 FSM 系统替代
public class AttackState : StateBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _attackClip;

    // ✅ OnEnterState 替代 OnStateEnter
    public override void OnEnterState()
    {
        base.OnEnterState(); // 启用组件
        _animancer.Play(_attackClip);
        Debug.Log("进入攻击状态");
    }

    // ✅ OnExitState 替代 OnStateExit
    public override void OnExitState()
    {
        Debug.Log("退出攻击状态");
        base.OnExitState(); // 禁用组件
    }

    // ✅ Update 替代 OnStateUpdate
    protected override void Update()
    {
        // 攻击状态的每帧逻辑
    }
}
```

---

## API兼容性

### 正常工作的 Animator API

```csharp
using UnityEngine;

public class WorkingAnimatorAPI : MonoBehaviour
{
    private Animator _animator;

    void Example()
    {
        // ✅ 根运动
        Vector3 deltaPosition = _animator.deltaPosition;
        Quaternion deltaRotation = _animator.deltaRotation;
        _animator.applyRootMotion = true;

        // ✅ Avatar 属性
        Avatar avatar = _animator.avatar;
        bool isHuman = _animator.isHuman;

        // ✅ IK 系统
        _animator.SetIKPosition(AvatarIKGoal.LeftHand, Vector3.zero);
        _animator.SetIKRotation(AvatarIKGoal.LeftHand, Quaternion.identity);
        _animator.SetLookAtPosition(Vector3.forward);

        // ✅ 骨骼变换
        Transform bone = _animator.GetBoneTransform(HumanBodyBones.Head);
    }
}
```

### 需要替换的 Animator API

```csharp
using Animancer;
using UnityEngine;

public class ReplacedAnimatorAPI : MonoBehaviour
{
    private Animator _animator;
    private AnimancerComponent _animancer;

    void Example()
    {
        // ❌ Animator.Play() → ✅ Animancer.Play()
        // _animator.Play("Idle");
        _animancer.Play(_idleClip);

        // ❌ Animator.CrossFade() → ✅ Animancer.Play(clip, fade)
        // _animator.CrossFade("Walk", 0.25f);
        _animancer.Play(_walkClip, 0.25f);

        // ❌ Animator.SetFloat() → ✅ 脚本变量
        // _animator.SetFloat("Speed", 5f);
        _speed = 5f;

        // ❌ Animator.GetFloat() → ✅ 脚本变量
        // float speed = _animator.GetFloat("Speed");
        float speed = _speed;

        // ❌ Animator.SetBool() → ✅ 脚本变量
        // _animator.SetBool("IsGrounded", true);
        _isGrounded = true;

        // ❌ Animator.SetTrigger() → ✅ 脚本标记
        // _animator.SetTrigger("Attack");
        _attackTriggered = true;

        // ❌ Animator.GetLayerWeight() → ✅ Animancer.Layers[].Weight
        // float weight = _animator.GetLayerWeight(1);
        float weight = _animancer.Layers[1].Weight;

        // ❌ Animator.speed → ✅ AnimancerGraph.Speed
        // _animator.speed = 2f;
        _animancer.Graph.Speed = 2f;
    }

    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private AnimationClip _walkClip;
    private float _speed;
    private bool _isGrounded;
    private bool _attackTriggered;
}
```

---

## 代码示例

### 示例1：完整的角色移动转换

**原始 Mecanim 方案:**

```
Animator Controller:
  Parameters:
    - Speed (Float)
    - IsGrounded (Bool)
  States:
    - Idle
    - Walk
    - Run
  Transitions:
    - Idle → Walk (Speed > 0.1)
    - Walk → Run (Speed > 0.5)
    - Any → Idle (Speed < 0.1)
```

**转换后的 Animancer 方案:**

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 完整的角色移动系统（Animancer版本）
/// </summary>
public class CharacterMovementAnimancer : MonoBehaviour
{
    [Header("组件")]
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private CharacterController _controller;

    [Header("动画")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    [Header("设置")]
    [SerializeField] private float _walkSpeed = 3f;
    [SerializeField] private float _runSpeed = 6f;

    // 参数（替代 Animator Parameters）
    private float _speed;
    private bool _isGrounded;

    void Update()
    {
        UpdateMovement();
        UpdateAnimation();
    }

    void UpdateMovement()
    {
        // 移动逻辑
        float input = Input.GetAxis("Vertical");
        bool sprint = Input.GetKey(KeyCode.LeftShift);

        float targetSpeed = sprint ? _runSpeed : _walkSpeed;
        _speed = input * targetSpeed;

        Vector3 movement = transform.forward * _speed * Time.deltaTime;
        _controller.Move(movement);

        // 地面检测
        _isGrounded = _controller.isGrounded;
    }

    void UpdateAnimation()
    {
        // 动画逻辑（替代 Animator 状态机）
        if (!_isGrounded)
        {
            // 空中动画（如果有）
            return;
        }

        if (_speed < 0.1f)
        {
            // Idle
            _animancer.Play(_idle, 0.25f);
        }
        else if (_speed < 4f)
        {
            // Walk
            _animancer.Play(_walk, 0.25f);
        }
        else
        {
            // Run
            _animancer.Play(_run, 0.25f);
        }
    }
}
```

### 示例2：战斗系统转换

**原始 Mecanim 方案:**

```
Animator Controller:
  Parameters:
    - AttackTrigger (Trigger)
    - ComboIndex (Int)
  States:
    - Idle
    - Attack1
    - Attack2
    - Attack3
  Transitions:
    - Idle → Attack1 (AttackTrigger)
    - Attack1 → Attack2 (AttackTrigger && NormalizedTime > 0.5)
    - Attack2 → Attack3 (AttackTrigger && NormalizedTime > 0.5)
```

**转换后的 Animancer 方案:**

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 战斗系统（Animancer版本）
/// </summary>
public class CombatSystemAnimancer : MonoBehaviour
{
    [Header("组件")]
    [SerializeField] private AnimancerComponent _animancer;

    [Header("动画")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _attack1;
    [SerializeField] private AnimationClip _attack2;
    [SerializeField] private AnimationClip _attack3;

    // 参数
    private bool _attackTriggered;
    private int _comboIndex = 0;
    private bool _canCombo = false;

    void Update()
    {
        // 检测输入
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            _attackTriggered = true;
        }

        // 处理攻击
        if (_attackTriggered)
        {
            TryAttack();
            _attackTriggered = false;
        }
    }

    void TryAttack()
    {
        var currentState = _animancer.States.Current;
        float normalizedTime = currentState?.NormalizedTime ?? 1f;

        // 检查是否可以连击
        if (_comboIndex > 0 && normalizedTime < 0.5f)
        {
            // 太早，无法连击
            return;
        }

        // 执行攻击
        _comboIndex++;

        switch (_comboIndex)
        {
            case 1:
                PlayAttack(_attack1);
                break;
            case 2:
                PlayAttack(_attack2);
                break;
            case 3:
                PlayAttack(_attack3);
                _comboIndex = 0; // 重置连击
                break;
        }
    }

    void PlayAttack(AnimationClip clip)
    {
        var state = _animancer.Play(clip);

        // 添加事件
        state.Events.OnEnd = () =>
        {
            // 攻击结束，返回Idle
            _animancer.Play(_idle);
            _comboIndex = 0;
        };
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

#### 1. 逐步转换

```csharp
// ✅ 好：先转换简单的动画
// 第1周：Idle, Walk
// 第2周：Jump, Attack
// 第3周：复杂连击
```

#### 2. 使用 Transition Assets

```csharp
// ✅ 好：预定义配置
[SerializeField] private ClipTransition _walkTransition;

void Start()
{
    _walkTransition.FadeDuration = 0.25f;
    _walkTransition.Speed = 1.2f;
}
```

#### 3. 保留 AnimationClip

```csharp
// ✅ 好：AnimationClip 可直接复用
// 无需重新制作动画
```

### ❌ DON'T（避免做法）

#### 1. 尝试一次性转换全部

```csharp
// ❌ 差：风险太大
// 转换大型项目需要循序渐进
```

#### 2. 忽略边界情况

```csharp
// ❌ 差：未处理动画被打断的情况
_animancer.Play(_attack);

// ✅ 好：添加事件回调
var state = _animancer.Play(_attack);
state.Events.OnEnd = OnAttackEnd;
```

---

## FAQ

### Q1: 必须完全移除 Animator Controller 吗？

**A:** 不必须。可以使用 Hybrid 模式保留 Controller：

```csharp
// 保留 Controller 用于基础动画
[SerializeField] private HybridAnimancerComponent _animancer;
_animancer.PlayController();

// Animancer 用于特殊动画
_animancer.Play(_specialAttack);
```

### Q2: Blend Tree 如何转换？

**A:** 使用 Mixer States：

| Mecanim | Animancer |
|---------|-----------|
| 1D Blend Tree | LinearMixerTransition |
| 2D Blend Tree | CartesianMixerTransition |
| Direct Blend Tree | ManualMixerTransition |

### Q3: Sub-State Machine 如何处理？

**A:** 使用嵌套的 FSM：

```csharp
// 主状态机
StateMachine<CharacterState> _mainFSM;

// 战斗子状态机
StateMachine<CombatState> _combatFSM;
```

### Q4: 转换后性能会提升吗？

**A:** 通常会。Animancer 更轻量：

- 无参数查找开销
- 无隐式状态机计算
- 更少的内存占用

### Q5: 如何处理现有的 Animator 脚本引用？

**A:** 逐步替换：

```csharp
// 原始代码
[SerializeField] private Animator _animator;
_animator.SetFloat("Speed", 5f);

// 转换后
[SerializeField] private AnimancerComponent _animancer;
private float _speed = 5f;
```

---

## 参考资料

### 📚 相关文档
- [Animator Controllers](https://kybernetik.com.au/animancer/docs/manual/animator-controllers/)
- [Controller States](https://kybernetik.com.au/animancer/docs/manual/animator-controllers/controller-states/)
- [Mixer States](https://kybernetik.com.au/animancer/docs/manual/blending/mixers/)
- [FSM System](https://kybernetik.com.au/animancer/docs/manual/fsm/)

### 💡 转换工具
- Controller State Generator（Weaver插件）
- Transition Asset Generator

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
