# Animancer - Playing 播放对比

## Mecanim vs Animancer: 播放动画

### 无脚本播放

**Mecanim:** 创建AnimatorController资源 → 配置状态 → 分配给Animator组件

**Animancer:** 添加NamedAnimancerComponent → 添加AnimationClip到动画数组

### 脚本控制播放

**Mecanim问题:** 同一帧多个Play()命令，只有首个生效

```csharp
_animator.Play("Jump");  // 播放
_animator.Play("Hit");   // ❌ 被忽略
```

**Animancer优势:** 所有命令都会执行

```csharp
var jumpState = _animancer.Play(_jump);  // 播放
var hitState = _animancer.Play(_hit);    // ✅ 覆盖跳跃
```

### 理解与维护

**Mecanim:** 需要查看Controller资源，检查多个状态和过渡

**Animancer:** 所有逻辑集中在脚本，Inspector直接显示使用的动画

### 复用性

**Mecanim:** 修改脚本后，需要手动更新所有使用该脚本的Controller资产

**Animancer:** 修改脚本后自动生效，无需更新资源文件

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
