---
title: "Animancer - Timeline"
date: 2025-12-25
draft: false
---

# Animancer - Timeline 官方文档

## 📋 目录
- [概述](#概述)
- [PlayableAssetTransition](#playableassettransition)
- [PlayableAssetState](#playableassetstate)
- [代码示例](#代码示例)
- [重要限制](#重要限制)
- [最佳实践](#最佳实践)
- [参考资料](#参考资料)

---

## 概述

**Timeline 集成**允许 Animancer 播放 Unity Timeline 资产作为动画状态。

> **⚠️ 授权要求：此功能仅限 Pro 版本**

### 🎯 典型应用场景

- 过场动画（Cutscene）
- 复杂的多轨道动画序列
- 带特效、音频、相机的动画

### 核心类型

| 类型 | 说明 |
|------|------|
| **PlayableAssetTransition** | Timeline 转换配置 |
| **PlayableAssetState** | Timeline 播放状态 |

---

## PlayableAssetTransition

### 基本用法

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

public class TimelineExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _cutsceneTimeline;

    void Start()
    {
        // 创建 Timeline 转换
        var transition = new PlayableAssetTransition
        {
            Asset = _cutsceneTimeline,
            FadeDuration = 0.25f
        };

        // 播放 Timeline
        _animancer.Play(transition);
    }
}
```

### Transition 配置

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

public class TimelineTransitionConfig : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _timeline;

    void PlayTimeline()
    {
        var transition = new PlayableAssetTransition
        {
            // Timeline 资产
            Asset = _timeline,

            // 淡入时间
            FadeDuration = 0.5f,

            // 播放速度
            Speed = 1f,

            // 是否循环
            IsLooping = false,

            // 起始时间（秒）
            NormalizedStartTime = 0f
        };

        var state = _animancer.Play(transition);

        // 添加结束事件
        state.Events.OnEnd = OnTimelineEnd;
    }

    void OnTimelineEnd()
    {
        Debug.Log("Timeline 播放完成");
    }
}
```

---

## PlayableAssetState

### 状态访问

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

public class TimelineStateAccess : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _timeline;

    private PlayableAssetState _timelineState;

    void Start()
    {
        // 播放并获取状态
        _timelineState = _animancer.Play(_timeline) as PlayableAssetState;

        if (_timelineState != null)
        {
            Debug.Log($"Timeline 长度: {_timelineState.Length}秒");
            Debug.Log($"当前时间: {_timelineState.Time}秒");
        }
    }

    void Update()
    {
        if (_timelineState != null)
        {
            // 查询播放进度
            float progress = _timelineState.NormalizedTime;
            Debug.Log($"播放进度: {progress * 100}%");
        }
    }
}
```

### 播放控制

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

public class TimelineControl : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _timeline;

    private PlayableAssetState _state;

    void Start()
    {
        _state = _animancer.Play(_timeline) as PlayableAssetState;
    }

    void Update()
    {
        if (_state == null) return;

        // 暂停/继续
        if (Input.GetKeyDown(KeyCode.Space))
        {
            _state.IsPlaying = !_state.IsPlaying;
        }

        // 调整速度
        if (Input.GetKeyDown(KeyCode.Alpha1))
            _state.Speed = 0.5f; // 慢速

        if (Input.GetKeyDown(KeyCode.Alpha2))
            _state.Speed = 1f;   // 正常

        if (Input.GetKeyDown(KeyCode.Alpha3))
            _state.Speed = 2f;   // 快速

        // 跳转到指定时间
        if (Input.GetKeyDown(KeyCode.R))
            _state.Time = 0; // 重置到开始
    }
}
```

---

## 代码示例

### 示例1：过场动画系统

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;
using System;

/// <summary>
/// 过场动画播放器
/// </summary>
public class CutscenePlayer : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset[] _cutscenes;

    private PlayableAssetState _currentCutscene;
    private int _currentIndex = 0;

    public event Action OnCutsceneComplete;
    public event Action OnAllCutscenesComplete;

    public void PlayCutscene(int index)
    {
        if (index < 0 || index >= _cutscenes.Length)
        {
            Debug.LogError($"过场动画索引 {index} 超出范围");
            return;
        }

        _currentIndex = index;
        var timeline = _cutscenes[index];

        // 播放 Timeline
        var transition = new PlayableAssetTransition
        {
            Asset = timeline,
            FadeDuration = 0.5f
        };

        _currentCutscene = _animancer.Play(transition) as PlayableAssetState;

        // 添加完成回调
        if (_currentCutscene != null)
        {
            _currentCutscene.Events.OnEnd = OnCutsceneEnd;
        }

        Debug.Log($"播放过场动画 {index}: {timeline.name}");
    }

    public void PlayNext()
    {
        if (_currentIndex + 1 < _cutscenes.Length)
        {
            PlayCutscene(_currentIndex + 1);
        }
        else
        {
            Debug.Log("所有过场动画已播放完毕");
            OnAllCutscenesComplete?.Invoke();
        }
    }

    public void Skip()
    {
        if (_currentCutscene != null)
        {
            _currentCutscene.Time = _currentCutscene.Length;
        }
    }

    public void Pause()
    {
        if (_currentCutscene != null)
        {
            _currentCutscene.IsPlaying = false;
        }
    }

    public void Resume()
    {
        if (_currentCutscene != null)
        {
            _currentCutscene.IsPlaying = true;
        }
    }

    void OnCutsceneEnd()
    {
        Debug.Log($"过场动画 {_currentIndex} 播放完成");
        OnCutsceneComplete?.Invoke();
    }

    void Update()
    {
        // 按 Esc 跳过
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Skip();
        }

        // 按 Space 暂停/继续
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (_currentCutscene != null)
            {
                _currentCutscene.IsPlaying = !_currentCutscene.IsPlaying;
            }
        }
    }
}
```

### 示例2：Timeline 序列播放器

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;
using System.Collections.Generic;

/// <summary>
/// Timeline 序列播放器
/// 按顺序播放多个 Timeline
/// </summary>
public class TimelineSequence : MonoBehaviour
{
    [System.Serializable]
    public class TimelineEntry
    {
        public PlayableAsset Timeline;
        public float FadeDuration = 0.25f;
        public bool WaitForCompletion = true;
    }

    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private List<TimelineEntry> _sequence;

    private int _currentIndex = 0;
    private PlayableAssetState _currentState;

    void Start()
    {
        PlaySequence();
    }

    public void PlaySequence()
    {
        _currentIndex = 0;
        PlayCurrent();
    }

    void PlayCurrent()
    {
        if (_currentIndex >= _sequence.Count)
        {
            Debug.Log("序列播放完成");
            return;
        }

        var entry = _sequence[_currentIndex];

        var transition = new PlayableAssetTransition
        {
            Asset = entry.Timeline,
            FadeDuration = entry.FadeDuration
        };

        _currentState = _animancer.Play(transition) as PlayableAssetState;

        if (_currentState != null && entry.WaitForCompletion)
        {
            _currentState.Events.OnEnd = PlayNext;
        }
        else
        {
            // 立即播放下一个
            PlayNext();
        }

        Debug.Log($"播放 Timeline {_currentIndex}: {entry.Timeline.name}");
    }

    void PlayNext()
    {
        _currentIndex++;
        PlayCurrent();
    }
}
```

### 示例3：Timeline 与动画混合

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;

/// <summary>
/// Timeline 与普通动画的混合
/// </summary>
public class TimelineBlending : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _cutsceneTimeline;
    [SerializeField] private AnimationClip _idleClip;
    [SerializeField] private AnimationClip _walkClip;

    void Start()
    {
        // 初始播放 Idle
        _animancer.Play(_idleClip);
    }

    public void PlayCutscene()
    {
        // 从 Idle/Walk 淡入到 Timeline
        var transition = new PlayableAssetTransition
        {
            Asset = _cutsceneTimeline,
            FadeDuration = 0.5f // 平滑过渡
        };

        var state = _animancer.Play(transition);

        // Timeline 结束后返回 Idle
        state.Events.OnEnd = () =>
        {
            _animancer.Play(_idleClip, 0.5f);
        };
    }

    public void StopCutscene()
    {
        // 随时可以打断 Timeline 返回游戏动画
        _animancer.Play(_walkClip, 0.25f);
    }
}
```

### 示例4：Timeline 事件监听

```csharp
using Animancer;
using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;

/// <summary>
/// 监听 Timeline 中的事件
/// </summary>
public class TimelineEventListener : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _animancer;
    [SerializeField] private PlayableAsset _timeline;

    void Start()
    {
        PlayTimelineWithEvents();
    }

    void PlayTimelineWithEvents()
    {
        var state = _animancer.Play(_timeline) as PlayableAssetState;

        if (state != null)
        {
            // 在25%进度触发事件
            state.Events.AddNormalized(0.25f, () =>
            {
                Debug.Log("Timeline 播放到 25%");
            });

            // 在50%进度触发事件
            state.Events.AddNormalized(0.5f, () =>
            {
                Debug.Log("Timeline 播放到 50%");
            });

            // 在75%进度触发事件
            state.Events.AddNormalized(0.75f, () =>
            {
                Debug.Log("Timeline 播放到 75%");
            });

            // 结束事件
            state.Events.OnEnd = () =>
            {
                Debug.Log("Timeline 播放完成");
            };
        }
    }
}
```

---

## 重要限制

### ⚠️ 限制1：不支持多个 Animator

> **Timeline 默认控制场景中的所有 Animator，但 Animancer 只能控制一个。**

```csharp
// ❌ 问题：Timeline 有多个 Animation Track 绑定不同角色
// Timeline:
//   - Track 1 → Character A (Animator)
//   - Track 2 → Character B (Animator)
//   - Track 3 → Character C (Animator)

