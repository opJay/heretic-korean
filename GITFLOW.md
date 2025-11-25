# Git Workflow for Heretic Korean Fork

이 문서는 `heretic-korean` 포크에서 원본 레포지토리(`p-e-w/heretic`)와의 동기화를 유지하면서 한국어 지원을 추가하는 Git 워크플로우를 설명합니다.

---

## ⚠️ 중요: 기본 브랜치

**이 레포지토리의 기본 브랜치는 `korean`입니다.**

- ✅ GitHub에서 레포지토리를 방문하면 **`korean` 브랜치**가 기본으로 표시됩니다
- ✅ Clone 시 자동으로 **`korean` 브랜치**가 체크아웃됩니다
- ✅ **한글 README.md**가 기본으로 표시됩니다
- ⚠️ `master` 브랜치는 upstream 동기화 전용으로 사용됩니다

### Clone 시 확인

```bash
# 기본 clone
git clone https://github.com/opJay/heretic-korean.git
cd heretic-korean

# 현재 브랜치 확인
git branch
# * korean  ← 기본 브랜치

# 모든 브랜치 확인
git branch -a
# * korean
#   master
#   remotes/origin/HEAD -> origin/korean
#   remotes/origin/korean
#   remotes/origin/master
```

**왜 korean을 기본 브랜치로 했나요?**

1. **한국어 사용자 경험**: GitHub 방문 시 한글 README가 즉시 보임
2. **작업 편의성**: 대부분의 작업이 korean 브랜치에서 진행됨
3. **명확한 목적**: 이 포크의 주 목적이 한국어 지원임을 명시

---

## 📊 브랜치 전략

### 브랜치 구조

```
upstream (원본)          origin (내 포크)         local (로컬)
─────────────          ────────────────         ───────────
p-e-w/heretic          opJay/heretic-korean

┌─────────┐            ┌─────────┐              ┌─────────┐
│ master  │────pull───→│ master  │────pull─────→│ master  │
└─────────┘            └─────────┘              └─────────┘
                                                      │
                                                   checkout
                                                      ↓
                       ┌─────────┐              ┌─────────┐
                       │ korean  │←────push─────│ korean  │
                       └─────────┘              └─────────┘
```

### 각 브랜치의 역할

- **`master` 브랜치**: 원본(`upstream`)과 동일하게 유지, 동기화 전용
- **`korean` 브랜치**: 한국어 지원을 위한 모든 수정사항 포함, 실제 작업 브랜치

### 왜 이런 전략을 사용하나요?

1. **충돌 최소화**: master를 원본과 동일하게 유지하면 동기화가 항상 간단함
2. **명확한 분리**: 한국어 수정사항이 korean 브랜치에만 있어 관리가 쉬움
3. **원본 추적 용이**: 원본에 어떤 변경사항이 있었는지 master를 통해 명확히 파악

---

## 🚀 초기 설정 (한 번만 실행)

이미 완료되었지만, 참고용으로 기록합니다.

### 1. Remote 확인 및 설정

```bash
# 현재 remote 확인
git remote -v

# 출력 예시:
# origin    https://github.com/opJay/heretic-korean.git (fetch)
# origin    https://github.com/opJay/heretic-korean.git (push)
# upstream  https://github.com/p-e-w/heretic.git (fetch)
# upstream  https://github.com/p-e-w/heretic.git (push)
```

**upstream이 없다면 추가:**
```bash
git remote add upstream https://github.com/p-e-w/heretic.git
```

### 2. Upstream과 동기화

```bash
# upstream의 최신 변경사항 가져오기
git fetch upstream

# master로 전환
git checkout master

# upstream/master 병합
git merge upstream/master

# GitHub 포크에 push
git push origin master
```

### 3. Korean 브랜치 생성

```bash
# korean 브랜치 생성 및 전환
git checkout -b korean

# GitHub에 korean 브랜치 생성 및 추적 설정
git push -u origin korean
```

---

## 🔄 정기 동기화 프로세스

원본 레포지토리에 새로운 업데이트가 있을 때마다 실행합니다.

### Phase 1: Master 동기화

```bash
# 1. master 브랜치로 전환
git checkout master

# 2. 현재 상태 확인 (선택사항)
git status

# 3. upstream에서 최신 변경사항 가져오기
git fetch upstream

# 4. upstream/master를 local master에 병합
git merge upstream/master

# 5. origin/master에 push
git push origin master
```

**각 단계 설명:**

#### `git checkout master`
- 작업 브랜치를 master로 변경
- 파일들이 master 브랜치 상태로 바뀜

#### `git fetch upstream`
- upstream의 모든 브랜치와 태그 다운로드
- 파일은 변경하지 않음 (`.git` 폴더에만 저장)

