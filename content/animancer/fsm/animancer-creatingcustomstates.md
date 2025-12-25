---
title: "Animancer - Creating Custom States"
date: 2025-12-25
draft: false
---

# Animancer - Creating Custom States 官方文档

## 📋 目录
- [概述](#概述)
- [实现方法](#实现方法)
- [必需步骤](#必需步骤)
- [代码示例](#代码示例)
- [高级技巧](#高级技巧)
- [参考资料](#参考资料)

---

## 概述

**自定义状态（Custom States）** 允许开发者通过继承 `AnimancerState` 创建个性化的动画状态类型。

> **"你可以通过继承 `AnimancerState`（或其派生类型）来实现自己的状态类型"**

### ⚠️ 授权要求

> **此功能仅限 Pro 版本**

---

## 实现方法

### 基本要求

创建自定义状态需要：

1. **继承 AnimancerState** - 基础类或其派生类
2. **覆盖 Length 属性** - 返回动画时长
3. **实现 CreatePlayable()** - 生成 Playable 对象

---

## 必需步骤

### 步骤1：继承 AnimancerState

```csharp
using Animancer;
using UnityEngine.Playables;

public class MyCustomState : AnimancerState
{
    // 实现必需成员...
}
```

### 步骤2：覆盖 Length 属性

```csharp
private AnimationClip _clip;

public override float Length => _clip.length;
```

### 步骤3：实现 CreatePlayable()

```csharp
protected override void CreatePlayable(out Playable playable)
{
    playable = AnimationClipPlayable.Create(Root.Graph, _clip);
}
```

---

## 代码示例

### 示例1：基础自定义状态

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

/// <summary>
/// 基础自定义动画状态
/// </summary>
public class MyCustomState : AnimancerState
{
    private AnimationClip _clip;

    // 构造函数
    public MyCustomState(AnimationClip clip)
    {
        _clip = clip;
    }

    // 1. 覆盖Length属性
    public override float Length => _clip.length;

    // 2. 实现CreatePlayable方法
    protected override void CreatePlayable(out Playable playable)
    {
        playable = AnimationClipPlayable.Create(Root.Graph, _clip);
    }
}
```

### 示例2：带事件的自定义状态

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;
using System;

/// <summary>
/// 带自定义事件的状态
/// </summary>
public class EventState : AnimancerState
{
    private AnimationClip _clip;

    public event Action OnStateStart;
    public event Action OnStateMidpoint;
    public event Action OnStateEnd;

    public EventState(AnimationClip clip)
    {
        _clip = clip;
    }

    public override float Length => _clip.length;

    protected override void CreatePlayable(out Playable playable)
    {
        playable = AnimationClipPlayable.Create(Root.Graph, _clip);
    }

    public override void OnEnterState()
    {
        base.OnEnterState();
        OnStateStart?.Invoke();

        // 添加中点事件
        Events.AddNormalized(0.5f, () => OnStateMidpoint?.Invoke());

        // 添加结束事件
        Events.OnEnd = () => OnStateEnd?.Invoke();
    }
}
```

### 示例3：可配置参数的状态

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

/// <summary>
/// 可配置参数的自定义状态
/// </summary>
public class ConfigurableState : AnimancerState
{
    private AnimationClip _clip;
    private float _speedMultiplier = 1f;
    private bool _looping;

    public ConfigurableState(
        AnimationClip clip,
        float speedMultiplier = 1f,
        bool looping = false)
    {
        _clip = clip;
        _speedMultiplier = speedMultiplier;
        _looping = looping;
    }

    public override float Length => _clip.length / _speedMultiplier;

    protected override void CreatePlayable(out Playable playable)
    {
        var clipPlayable = AnimationClipPlayable.Create(Root.Graph, _clip);
        clipPlayable.SetSpeed(_speedMultiplier);
        playable = clipPlayable;
    }

    public override void OnEnterState()
    {
        base.OnEnterState();
        IsLooping = _looping;
        Speed = _speedMultiplier;
    }
}
```

### 示例4：混合多个Clip的状态

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;

/// <summary>
/// 混合多个AnimationClip的自定义状态
/// </summary>
public class BlendedState : AnimancerState
{
    private AnimationClip _clip1;
    private AnimationClip _clip2;
    private float _blendWeight = 0.5f;

    public BlendedState(
        AnimationClip clip1,
        AnimationClip clip2,
        float blendWeight = 0.5f)
    {
        _clip1 = clip1;
        _clip2 = clip2;
        _blendWeight = Mathf.Clamp01(blendWeight);
    }

    public override float Length
    {
        get
        {
            // 返回较长的动画长度
            return Mathf.Max(_clip1.length, _clip2.length);
        }
    }

    protected override void CreatePlayable(out Playable playable)
    {
        // 创建混合器
        var mixer = AnimationMixerPlayable.Create(Root.Graph, 2);

        // 创建两个Clip的Playable
        var playable1 = AnimationClipPlayable.Create(Root.Graph, _clip1);
        var playable2 = AnimationClipPlayable.Create(Root.Graph, _clip2);

        // 连接到混合器
        Root.Graph.Connect(playable1, 0, mixer, 0);
        Root.Graph.Connect(playable2, 0, mixer, 1);

        // 设置混合权重
        mixer.SetInputWeight(0, 1f - _blendWeight);
        mixer.SetInputWeight(1, _blendWeight);

        playable = mixer;
    }

    // 动态调整混合权重
    public void SetBlendWeight(float weight)
    {
        _blendWeight = Mathf.Clamp01(weight);

        if (Playable.IsValid() && Playable.GetPlayableType() == typeof(AnimationMixerPlayable))
        {
            var mixer = (AnimationMixerPlayable)Playable;
            mixer.SetInputWeight(0, 1f - _blendWeight);
            mixer.SetInputWeight(1, _blendWeight);
        }
    }
}
```

### 示例5：实际使用自定义状态

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 使用自定义状态
/// </summary>
public class CustomStateUsageExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;

    [SerializeField] private AnimationClip _walkClip;
    [SerializeField] private AnimationClip _runClip;
    [SerializeField] private AnimationClip _attackClip;

    void Start()
    {
        // 示例1：使用基础自定义状态
        var customState = new MyCustomState(_walkClip);
        _animancer.States.GetOrCreate(customState);
        _animancer.Play(customState);

        // 示例2：使用带事件的状态
        var eventState = new EventState(_attackClip);
        eventState.OnStateStart += () => Debug.Log("攻击开始");
        eventState.OnStateMidpoint += () => Debug.Log("攻击中点");
        eventState.OnStateEnd += () => Debug.Log("攻击结束");
        _animancer.Play(eventState);

        // 示例3：使用可配置状态
        var configState = new ConfigurableState(
            _runClip,
            speedMultiplier: 1.5f,
            looping: true
        );
        _animancer.Play(configState);

        // 示例4：使用混合状态
        var blendState = new BlendedState(_walkClip, _runClip, 0.5f);
        _animancer.Play(blendState);

        // 动态调整混合权重
        blendState.SetBlendWeight(0.8f);
    }
}
```

---

## 高级技巧

### 1. 覆盖其他方法

```csharp
public class AdvancedState : AnimancerState
{
    protected override void OnStartFade()
    {
        base.OnStartFade();
        Debug.Log("开始淡入淡出");
    }

    public override void OnEnterState()
    {
        base.OnEnterState();
        Debug.Log("进入状态");
    }

    public override void OnExitState()
    {
        base.OnExitState();
        Debug.Log("退出状态");
    }

    protected override void Update()
    {
        base.Update();
        // 自定义每帧更新逻辑
    }
}
```

### 2. 状态缓存

```csharp
public class CachedStateExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private AnimationClip _clip;

    private MyCustomState _cachedState;

    void Start()
    {
        // 创建并缓存状态
        _cachedState = new MyCustomState(_clip);
        _animancer.States.GetOrCreate(_cachedState);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 复用缓存的状态
            _animancer.Play(_cachedState);
        }
    }
}
```

### 3. 继承已有状态类型

```csharp
// 继承ClipState
public class EnhancedClipState : ClipState
{
    public EnhancedClipState(AnimationClip clip) : base(clip)
    {
    }

    public override void OnEnterState()
    {
        base.OnEnterState();
        // 添加自定义逻辑
    }
}
```

---

## 最佳实践

### ✅ DO（推荐做法）

1. **继承合适的基类**
```csharp
// ✅ 好：根据需求选择基类
public class MyState : ClipState { }  // 单Clip
public class MyState : MixerState { } // 混合器
public class MyState : AnimancerState { } // 完全自定义
```

2. **实现必需成员**
```csharp
// ✅ 好：覆盖必需的属性和方法
public override float Length => _clip.length;
protected override void CreatePlayable(out Playable playable) { }
```

3. **添加有用的构造函数**
```csharp
// ✅ 好：方便创建
public MyState(AnimationClip clip, float speed = 1f)
{
    _clip = clip;
    Speed = speed;
}
```

### ❌ DON'T（避免做法）

1. **忘记调用base方法**
```csharp
// ❌ 差：忘记调用基类
public override void OnEnterState()
{
    // 忘记 base.OnEnterState();
}
```

2. **Length返回错误值**
```csharp
// ❌ 差：返回固定值
public override float Length => 1.0f; // 应该返回实际长度
```

---

## 参考资料

### 📚 相关文档
- [Animancer States](https://kybernetik.com.au/animancer/docs/manual/playing/states/)
- [Playables API](https://docs.unity3d.com/Manual/Playables.html)

### 💡 Unity API
- `AnimationClipPlayable`
- `AnimationMixerPlayable`
- `PlayableGraph`

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+（需要 Pro 版本）
