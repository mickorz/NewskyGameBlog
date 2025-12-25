---
title: "Animancer FSM - Input Buffer"
date: 2025-12-25
draft: false
---

# Animancer FSM - Input Buffer 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [使用步骤](#使用步骤)
- [代码示例](#代码示例)
- [重要限制](#重要限制)
- [参考资料](#参考资料)

---

## 概述

**Input Buffer（输入缓冲）** 允许状态机在无法立即转换时将状态变更请求加入队列，并在指定时间内重试转换。

### 🎯 典型应用场景

> **"如果玩家正在攻击并再次按下攻击键，你可能希望当前动画先完成，然后只要输入没有发生太久之前，就开始连击中的下一次攻击"**

---

## 核心概念

### 🔄 工作流程

```
玩家输入攻击
    ↓
当前状态：Attack1（无法退出）
    ↓
Buffer(Attack2, 0.5秒)  ← 缓冲输入
    ↓
每帧 Update()
    ↓
Attack1完成 → TrySetState(Attack2) ✅ 成功！
```

### 📊 Buffer vs 直接切换

| 方式 | 行为 | 结果 |
|------|------|------|
| **TrySetState** | 立即尝试切换 | 失败则丢弃输入 |
| **Buffer** | 缓冲输入并重试 | 在超时前持续尝试 |

---

## 使用步骤

### 步骤1：创建 InputBuffer

```csharp
using Animancer.FSM;
using UnityEngine;

public class CombatController : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;
    private StateMachine<IState>.InputBuffer _inputBuffer;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();

        // 创建InputBuffer
        _inputBuffer = new StateMachine<IState>.InputBuffer(_stateMachine);
    }
}
```

### 步骤2：缓冲输入

```csharp
void Update()
{
    if (Input.GetKeyDown(KeyCode.Mouse0))
    {
        // 使用Buffer代替TrySetState
        // 参数：状态，超时时间（秒）
        _inputBuffer.Buffer(_attackState, 0.5f);
    }
}
```

### 步骤3：每帧更新

```csharp
void Update()
{
    // 每帧调用Update重试缓冲的状态
    _inputBuffer.Update();

    // 处理输入...
}
```

---

## 代码示例

### 示例1：基础连击系统

```csharp
using Animancer;
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 使用InputBuffer实现连击系统
/// </summary>
public class ComboSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    private StateMachine<AttackState> _stateMachine;
    private StateMachine<AttackState>.InputBuffer _inputBuffer;

    private IdleState _idle;
    private Attack1State _attack1;
    private Attack2State _attack2;
    private Attack3State _attack3;

    [Header("缓冲设置")]
    [SerializeField] private float _bufferTimeout = 0.5f; // 输入缓冲时间

    void Awake()
    {
        // 初始化状态机
        _stateMachine = new StateMachine<AttackState>();
        _inputBuffer = new StateMachine<AttackState>.InputBuffer(_stateMachine);

        // 创建状态
        _idle = new IdleState(this);
        _attack1 = new Attack1State(this);
        _attack2 = new Attack2State(this);
        _attack3 = new Attack3State(this);

        _stateMachine.TrySetState(_idle);
    }

    void Update()
    {
        // 每帧更新InputBuffer
        _inputBuffer.Update();

        // 处理攻击输入
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            HandleAttackInput();
        }
    }

    void HandleAttackInput()
    {
        var current = _stateMachine.CurrentState;

        if (current == _idle)
        {
            // 从Idle直接进入Attack1
            _stateMachine.TrySetState(_attack1);
        }
        else if (current == _attack1)
        {
            // 缓冲Attack2
            _inputBuffer.Buffer(_attack2, _bufferTimeout);
            Debug.Log("缓冲Attack2输入");
        }
        else if (current == _attack2)
        {
            // 缓冲Attack3
            _inputBuffer.Buffer(_attack3, _bufferTimeout);
            Debug.Log("缓冲Attack3输入");
        }
    }

    // 状态基类
    public abstract class AttackState : IState
    {
        protected ComboSystem Controller;
        protected bool _attackFinished;

        public AttackState(ComboSystem controller)
        {
            Controller = controller;
        }

        public virtual bool CanEnterState => true;

        // 攻击未完成不能退出
        public bool CanExitState => _attackFinished;

        public abstract void OnEnterState();

        public virtual void OnExitState()
        {
            _attackFinished = false;
        }
    }

    // Idle状态
    public class IdleState : AttackState
    {
        public IdleState(ComboSystem controller) : base(controller) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Idle");
            Controller._animancer.Play(Controller._idleClip);
        }
    }

    // Attack1状态
    public class Attack1State : AttackState
    {
        public Attack1State(ComboSystem controller) : base(controller) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Attack1");
            _attackFinished = false;

            var state = Controller._animancer.Play(Controller._attack1Clip);
            state.Events.OnEnd = () =>
            {
                _attackFinished = true;
                Controller._stateMachine.TrySetState(Controller._idle);
            };
        }
    }

    // Attack2状态
    public class Attack2State : AttackState
    {
        public Attack2State(ComboSystem controller) : base(controller) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Attack2 (从缓冲进入)");
            _attackFinished = false;

            var state = Controller._animancer.Play(Controller._attack2Clip);
            state.Events.OnEnd = () =>
            {
                _attackFinished = true;
                Controller._stateMachine.TrySetState(Controller._idle);
            };
        }
    }

    // Attack3状态
    public class Attack3State : AttackState
    {
        public Attack3State(ComboSystem controller) : base(controller) { }

        public override void OnEnterState()
        {
            Debug.Log("→ Attack3 (从缓冲进入)");
            _attackFinished = false;

            var state = Controller._animancer.Play(Controller._attack3Clip);
            state.Events.OnEnd = () =>
            {
                _attackFinished = true;
                Controller._stateMachine.TrySetState(Controller._idle);
            };
        }
    }

    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private AnimationClip _attack1Clip;
    [SerializeField] private AnimationClip _attack2Clip;
    [SerializeField] private AnimationClip _attack3Clip;
}
```

### 示例2：带缓冲的跳跃系统

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 使用InputBuffer的跳跃系统
/// 允许在空中时缓冲跳跃输入
/// </summary>
public class JumpSystem : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;
    private StateMachine<IState>.InputBuffer _inputBuffer;

    private GroundedState _grounded;
    private JumpState _jump;

    [SerializeField] private float _jumpBufferTime = 0.2f;

    void Awake()
    {
        _stateMachine = new StateMachine<IState>();
        _inputBuffer = new StateMachine<IState>.InputBuffer(_stateMachine);

        _grounded = new GroundedState();
        _jump = new JumpState();

        _stateMachine.TrySetState(_grounded);
    }

    void Update()
    {
        _inputBuffer.Update();

        // 跳跃输入
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 缓冲跳跃输入
            // 如果在空中，落地后会自动执行跳跃
            _inputBuffer.Buffer(_jump, _jumpBufferTime);
            Debug.Log("缓冲跳跃输入");
        }
    }

    // Grounded状态
    public class GroundedState : IState
    {
        public bool CanEnterState => IsGrounded();
        public bool CanExitState => true;

        public void OnEnterState()
        {
            Debug.Log("落地");
        }

        public void OnExitState() { }

        bool IsGrounded()
        {
            // 实际项目中的地面检测逻辑
            return Physics.Raycast(
                transform.position,
                Vector3.down,
                1.1f
            );
        }
    }

    // Jump状态
    public class JumpState : IState
    {
        public bool CanEnterState => true;
        public bool CanExitState => true;

        public void OnEnterState()
        {
            Debug.Log("跳跃！");
            // 应用跳跃力
        }

        public void OnExitState() { }
    }
}
```

### 示例3：检查缓冲状态

```csharp
using Animancer.FSM;
using UnityEngine;

/// <summary>
/// 检查和清除缓冲状态
/// </summary>
public class BufferInspection : MonoBehaviour
{
    private StateMachine<IState> _stateMachine;
    private StateMachine<IState>.InputBuffer _inputBuffer;

    void Update()
    {
        _inputBuffer.Update();

        // 检查是否有缓冲的状态
        if (_inputBuffer.IsActive)
        {
            Debug.Log($"缓冲中: {_inputBuffer.State}");
            Debug.Log($"剩余时间: {_inputBuffer.TimeLeft}秒");
        }

        // 取消缓冲
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            _inputBuffer.Clear();
            Debug.Log("清除输入缓冲");
        }
    }
}
```

---

## 重要限制

### ⚠️ 单一缓冲限制

> **"系统设计上一次只处理一个缓冲状态。如果在缓冲状态执行前发生多个输入，只保留最近的输入。"**

```csharp
// 快速连续输入
_inputBuffer.Buffer(attack1, 0.5f);  // 缓冲Attack1
_inputBuffer.Buffer(attack2, 0.5f);  // 覆盖为Attack2
_inputBuffer.Buffer(attack3, 0.5f);  // 覆盖为Attack3

