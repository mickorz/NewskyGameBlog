# Animancer Transition Libraries 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/transitions/libraries/
> 抓取日期：2025-01-24
> **注意**：这是 Animancer Pro 专属功能

---

## 概述 (Overview)

**Transition Libraries** 是 Animancer **Pro 版本**的独占功能，允许开发者**无需编写额外代码**即可定义动画库如何修改特定的动画过渡组合。

### 核心功能

> "定义如何修改特定的过渡组合，而无需额外代码"

**主要用途**：
1. **自动调整淡入时长**：根据动画状态变化自动设置 Fade Duration
2. **动画别名系统**：为动画分配自定义名称，通过字符串播放动画
3. **集中管理**：作为中心动画列表，统一管理所有动画资源

---

## 关键组件 (Key Components)

### Library 窗口功能

打开 Transition Library 窗口后，你会看到以下界面：

```
┌────────────────────────────────────────────┐
│ Transition Library                         │
├────────────────────────────────────────────┤
│ Pages: [▼ Modifiers] [Aliases]             │  ← 页面切换下拉菜单
├────────────────────────────────────────────┤
│ Asset: [PlayerAnimationLibrary.asset]  [○] │  ← 资源路径（可点击选中）
├────────────────────────────────────────────┤
│ [Revert] [Apply] [☑ Auto Apply]           │  ← 管理按钮
├────────────────────────────────────────────┤
│                                            │
│ (Modifiers 或 Aliases 页面内容)           │
│                                            │
└────────────────────────────────────────────┘
```

#### 1. **Pages 下拉菜单**

切换不同的功能页面：
- **Modifiers（修改器）**：设置动画间的过渡规则
- **Aliases（别名）**：为动画分配自定义名称

#### 2. **Asset 路径显示**

显示当前编辑的 Library 资源文件路径，点击可在 Project 窗口中选中该资源。

#### 3. **管理按钮**

- **Revert（还原）**：撤销未保存的修改
- **Apply（应用）**：保存当前的修改
- **Auto Apply（自动应用）**：
  - 启用后，修改会实时生效
  - **在 Play Mode 下**特别有用，可以即时预览效果
  - 退出 Play Mode 时会提示是否保存

---

## Modifiers 系统（过渡修改器）

### 功能说明

Transition Modifiers 页面允许你**自定义特定动画转换**的过渡时长。

### 工作原理

通过一个**表格界面**来配置动画间的过渡：

```
        │  Idle  │  Walk  │  Run   │  Attack │
────────┼────────┼────────┼────────┼─────────┤
 Idle   │   -    │  0.25  │  0.30  │  0.10   │
────────┼────────┼────────┼────────┼─────────┤
 Walk   │  0.25  │   -    │  0.20  │  0.15   │
────────┼────────┼────────┼────────┼─────────┤
 Run    │  0.30  │  0.20  │   -    │  0.20   │
────────┼────────┼────────┼────────┼─────────┤
 Attack │  0.15  │  0.15  │  0.15  │   -     │
```

**说明**：
- **行**：表示 "From"（从哪个动画）
- **列**：表示 "To"（到哪个动画）
- **单元格值**：该转换的 Fade Duration
- **加粗数字**：表示已自定义的值
- **普通数字**：表示使用目标动画的默认 Fade Duration

---

### 使用示例

#### 场景：角色从 Walk 切换到 Shoot

**默认行为**：
```csharp
// Shoot.asset 的默认 Fade Duration = 0.1s
_Animancer.Play(_ShootAnimation);
// 从任何动画切换到 Shoot 都使用 0.1s
```

**使用 Modifier 后**：
```
在 Library 的 Modifiers 表格中设置：
Walk → Shoot = 0.05s  (快速反应)
Run  → Shoot = 0.05s  (快速反应)
Idle → Shoot = 0.1s   (保持默认)
```

**效果**：
- 从 Walk 切换到 Shoot：使用 0.05s（更快的战斗反应）
- 从 Run 切换到 Shoot：使用 0.05s
- 从 Idle 切换到 Shoot：使用 0.1s（默认值）

---

### 创建和配置步骤

#### 步骤1：创建 Transition Library

```
方法一：菜单创建
1. 右键 Project 窗口
2. Create → Animancer → Transition Library
3. 命名为 "PlayerAnimationLibrary"

方法二：代码创建
ScriptableObject.CreateInstance<TransitionLibrary>();
```

#### 步骤2：添加 TransitionAsset

**方法A：在 Library 窗口中创建**

