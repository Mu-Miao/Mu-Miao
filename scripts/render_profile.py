"""Render blog-themed profile graphics from public GitHub data."""
from collections import Counter
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
USER = 'Mu-Miao'
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
PALETTES = {
    'dark': dict(bg='#060608', panel='#111114', fg='#f5f5f7', muted='#a0a0ab', line='#323238', pink='#f472b6', dots='#6f6f76'),
    'light': dict(bg='#e8e8ec', panel='#f7f7fa', fg='#1d1d1f', muted='#64646e', line='#c8c8d0', pink='#db2777', dots='#9a9aa2'),
}

def api(endpoint, paginate=False):
    args = ['gh', 'api', endpoint]
    if paginate:
        args += ['--paginate', '--slurp']
    result = json.loads(subprocess.check_output(args, text=True))
    return [item for page in result for item in page] if paginate else result

def collect():
    user = api(f'users/{USER}')
    repos = api(f'users/{USER}/repos?type=owner&per_page=100', paginate=True)
    repos = [r for r in repos if not r['private'] and r['owner']['login'].lower() == USER.lower()]
    originals = [r for r in repos if not r['fork'] and r['name'].lower() != USER.lower()]
    languages = Counter()
    for repo in originals:
        languages.update(api(f"repos/{USER}/{repo['name']}/languages"))
    return dict(updated=datetime.now(timezone.utc).strftime('%Y-%m-%d'), source='GitHub REST API; public owned repositories only', public_repos=len(repos), original_projects=len(originals), stars=sum(r['stargazers_count'] for r in originals), followers=user['followers'], projects=sorted(r['name'] for r in originals), languages_bytes=dict(languages.most_common()))

