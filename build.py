#!/usr/bin/env python3
"""
Static Site Builder for Gagan Bhusal's Portfolio
Combines modular files from:
  - sections/bio.html
  - sections/research-interests.html
  - sections/experience.html
  - sections/education.html
  - sections/skills.html
  - projects/*.html
into the standalone root index.html for GitHub Pages.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ORDER = [
    'unitree-go2',
    'unitree-g1',
    'alphazero',
    'ghost-net',
    'satellite-sr',
    'pinn',
    'stem-quadruped',
    'transformer'
]

def parse_project_file(filepath, pid):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract title
    title_m = re.search(r'<h1 class="modal-title">\s*(.*?)\s*</h1>', html, re.DOTALL)
    title = title_m.group(1).strip() if title_m else pid

    # Extract badge & status
    badge_m = re.search(r'<span class="modal-badge">\s*(.*?)\s*</span>', html, re.DOTALL)
    badge = badge_m.group(1).strip() if badge_m else ''

    status_m = re.search(r'<span class="modal-date">\s*(.*?)\s*</span>', html, re.DOTALL)
    status = status_m.group(1).strip() if status_m else ''

    # Extract tags
    tags = re.findall(r'<span class="port-tag[^"]*">\s*(.*?)\s*</span>', html)

    # Extract links
    links = []
    link_matches = re.findall(r'<a\s+href="([^"]+)"\s+class="modal-action-link"([^>]*)>\s*(.*?)\s*</a>', html)
    for url, extra, text in link_matches:
        if 'Standalone Page' in text:
            continue
        is_ext = 'target="_blank"' in extra
        links.append({'text': text.strip(), 'url': url.strip(), 'external': is_ext})

    # Extract dynamic media from .modal-media-box
    media_m = re.search(r'<div class="modal-media-box">\s*(.*?)\s*</div>', html, re.DOTALL)
    if media_m:
        raw_media = media_m.group(1).strip()
        # Adjust relative paths from project subfolder (../assets/) to root (assets/)
        clean_modal_media = raw_media.replace('../assets/', 'assets/')
    else:
        clean_modal_media = f'<img src="assets/projects/{pid}.jpg" alt="{title}" style="width: 100%; max-height: 440px; object-fit: cover; display: block;">'

    # Build card media snippet from the project media
    if '<video' in clean_modal_media:
        v_src_m = re.search(r'<source\s+src="([^"]+)"', clean_modal_media)
        v_poster_m = re.search(r'poster="([^"]+)"', clean_modal_media)
        v_src = v_src_m.group(1) if v_src_m else f'assets/projects/{pid}.mp4'
        v_poster = v_poster_m.group(1) if v_poster_m else f'assets/projects/{pid}.jpg'
        card_media_html = f'''<video autoplay loop muted playsinline poster="{v_poster}" preload="auto">
                                <source src="{v_src}" type="video/mp4">
                            </video>'''
    else:
        img_src_m = re.search(r'<img\s+src="([^"]+)"', clean_modal_media)
        img_alt_m = re.search(r'alt="([^"]*)"', clean_modal_media)
        img_src = img_src_m.group(1) if img_src_m else f'assets/projects/{pid}.jpg'
        img_alt = img_alt_m.group(1) if img_alt_m else title
        card_media_html = f'<img src="{img_src}" alt="{img_alt}" loading="lazy">'

    # Wrap clean modal media
    modal_media_box = f'<div class="modal-media-box">\n                        {clean_modal_media}\n                    </div>'

    # Extract card summary block
    summary_m = re.search(r'<div class="project-card-summary"[^>]*data-badge-label="([^"]*)"[^>]*data-has-dot="([^"]*)"[^>]*data-is-featured="([^"]*)"[^>]*data-date="([^"]*)"[^>]*>(.*?)</div>\s*<!-- CARD_SUMMARY_END -->', html, re.DOTALL)
    
    if summary_m:
        badge_label = summary_m.group(1)
        has_dot = summary_m.group(2).lower() == 'true'
        is_featured = summary_m.group(3).lower() == 'true'
        date = summary_m.group(4)
        inner_summary = summary_m.group(5)
        
        desc_m = re.search(r'<p class="port-card-desc">\s*(.*?)\s*</p>', inner_summary, re.DOTALL)
        card_desc = desc_m.group(1).strip() if desc_m else ''

        slot_m = re.search(r'<div class="card-footer-slot">\s*(.*?)\s*</div>', inner_summary, re.DOTALL)
        footer_slot = slot_m.group(1).strip() if slot_m else ''
    else:
        badge_label = ''
        has_dot = False
        is_featured = False
        date = '2026'
        card_desc = ''
        footer_slot = ''

    # Extract Overview
    overview_m = re.search(r'<h4 class="modal-section-title">Project Overview &amp; Motivation</h4>\s*<p class="modal-body-text">\s*(.*?)\s*</p>', html, re.DOTALL)
    overview = overview_m.group(1).strip() if overview_m else ''

    # Extract Architecture
    arch_m = re.search(r'<h4 class="modal-section-title">System Architecture &amp; Methodology</h4>\s*<div class="modal-body-text">\s*(.*?)\s*</div>', html, re.DOTALL)
    architecture = arch_m.group(1).strip() if arch_m else ''

    # Extract Demos
    demos = []
    demo_blocks = re.findall(r'<div class="modal-section">\s*<h4 class="modal-section-title">([^<]+)</h4>\s*<p class="modal-body-text">\s*(.*?)\s*</p>', html, re.DOTALL)
    for d_title, d_desc in demo_blocks:
        if 'Overview' not in d_title and 'Architecture' not in d_title and 'Technical' not in d_title:
            demos.append({
                'title': d_title.strip(),
                'desc': d_desc.strip(),
                'metrics': []
            })

    # Extract Specs
    specs = []
    specs_m = re.search(r'<h4 class="modal-section-title">Technical Specifications &amp; Stack</h4>\s*<ul class="modal-bullets">\s*(.*?)\s*</ul>', html, re.DOTALL)
    if specs_m:
        specs = [s.strip() for s in re.findall(r'<li>\s*(.*?)\s*</li>', specs_m.group(1))]

    return {
        'pid': pid,
        'title': title,
        'status': status,
        'badge': badge,
        'date': date,
        'tags': tags,
        'links': links,
        'card_desc': card_desc,
        'badge_label': badge_label,
        'has_dot': has_dot,
        'is_featured': is_featured,
        'footer_slot': footer_slot,
        'card_media_html': card_media_html,
        'modal_media_box': modal_media_box,
        'overview': overview,
        'architecture': architecture,
        'demos': demos,
        'specs': specs
    }

def generate_card_html(p):
    pid = p['pid']
    featured_class = ' port-card-featured' if p['is_featured'] else ''
    dot_html = '<span class="port-media-dot"></span>' if p['has_dot'] else ''
    badge_html = f'<span class="port-media-badge">{dot_html}{p["badge_label"]}</span>' if p['badge_label'] else ''

    card_tags = []
    for t in p['tags'][:6]:
        cls = 'port-tag port-tag-status' if 'In Progress' in t else 'port-tag'
        card_tags.append(f'                            <span class="{cls}">{t}</span>')
    tags_html = '\n'.join(card_tags)

    footer_row = f'''                        <div class="port-card-footer-row">
                            {p['footer_slot']}
                        </div>''' if p['footer_slot'] else ''

    card = f'''                <!-- {p["title"]} -->
                <div class="port-card{featured_class}" data-project-id="{pid}">
                    <div class="port-card-top">
                        <div class="port-card-header">
                            <h3 class="port-card-title">
                                {p["title"]}
                            </h3>
                            <span class="port-card-date">{p["date"]}</span>
                        </div>
                        <div class="port-card-media-box">
                            {p['card_media_html']}
                            {badge_html}
                        </div>
                        <p class="port-card-desc">
                            {p["card_desc"]}
                        </p>
                    </div>
                    <div>
                        <div class="port-card-tags">
{tags_html}
                        </div>
{footer_row}
                    </div>
                </div>'''
    return card

def build():
    print("Building standalone portfolio...")
    with open(os.path.join(BASE_DIR, 'template.html'), 'r', encoding='utf-8') as f:
        template = f.read()

    # Read sections
    def read_section(filename):
        path = os.path.join(BASE_DIR, 'sections', filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as sf:
                return sf.read().strip()
        return ''

    bio_html = read_section('bio.html')
    interests_html = read_section('research-interests.html')
    exp_html = read_section('experience.html')
    edu_html = read_section('education.html')
    skills_html = read_section('skills.html')

    # Inject research interests into bio if placeholder is present
    if '{{RESEARCH_INTERESTS}}' in bio_html:
        bio_html = bio_html.replace('{{RESEARCH_INTERESTS}}', interests_html)

    # Read projects
    projects_list = []
    projects_data_dict = {}
    cards_html_list = []

    for pid in PROJECT_ORDER:
        p_path = os.path.join(BASE_DIR, 'projects', f'{pid}.html')
        if os.path.exists(p_path):
            p = parse_project_file(p_path, pid)
            projects_list.append(p)
            cards_html_list.append(generate_card_html(p))

            projects_data_dict[pid] = {
                'title': p['title'],
                'status': p['status'],
                'badge': p['badge'],
                'date': p['date'],
                'tags': p['tags'],
                'links': p['links'],
                'mediaHtml': p['modal_media_box'],
                'overview': p['overview'],
                'architecture': p['architecture'],
                'demos': p['demos'],
                'specs': p['specs']
            }

    grid_html = '\n\n'.join(cards_html_list)
    projects_json = json.dumps(projects_data_dict, indent=12)

    # Replace template placeholders
    output = template.replace('{{BIO}}', bio_html)
    output = output.replace('{{RESEARCH_INTERESTS}}', interests_html)
    output = output.replace('{{PROJECTS_GRID}}', grid_html)
    output = output.replace('{{EXPERIENCE}}', exp_html)
    output = output.replace('{{EDUCATION}}', edu_html)
    output = output.replace('{{SKILLS}}', skills_html)
    output = output.replace('{{PROJECTS_DATA_JSON}}', projects_json)

    out_path = os.path.join(BASE_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(output)

    print(f"Successfully generated {out_path} ({len(output)} bytes)")

if __name__ == '__main__':
    build()