**출력 예시:**
```
From https://github.com/p-e-w/heretic
   1efc4ee..abc1234  master     -> upstream/master
 * [new tag]         v2.0.0     -> v2.0.0
```

#### `git merge upstream/master`
- upstream/master의 커밋들을 local master에 통합

**케이스 1: Fast-forward (가장 일반적)**
```
Updating 1efc4ee..abc1234
Fast-forward
 src/heretic/model.py | 15 +++++++++++++++
 README.md            |  3 ++-
 2 files changed, 17 insertions(+), 1 deletion(-)
```
→ master를 건드리지 않았으므로 항상 fast-forward됩니다.

**케이스 2: 이미 최신**
```
Already up to date.
```

#### `git push origin master`
- GitHub의 내 포크(origin)를 최신 상태로 업데이트

---

### Phase 2: Korean 브랜치에 반영

```bash
# 1. korean 브랜치로 전환
git checkout korean

# 2. master의 변경사항을 korean에 병합
git merge master

# 3. 충돌이 없다면 push
git push origin korean
```

**각 단계 설명:**

#### `git checkout korean`
- korean 브랜치로 전환
- 한국어 설정 파일 등이 보임

#### `git merge master`
- master의 최신 변경사항을 korean에 통합

**케이스 1: 충돌 없음 (이상적)**
```
Merge made by the 'ort' strategy.
 src/heretic/model.py | 15 +++++++++++++++
 1 file changed, 15 insertions(+)
```
→ 자동으로 병합 커밋 생성

**케이스 2: 충돌 발생**
```
Auto-merging config.default.toml
CONFLICT (content): Merge conflict in config.default.toml
Automatic merge failed; fix conflicts and then commit the result.
```
→ 수동 해결 필요 (아래 참조)

#### `git push origin korean`
- GitHub의 korean 브랜치 업데이트

---

## ⚠️ 충돌 해결 가이드

### 1. 충돌 파일 확인

```bash
git status
```

**출력:**
```
Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.default.toml
```

### 2. 충돌 파일 열기

**충돌 표시 예시:**
```toml
<<<<<<< HEAD (korean 브랜치의 내용)
refusal_markers = [
    "죄송",
    "미안",
    "할 수 없",
]
=======
refusal_markers = [
    "sorry",
    "i can't",
    "i apologize",  # ← 원본에서 새로 추가됨
]
>>>>>>> master
```

### 3. 수동으로 통합

**통합 결과:**
```toml
refusal_markers = [
    # 한국어 패턴
    "죄송",
    "미안",
    "할 수 없",
    # 영어 패턴 (원본 업데이트 반영)
    "sorry",
    "i can't",
    "i apologize",
]
```

### 4. 충돌 해결 완료

```bash
# 충돌 해결된 파일 staging
git add config.default.toml

# 병합 커밋 완료
git commit

# 기본 메시지 사용 또는 수정:
# "Merge branch 'master' into korean"

# Push
git push origin korean
```

### 5. 충돌이 너무 복잡할 때

```bash
# 병합 취소하고 처음부터
git merge --abort

# 상태 확인
git status
# On branch korean
# nothing to commit, working tree clean
```

---

## 🎯 일상 작업 흐름

### 새로운 한국어 기능 추가할 때

```bash
# 1. korean 브랜치에 있는지 확인
git branch
# * korean  ← 현재 브랜치

# 2. (선택) 최신 상태로 동기화
git checkout master
git fetch upstream
git merge upstream/master
git push origin master
git checkout korean
git merge master

# 3. 작업 진행
# - config.korean.toml 수정
# - README.ko.md 작성
# - 데이터셋 추가 등

# 4. 변경사항 확인
git status
git diff

# 5. Staging
git add <파일들>

# 6. 커밋
git commit -m "Add Korean refusal markers to config"

# 7. Push
git push origin korean
```

---

## 📋 빠른 참조 명령어

### 한 줄로 동기화

```bash
# Master 동기화
git checkout master && git fetch upstream && git merge upstream/master && git push origin master

# Korean에 반영
git checkout korean && git merge master && git push origin korean
```

### 상태 확인

```bash
# 현재 브랜치 확인
git branch

# Remote 상태 확인
git remote -v

# 변경사항 확인
git status

# 커밋 히스토리 (그래프)
git log --oneline --graph --all -10
```

### 되돌리기

```bash
# 마지막 커밋 취소 (push 전)
git reset --soft HEAD~1

# 마지막 커밋 완전 제거 (push 전)
git reset --hard HEAD~1

# Push 후 되돌리기 (새 커밋으로)
git revert HEAD
git push
```

---

## 🔧 충돌 최소화 팁

