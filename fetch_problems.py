#!/usr/bin/env python3
"""
백준 문제 목록을 solved.ac API에서 가져와서 HTML로 생성하는 스크립트
"""

import requests
import json
from datetime import datetime

# solved.ac API 설정
API_BASE_URL = "https://solved.ac/api/v3"
PROBLEMS_PER_PAGE = 100

# 난이도 매핑 (solved.ac 티어)
TIER_NAMES = {
    1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
    6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
    11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
    16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
    21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
    26: "Ruby V", 27: "Ruby IV", 28: "Ruby III", 29: "Ruby II", 30: "Ruby I",
}

def get_tier_class(level):
    """티어 레벨을 CSS 클래스로 변환"""
    if level <= 5:
        return "bronze"
    elif level <= 10:
        return "silver"
    elif level <= 15:
        return "gold"
    elif level <= 20:
        return "platinum"
    elif level <= 25:
        return "diamond"
    else:
        return "ruby"

def fetch_problems_by_tier(tier_min, tier_max, page=1):
    """특정 난이도 범위의 문제 가져오기"""
    url = f"{API_BASE_URL}/search/problem"
    params = {
        "query": f"tier:{tier_min}..{tier_max}",
        "page": page,
        "sort": "level",  # 난이도순 정렬
        "direction": "asc"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching problems: {e}")
        return None

def fetch_all_problems():
    """모든 난이도의 문제 가져오기"""
    all_problems = []

    # Bronze부터 Gold까지만 가져오기 (1~15)
    # 너무 많으면 Silver~Gold만 (6~15)로 조정 가능
    tier_ranges = [
        (1, 5, "Bronze"),
        (6, 10, "Silver"),
        (11, 15, "Gold"),
    ]

    for tier_min, tier_max, tier_name in tier_ranges:
        print(f"Fetching {tier_name} problems...")
        page = 1

        while page <= 2:  # 각 난이도별 최대 2페이지 (200문제)
            data = fetch_problems_by_tier(tier_min, tier_max, page)

            if not data or "items" not in data:
                break

            problems = data["items"]
            if not problems:
                break

            all_problems.extend(problems)
            print(f"  Page {page}: {len(problems)} problems")

            page += 1

    return all_problems

def generate_html(problems):
    """문제 목록을 HTML로 생성"""

    # 모든 태그 수집
    all_tags = set()
    for problem in problems:
        for tag in problem.get("tags", []):
            all_tags.add(tag["displayNames"][0]["name"])  # 한글 이름

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>백준 문제 목록</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}

        .update-time {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .filters {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .filter-group {{
            margin-bottom: 15px;
        }}

        .filter-group label {{
            font-weight: bold;
            display: block;
            margin-bottom: 8px;
            color: #333;
        }}

        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .filter-btn {{
            padding: 6px 12px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 13px;
        }}

        .filter-btn:hover {{
            border-color: #007bff;
        }}

        .filter-btn.active {{
            background: #007bff;
            color: white;
            border-color: #007bff;
        }}

        .tag-btn {{
            padding: 5px 10px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}

        .tag-btn.active {{
            background: #28a745;
            color: white;
            border-color: #28a745;
        }}

        .search-box {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }}

        .stats {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .problem-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .problem-table th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}

        .problem-table td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }}

        .problem-row {{
            transition: background 0.2s;
            cursor: pointer;
        }}

        .problem-row:hover {{
            background: #f8f9fa;
        }}

        .problem-number {{
            font-weight: bold;
            color: #007bff;
        }}

        .problem-title {{
            color: #333;
        }}

        .tier {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}

        .bronze {{ background: #ad5600; color: white; }}
        .silver {{ background: #435f7a; color: white; }}
        .gold {{ background: #ec9a00; color: white; }}
        .platinum {{ background: #27e2a4; color: white; }}
        .diamond {{ background: #00b4fc; color: white; }}
        .ruby {{ background: #ff0062; color: white; }}

        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}

        .tag {{
            background: #e9ecef;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            color: #495057;
        }}

        .accepted-rate {{
            color: #28a745;
            font-weight: bold;
        }}

        .hidden {{
            display: none !important;
        }}

        .reset-btn {{
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }}

        .reset-btn:hover {{
            background: #c82333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 백준 문제 목록</h1>
        <div class="update-time">마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="filters">
            <div class="filter-group">
                <label>난이도 필터:</label>
                <div class="filter-buttons">
                    <button class="filter-btn" data-tier="all">전체</button>
                    <button class="filter-btn" data-tier="bronze">Bronze</button>
                    <button class="filter-btn" data-tier="silver">Silver</button>
                    <button class="filter-btn" data-tier="gold">Gold</button>
                </div>
            </div>

            <div class="filter-group">
                <label>태그 필터 (복수 선택 가능):</label>
                <div class="filter-buttons" id="tag-filters">
                    <!-- 태그 버튼들이 여기에 동적으로 추가됨 -->
                </div>
            </div>

            <div class="filter-group">
                <label>문제 검색:</label>
                <input type="text" class="search-box" id="search-box" placeholder="문제 번호 또는 제목으로 검색...">
            </div>

            <button class="reset-btn" onclick="resetFilters()">필터 초기화</button>
        </div>

        <div class="stats">
            <div>총 <strong id="total-count">{len(problems)}</strong>개 문제</div>
            <div>표시된 문제: <strong id="visible-count">{len(problems)}</strong>개</div>
        </div>

        <table class="problem-table">
            <thead>
                <tr>
                    <th style="width: 80px;">번호</th>
                    <th style="width: 300px;">제목</th>
                    <th style="width: 120px;">난이도</th>
                    <th>태그</th>
                    <th style="width: 80px;">정답률</th>
                </tr>
            </thead>
            <tbody id="problem-list">
"""

    # 문제 목록 추가
    for problem in problems:
        problem_id = problem["problemId"]
        title = problem["titleKo"]
        level = problem["level"]
        tier_name = TIER_NAMES.get(level, "Unrated")
        tier_class = get_tier_class(level)
        accepted_rate = problem.get("acceptedUserCount", 0) / max(problem.get("submittedUserCount", 1), 1) * 100

        tags = problem.get("tags", [])
        tag_names = [tag["displayNames"][0]["name"] for tag in tags]
        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in tag_names])
        tags_data = ",".join(tag_names)

        html_content += f"""
                <tr class="problem-row" data-tier="{tier_class}" data-tags="{tags_data}" data-search="{problem_id} {title.lower()}" onclick="window.open('https://www.acmicpc.net/problem/{problem_id}', '_blank')">
                    <td class="problem-number">#{problem_id}</td>
                    <td class="problem-title">{title}</td>
                    <td><span class="tier {tier_class}">{tier_name}</span></td>
                    <td><div class="tags">{tags_html}</div></td>
                    <td class="accepted-rate">{accepted_rate:.1f}%</td>
                </tr>
"""

    html_content += """
            </tbody>
        </table>
    </div>

    <script>
        // 태그 목록 생성
        const allTags = new Set();
        document.querySelectorAll('.problem-row').forEach(row => {
            const tags = row.dataset.tags.split(',').filter(t => t);
            tags.forEach(tag => allTags.add(tag));
        });

        const tagFilters = document.getElementById('tag-filters');
        Array.from(allTags).sort().forEach(tag => {
            const btn = document.createElement('button');
            btn.className = 'tag-btn';
            btn.textContent = tag;
            btn.dataset.tag = tag;
            btn.onclick = () => toggleTag(btn);
            tagFilters.appendChild(btn);
        });

        // 필터 상태
        let selectedTier = 'all';
        let selectedTags = new Set();
        let searchText = '';

        // 난이도 필터
        document.querySelectorAll('[data-tier]').forEach(btn => {
            if (btn.classList.contains('filter-btn')) {
                btn.onclick = () => {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    selectedTier = btn.dataset.tier;
                    applyFilters();
                };
            }
        });

        // 태그 필터 (복수 선택)
        function toggleTag(btn) {
            const tag = btn.dataset.tag;
            if (selectedTags.has(tag)) {
                selectedTags.delete(tag);
                btn.classList.remove('active');
            } else {
                selectedTags.add(tag);
                btn.classList.add('active');
            }
            applyFilters();
        }

        // 검색
        document.getElementById('search-box').addEventListener('input', (e) => {
            searchText = e.target.value.toLowerCase();
            applyFilters();
        });

        // 필터 적용
        function applyFilters() {
            let visibleCount = 0;

            document.querySelectorAll('.problem-row').forEach(row => {
                let show = true;

                // 난이도 필터
                if (selectedTier !== 'all' && row.dataset.tier !== selectedTier) {
                    show = false;
                }

                // 태그 필터 (선택된 태그 중 하나라도 포함되어야 함)
                if (selectedTags.size > 0) {
                    const rowTags = row.dataset.tags.split(',');
                    const hasTag = Array.from(selectedTags).some(tag => rowTags.includes(tag));
                    if (!hasTag) show = false;
                }

                // 검색 필터
                if (searchText && !row.dataset.search.includes(searchText)) {
                    show = false;
                }

                row.classList.toggle('hidden', !show);
                if (show) visibleCount++;
            });

            document.getElementById('visible-count').textContent = visibleCount;
        }

        // 필터 초기화
        function resetFilters() {
            selectedTier = 'all';
            selectedTags.clear();
            searchText = '';

            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('search-box').value = '';

            applyFilters();
        }
    </script>
</body>
</html>
"""

    return html_content

def main():
    print("백준 문제 목록을 가져오는 중...")
    problems = fetch_all_problems()

    if not problems:
        print("문제를 가져오는데 실패했습니다.")
        return

    print(f"\n총 {len(problems)}개의 문제를 가져왔습니다.")

    print("HTML 파일 생성 중...")
    html_content = generate_html(problems)

    with open("problem_list.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("[OK] problem_list.html file created!")
    print("\nHow to use:")
    print("1. Open problem_list.html in VS Code")
    print("2. Right-click > 'Open with Live Server' or open in browser")
    print("3. Filter by difficulty and tags, click to open problem on BOJ site")

if __name__ == "__main__":
    main()
