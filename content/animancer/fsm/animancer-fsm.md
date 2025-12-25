# Animancer FSM 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [基本使用步骤](#基本使用步骤)
- [IState接口](#istate接口)
- [状态转换流程](#状态转换流程)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

**Animancer FSM** 是一个通用的有限状态机（Finite State Machine）系统，设计上具有足够的灵活性以满足大多数需求，且**不与动画系统绑定**。

### 🎯 核心特性

> **"通用 FSM 系统，灵活性足以满足大多数需求，但不与动画系统绑定"**

### 📁 源代码位置

完整源代码位于：
```
Assets/Plugins/Animancer/Utilities/FSM/
```

### 🔑 关键优势

| 特性 | 说明 |
|------|------|
| **通用性** | 不局限于动画，可用于任何需要状态管理的场景 |
| **灵活性** | 支持各种状态类型和转换规则 |
| **开源** | 提供完整源代码，可自由修改和扩展 |
| **类型安全** | 使用泛型保证类型安全 |
| **轻量级** | 简洁的API设计，易于学习和使用 |

---

## 核心概念

### 🎭 有限状态机（FSM）

有限状态机是一种数学模型，用于描述系统在不同状态之间的转换行为。

```
状态机结构：
┌──────────────────────────────────────┐
│        StateMachine<TState>          │
│                                      │
│  ┌────────┐      ┌────────┐        │
│  │ State1 │ ───> │ State2 │        │
│  └────────┘      └────────┘        │
│      ↑               │              │
│      └───────────────┘              │
│                                      │
│  CurrentState: IState                │
│  PreviousState: IState               │
└──────────────────────────────────────┘
```

### 📦 主要组件

#### 1. StateMachine<TState>

状态机容器，管理状态的切换和生命周期。

```csharp
public class StateMachine<TState> where TState : class, IState
{
    public TState CurrentState { get; }
    public TState PreviousState { get; }

    public bool TrySetState(TState state);
    public bool TryResetState(TState state);
    public void ForceSetState(TState state);
}
```

#### 2. IState 接口

所有状态必须实现的接口。

```csharp
public interface IState
{
    bool CanEnterState { get; }
    bool CanExitState { get; }

    void OnEnterState();
    void OnExitState();
}
```

---

## 基本使用步骤

### 步骤1：创建状态类

实现 `IState` 接口或继承基类：

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 简单的状态类示例
/// </summary>
public class IdleState : IState
{
    public bool CanEnterState => true;
    public bool CanExitState => true;

    public void OnEnterState()
    {
        Debug.Log("进入 Idle 状态");
    }

    public void OnExitState()
    {
        Debug.Log("退出 Idle 状态");
    }
}
```

### 步骤2：创建状态机字段

使用 `StateMachine<TState>` 泛型：

```csharp
public class CharacterController : MonoBehaviour
{
    // 定义状态机
    private StateMachine<IState> _stateMachine;

    // 定义状态实例
    private IdleState _idleState;
    private WalkState _walkState;
}
```

### 步骤3：初始化状态机

在 Awake 或 Start 中创建实例：

```csharp
void Awake()
{
    // 创建状态机
    _stateMachine = new StateMachine<IState>();

    // 创建状态实例
    _idleState = new IdleState();
    _walkState = new WalkState();

    // 设置初始状态
    _stateMachine.TrySetState(_idleState);
}
```

### 步骤4：状态转换

调用 `TrySetState()` 进行状态切换：

```csharp
void Update()
{
    float speed = Input.GetAxis("Vertical");

    if (speed > 0.1f)
    {
        // 尝试切换到Walk状态
        _stateMachine.TrySetState(_walkState);
    }
    else
    {
        // 尝试切换到Idle状态
        _stateMachine.TrySetState(_idleState);
    }
}
```

### 步骤5：访问当前状态

通过 `CurrentState` 属性：

```csharp
void Update()
{
    // 获取当前状态
    var current = _stateMachine.CurrentState;

    Debug.Log($"当前状态: {current.GetType().Name}");

    // 获取前一个状态
    var previous = _stateMachine.PreviousState;
    Debug.Log($"前一个状态: {previous?.GetType().Name}");
}
```

---

## IState接口

### 📋 接口成员详解

```csharp
public interface IState
{
    /// <summary>
    /// 是否能进入该状态
    /// </summary>
    bool CanEnterState { get; }

    /// <summary>
    /// 是否能退出该状态
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

### 🎯 成员说明

#### CanEnterState（是否可进入）

```csharp
public class BusyState : IState
{
    private bool _isProcessing;

    // 只有在不处理任务时才能进入
    public bool CanEnterState => !_isProcessing;

    public bool CanExitState => true;

    public void OnEnterState()
    {
        _isProcessing = true;
        StartProcessing();
    }

    public void OnExitState()
    {
        _isProcessing = false;
    }
}
```

#### CanExitState（是否可退出）

```csharp
public class AttackState : IState
{
    private bool _attackFinished;

    public bool CanEnterState => true;

    // 只有攻击完成才能退出
    public bool CanExitState => _attackFinished;

    public void OnEnterState()
    {
        _attackFinished = false;
        PerformAttack();
    }

    void OnAttackComplete()
    {
        _attackFinished = true;
    }

    public void OnExitState() { }
}
```

#### OnEnterState（进入回调）

```csharp
public void OnEnterState()
{
    Debug.Log("状态激活");

    // 播放动画
    _animancer.Play(_animation);

    // 启用组件
    EnableComponents();

    // 注册事件
    RegisterEvents();
}
```

#### OnExitState（退出回调）

```csharp
public void OnExitState()
{
    Debug.Log("状态停用");

    // 停止动画
    _animancer.Stop();

    // 禁用组件
    DisableComponents();

    // 注销事件
    UnregisterEvents();
}
```

---

## 状态转换流程

### 🔄 TrySetState 执行流程

```
调用 TrySetState(nextState)
    ↓
1. 检查 currentState.CanExitState
    ├─ false → 返回 false（转换失败）
    └─ true → 继续
    ↓
2. 检查 nextState.CanEnterState
    ├─ false → 返回 false（转换失败）
    └─ true → 继续
    ↓
3. 调用 currentState.OnExitState()
    ↓
4. 调用 nextState.OnEnterState()
    ↓
5. 更新状态
    ├─ PreviousState = currentState
    └─ CurrentState = nextState
    ↓
返回 true（转换成功）
```

### 📝 代码示例

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 状态转换流程示例
/// </summary>
public class StateTransitionExample : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();

        var idleState = new LoggerState("Idle");
        var walkState = new LoggerState("Walk");

        // 设置初始状态
        _stateMachine.TrySetState(idleState);
        // 输出: [Idle] OnEnterState

        // 尝试切换状态
        bool success = _stateMachine.TrySetState(walkState);
        // 输出: [Idle] OnExitState
        // 输出: [Walk] OnEnterState

        Debug.Log($"转换结果: {success}"); // true
        Debug.Log($"当前状态: {_stateMachine.CurrentState}"); // Walk
        Debug.Log($"前一个状态: {_stateMachine.PreviousState}"); // Idle
    }
}

/// <summary>
/// 日志记录状态（用于演示）
/// </summary>
public class LoggerState : IState
{
    private readonly string _name;

    public LoggerState(string name)
    {
        _name = name;
    }

    public bool CanEnterState
    {
        get
        {
            Debug.Log($"[{_name}] CanEnterState 检查");
            return true;
        }
    }

    public bool CanExitState
    {
        get
        {
            Debug.Log($"[{_name}] CanExitState 检查");
            return true;
        }
    }

    public void OnEnterState()
    {
        Debug.Log($"[{_name}] OnEnterState");
    }

    public void OnExitState()
    {
        Debug.Log($"[{_name}] OnExitState");
    }

    public override string ToString() => _name;
}
```

---

## 代码示例

### 示例1：基础角色控制器

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 基础角色控制器
/// 使用FSM管理角色状态
/// </summary>
public class BasicCharacterController : MonoBehaviour
{
    [Header("组件")]
    [SerializeField] private AnimancerComponent _animancer;

    [Header("动画")]
    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private AnimationClip _walkClip;
    [SerializeField] private AnimationClip _runClip;

    // 状态机
    private StateMachine<CharacterState> _stateMachine;

    // 状态实例
    private IdleState _idle;
    private WalkState _walk;
    private RunState _run;

    void Awake()
    {
        // 创建状态机
        _stateMachine = new StateMachine<CharacterState>();

        // 创建状态
        _idle = new IdleState(this);
        _walk = new WalkState(this);
        _run = new RunState(this);

        // 设置初始状态
        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        // 获取输入
        float speed = Input.GetAxis("Vertical");
        bool isRunning = Input.GetKey(KeyCode.LeftShift);

        // 状态转换逻辑
        if (speed > 0.1f)
        {
            if (isRunning)
            {
                _stateMachine.TrySetState(_run);
            }
            else
            {
                _stateMachine.TrySetState(_walk);
            }
        }
        else
        {
            _stateMachine.TrySetState(_idle);
        }
    }

    // 基础状态类
    public abstract class CharacterState : IState
    {
        protected readonly BasicCharacterController Controller;

        public CharacterState(BasicCharacterController controller)
        {
            Controller = controller;
        }

        public virtual bool CanEnterState => true;
        public virtual bool CanExitState => true;

        public abstract void OnEnterState();
        public abstract void OnExitState();
    }

    // Idle状态
    public class IdleState : CharacterState
    {
        public IdleState(BasicCharacterController controller) : base(controller) { }

        public override void OnEnterState()
        {
            Controller._animancer.Play(Controller._idleClip);
            Debug.Log("进入Idle状态");
        }

        public override void OnExitState()
        {
            Debug.Log("退出Idle状态");
        }
    }

    // Walk状态
    public class WalkState : CharacterState
    {
        public WalkState(BasicCharacterController controller) : base(controller) { }

        public override void OnEnterState()
        {
            Controller._animancer.Play(Controller._walkClip);
            Debug.Log("进入Walk状态");
        }

        public override void OnExitState()
        {
            Debug.Log("退出Walk状态");
        }
    }

    // Run状态
    public class RunState : CharacterState
    {
        public RunState(BasicCharacterController controller) : base(controller) { }

        public override void OnEnterState()
        {
            Controller._animancer.Play(Controller._runClip);
            Debug.Log("进入Run状态");
        }

        public override void OnExitState()
        {
            Debug.Log("退出Run状态");
        }
    }
}
```

### 示例2：战斗系统FSM

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 战斗系统FSM
/// 演示攻击、防御、受击状态管理
/// </summary>
public class CombatSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    private StateMachine<CombatState> _stateMachine;

    private IdleState _idle;
    private AttackState _attack;
    private BlockState _block;
    private HitState _hit;

    void Awake()
    {
        _stateMachine = new StateMachine<CombatState>();

        _idle = new IdleState(this);
        _attack = new AttackState(this);
        _block = new BlockState(this);
        _hit = new HitState(this);

        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            _stateMachine.TrySetState(_attack);
        }

        if (Input.GetKey(KeyCode.Mouse1))
        {
            _stateMachine.TrySetState(_block);
        }
        else if (_stateMachine.CurrentState == _block)
        {
            _stateMachine.TrySetState(_idle);
        }
    }

    // 受到攻击（外部调用）
    public void TakeDamage(int damage)
    {
        _stateMachine.ForceSetState(_hit);
    }

    // 战斗状态基类
    public abstract class CombatState : IState
    {
        protected readonly CombatSystem System;

        public CombatState(CombatSystem system)
        {
            System = system;
        }

        public virtual bool CanEnterState => true;
        public virtual bool CanExitState => true;

        public abstract void OnEnterState();
        public virtual void OnExitState() { }
    }

    // Idle状态
    public class IdleState : CombatState
    {
        public IdleState(CombatSystem system) : base(system) { }

        public override void OnEnterState()
        {
            Debug.Log("战斗Idle");
        }
    }

    // Attack状态
    public class AttackState : CombatState
    {
        private bool _attackFinished;

        public AttackState(CombatSystem system) : base(system) { }

        // 攻击未完成时不能退出
        public override bool CanExitState => _attackFinished;

        public override void OnEnterState()
        {
            Debug.Log("开始攻击");
            _attackFinished = false;

            // 播放攻击动画并监听结束事件
            var state = System._animancer.Play(System._attackClip);
            state.Events.OnEnd = OnAttackFinished;
        }

        void OnAttackFinished()
        {
            _attackFinished = true;
            Debug.Log("攻击完成");

            // 自动返回Idle
            System._stateMachine.TrySetState(System._idle);
        }
    }

    // Block状态
    public class BlockState : CombatState
    {
        public BlockState(CombatSystem system) : base(system) { }

        public override void OnEnterState()
        {
            Debug.Log("防御姿态");
        }

        public override void OnExitState()
        {
            Debug.Log("取消防御");
        }
    }

    // Hit状态（受击）
    public class HitState : CombatState
    {
        private bool _hitFinished;

        public HitState(CombatSystem system) : base(system) { }

        public override bool CanExitState => _hitFinished;

        public override void OnEnterState()
        {
            Debug.Log("受到攻击");
            _hitFinished = false;

            var state = System._animancer.Play(System._hitClip);
            state.Events.OnEnd = () => {
                _hitFinished = true;
                System._stateMachine.TrySetState(System._idle);
            };
        }
    }

    [SerializeField] private AnimationClip _attackClip;
    [SerializeField] private AnimationClip _hitClip;
}
```

### 示例3：带Update的状态

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 带Update方法的状态系统
/// 演示如何在状态中实现每帧更新逻辑
/// </summary>
public class UpdatableStateSystem : MonoBehaviour
{
    private StateMachine<UpdatableState> _stateMachine;

    void Awake()
    {
        _stateMachine = new StateMachine<UpdatableState>();
        _stateMachine.TrySetState(new PatrolState(this));
    }

    void Update()
    {
        // 调用当前状态的Update
        _stateMachine.CurrentState?.Update();
    }

    // 可更新的状态基类
    public abstract class UpdatableState : IState
    {
        protected readonly UpdatableStateSystem System;

        public UpdatableState(UpdatableStateSystem system)
        {
            System = system;
        }

        public virtual bool CanEnterState => true;
        public virtual bool CanExitState => true;

        public abstract void OnEnterState();
        public virtual void OnExitState() { }

        // 每帧更新方法
        public abstract void Update();
    }

    // 巡逻状态
    public class PatrolState : UpdatableState
    {
        private Vector3[] _waypoints;
        private int _currentWaypoint;
        private float _speed = 2f;

        public PatrolState(UpdatableStateSystem system) : base(system)
        {
            _waypoints = new[]
            {
                new Vector3(0, 0, 0),
                new Vector3(5, 0, 0),
                new Vector3(5, 0, 5),
                new Vector3(0, 0, 5)
            };
        }

        public override void OnEnterState()
        {
            Debug.Log("开始巡逻");
            _currentWaypoint = 0;
        }

        public override void Update()
        {
            // 移动到当前路径点
            Vector3 target = _waypoints[_currentWaypoint];
            Vector3 current = System.transform.position;

            System.transform.position = Vector3.MoveTowards(
                current, target, _speed * Time.deltaTime
            );

            // 到达路径点，切换到下一个
            if (Vector3.Distance(current, target) < 0.1f)
            {
                _currentWaypoint = (_currentWaypoint + 1) % _waypoints.Length;
                Debug.Log($"到达路径点 {_currentWaypoint}");
            }
        }
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **使用基类封装通用逻辑**
```csharp
// ✅ 好：创建状态基类
public abstract class CharacterState : IState
{
    protected CharacterController Controller;

