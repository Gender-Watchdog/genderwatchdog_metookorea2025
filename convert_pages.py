#!/usr/bin/env python3
"""
Convert /pages/ directory HTML files to Jekyll format
"""

import re
from pathlib import Path

# Pages configuration
PAGES_CONFIG = {
    'pages/xiaohongshu/xiaohongshu-en.html': {
        'lang': 'en',
        'lang_name': 'English',
        'title': 'Xiaohongshu Viral Posts Collapse Dongguk University\'s Chinese Student Recruitment | GenderWatchdog',
        'description': 'GenderWatchdog\'s exposé goes viral on Xiaohongshu, collapsing Dongguk\'s Chinese student recruitment.',
        'permalink': '/xiaohongshu/',
        'og_image': '/imgs/xiaohongshu/xiaohongshu-viral-impact.jpg',
        'site_name': 'Gender Watchdog',
        'nav_home': 'Home',
        'nav_resources': 'Resources',
        'home_url': '/',
    },
    'pages/xiaohongshu/xiaohongshu.html': {
        'lang': 'ko',
        'lang_name': '한국어',
        'title': '샤오홍슈 바이럴 포스트가 동국대학교 중국 학생 모집 붕괴시켜 | 젠더와치독',
        'description': '젠더와치독의 동국대학교 성폭력 은폐 폭로가 샤오홍슈에서 바이럴.',
        'permalink': '/ko/xiaohongshu/',
        'og_image': '/imgs/xiaohongshu/xiaohongshu-viral-impact.jpg',
        'site_name': '젠더와치독',
        'nav_home': '홈',
        'nav_resources': '자료',
        'home_url': '/ko/',
        'google_fonts': 'Noto+Sans+KR:wght@300;400;500;700',
    },
    'pages/xiaohongshu/xiaohongshu-ja.html': {
        'lang': 'ja',
        'lang_name': '日本語',
        'title': 'Xiaohongshuバイラル投稿が東国大学の中国人学生募集を崩壊させる | ジェンダーウォッチドッグ',
        'description': 'ジェンダーウォッチドッグの東国大学性暴力隠蔽の暴露がXiaohongshuでバイラル。',
        'permalink': '/ja/xiaohongshu/',
        'og_image': '/imgs/xiaohongshu/xiaohongshu-viral-impact.jpg',
        'site_name': 'ジェンダーウォッチドッグ',
        'nav_home': 'ホーム',
        'nav_resources': 'リソース',
        'home_url': '/ja/',
        'google_fonts': 'Noto+Sans+JP:wght@300;400;500;700',
    },
    'pages/xiaohongshu/xiaohongshu-zh-tw.html': {
        'lang': 'zh-tw',
        'lang_name': '繁體中文',
        'title': 'Xiaohongshu病毒式傳播使東國大學中國學生招募崩潰 | 性別監察犬',
        'description': '性別監察犬揭露東國大學性暴力掩蓋在Xiaohongshu上病毒式傳播。',
        'permalink': '/zh-tw/xiaohongshu/',
        'og_image': '/imgs/xiaohongshu/xiaohongshu-viral-impact.jpg',
        'site_name': '性別監察犬',
        'nav_home': '首頁',
        'nav_resources': '資源',
        'home_url': '/zh-tw/',
        'google_fonts': 'Noto+Sans+TC:wght@300;400;500;700',
    },
    'pages/xiaohongshu/xiahongshu-zh-cn.html': {
        'lang': 'zh-ch',
        'lang_name': '简体中文',
        'title': 'Xiaohongshu病毒式传播使东国大学中国学生招募崩溃 | 性别监察犬',
        'description': '性别监察犬揭露东国大学性暴力掩盖在Xiaohongshu上病毒式传播。',
        'permalink': '/zh-ch/xiaohongshu/',
        'og_image': '/imgs/xiaohongshu/xiaohongshu-viral-impact.jpg',
        'site_name': '性别监察犬',
        'nav_home': '主页',
        'nav_resources': '资源',
        'home_url': '/zh-ch/',
        'google_fonts': 'Noto+Sans+SC:wght@300;400;500;700',
    },
    'pages/new-administration/election-issue.html': {
        'lang': 'en',
        'lang_name': 'English',
        'title': 'New Government & Dongguk Scandal: In-Depth Analysis | Gender Watchdog',
        'description': 'Analysis of how the new government will address the Dongguk University sexual violence scandal.',
        'permalink': '/new-administration/election-issue/',
        'og_image': '/imgs/og-image-en.jpg',
        'site_name': 'Gender Watchdog',
        'nav_home': 'Home',
        'nav_resources': 'Resources',
        'home_url': '/',
    },
    'pages/new-administration/election-issue-ko.html': {
        'lang': 'ko',
        'lang_name': '한국어',
        'title': '새 정부와 동국대 스캔들: 심층 분석 | 젠더와치독',
        'description': '새 정부가 동국대학교 성폭력 스캔들을 어떻게 다룰 것인가에 대한 분석.',
        'permalink': '/ko/new-administration/election-issue/',
        'og_image': '/imgs/og-image-ko.jpg',
        'site_name': '젠더와치독',
        'nav_home': '홈',
        'nav_resources': '자료',
        'home_url': '/ko/',
        'google_fonts': 'Noto+Sans+KR:wght@300;400;500;700',
        'structured_data_file': '/structured-data/election-issue-ko.json',
    },
    'pages/new-administration/election-issue-ja.html': {
        'lang': 'ja',
        'lang_name': '日本語',
        'title': '新政府と東国大学スキャンダル: 詳細分析 | ジェンダーウォッチドッグ',
        'description': '新政府が東国大学性暴力スキャンダルにどう対処するかの分析。',
        'permalink': '/ja/new-administration/election-issue/',
        'og_image': '/imgs/og-image-ja.jpg',
        'site_name': 'ジェンダーウォッチドッグ',
        'nav_home': 'ホーム',
        'nav_resources': 'リソース',
        'home_url': '/ja/',
        'google_fonts': 'Noto+Sans+JP:wght@300;400;500;700',
    },
    'pages/new-administration/election-issue-zh-tw.html': {
        'lang': 'zh-tw',
        'lang_name': '繁體中文',
        'title': '新政府與東國大學醜聞: 深度分析 | 性別監察犬',
        'description': '新政府如何應對東國大學性暴力醜聞的分析。',
        'permalink': '/zh-tw/new-administration/election-issue/',
        'og_image': '/imgs/og-image-zh-tw.jpg',
        'site_name': '性別監察犬',
        'nav_home': '首頁',
        'nav_resources': '資源',
        'home_url': '/zh-tw/',
        'google_fonts': 'Noto+Sans+TC:wght@300;400;500;700',
    },
    'pages/new-administration/election-issu-zh-cn.html': {
        'lang': 'zh-ch',
        'lang_name': '简体中文',
        'title': '新政府与东国大学丑闻: 深度分析 | 性别监察犬',
        'description': '新政府如何应对东国大学性暴力丑闻的分析。',
        'permalink': '/zh-ch/new-administration/election-issue/',
        'og_image': '/imgs/og-image-zh-ch.jpg',
        'site_name': '性别监察犬',
        'nav_home': '主页',
        'nav_resources': '资源',
        'home_url': '/zh-ch/',
        'google_fonts': 'Noto+Sans+SC:wght@300;400;500;700',
    },
    'pages/state-sex-trafficking/state-sex-traffic-en.html': {
        'lang': 'en',
        'lang_name': 'English',
        'title': 'State-Sanctioned Sex Trafficking Analysis | Gender Watchdog',
        'description': 'Analysis of Korea\'s state-sanctioned sex trafficking system targeting foreign students.',
        'permalink': '/state-sex-trafficking/',
        'og_image': '/imgs/og-image-en.jpg',
        'site_name': 'Gender Watchdog',
        'nav_home': 'Home',
        'nav_resources': 'Resources',
        'home_url': '/',
    },
}

