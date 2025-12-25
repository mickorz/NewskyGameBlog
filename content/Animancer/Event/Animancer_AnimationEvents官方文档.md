# Animancer - Animation Events 官方文档

## 📋 目录
- [概述](#概述)
- [核心概念](#核心概念)
- [实现步骤](#实现步骤)
- [参数类型](#参数类型)
- [性能优化](#性能优化)
- [代码示例](#代码示例)
- [最佳实践](#最佳实践)
- [FAQ常见问题](#faq常见问题)
- [参考资料](#参考资料)

---

## 概述

**Animation Events** 是 Unity 内置的事件系统，可以在动画的特定时刻触发回调函数。

### 🔑 关键特性

> **"Unity's inbuilt Animation Event system works the same when using Animancer as without it"**
>
> Animancer 完全支持 Unity 原生的 Animation Events，使用方式与 Unity Animator **完全相同**。

### 📊 与 Animancer Events 对比

| 特性 | Animation Events | Animancer Events |
|------|------------------|------------------|
| **来源** | Unity内置 | Animancer自定义 |
| **兼容性** | 与Animator完全相同 | Animancer专属 |
| **配置位置** | AnimationClip中 | 代码或Inspector |
| **灵活性** | 固定配置 | 动态可修改 |
| **性能** | 较低（有GC） | 较高（无GC） |
| **学习成本** | 低（Unity标准） | 中（新API） |

---

## 核心概念

### 🎯 工作原理

```
AnimationClip (配置事件)
    └── 播放到事件时间点
            └── 查找同GameObject上的MonoBehaviour
                    └── 调用匹配的方法名
```

### 🔗 关键要素

1. **事件定义**：在 AnimationClip 中配置
2. **方法名匹配**：事件的 Function Name 必须与脚本方法名完全一致
3. **组件位置**：脚本必须附加到拥有 Animator/AnimancerComponent 的同一 GameObject

---

## 实现步骤

### 步骤1：添加事件

根据动画资源类型选择配置方式：

#### 方式A：模型文件（FBX）

1. 选中模型文件（.fbx）
2. 在 Inspector 中切换到 **Animation Tab**
3. 选择要编辑的动画片段
4. 在 **Events** 面板中添加事件
5. 设置事件时间和 Function Name
6. 点击 **Apply** 应用修改

#### 方式B：动画文件（.anim）

1. 打开 **Animation Window** (Window > Animation > Animation)
2. 选择要编辑的 GameObject 和动画片段
3. 在时间轴上点击添加事件标记
4. 在 Inspector 中设置 Function Name
5. 保存修改

### 步骤2：编写脚本

创建一个 MonoBehaviour 脚本，添加与事件 Function Name **完全匹配**的方法：

```csharp
using UnityEngine;

public class CharacterAnimationEvents : MonoBehaviour
{
    // 方法名必须与AnimationClip中的Function Name完全一致
    public void PlayFootstepSound()
    {
        Debug.Log("播放脚步声");
    }
}
```

### 步骤3：绑定组件

将脚本附加到拥有 Animator 或 AnimancerComponent 的 GameObject。

---

## 参数类型

Animation Events 支持以下参数类型：

### 1. 无参数（推荐）⭐

```csharp
public void OnJumpStart()
{
    Debug.Log("跳跃开始");
}
```

**优点：** 性能最优、无 GC 分配

### 2. Int/Float 参数

```csharp
public void OnAttackHit(int damage)
{
    Debug.Log($"攻击伤害: {damage}");
}
```

### 3. String 参数（⚠️ 性能警告）

```csharp
public void OnPlaySound(string soundName)
{
    Debug.Log($"播放音效: {soundName}");
}
```

> **⚠️ 性能警告：** "Any event with a `string` or `AnimationEvent` parameter will allocate some Garbage every time it is triggered"

---

## 性能优化

### ❌ 性能陷阱

```csharp
// ❌ 差：String参数会产生GC
public void OnPlaySound(string soundName) { }
```

### ✅ 优化方案

```csharp
// ✅ 好：使用Int参数（枚举索引），无GC
public void OnPlaySound(int soundTypeIndex)
{
    SoundType type = (SoundType)soundTypeIndex;
    AudioManager.Play(type);
}
```

---

## 代码示例

### 示例1：完整的脚步声系统

```csharp
using UnityEngine;

/// <summary>
/// 角色动画事件接收器
/// 处理来自AnimationClip的所有事件回调
/// </summary>
public class CharacterAnimationEvents : MonoBehaviour
{
    [SerializeField] private AudioSource _audioSource;
    [SerializeField] private AudioClip[] _footstepSounds;

    /// <summary>
    /// 脚步事件回调
    /// Animation Clip配置：Function Name = "OnFootstep"
    /// </summary>
    public void OnFootstep()
    {
        if (_footstepSounds.Length > 0)
        {
            var clip = _footstepSounds[Random.Range(0, _footstepSounds.Length)];
            _audioSource.PlayOneShot(clip);
        }
    }
}
```

### 示例2：使用Int参数的攻击系统

```csharp
using UnityEngine;

/// <summary>
/// 战斗动画事件接收器
/// 使用Int参数优化性能（避免String参数的GC）
/// </summary>
public class CombatAnimationEvents : MonoBehaviour
{
    [SerializeField] private WeaponController _weaponController;

    /// <summary>
    /// 攻击伤害事件
    /// Animation Clip配置：
    /// - Attack1: Function="OnAttackHit", Int=30
    /// - Attack2: Function="OnAttackHit", Int=50
    /// </summary>
    public void OnAttackHit(int damage)
    {
        Debug.Log($"攻击伤害判定: {damage}");
        _weaponController.CheckHit(damage);
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **优先使用无参数方法**
2. **使用Int/Float参数代替String**
3. **方法名与Function Name完全一致**
4. **添加详细的注释说明配置**

### ❌ DON'T（避免做法）

1. **避免String参数（会产生GC）**
2. **避免AnimationEvent参数（会产生GC）**
3. **方法名拼写错误**
4. **在事件中执行耗时操作**

---

## FAQ常见问题

### Q1: Animation Events 和 Animancer Events 应该用哪个？

**A:** 根据场景选择：
- 简单固定事件 → Animation Events
- 需要动态修改 → Animancer Events
- 性能敏感场景 → Animancer Events

### Q2: 为什么我的事件没有触发？

**A:** 检查：
1. 方法名是否完全匹配（包括大小写）
2. 脚本是否在正确的GameObject上
3. 方法是否为public
4. 动画是否在播放

### Q3: String参数为什么会产生GC？

**A:** Unity内部实现会装箱String参数并使用反射，每次触发都产生GC分配。

---

## 参考资料

### 📚 相关文档
- [Animancer Events 主页](https://kybernetik.com.au/animancer/docs/manual/events/)
- [Unity Animation Events 官方文档](https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html)

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+
