---
title: "Animancer - Speed and Time 速度时间对比"
date: 2025-12-25
draft: false
---

# Animancer - Speed and Time 速度时间对比

## Mecanim vs Animancer: 速度和时间控制

### 固定速度

**Mecanim:** 在Controller的状态Speed字段设置，无法运行时修改

**Animancer:**
```csharp
// 方式1: 代码设置
var state = _animancer.Play(_walk);
state.Speed = 1.5f;

// 方式2: Transition预设
_walkTransition.Speed = 1.5f;
_animancer.Play(_walkTransition);
```

### 动态速度

**Mecanim:** 创建Float参数 → 配置Multiplier字段 → SetFloat()

**Animancer:**
```csharp
var state = _animancer.Play(_walk);
state.Speed = 2f; // 直接设置
```

### 时间控制

**Mecanim:** 使用Play()和CrossFade()的normalizedTime参数

**Animancer:**
```csharp
var state = _animancer.Play(_walk);
state.Time = 1.5f;           // 跳转到1.5秒
state.NormalizedTime = 0.5f; // 跳转到50%
```

### 常量时间控制（手动控制播放头）

**Mecanim:** 需要参数设置持续管理normalized time

**Animancer:**
```csharp
state.Speed = 0;  // 或 state.IsPlaying = false
state.Time = 1.5f;  // 手动设置时间
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