def extract_content(html_path):
    """Extract content between </header> and <footer> or end of body"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to find content between </header> and <footer>
    match = re.search(r'</header>(.*?)(?:<footer|</body>|</html>)', content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no header, try to extract body content
    match = re.search(r'<body>(.*?)(?:</body>|</html>)', content, re.DOTALL)
    if match:
        body_content = match.group(1).strip()
        # Remove header if present
        body_content = re.sub(r'<header.*?</header>', '', body_content, flags=re.DOTALL)
        # Remove footer if present
        body_content = re.sub(r'<footer.*?</footer>', '', body_content, flags=re.DOTALL)
        return body_content.strip()

    return None

def create_front_matter(config):
    """Create YAML front matter from config"""
    front_matter = ['---', 'layout: page']

    # Add basic fields
    for key in ['lang', 'lang_name', 'title', 'description', 'permalink']:
        if key in config:
            # Escape quotes in values
            value = str(config[key]).replace('"', '\\"')
            front_matter.append(f'{key}: "{value}"')

    # Add other fields
    for key in ['og_image', 'site_name', 'nav_home', 'nav_resources', 'home_url', 'structured_data_file', 'google_fonts']:
        if key in config:
            value = str(config[key]).replace('"', '\\"')
            front_matter.append(f'{key}: "{value}"')

    front_matter.append('---')
    return '\n'.join(front_matter)

def convert_file(source_file, config):
    """Convert HTML file to Jekyll format"""
    source_path = Path(source_file)

    if not source_path.exists():
        print(f"Warning: {source_file} not found, skipping")
        return False

    # Extract content
    content = extract_content(source_path)
    if not content:
        print(f"Error: Could not extract content from {source_file}")
        return False

    # Create front matter
    front_matter = create_front_matter(config)

    # Determine output path - keep in same directory structure but under _pages
    relative_path = source_path.relative_to('pages')
    output_file = Path('_pages') / relative_path

    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write new file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write('\n\n')
        f.write(content)

    print(f"✓ Converted {source_file} -> {output_file}")
    return True

def main():
    """Convert all pages"""
    print("Converting /pages/ directory to Jekyll format...")

    success_count = 0
    for source_file, config in PAGES_CONFIG.items():
        if convert_file(source_file, config):
            success_count += 1

    print(f"\n✓ Successfully converted {success_count}/{len(PAGES_CONFIG)} files")

if __name__ == '__main__':
    main()
