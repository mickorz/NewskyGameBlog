---
title: "Animancer FSM - State Types"
date: 2025-12-25
draft: false
---

# Animancer FSM - State Types 官方文档

## 📋 目录
- [概述](#概述)
- [状态类型选择](#状态类型选择)
- [基础实现](#基础实现)
- [内置基础类](#内置基础类)
- [代码示例](#代码示例)
- [参考资料](#参考资料)

---

## 概述

Animancer的状态机系统是通用的，需要定义基础状态类型作为 `StateMachine<TState>` 的泛型参数。

### 🔑 唯一要求

> **状态类必须实现 `IState` 接口**

---

## 状态类型选择

### 📦 三种实现方式

| 类型 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **MonoBehaviour** | 需要Unity生命周期方法 | 可使用Update/FixedUpdate | 需要附加到GameObject |
| **ScriptableObject** | 可复用的状态资产 | 可在Inspector配置 | 需要创建Asset文件 |
| **普通C#类** | 纯逻辑状态 | 轻量级，无开销 | 无Unity功能 |

### 🎯 选择建议

```csharp
// 方式1：MonoBehaviour - 需要Unity生命周期
public class IdleState : StateBehaviour
{
    void Update() { /* 每帧更新 */ }
    void OnTriggerEnter(Collider other) { /* 碰撞检测 */ }
}

// 方式2：ScriptableObject - 可复用配置
[CreateAssetMenu(menuName = "States/Idle")]
public class IdleStateAsset : State
{
    [SerializeField] private float _duration;
}

// 方式3：普通C#类 - 纯逻辑（推荐）
public class IdleState : IState
{
    public bool CanEnterState => true;
    public bool CanExitState => true;
    public void OnEnterState() { }
    public void OnExitState() { }
}
```

---

## 基础实现

### 📝 最小实现

```csharp
/// <summary>
/// 最基础的状态实现
/// </summary>
public class MinimalState : IState
{
    // 可以进入
    public bool CanEnterState => true;

    // 可以退出
    public bool CanExitState => true;

    // 进入状态时调用
    public void OnEnterState()
    {
        Debug.Log("进入状态");
    }

    // 退出状态时调用
    public void OnExitState()
    {
        Debug.Log("退出状态");
    }
}
```

### 🎨 自定义基类

> **推荐**："可以简单地继承它，仅覆盖实际需要使用的成员"

```csharp
/// <summary>
/// 自定义状态基类
/// 封装通用逻辑
/// </summary>
public abstract class State : IState
{
    // 默认实现
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;

    // 默认空实现
    public virtual void OnEnterState() { }
    public virtual void OnExitState() { }
}

// 使用示例
public class IdleState : State
{
    // 只需覆盖需要的方法
    public override void OnEnterState()
    {
        Debug.Log("Idle");
    }
}
```

---

## 内置基础类

### 1. State 类

**功能：** 提供 `IState` 接口的默认实现。

```csharp
/// <summary>
/// Animancer内置基类
/// </summary>
public class State : IState
{
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;
    public virtual void OnEnterState() { }
    public virtual void OnExitState() { }
}
```

**使用示例：**

```csharp
// 继承State类
public class WalkState : State
{
    public override void OnEnterState()
    {
        Debug.Log("开始行走");
    }
}
```

### 2. DelegateState 类

**功能：** 通过为接口成员分配委托来实现逻辑。

```csharp
/// <summary>
/// 委托状态
/// 使用委托实现状态逻辑
/// </summary>
public class DelegateState : IState
{
    public Func<bool> CanEnter;
    public Func<bool> CanExit;
    public Action OnEnter;
    public Action OnExit;

    public bool CanEnterState => CanEnter?.Invoke() ?? true;
    public bool CanExitState => CanExit?.Invoke() ?? true;
    public void OnEnterState() => OnEnter?.Invoke();
    public void OnExitState() => OnExit?.Invoke();
}
```

**使用示例：**

```csharp
// 使用委托配置状态
var idleState = new DelegateState
{
    OnEnter = () => Debug.Log("进入Idle"),
    OnExit = () => Debug.Log("退出Idle")
};

var walkState = new DelegateState
{
    CanEnter = () => speed > 0.1f,  // 有速度才能进入
    OnEnter = () => _animancer.Play(_walkClip)
};

_stateMachine.TrySetState(idleState);
```

### 3. StateBehaviour 类

**功能：** 继承 MonoBehaviour，支持 Unity 生命周期消息。

> **关键特性**："OnEnterState和OnExitState方法分别启用和禁用自身"

```csharp
/// <summary>
/// MonoBehaviour状态基类
/// 进入时启用，退出时禁用
/// </summary>
public abstract class StateBehaviour : MonoBehaviour, IState
{
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;

    public virtual void OnEnterState()
    {
        enabled = true; // 自动启用
    }

    public virtual void OnExitState()
    {
        enabled = false; // 自动禁用
    }

    // 可使用Unity生命周期方法
    protected virtual void Update() { }
    protected virtual void FixedUpdate() { }
    protected virtual void OnTriggerEnter(Collider other) { }
}
```

**使用示例：**

```csharp
/// <summary>
/// Idle状态（MonoBehaviour实现）
/// </summary>
public class IdleBehaviour : StateBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idleClip;

    public override void OnEnterState()
    {
        base.OnEnterState(); // 调用基类（启用组件）
        _animancer.Play(_idleClip);
        Debug.Log("Idle状态激活");
    }

    protected override void Update()
    {
        // 只在状态激活时执行
        Debug.Log("Idle Update");
    }

    public override void OnExitState()
    {
        Debug.Log("Idle状态停用");
        base.OnExitState(); // 调用基类（禁用组件）
    }
}
```

---

## 代码示例

### 示例1：三种类型对比

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 三种状态类型对比示例
/// </summary>
public class StateTypesComparison : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();

        // 类型1：普通C#类
        var pocoState = new POCOState();

        // 类型2：ScriptableObject（需要预先创建Asset）
        // var soState = Resources.Load<ScriptableObjectState>("States/Idle");

        // 类型3：MonoBehaviour（需要添加到GameObject）
        var monoState = gameObject.AddComponent<MonoBehaviourState>();

        // 设置初始状态
        _stateMachine.TrySetState(pocoState);
    }

    // 1. 普通C#类实现
    public class POCOState : IState
    {
        public bool CanEnterState => true;
        public bool CanExitState => true;

        public void OnEnterState()
        {
            Debug.Log("[POCO] Enter");
        }

        public void OnExitState()
        {
            Debug.Log("[POCO] Exit");
        }
    }

    // 2. ScriptableObject实现
    [CreateAssetMenu(menuName = "States/SO State")]
    public class ScriptableObjectState : State
    {
        [SerializeField] private string _stateName;

        public override void OnEnterState()
        {
            Debug.Log($"[SO] Enter: {_stateName}");
        }
    }

    // 3. MonoBehaviour实现
    public class MonoBehaviourState : StateBehaviour
    {
        public override void OnEnterState()
        {
            base.OnEnterState();
            Debug.Log("[MonoBehaviour] Enter");
        }

        protected override void Update()
        {
            // 只在状态激活时执行
            Debug.Log("[MonoBehaviour] Update");
        }

        public override void OnExitState()
        {
            Debug.Log("[MonoBehaviour] Exit");
            base.OnExitState();
        }
    }
}
```

### 示例2：DelegateState实用案例

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// DelegateState实用示例
/// 快速原型设计和测试
/// </summary>
public class DelegateStateExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private AnimationClip _walkClip;

    private StateMachine<DelegateState> _stateMachine;
    private DelegateState _idle;
    private DelegateState _walk;

    void Awake()
    {
        _stateMachine = new StateMachine<DelegateState>();

        // 快速创建Idle状态
        _idle = new DelegateState
        {
            OnEnter = () =>
            {
                Debug.Log("→ Idle");
                _animancer.Play(_idleClip);
            },
            OnExit = () => Debug.Log("← Idle")
        };

        // 快速创建Walk状态（带条件）
        _walk = new DelegateState
        {
            CanEnter = () =>
            {
                // 只有在地面上才能行走
                bool isGrounded = Physics.Raycast(
                    transform.position,
                    Vector3.down,
                    1.1f
                );
                return isGrounded;
            },

            OnEnter = () =>
            {
                Debug.Log("→ Walk");
                _animancer.Play(_walkClip);
            },

            OnExit = () => Debug.Log("← Walk")
        };

        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        float speed = Input.GetAxis("Vertical");

        if (speed > 0.1f)
        {
            bool success = _stateMachine.TrySetState(_walk);
            if (!success)
            {
                Debug.Log("无法进入Walk状态（可能不在地面）");
            }
        }
        else
        {
            _stateMachine.TrySetState(_idle);
        }
    }
}
```

### 示例3：StateBehaviour完整示例

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// StateBehaviour完整示例
/// 展示MonoBehaviour状态的完整用法
/// </summary>
public class StateBehaviourExample : MonoBehaviour
{
    private StateMachine<StateBehaviour> _stateMachine;

    void Awake()
    {
        _stateMachine = new StateMachine<StateBehaviour>();

        // 添加状态组件
        var idle = gameObject.AddComponent<IdleStateBehaviour>();
        var patrol = gameObject.AddComponent<PatrolStateBehaviour>();

        // 设置初始状态
        _stateMachine.TrySetState(idle);
    }
}

/// <summary>
/// Idle状态行为
/// </summary>
public class IdleStateBehaviour : StateBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    private float _idleTime;

    public override void OnEnterState()
    {
        base.OnEnterState();
        _idleTime = 0f;
        _animancer.Play(_idleClip);
        Debug.Log("进入Idle");
    }

    protected override void Update()
    {
        _idleTime += Time.deltaTime;

        // Idle 3秒后自动切换到Patrol
        if (_idleTime >= 3f)
        {
            var patrol = GetComponent<PatrolStateBehaviour>();
            var fsm = GetComponent<StateBehaviourExample>();
            // fsm._stateMachine.TrySetState(patrol);
        }
    }

    [SerializeField] private AnimationClip _idleClip;
}

/// <summary>
/// Patrol状态行为
/// </summary>
public class PatrolStateBehaviour : StateBehaviour
{
    [SerializeField] private Transform[] _waypoints;
    private int _currentWaypoint;

    public override void OnEnterState()
    {
        base.OnEnterState();
        _currentWaypoint = 0;
        Debug.Log("开始巡逻");
    }

    protected override void Update()
    {
        if (_waypoints == null || _waypoints.Length == 0) return;

        // 移动到当前路径点
        Transform target = _waypoints[_currentWaypoint];
        transform.position = Vector3.MoveTowards(
            transform.position,
            target.position,
            2f * Time.deltaTime
        );

        // 到达后切换下一个路径点
        if (Vector3.Distance(transform.position, target.position) < 0.1f)
        {
            _currentWaypoint = (_currentWaypoint + 1) % _waypoints.Length;
        }
    }

    public override void OnExitState()
    {
        Debug.Log("结束巡逻");
        base.OnExitState();
    }
}
```

---

## 参考资料

### 📚 相关文档
- [FSM Overview](https://kybernetik.com.au/animancer/docs/manual/fsm/overview)
- [FSM Initialization](https://kybernetik.com.au/animancer/docs/manual/fsm/initialization/)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`
  - `IState.cs`
  - `State.cs`
  - `DelegateState.cs`
  - `StateBehaviour.cs`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
