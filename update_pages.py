import os
import re

# List of files to update
files = [
    "/home/nginx/Documents/2_GenderWatchdog/genderwatchdog-home/_pages/index-ko.html",
    "/home/nginx/Documents/2_GenderWatchdog/genderwatchdog-home/_pages/index-ja.html",
    "/home/nginx/Documents/2_GenderWatchdog/genderwatchdog-home/_pages/index-vn.html",
    "/home/nginx/Documents/2_GenderWatchdog/genderwatchdog-home/_pages/index-zh-ch.html",
    "/home/nginx/Documents/2_GenderWatchdog/genderwatchdog-home/_pages/index-zh-tw.html"
]

# HTML Blocks to Insert
global_fraud_alert = """    <!-- Global Fraud Alert: 3 Confirmed False Partnerships -->
    <section class="container my-4">
        <div class="alert alert-danger shadow-lg p-4" role="alert" style="font-size:1.08rem;">
            <div class="d-flex align-items-center mb-2">
                <i class="bi bi-globe-americas fs-3 me-3"></i>
                <div>
                    <strong>Global Fraud Alert: 3 Confirmed False Partnerships Expose Dongguk University's "House of Cards"</strong> <span class="badge bg-dark ms-2">Dec 23, 2025</span>
                </div>
            </div>
            <div class="mb-2">
                <strong>This is a critical turning point.</strong> The confirmation of <strong>3 false or misrepresented partnerships</strong> (UBC, University of Southampton, and one Canadian university requesting anonymity) across <strong>2 continents</strong> transforms what could have been "isolated administrative errors" into a <strong>global pattern of systemic fraud</strong>.
            </div>
            <div class="mb-2">
                For over 260 days, Dongguk University has remained silent while we exposed that their "Global Network" is built on a foundation of lies. Our investigation reveals that <strong>40% of claimed Canadian partnerships are false</strong>.
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <img src="imgs/foi-reqeusts-europe/u-southampton-foi-response.png" class="img-fluid rounded shadow-sm mb-2" alt="University of Southampton FOI Response">
                    <small class="text-muted d-block">University of Southampton FOI Response: No partnership exists.</small>
                </div>
                <div class="col-md-6">
                    <img src="imgs/foi-ubc-oipc-intervention/ubc-foi-response-12182025.png" class="img-fluid rounded shadow-sm mb-2" alt="UBC FOI Response">
                    <small class="text-muted d-block">UBC FOI Response: No active institutional agreement exists.</small>
                </div>
            </div>
            <a href="https://blog.genderwatchdog.org/global-fraud-alert-3-confirmed-false-partnerships-expose-dongguk-universitys-house-of-cards/" class="btn btn-danger fw-bold">
                <i class="bi bi-file-earmark-text me-1"></i> Read Full Global Fraud Alert
            </a>
        </div>
    </section>
"""

professor_f_alert = """    <!-- Professor F Sexual Violence Case Alert -->
    <section class="container my-4">
        <div class="alert alert-dark shadow-lg p-4" role="alert" style="font-size:1.08rem;">
            <div class="d-flex align-items-center mb-2">
                <i class="bi bi-person-x-fill fs-3 me-3"></i>
                <div>
                    <strong>New Sexual Violence Case: "Your Voice is Sex-Appealing" – Professor F's Abuse & Institutional Silence</strong> <span class="badge bg-danger ms-2">Dec 3, 2025</span>
                </div>
            </div>
            <div class="mb-2">
                Just as international partners are beginning to question Dongguk University's safety record, a new sexual violence scandal has erupted. <strong>Professor F</strong> (Dept. of Cultural Heritage) has been accused of repeated sexual harassment, including touching students' thighs and making comments like <strong>"Your voice is sex-appealing."</strong>
            </div>
            <div class="mb-2">
                <strong>The Timeline of Silence:</strong> Despite the university's own Human Rights Center confirming the facts in June 2025, the Board of Directors failed to convene for <strong>nearly four months</strong> to discuss disciplinary action, allowing the professor to remain in his position through the fall semester.
            </div>
            <div class="mb-3">
                <span class="text-danger fw-bold">This mirrors the 220+ days of silence regarding falsified partnerships.</span> Whether it is fraud or sexual violence, the institution's default response is silence and delay.
            </div>
            <a href="https://blog.genderwatchdog.org/new-sexual-violence-case-at-dongguk-university-professor-f-abuse-and-institutional-silence/" class="btn btn-danger fw-bold">
                <i class="bi bi-file-earmark-text me-1"></i> Read Full Professor F Case Analysis
            </a>
        </div>
    </section>
"""

sex_trafficking_alert = """    <!-- State-Sanctioned Sex Trafficking Alert -->
    <section class="container my-4">
        <div class="alert alert-dark shadow-lg p-4" role="alert" style="font-size:1.08rem;">
            <div class="d-flex align-items-center mb-2">
                <i class="bi bi-shield-exclamation fs-3 me-3"></i>
                <div>
                    <strong>CRITICAL ANALYSIS: Korea's State-Sanctioned Sex Trafficking System</strong> <span class="badge bg-danger ms-2">Targeting Foreign Students Through Racism & Defamation Laws</span>
                </div>
            </div>
            <div class="mb-2">
                <strong>Korea ranked 5th worst globally for racism</strong>, creating the foundation for systematic sexual violence against foreign students. Our comprehensive analysis reveals how Korea uses <b>Hallyu cultural appeal to lure foreign women</b> into universities where they face racialized sexual violence, then weaponizes defamation laws to criminalize truthful victim testimony.
            </div>
            <div class="mb-2">
                <b>The UN definition of human trafficking applies directly to Korea's educational system:</b> recruitment through cultural deception, fraudulent partnerships, and exploitation for profit. With 61.5% of female arts students experiencing sexual violence (KWDI data), foreign women face additional vulnerabilities through visa dependency, language barriers, and racial sexual objectification.
            </div>
            <div class="mb-3">
                <span class="text-danger fw-bold">Korea's defamation laws create a triple threat:</span> Truth is not a defense, foreign victims must prove "public interest" in a racist society, and speaking about sexual violence becomes criminally prosecutable. This mirrors historical comfort women trafficking systems but uses modern cultural soft power as the recruitment mechanism.
            </div>
            <a href="/state-sex-trafficking/" class="btn btn-danger fw-bold">
                <i class="bi bi-file-earmark-text me-1"></i> Read Full State-Sanctioned Sex Trafficking Analysis
            </a>
        </div>
    </section>
"""

