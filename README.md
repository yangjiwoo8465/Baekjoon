# 백준(BOJ) 자동화 프로젝트

VS Code에서 백준 문제 풀이를 효율적으로 관리하고 자동으로 GitHub에 백업하는 환경입니다.

## 📋 프로젝트 개요

이 프로젝트는 백준 온라인 저지(Baekjoon Online Judge) 문제 풀이를 위한 완전 자동화된 개발 환경입니다.

**주요 기능:**
- 🔧 **BOJ-extension**: 문제 파일 생성 및 테스트
- 🚀 **Goinmul**: 백준 로그인 및 코드 제출
- 📦 **GitDoc**: 저장 시 자동 Git 커밋 및 GitHub 푸시
- 🔐 **SSH 인증**: 안전한 GitHub 연결

---

## 🛠️ 설치된 확장 프로그램

### 1. BOJ-extension (`dltkdgns00.boj-ex`)
문제 파일 자동 생성 및 테스트를 지원합니다.

**주요 기능:**
- 문제 번호로 파일 자동 생성
- 헤더 코멘트 자동 삽입
- 테스트 케이스 실행 (Python, C++, Java, Rust, JS 지원)
- GitHub 워크플로우 생성

### 2. Goinmul (`ckcks12.goinmul`)
백준 로그인 및 코드 제출을 지원합니다.

**주요 기능:**
- 쿠키 기반 로그인
- 현재 파일 백준에 제출
- 문제 번호 자동 저장

### 3. GitDoc (`vsls-contrib.gitdoc`)
파일 저장 시 자동으로 Git 커밋 및 푸시합니다.

**주요 기능:**
- 저장할 때마다 자동 커밋
- 자동 GitHub 푸시
- 커스텀 커밋 메시지 포맷

---

## ⚙️ 설정 파일

### [.vscode/settings.json](.vscode/settings.json)

```json
{
  // Goinmul 설정 (로그인 및 제출)
  "goinmul.baekjoon.id": "your_baekjoon_id",
  "goinmul.baekjoon.pw": "your_baekjoon_password",
  "goinmul.baekjoon.lang": "python3",
  "goinmul.baekjoon.open": "close",

  // BOJ-extension 설정 (파일 생성 및 테스트)
  "boj-ex.language": "python",
  "boj-ex.userid": "your_baekjoon_id",

  // GitDoc 설정 (자동 커밋 및 푸시)
  "gitdoc.enabled": true,
  "gitdoc.autoPush": "onSave",
  "gitdoc.commitMessageFormat": "Solve: BOJ ${message}"
}
```

### [.gitignore](.gitignore)

```
__pycache__
.DS_Store
input.txt
output.txt
.vscode        # 로그인 정보가 포함된 settings.json 제외
*.class
*.exe
```

---

## 🚀 사용 방법

### 1️⃣ 초기 설정

#### Goinmul 설정
1. [.vscode/settings.json](.vscode/settings.json) 열기
2. 백준 계정 정보 입력
   ```json
   "goinmul.baekjoon.id": "your_baekjoon_id",
   "goinmul.baekjoon.pw": "your_baekjoon_password",
   "goinmul.baekjoon.lang": "python3",
   ```
   > ⚠️ **보안**: `.vscode/` 폴더는 `.gitignore`에 포함되어 있어 Git에 업로드되지 않습니다.
3. `F1` → **"백준 로그인"** 실행하여 로그인 확인

#### BOJ-extension 사용자 ID 설정
1. [.vscode/settings.json](.vscode/settings.json) 열기
2. `"boj-ex.userid"` 값에 백준 아이디 입력
   ```json
   "boj-ex.userid": "yangjiwoo8465"
   ```

---

### 2️⃣ 문제 풀이 워크플로우

#### 방법 A: BOJ-extension 사용 (추천)

1. **문제 파일 생성**
   - VS Code 사이드바에서 BOJ-extension 아이콘 클릭
   - "문제 보기" 또는 "문제 생성" 선택
   - 문제 번호 입력

2. **코드 작성**
   - 자동 생성된 파일에 코드 작성
   - 저장하면 GitDoc이 자동으로 커밋 및 푸시

3. **테스트 실행**
   - BOJ-extension의 테스트 기능 사용
   - 테스트 케이스 자동 검증

4. **제출**
   - BOJ-extension의 "제출하기" 버튼 클릭
   - 코드가 클립보드에 자동 복사됨
   - 열린 백준 제출 페이지에 붙여넣기 후 제출