// Animancer 只能控制一个 Animator（通常是主角）
_animancer.Play(_timeline); // 只有主角会播放动画
```

**解决方案**：为每个角色创建单独的 Timeline

```csharp
// ✅ 每个角色自己的 Timeline
[SerializeField] private PlayableAsset _characterATimeline;
[SerializeField] private PlayableAsset _characterBTimeline;

_characterA.Animancer.Play(_characterATimeline);
_characterB.Animancer.Play(_characterBTimeline);
```

### ⚠️ 限制2：无法在 Timeline 中引用 Animancer 状态

```csharp
// ❌ 不支持：在 Timeline Track 中直接引用 Animancer 状态
// Timeline 使用 Animation Clip，不能直接使用 Animancer Transition
```

**解决方案**：使用原始 AnimationClip

```csharp
// ✅ 在 Timeline 中使用 AnimationClip
// Timeline Animation Track → 拖入 .anim 文件
```

### ⚠️ 限制3：Timeline 内的事件优先级高

```csharp
// ⚠️ 注意：Timeline 自带的 Signal 和 Marker 优先级更高
// 如果 Timeline 中已有事件，Animancer Events 可能不会触发
```

---

## 最佳实践

### ✅ DO（推荐做法）

#### 1. 为过场动画使用 Timeline

```csharp
// ✅ 好：复杂过场动画用 Timeline
var cutscene = new PlayableAssetTransition
{
    Asset = _cinematicTimeline,
    FadeDuration = 1f
};
_animancer.Play(cutscene);
```

#### 2. 缓存 PlayableAssetState

```csharp
// ✅ 好：缓存状态以便控制
private PlayableAssetState _cutsceneState;