```
1. 打开 Transition Library 窗口
2. 点击 "Create Transition" 按钮
3. 配置 Transition 并保存为 Sub-Asset
```

**方法B：拖入现有的 TransitionAsset**

```
1. 先创建 TransitionAsset（Assets → Create → Animancer → Transition Asset）
2. 将其拖入 Transition Library 窗口
```

**文件结构（Sub-Asset 方式）**：
```
PlayerAnimationLibrary.asset
├─ Idle (Sub-Asset)
├─ Walk (Sub-Asset)
├─ Run (Sub-Asset)
└─ Attack (Sub-Asset)
```

#### 步骤3：配置 Modifiers 表格

```
1. 切换到 "Modifiers" 页面
2. 点击表格中的单元格
3. 输入自定义的 Fade Duration 值
4. 点击 "Apply" 保存
```

**配置示例**：
```
         │  Idle  │  Walk  │  Run
─────────┼────────┼────────┼────────
 Idle    │   -    │  0.25  │  0.30
 Walk    │  0.25  │   -    │  0.20
 Run     │  0.30  │  0.20  │   -
```

---

### 代码集成

#### 使用 Transition Library

```csharp
using Animancer;
using UnityEngine;

public class PlayerAnimations : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    // 引用 Transition Library
    [SerializeField]
    private TransitionLibrary _AnimationLibrary;

    // 引用 Library 中的 Transition Assets
    [SerializeField]
    private TransitionAsset _Idle;

    [SerializeField]
    private TransitionAsset _Walk;

    [SerializeField]
    private TransitionAsset _Run;

    void Update()
    {
        float speed = GetMovementSpeed();

        // 播放动画，Library 会自动应用正确的 Fade Duration
        if (speed < 0.1f)
        {
            _Animancer.Play(_Idle);
            // Library 自动处理从当前动画到 Idle 的过渡
        }
        else if (speed < 3f)
        {
            _Animancer.Play(_Walk);
            // Library 自动处理过渡
        }
        else
        {
            _Animancer.Play(_Run);
            // Library 自动处理过渡
        }
    }

    float GetMovementSpeed()
    {
        // 返回当前移动速度
        return 2.5f;
    }
}
```

**关键点**：
- Library 会**自动**根据配置的 Modifiers 调整 Fade Duration
- 你只需要调用 `Play()`，无需手动设置淡入时长
- 所有过渡规则都集中在 Library 中管理

---

## Aliases 功能（动画别名系统）

### 功能说明

Transition Aliases 页面允许你为动画**分配自定义名称**，从而可以通过字符串播放动画，**无需直接引用 TransitionAsset**。

### 使用场景

#### 场景1：基于配置的动画系统

```csharp
// 通过字符串配置动画
[System.Serializable]
public class SkillConfig
{
    public string SkillName;
    public string AnimationAlias; // 使用别名而非直接引用
}
```

#### 场景2：动态动画加载

```csharp
// 根据技能名称动态播放动画
public void PlaySkillAnimation(string skillName)
{
    string alias = GetAnimationAlias(skillName);
    _Animancer.TryPlay(alias); // 通过别名播放
}
```

---

### 配置步骤

#### 步骤1：在 Library 中设置别名

```
1. 打开 Transition Library 窗口
2. 切换到 "Aliases" 页面
3. 为每个 Transition 分配别名
```

**配置示例**：
```
┌──────────────────┬──────────────────┐
│ Transition       │ Alias            │
├──────────────────┼──────────────────┤
│ Idle.asset       │ "idle"           │
│ Walk.asset       │ "walk"           │
│ Run.asset        │ "run"            │
│ Attack1.asset    │ "attack_light"   │
│ Attack2.asset    │ "attack_heavy"   │
│ Skill_Fireball   │ "skill_fire"     │
└──────────────────┴──────────────────┘
```

#### 步骤2：代码中使用别名

```csharp
using Animancer;
using UnityEngine;

public class AliasExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    void Update()
    {
        // 使用别名播放动画
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.TryPlay("walk");
        }
        else
        {
            _Animancer.TryPlay("idle");
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            _Animancer.TryPlay("attack_light");
        }

        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            _Animancer.TryPlay("skill_fire");
        }
    }
}
```

---

### 高级应用

#### 应用1：技能系统集成

