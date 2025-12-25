# Why Animancer? 为什么选择Animancer？

## 📋 目录
- [概述](#概述)
- [六大问题](#六大问题)
- [Animancer解决方案](#animancer解决方案)
- [参考资料](#参考资料)

---

## 概述

Unity的Mecanim Animator Controller系统存在六个核心问题，Animancer提供了针对性的解决方案。

---

## 六大问题

### 1. 简洁性问题（Simplicity）

**Mecanim的问题：**
> "Everything requires extra steps. To play something you need to make a state, give it an animation, make a parameter, make a transition based on the parameter, and set the parameter with a script."

播放一个动画需要7个步骤：
1. 获取Animator组件
2. 创建Animator Controller资产
3. 分配到Controller字段
4. 创建状态
5. 给状态命名
6. 分配动画
7. 调用Play方法

**Animancer的解决：**
```csharp
_animancer.Play(_clip); // 1行代码
```

---

### 2. 透明性问题（Transparency）

**Mecanim的问题：**
- 无法访问源代码进行调试
- 内部决策过程不可见
- 状态播放没有即时反馈

**Animancer的解决：**
- Pro版本提供完整源代码
- 命令立即执行，可直接检查状态
- 独立的FSM系统（Lite和Pro版都包含源代码）

```csharp
// Mecanim - 延迟执行，无反馈
_animator.Play("State Name");

// Animancer - 立即执行，返回成功/失败
bool success = _stateMachine.TrySetState(state);
```

---

### 3. 适应性问题（Adaptability）

**Mecanim的问题：**
强制将所有动画逻辑集中在单个Animator Controller中，违背了"关注点分离"原则。

**Animancer的解决：**
脚本可以灵活组织动画逻辑：
```csharp
// 按功能模块组织
public class CombatSystem : MonoBehaviour
{
    [SerializeField] private AnimationClip[] _attacks;
}

public class MovementSystem : MonoBehaviour
{
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;
}
```

---

### 4. 清晰性问题（Clarity）

**Mecanim的问题：**
违反"单一责任原则"：
- 查看脚本无法得知需要什么Controller
- 查看Controller无法得知需要什么脚本
- 难以追踪参数使用情况

**Animancer的解决：**
所有依赖在脚本中明确定义：
```csharp
public class Character : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    // 一目了然需要哪些动画
}
```

---

### 5. 安全性问题（Safety）

**Mecanim的问题：**
依赖"魔法字符串"：
```csharp
_animator.Play("Walk"); // 拼写错误运行时才发现
_animator.SetFloat("Speed", 5f); // 参数不存在无警告
```

**五大风险：**
1. 动画状态名称是否在Controller中存在？
2. 有哪些其他可用动画？
3. 动画结束后会发生什么？
4. 重命名时需要修改哪些地方？
5. 脚本是否被多个Controller使用？

**Animancer的解决：**
```csharp
[SerializeField] private AnimationClip _walk;
_animancer.Play(_walk); // 编译时检查
// 未赋值会有编译警告
```

---

### 6. 可靠性问题（Reliability）

**Mecanim的问题：**
> "It responds on the next update, and might not even do what you expect."

**问题1：延迟响应**
```csharp
_animator.Play("Jump");
var info = _animator.GetCurrentAnimatorStateInfo(0);
// info 仍然显示前一个动画！必须等下一帧
```

**问题2：命令丢失**
同一帧内多次调用Play()，只有第一个生效，后续命令被静默忽略。

**Animancer的解决：**
```csharp
var state = _animancer.Play(_jump);
Debug.Log(state.Length); // 立即获取动画长度
Debug.Log(state.IsPlaying); // 立即获取播放状态
```

---

## Animancer解决方案总结

| 问题 | Mecanim | Animancer |
|------|---------|-----------|
| **简洁性** | 7个步骤 | 1行代码 |
| **透明性** | 黑盒系统 | 开源+即时反馈 |
| **适应性** | 强制集中 | 灵活组织 |
| **清晰性** | 依赖不明 | 明确声明 |
| **安全性** | 魔法字符串 | 强类型引用 |
| **可靠性** | 延迟+丢失 | 即时+可靠 |

---

## 代码对比示例

### 播放动画

```csharp
// Mecanim - 复杂
// 1. 创建Controller资产
// 2. 创建状态和参数
// 3. 配置过渡
_animator.SetTrigger("Attack");

// Animancer - 简单
_animancer.Play(_attack);
```

### 等待动画结束

```csharp
// Mecanim - 复杂
IEnumerator WaitForAnimation()
{
    _animator.Play("Attack");
    while (true)
    {
        var info = _animator.GetCurrentAnimatorStateInfo(0);
        if (info.IsName("Attack") && info.normalizedTime >= 1f)
            break;
        yield return null;
    }
    OnComplete();
}

// Animancer - 简单
void PlayAttack()
{
    var state = _animancer.Play(_attack);
    state.Events.OnEnd = OnComplete;
}
```

### 控制速度

```csharp
// Mecanim - 复杂
// 1. 创建Float参数
// 2. 配置Speed Multiplier
_animator.SetFloat("SpeedMultiplier", 1.5f);

// Animancer - 简单
var state = _animancer.Play(_walk);
state.Speed = 1.5f;
```

---

## 参考资料

### 📚 详细文档
- [Simplicity 简洁性](./Animancer_Simplicity官方文档.md)
- [Transparency 透明性](./Animancer_Transparency官方文档.md)
- [Adaptability 适应性](./Animancer_Adaptability官方文档.md)
- [Clarity 清晰性](./Animancer_Clarity官方文档.md)
- [Safety 安全性](./Animancer_Safety官方文档.md)
- [Reliability 可靠性](./Animancer_Reliability官方文档.md)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