    // 通用逻辑
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;
}
```

2. **状态持有必要的引用**
```csharp
// ✅ 好：通过构造函数传递依赖
public class AttackState : CharacterState
{
    public AttackState(CharacterController controller)
        : base(controller)
    {
    }
}
```

3. **使用TrySetState检查转换结果**
```csharp
// ✅ 好：检查转换是否成功
if (_stateMachine.TrySetState(newState))
{
    Debug.Log("状态切换成功");
}
else
{
    Debug.Log("状态切换失败");
}
```

4. **在OnExitState中清理资源**
```csharp
// ✅ 好：清理资源
public override void OnExitState()
{
    UnregisterEvents();
    StopCoroutines();
    ReleaseResources();
}
```

### ❌ DON'T（避免做法）

1. **不要在状态间产生强耦合**
```csharp
// ❌ 差：状态直接引用其他状态
public class StateA : IState
{
    private StateB _stateB; // 强耦合
}
```

2. **不要忘记检查CanEnter/CanExit**
```csharp
// ❌ 差：总是返回true
public bool CanExitState => true; // 可能导致问题
```

3. **不要在状态中直接调用状态切换**
```csharp
// ❌ 差：状态内部切换状态
public override void OnEnterState()
{
    _stateMachine.TrySetState(_otherState); // 不推荐
}
```

---

## FAQ常见问题

### Q1: FSM和动画系统是如何配合的？

**A:** FSM管理逻辑状态，每个状态内部可以播放对应的动画：

```csharp
public override void OnEnterState()
{
    _animancer.Play(_stateAnimation);
}
```

### Q2: 如何实现状态的Update逻辑？

**A:** 在MonoBehaviour的Update中调用：

```csharp
void Update()
{
    _stateMachine.CurrentState?.Update();
}
```

### Q3: CanEnterState和CanExitState有什么用？

**A:** 控制状态转换的条件：

```csharp
// 攻击未完成不能退出
public bool CanExitState => _attackFinished;
```

### Q4: TrySetState 和 ForceSetState 的区别？

**A:**

| 方法 | 检查Can条件 | 使用场景 |
|------|-----------|---------|
| **TrySetState** | ✅ 检查 | 正常状态转换 |
| **ForceSetState** | ❌ 不检查 | 强制转换（如受击） |

### Q5: 如何调试状态机？

**A:** 在状态回调中添加日志：

```csharp
public override void OnEnterState()
{
    Debug.Log($"[{GetType().Name}] Enter");
}
```

---

## 参考资料

### 📚 详细文档
- [FSM Overview](https://kybernetik.com.au/animancer/docs/manual/fsm/overview)
- [State Types](https://kybernetik.com.au/animancer/docs/manual/fsm/state-types)
- [Initialization](https://kybernetik.com.au/animancer/docs/manual/fsm/initialization/)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)
- [FSM Utilities](https://kybernetik.com.au/animancer/docs/manual/fsm/utilities/)

### 🔗 示例资源
- [FSM 示例](https://kybernetik.com.au/animancer/docs/samples/)
- [3D Game Kit 示例](https://kybernetik.com.au/animancer/docs/samples/)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