#### 방법 B: Goinmul 직접 제출

1. **코드 작성 및 저장**
   - `.py`, `.cpp`, `.java` 등의 파일 생성
   - 코드 작성 후 저장 (GitDoc이 자동 커밋)

2. **백준에 제출**
   - `F1` → **"백준 제출"** 또는 **"baekjoon submit"**
   - 문제 번호 입력
   - 자동으로 백준에 제출됨

> ⚠️ **주의**: 백준의 보안 강화로 인해 Goinmul의 자동 제출이 작동하지 않을 수 있습니다. 이 경우 방법 A(BOJ-extension)를 사용하세요.

---

### 3️⃣ Git 및 GitHub 관리

#### 자동 백업
- 파일을 저장할 때마다 GitDoc이 자동으로:
  1. `git add .`
  2. `git commit -m "Solve: BOJ <파일명>"`
  3. `git push origin main`

#### 수동 커밋 (필요 시)
```bash
cd Baekjoon
git add .
git commit -m "Solve: BOJ 1000"
git push
```

#### 원격 저장소
- **Repository**: https://github.com/yangjiwoo8465/Baekjoon
- **인증 방식**: SSH (git@github.com:yangjiwoo8465/Baekjoon.git)

---

## 📁 프로젝트 구조

```
Baekjoon/
├── .git/                   # Git 저장소
├── .vscode/
│   └── settings.json       # VS Code 및 확장 설정 (ID/PW 포함, Git 제외)
├── .gitignore              # Git 제외 파일 목록
├── README.md               # 프로젝트 설명서 (이 파일)
└── [문제 파일들]            # 백준 문제 풀이 코드
    ├── 1000.py
    ├── 1001.py
    └── ...
```

---

## 🔧 트러블슈팅

### Goinmul 제출이 안 될 때
**증상**: "Goinmul: Submit" 명령이 실패하거나 오류 발생

**해결 방법**:
1. BOJ-extension의 제출 기능 사용 (클립보드 복사 방식)
2. 백준 웹사이트에서 직접 제출

### GitDoc 자동 푸시가 안 될 때
**증상**: 파일을 저장해도 GitHub에 업로드되지 않음

**확인 사항**:
1. SSH 키가 GitHub에 등록되어 있는지 확인
   ```bash
   ssh -T git@github.com
   ```
   성공 메시지: `Hi yangjiwoo8465! You've successfully authenticated...`

2. GitDoc 설정 확인
   - [.vscode/settings.json](.vscode/settings.json)에서 `"gitdoc.enabled": true` 확인

3. Git 상태 확인
   ```bash
   cd Baekjoon
   git status
   ```

### SSH 인증 실패 시
**증상**: `Permission denied (publickey)` 오류

**해결 방법**:
1. GitHub에 SSH 키 등록 확인: https://github.com/settings/keys
2. SSH 키 재등록
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   출력된 공개키를 GitHub에 등록

---

## 📚 참고 자료

### 확장 프로그램
- [BOJ-extension](https://github.com/dltkdgns00/BOJ-extension) - GitHub Repository
- [Goinmul](https://marketplace.visualstudio.com/items?itemName=ckcks12.goinmul) - VS Code Marketplace
- [GitDoc](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.gitdoc) - VS Code Marketplace

### 백준 관련
- [백준 온라인 저지](https://www.acmicpc.net/) - 공식 사이트
- [백준 문제 풀이 환경 구축](https://blog.koder.page/vscode-ps-env/) - 참고 블로그

### Git 및 GitHub
- [GitHub SSH 설정 가이드](https://docs.github.com/ko/authentication/connecting-to-github-with-ssh) - 공식 문서

---

## 🎯 추천 워크플로우

1. **매일 문제 풀이**
   - BOJ-extension으로 문제 파일 생성
   - 코드 작성 및 테스트
   - 저장 → GitDoc이 자동으로 GitHub에 백업

2. **코드 제출**
   - BOJ-extension의 제출 버튼 클릭 (클립보드 복사)
   - 백준 사이트에서 붙여넣기 후 제출

3. **주기적으로 확인**
   - GitHub Repository에서 풀이 기록 확인
   - 커밋 히스토리로 학습 진행도 추적

---

## 📝 라이선스

이 프로젝트는 개인 학습 목적으로 만들어졌습니다.

---

## ✨ 기여자

- **yangjiwoo8465** - 프로젝트 생성 및 관리

---

**Happy Coding! 🚀**
