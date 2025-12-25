---
title: "Animancer FSM - Overview"
date: 2025-12-25
draft: false
---

# Animancer FSM - Overview 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [三大核心脚本](#三大核心脚本)
- [设计目标](#设计目标)
- [主要限制](#主要限制)
- [代码示例](#代码示例)
- [参考资料](#参考资料)

---

## 概述

**有限状态机（Finite State Machine, FSM）** 是一个管理对象当前状态及其可能状态转换的系统。

### 🎯 典型应用

角色状态管理：
```
待机 (Idle) ⟷ 行走 (Walk) ⟷ 跑步 (Run)
   ↓                              ↓
跳跃 (Jump) ⟷ 下落 (Fall)
```

---

## 核心概念

### 📦 什么是有限状态机？

FSM 由以下要素组成：

1. **状态（States）**：系统可能处于的不同模式
2. **转换（Transitions）**：状态之间的切换规则
3. **当前状态（Current State）**：系统当前所处的状态
4. **事件（Events）**：触发状态转换的条件

### 🎭 状态机示例

```
┌─────────────────────────────────┐
│      Character StateMachine      │
├─────────────────────────────────┤
│ States:                         │
│  • Idle                        │
│  • Walk                        │
│  • Run                         │
│  • Jump                        │
│                                │
│ Current State: Walk            │
│ Previous State: Idle           │
└─────────────────────────────────┘
```

---

## 三大核心脚本

### 📋 核心组件对比

| 脚本 | 类型 | 功能 | 使用方式 |
|------|------|------|---------|
| **IState** | 接口 | 定义状态行为 | 状态类实现此接口 |
| **StateMachine<TState>** | 泛型类 | 管理状态切换 | 持有和管理状态 |
| **StateChange<TState>** | 结构体 | 访问转换信息 | 状态转换时使用 |

### 1. IState 接口

```csharp
public interface IState
{
    /// <summary>
    /// 能否进入该状态
    /// </summary>
    bool CanEnterState { get; }

    /// <summary>
    /// 能否退出该状态
    /// </summary>
    bool CanExitState { get; }

    /// <summary>
    /// 进入状态时调用
    /// </summary>
    void OnEnterState();

    /// <summary>
    /// 退出状态时调用
    /// </summary>
    void OnExitState();
}
```

**示例实现：**

```csharp
public class IdleState : IState
{
    public bool CanEnterState => true;
    public bool CanExitState => true;

    public void OnEnterState()
    {
        Debug.Log("进入待机状态");
    }

    public void OnExitState()
    {
        Debug.Log("离开待机状态");
    }
}
```

### 2. StateMachine<TState>

```csharp
public class StateMachine<TState> where TState : class, IState
{
    /// <summary>
    /// 当前状态
    /// </summary>
    public TState CurrentState { get; }

    /// <summary>
    /// 前一个状态
    /// </summary>
    public TState PreviousState { get; }

    /// <summary>
    /// 尝试切换状态
    /// </summary>
    public bool TrySetState(TState state);

    /// <summary>
    /// 强制切换状态
    /// </summary>
    public void ForceSetState(TState state);
}
```

**使用示例：**

```csharp
public class Character : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;
    private IdleState _idle;
    private WalkState _walk;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();
        _idle = new IdleState();
        _walk = new WalkState();

        // 设置初始状态
        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        // 根据输入切换状态
        if (Input.GetKey(KeyCode.W))
        {
            _stateMachine.TrySetState(_walk);
        }
        else
        {
            _stateMachine.TrySetState(_idle);
        }
    }
}
```

### 3. StateChange<TState>

```csharp
public struct StateChange<TState>
{
    /// <summary>
    /// 前一个状态
    /// </summary>
    public TState PreviousState { get; }

    /// <summary>
    /// 下一个状态
    /// </summary>
    public TState NextState { get; }
}
```

**使用场景：**

```csharp
// 在状态转换事件中使用
_stateMachine.OnStateChanged += (change) =>
{
    Debug.Log($"从 {change.PreviousState} 切换到 {change.NextState}");
};
```

---

## 设计目标

### ✅ 核心设计原则

> **"避免在基础场景中实现不必要的函数"**

### 📊 设计特性对比

| 特性 | 说明 | 优势 |
|------|------|------|
| **高效性** | 最小化性能开销 | 适合频繁状态切换 |
| **简洁性** | 只实现必需功能 | 易于学习和使用 |
| **通用性** | 开发者自定义基础状态类型 | 适应各种项目需求 |
| **灵活性** | 支持多种状态实现方式 | MonoBehaviour/ScriptableObject/POCO |
| **开放性** | 源代码完全可见 | 便于调试和扩展 |
| **独立性** | 与Unity整合但可独立使用 | 可移植性强 |

### 🎯 详细说明

#### 高效性（Performance）

```csharp
// 状态切换开销极小
_stateMachine.TrySetState(newState); // O(1) 操作，无GC分配
```

#### 简洁性（Simplicity）

```csharp
// 最小化API
public interface IState
{
    bool CanEnterState { get; }
    bool CanExitState { get; }
    void OnEnterState();
    void OnExitState();
}
```

#### 通用性（Generic）

```csharp
// 自定义状态基类
public abstract class MyBaseState : IState
{
    protected Character Character;
    // 添加项目特定的通用逻辑
}

// 使用自定义基类
StateMachine<MyBaseState> _stateMachine;
```

#### 灵活性（Flexible）

```csharp
// 方式1：MonoBehaviour
public class IdleState : StateBehaviour { }

// 方式2：ScriptableObject
[CreateAssetMenu]
public class IdleState : State { }

// 方式3：普通C#类
public class IdleState : IState { }
```

#### 开放性（Transparent）

```
源代码位置：
Assets/Plugins/Animancer/Utilities/FSM/
    ├─ IState.cs
    ├─ StateMachine.cs
    └─ StateChange.cs
```

#### 独立性（Standalone）

```csharp
// 可在非Unity项目中使用（移除UnityEngine引用）
public class NonUnityFSM
{
    private StateMachine<IState> _fsm;
    // 不依赖Unity API
}
```

---

## 主要限制

### ⚠️ 限制1：可视化差异

**问题：** 脚本系统缺乏 Animator Controller 那样的图形化连接展示。

**对比：**

| 系统 | 可视化 | 说明 |
|------|--------|------|
| **Animator Controller** | ✅ 图形化状态图 | 可视化查看所有状态和转换 |
| **Animancer FSM** | ❌ 纯代码 | 需要查看代码理解状态结构 |

**解决方案：**

```csharp
// 使用详细的注释和文档
/// <summary>
/// 角色状态机结构：
///
/// Idle ⟷ Walk ⟷ Run
///   ↓              ↓
/// Jump ⟷ Fall
///
/// </summary>
public class CharacterStateMachine
{
    // 状态定义...
}
```

### ⚠️ 限制2：网络同步

**问题：** 难以通过网络同步状态。

**原因：** 状态对象无法直接序列化传输。

**解决方案：** 使用 **Keyed State Machine**

```csharp
// 为状态分配键（Key）
public class CharacterStates
{
    public const int Idle = 0;
    public const int Walk = 1;
    public const int Run = 2;
}

// 网络同步
[Command]
void CmdChangeState(int stateKey)
{
    // 根据键切换状态
    switch (stateKey)
    {
        case CharacterStates.Idle:
            _stateMachine.TrySetState(_idle);
            break;
        case CharacterStates.Walk:
            _stateMachine.TrySetState(_walk);
            break;
    }
}
```

---

## 代码示例

### 示例1：完整的角色状态机

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 完整的角色状态机示例
///
/// 状态结构：
/// Idle ⟷ Walk ⟷ Run
///   ↓
/// Jump
/// </summary>
public class CharacterFSM : MonoBehaviour
{
    // 状态机
    private StateMachine<CharacterState> _stateMachine;

    // 状态实例
    private IdleState _idle;
    private WalkState _walk;
    private RunState _run;
    private JumpState _jump;

    void Awake()
    {
        // 初始化状态机
        _stateMachine = new StateMachine<CharacterState>();

        // 创建状态实例
        _idle = new IdleState(this);
        _walk = new WalkState(this);
        _run = new RunState(this);
        _jump = new JumpState(this);

        // 设置初始状态
        _stateMachine.TrySetState(_idle);

        // 监听状态变化
        // _stateMachine.OnStateChanged += OnStateChanged;
    }

    void Update()
    {
        HandleInput();
        UpdateCurrentState();
    }

    void HandleInput()
    {
        // 跳跃输入
        if (Input.GetKeyDown(KeyCode.Space))
        {
            _stateMachine.TrySetState(_jump);
            return;
        }

        // 移动输入
        float speed = Input.GetAxis("Vertical");
        bool isRunning = Input.GetKey(KeyCode.LeftShift);

        if (speed > 0.1f)
        {
            if (isRunning)
                _stateMachine.TrySetState(_run);
            else
                _stateMachine.TrySetState(_walk);
        }
        else
        {
            _stateMachine.TrySetState(_idle);
        }
    }

    void UpdateCurrentState()
    {
        // 调用当前状态的Update（如果有）
        (_stateMachine.CurrentState as IUpdatable)?.Update();
    }

    // 状态基类
    public abstract class CharacterState : IState
    {
        protected CharacterFSM Character;

        public CharacterState(CharacterFSM character)
        {
            Character = character;
        }

        public virtual bool CanEnterState => true;
        public virtual bool CanExitState => true;

        public abstract void OnEnterState();
        public virtual void OnExitState() { }
    }

    // Idle状态
    public class IdleState : CharacterState
    {
        public IdleState(CharacterFSM character) : base(character) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Idle");
        }
    }

    // Walk状态
    public class WalkState : CharacterState
    {
        public WalkState(CharacterFSM character) : base(character) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Walk");
        }
    }

    // Run状态
    public class RunState : CharacterState
    {
        public RunState(CharacterFSM character) : base(character) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Run");
        }
    }

    // Jump状态
    public class JumpState : CharacterState
    {
        public JumpState(CharacterFSM character) : base(character) { }

        public override bool CanEnterState
        {
            get
            {
                // 只能从地面状态跳跃
                var current = Character._stateMachine.CurrentState;
                return current == Character._idle ||
                       current == Character._walk ||
                       current == Character._run;
            }
        }

        public override void OnEnterState()
        {
            Debug.Log("→ Jump");
            // 跳跃完成后自动返回Idle
            Character.Invoke(nameof(ReturnToIdle), 1f);
        }

        void ReturnToIdle()
        {
            Character._stateMachine.TrySetState(Character._idle);
        }
    }

    // 可更新接口（可选）
    public interface IUpdatable
    {
        void Update();
    }
}
```

---

## 参考资料

### 📚 相关文档
- [FSM 主页](https://kybernetik.com.au/animancer/docs/manual/fsm/)
- [State Types](https://kybernetik.com.au/animancer/docs/manual/fsm/state-types)
- [Initialization](https://kybernetik.com.au/animancer/docs/manual/fsm/initialization/)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)

### 🔗 示例资源
- [FSM 示例](https://kybernetik.com.au/animancer/docs/samples/)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
