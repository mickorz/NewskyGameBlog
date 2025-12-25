# Animancer - Transparency 透明性

## 📋 目录
- [核心理念](#核心理念)
- [Mecanim的问题](#mecanim的问题)
- [Animancer的解决](#animancer的解决)
- [代码对比](#代码对比)
- [参考资料](#参考资料)

---

## 核心理念

> **"追逐两只兔子，一只都抓不到" - 孔子**

Mecanim试图同时做两件事：
1. 动画系统
2. 有限状态机

Animancer专注于做好一件事：**动画管理**

---

## Mecanim的问题

### 1. 混合职责

```
Animator Controller = 动画系统 + FSM
         ↓
    都做得不够好
```

**动画系统的问题：**
- 内部逻辑不可见
- 无法调试
- 延迟执行

**FSM的问题：**
- 强制使用特定的逻辑定义方式
- 无法自由修改
- 无法访问源代码

### 2. 黑盒系统

```csharp
// Mecanim - 无法知道内部发生了什么
_animator.Play("Walk");
// 🤔 它真的播放了吗？
// 🤔 什么时候开始播放？
// 🤔 为什么没有播放？
// ❌ 无法调试
```

### 3. 延迟反馈

```csharp
// 调用Play
_animator.Play("Jump");

// 立即检查状态
var info = _animator.GetCurrentAnimatorStateInfo(0);
if (info.IsName("Jump"))
{
    // ❌ 永远不会进入这里！
    // 因为状态还没更新
}
```

---

## Animancer的解决

### 1. 职责分离

```
Animancer = 纯动画系统
FSM系统 = 独立的状态机（可选）
         ↓
    各司其职，都做得很好
```

### 2. 完全透明

```csharp
// Animancer - 完全可见
var state = _animancer.Play(_walk);

// ✅ 立即获取所有信息
Debug.Log($"Is Playing: {state.IsPlaying}");
Debug.Log($"Length: {state.Length}");
Debug.Log($"Time: {state.Time}");
Debug.Log($"Weight: {state.Weight}");
Debug.Log($"Speed: {state.Speed}");
```

### 3. 源代码访问

**Pro版本：**
- ✅ 包含完整Animancer源代码
- ✅ 可以调试内部实现
- ✅ 可以修改和扩展

**Lite版本：**
- ✅ FSM系统源代码包含
- ✅ 可以自由修改FSM

---

## 代码对比

### 状态切换

**Mecanim - 延迟执行，无反馈：**

```csharp
// 调用方法
_animator.Play("State Name");

// ❌ 无返回值
// ❌ 不知道是否成功
// ❌ 需要等待下一帧才能确认
```

**Animancer - 即时执行，有反馈：**

```csharp
// FSM方式
bool success = _stateMachine.TrySetState(state);

if (success)
{
    Debug.Log("成功切换状态");
}
else
{
    Debug.Log("无法切换状态");
    // 可以检查原因：
    if (!state.CanEnterState)
        Debug.Log("CanEnterState返回false");
}
```

### 调试动画

**Mecanim - 黑盒：**

```csharp
// 播放动画
_animator.Play("Attack");

// ❓ 无法知道：
// - 为什么没播放？
// - 过渡参数是什么？
// - 当前权重是多少？
// - 混合了哪些动画？
```

**Animancer - 透明：**

```csharp
// 播放动画
var state = _animancer.Play(_attack);

// ✅ 可以检查所有细节
Debug.Log($"Current State: {_animancer.States.Current}");
Debug.Log($"Previous State: {_animancer.States.Previous}");
Debug.Log($"Layer Count: {_animancer.Layers.Count}");

// ✅ 可以遍历所有状态
foreach (var s in _animancer.States)
{
    Debug.Log($"State: {s.Key}, Weight: {s.Weight}");
}
```

### FSM实现

**Mecanim - 固定实现：**

```csharp
// ❌ 无法修改FSM行为
// ❌ 必须使用Animator Controller的方式
// ❌ 无法访问源代码
```

**Animancer - 开源FSM：**

```csharp
// ✅ 完整的FSM源代码
// ✅ 可以自由修改
// ✅ 可以扩展功能

public class MyCustomState : StateBehaviour
{
    // 可以添加自定义逻辑
    public override void OnEnterState()
    {
        base.OnEnterState();
        // 自定义进入逻辑
    }

    public override bool CanEnterState
    {
        get
        {
            // 自定义条件检查
            return myCustomCondition;
        }
    }
}
```

---

## 实战优势

### 1. 即时调试

```csharp
void Update()
{
    // Animancer - 实时监控
    var current = _animancer.States.Current;
    if (current != null)
    {
        Debug.Log($"Playing: {current.Key}");
        Debug.Log($"Time: {current.Time}/{current.Length}");
        Debug.Log($"Progress: {current.NormalizedTime * 100}%");
    }
}
```

### 2. 精确控制

```csharp
// 完全掌控动画播放
var state = _animancer.Play(_attack);

// 随时可以：
state.Time = 0.5f;              // 跳转到0.5秒
state.NormalizedTime = 0.5f;    // 跳转到50%
state.Speed = 2f;               // 2倍速
state.Weight = 0.5f;            // 50%权重
state.IsPlaying = false;        // 暂停
```

### 3. 条件检查

```csharp
// 检查为什么无法切换状态
if (!_walkState.CanEnterState)
{
    Debug.Log("无法进入Walk状态，原因：");

    // 自定义的条件检查
    if (!IsGrounded())
        Debug.Log("- 不在地面上");
    if (IsStunned())
        Debug.Log("- 被击晕");
    if (IsDead())
        Debug.Log("- 已死亡");
}
```

---

## 最佳实践

### ✅ 利用透明性优势

```csharp
// 1. 实时监控
void OnGUI()
{
    var current = _animancer.States.Current;
    if (current != null)
    {
        GUILayout.Label($"Current: {current.Key}");
        GUILayout.Label($"Weight: {current.Weight:F2}");
        GUILayout.Label($"Time: {current.Time:F2}s");
    }
}

// 2. 详细日志
void LogAnimationState(AnimancerState state)
{
    Debug.Log($"=== Animation State ===");
    Debug.Log($"Clip: {state.Clip.name}");
    Debug.Log($"Length: {state.Length}s");
    Debug.Log($"Speed: {state.Speed}x");
    Debug.Log($"Weight: {state.Weight}");
    Debug.Log($"IsPlaying: {state.IsPlaying}");
    Debug.Log($"IsLooping: {state.IsLooping}");
}

// 3. 条件追踪
void TraceStateTransition()
{
    var previous = _animancer.States.Previous;
    var current = _animancer.States.Current;

    Debug.Log($"Transition: {previous?.Key} → {current?.Key}");
}
```

---

## 参考资料

### 📚 相关文档
- [\1](./animancer-why.md)
- [\1](./animancer-simplicity.md)
- [\1](../fsm/animancer-fsm.md)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