void PlayCutscene()
{
    _cutsceneState = _animancer.Play(_timeline) as PlayableAssetState;
}

void Skip()
{
    if (_cutsceneState != null)
        _cutsceneState.Time = _cutsceneState.Length;
}
```

#### 3. 添加结束回调

```csharp
// ✅ 好：处理 Timeline 结束
state.Events.OnEnd = () =>
{
    // 返回游戏状态
    _animancer.Play(_idleClip);
};
```

### ❌ DON'T（避免做法）

#### 1. 在游戏循环中使用 Timeline

```csharp
// ❌ 差：Timeline 不适合游戏循环动画
_animancer.Play(_walkTimeline); // 用 AnimationClip 代替
```

#### 2. 过度依赖 Timeline

```csharp
// ❌ 差：简单动画不需要 Timeline
var simpleAnim = new PlayableAssetTransition
{
    Asset = _oneClipTimeline // 直接用 AnimationClip
};

// ✅ 好
_animancer.Play(_animClip);
```

#### 3. 忘记释放资源

```csharp
// ❌ 差：不清理
_animancer.Play(_timeline);

// ✅ 好：播放完毕后停止
state.Events.OnEnd = () =>
{
    _animancer.Stop(state);
};
```

---

## FAQ

### Q1: Timeline 和 AnimationClip 有什么区别？

**A:**

| 特性 | AnimationClip | Timeline |
|------|---------------|----------|
| **用途** | 单个动画 | 多轨道序列 |
| **复杂度** | 简单 | 复杂 |
| **性能** | 轻量 | 较重 |
| **适用场景** | 游戏循环动画 | 过场动画 |

### Q2: 如何在 Timeline 中控制多个角色？

**A:** 为每个角色创建独立的 Timeline 或使用 PlayableDirector：

```csharp
// 方案1：每个角色单独的 Timeline
_characterA.Animancer.Play(_timelineA);
_characterB.Animancer.Play(_timelineB);

// 方案2：使用 Unity 的 PlayableDirector
GetComponent<PlayableDirector>().Play(_multiCharTimeline);
```

### Q3: Timeline 播放期间可以切换到其他动画吗？

**A:** 可以，使用 `Play()` 打断：

```csharp
// 播放 Timeline
var state = _animancer.Play(_timeline);

// 随时可以打断
if (Input.GetKeyDown(KeyCode.Escape))
{
    _animancer.Play(_idleClip, 0.25f); // 打断并淡入 Idle
}
```

### Q4: 如何循环播放 Timeline？

**A:** 设置 IsLooping：

```csharp
var transition = new PlayableAssetTransition
{
    Asset = _timeline,
    IsLooping = true // 循环播放
};
_animancer.Play(transition);
```

### Q5: Timeline 性能如何？

**A:** Timeline 比普通 AnimationClip 开销更大：

- **AnimationClip**: ~0.1ms
- **Timeline (1 track)**: ~0.3ms
- **Timeline (多 track)**: ~1ms+

因此，仅在需要多轨道功能时使用 Timeline。

---

## 参考资料

### 📚 相关文档
- [Unity Timeline Manual](https://docs.unity3d.com/Packages/com.unity.timeline@latest)
- [Playables API](https://docs.unity3d.com/Manual/Playables.html)
- [Animancer Pro Features](https://kybernetik.com.au/animancer/docs/manual/timeline/)

### 💡 相关类型
- `PlayableAssetTransition` - Timeline 转换配置
- `PlayableAssetState` - Timeline 播放状态
- `PlayableAsset` - Unity Timeline 资产基类
- `PlayableDirector` - Unity Timeline 播放器

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+ (Pro Only)
