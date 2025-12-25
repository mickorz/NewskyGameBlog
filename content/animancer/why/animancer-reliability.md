# Animancer - Reliability 可靠性

## 📋 目录
- [核心问题](#核心问题)
- [延迟响应问题](#延迟响应问题)
- [命令丢失问题](#命令丢失问题)
- [Animancer的即时可靠性](#animancer的即时可靠性)
- [参考资料](#参考资料)

---

## 核心问题

> **"Animator Controller在下一次更新才会响应，甚至可能不会按预期执行"**

Mecanim的两大可靠性问题：
1. **延迟响应** - 命令要等到下一帧才生效
2. **命令丢失** - 同一帧多个命令会被忽略

---

## 延迟响应问题

### 问题1：状态检查延迟

```csharp
// Mecanim
_animator.Play("Jump");

// ❌ 立即检查 - 错误的结果
var info = _animator.GetCurrentAnimatorStateInfo(0);
if (info.IsName("Jump"))
{
    // 永远不会进入这里！
    // 因为状态还没更新
    Debug.Log("正在跳跃");
}

// ✅ 需要等待下一帧
yield return null; // 等待
var info = _animator.GetCurrentAnimatorStateInfo(0);
if (info.IsName("Jump"))
{
    // 现在可以了
    Debug.Log("正在跳跃");
}
```

### 问题2：无法立即获取信息

```csharp
// Mecanim - 延迟
_animator.Play("Attack");

// ❌ 无法立即获取动画长度
// 需要：
// 1. 等待下一帧
// 2. 查询StateInfo
// 3. 手动计算长度

// Animancer - 即时
var state = _animancer.Play(_attack);
Debug.Log($"动画长度: {state.Length}秒"); // ✅ 立即可用
```

---

## 命令丢失问题

### 问题：同一帧多个Play()命令

```csharp
// 场景：玩家同时按跳跃和攻击
void Update()
{
    bool jump = Input.GetKeyDown(KeyCode.Space);
    bool attack = Input.GetKeyDown(KeyCode.Mouse0);

    // Mecanim
    if (jump)
        _animator.Play("Jump");

    if (attack)
        _animator.Play("Attack");

    // ❌ 问题：只有 Jump 会播放
    // Attack 命令被静默忽略
    // 无任何警告或错误
}
```

### Unity官方示例的问题

> **文档引用Unity 3D Game Kit：角色出现浮空而非播放跳跃动画**

即使是Unity官方团队，也难以可靠使用Mecanim系统。

---

## Animancer的即时可靠性

### 1. 即时响应

```csharp
// Animancer - 立即生效
var state = _animancer.Play(_jump);

// ✅ 立即获取所有信息
Debug.Log($"Is Playing: {state.IsPlaying}");
Debug.Log($"Length: {state.Length}");
Debug.Log($"Time: {state.Time}");
Debug.Log($"NormalizedTime: {state.NormalizedTime}");

// ✅ 立即检查状态
if (_animancer.States.Current == state)
{
    Debug.Log("跳跃动画正在播放");
}
```

### 2. 正确处理多个命令

```csharp
// Animancer - 所有命令都会执行
void Update()
{
    bool jump = Input.GetKeyDown(KeyCode.Space);
    bool attack = Input.GetKeyDown(KeyCode.Mouse0);

    if (jump)
    {
        var jumpState = _animancer.Play(_jump);
        // ✅ 跳跃动画开始播放
    }

    if (attack)
    {
        var attackState = _animancer.Play(_attack);
        // ✅ 攻击动画会覆盖跳跃
        // 行为可预测
    }

    // 最后一个命令生效（符合预期）
}
```

### 3. 便捷的等待方法

```csharp
// 方法1：End Events
void PlayAttack()
{
    var state = _animancer.Play(_attack);
    state.Events.OnEnd = OnAttackComplete;
}

// 方法2：Coroutine
IEnumerator PlayAttackCoroutine()
{
    var state = _animancer.Play(_attack);
    yield return state; // 等待动画结束
    OnAttackComplete();
}

// 方法3：手动检查
void Update()
{
    var state = _animancer.States.Current;
    if (state != null && state.NormalizedTime >= 1f)
    {
        OnAttackComplete();
    }
}
```

---

## 实战对比

### 场景：跳跃系统

**Mecanim方式：**

```csharp
public class MecanimJump : MonoBehaviour
{
    private Animator _animator;
    private bool _isJumping;

    void Jump()
    {
        _animator.Play("Jump");
        // ❌ 无法立即知道动画长度
        // 需要预先计算或延迟检查

        StartCoroutine(WaitForJump());
    }

    IEnumerator WaitForJump()
    {
        // ❌ 需要等待状态更新
        yield return null;

        var info = _animator.GetCurrentAnimatorStateInfo(0);
        if (info.IsName("Jump"))
        {
            _isJumping = true;

            // ❌ 需要手动等待动画结束
            while (info.normalizedTime < 1f)
            {
                yield return null;
                info = _animator.GetCurrentAnimatorStateInfo(0);
            }

            _isJumping = false;
            OnJumpComplete();
        }
    }

    void OnJumpComplete()
    {
        Debug.Log("跳跃完成");
    }
}
```

**Animancer方式：**

```csharp
public class AnimancerJump : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _jump;

    void Jump()
    {
        var state = _animancer.Play(_jump);

        // ✅ 立即获取信息
        Debug.Log($"跳跃动画长度: {state.Length}秒");

        // ✅ 简单的结束回调
        state.Events.OnEnd = OnJumpComplete;
    }

    void OnJumpComplete()
    {
        Debug.Log("跳跃完成");
    }
}
```

---

## 命令可预测性

### Mecanim的不可预测性

```csharp
// 场景：连续播放3个动画
_animator.Play("Anim1");
_animator.Play("Anim2");
_animator.Play("Anim3");

// ❌ 只有Anim1播放
// ❌ Anim2和Anim3被忽略
// ❌ 无警告，无错误
```

### Animancer的可预测性

```csharp
// 场景：连续播放3个动画
_animancer.Play(_anim1);
_animancer.Play(_anim2);
_animancer.Play(_anim3);

// ✅ Anim3会播放（最后一个命令）
// ✅ 行为可预测

// 如果需要按顺序播放：
var state1 = _animancer.Play(_anim1);
state1.Events.OnEnd = () =>
{
    var state2 = _animancer.Play(_anim2);
    state2.Events.OnEnd = () =>
    {
        _animancer.Play(_anim3);
    };
};
```

---

## 最佳实践

### ✅ 利用即时反馈

```csharp
// 检查动画是否成功播放
var state = _animancer.Play(_clip);
if (state.IsPlaying)
{
    Debug.Log("动画正在播放");
}
else
{
    Debug.LogWarning("动画未能播放");
}

// 立即获取动画信息
Debug.Log($"动画: {state.Clip.name}");
Debug.Log($"长度: {state.Length}秒");
Debug.Log($"当前时间: {state.Time}秒");
Debug.Log($"进度: {state.NormalizedTime * 100}%");
```

### ✅ 使用事件系统

```csharp
// 简洁的事件处理
var state = _animancer.Play(_attack);

state.Events.OnEnd = OnAttackEnd;
state.Events.AddNormalized(0.3f, OnAttackHit);
state.Events.AddNormalized(0.7f, OnAttackRecovery);
```

### ✅ Coroutine集成

```csharp
IEnumerator AttackSequence()
{
    // 播放并等待Attack1
    var state1 = _animancer.Play(_attack1);
    yield return state1;

    // 播放并等待Attack2
    var state2 = _animancer.Play(_attack2);
    yield return state2;

    // 播放并等待Attack3
    var state3 = _animancer.Play(_attack3);
    yield return state3;

    // 返回Idle
    _animancer.Play(_idle);
}
```

---

## 参考资料

### 📚 相关文档
- [\1](./animancer-why.md)
- [\1](./animancer-safety.md)
- [\1](../event/animancer-events.md)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