```csharp
using Animancer;
using UnityEngine;

[System.Serializable]
public class Skill
{
    public string SkillName;
    public string AnimationAlias;
    public float Cooldown;
}

public class SkillSystem : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private Skill[] _Skills;

    public void CastSkill(int skillIndex)
    {
        if (skillIndex < 0 || skillIndex >= _Skills.Length)
            return;

        Skill skill = _Skills[skillIndex];

        // 通过别名播放技能动画
        if (_Animancer.TryPlay(skill.AnimationAlias))
        {
            Debug.Log($"释放技能: {skill.SkillName}");
        }
        else
        {
            Debug.LogWarning($"未找到动画别名: {skill.AnimationAlias}");
        }
    }
}
```

**Inspector 配置**：
```
Skills:
├─ [0] 火球术
│  ├─ Skill Name: "Fireball"
│  ├─ Animation Alias: "skill_fire"
│  └─ Cooldown: 5
├─ [1] 冰冻术
│  ├─ Skill Name: "Ice Blast"
│  ├─ Animation Alias: "skill_ice"
│  └─ Cooldown: 8
```

---

#### 应用2：状态机集成

```csharp
using Animancer;
using UnityEngine;

public class StateMachineWithAliases : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    private enum CharacterState
    {
        Idle,
        Walk,
        Run,
        Attack,
        Defend
    }

    private CharacterState _CurrentState;

    // 状态到别名的映射
    private readonly System.Collections.Generic.Dictionary<CharacterState, string> _StateToAlias =
        new System.Collections.Generic.Dictionary<CharacterState, string>()
        {
            { CharacterState.Idle, "idle" },
            { CharacterState.Walk, "walk" },
            { CharacterState.Run, "run" },
            { CharacterState.Attack, "attack" },
            { CharacterState.Defend, "defend" }
        };

    public void ChangeState(CharacterState newState)
    {
        _CurrentState = newState;

        // 通过别名播放对应的动画
        if (_StateToAlias.TryGetValue(newState, out string alias))
        {
            _Animancer.TryPlay(alias);
        }
    }

    void Update()
    {
        // 根据输入切换状态
        if (Input.GetKey(KeyCode.W))
            ChangeState(CharacterState.Walk);
        else if (Input.GetKey(KeyCode.LeftShift))
            ChangeState(CharacterState.Run);
        else if (Input.GetKeyDown(KeyCode.Mouse0))
            ChangeState(CharacterState.Attack);
        else
            ChangeState(CharacterState.Idle);
    }
}
```

---

#### 应用3：多语言/多配置支持

```csharp
// 不同地区使用不同的动画别名
public class LocalizedAnimations : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 根据地区配置不同的别名映射
    private System.Collections.Generic.Dictionary<string, string> GetRegionalAliases()
    {
        string region = GetCurrentRegion();

        switch (region)
        {
            case "JP":
                return new System.Collections.Generic.Dictionary<string, string>()
                {
                    { "greeting", "bow" },          // 日本：鞠躬
                    { "celebration", "clap_hands" }
                };

            case "US":
                return new System.Collections.Generic.Dictionary<string, string>()
                {
                    { "greeting", "wave_hand" },    // 美国：挥手
                    { "celebration", "fist_pump" }
                };

            default:
                return new System.Collections.Generic.Dictionary<string, string>();
        }
    }

    public void PlayGreeting()
    {
        var aliases = GetRegionalAliases();
        if (aliases.TryGetValue("greeting", out string alias))
        {
            _Animancer.TryPlay(alias);
        }
    }

    string GetCurrentRegion() => "US"; // 示例
}
```

---

## 相关示例 (Related Samples)

Animancer 提供了几个示例来演示 Transition Libraries 的用法：

### 1. Library Character

**展示内容**：
- Transition Library 的基本使用
- 如何创建和配置 Library
- Modifiers 的基础应用

### 2. Named Character

**展示内容**：
- 动画别名系统的实现
- 通过字符串播放动画
- 别名在状态机中的应用

### 3. Animation Serialization

**展示内容**：
- 使用 Library 作为中心动画列表
- 序列化动画数据
- 运行时动态加载动画

---

## 实战案例

### 案例1：完整的角色动画系统