### 1. 파일 분리 전략

**충돌 확률 높음 ❌**
```
config.default.toml 수정 (원본도 자주 수정)
README.md 수정 (원본도 자주 수정)
```

**충돌 확률 낮음 ✅**
```
config.korean.toml 생성 (새 파일)
README.ko.md 생성 (새 파일)
datasets/ 디렉토리 추가 (새 디렉토리)
```

### 2. 주석으로 구분

원본 파일을 수정해야 한다면:

```python
# ===== KOREAN CUSTOMIZATION START =====
korean_markers = ["죄송", "미안"]
# ===== KOREAN CUSTOMIZATION END =====
```

### 3. 정기 동기화

- **작업 시작 전**: 항상 최신 상태로 동기화
- **주 1회**: 정기적으로 upstream 확인
- **중요 릴리스**: 원본에 새 버전이 나오면 즉시 동기화

---

## 🆘 문제 해결

### Q: "Your branch is behind 'origin/korean' by 3 commits"

**원인:** 다른 컴퓨터나 GitHub에서 직접 수정한 경우

**해결:**
```bash
git pull origin korean
```

### Q: Push가 rejected됨

**에러:**
```
! [rejected]        korean -> korean (non-fast-forward)
error: failed to push some refs
```

**해결:**
```bash
# 원격 변경사항 먼저 가져오기
git pull origin korean

# 충돌 해결 후
git push origin korean
```

### Q: 실수로 master에서 작업했을 때

```bash
# 현재 변경사항을 stash에 임시 저장
git stash

# korean 브랜치로 전환
git checkout korean

# stash에서 변경사항 복원
git stash pop
```

---

## 📅 동기화 체크리스트

### 주기적 실행 (주 1회 권장)

- [ ] `git checkout master`
- [ ] `git fetch upstream`
- [ ] `git merge upstream/master`
- [ ] 충돌 확인 및 해결
- [ ] `git push origin master`
- [ ] `git checkout korean`
- [ ] `git merge master`
- [ ] 충돌 확인 및 해결
- [ ] `git push origin korean`
- [ ] `git log --graph --oneline -10` 으로 결과 확인

---

## 🎓 Git 명령어 상세 설명

### `git fetch upstream`

**기능:** 원격 레포지토리의 변경사항을 다운로드 (병합하지 않음)

**내부 동작:**
1. upstream과 연결
2. 모든 브랜치와 태그 정보 다운로드
3. `.git/refs/remotes/upstream/` 에 저장

**장점:** 안전함 - 로컬 파일은 변경되지 않음

---

### `git merge upstream/master`

**기능:** upstream/master의 커밋들을 현재 브랜치에 통합

**병합 타입:**

**1) Fast-forward (빠른 감기)**
```
Before:
  A---B---C  (upstream/master)
       \
        (master - 변경사항 없음)

After:
  A---B---C  (master)
```
조건: 현재 브랜치에 새 커밋이 없을 때
메시지: `Fast-forward`

**2) 3-way Merge**
```
Before:
  A---B---C  (upstream/master)
       \
        D---E  (master)

After:
  A---B---C------M  (master)
       \        /
        D---E--/
```
조건: 양쪽 모두 새 커밋이 있을 때
메시지: `Merge made by the 'ort' strategy`

**3) 충돌 발생**
```
CONFLICT (content): Merge conflict in <파일>
```
조건: 같은 파일의 같은 부분을 수정했을 때

---

### `git push -u origin korean`

**기능:** 로컬 브랜치를 원격에 push하고 추적 관계 설정

**옵션 설명:**
- `-u` (또는 `--set-upstream`): 추적 관계 설정
- `origin`: 원격 이름
- `korean`: 브랜치 이름

**추적 관계란?**
설정 후에는 다음처럼 간단하게 사용 가능:
```bash
# -u 설정 전
git push origin korean

# -u 설정 후
git push  # 자동으로 origin/korean에 push됨
git pull  # 자동으로 origin/korean에서 pull함
```

---

## 🌳 Git 히스토리 시각화

### 동기화 전

```bash
git log --oneline --graph --all -10
```

```
* f1a2b3c (HEAD -> korean, origin/korean) Add Korean config
* e4d5c6b Add Korean README
* 1efc4ee (origin/master, master) Featuring Notebook Compatibility
* 452b35e Add trust_remote_code configuration option
```

### 동기화 후

```
*   a1b2c3d (HEAD -> korean, origin/korean) Merge master into korean
|\
| * 9876543 (upstream/master, origin/master, master) Add new optimization
| * 5432109 Fix bug in evaluator
|/
* f1a2b3c Add Korean config
* e4d5c6b Add Korean README
* 1efc4ee Featuring Notebook Compatibility
```

