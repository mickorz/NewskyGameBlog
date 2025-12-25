# Animancer FSM - State Selector 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [使用步骤](#使用步骤)
- [优先级设置](#优先级设置)
- [代码示例](#代码示例)
- [参考资料](#参考资料)

---

## 概述

**State Selector（状态选择器）** 提供了一种简单的方式来管理优先级排序的潜在状态列表。

> **"`StateSelector` 类提供了一种简单的方式来管理优先级排序的潜在状态列表"**

### 🎯 典型应用场景

- AI决策系统
- 自动状态选择
- 优先级行为管理

---

## 核心概念

### 🔄 工作流程

```
请求状态切换
    ↓
StateSelector 按优先级评估状态列表
    ├─ 高优先级状态（如：Death）
    ├─ 中优先级状态（如：Attack）
    └─ 低优先级状态（如：Idle）
    ↓
第一个满足 CanEnterState 的状态被选中
    ↓
成功进入 → 自动清空选择器
```

### 📊 优先级系统

| 优先级 | 值 | 典型状态 |
|--------|-----|---------|
| **最高** | 100+ | Death, Stunned |
| **高** | 50-99 | Attack, Skill |
| **中** | 10-49 | Walk, Run |
| **低** | 0-9 | Idle |

---

## 使用步骤

### 步骤1：创建 StateSelector

```csharp
using Animancer.FSM;
using UnityEngine;

public class AIController : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;
    private StateMachine<IState>.StateSelector _selector;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();

        // 创建StateSelector
        _selector = new StateMachine<IState>.StateSelector(_stateMachine);
    }
}
```

### 步骤2：添加状态（带优先级）

```csharp
void Awake()
{
    _stateMachine = new StateMachine<IState>();
    _selector = new StateMachine<IState>.StateSelector(_stateMachine);

    // 添加状态并设置优先级（优先级越高越先评估）
    _selector.Add(_deathState, 100);  // 最高优先级
    _selector.Add(_attackState, 50);   // 高优先级
    _selector.Add(_walkState, 10);     // 中优先级
    _selector.Add(_idleState, 0);      // 低优先级（默认）
}
```

### 步骤3：请求状态切换

```csharp
void Update()
{
    // 使用StateSelector的方法自动选择最高优先级的可用状态
    _selector.TrySetState();

    // 或使用ResetState
    // _selector.TryResetState();

    // 或强制设置
    // _selector.ForceSetState();
}
```

### 步骤4：自动清空

状态成功进入后，选择器会**自动清空**，需要重新添加状态。

---

## 优先级设置

### 方式1：参数设置（推荐）

```csharp
// 添加状态时传入优先级
_selector.Add(_deathState, 100);
_selector.Add(_attackState, 50);
_selector.Add(_idleState, 0);
```

### 方式2：接口实现

```csharp
/// <summary>
/// 实现IPrioritizable接口
/// </summary>
public interface IPrioritizable
{
    int Priority { get; }
}

/// <summary>
/// 状态基类实现优先级
/// </summary>
public abstract class PrioritizedState : IState, IPrioritizable
{
    public abstract int Priority { get; }

    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;
    public abstract void OnEnterState();
    public virtual void OnExitState() { }
}

// 使用示例
public class DeathState : PrioritizedState
{
    public override int Priority => 100; // 最高优先级
    public override void OnEnterState() => Debug.Log("Death");
}

public class AttackState : PrioritizedState
{
    public override int Priority => 50;
    public override void OnEnterState() => Debug.Log("Attack");
}

// 添加时无需指定优先级
_selector.Add(_deathState);  // 自动使用 Priority 属性
_selector.Add(_attackState);
```

---

## 代码示例

### 示例1：AI决策系统

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// AI决策系统
/// 使用StateSelector自动选择最合适的行为
/// </summary>
public class AIBehaviorSystem : MonoBehaviour
{
    [SerializeField] private Transform _target;
    [SerializeField] private float _attackRange = 2f;
    [SerializeField] private float _chaseRange = 10f;

    private StateMachine<AIState> _stateMachine;
    private StateMachine<AIState>.StateSelector _selector;

    // 状态实例
    private IdleState _idle;
    private PatrolState _patrol;
    private ChaseState _chase;
    private AttackState _attack;

    void Awake()
    {
        _stateMachine = new StateMachine<AIState>();
        _selector = new StateMachine<AIState>.StateSelector(_stateMachine);

        // 创建状态
        _idle = new IdleState(this);
        _patrol = new PatrolState(this);
        _chase = new ChaseState(this);
        _attack = new AttackState(this);

        // 设置初始状态
        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        // 每帧评估状态
        EvaluateStates();
    }

    void EvaluateStates()
    {
        // 清空之前的评估
        // （实际上成功进入状态后会自动清空）

        // 按优先级添加可能的状态
        float distance = Vector3.Distance(transform.position, _target.position);

        // 攻击优先级最高
        if (distance <= _attackRange)
        {
            _selector.Add(_attack, 100);
        }

        // 追逐次之
        if (distance <= _chaseRange)
        {
            _selector.Add(_chase, 50);
        }

        // 巡逻
        _selector.Add(_patrol, 10);

        // Idle最低
        _selector.Add(_idle, 0);

        // 自动选择最高优先级的可用状态
        _selector.TrySetState();
    }

    // AI状态基类
    public abstract class AIState : IState
    {
        protected AIBehaviorSystem AI;

        public AIState(AIBehaviorSystem ai)
        {
            AI = ai;
        }

        public abstract bool CanEnterState { get; }
        public virtual bool CanExitState => true;
        public abstract void OnEnterState();
        public virtual void OnExitState() { }
    }

    // Idle状态
    public class IdleState : AIState
    {
        public IdleState(AIBehaviorSystem ai) : base(ai) { }
        public override bool CanEnterState => true;
        public override void OnEnterState() => Debug.Log("AI: Idle");
    }

    // Patrol状态
    public class PatrolState : AIState
    {
        public PatrolState(AIBehaviorSystem ai) : base(ai) { }
        public override bool CanEnterState => true;
        public override void OnEnterState() => Debug.Log("AI: Patrol");
    }

    // Chase状态
    public class ChaseState : AIState
    {
        public ChaseState(AIBehaviorSystem ai) : base(ai) { }

        public override bool CanEnterState
        {
            get
            {
                float distance = Vector3.Distance(
                    AI.transform.position,
                    AI._target.position
                );
                return distance <= AI._chaseRange && distance > AI._attackRange;
            }
        }

        public override void OnEnterState() => Debug.Log("AI: Chase");
    }

    // Attack状态
    public class AttackState : AIState
    {
        public AttackState(AIBehaviorSystem ai) : base(ai) { }

        public override bool CanEnterState
        {
            get
            {
                float distance = Vector3.Distance(
                    AI.transform.position,
                    AI._target.position
                );
                return distance <= AI._attackRange;
            }
        }

        public override void OnEnterState() => Debug.Log("AI: Attack!");
    }
}
```

### 示例2：使用IPrioritizable接口

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 使用IPrioritizable接口的状态系统
/// </summary>
public class PrioritizedStateSystem : MonoBehaviour
{
    private StateMachine<PriorityState> _stateMachine;
    private StateMachine<PriorityState>.StateSelector _selector;

    void Awake()
    {
        _stateMachine = new StateMachine<PriorityState>();
        _selector = new StateMachine<PriorityState>.StateSelector(_stateMachine);

        // 添加状态（无需手动指定优先级）
        _selector.Add(new CriticalState());  // Priority: 100
        _selector.Add(new HighState());      // Priority: 50
        _selector.Add(new NormalState());    // Priority: 10
        _selector.Add(new LowState());       // Priority: 0

        // 自动按Priority排序
        _selector.TrySetState();
    }
}

/// <summary>
/// 带优先级的状态基类
/// </summary>
public abstract class PriorityState : IState, IPrioritizable
{
    public abstract int Priority { get; }
    public virtual bool CanEnterState => true;
    public virtual bool CanExitState => true;
    public abstract void OnEnterState();
    public virtual void OnExitState() { }
}

public class CriticalState : PriorityState
{
    public override int Priority => 100;
    public override void OnEnterState() => Debug.Log("Critical!");
}

public class HighState : PriorityState
{
    public override int Priority => 50;
    public override void OnEnterState() => Debug.Log("High");
}

public class NormalState : PriorityState
{
    public override int Priority => 10;
    public override void OnEnterState() => Debug.Log("Normal");
}

public class LowState : PriorityState
{
    public override int Priority => 0;
    public override void OnEnterState() => Debug.Log("Low");
}

// IPrioritizable接口定义
public interface IPrioritizable
{
    int Priority { get; }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **合理设置优先级**
```csharp
// ✅ 好：清晰的优先级层级
_selector.Add(_death, 100);    // 致命
_selector.Add(_stunned, 90);   // 控制
_selector.Add(_attack, 50);    // 战斗
_selector.Add(_idle, 0);       // 默认
```

2. **使用IPrioritizable接口**
```csharp
// ✅ 好：优先级封装在状态内
public abstract class CharacterState : IState, IPrioritizable
{
    public virtual int Priority => 0;
}
```

3. **定期评估状态**
```csharp
// ✅ 好：每帧或定时评估
void Update()
{
    EvaluateAndSelectState();
}
```

### ❌ DON'T（避免做法）

1. **优先级混乱**
```csharp
// ❌ 差：优先级不清晰
_selector.Add(_attack, 73);
_selector.Add(_idle, 42);
```

2. **忘记清空选择器**
```csharp
// ❌ 差：重复添加状态
// StateSelector成功后会自动清空，无需担心
```

---

## 参考资料

### 📚 相关文档
- [FSM 主页](https://kybernetik.com.au/animancer/docs/manual/fsm/)
- [State Types](https://kybernetik.com.au/animancer/docs/manual/fsm/state-types)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
