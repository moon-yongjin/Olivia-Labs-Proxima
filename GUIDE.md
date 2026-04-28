# 🐕 Proxima - 진돗개 에디션 마스터 가이드 (v3.1.0)

이 문서는 Proxima 프로젝트의 진돗개 에디션 개발 과정과 핵심 해결책을 기록한 **최종 마스터 가이드**입니다. 새로운 세션에서도 이 문서만 보면 모든 히스토리를 파악할 수 있습니다.

---

## 1. 🚀 핵심 성과 및 해결책

### 1.1 Grok(xAI) 자동화 완전 정복 (가장 중요!)
*   **문제점**: Grok의 Tiptap 에디터가 일반적인 타이핑 이벤트를 차단하고, 쿠키/업그레이드 팝업이 전송 버튼을 가림.
*   **해결책 (Nuclear Fix)**:
    1.  **팝업 제거**: ESC 키 전송 및 CSS(`display: none`)를 강제로 주입하여 OneTrust 쿠키 배너와 'Super Grok' 업그레이드 배너를 0.1초 만에 제거.
    2.  **직접 주입 (Deep Injection)**: `document.execCommand('insertText', ...)`를 사용하여 에디터의 내부 상태를 무시하고 텍스트를 강제로 주입.
    3.  **입력창 재포커스**: 팝업 제거 후 포커스가 유실되는 문제를 방지하기 위해 입력을 시작하기 직전 명시적으로 다시 클릭(`click()`) 및 포커스(`focus()`) 수행.

### 1.2 전용 CLI (`proxima`) 구축
*   **파일**: `cli.js` (전역 명령어 등록 완료)
*   **사용법**:
    - `proxima status`: 모든 AI 연결 상태 및 응답 속도 확인.
    - `proxima ask [provider] "[prompt]"`: 터미널에서 즉시 질문 및 답변 수신.
    - `proxima models`: 현재 사용 가능한 모델 목록 조회.

---

## 2. 📂 저장소 관리 및 배포

### 2.1 저장소 구조 (Cleanup 완료)
*   **`archive/`**: 과거의 모든 실험용 스크립트, 테스트 파일, 임시 파일들이 모여 있는 곳입니다. (root 디렉토리는 항상 클린하게 유지)
*   **`.gitignore`**: `slam_dunk*`, `test_*`, `debug_*` 등의 패턴이 자동으로 제외되도록 설정되어 있습니다.

### 2.2 자동 배포 (GitHub Actions)
*   **설정**: `.github/workflows/build.yml`
*   **프로세스**: 
    1. `package.json` 버전 수정 
    2. 새 태그(예: `v3.1.1`) 푸시 
    3. GitHub 서버가 자동으로 `.exe` 파일 빌드 및 **Releases** 페이지에 업로드.

---

## 3. 🛠️ 기술적 팁 (Future Reference)

*   **응답 캡처 오류 시**: `electron/main-v2.cjs`의 `getProviderResponse` 함수 내 `tiptap` 필터링 로직을 확인하세요.
*   **Grok UI 변경 시**: `archive/dump_grok_input.js`를 실행하여 새로운 입력창 클래스명이나 구조를 먼저 파악하세요.
*   **유튜브 채널**: 모든 업데이트 내역과 활용 가이드는 **[Real AI Logic](https://www.youtube.com/@Real_AI_Logic)** 채널을 참조하세요.

---
**이 가이드는 Proxima 진돗개 에디션의 심장과 같습니다. 어떤 문제가 생겨도 이 문서의 로직을 먼저 확인하세요!** ⚡