# Patterns to identify sections in different languages
lee_admin_patterns = [
    r'<!-- 정부 책임 위기 경고 -->',
    r'<!-- 政府責任危機警告 -->',
    r'<!-- Cảnh báo Khủng hoảng Trách nhiệm Chính phủ -->',
    r'<!-- 政府问责危机警告 -->',
    r'<!-- 政府問責危機警告 -->'
]

sidus_patterns = [
    r'<!-- 시더스 법적 위협: 피해자 협박 전술 긴급 알림 -->',
    r'<!-- シーダス法的脅迫：被害者脅迫戦術アラート -->',
    r'<!-- Sidus Legal Threat: Intimidation Tactics Alert -->',
    r'<!-- 突发：希德斯法律威胁警报 -->',
    r'<!-- 突發：希德斯法律威脅警報 -->'
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Processing {os.path.basename(file_path)}...")

    # 1. Insert 'Global Fraud Alert' Block
    xiaohongshu_match = re.search(r'(<!-- .*Xiaohongshu.* -->)', content)
    if xiaohongshu_match:
        xiaohongshu_start_idx = xiaohongshu_match.start()
        content = content[:xiaohongshu_start_idx] + global_fraud_alert + "\n" + content[xiaohongshu_start_idx:]
    else:
        print(f"  Warning: Xiaohongshu section not found.")

    # 2. Update Xiaohongshu Section Styles
    # Find the section again (indices shifted)
    xiaohongshu_match = re.search(r'(<!-- .*Xiaohongshu.* -->)', content)
    if xiaohongshu_match:
        start_pos = xiaohongshu_match.end()
        
        # Find the end of this section to limit replacements
        section_end_match = re.search(r'</section>', content[start_pos:])
        if section_end_match:
            section_end_pos = start_pos + section_end_match.end()
            section_content = content[start_pos:section_end_pos]
            
            # Replace alert-info -> alert-danger
            section_content = section_content.replace('alert-info', 'alert-danger')
            # Replace text-primary -> text-dark
            section_content = section_content.replace('text-primary', 'text-dark')
            # Replace btn-outline-primary -> btn-outline-danger
            section_content = section_content.replace('btn-outline-primary', 'btn-outline-danger')
            
            content = content[:start_pos] + section_content + content[section_end_pos:]

    # 3. Insert 'Professor F' Block
    # Insert before Lee Admin section
    lee_match = None
    for pattern in lee_admin_patterns:
        lee_match = re.search(pattern, content)
        if lee_match:
            break
            
    if lee_match:
        lee_start_idx = lee_match.start()
        content = content[:lee_start_idx] + professor_f_alert + "\n" + content[lee_start_idx:]
    else:
        print(f"  Warning: Lee Admin section not found.")

    # 4. Update Lee Administration Section Styles
    # Find Lee Admin section again
    for pattern in lee_admin_patterns:
        lee_match = re.search(pattern, content)
        if lee_match:
            break
            
    if lee_match:
        start_pos = lee_match.end()
        # Find next alert-danger and replace with alert-dark
        alert_match = re.search(r'alert-danger', content[start_pos:])
        if alert_match:
            abs_start = start_pos + alert_match.start()
            abs_end = start_pos + alert_match.end()
            content = content[:abs_start] + 'alert-dark' + content[abs_end:]

    # 5. Insert 'Sex Trafficking' Block
    # Insert before Sidus section
    sidus_match = None
    for pattern in sidus_patterns:
        sidus_match = re.search(pattern, content)
        if sidus_match:
            break
            
    if sidus_match:
        sidus_start_idx = sidus_match.start()
        content = content[:sidus_start_idx] + sex_trafficking_alert + "\n" + content[sidus_start_idx:]
    else:
        print(f"  Warning: Sidus section not found.")

    # 6. Update Sidus Section Styles
    # Find Sidus section again
    for pattern in sidus_patterns:
        sidus_match = re.search(pattern, content)
        if sidus_match:
            break
            
    if sidus_match:
        start_pos = sidus_match.end()
        # Find next alert-danger and replace with alert-dark
        alert_match = re.search(r'alert-danger', content[start_pos:])
        if alert_match:
            abs_start = start_pos + alert_match.start()
            abs_end = start_pos + alert_match.end()
            content = content[:abs_start] + 'alert-dark' + content[abs_end:]

    # 7. Update 'Falsified International Partnerships' Link
    new_link = "https://blog.genderwatchdog.org/global-fraud-alert-3-confirmed-false-partnerships-expose-dongguk-universitys-house-of-cards/"
    content = re.sub(r'href="[^"]*dongguk-universitys-false-partnership-claims[^"]*"', f'href="{new_link}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Successfully updated {os.path.basename(file_path)}")

print("All files processed.")
