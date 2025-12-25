# Animancer - Waiting 等待对比

## Mecanim vs Animancer: 等待动画结束

### Mecanim方式

**方式1: 状态信息检查**
```csharp
while (true)
{
    var info = _animator.GetCurrentAnimatorStateInfo(0);
    if (info.IsName("Attack") && info.normalizedTime >= 1f)
        break;
    yield return null;
}
```
需要Exit Time transitions和哈希码管理，用户体验差

**方式2: StateMachineBehaviour**
```csharp
public class AttackBehaviour : StateMachineBehaviour
{
    public override void OnStateExit(Animator animator, ...)
    {
        // 状态结束回调
    }
}
```

### Animancer方式

**方式1: End Events**
```csharp
var state = _animancer.Play(_attack);
state.Events.OnEnd = OnAttackComplete;
```

**方式2: Coroutines**
```csharp
IEnumerator PlayAttack()
{
    var state = _animancer.Play(_attack);
    yield return state; // 等待结束
    OnAttackComplete();
}
```

**方式3: 手动检查**
```csharp
if (state.NormalizedTime >= 1f)
{
    OnAttackComplete();
}
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
