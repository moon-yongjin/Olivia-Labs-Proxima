# 📋 CHANGELOG - Proxima (Jindotgae Edition)

## [3.1.0] - 2026-04-29 (현재 버전)

### ✨ 새로운 기능
- **Proxima CLI (`proxima`) 도입**: 터미널에서 AI 상태 확인 및 질문 전송 기능 추가.
- **SDK ESM 지원**: `sdk/proxima.js`에 ESM 내보내기 설정을 추가하여 CLI와의 연동성 강화.

### 🛠️ 버그 수정 및 개선
- **Grok 한국어 UI 대응**: "제출", "전송" 버튼 인식 로직 추가.
- **Grok 자동화 Breakthrough**: `document.execCommand('insertText')` 방식을 도입하여 Tiptap/ProseMirror 에디터 입력 문제 완벽 해결.
- **모달 클리너**: OneTrust 쿠키 배너 및 업그레이드 팝업 자동 제거 로직 추가.
- **응답 캡처 정밀화**: 에디터 영역이 응답에 섞이지 않도록 필터링 강화.

### 🚀 배포 사항
- `package.json`의 `bin` 필드에 `proxima` 명령어 등록 완료.
- 깃허브 리포지토리(`jindogae-lab/Jindotgae-Proxima`) 최신화.
