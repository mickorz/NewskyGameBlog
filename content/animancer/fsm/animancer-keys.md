---
title: "Animancer FSM - Keys"
date: 2025-12-25
draft: false
---

# Animancer FSM - Keys 官方文档

## 两种状态机实现

### 1. Keyless StateMachine<TState>（无键）

```csharp
public class KeylessExample : MonoBehaviour
{
    private StateMachine<IState> _fsm;
    private IdleState _idle;
    private WalkState _walk;

    void Awake()
    {
        _fsm = new StateMachine<IState>();
        _idle = new IdleState();
        _walk = new WalkState();

        // 需要直接引用状态对象
        _fsm.TrySetState(_idle);
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
            _fsm.TrySetState(_walk); // 直接引用
        else
            _fsm.TrySetState(_idle);
    }
}
```

**优点：** 简单、易调试、无额外开销
**缺点：** 需要持有所有状态引用

### 2. Keyed StateMachine<TKey, TState>（有键）

```csharp
public class KeyedExample : MonoBehaviour
{
    public enum StateKey { Idle, Walk, Run }

    private StateMachine<StateKey, IState> _fsm;

    void Awake()
    {
        _fsm = new StateMachine<StateKey, IState>();

        // 注册状态和键的映射
        _fsm.Add(StateKey.Idle, new IdleState());
        _fsm.Add(StateKey.Walk, new WalkState());
        _fsm.Add(StateKey.Run, new RunState());

        // 使用键切换状态
        _fsm.ForceSetState(StateKey.Idle);
    }

    void Update()
    {
        float speed = Input.GetAxis("Vertical");
        bool sprint = Input.GetKey(KeyCode.LeftShift);

        if (speed > 0.1f)
        {
            // 使用键切换，无需状态对象引用
            _fsm.TrySetState(sprint ? StateKey.Run : StateKey.Walk);
        }
        else
        {
            _fsm.TrySetState(StateKey.Idle);
        }
    }
}
```

**优点：**
- 支持序列化（保存/加载）
- 网络同步友好（传输枚举值）
- 降低组件间耦合

**缺点：** 需要额外的键管理

## 网络同步示例

```csharp
// 发送状态键而非状态对象
[Command]
void CmdChangeState(StateKey key)
{
    _fsm.TrySetState(key);
}

// 同步到客户端
[ClientRpc]
void RpcSyncState(StateKey key)
{
    _fsm.ForceSetState(key);
}
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
