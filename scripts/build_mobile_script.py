from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/recording-script.md'
OUTPUT = ROOT / 'output/pdf/secondline-mobile-script.pdf'
PAGE_WIDTH, PAGE_HEIGHT = 360, 640
MARGIN = 25
CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2
INK = colors.HexColor('#102926')
MUTED = colors.HexColor('#536763')
CORAL = colors.HexColor('#B45340')
PAPER = colors.HexColor('#FBF8F0')

pdfmetrics.registerFont(TTFont('Korean', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
source = SOURCE.read_text()
sections = re.findall(r'### ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)', source, re.S)
speeches = [[line[2:] for line in body.splitlines() if line.startswith('> ')] for _, body in sections]
if len(speeches) != 6 or [len(parts) for parts in speeches] != [1, 1, 2, 1, 1, 3]:
    raise ValueError('The source script structure changed; review mobile cards before export.')

styles = {
    'title': ParagraphStyle('title', fontName='Korean', fontSize=25, leading=34, textColor=INK),
    'cue': ParagraphStyle('cue', fontName='Korean', fontSize=14, leading=21, textColor=MUTED, wordWrap='CJK'),
    'english': ParagraphStyle('english', fontName='Helvetica', fontSize=21, leading=29, textColor=INK),
    'small': ParagraphStyle('small', fontName='Korean', fontSize=12, leading=18, textColor=MUTED, wordWrap='CJK'),
    'label': ParagraphStyle('label', fontName='Korean', fontSize=13, leading=20, textColor=CORAL),
}

cards = [
    {
        'step': '촬영 전', 'time': '준비 5분', 'title': '폰으로 보는\nSecondLine 대본',
        'blocks': [
            ('cue', '한글은 조작 안내입니다.<br/>영어만 소리 내어 읽으세요.'),
            ('label', '목표 영상: 약 3분 - 3분 30초'),
            ('cue', '1. 내 목소리와 AI 소리를 시험 녹화합니다.<br/>2. 앱을 새로고침합니다.<br/>3. 영어 대본을 천천히 읽습니다.'),
            ('cue', '라이브는 60초입니다.<br/>연결 중에는 연습 답변만 말하고,<br/>제품 설명은 시작 전과 종료 후에 읽습니다.'),
            ('small', '<link href="https://secondline-voice-agent.vercel.app" color="#B45340">데모 열기</link>'),
        ],
    },
    {
        'step': '01 / 소개', 'time': '0:00 - 0:25', 'title': '앱 제목을 보여주세요',
        'blocks': [('cue', '아직 라이브 버튼을 누르지 않습니다.'), ('label', '영어 대본'), ('english', escape(speeches[0][0]))],
    },
    {
        'step': '02 / 선택', 'time': '0:25 - 0:40', 'title': 'An account code 선택',
        'blocks': [('cue', '시나리오를 선택하고 아래 문장을 읽습니다.'), ('label', '영어 대본'), ('english', escape(speeches[1][0])), ('cue', '다 읽은 뒤<br/>Start live voice rehearsal 클릭<br/>마이크 허용 → AI 인사말 듣기')],
    },
    {
        'step': '03 / 라이브', 'time': '0:40 - 1:20', 'title': '인사말 뒤에 답하세요',
        'blocks': [('label', '영어 답변'), ('english', escape(speeches[2][0])), ('cue', '말한 뒤 조용히 기다립니다.<br/>내 전사와 실제 코치 답변을 보여주세요.'), ('label', '확인 방법을 추가로 물을 때만'), ('english', escape(speeches[2][1])), ('cue', '이미 끝났다면 추가 답변 없이<br/>End exercise 클릭.<br/>전체 라이브 구간은 60초 이내입니다.')],
    },
    {
        'step': '04 / 보고서', 'time': '1:20 - 1:55', 'title': 'What stood out?로 이동',
        'blocks': [('cue', '세션 종료 후 실제 문구 인용과<br/>본인 대응 항목을 보여줍니다.'), ('label', '영어 대본'), ('english', escape(speeches[3][0]))],
    },
    {
        'step': '05 / 기술', 'time': '1:55 - 2:30', 'title': '보고서 또는 PDF 4쪽',
        'blocks': [('cue', '라이브가 끝난 상태에서 읽습니다.'), ('label', '영어 대본'), ('english', escape(speeches[4][0]))],
    },
    {
        'step': '06 / 이용자', 'time': '2:30 - 3:25 · 1/3', 'title': '누구를 위한 제품인가',
        'blocks': [('cue', '보고서의 본인 대응 항목을 보여줍니다.<br/>다음 두 페이지까지 이어 읽으세요.'), ('label', '영어 대본'), ('english', escape(speeches[5][0]))],
    },
    {
        'step': '06 / 기대 이점', 'time': '2:30 - 3:25 · 2/3', 'title': '교육에서의 활용',
        'blocks': [('cue', '앞 페이지에 이어서 읽습니다.'), ('label', '영어 대본'), ('english', escape(speeches[5][1]))],
    },
    {
        'step': '06 / 마무리', 'time': '2:30 - 3:25 · 3/3', 'title': '앱 제목으로 돌아오기',
        'blocks': [('cue', '기대 효과와 아직 검증하지 않은 점을<br/>함께 설명하고 녹화를 종료합니다.'), ('label', '영어 대본'), ('english', escape(speeches[5][2]))],
    },
    {
        'step': '촬영 후', 'time': '마지막 확인', 'title': '파일을 재생하세요',
        'blocks': [
            ('cue', '□ 내 설명과 연습 답변이 들립니다.<br/><br/>□ AI 응답도 들립니다.<br/><br/>□ 새로 말한 문장이 전사됩니다.<br/><br/>□ 그 대화의 보고서가 보입니다.<br/><br/>□ API 키가 보이지 않습니다.'),
            ('label', '최종 파일: MP4 / 5분 이내 / 300MB 미만'),
            ('cue', 'MOV로 저장되면 파일 경로를 알려주세요.<br/>MP4 변환과 파일 검사를 이어갑니다.'),
            ('small', '<link href="https://lablab.ai/ai-articles/hackathon-guidelines" color="#B45340">공식 영상 제출 안내</link> · <link href="https://support.apple.com/en-ae/102618" color="#B45340">맥 녹화 안내</link>'),
        ],
    },
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
document = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
document.setTitle('SecondLine - Korean filming guide and English mobile script')
document.setAuthor('blancolabs')

for number, card in enumerate(cards, 1):
    document.setFillColor(PAPER)
    document.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    document.setFont('Helvetica-Bold', 11)
    document.setFillColor(CORAL)
    document.drawString(MARGIN, PAGE_HEIGHT - 32, 'SECONDLINE / RECORDING SCRIPT')
    document.setStrokeColor(colors.HexColor('#D5DDD4'))
    document.line(MARGIN, PAGE_HEIGHT - 46, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 46)
    cursor = PAGE_HEIGHT - 65
    blocks = [('label', escape(card['step']) + ' · ' + escape(card['time'])), ('title', escape(card['title']).replace('\n', '<br/>')), *card['blocks']]
    for kind, content in blocks:
        paragraph = Paragraph(content, styles[kind])
        _, height = paragraph.wrap(CONTENT_WIDTH, PAGE_HEIGHT)
        if cursor - height < 40:
            raise ValueError(f'Card {number} overflows; split its content instead of shrinking type.')
        paragraph.drawOn(document, MARGIN, cursor - height)
        cursor -= height + (16 if kind in ('title', 'english') else 10)
    document.setFont('Korean', 10)
    document.setFillColor(MUTED)
    document.drawString(MARGIN, 19, '한글: 안내  |  영어: 읽을 대본')
    document.drawRightString(PAGE_WIDTH - MARGIN, 19, f'{number} / {len(cards)}')
    document.showPage()

document.save()
print(f'Created {OUTPUT} ({len(cards)} mobile pages)')
