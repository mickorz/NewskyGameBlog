---
title: "Animancer FSM - Changing States"
date: 2025-12-25
draft: false
---

# Animancer FSM - Changing States 官方文档

## 三种状态切换方法

### 1. TrySetState（推荐）

```csharp
// 尝试进入新状态，如果已是当前状态则返回true
bool success = _stateMachine.TrySetState(newState);
```

- 检查 `CanExitState` 和 `CanEnterState`
- 如果已是当前状态，直接返回true

### 2. TryResetState

```csharp
// 即使已是当前状态，也重新进入
_stateMachine.TryResetState(newState);
```

- 验证退出和进入条件
- 强制重新执行状态转换

### 3. ForceSetState

```csharp
// 跳过所有检查，强制切换
_stateMachine.ForceSetState(newState);
```

- **不检查** `CanExit` 和 `CanEnter`
- 用于强制状态（如死亡、受击）

## 访问状态转换信息

```csharp
// 静态属性访问
var previous = StateChange<MyState>.PreviousState;
var next = StateChange<MyState>.NextState;

// 扩展方法
var previous = this.GetPreviousState<MyState>();
```

## 实用示例

```csharp
// 跳跃状态：只能从地面状态进入
public class JumpState : IState
{
    public bool CanEnterState => IsGrounded();
    public bool CanExitState => true;

    public void OnEnterState() { }
    public void OnExitState() { }

    bool IsGrounded()
    {
        return Physics.Raycast(transform.position, Vector3.down, 1.1f);
    }
}

// 攻击状态：攻击未完成不能退出
public class AttackState : IState
{
    private bool _attackFinished;

    public bool CanEnterState => true;
    public bool CanExitState => _attackFinished;

    public void OnEnterState()
    {
        _attackFinished = false;
        PerformAttack();
    }

    public void OnExitState() { }
}

// 死亡状态：强制进入（跳过检查）
public void Die()
{
    _stateMachine.ForceSetState(_deathState);
}
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
