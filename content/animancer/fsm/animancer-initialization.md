---
title: "Animancer FSM - Initialization"
date: 2025-12-25
draft: false
---

# Animancer FSM - Initialization 官方文档

## 概述

本文档介绍在Animancer中创建和初始化有限状态机（FSM）的方法。

## 两种初始化方式

### 方式1：序列化字段（推荐用于Inspector可见）

```csharp
[DefaultExecutionOrder(-10000)]
public class Character : MonoBehaviour
{
    [SerializeField] private StateMachine<MyState> _StateMachine;
    public StateMachine<MyState> StateMachine => _StateMachine;

    protected virtual void Awake()
    {
        _StateMachine.InitializeAfterDeserialize();
    }
}
```

**关键点：**
- 使用 `[DefaultExecutionOrder(-10000)]` 确保提前初始化
- 调用 `InitializeAfterDeserialize()` 方法

### 方式2：只读字段（推荐用于代码初始化）

```csharp
public class Character : MonoBehaviour
{
    public readonly StateMachine<MyState> StateMachine = new();

    protected virtual void Awake()
    {
        StateMachine.TrySetState(firstState);
    }
}
```

## 避免的做法

❌ **在Awake中创建**：其他脚本可能执行更早
❌ **字段初始化器**：无法访问实例字段
❌ **构造函数**：执行时序早于Unity序列化系统

## 默认状态功能

使用 `StateMachine<TState>.WithDefault` 设置默认状态：

```csharp
var stateMachine = new StateMachine<MyState>.WithDefault(defaultState);
// 当无当前状态时自动进入默认状态
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