```csharp
using Animancer;
using UnityEngine;

/// <summary>
/// 使用 Transition Library 的完整角色动画系统
/// </summary>
public class CompleteCharacterSystem : MonoBehaviour
{
    [Header("组件引用")]
    [SerializeField] private AnimancerComponent _Animancer;

    [Header("动画库")]
    [SerializeField] private TransitionLibrary _AnimationLibrary;

    [Header("移动动画")]
    [SerializeField] private TransitionAsset _Idle;
    [SerializeField] private TransitionAsset _Walk;
    [SerializeField] private TransitionAsset _Run;

    [Header("战斗动画")]
    [SerializeField] private TransitionAsset _Attack1;
    [SerializeField] private TransitionAsset _Attack2;
    [SerializeField] private TransitionAsset _Defend;

    [Header("技能动画（使用别名）")]
    private const string SKILL_FIRE = "skill_fire";
    private const string SKILL_ICE = "skill_ice";
    private const string SKILL_LIGHTNING = "skill_lightning";

    // 当前状态
    private enum State { Idle, Walk, Run, Attack, Defend, Skill }
    private State _CurrentState = State.Idle;

    void Update()
    {
        HandleMovement();
        HandleCombat();
        HandleSkills();
    }

    void HandleMovement()
    {
        float speed = GetMovementSpeed();

        if (speed < 0.1f && _CurrentState != State.Idle)
        {
            _CurrentState = State.Idle;
            _Animancer.Play(_Idle);
            // Library 自动处理从其他动画到 Idle 的过渡
        }
        else if (speed < 3f && _CurrentState != State.Walk)
        {
            _CurrentState = State.Walk;
            _Animancer.Play(_Walk);
        }
        else if (speed >= 3f && _CurrentState != State.Run)
        {
            _CurrentState = State.Run;
            _Animancer.Play(_Run);
        }
    }

    void HandleCombat()
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            _CurrentState = State.Attack;
            _Animancer.Play(_Attack1);
        }
        else if (Input.GetKeyDown(KeyCode.Mouse1))
        {
            _CurrentState = State.Attack;
            _Animancer.Play(_Attack2);
        }
        else if (Input.GetKey(KeyCode.LeftShift))
        {
            _CurrentState = State.Defend;
            _Animancer.Play(_Defend);
        }
    }

    void HandleSkills()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            _CurrentState = State.Skill;
            _Animancer.TryPlay(SKILL_FIRE); // 使用别名
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            _CurrentState = State.Skill;
            _Animancer.TryPlay(SKILL_ICE);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            _CurrentState = State.Skill;
            _Animancer.TryPlay(SKILL_LIGHTNING);
        }
    }

    float GetMovementSpeed()
    {
        Vector2 input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
        return input.magnitude * 5f;
    }
}
```

**Library 配置**：
```
PlayerAnimationLibrary.asset
├─ Modifiers:
│  ├─ Idle → Walk: 0.25
│  ├─ Walk → Run: 0.20
│  ├─ Run → Attack: 0.10
│  └─ Any → Defend: 0.05
└─ Aliases:
   ├─ Skill_Fireball → "skill_fire"
   ├─ Skill_IceBlast → "skill_ice"
   └─ Skill_Lightning → "skill_lightning"
```

---

### 案例2：敌人 AI 动画系统

```csharp
using Animancer;
using UnityEngine;

public class EnemyAI : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionLibrary _EnemyAnimLibrary;

    // 使用别名系统
    private const string IDLE = "enemy_idle";
    private const string PATROL = "enemy_patrol";
    private const string CHASE = "enemy_chase";
    private const string ATTACK = "enemy_attack";
    private const string HIT = "enemy_hit";
    private const string DEATH = "enemy_death";

    private enum AIState { Idle, Patrol, Chase, Attack, Hit, Death }
    private AIState _CurrentState;

    public void ChangeState(AIState newState)
    {
        if (_CurrentState == newState) return;

        _CurrentState = newState;

        // 通过别名播放对应动画
        string alias = GetAliasForState(newState);
        _Animancer.TryPlay(alias);
    }

    string GetAliasForState(AIState state)
    {
        switch (state)
        {
            case AIState.Idle: return IDLE;
            case AIState.Patrol: return PATROL;
            case AIState.Chase: return CHASE;
            case AIState.Attack: return ATTACK;
            case AIState.Hit: return HIT;
            case AIState.Death: return DEATH;
            default: return IDLE;
        }
    }

    void Update()
    {
        // AI 逻辑示例
        float distanceToPlayer = GetDistanceToPlayer();

        if (distanceToPlayer > 10f)
        {
            ChangeState(AIState.Patrol);
        }
        else if (distanceToPlayer > 2f)
        {
            ChangeState(AIState.Chase);
        }
        else
        {
            ChangeState(AIState.Attack);
        }
    }

    float GetDistanceToPlayer()
    {
        // 返回到玩家的距离
        return 5f; // 示例值
    }
}
```

