# SecondLine 촬영 가이드 — 한글 안내 / 영어 대본

목표는 약 3분~3분 30초짜리 화면 녹화입니다. 안내는 한글이며, 인용문 안의 대본만 영어로 읽습니다. 공식 제출 안내의 영상 제한은 5분 이내·300MB 미만입니다. 최종 파일은 MP4로 준비합니다. [제출 안내](https://lablab.ai/ai-articles/hackathon-guidelines)

## 1. 녹화 준비 — 약 5분

1. Chrome에서 [공개 데모](https://secondline-voice-agent.vercel.app)를 엽니다. 계정·메일·API 키가 보이는 탭은 닫거나 녹화 영역 밖으로 옮깁니다.
2. 페이지 글자가 읽히도록 창을 크게 하고 알림을 끕니다. 앱에서 `An account code`를 선택합니다.
3. 맥 기본 녹화는 `Shift + Command + 5` → 화면 기록 → 옵션 → 사용할 마이크 선택 순서입니다. `Include System Audio` 옵션이 있으면 함께 켭니다. Apple 안내상 이 옵션은 macOS 27부터 지원됩니다. [Apple 녹화 안내](https://support.apple.com/en-ae/102618)
4. 시스템 소리 녹음 옵션이 없으면 스피커를 통해 나오는 AI 음성이 녹화용 마이크에 들어오는지 시험합니다. 이 방식에서는 이어폰을 빼고 스피커를 적당한 볼륨으로 사용합니다. 두 소리를 기록할 수 있는 기존 녹화 앱이 있으면 그것을 써도 됩니다.
5. 먼저 짧게 시험 녹화합니다. 앱을 시작하고 인사말을 들은 뒤 영어로 한 문장 말합니다. 종료·저장 후 재생해서 **내 목소리와 AI 목소리가 둘 다 들리는지** 확인합니다. 확인 후 앱을 새로고침합니다.

기본 화면 녹화 파일은 MOV로 저장될 수 있습니다. 확장자를 바꾸는 것으로 MP4 변환을 대신하지 않습니다. 촬영 후 파일 경로를 알려주면 변환과 길이·용량 검사를 이어갈 수 있습니다.

## 2. 꼭 지킬 촬영 순서

앱의 라이브 연습은 60초 뒤 종료됩니다. `Start live voice rehearsal`부터 `End exercise`까지는 **연습 답변만 말합니다**. 제품 설명도 마이크에 들어가 AI에 전달되므로 소개는 시작 전에, 결과·기술 설명은 종료 후에 읽습니다.

첫 촬영은 AI 인사말을 끝까지 듣고 답하는 구성이 가장 단순합니다. AI가 말하는 중 끼어들기를 실제로 확인한 경우에만 그 기능을 시연했다고 말합니다. 아래 기본 대본은 끼어들기 성공을 주장하지 않습니다.

## 3. 약 3분~3분 30초 촬영 대본

시간은 목표이며 AI 응답 속도에 따라 조금 달라져도 됩니다.

### 0:00–0:25 — 제품 소개

화면: 앱 맨 위 제목과 설명. 아직 라이브 버튼은 누르지 않습니다.

> Hi, I'm the creator of SecondLine. SecondLine helps people practice what to say when someone pressures them to share a code or send money. Every scenario is fictional. The goal is to pause and verify through a contact route you find yourself.

### 0:25–0:40 — 연습 선택

화면: 아래로 내려 `An account code`를 선택하고 다음 문장을 읽습니다. 다 읽은 뒤 `Start live voice rehearsal`을 누르고 마이크를 허용합니다.

> I'll demonstrate the account-code scenario using a live AssemblyAI Voice Agent session.

### 0:40–1:20 — 실제 음성 대화

화면: 연결 후 AI 인사말이 들리고 전사가 표시되는 것을 기다립니다. 인사말이 끝나면 다음 문장을 천천히 말합니다.

> Pause. I will not share a code. I will hang up and use the official app I open myself.

말한 뒤 조용히 기다려 본인 전사와 코치 답변을 보여줍니다. 코치가 연습을 마치면 `End exercise`를 누릅니다. 독립 확인 방법을 추가로 물을 때만 다음 문장을 말합니다.

> I will find the official contact number myself, not use a number the caller gives me.

코치가 이미 끝냈다면 추가 문장을 억지로 말하지 않습니다. 전체 라이브 구간은 60초 이내로 끝냅니다.

### 1:20–1:55 — 보고서 설명

화면: `What stood out?`로 내려 압박 문구 인용과 본인 대응 항목을 보여줍니다. 실제 인용과 대응 항목이 표시된 경우 다음 문장을 읽습니다.

> This report uses the words captured during my exercise. It highlights pressure cues and the boundary I practiced. It gives me a next step to try again. These are practice cues, not a verdict about whether a real caller is a scammer.

선택 사항: 오른쪽 확인 방법 입력란에 `I will open the official app myself.`를 적고 `Save my response`를 누릅니다. 저장은 현재 페이지 세션에만 적용됩니다.

### 1:55–2:30 — 기술 설명

화면: 보고서를 그대로 보여줘도 됩니다. 준비가 되어 있으면 발표 PDF 4쪽으로 전환합니다. 라이브 세션을 끝낸 상태에서 다음 대본을 읽습니다.

> AssemblyAI's Voice Agent API handles speech recognition and spoken replies. Our Python backend keeps the API key private and issues a temporary browser token. The reflection uses simple local rules applied to the captured transcript. The public application is deployed on Vercel, and the source code is available on GitHub.

### 2:30–3:25 — 이용자·기대 이점과 마무리

화면: 보고서의 본인 대응 항목을 보여준 뒤 앱 제목으로 돌아갑니다. 이 구간은 라이브 세션을 끝낸 뒤 읽습니다. 이용자와 교육 활용은 가설로 설명하며, 검증된 학습 효과나 실제 고객이 있다고 주장하지 않습니다.

> SecondLine is designed for people who know they should be careful, but struggle to find the words when someone pressures them. It lets them practice a clear refusal, ending the conversation, and choosing an independent contact route.
>
> Financial-literacy educators could use these short exercises to help learners explain their next step in their own words. The quote-linked report makes that response visible and gives them a chance to try again.
>
> These are potential benefits; we have not measured learning outcomes or real-world fraud prevention. Our goal is simple: help people rehearse the pause before a pressured decision. Thank you.

## 4. 오류가 날 때

- 마이크 허용 창이 나오면 허용하고 잠시 기다립니다. 실수로 차단했다면 Chrome 사이트 권한에서 마이크를 허용한 뒤 새로고침합니다.
- 전사가 틀리면 연습을 끝내고 새로 시작해 짧게 다시 말합니다. 필요한 대사는 위의 한 문장입니다.
- 코치가 예상과 다르게 답하면 실제 답변을 듣고 끝냅니다. 정해진 답변을 기다리며 대화를 늘리지 않습니다.
- 녹화에 AI 소리만 없으면 재촬영 전에 녹음 경로를 고칩니다. 앱에서 들리는 것과 영상에 기록된 것은 별개입니다.
- `Offline typed walkthrough`는 음성 API 시연을 대신하지 않습니다. 라이브 연결이 실패하면 오류 화면·상황을 알려주고 해결한 뒤 촬영합니다.

## 5. 촬영 후 확인

최종 영상을 재생해 다음 다섯 가지를 확인합니다.

- 내 설명·연습 답변·AI 응답이 들립니다.
- 새로 말한 영어 문장이 화면 전사에 표시됩니다.
- 그 대화에서 생성된 보고서가 보입니다.
- API 키와 개인 계정 정보가 보이지 않습니다.
- 최종 MP4가 5분 이내·300MB 미만입니다.

촬영 파일의 절대 경로를 전달하면 MP4 변환·길이·용량·음성 트랙 확인을 이어갈 수 있습니다. 영상 업로드와 최종 대회 제출은 아직 완료되지 않았습니다.