def text(x, y, value, size=20, fill='currentColor', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'

def svg(name, theme, width, height, title, body, defs='', styles=''):
    p = PALETTES[theme]
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title><defs>{defs}</defs>
<style>text{{font-family:{FONT}}}{styles}</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="24" fill="{p['bg']}" stroke="{p['line']}"/>{body}</svg>'''
    (ASSETS / f'{name}-{theme}.svg').write_text(content)

def header(theme):
    p = PALETTES[theme]
    dots = []
    for row in range(26):
        for col in range(85):
            x = col * 14 + 12
            y = row * 14 + 17 + math.sin(col * .12 + row * .08) * 13
            opacity = .14 + .25 * (math.sin(col * .085 + row * .2) + 1) / 2
            r = 1.5 + 1.5 * (math.sin(col * .1 - row * .17) + 1) / 2
            if (col + row) % 3 == 0:
                dots.append(f'<path d="M{x} {y-r:.2f}l{r:.2f} {r*2:.2f}h{-r*2:.2f}z" opacity="{opacity:.2f}"/>')
            elif (col + row) % 3 == 1:
                dots.append(f'<rect x="{x-r:.2f}" y="{y-r:.2f}" width="{r*2:.2f}" height="{r*2:.2f}" opacity="{opacity:.2f}"/>')
            else:
                dots.append(f'<circle cx="{x}" cy="{y:.2f}" r="{r:.2f}" opacity="{opacity:.2f}"/>')
    defs = f'''<clipPath id="round"><rect width="1200" height="400" rx="24"/></clipPath>
<radialGradient id="scrim"><stop stop-color="{p['bg']}" stop-opacity=".94"/><stop offset="1" stop-color="{p['bg']}" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity=".025"/></linearGradient>
<linearGradient id="beam"><stop stop-color="{p['pink']}" stop-opacity="0"/><stop offset=".5" stop-color="{p['pink']}" stop-opacity=".18"/><stop offset="1" stop-color="{p['pink']}" stop-opacity="0"/></linearGradient>'''
    styles = '.beam{animation:sweep 11s ease-in-out infinite}.spark{animation:breathe 4s ease-in-out infinite}.spark2{animation-delay:2s}@keyframes sweep{0%,100%{transform:translateX(-380px);opacity:0}15%,75%{opacity:1}85%{transform:translateX(1500px);opacity:0}}@keyframes breathe{0%,100%{opacity:.3}50%{opacity:1}}@media(prefers-reduced-motion:reduce){.beam,.spark{animation:none}.beam{opacity:0}}'
    body = f'''<g clip-path="url(#round)"><g fill="{p['dots']}">{''.join(dots)}</g>
{text(600,260,'MASHUTABA',177,p['bg'],800,'text-anchor="middle" letter-spacing="-12" stroke="'+p['dots']+'" stroke-opacity=".18"')}
<rect width="1200" height="400" fill="url(#scrim)"/><rect class="beam" x="-220" width="160" height="400" fill="url(#beam)"/>
<rect x="44" y="26" width="1112" height="46" rx="23" fill="url(#glass)" stroke="{p['line']}"/>
<path d="M74 39v20m-9-15 18 10m-18 0 18-10" stroke="{p['pink']}" stroke-width="4" stroke-linecap="round"/>
{text(98,55,'MASHUTABA',16,p['fg'],600,'letter-spacing="2.2"')}
{text(1131,55,'CODE / NOTES / EXPERIMENTS',13,p['muted'],400,'text-anchor="end" letter-spacing="1.8"')}
{text(600,141,'BUILD. DEBUG. WRITE.',15,p['pink'],500,'text-anchor="middle" letter-spacing="4"')}
{text(600,216,'把复杂的事，慢慢想明白',53,p['fg'],650,'text-anchor="middle" letter-spacing="-1.5"')}
{text(600,260,'写代码，也写那些无法被编译的部分',22,p['muted'],400,'text-anchor="middle"')}
<rect x="490" y="303" width="220" height="43" rx="22" fill="{p['fg']}"/>
{text(600,331,'PROJECTS  /  FIELD NOTES',12,p['bg'],600,'text-anchor="middle" letter-spacing="1.1"')}
<g class="spark" stroke="{p['pink']}" stroke-width="1.4"><path d="M197 165h20m-10-10v20M1007 279h18m-9-9v18"/><rect x="965" y="128" width="8" height="8" transform="rotate(45 969 132)"/></g>
<g class="spark spark2" fill="{p['pink']}"><circle cx="252" cy="298" r="2"/><circle cx="1018" cy="199" r="2"/><circle cx="851" cy="312" r="2"/></g></g>'''
    svg('hero',theme,1200,400,'把复杂的事，慢慢想明白 · 写代码，也写那些无法被编译的部分',body,defs,styles)

def card_base(p, title, subtitle):
    return f'''<rect x="20" y="20" width="540" height="260" rx="18" fill="{p['panel']}"/><path d="M36 64H544" stroke="{p['line']}"/><circle cx="39" cy="41" r="4" fill="{p['pink']}"/>{text(53,47,title,19,p['fg'],600)}{text(544,46,subtitle,11,p['muted'],400,'text-anchor="end" letter-spacing="1"')}'''

def statistics(theme, data):
    p=PALETTES[theme]
    body=card_base(p,'公开足迹','PUBLIC SIGNALS')
    for x,y,value,label in [(40,112,data['public_repos'],'公开仓库'),(305,112,data['original_projects'],'原创项目'),(40,214,data['stars'],'项目 Stars'),(305,214,data['followers'],'关注者')]:
        body+=text(x,y,value,43,p['fg'],650)+text(x,y+27,label,16,p['muted'])
    body+=f'<path d="M285 88V242M40 158H540" stroke="{p["line"]}"/>'
    body+=text(40,270,f'GITHUB / UPDATED {data["updated"]} UTC',10,p['muted'],400,'letter-spacing="1"')
    svg('stats',theme,580,300,f'公开仓库 {data["public_repos"]} · 原创项目 {data["original_projects"]} · Stars {data["stars"]} · 关注者 {data["followers"]}',body)

def languages(theme,data):
    p=PALETTES[theme]
    body=card_base(p,'代码语言','LANGUAGE MIX')
    values=list(data['languages_bytes'].items())
    total=sum(v for _,v in values)
    shown=values[:4]
    if len(values)>4:
        shown.append(('Other',sum(v for _,v in values[4:])))
    colors=[p['pink'],'#a78bfa','#38bdf8','#34d399','#90909c']
    for i,(lang,count) in enumerate(shown):
        ratio=count/total if total else 0
        y=92+i*33
        body+=text(40,y,lang,15,p['fg'],500)+text(540,y,f'{ratio:.1%}',13,p['muted'],400,'text-anchor="end"')
        body+=f'<rect x="181" y="{y-10}" width="258" height="7" rx="3.5" fill="{p["line"]}"/><rect x="181" y="{y-10}" width="{max(2,258*ratio):.2f}" height="7" rx="3.5" fill="{colors[i]}"/>'
    if not shown:
        body+=text(40,130,'暂无公开代码语言数据',18,p['muted'])
    body+=text(40,270,'PUBLIC ORIGINAL REPOS / BY CODE BYTES',10,p['muted'],400,'letter-spacing=".7"')
    svg('languages',theme,580,300,'公开原创项目的语言构成，按 GitHub 统计的代码字节数计算',body)

def projects(theme):
    p=PALETTES[theme]
    entries=[
        ('helmdesk','01','HelmDesk · 领航台','任务队列、代码差异、验证与用量，放进同一个中文看板。','TypeScript / React / SwiftUI / MCP','AI AGENT / MACOS'),
        ('cube','02','Cube','连接前后端与设备，探索实时通信、设备服务与 OTA 升级。','Vue 3 / FastAPI / MQTT / WebSocket','WEB / IOT'),
        ('sunward','03','Sunward · 逐日计划','双轮小车固件：轮速闭环、编码器里程、航向保持与巡线。','C / STM32 HAL / PI Control','EMBEDDED / ROBOTICS'),
    ]
    for name,number,title,desc,stack,tag in entries:
        body=f'''<rect x="1" y="1" width="1198" height="158" rx="23" fill="{p['panel']}"/><path d="M26 34V126" stroke="{p['pink']}" stroke-width="3" stroke-linecap="round"/>
{text(48,51,number,13,p['pink'],500,'letter-spacing="2"')}{text(92,56,title,28,p['fg'],650)}{text(92,87,desc,18,p['muted'])}{text(92,125,stack,14,p['pink'])}{text(1150,43,tag,12,p['muted'],400,'text-anchor="end" letter-spacing="1"')}{text(1147,123,'↗',37,p['fg'],300,'text-anchor="end"')}'''
        svg(name,theme,1200,160,f'{title} · {desc}',body)
        mobile_body=f'''<rect x="1" y="1" width="638" height="208" rx="23" fill="{p['panel']}"/><path d="M20 30V180" stroke="{p['pink']}" stroke-width="3" stroke-linecap="round"/>
{text(40,38,tag,11,p['pink'],500,'letter-spacing="1"')}{text(40,79,title,28,p['fg'],650)}{text(40,114,desc[:18],18,p['muted'])}{text(40,141,desc[18:],18,p['muted'])}{text(40,183,stack,14,p['pink'])}{text(598,183,'↗',30,p['fg'],300,'text-anchor="end"')}'''
        svg(name+'-mobile',theme,640,210,f'{title} · {desc}',mobile_body)

def dashboard(theme):
    # Nested vector cards retain their text accessibility and render without dependencies.
    cards=[]
    for name in ['stats','languages']:
        raw=(ASSETS/f'{name}-{theme}.svg').read_text()
        cards.append(raw[raw.index('</title>')+len('</title>'):raw.rindex('</svg>')])
    title='公开足迹与代码语言统计'
    svg('dashboard',theme,1200,300,title,f'<g>{cards[0]}</g><g transform="translate(620 0)">{cards[1]}</g>')
    svg('dashboard-mobile',theme,600,620,title,f'<g transform="translate(10 0)">{cards[0]}</g><g transform="translate(10 320)">{cards[1]}</g>')

def blog_banner(theme):
    p=PALETTES[theme]
    defs=f'<radialGradient id="pink"><stop stop-color="{p["pink"]}" stop-opacity=".13"/><stop offset="1" stop-color="{p["pink"]}" stop-opacity="0"/></radialGradient>'
    body=f'''<rect x="650" y="1" width="548" height="198" rx="23" fill="url(#pink)"/>{text(42,45,'MASHUTABA / FIELD NOTES',13,p['pink'],500,'letter-spacing="2.6"')}{text(42,105,'文章负责解释为什么，代码负责证明不是吹牛。',32,p['fg'],600)}{text(42,155,'开发手记 · 单片机 · 教学篇 · 随笔',17,p['muted'])}<rect x="988" y="128" width="170" height="38" rx="19" fill="{p['fg']}"/>{text(1073,153,'打开博客 ↗',16,p['bg'],600,'text-anchor="middle"')}'''
    svg('blog',theme,1200,200,'文章负责解释为什么，代码负责证明不是吹牛。打开麻薯ta爸的博客',body,defs)

def main():
    ASSETS.mkdir(exist_ok=True)
    data=collect()
    for theme in PALETTES:
        header(theme)
        statistics(theme,data)
        languages(theme,data)
        dashboard(theme)
        projects(theme)
        blog_banner(theme)
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'data/public-stats.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(f'Rendered both themes from {data["original_projects"]} public original projects; updated {data["updated"]}.')

if __name__=='__main__':
    main()