---

## 最佳实践

### 1. **合理组织 Library 结构**

**推荐做法**：
```
为不同角色类型创建独立的 Library

Assets/Animations/Libraries/
├─ PlayerAnimationLibrary.asset
├─ EnemyMeleeLibrary.asset
├─ EnemyRangedLibrary.asset
└─ NPCLibrary.asset
```

**好处**：
- 避免单一 Library 过于庞大
- 便于团队协作
- 减少冲突风险

---

### 2. **Modifiers 设置原则**

**原则**：只配置需要特殊处理的过渡

```
❌ 不推荐：为每个过渡都设置值
Idle → Walk: 0.25
Idle → Run: 0.25
Idle → Attack: 0.25
...（所有组合都设置）

✅ 推荐：只设置特殊的过渡
Run → Attack: 0.05  (需要快速反应)
Walk → Defend: 0.05 (需要快速防御)
其他：使用默认值
```

---

### 3. **别名命名规范**

**推荐命名方式**：

```
格式：{类别}_{动作}_{变体}

示例：
├─ move_idle
├─ move_walk
├─ move_run
├─ combat_attack_light
├─ combat_attack_heavy
├─ combat_defend
├─ skill_fire_cast
├─ skill_fire_loop
└─ skill_fire_end
```

**好处**：
- 清晰的层次结构
- 易于搜索和过滤
- 支持自动化工具处理

---

### 4. **使用 Auto Apply 的时机**

**何时启用**：
- ✅ 在 Play Mode 下调试动画过渡
- ✅ 需要实时预览效果
- ✅ 快速迭代阶段

**何时禁用**：
- ❌ 正式开发阶段（避免误操作）
- ❌ 多人协作时（避免意外保存）

---

## 常见问题 FAQ

### Q1: Transition Library 是否必须使用？

**A**: 不是必须的。Library 是一个**优化工具**，适合以下场景：
- 大量动画需要管理
- 需要精细控制动画间的过渡
- 使用别名系统

小型项目可以不使用 Library。

---

### Q2: 免费版可以使用 Transition Library 吗？

**A**: 不可以。Transition Library 是 **Animancer Pro** 专属功能。

---

### Q3: Modifiers 和直接设置 FadeDuration 有什么区别？

**A**:

**直接设置**：
```csharp
transition.FadeDuration = 0.5f;
// 从任何动画切换都使用 0.5s
```

**使用 Modifiers**：
```
可以为不同的"来源动画"设置不同的过渡时长
Walk → Attack: 0.1s
Run → Attack: 0.05s
Idle → Attack: 0.15s
```

---

### Q4: 如何在代码中访问 Library 的别名？

**A**: 使用 `TryPlay` 方法：

```csharp
// 返回 AnimancerState，如果找不到则返回 null
AnimancerState state = _Animancer.TryPlay("alias_name");

if (state != null)
{
    Debug.Log("动画播放成功");
}
else
{
    Debug.LogWarning("未找到别名");
}
```

---

### Q5: 可以在运行时修改 Library 吗？

**A**: 可以，但不推荐。Library 是 ScriptableObject，运行时的修改不会保存。

**如果需要动态调整**：
```csharp
// 运行时临时修改
transition.FadeDuration = 0.5f;
_Animancer.Play(transition);
```

---

## 总结

### 核心要点

1. **Transition Library 是 Pro 功能**
   - 需要 Animancer Pro 版本
   - 提供高级动画管理能力

2. **两大核心功能**
   - **Modifiers**：自定义动画间的过渡规则
   - **Aliases**：通过字符串名称播放动画

3. **适用场景**
   - 大量动画需要管理
   - 需要精细控制过渡
   - 基于配置的动画系统

4. **最佳实践**
   - 合理组织 Library 结构
   - 只配置特殊的过渡
   - 使用规范的别名命名
   - 谨慎使用 Auto Apply

### Library 功能速查表

| 功能 | 用途 | 适用场景 |
|------|------|---------|
| **Modifiers** | 自定义过渡时长 | 需要精细控制过渡效果 |
| **Aliases** | 字符串播放动画 | 配置驱动的动画系统 |
| **Auto Apply** | 实时预览效果 | 调试和快速迭代 |
| **Sub-Assets** | 集中管理资源 | 统一动画配置 |

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/transitions/libraries/
**Animancer 版本**：7.0+ Pro
**适用项目**：animator-third-person-controller (ShooterTPP)
