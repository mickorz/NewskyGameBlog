---
title: "Animancer - Weapon Animations 武器动画对比"
date: 2025-12-25
draft: false
---

# Animancer - Weapon Animations 武器动画对比

## Mecanim vs Animancer: 武器动画系统

### Mecanim方案

**步骤:**
1. 创建AnimatorController资源
2. 创建多个状态（轻攻击、重攻击、特殊攻击等）
3. 为每个状态创建占位符AnimationClips
4. 每个武器配置：AnimationClips + 占位符名称
5. 代码：创建AnimatorOverrideController并覆盖动画

```csharp
var overrideController = new AnimatorOverrideController(_baseController);
overrideController["PlaceholderLightAttack"] = weapon.LightAttackClip;
overrideController["PlaceholderHeavyAttack"] = weapon.HeavyAttackClip;
_animator.runtimeAnimatorController = overrideController;
```

### Animancer方案

**步骤:**
1. 添加AnimancerComponent
2. 每个武器配置：AnimationClips
3. 代码：直接Play()所需Clip

```csharp
// 播放武器动画
_animancer.Play(weapon.LightAttackClip);

// 切换武器时可选：释放旧状态
_animancer.States.Dispose(oldWeapon.LightAttackClip);
```

### 核心差异

**Mecanim:** 需要维护Controller与代码同步，占位符管理复杂

**Animancer:** 无需Controller，直接播放，简洁灵活

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
