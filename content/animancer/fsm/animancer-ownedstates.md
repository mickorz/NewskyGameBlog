---
title: "Animancer FSM - Owned States"
date: 2025-12-25
draft: false
---

# Animancer FSM - Owned States 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [实现方式](#实现方式)
- [扩展方法](#扩展方法)
- [代码示例](#代码示例)
- [参考资料](#参考资料)

---

## 概述

**Owned States（状态所有权）** 允许状态持有对其父状态机的引用，无需状态预先知道状态机的存在。

> **"状态可以可选地实现 `IOwnedState` 接口，以便在状态中使用 `StateExtensions` 类的扩展方法"**

---

## 核心概念

### 🔑 问题：状态如何切换？

```csharp
// ❌ 传统方式：状态需要引用角色来访问状态机
public class WalkState : IState
{
    private Character _character;

    public void DoSomething()
    {
        _character.StateMachine.TrySetState(_character.RunState);
    }
}
```

### ✅ 解决方案：Owned States

```csharp
// ✅ Owned States：状态直接知道自己的状态机
public class WalkState : IOwnedState<CharacterState>
{
    public StateMachine<CharacterState> OwnerStateMachine { get; set; }

    public void DoSomething()
    {
        this.TryEnterState(_runState); // 扩展方法！
    }
}
```

---

## 实现方式

### IOwnedState 接口

```csharp
/// <summary>
/// 状态所有权接口
/// </summary>
public interface IOwnedState<TState>
    where TState : class, IState
{
    /// <summary>
    /// 拥有此状态的状态机
    /// </summary>
    StateMachine<TState> OwnerStateMachine { get; }
}
```

### 完整实现示例

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 角色控制器
/// </summary>
public class Character : MonoBehaviour
{
    [SerializeField]
    private CharacterState.StateMachine _stateMachine;

    public CharacterState.StateMachine StateMachine => _stateMachine;

    protected virtual void Awake()
    {
        _stateMachine.InitializeAfterDeserialize();
    }
}

/// <summary>
/// 角色状态基类
/// 实现IOwnedState接口
/// </summary>
public abstract class CharacterState : StateBehaviour, IOwnedState<CharacterState>
{
    [SerializeField]
    private Character _character;

    // 实现IOwnedState接口
    public StateMachine<CharacterState> OwnerStateMachine
        => _character.StateMachine;

    // IState接口成员
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;
    public abstract void OnEnterState();
    public virtual void OnExitState() { }
}
```

---

## 扩展方法

### 可用的扩展方法

实现 `IOwnedState` 后，状态可以使用以下扩展方法：

```csharp
// 状态转换
this.TryEnterState();      // 尝试进入此状态
this.TryResetState();      // 重置并进入此状态
this.ForceEnterState();    // 强制进入此状态

// 状态查询
this.IsCurrentState();     // 是否为当前状态
this.GetPreviousState();   // 获取前一个状态
```

### 使用对比

#### 不使用 IOwnedState

```csharp
public class WalkState : IState
{
    private Character _character;

    public void TransitionToRun()
    {
        // ❌ 需要通过角色访问状态机
        _character.StateMachine.TrySetState(_character.RunState);
    }

    public bool IsWalking()
    {
        // ❌ 需要通过角色检查
        return _character.StateMachine.CurrentState == this;
    }
}
```

#### 使用 IOwnedState

```csharp
public class WalkState : CharacterState
{
    private RunState _runState;

    public void TransitionToRun()
    {
        // ✅ 直接使用扩展方法
        _runState.TryEnterState();
    }

    public bool IsWalking()
    {
        // ✅ 直接检查
        return this.IsCurrentState();
    }
}
```

---

## 代码示例

### 示例1：完整的Owned States实现

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 角色控制器（使用Owned States）
/// </summary>
public class Character : MonoBehaviour
{
    [Header("组件")]
    [SerializeField] private AnimancerComponent _animancer;

    [Header("状态机")]
    [SerializeField] private CharacterState.StateMachine _stateMachine;

    public CharacterState.StateMachine StateMachine => _stateMachine;

    protected virtual void Awake()
    {
        _stateMachine.InitializeAfterDeserialize();
    }
}

/// <summary>
/// 角色状态基类
/// 实现IOwnedState以使用扩展方法
/// </summary>
public abstract class CharacterState : StateBehaviour, IOwnedState<CharacterState>
{
    [SerializeField] protected Character _character;
    [SerializeField] protected AnimancerComponent _animancer;

    // 实现IOwnedState
    public StateMachine<CharacterState> OwnerStateMachine
        => _character.StateMachine;

    // IState接口
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;

    public override void OnEnterState()
    {
        base.OnEnterState(); // 启用组件
        Debug.Log($"Enter: {GetType().Name}");
    }

    public override void OnExitState()
    {
        Debug.Log($"Exit: {GetType().Name}");
        base.OnExitState(); // 禁用组件
    }
}

/// <summary>
/// Idle状态
/// </summary>
public class IdleState : CharacterState
{
    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private WalkState _walkState;

    public override void OnEnterState()
    {
        base.OnEnterState();
        _animancer.Play(_idleClip);
    }

    protected override void Update()
    {
        float input = Input.GetAxis("Vertical");

        if (input > 0.1f)
        {
            // ✅ 使用扩展方法切换状态
            _walkState.TryEnterState();
        }
    }
}

/// <summary>
/// Walk状态
/// </summary>
public class WalkState : CharacterState
{
    [SerializeField] private AnimationClip _walkClip;
    [SerializeField] private RunState _runState;
    [SerializeField] private IdleState _idleState;

    public override void OnEnterState()
    {
        base.OnEnterState();
        _animancer.Play(_walkClip);
    }

    protected override void Update()
    {
        float input = Input.GetAxis("Vertical");
        bool sprint = Input.GetKey(KeyCode.LeftShift);

        if (input < 0.1f)
        {
            // ✅ 返回Idle
            _idleState.TryEnterState();
        }
        else if (sprint)
        {
            // ✅ 切换到Run
            _runState.TryEnterState();
        }
    }
}

/// <summary>
/// Run状态
/// </summary>
public class RunState : CharacterState
{
    [SerializeField] private AnimationClip _runClip;
    [SerializeField] private WalkState _walkState;
    [SerializeField] private IdleState _idleState;

    public override void OnEnterState()
    {
        base.OnEnterState();
        _animancer.Play(_runClip);
    }

    protected override void Update()
    {
        float input = Input.GetAxis("Vertical");
        bool sprint = Input.GetKey(KeyCode.LeftShift);

        if (input < 0.1f)
        {
            _idleState.TryEnterState();
        }
        else if (!sprint)
        {
            _walkState.TryEnterState();
        }
    }
}
```

### 示例2：状态查询和管理

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 使用Owned States的状态查询
/// </summary>
public class StateQueryExample : CharacterState
{
    [SerializeField] private IdleState _idleState;
    [SerializeField] private AttackState _attackState;

    protected override void Update()
    {
        // ✅ 检查当前状态
        if (this.IsCurrentState())
        {
            Debug.Log("我是当前状态");
        }

        // ✅ 检查其他状态
        if (_idleState.IsCurrentState())
        {
            Debug.Log("当前是Idle状态");
        }

        // ✅ 获取前一个状态
        var previous = this.GetPreviousState();
        if (previous == _attackState)
        {
            Debug.Log("从攻击状态切换过来");
        }

        // ✅ 切换状态
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            _attackState.TryEnterState();
        }
    }
}
```

### 示例3：不同切换方法

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 演示不同的状态切换方法
/// </summary>
public class TransitionMethodsExample : CharacterState
{
    [SerializeField] private IdleState _idleState;
    [SerializeField] private AttackState _attackState;
    [SerializeField] private DeathState _deathState;

    void HandleInput()
    {
        // TryEnterState：尝试进入，检查Can条件
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            bool success = _attackState.TryEnterState();
            if (success)
                Debug.Log("进入攻击状态");
            else
                Debug.Log("无法进入攻击状态");
        }

        // TryResetState：即使已是当前状态也重新进入
        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            _attackState.TryResetState();
        }

        // ForceEnterState：跳过所有检查，强制进入
        if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            _deathState.ForceEnterState();
        }
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **状态基类实现IOwnedState**
```csharp
// ✅ 好：在基类中实现
public abstract class CharacterState : StateBehaviour, IOwnedState<CharacterState>
{
    public StateMachine<CharacterState> OwnerStateMachine => _character.StateMachine;
}
```

2. **使用扩展方法简化代码**
```csharp
// ✅ 好：简洁清晰
_walkState.TryEnterState();
this.IsCurrentState();
```

3. **序列化状态引用**
```csharp
// ✅ 好：在Inspector中配置状态引用
[SerializeField] private WalkState _walkState;
[SerializeField] private RunState _runState;
```

### ❌ DON'T（避免做法）

1. **不实现IOwnedState时手动管理**
```csharp
// ❌ 差：不如使用IOwnedState
_character.StateMachine.TrySetState(_walkState);
```

2. **循环依赖**
```csharp
// ❌ 差：状态间循环引用
public class StateA : CharacterState
{
    [SerializeField] private StateB _stateB;
}

public class StateB : CharacterState
{
    [SerializeField] private StateA _stateA; // 循环！
}
```

---

## 参考资料

### 📚 相关文档
- [FSM 主页](https://kybernetik.com.au/animancer/docs/manual/fsm/)
- [State Types](https://kybernetik.com.au/animancer/docs/manual/fsm/state-types)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`
  - `IOwnedState.cs`
  - `StateExtensions.cs`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
