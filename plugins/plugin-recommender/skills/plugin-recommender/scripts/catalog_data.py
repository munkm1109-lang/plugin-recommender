RULES = [
    {
        "terms": ["ppt", "powerpoint", "발표", "발표자료", "슬라이드", "프레젠테이션"],
        "plugins": {"Presentations": 120, "Documents": 12, "PDF": 8},
    },
    {"terms": ["pdf", "피디에프"], "plugins": {"PDF": 80, "Documents": 16}},
    {
        "terms": ["엑셀", "excel", "xlsx", "스프레드시트", "spreadsheet", "표로", "표를", "테이블", "csv"],
        "plugins": {"Spreadsheets": 80, "Data Analytics": 14},
    },
    {
        "terms": ["문서", "word", "docx", "보고서", "제안서", "메모"],
        "plugins": {"Documents": 55, "PDF": 8, "Presentations": 6},
    },
    {
        "terms": ["figma", "피그마", "디자인", "ui", "ux", "화면", "프로토타입", "컴포넌트"],
        "plugins": {"Figma": 80, "Product Design": 24},
    },
    {"terms": ["이미지", "그림", "아이콘", "시각자료", "비주얼"], "plugins": {"Product Design": 45, "Figma": 20}},
    {"terms": ["배포", "호스팅", "deploy", "deployment", "vercel"], "plugins": {"Vercel": 90, "GitHub": 18, "Browser": 10}},
    {
        "terms": ["github", "깃허브", "repo", "repository", "pr", "pull request", "issue", "이슈"],
        "plugins": {"GitHub": 90, "CodeRabbit": 20},
    },
    {"terms": ["브라우저", "browser", "localhost", "웹사이트", "화면확인"], "plugins": {"Browser": 70, "Chrome": 35}},
    {"terms": ["chrome", "크롬", "로그인 세션", "쿠키"], "plugins": {"Chrome": 80, "Browser": 18}},
    {
        "terms": ["데이터", "분석", "대시보드", "dashboard", "kpi", "지표", "차트", "리포트"],
        "plugins": {"Data Analytics": 80, "Spreadsheets": 18},
    },
    {"terms": ["notion", "노션", "task", "태스크", "업무관리"], "plugins": {"Notion": 80}},
    {"terms": ["메일", "email", "gmail", "outlook", "수신함"], "plugins": {"Gmail": 70, "Outlook Email": 70}},
    {"terms": ["캘린더", "calendar", "일정", "미팅", "회의"], "plugins": {"Google Calendar": 75, "Outlook Calendar": 55}},
]


USAGE_OVERRIDES = {
    "Presentations": "PPTX 발표자료 생성, 편집, 렌더링, 슬라이드 검수가 필요한 작업에 사용합니다.",
    "Documents": "Word/DOCX 문서 작성, 편집, 구조화, 문서형 산출물 생성에 사용합니다.",
    "PDF": "PDF 읽기, 추출, 생성, 렌더링, 시각 검수가 필요한 작업에 사용합니다.",
    "Spreadsheets": "Excel/XLSX/CSV 표 작성, 정리, 계산, 스프레드시트 산출물 생성에 사용합니다.",
    "Data Analytics": "데이터 분석, KPI 진단, 리포트, 대시보드 작성에 사용합니다.",
    "Vercel": "웹앱 배포, 호스팅, Vercel 프로젝트 확인과 배포 상태 점검에 사용합니다.",
    "GitHub": "저장소, 이슈, PR, 코드리뷰, GitHub 기반 개발 흐름에 사용합니다.",
    "Browser": "로컬 웹앱, localhost, 웹 화면 확인과 브라우저 테스트에 사용합니다.",
    "Chrome": "기존 Chrome 로그인 세션, 쿠키, 탭 상태가 필요한 웹 작업에 사용합니다.",
}
