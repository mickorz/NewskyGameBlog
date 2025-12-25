# Animancer - Adaptability 适应性

## 📋 目录
- [关注点分离](#关注点分离)
- [Mecanim的强制分离问题](#mecanim的强制分离问题)
- [Animancer的灵活组织](#animancer的灵活组织)
- [参数系统问题](#参数系统问题)
- [参考资料](#参考资料)

---

## 关注点分离

> **"将代码分离成不同部分，每部分覆盖不同的关注点"**

**好的分离：** 模块化、可重用、易维护

**坏的分离：** 强制分离本应耦合的内容

---

## Mecanim的强制分离问题

### 问题：不应该分离的被分离了

```
游戏逻辑（脚本）  ←→  动画逻辑（Controller）
         ↓
    需要紧密协作
         ↓
   浪费时间协调两者
```

**示例：**
```csharp
// 脚本中
if (shouldAttack)
{
    _animator.SetTrigger("Attack");
}

// Controller中需要：
// 1. 创建"Attack"触发器参数
// 2. 创建Attack状态
// 3. 配置过渡条件
// 4. 两者必须保持同步！
```

---

## Animancer的灵活组织

### 1. 按功能模块组织

```csharp
// 移动模块
public class MovementController : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    void UpdateMovement(float speed)
    {
        if (speed < 0.1f)
            _animancer.Play(_idle);
        else if (speed < 5f)
            _animancer.Play(_walk);
        else
            _animancer.Play(_run);
    }
}

// 战斗模块
public class CombatController : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip[] _attacks;

    void Attack(int comboIndex)
    {
        _animancer.Play(_attacks[comboIndex]);
    }
}
```

### 2. 按角色部位组织

```csharp
// 下半身动画
public class LowerBodyAnimations : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [Header("移动")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;
    [SerializeField] private AnimationClip _run;

    void PlayOnLayer0()
    {
        _animancer.Layers[0].Play(_walk);
    }
}

// 上半身动画
public class UpperBodyAnimations : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AvatarMask _upperBodyMask;

    [Header("战斗")]
    [SerializeField] private AnimationClip _aim;
    [SerializeField] private AnimationClip _shoot;

    void Start()
    {
        _animancer.Layers[1].SetMask(_upperBodyMask);
    }

    void PlayOnLayer1()
    {
        _animancer.Layers[1].Play(_aim);
    }
}
```

### 3. 按武器类型组织

```csharp
[System.Serializable]
public class WeaponAnimations
{
    public AnimationClip Idle;
    public AnimationClip Draw;
    public AnimationClip[] Attacks;
    public AnimationClip Block;
}

public class WeaponSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [SerializeField] private WeaponAnimations _sword;
    [SerializeField] private WeaponAnimations _bow;
    [SerializeField] private WeaponAnimations _staff;

    private WeaponAnimations _currentWeapon;

    void EquipSword()
    {
        _currentWeapon = _sword;
        _animancer.Play(_currentWeapon.Draw);
    }

    void Attack()
    {
        _animancer.Play(_currentWeapon.Attacks[0]);
    }
}
```

---

## 参数系统问题

### Mecanim参数的三大缺陷

#### 1. 触发器滞后问题

**场景：** 玩家快速按攻击键

```csharp
// Mecanim
_animator.SetTrigger("Attack");

// 问题：
// - 如果当前正在播放其他动作
// - 触发器会被缓存
// - 等其他动作结束后才触发
// - 导致延迟响应或意外触发
```

**示例：**
```
玩家输入：跳跃 → 攻击
         ↓       ↓
实际执行：跳跃 → 着陆 → 攻击（延迟触发）
                     ↑
                  不想要的攻击！
```

#### 2. 缺乏IDE功能

**Mecanim参数：**
- ❌ 无法重命名（需手动查找所有引用）
- ❌ 无法查找引用
- ❌ 无法跨文件对比
- ❌ 无代码补全

```csharp
// 拼写错误，运行时才发现
_animator.SetFloat("Spead", 5f); // 应该是"Speed"
```

**Animancer脚本变量：**
- ✅ IDE自动重命名
- ✅ 查找所有引用
- ✅ 代码补全
- ✅ 编译时检查

```csharp
[SerializeField] private float _speed;
// IDE支持重命名、查找引用等
```

#### 3. 验证困难

**Mecanim：**
```csharp
// 参数是否存在？运行时才知道
_animator.SetFloat("NonExistentParam", 5f);
// ❌ 无警告，无错误，静默失败
```

**Animancer：**
```csharp
[SerializeField] private AnimationClip _clip;
// 如果未赋值，Inspector会显示警告
// 编译器也会在某些情况下警告
```

---

## 对比示例

### 武器切换系统

**Mecanim方式 - 集中但僵化：**

```csharp
// 所有武器动画必须在单个Controller中
// Animator Controller:
//   - Sword Layer
//     - SwordIdle, SwordAttack1, SwordAttack2
//   - Bow Layer
//     - BowIdle, BowDraw, BowShoot
//   - Staff Layer
//     - StaffIdle, StaffCast1, StaffCast2

// 脚本中：
_animator.SetInteger("WeaponType", (int)WeaponType.Sword);
_animator.SetTrigger("Attack");
```

**Animancer方式 - 分离且灵活：**

```csharp
// 每个武器独立管理自己的动画
public class SwordController : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip[] _attacks;

    void Attack(int index)
    {
        _animancer.Play(_attacks[index]);
    }
}

public class BowController : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _draw;
    [SerializeField] private AnimationClip _shoot;

    void Shoot()
    {
        _animancer.Play(_shoot);
    }
}
```

---

## 最佳实践

### ✅ 灵活组织动画

```csharp
// 方式1：单一职责
public class IdleAnimations : MonoBehaviour
{
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _idleVariation1;
    [SerializeField] private AnimationClip _idleVariation2;
}

// 方式2：功能分组
public class CharacterAnimations : MonoBehaviour
{
    [SerializeField] private MovementAnims _movement;
    [SerializeField] private CombatAnims _combat;
    [SerializeField] private EmoteAnims _emotes;
}

// 方式3：状态分组
public class AIAnimations : MonoBehaviour
{
    [SerializeField] private AnimationClip _patrol;
    [SerializeField] private AnimationClip _chase;
    [SerializeField] private AnimationClip _attack;
    [SerializeField] private AnimationClip _retreat;
}
```

---

## 参考资料

### 📚 相关文档
- [Why Animancer](./Animancer_Why官方文档.md)
- [Clarity 清晰性](./Animancer_Clarity官方文档.md)
- [Safety 安全性](./Animancer_Safety官方文档.md)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
