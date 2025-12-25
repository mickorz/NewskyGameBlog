---
title: "Animancer - Simplicity 简洁性"
date: 2025-12-25
draft: false
---

# Animancer - Simplicity 简洁性

## 📋 目录
- [核心原则](#核心原则)
- [复杂度对比](#复杂度对比)
- [控制灵活性](#控制灵活性)
- [参考资料](#参考资料)

---

## 核心原则

> **动画系统应该只需要两个输入：要动画的对象 + 要播放的动画**

### 理想方案

```csharp
thing.Play(animation);
```

---

## 复杂度对比

### Mecanim方式：7个步骤

```
1. 获取Animator组件
    ↓
2. 创建Animator Controller资产
    ↓
3. 分配到Controller字段
    ↓
4. 创建状态
    ↓
5. 给状态命名
    ↓
6. 分配动画片段
    ↓
7. 调用Play方法
```

**代码：**
```csharp
_animator.Play("StateName"); // 需要7步准备工作
```

### Animancer方式：1个步骤

```csharp
[SerializeField] private AnimancerComponent _animancer;
[SerializeField] private AnimationClip _clip;

_animancer.Play(_clip); // 仅此而已
```

---

## 控制灵活性

### Mecanim的限制

| 功能 | Mecanim | Animancer |
|------|---------|-----------|
| **即时播放** | ❌ 需要预配置 | ✅ 直接播放 |
| **运行时修改过渡** | ❌ 不可能 | ✅ 随时修改 |
| **动态速度调整** | ⚠️ 需要参数 | ✅ 直接设置 |
| **运行时Layer Mask** | ❌ 不支持 | ✅ 支持 |
| **Inspector手动播放** | ❌ 不支持 | ✅ 支持 |

### 代码示例

**运行时修改过渡时间：**

```csharp
// Mecanim - 不可能
// Controller中的过渡时间是固定的

// Animancer - 简单
_animancer.Play(_clip, fadeDuration: 0.5f); // 随时修改
```

**动态速度调整：**

```csharp
// Mecanim - 需要参数
// 1. 创建Float参数 "SpeedMultiplier"
// 2. 在状态中设置Parameter
_animator.SetFloat("SpeedMultiplier", 2f);

// Animancer - 直接设置
var state = _animancer.Play(_clip);
state.Speed = 2f;
```

**运行时修改Layer Mask：**

```csharp
// Mecanim - 不支持
// Layer Mask必须在Controller中预先配置

// Animancer - 支持
var layer = _animancer.Layers[1];
layer.SetMask(_upperBodyMask); // 运行时修改
```

---

## 规模化问题

### Mecanim Controller 的混乱

> **"随着复杂度增加，Controller会变成无法组织的混乱网络"**

```
简单Controller (5个状态)
  ↓
中等Controller (20个状态)
  ↓
复杂Controller (50+个状态)
  ↓
❌ 混乱的意大利面网络
```

**Unity官方示例的问题：**
即使是Unity官方博客中的示例，也会随着复杂度增加而"变成无法轻松组织的混乱网络"。

### Animancer 的可扩展性

```csharp
// 小型系统
public class SimpleCharacter : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
}

// 大型系统 - 模块化组织
public class ComplexCharacter : MonoBehaviour
{
    [SerializeField] private MovementAnimations _movement;
    [SerializeField] private CombatAnimations _combat;
    [SerializeField] private InteractionAnimations _interactions;
}

[System.Serializable]
public class MovementAnimations
{
    public AnimationClip Idle;
    public AnimationClip Walk;
    public AnimationClip Run;
    public AnimationClip Jump;
}
```

---

## 实战对比

### 场景：播放攻击动画

**Mecanim：**

1. 打开Animator Controller
2. 创建"Attack"状态
3. 分配动画片段
4. 创建Bool参数"IsAttacking"
5. 创建Idle→Attack过渡
6. 设置过渡条件：IsAttacking == true
7. 创建Attack→Idle过渡
8. 设置Exit Time

```csharp
// 代码中
_animator.SetBool("IsAttacking", true);
// 需要在某处重置为false
```

**Animancer：**

```csharp
void Attack()
{
    var state = _animancer.Play(_attackClip);
    state.Events.OnEnd = () => _animancer.Play(_idleClip);
}
```

---

## 最佳实践

### ✅ Animancer的简洁优势

```csharp
// 1. 无需预配置
_animancer.Play(_newClip); // 立即播放任何Clip

// 2. 灵活的淡入时间
_animancer.Play(_clip, 0.1f);  // 快速切换
_animancer.Play(_clip, 0.5f);  // 平滑切换

// 3. 动态控制
var state = _animancer.Play(_clip);
state.Speed = 2f;        // 速度
state.Time = 0.5f;       // 时间
state.Weight = 0.8f;     // 权重
state.IsLooping = false; // 循环

// 4. 即时事件
state.Events.OnEnd = OnComplete;
state.Events.AddNormalized(0.5f, OnHalfway);
```

---

## 参考资料

### 📚 相关文档
- [\1]({{< ref "animancer-why.md" >}})
- [\1]({{< ref "animancer-transparency.md" >}})
- [\1]({{< ref "animancer-adaptability.md" >}})

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
