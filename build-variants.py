#!/usr/bin/env python3
"""브랜드/학교급 변형 파일을 생성한다.

`Codle Landing.dc.html` 하나가 단일 소스다. 본문의 발행사 이름·학교급·워드마크는
`variant` prop 으로 런타임에 갈리지만, <helmet> 안의 title/OG 메타는 런타임 보간이
되지 않는다. 크롤러는 JS를 실행하지 않으므로 링크 미리보기를 제대로 뽑으려면
변형마다 메타가 정적으로 박힌 파일이 필요하다.

이 스크립트가 하는 일은 세 가지뿐이다.
  1. <helmet> 의 title / description / OG / 트위터 메타 교체
  2. `variant` prop 의 default 교체

`Codle Landing.dc.html` 자체가 금성 고등 변형이자 편집 대상이라 다시 쓰지 않는다.

사용:  python3 build-variants.py
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "Codle Landing.dc.html"

VARIANTS = {
    "kumsung-middle": {
        "file": "Codle Landing 금성 중등.dc.html",
        "publisher": "금성",
        "level": "중등",
        "og": "./assets/og-kumsung-middle.png",
    },
    "ybm-high": {
        "file": "Codle Landing YBM 고등.dc.html",
        "publisher": "YBM",
        "level": "고등",
        "og": "./assets/og-ybm-high.png",
    },
    "ybm-middle": {
        "file": "Codle Landing YBM 중등.dc.html",
        "publisher": "YBM",
        "level": "중등",
        "og": "./assets/og-ybm-middle.png",
    },
}

DESCRIPTION = "교과 내용부터 AI 교육까지 한 번에! 500개 학교가 증명한 코들!"


def title_for(cfg):
    return f"{cfg['publisher']} {cfg['level']} 정보 AI 디지털 교육 자료 웹전시"


def patch_meta(src, cfg):
    title = title_for(cfg)
    rules = [
        (r"<title>.*?</title>", f"<title>{title}</title>"),
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{title}">'),
        (r'<meta property="og:title" content="[^"]*">',
         f'<meta property="og:title" content="{title}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{DESCRIPTION}">'),
        (r'<meta property="og:image" content="[^"]*">',
         f'<meta property="og:image" content="{cfg["og"]}">'),
        (r'<meta name="twitter:title" content="[^"]*">',
         f'<meta name="twitter:title" content="{title}">'),
        (r'<meta name="twitter:description" content="[^"]*">',
         f'<meta name="twitter:description" content="{DESCRIPTION}">'),
        (r'<meta name="twitter:image" content="[^"]*">',
         f'<meta name="twitter:image" content="{cfg["og"]}">'),
    ]
    for pattern, replacement in rules:
        src, n = re.subn(pattern, replacement, src, count=1)
        if n != 1:
            raise SystemExit(f"메타 치환 실패: {pattern}")
    return src


def patch_variant_prop(src, key):
    match = re.search(r'data-props="([^"]*)"', src)
    if not match:
        raise SystemExit("data-props 를 찾지 못했다")
    props = json.loads(html.unescape(match.group(1)))
    props["variant"]["default"] = key
    encoded = html.escape(json.dumps(props, ensure_ascii=False), quote=True)
    return src[: match.start(1)] + encoded + src[match.end(1):]


def main():
    src = SOURCE.read_text(encoding="utf-8")

    for key, cfg in VARIANTS.items():
        out = patch_variant_prop(patch_meta(src, cfg), key)
        path = ROOT / cfg["file"]
        path.write_text(out, encoding="utf-8")
        print(f"  {cfg['file']:<38} {title_for(cfg)}")

    print(f"\n{len(VARIANTS)}개 변형 생성 완료 (금성 고등은 소스 파일 자체)")


if __name__ == "__main__":
    sys.exit(main())
