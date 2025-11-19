#!/usr/bin/env python3
"""
Convert existing HTML index files to Jekyll format with front matter
"""

import re
from pathlib import Path

# Language configuration
LANG_CONFIG = {
    'index.html': {
        'lang': 'en',
        'lang_name': 'English',
        'home_url': '/',
        'permalink': '/',
        'title': 'Gender Watchdog | Documenting Racialized Sexual Violence at Dongguk University | KWDI Report Analysis',
        'description': "Documentation of racialized sexual violence, institutional cover-ups, and alleged misuse of public funds at Dongguk University and other Korean institutions.",
        'og_image': '/imgs/og-image-en.jpg',
        'site_name': 'Gender Watchdog',
        'nav_home': 'Home',
        'nav_resources': 'Resources',
        'structured_data_file': '/structured-data/index.json',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
    'index-ko.html': {
        'lang': 'ko',
        'lang_name': '한국어',
        'home_url': '/ko/',
        'permalink': '/ko/',
        'title': '젠더와치독 | 동국대/동국대학교/동대(Dongguk) 인종적 성폭력 문제와 대학 내 성폭력 대응 | 성폭력 인식 테스트 비판',
        'description': '동국대학교(동국대/동대/Dongguk)의 인종적 성폭력 문제, 제도적 은폐, 그리고 공공자금 오용 의혹에 관한 문서화.',
        'og_image': '/imgs/og-image-ko.jpg',
        'site_name': '젠더와치독',
        'nav_home': '홈',
        'nav_resources': '자료',
        'structured_data_file': '/structured-data/index-ko.json',
        'google_fonts': 'Noto+Sans+KR:wght@300;400;500;700',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
    'index-ja.html': {
        'lang': 'ja',
        'lang_name': '日本語',
        'home_url': '/ja/',
        'permalink': '/ja/',
        'title': 'ジェンダーウォッチドッグ | 東国大学における人種差別的性暴力と制度的隠蔽の記録',
        'description': '東国大学およびその他の韓国の教育機関における人種差別的性暴力、制度的隠蔽、公的資金の不正使用疑惑の記録。',
        'og_image': '/imgs/og-image-ja.jpg',
        'site_name': 'ジェンダーウォッチドッグ',
        'nav_home': 'ホーム',
        'nav_resources': 'リソース',
        'structured_data_file': '/structured-data/index-ja.json',
        'google_fonts': 'Noto+Sans+JP:wght@300;400;500;700',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
    'index-zh-ch.html': {
        'lang': 'zh-ch',
        'lang_name': '简体中文',
        'home_url': '/zh-ch/',
        'permalink': '/zh-ch/',
        'title': '性别监察犬 | 记录东国大学的种族化性暴力与制度性背叛',
        'description': '记录东国大学及其他韩国机构的种族化性暴力、制度性掩盖和涉嫌滥用公共资金。',
        'og_image': '/imgs/og-image-zh-ch.jpg',
        'site_name': '性别监察犬',
        'nav_home': '主页',
        'nav_resources': '资源',
        'structured_data_file': '/structured-data/index-zh-ch.json',
        'google_fonts': 'Noto+Sans+SC:wght@300;400;500;700',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
    'index-zh-tw.html': {
        'lang': 'zh-tw',
        'lang_name': '繁體中文',
        'home_url': '/zh-tw/',
        'permalink': '/zh-tw/',
        'title': '性別監察犬 | 記錄東國大學的種族化性暴力與制度性背叛',
        'description': '記錄東國大學及其他韓國機構的種族化性暴力、制度性掩蓋和涉嫌濫用公共資金。',
        'og_image': '/imgs/og-image-zh-tw.jpg',
        'site_name': '性別監察犬',
        'nav_home': '首頁',
        'nav_resources': '資源',
        'structured_data_file': '/structured-data/index-zh-tw.json',
        'google_fonts': 'Noto+Sans+TC:wght@300;400;500;700',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
    'index-vn.html': {
        'lang': 'vn',
        'lang_name': 'Tiếng Việt',
        'home_url': '/vn/',
        'permalink': '/vn/',
        'title': 'Gender Watchdog | Ghi lại Bạo lực Tình dục có Yếu tố Phân biệt Chủng tộc tại Đại học Dongguk',
        'description': 'Ghi lại bạo lực tình dục có yếu tố phân biệt chủng tộc, che đậy thể chế và cáo buộc lạm dụng quỹ công tại Đại học Dongguk.',
        'og_image': '/imgs/og-image-vn.jpg',
        'site_name': 'Gender Watchdog',
        'nav_home': 'Trang chủ',
        'nav_resources': 'Tài nguyên',
        'structured_data_file': '/structured-data/index-vn.json',
        'translations': [
            {'lang': 'en', 'url': '/', 'label': 'English'},
            {'lang': 'ko', 'url': '/ko/', 'label': '한국어'},
            {'lang': 'ja', 'url': '/ja/', 'label': '日本語'},
            {'lang': 'zh-ch', 'url': '/zh-ch/', 'label': '简体中文'},
            {'lang': 'zh-tw', 'url': '/zh-tw/', 'label': '繁體中文'},
            {'lang': 'vn', 'url': '/vn/', 'label': 'Tiếng Việt'},
        ]
    },
}

def extract_content(html_path):
    """Extract content between </header> and <footer>"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find content between </header> and <footer>
    match = re.search(r'</header>(.*?)<footer', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def create_front_matter(config):
    """Create YAML front matter from config"""
    front_matter = ['---', 'layout: home']

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

    # Add translations array
    if 'translations' in config:
        front_matter.append('translations:')
        for trans in config['translations']:
            front_matter.append(f'  - lang: "{trans["lang"]}"')
            front_matter.append(f'    url: "{trans["url"]}"')
            front_matter.append(f'    label: "{trans["label"]}"')

    front_matter.append('---')
    return '\n'.join(front_matter)

def convert_file(source_file, config, output_dir='_pages'):
    """Convert HTML file to Jekyll format"""
    source_path = Path(source_file)

    # Extract content
    content = extract_content(source_path)
    if not content:
        print(f"Error: Could not extract content from {source_file}")
        return False

    # Create front matter
    front_matter = create_front_matter(config)

    # Determine output filename based on language
    if config['lang'] == 'en':
        output_filename = 'index.html'
    else:
        output_filename = f"index-{config['lang']}.html"

    # Create output directory if needed
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Write new file
    output_file = output_path / output_filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write('\n\n')
        f.write(content)

    print(f"✓ Converted {source_file} -> {output_file}")
    return True

def main():
    """Convert all index files"""
    print("Converting index files to Jekyll format...")

    success_count = 0
    for source_file, config in LANG_CONFIG.items():
        if Path(source_file).exists():
            if convert_file(source_file, config):
                success_count += 1
        else:
            print(f"Warning: {source_file} not found, skipping")

    print(f"\n✓ Successfully converted {success_count}/{len(LANG_CONFIG)} files")

if __name__ == '__main__':
    main()