**해석:**
- 새 커밋 `9876543`, `5432109`가 master를 통해 korean에 병합됨
- 병합 커밋 `a1b2c3d`가 생성됨
- korean 브랜치가 최신 원본 코드 + 한국어 수정사항 포함

---

## 🎯 실전 시나리오

### 시나리오 1: 원본에 새 기능 추가됨

**상황:** upstream에 새 모델 아키텍처 지원이 추가됨

**워크플로우:**
```bash
# 1. Master 동기화
git checkout master
git fetch upstream
git merge upstream/master  # Fast-forward로 새 기능 받음
git push origin master

# 2. Korean에 반영
git checkout korean
git merge master           # 충돌 없음 (새 기능이라서)
git push origin korean

# 완료! korean 브랜치도 새 기능 사용 가능
```

---

### 시나리오 2: 같은 파일 수정으로 충돌

**상황:** 원본이 `config.default.toml`을 수정, 나도 같은 파일 수정

**워크플로우:**
```bash
# 1. Master 동기화 (충돌 없음)
git checkout master
git fetch upstream
git merge upstream/master  # 원본 변경사항만 받음
git push origin master

# 2. Korean에 반영 시도
git checkout korean
git merge master

# 충돌 발생!
# CONFLICT (content): Merge conflict in config.default.toml
```

**충돌 해결:**
```bash
# 1. 충돌 파일 확인
git status
# Unmerged paths:
#   both modified:   config.default.toml

# 2. 에디터로 열어서 수동 병합
# <<<<<<< HEAD
# korean 브랜치의 내용
# =======
# master에서 온 내용
# >>>>>>> master

# 3. 마커 제거하고 올바르게 통합

# 4. 해결 완료 표시
git add config.default.toml

# 5. 병합 커밋 생성
git commit
# 에디터가 열림, 기본 메시지 사용 또는 수정

# 6. Push
git push origin korean
```

---

### 시나리오 3: 충돌 미리 보기

**충돌이 걱정된다면:**
```bash
# Master와 Korean의 차이 먼저 확인
git diff master..korean

# 병합 시뮬레이션 (실제 병합하지 않음)
git merge --no-commit --no-ff master

# 확인 후 취소
git merge --abort
```

---

## 🔍 유용한 명령어 모음

### 현재 상태 파악

```bash
# 간단한 상태
git status

# 상세한 상태
git status -v

# 브랜치 목록
git branch -a

# Remote 정보
git remote -v

# 최근 커밋 10개
git log --oneline -10

# 그래프로 보기
git log --oneline --graph --all -20
```

### 변경사항 확인

```bash
# 작업 디렉토리 변경사항
git diff

# Staging area 변경사항
git diff --staged

# 두 브랜치 비교
git diff master..korean

# 특정 파일 히스토리
git log --oneline -- config.korean.toml
```

### 브랜치 관리

```bash
# 브랜치 생성
git branch <이름>

# 브랜치 전환
git checkout <이름>

# 생성 + 전환
git checkout -b <이름>

# 브랜치 삭제 (로컬)
git branch -d <이름>

# 브랜치 삭제 (원격)
git push origin --delete <이름>
```

---

## 💡 Best Practices

### ✅ DO

1. **작업 전 항상 동기화**
   ```bash
   git checkout korean
   git pull origin korean
   ```

2. **커밋 메시지 명확히**
   ```bash
   git commit -m "Add Korean refusal markers for EXAONE model"
   ```

3. **자주 커밋, 자주 push**
   - 작은 단위로 커밋
   - 하루 작업 끝나면 push

4. **브랜치 확인 습관**
   ```bash
   git branch  # 커밋 전 항상 확인
   ```

### ❌ DON'T

1. **Master에서 직접 작업하지 말기**
   - Master는 동기화 전용

2. **Force push 지양**
   ```bash
   git push --force  # 위험! 협업 시 문제
   ```

3. **Pull 없이 push**
   - 항상 pull 후 push

4. **대용량 파일 커밋**
   - `.gitignore`에 추가
   - Git LFS 고려

---

## 🔗 관련 자료

- [Git 공식 문서](https://git-scm.com/doc)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)
- [Pro Git Book (한국어)](https://git-scm.com/book/ko/v2)

---

## 📞 도움이 필요할 때

**문제 발생 시:**
1. `git status` 로 현재 상태 확인
2. `git log --graph --oneline -10` 로 히스토리 확인
3. 이 문서의 해당 섹션 참조
4. 복구 불가능해 보이면: 새로운 클론으로 시작

**백업:**
```bash
# 현재 상태 백업
git branch korean-backup
```

---

## 📝 변경 이력

- 2025-11-25: 초기 버전 작성
