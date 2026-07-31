#!/usr/bin/env python3
"""Generate vault graph with embedded d3.js (no CDN dependency)."""
import os, re, json

vault_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(vault_root, "vault-graph.html")
d3_path = "/tmp/d3.v7.min.js"

with open(d3_path) as f:
    d3_src = f.read()

nodes, edges = [], []
seen_files, seen_edges = set(), set()

for root, dirs, fnames in os.walk(vault_root):
    if '.git' in root:
        continue
    for f in fnames:
        if not f.endswith('.md'):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, vault_root)
        label = os.path.splitext(f)[0]
        parts = rel.split(os.sep)
        group = parts[0] if len(parts) > 1 else "root"
        # disambiguate index files: use parent folder name
        if label == 'index' and len(parts) > 1:
            label = parts[-2]
        elif label == 'index':
            label = 'Home'
        seen_files.add(rel)
        nodes.append({"id": rel, "label": label, "group": group, "file": rel})

for root, dirs, fnames in os.walk(vault_root):
    if '.git' in root:
        continue
    for f in fnames:
        if not f.endswith('.md'):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, vault_root)
        with open(full, encoding='utf-8') as fh:
            content = fh.read()
        for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content):
            target = m.group(1).strip()
            found = False
            for sf in seen_files:
                if sf == target or sf.endswith("/" + target) or sf == target + ".md" or sf.endswith(target + ".md"):
                    target_rel = sf
                    found = True
                    break
            if found and target_rel != rel:
                ek = tuple(sorted([rel, target_rel]))
                if ek not in seen_edges:
                    seen_edges.add(ek)
                    edges.append({"source": rel, "target": target_rel})

colors = {
    "Synergy": "#4e79a7",
    "Projects": "#e15759",
    "Concepts": "#76b7b2",
    "Dev": "#b07aa1",
    "AI-ML": "#ff9da7",
    "Trading": "#59a14f",
    "System": "#af7aa1",
    "root": "#edc948",
    "scripts": "#9c755f",
}

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Vault Graph</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#1a1a2e; overflow:hidden; font-family:system-ui,-apple-system,sans-serif; }}
#graph {{ width:100vw; height:100vh; }}
svg {{ width:100%; height:100%; }}
.node {{ cursor:pointer; }}
.link {{ stroke:#4a4a6a; stroke-opacity:0.4; }}
.label {{ fill:#ccc; font-size:10px; pointer-events:none; text-shadow:0 1px 3px #000; }}
.header {{ position:fixed; top:0; left:0; right:0; text-align:center; color:#eee; font-size:13px; padding:6px 12px; background:rgba(26,26,46,0.9); z-index:10; border-bottom:1px solid #333; }}
.legend {{ position:fixed; bottom:0; left:0; right:0; display:flex; flex-wrap:wrap; gap:6px; justify-content:center; color:#aaa; font-size:11px; padding:6px 12px; background:rgba(26,26,46,0.9); z-index:10; border-top:1px solid #333; }}
.l-item {{ display:flex; align-items:center; gap:3px; }}
.dot {{ width:8px; height:8px; border-radius:50%; display:inline-block; }}
#tip {{ position:fixed; display:none; background:rgba(0,0,0,0.88); color:#eee; padding:5px 10px; border-radius:5px; font-size:13px; z-index:100; pointer-events:none; border:1px solid #555; max-width:80vw; }}
</style>
</head>
<body>
<div class="header">✦ vault-graph · {len(nodes)} notes · {len(edges)} links</div>
<div id="graph"></div>
<div id="tip"></div>
<div class="legend">
"""
for g, c in colors.items():
    html += f'<span class="l-item"><span class="dot" style="background:{c}"></span>{g}</span>'
html += "</div>"

html += """
<script>
""" + d3_src + f"""

const nd = {json.dumps(nodes)};
const ed = {json.dumps(edges)};
const colors = {json.dumps(colors)};

const svg = d3.select("#graph").append("svg")
    .attr("width", "100%").attr("height", "100%");

const w = window.innerWidth, h = window.innerHeight;

// arrow marker
svg.append("defs").append("marker")
    .attr("id","a").attr("viewBox","0 -5 10 10")
    .attr("refX",18).attr("refY",0)
    .attr("markerWidth",5).attr("markerHeight",5)
    .attr("orient","auto")
    .append("path").attr("d","M0,-5L10,0L0,5").attr("fill","#6a6a8a");

const g = svg.append("g");
svg.call(d3.zoom().scaleExtent([0.1,4]).on("zoom",e=>g.attr("transform",e.transform)));

const link = g.selectAll("line").data(ed).enter().append("line")
    .attr("class","link").attr("marker-end","url(#a)").attr("stroke-width",1.5);

const ng = g.selectAll("g.node").data(nd).enter().append("g").attr("class","node")
    .call(d3.drag().on("start",(e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}})
        .on("drag",(e,d)=>{{d.fx=e.x;d.fy=e.y;}})
        .on("end",(e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}));

ng.append("circle").attr("r",6)
    .attr("fill",d=>colors[d.group]||"#888")
    .attr("stroke","#fff").attr("stroke-width",1);

ng.append("text").attr("class","label").attr("dx",10).attr("dy",3).text(d=>d.label);

const sim = d3.forceSimulation(nd)
    .force("link",d3.forceLink(ed).id(d=>d.id).distance(180))
    .force("charge",d3.forceManyBody().strength(-350))
    .force("center",d3.forceCenter(w/2,h/2))
    .force("collide",d3.forceCollide(40))
    .on("tick",()=>{{
        link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
            .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
        ng.attr("transform",d=>`translate(${{d.x}},${{d.y}})`);
    }});

const tip = d3.select("#tip");
ng.on("mouseover touchstart",(e,d)=>{{
    tip.style("display","block").html(`<b>${{d.label}}</b><br><small>${{d.file}}</small>`);
}}).on("mousemove",e=>{{
    tip.style("left",(e.pageX+10)+"px").style("top",(e.pageY-10)+"px");
}}).on("mouseout touchend",()=>tip.style("display","none"));

ng.on("mouseenter",(e,d)=>{{
    const c=new Set(); ed.forEach(e=>{{if(e.source.id===d.id)c.add(e.target.id);if(e.target.id===d.id)c.add(e.source.id);}});
    c.add(d.id); ng.style("opacity",n=>c.has(n.id)?1:0.15); link.style("opacity",e=>e.source.id===d.id||e.target.id===d.id?0.8:0.05);
}}).on("mouseleave",()=>{{ng.style("opacity",1);link.style("opacity",0.4);}});

ng.on("click",(e,d)=>{{const href="/"+(d.file||"").replace(/\.md$/, ".html");window.open(href,"_blank");}});

// handle resize
window.addEventListener("resize",()=>{{
    sim.force("center",d3.forceCenter(window.innerWidth/2,window.innerHeight/2));
    sim.alpha(0.3).restart();
}});
</script>
</body>
</html>"""

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Graph: {output_path} ({len(nodes)} nodes, {len(edges)} edges, {len(html)//1024} KB)")