// 最终只会执行Attack3
```

### 💡 解决方案：序列缓冲

如果需要顺序执行多个命令，可以创建 `InputSequenceBuffer` 变体：

```csharp
/// <summary>
/// 输入序列缓冲（自定义实现）
/// 管理一个状态列表
/// </summary>
public class InputSequenceBuffer
{
    private Queue<IState> _bufferedStates = new Queue<IState>();
    private StateMachine<IState> _stateMachine;
    private float _timeout;

    public InputSequenceBuffer(StateMachine<IState> stateMachine)
    {
        _stateMachine = stateMachine;
    }

    public void Buffer(IState state, float timeout)
    {
        _bufferedStates.Enqueue(state);
        _timeout = timeout;
    }

    public void Update()
    {
        if (_bufferedStates.Count == 0) return;

        _timeout -= Time.deltaTime;

        if (_timeout <= 0)
        {
            _bufferedStates.Clear();
            return;
        }

        var nextState = _bufferedStates.Peek();
        if (_stateMachine.TrySetState(nextState))
        {
            _bufferedStates.Dequeue();
            Debug.Log($"执行缓冲状态: {nextState}");
        }
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **合理设置超时时间**
```csharp
// ✅ 好：根据游戏节奏设置
_inputBuffer.Buffer(nextState, 0.3f); // 快节奏
_inputBuffer.Buffer(nextState, 0.8f); // 慢节奏
```

2. **每帧调用Update**
```csharp
// ✅ 好：在Update中调用
void Update()
{
    _inputBuffer.Update();
}
```

3. **检查是否已有缓冲**
```csharp
// ✅ 好：避免覆盖重要输入
if (!_inputBuffer.IsActive)
{
    _inputBuffer.Buffer(state, timeout);
}
```

### ❌ DON'T（避免做法）

1. **超时时间过长**
```csharp
// ❌ 差：太长的缓冲时间影响手感
_inputBuffer.Buffer(state, 2.0f); // 太长！
```

2. **忘记调用Update**
```csharp
// ❌ 差：不调用Update，缓冲永远不会执行
void Update()
{
    // 忘记调用 _inputBuffer.Update();
}
```

---

## 参考资料

### 📚 相关文档
- [FSM 主页](https://kybernetik.com.au/animancer/docs/manual/fsm/)
- [Changing States](https://kybernetik.com.au/animancer/docs/manual/fsm/changing-states)
- [Weapons Sample](https://kybernetik.com.au/animancer/docs/samples/fsm/weapons#attack-input)

### 💡 源代码
- 路径: `Assets/Plugins/Animancer/Utilities/FSM/`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
