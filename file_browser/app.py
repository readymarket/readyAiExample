from flask import Flask, render_template, request, redirect, url_for
import os
import markdown
import re
from pathlib import Path
from textwrap import dedent

app = Flask(__name__)

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent / 'data'

def parse_website_outline(directory):
    """解析 .website-outline 檔案並返回路徑與描述的字典"""
    outline_path = directory / '.website-outline'
    if not outline_path.exists():
        return {}
    
    outline = {}
    with open(outline_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('#', 1)
            path = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            
            # 將 .html 轉換為 .md
            md_path = path.replace('.html', '.md')
            outline[path] = {
                'md_path': md_path,
                'description': description
            }
    
    return outline

def read_website_outline_think(directory):
    """讀取 .website-outline.think 檔案內容"""
    think_path = directory / '.website-outline.think'
    if not think_path.exists():
        return ""
    
    with open(think_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_subdirectories(directory):
    """獲取目錄下的所有子目錄"""
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and not d.startswith('.')]

def read_file_content(file_path):
    """讀取檔案內容"""
    if not os.path.exists(file_path):
        return ""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_profile(directory):
    """讀取目錄下的 .profile 文件"""
    profile_path = directory / '.profile'
    if not profile_path.exists():
        return ""
    
    return read_file_content(profile_path)

def convert_md_to_html(content):
    """將 Markdown 內容轉換為 HTML"""
    return markdown.markdown(content, extensions=['tables', 'fenced_code'])

@app.route('/')
def index():
    """首頁，顯示所有可用的目錄"""
    subdirs = get_subdirectories(PROJECT_ROOT)
    
    # 為每個子目錄讀取 .profile 文件
    profiles = {}
    for subdir in subdirs:
        profile_content = read_profile(PROJECT_ROOT / subdir)
        if profile_content:
            profiles[subdir] = profile_content
    
    return render_template('index.html', subdirs=subdirs, profiles=profiles)

@app.route('/browse/<path:directory>')
def browse(directory):
    """瀏覽特定目錄"""
    dir_path = PROJECT_ROOT / directory
    
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return redirect(url_for('index'))
    
    # 解析 .website-outline
    outline = parse_website_outline(dir_path)
    
    # 讀取 .website-outline.think 文件
    outline_think_content = read_website_outline_think(dir_path)
    
    # 獲取子目錄
    subdirs = get_subdirectories(dir_path)
    
    # 讀取當前目錄的 .profile 文件
    profile_content = read_profile(dir_path)
    
    # 為每個子目錄讀取 .profile 文件
    profiles = {}
    for subdir in subdirs:
        subdir_profile = read_profile(dir_path / subdir)
        if subdir_profile:
            profiles[subdir] = subdir_profile
    
    return render_template('browse.html', 
                          directory=directory,
                          outline=outline,
                          subdirs=subdirs,
                          profile_content=profile_content,
                          profiles=profiles,
                          outline_think_content=outline_think_content)

@app.route('/view/<path:directory>/<path:file_path>')
def view_file(directory, file_path):
    """查看特定檔案"""
    dir_path = PROJECT_ROOT / directory
    
    # 解析 .website-outline
    outline = parse_website_outline(dir_path)
    
    # 讀取 .website-outline.think 文件
    outline_think_content = read_website_outline_think(dir_path)
    
    # 找到對應的 HTML 路徑
    html_path = None
    for path, info in outline.items():
        if info['md_path'] == f'/{file_path}':
            html_path = path
            break
    
    # 確定檔案路徑
    file_parts = file_path.split('/')
    file_name = file_parts[-1]
    file_dir = '/'.join(file_parts[:-1])
    
    full_dir_path = dir_path / file_dir
    
    # 讀取 Markdown 檔案
    md_file_path = full_dir_path / file_name
    md_content = read_file_content(md_file_path)
    html_content = convert_md_to_html(md_content)
    
    # 讀取參考資料和思路檔案
    reference_file = full_dir_path / f'.{file_name.replace(".md", "")}.reference'
    think_file = full_dir_path / f'.{file_name.replace(".md", "")}.think'
    
    reference_content = read_file_content(reference_file)
    think_content = read_file_content(think_file)
    
    return render_template('view.html',
                          directory=directory,
                          file_path=file_path,
                          html_path=html_path,
                          html_content=html_content,
                          reference_content=reference_content,
                          think_content=think_content,
                          outline_think_content=outline_think_content)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
