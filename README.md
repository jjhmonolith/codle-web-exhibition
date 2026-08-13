# 코들 웹전시 랜딩 (Claude Design)

[codle.framer.website](https://codle.framer.website/) 로 운영 중인 **금성 고등 정보 AI·디지털 교육자료 웹전시** 페이지를
Claude Design(`.dc.html`) 포맷으로 재현하고, **발행사 · 학교급 4종**으로 확장한 랜딩입니다.

| 변형 | 파일 |
| --- | --- |
| 금성 고등 | `Codle Landing.dc.html` (소스 겸 기본값) |
| 금성 중등 | `Codle Landing 금성 중등.dc.html` |
| YBM 고등 | `Codle Landing YBM 고등.dc.html` |
| YBM 중등 | `Codle Landing YBM 중등.dc.html` |

원본 Framer 사이트는 브레이크포인트마다 DOM을 따로 내려보내지만, 이 재현본은
**단일 DOM + 미디어 쿼리**로 데스크톱·태블릿·모바일을 모두 처리합니다.

## 구성

```
Codle Landing.dc.html   페이지 전체 (마크업 + 스타일 + 로직) · 4종 공통 소스
build-variants.py       나머지 3종 생성
assets/                 파비콘, 애플 터치 아이콘, OG 이미지
media/                  수업·맞춤학습 데모 영상 6종 (H.264 mp4)
support.js              Claude Design 런타임 (vendored)
image-slot.js           Claude Design 이미지 슬롯 런타임 (vendored)
uploads/                Claude Design 첨부
.thumbnail              Claude Design 카드 썸네일 (609x640 WebP)
docs/원본-대조-평가.md    원본 대비 대조 분석 및 작업 기록
```

## 4종을 만드는 방식

발행사 이름 · 학교급 · 워드마크는 `variant` prop 으로 갈립니다. 컴포넌트 안 `BRANDS` / `LEVELS`
설정에서 값을 읽어 본문에 `{{ }}` 로 흘려보내므로, Claude Design 에서는 prop 하나만 바꾸면
4종이 즉시 전환됩니다.

다만 `<helmet>` 안의 `<title>` 과 OG 메타는 **런타임 보간이 되지 않습니다.** 크롤러는 JS를
실행하지 않으므로 링크 미리보기를 제대로 뽑으려면 변형마다 메타가 정적으로 박힌 파일이 필요합니다.
`build-variants.py` 가 그 일만 합니다.

```bash
python3 build-variants.py
```

카피나 레이아웃을 고칠 때는 **`Codle Landing.dc.html` 만 고치고 다시 빌드**하면 됩니다.

### 브랜드별로 갈리는 것

| 항목 | 금성 | YBM |
| --- | --- | --- |
| 워드마크 | `#m-kumsung` 심볼 | `#m-ybm` 심볼 |
| 히어로 배지 | `{학교급} 정보 AI∙디지털 교육자료` | 동일 |
| 해결 섹션 제목 | `이미 금성&코들이 해결했어요!` | `이미 YBM&코들이…` |
| 모바일 CTA | `금성x코들이 함께 할게요!` + 금성 캐릭터 | `YBMx코들이…`, **캐릭터 없음** |
| 푸터 | (주)금성출판사 / 마포구 / 080-969-1000 | (주)와이비엠 / 종로구 / 1544-0554 |
| OG 카드 | `assets/og-kumsung-*.png` | `assets/og-ybm-*.png` |

### 체험하기 버튼이 여는 데모 교실

발행사·학교급마다 테넌트와 교실 id 가 다릅니다. 운영 중인 각 랜딩에서 확인한 값입니다.

| 변형 | 데모 URL |
| --- | --- |
| 금성 고등 | `https://2v8p.aidt.me/demos?id=zvOMpET-bvA&user_type=teacher\|student` |
| 금성 중등 | `https://2dnn.aidt.me/demos?id=O3X3ULB4Ljc&user_type=teacher\|student` |
| YBM 고등 | `https://he75.aidt.me/demos?id=W9z60U3s9NI&user_type=teacher\|student` |
| YBM 중등 | `https://dgfz.aidt.me/demos?id=cnDDMoVANU8&user_type=teacher\|student` |

주소는 `build-variants.py` 가 **정적으로 박아 넣습니다.** JS가 실패해도 링크는 살아 있습니다.
런타임이 하는 일은 행사용으로 붙는 `?authCode=` 를 `guest_id` 로 얹어주는 것뿐입니다.
`...?authCode=2024-12-03-exhibition-01` 로 접속하면 버튼 링크에 `&guest_id=2024-12-03-exhibition-01` 이 붙습니다.

### 4종이 공유하는 것

과목 내용과 광고 카피가 같으므로 아래는 그대로 씁니다.

- 데모 영상 10개 전부. 발행사 로고도 학교급 표기도 들어 있지 않습니다
- 3D 오브젝트, 코들 마스코트, 코들 로고, 파비콘
- 수업 / AI 기능 / 맞춤 학습 섹션 카피, 레이아웃, 반응형, 인터랙션 로직

## 메타데이터

`<helmet>` 안에 문서 제목, description, 파비콘, OG/트위터 카드를 선언합니다.
아이콘과 OG 이미지는 외부 CDN을 핫링크하지 않고 `assets/` 에 포함해 자급자족합니다.

| 항목 | 값 |
| --- | --- |
| `<title>` | `{발행사} {학교급} 정보 AI 디지털 교육 자료 웹전시` |
| 파비콘 | `assets/favicon.png` (32x32, 코들 말풍선 마크) |
| 애플 터치 아이콘 | `assets/apple-touch-icon.png` (180x180) |
| OG / 트위터 이미지 | `assets/og-{브랜드}-{학교급}.png` (1200x630, `summary_large_image`) |
| `theme-color` | `#3E88FF` |

## 미리보기

```bash
python3 -m http.server 8777
# http://localhost:8777/Codle%20Landing.dc.html
```

`support.js` 를 상대 경로로 불러오므로 `file://` 로 직접 열면 동작하지 않습니다. 반드시 HTTP로 서빙하세요.

## 섹션

| # | 섹션 | 내용 |
| --- | --- | --- |
| 1 | 히어로 | 3D 오브젝트 부유 + 헤드라인 마퀴 + 브랜드 락업 + 체험하기 CTA |
| 2 | 해결 | 말풍선 칩 캐스케이드 + 3D 일러스트 |
| 3 | 수업 기능 | 5개 기능, 텍스트 위 / 데모 영상 아래 |
| 4 | AI 기능 | 학생용·선생님용 2슬라이드 캐러셀 |
| 5 | 맞춤 학습 | 3개 카드, 라벤더 배경 미디어 + 중앙 정렬 카피 |
| 6 | 체험 가이드 CTA | **모바일 전용** (원본 데스크톱에는 없음) |
| 7 | 푸터 | 금성출판사 / 팀모노리스 |

## 브레이크포인트

| 구간 | 처리 |
| --- | --- |
| `>1100px` | 데스크톱 기준 |
| `≤1100px` | 타입 축소, 일러스트 재배치 |
| `600~810px` | 모바일 배치 + 타입 상향 |
| `≤810px` | 모바일. 상단 내비 숨김, 마퀴 정지, 캐러셀 컨트롤 하단 이동, CTA 섹션 노출 |
| `≤380px` | 소형 모바일 |

인라인 스타일 위에 얹어야 해서 미디어 쿼리는 `!important` 를 사용합니다.

## 인터랙션

**CSS만으로 (JS가 죽어도 무해)**

- 상단 내비 비활성 항목 hover. 활성 여부는 `data-on` 바인딩으로 CSS에 전달
- 버튼·화살표·칩·카드·미디어 hover 및 active
- `:focus-visible` 포커스 링
- `prefers-reduced-motion: reduce` 시 모든 움직임 정지

hover 규칙은 전부 `@media (hover: hover)` 안에 있습니다. 모바일 탭 후 hover 잔상을 막습니다.

**JS**

- 스크롤 스파이: passive 리스너 + rAF 1프레임 스로틀
- 스크롤 리빌: 같은 핸들러에 얹음. `IntersectionObserver` 를 쓰지 않는 이유는
  앵커 점프로 여러 화면을 건너뛸 때 지나친 요소가 `opacity: 0` 으로 남기 때문
- AI 캐러셀: 화살표 / 도트 / 키보드 좌우 방향키 / 모바일 스와이프
- 영상: 화면에서 한 뷰포트 이상 떨어지면 정지, 가까워지면 재생

리빌은 JS가 `.js-reveal` 을 붙인 뒤에만 `opacity: 0` 이 적용됩니다. JS가 실패하면 본문은 처음부터 보입니다.

## 알려진 차이

원본 대비 의도적으로 다르게 둔 부분입니다.

- 해결 섹션 일러스트 부유, AI 말풍선 띠 마퀴, 맞춤학습 원형 회전 배지를 정지 상태로 유지
- 카피는 데스크톱 기준으로 통일. 원본은 브레이크포인트마다 카피가 다름
  (데스크톱 `고등 정보` vs 모바일 `중등 정보` 등)

자세한 대조 결과는 [docs/원본-대조-평가.md](docs/원본-대조-평가.md) 참고.

## 알아둘 것

- OG 카드 4종은 사이트 디자인 토큰으로 직접 생성한 것입니다. 발행사에서 공식 카드를 받으면
  같은 파일명으로 교체하면 됩니다
- YBM 회사 정보(주소·고객센터)는 공개 정보 기준입니다. 실제 표기와 다르면
  `Codle Landing.dc.html` 의 `BRANDS.ybm` 에서 고치고 다시 빌드하세요
- 데모 영상은 마이크로비트·메이크코드 중심이라 중등 정보에 더 가깝습니다.
  고등용으로 파이썬 위주 영상이 필요하면 `media/` 만 교체하면 됩니다

## 저작권

페이지에 포함된 브랜드 자산과 화면 캡처 영상의 권리는 **(주)금성출판사**, **(주)와이비엠**,
**(주)팀모노리스** 에 있습니다.
