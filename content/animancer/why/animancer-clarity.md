---
title: "Animancer - Clarity 清晰性"
date: 2025-12-25
draft: false
---

# Animancer - Clarity 清晰性

## 📋 目录
- [单一责任原则](#单一责任原则)
- [Mecanim的依赖模糊问题](#mecanim的依赖模糊问题)
- [Animancer的明确声明](#animancer的明确声明)
- [团队协作优势](#团队协作优势)
- [参考资料](#参考资料)

---

## 单一责任原则

> **"每个类或函数应该仅对应用程序功能的单一部分负责"**

Animator Controller 违反了这一原则：
- 脚本不清楚需要什么Controller
- Controller不清楚需要什么脚本
- 两者的关系隐藏且难以追踪

---

## Mecanim的依赖模糊问题

### 问题1：脚本→Controller 不明确

```csharp
public class CharacterController : MonoBehaviour
{
    private Animator _animator;

    void Attack()
    {
        _animator.SetTrigger("Attack");
    }
}
```

**疑问：**
- 🤔 这个脚本应该使用哪个Animator Controller？
- 🤔 Controller中需要有哪些状态？
- 🤔 需要哪些参数？
- ❌ 查看脚本无法得知答案

### 问题2：Controller→脚本 不明确

```
Animator Controller:
  States:
    - Idle
    - Walk
    - Run
    - Attack
  Parameters:
    - Speed (Float)
    - IsGrounded (Bool)
    - AttackTrigger (Trigger)
```

**疑问：**
- 🤔 哪个脚本会设置这些参数？
- 🤔 哪个脚本会触发Attack？
- 🤔 Speed参数的取值范围是多少？
- ❌ 查看Controller无法得知答案

### 问题3：参数使用追踪困难

**场景：** Unity 3D Game Kit示例

```
Parameters:
  - AirborneVerticalSpeed
  - VerticalSpeed
```

**疑问：**
- 🤔 这两个参数有什么区别？
- 🤔 其中一个是否还在使用？
- 🤔 能否安全删除？

**验证方法：**
- ❌ 删除后看游戏是否坏掉（不可靠）
- ❌ 搜索脚本中的字符串引用（容易遗漏）

---

## Animancer的明确声明

### 1. 所有依赖在脚本中声明

```csharp
public class Character : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // ✅ 明确需要的动画
    [Header("Movement")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    [Header("Combat")]
    [SerializeField] private AnimationClip _attack1;
    [SerializeField] private AnimationClip _attack2;
    [SerializeField] private AnimationClip _attack3;

    [Header("Reactions")]
    [SerializeField] private AnimationClip _hit;
    [SerializeField] private AnimationClip _death;
}
```

**优势：**
- ✅ 查看脚本就知道需要哪些动画
- ✅ Inspector显示未赋值的警告
- ✅ 易于理解角色功能

### 2. 模块化组织

```csharp
// 按功能分组
[System.Serializable]
public class MovementAnimations
{
    public AnimationClip Idle;
    public AnimationClip Walk;
    public AnimationClip Run;
    public AnimationClip Jump;
}

[System.Serializable]
public class CombatAnimations
{
    public AnimationClip[] LightAttacks;
    public AnimationClip[] HeavyAttacks;
    public AnimationClip Block;
    public AnimationClip Parry;
}

public class Character : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private MovementAnimations _movement;
    [SerializeField] private CombatAnimations _combat;
}
```

### 3. 清晰的参数管理

```csharp
// Mecanim - 参数分散
_animator.SetFloat("Speed", 5f);
_animator.SetBool("IsGrounded", true);
_animator.SetInteger("WeaponType", 2);

// Animancer - 变量集中
public class CharacterData
{
    public float Speed;
    public bool IsGrounded;
    public WeaponType CurrentWeapon;
}
```

---

## 团队协作优势

### Mecanim的协作问题

```
程序员A: 修改脚本，添加新参数"JumpPower"
    ↓
美术B: 不知道需要在Controller中添加参数
    ↓
游戏运行时无警告，功能不工作
    ↓
调试困难
```

**问题：**
- ❌ 无法并行开发同一角色
- ❌ Controller合并冲突难以解决
- ❌ 变更历史难以追踪

### Animancer的协作优势

```
程序员A: 修改脚本，添加AnimationClip字段
    ↓
美术B: 在Inspector中看到新字段
    ↓
分配动画片段
    ↓
✅ 立即工作
```

**优势：**
- ✅ 可以并行开发
- ✅ 变更在脚本中可追踪
- ✅ Inspector自动显示所需内容

---

## 对比示例

### 场景：添加新攻击

**Mecanim流程：**

```
1. 程序员：修改脚本
   _animator.SetTrigger("SpecialAttack");

2. 程序员：找到所有使用该脚本的角色

3. 美术：打开每个角色的Controller
   - 创建"SpecialAttack"状态
   - 分配动画
   - 创建过渡
   - 创建触发器参数

4. 测试：验证所有角色是否正确配置
```

**Animancer流程：**

```
1. 程序员：修改脚本
   [SerializeField] private AnimationClip _specialAttack;
   _animancer.Play(_specialAttack);

2. 美术：在Inspector中为每个角色分配动画片段

3. ✅ 完成
```

---

## 最佳实践

### ✅ 清晰的动画组织

```csharp
// 方式1：直接声明
public class SimpleCharacter : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;

    // 一目了然
}

// 方式2：分组声明
public class ComplexCharacter : MonoBehaviour
{
    [Header("== Locomotion ==")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;
    [SerializeField] private AnimationClip _jump;

    [Header("== Combat ==")]
    [SerializeField] private AnimationClip[] _attacks;
    [SerializeField] private AnimationClip _block;

    [Header("== Reactions ==")]
    [SerializeField] private AnimationClip _hit;
    [SerializeField] private AnimationClip _death;

    // 分类清晰
}

// 方式3：结构化声明
[System.Serializable]
public class CharacterAnimations
{
    [System.Serializable]
    public class Locomotion
    {
        public AnimationClip Idle;
        public AnimationClip Walk;
        public AnimationClip Run;
    }

    [System.Serializable]
    public class Combat
    {
        public AnimationClip[] Attacks;
        public AnimationClip Block;
    }

    public Locomotion Movement;
    public Combat Fighting;
}

public class StructuredCharacter : MonoBehaviour
{
    [SerializeField] private CharacterAnimations _animations;

    // 高度结构化
}
```

### ✅ 自文档化代码

```csharp
public class SelfDocumentingCharacter : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [Header("基础移动 (3个)")]
    [Tooltip("站立不动时播放")]
    [SerializeField] private AnimationClip _idle;

    [Tooltip("慢速移动时播放 (< 5 m/s)")]
    [SerializeField] private AnimationClip _walk;

    [Tooltip("快速移动时播放 (>= 5 m/s)")]
    [SerializeField] private AnimationClip _run;

    [Header("连击系统 (3段)")]
    [Tooltip("第一段攻击")]
    [SerializeField] private AnimationClip _attack1;

    [Tooltip("第二段攻击")]
    [SerializeField] private AnimationClip _attack2;

    [Tooltip("第三段攻击（终结技）")]
    [SerializeField] private AnimationClip _attack3;
}
```

---

## 参考资料

### 📚 相关文档
- [\1]({{< ref "animancer-why.md" >}})
- [\1]({{< ref "animancer-adaptability.md" >}})
- [\1]({{< ref "animancer-safety.md" >}})

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
