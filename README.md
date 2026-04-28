<div align="center">

# ⚡ Proxima - 진돗개 에디션 (Jindotgae Edition)

### 하나의 API로 모든 AI 모델을 제어하세요 — 통합 AI 게이트웨이

[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)](https://github.com/jindogae-lab/Jindotgae-Proxima/releases)
[![License](https://img.shields.io/badge/license-Personal%20Use-green.svg)](LICENSE)
[![YouTube](https://img.shields.io/badge/YouTube-Real_AI_Logic-red.svg)](https://www.youtube.com/@Real_AI_Logic)

**ChatGPT, Claude, Gemini, Grok**을 별도의 API 키 없이 하나로 연결합니다.  
기존 웹 계정 로그인만으로 개발 환경에서 모든 AI를 자유롭게 활용하세요.

---

## 📺 관련 유튜브 채널
이 프로젝트의 자세한 활용법과 AI 자동화 기술은 **Real AI Logic** 채널에서 확인하실 수 있습니다!

### [👉 유튜브 채널 바로가기 (구독 & 좋아요!)](https://www.youtube.com/@Real_AI_Logic)

---

## ✨ 진돗개 에디션 (v3.1.0) 주요 특징

- 🆕 **전용 CLI (`proxima`)**: 터미널에서 즉시 AI에게 질문하고 답변을 받는 강력한 명령줄 인터페이스 도입.
- 🆕 **Grok 자동화 마스터**: 복잡한 Tiptap 에디터 및 쿠키 팝업 문제를 해결하여 Grok을 완벽하게 제어.
- 🆕 **강력한 팝업 제거**: OneTrust 쿠키 배너 및 업그레이드 유도 모달 자동 제거.
- 🆕 **멀티 이미지 생성**: ChatGPT, Grok, Gemini 등 여러 AI에게 동시에 이미지 생성을 요청하고 비교 가능.

</div>

## 🚀 시작하기

### 요구 사항
- **Windows 10/11**
- **Node.js 18+** → [Node.js 다운로드](https://nodejs.org/)

### 설치 방법

1. **설치 파일로 시작 (추천)**
   - [Releases](https://github.com/jindogae-lab/Jindotgae-Proxima/releases) 페이지에서 최신 `.exe` 파일을 다운로드하여 실행하세요.

2. **소스로 실행 (개발자용)**
   ```bash
   git clone https://github.com/jindogae-lab/Jindotgae-Proxima.git
   cd Jindotgae-Proxima
   npm install
   npm start
   ```

## 🛠️ CLI 사용법 (v3.1.0 신규)

터미널 어디서든 `proxima` 명령어를 사용할 수 있습니다.

- **AI 상태 확인**: `proxima status`
- **AI에게 질문하기**: `proxima ask chatgpt "오늘 날씨 어때?"`
- **지원 모델 목록**: `proxima models`

## 🤖 지원되는 AI 공급자

- **ChatGPT**: OpenAI의 최신 GPT-4o 모델 및 DALL-E 3 이미지 생성 지원.
- **Claude**: Anthropic의 강력한 코딩 도우미.
- **Gemini**: 구글의 초거대 AI 및 이미지 생성 지원.
- **Grok (xAI)**: 실시간 정보 검색 및 Flux 엔진 기반 고퀄리티 이미지 생성.

---

## ⚙️ MCP 도구 연동 (Cursor, VS Code 등)

`Cursor`, `Windsurf`, `Claude Desktop` 등의 설정에 다음 경로를 추가하세요:

```json
{
  "mcpServers": {
    "proxima": {
      "command": "node",
      "args": ["C:/설치경로/src/mcp-server-v3.js"]
    }
  }
}
```

---

## 📄 라이선스
이 소프트웨어는 **개인적, 비상업적 용도**로만 사용 가능합니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

---

<div align="center">

**Proxima v3.1.0 - 진돗개 에디션** ⚡  
Made with ❤️ by [Real AI Logic](https://www.youtube.com/@Real_AI_Logic) & [Zen4-bit]

</div>
