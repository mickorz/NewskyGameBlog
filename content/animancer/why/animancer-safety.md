# Animancer - Safety 安全性

## 📋 目录
- [魔法字符串问题](#魔法字符串问题)
- [五大风险](#五大风险)
- [Animancer的类型安全](#animancer的类型安全)
- [参考资料](#参考资料)

---

## 魔法字符串问题

> **"魔法字符串是一个`string`，用来控制某些与之没有真实关联的东西"**

### Mecanim的魔法字符串

```csharp
// ❌ 魔法字符串
_animator.Play("Walk");
_animator.SetFloat("Speed", 5f);
_animator.SetTrigger("Attack");

// 问题：
// - "Walk" 状态是否存在？编译器不知道
// - "Speed" 参数是否正确？编译器不知道
// - 拼写错误？运行时才发现
```

---

## 五大风险

### 风险1：状态/参数是否存在？

```csharp
// Mecanim
_animator.Play("Wlak"); // 拼写错误！
// ❌ 编译成功
// ❌ 运行时无警告
// ❌ 动画不播放，难以调试
```

```csharp
// Animancer
[SerializeField] private AnimationClip _walk;
_animancer.Play(_walk);
// ✅ 如果_walk为null，Inspector会警告
// ✅ 编译器可能也会警告（取决于设置）
```

### 风险2：可用动画列表不清晰

```csharp
// Mecanim - 需要打开Controller查看
// 无法从代码中得知

// Animancer - 直接在脚本中列出
[SerializeField] private AnimationClip _idle;
[SerializeField] private AnimationClip _walk;
[SerializeField] private AnimationClip _run;
[SerializeField] private AnimationClip _jump;
// ✅ 一目了然
```

### 风险3：动画结束时的行为不明确

```csharp
// Mecanim
_animator.Play("Attack");
// ❓ 结束后会做什么？
// 需要打开Controller查看过渡配置

// Animancer
var state = _animancer.Play(_attack);
state.Events.OnEnd = () =>
{
    // ✅ 明确定义结束行为
    _animancer.Play(_idle);
};
```

### 风险4：重命名困难

```csharp
// Mecanim - 手动查找所有引用
// 文件1
_animator.Play("Walk");

// 文件2
_animator.CrossFade("Walk", 0.25f);

// 文件3
if (_animator.GetCurrentAnimatorStateInfo(0).IsName("Walk"))

// Controller中还有 "Walk" 状态
// ❌ 需要手动修改所有位置

// Animancer - IDE自动重命名
[SerializeField] private AnimationClip _walkClip;
_animancer.Play(_walkClip);
// ✅ 重命名变量，IDE自动更新所有引用
```

### 风险5：跨Controller使用问题

```csharp
// Mecanim - 同一脚本用于多个角色
public class CharacterController : MonoBehaviour
{
    void Attack()
    {
        _animator.SetTrigger("Attack");
    }
}

// 问题：
// - 角色A的Controller有"Attack"触发器
// - 角色B的Controller忘记添加"Attack"触发器
// - ❌ 角色B的攻击不工作，难以发现

// Animancer - 明确依赖
public class CharacterController : MonoBehaviour
{
    [SerializeField] private AnimationClip _attack;

    void Attack()
    {
        _animancer.Play(_attack);
    }
}
// ✅ Inspector会显示未赋值警告
```

---

## Animancer的类型安全

### 1. 编译时检查

```csharp
// 强类型引用
[SerializeField] private AnimationClip _walk;

_animancer.Play(_walk);
// ✅ 如果类型错误，编译失败
// ✅ 如果为null，Inspector警告
```

### 2. IDE支持

```csharp
// 自动补全
_animancer.Play(_w...);
// ✅ IDE自动提示 _walk, _walkClip 等

// 查找引用
// ✅ 右键 _walk → Find All References

// 重命名
// ✅ 右键 _walk → Rename
```

### 3. 明确的事件处理

```csharp
// Mecanim - StateMachineBehaviour
public class AttackBehaviour : StateMachineBehaviour
{
    public override void OnStateExit(...)
    {
        // 代码与Controller分离
    }
}

// Animancer - 内联事件
var state = _animancer.Play(_attack);
state.Events.OnEnd = () =>
{
    // ✅ 逻辑集中在一处
    OnAttackComplete();
};
```

### 4. 集中的依赖管理

```csharp
public class Character : MonoBehaviour
{
    // ✅ 所有动画依赖一目了然
    [Header("Movement")]
    [SerializeField] private AnimationClip _idle;
    [SerializeField] private AnimationClip _walk;

    [Header("Combat")]
    [SerializeField] private AnimationClip _attack;
    [SerializeField] private AnimationClip _block;

    // ✅ Inspector显示未赋值警告
    // ✅ 易于检查和维护
}
```

---

## 实战对比

### 场景：实现攻击系统

**Mecanim方式：**

```csharp
public class MecanimCombat : MonoBehaviour
{
    private Animator _animator;

    void Attack()
    {
        // ❌ 魔法字符串
        _animator.SetTrigger("Attack");
    }

    void CheckAttackEnd()
    {
        // ❌ 魔法字符串 + 哈希码
        var info = _animator.GetCurrentAnimatorStateInfo(0);
        if (info.IsName("Attack") && info.normalizedTime >= 1f)
        {
            OnAttackComplete();
        }
    }

    void OnAttackComplete()
    {
        // 攻击结束逻辑
    }
}

// 风险：
// 1. "Attack" 拼写错误
// 2. 触发器参数名称变更
// 3. 状态名称变更
// 4. 多个Controller时不一致
```

**Animancer方式：**

```csharp
public class AnimancerCombat : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    // ✅ 类型安全
    [SerializeField] private AnimationClip _attackClip;

    void Attack()
    {
        var state = _animancer.Play(_attackClip);

        // ✅ 事件内联，逻辑集中
        state.Events.OnEnd = OnAttackComplete;
    }

    void OnAttackComplete()
    {
        // 攻击结束逻辑
    }

    // 优势：
    // 1. 编译时检查
    // 2. IDE支持重命名
    // 3. Inspector警告
    // 4. 逻辑清晰
}
```

---

## 最佳实践

### ✅ 使用强类型引用

```csharp
// ✅ 好：类型安全
[SerializeField] private AnimationClip _walk;
_animancer.Play(_walk);

// ❌ 差：魔法字符串
_animator.Play("Walk");
```

### ✅ 使用常量避免拼写错误

```csharp
// 如果必须使用字符串
public static class AnimationNames
{
    public const string WALK = "Walk";
    public const string RUN = "Run";
    public const string ATTACK = "Attack";
}

// 至少使用常量
_animator.Play(AnimationNames.WALK);
```

### ✅ 使用编辑器验证

```csharp
#if UNITY_EDITOR
using UnityEditor;

[CustomEditor(typeof(Character))]
public class CharacterEditor : Editor
{
    public override void OnInspectorGUI()
    {
        base.OnInspectorGUI();

        var character = (Character)target;

        // 验证所有AnimationClip是否已赋值
        if (character.IdleClip == null)
            EditorGUILayout.HelpBox("Idle Clip未赋值!", MessageType.Warning);
    }
}
#endif
```

---

## 参考资料

### 📚 相关文档
- [\1](./animancer-why.md)
- [\1](./animancer-clarity.md)
- [\1](./animancer-reliability.md)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
