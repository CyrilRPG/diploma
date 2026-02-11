#!/usr/bin/env python3
"""
Generate the full UPEC_LSPS1_S2 section from upecl1 JS flashcard files.
Creates: directory structure, index.html, favorites.html, all course HTML files.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/Users/cyrilwisa/Desktop/diploma")
SOURCE_DIR = BASE_DIR / "upecl1"
OUTPUT_DIR = BASE_DIR / "UPEC_LSPS1_S2"

# Structure definition: matiere -> {display_name, icon, sous_matieres}
# sous_matieres: {dir_name -> {display_name, source_dir, courses: [{src_file, html_file, title}]}}
STRUCTURE = {
    "ICM": {
        "display": "ICM",
        "icon": "fa-pills",
        "sous_matieres": None,
        "source_dir": "icm",
        "courses": [
            {"src": "1.js", "html": "fc1.html", "title": "Cours 1 - Le médicament"},
            {"src": "1.2.js", "html": "fc1_2.html", "title": "Cours 1.2 - Le médicament (suite)"},
            {"src": "2.js", "html": "fc2.html", "title": "Cours 2"},
            {"src": "3.js", "html": "fc3.html", "title": "Cours 3"},
            {"src": "4.js", "html": "fc4.html", "title": "Cours 4"},
            {"src": "5.js", "html": "fc5.html", "title": "Cours 5"},
            {"src": "6.1.js", "html": "fc6_1.html", "title": "Cours 6.1"},
            {"src": "6.2.js", "html": "fc6_2.html", "title": "Cours 6.2"},
            {"src": "7.js", "html": "fc7.html", "title": "Cours 7"},
            {"src": "8.js", "html": "fc8.html", "title": "Cours 8"},
            {"src": "9.js", "html": "fc9.html", "title": "Cours 9"},
            {"src": "10.js", "html": "fc10.html", "title": "Cours 10"},
            {"src": "11.js", "html": "fc11.html", "title": "Cours 11"},
            {"src": "12.js", "html": "fc12.html", "title": "Cours 12"},
            {"src": "13.js", "html": "fc13.html", "title": "Cours 13"},
            {"src": "14.js", "html": "fc14.html", "title": "Cours 14"},
            {"src": "15.js", "html": "fc15.html", "title": "Cours 15"},
        ]
    },
    "Bio_Informatique": {
        "display": "Bio-informatique",
        "icon": "fa-laptop-code",
        "sous_matieres": None,
        "source_dir": "bio informatique",
        "courses": [
            {"src": "1.js", "html": "fc1.html", "title": "Cours 1 - Introduction à la bio-informatique"},
            {"src": "2.js", "html": "fc2.html", "title": "Cours 2"},
            {"src": "3.js", "html": "fc3.html", "title": "Cours 3"},
        ]
    },
    "Circulation_Respiration": {
        "display": "Circulation Respiration",
        "icon": "fa-heartbeat",
        "sous_matieres": {
            "Anatomie": {
                "display": "Anatomie",
                "source_dir": "circu respi/anatomie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 11)
                ]
            },
            "Physiologie": {
                "display": "Physiologie",
                "source_dir": "circu respi/physiologie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 8)
                ]
            }
        }
    },
    "Regulation_Neuroendocrienne": {
        "display": "Régulation Neuroendocrienne",
        "icon": "fa-brain",
        "sous_matieres": {
            "Anatomie": {
                "display": "Anatomie",
                "source_dir": "régulation neuroendocrienne/anatomie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 7)
                ]
            },
            "Physiologie": {
                "display": "Physiologie",
                "source_dir": "régulation neuroendocrienne/physiologie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 7)
                ]
            }
        }
    },
    "Squelette_Motricite": {
        "display": "Squelette et Motricité",
        "icon": "fa-bone",
        "sous_matieres": {
            "Anatomie": {
                "display": "Anatomie",
                "source_dir": "squelette et motricité/1 Anatomie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 7)
                ]
            },
            "Activite_Physique": {
                "display": "Activité physique et santé",
                "source_dir": "squelette et motricité/2 Activité et physique et santé selon les spécificités liés a l_age",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 5)
                ]
            },
            "Situations_Handicap": {
                "display": "Situations de handicap",
                "source_dir": "squelette et motricité/3 situations de handicap",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 3)
                ]
            },
            "Physiologie": {
                "display": "Physiologie",
                "source_dir": "squelette et motricité/4 Physiologie",
                "courses": [
                    {"src": f"{i}.js", "html": f"fc{i}.html", "title": f"Cours {i}"}
                    for i in range(1, 3)
                ]
            }
        }
    }
}


def read_js_flashcards(filepath):
    """Read a JS flashcard file and return its content as a string for embedding."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    # Remove empty lines
    lines = [l for l in content.split('\n') if l.strip()]
    return '\n'.join(lines)


def build_menu_html(prefix=".."):
    """Build the complete navigation menu HTML."""
    lines = []
    lines.append(f'<nav id="menu">')
    lines.append(f'<header class="major"><h2>Menu</h2></header>')
    lines.append(f'<ul>')
    lines.append(f'<li><a href="{prefix}/index.html">Accueil</a></li>')
    lines.append(f'<li><a href="{prefix}/favorites.html">Favoris</a></li>')
    
    for mat_dir, mat_info in STRUCTURE.items():
        mat_display = mat_info["display"]
        if mat_info.get("sous_matieres"):
            lines.append(f'<li><span class="opener">{mat_display}</span><ul>')
            for sm_dir, sm_info in mat_info["sous_matieres"].items():
                sm_display = sm_info["display"]
                lines.append(f'<li><span class="opener">{sm_display}</span><ul>')
                for c in sm_info["courses"]:
                    lines.append(f'<li><a href="{prefix}/{mat_dir}/{sm_dir}/{c["html"]}">{c["title"]}</a></li>')
                lines.append(f'</ul></li>')
            lines.append(f'</ul></li>')
        else:
            lines.append(f'<li><span class="opener">{mat_display}</span><ul>')
            for c in mat_info["courses"]:
                lines.append(f'<li><a href="{prefix}/{mat_dir}/{c["html"]}">{c["title"]}</a></li>')
            lines.append(f'</ul></li>')
    
    lines.append(f'</ul></nav>')
    return '\n'.join(lines)


def get_course_html(matiere_display, course_title, flashcards_js, depth, menu_prefix):
    """Generate a complete course HTML page."""
    asset_prefix = "../" * depth
    menu_html = build_menu_html(menu_prefix)
    
    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="{asset_prefix}assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="{asset_prefix}images/diploma.jpeg" />
<script src="{asset_prefix}security.js" defer></script>
<script src="{asset_prefix}assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="{asset_prefix}index.html" class="logo"><strong>Diploma Santé</strong> - UPEC LSPS1 S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section>
<header class="main"><div class="header-left"><h1>{matiere_display}</h1><h2>{course_title}</h2></div><span class="image main"><img src="{asset_prefix}images/banner.png" alt="" /></span></header>

<style>
  #header {{ padding: 1rem 0; margin-bottom: 0.5rem; }}
  header.main {{ margin-top: 1.5rem !important; margin-bottom: 0.8rem !important; padding-bottom: 0.5rem !important; display: flex; align-items: center; gap: 2rem; }}
  header.main .header-left h1, header.main .header-left h2 {{ flex: 1; margin: 0 !important; }}
  header.main h1 {{ font-size: 2em !important; line-height: 1.3 !important; }}
  header.main h2 {{ font-size: 1.3em !important; color: #7f888f !important; }}
  header.main .header-left {{ flex: 1; display: flex; flex-direction: column; }}
  .image.main {{ flex: 1; max-height: none !important; overflow: visible !important; margin: 0 !important; display: flex; align-items: center; justify-content: center; }}
  .image.main img {{ width: 100% !important; height: auto !important; max-height: 120px !important; object-fit: contain !important; object-position: center; }}
  section {{ padding-top: 0 !important; }}
  .progress-container {{ width: 100%; max-width: 1000px; height: 20px; background-color: #eee; border-radius: 10px; overflow: hidden; margin: 0 auto 1rem; border: 1px solid #ddd; }}
  .progress-bar {{ height: 100%; background-color: #00aeef; width: 0%; transition: width 0.3s; }}
  .flashcards-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2rem; min-height: calc(100vh - 250px); padding: 1rem 0; }}
  .flashcard {{ width: 100%; max-width: 1000px; height: calc(100vh - 340px); min-height: 450px; perspective: 1500px; cursor: pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }}
  .flashcard-inner {{ position: relative; width: 100%; height: 100%; border-radius: 20px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25); background-color: white; transition: transform 0.6s; overflow: visible; transform-style: preserve-3d; }}
  .flashcard.show-answer .flashcard-inner {{ transform: rotateY(180deg); }}
  .flashcard-front, .flashcard-back {{ position: absolute; width: 100%; height: 100%; border-radius: 20px; backface-visibility: hidden; display: flex; justify-content: center; align-items: center; padding: 3rem; font-size: 2rem; text-align: center; }}
  .flashcard-front {{ background-color: white; color: #333; box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15); }}
  .flashcard-back {{ background-color: #73C3EC; color: white; overflow: visible; transform: rotateY(180deg); box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5); font-size: 2.2rem; text-shadow: 0 0 4px rgba(255, 255, 255, 0.3); }}
  .flashcard-button {{ margin-top: 1rem; display: flex; justify-content: center; align-items: center; gap: 1rem; width: 100%; flex-wrap: wrap; }}
  .check-icon, .cross-icon, .favorite-icon {{ display: none; position: absolute; cursor: pointer; z-index: 1000; transition: all 0.3s; opacity: 0.8; pointer-events: auto; }}
  .check-icon {{ top: 30px; left: 30px; align-items: center; justify-content: center; width: 45px; height: 45px; overflow: visible; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); cursor: pointer; transition: all 0.3s; color: #888; font-size: 20px; }}
  .check-icon i {{ pointer-events: none; transform: scaleX(-1); }}
  .cross-icon {{ top: 30px; right: 30px; stroke: #888; align-items: center; justify-content: center; width: 45px; height: 45px; overflow: visible; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); cursor: pointer; transition: all 0.3s; }}
  body.dark-mode .check-icon, body.dark-mode .cross-icon {{ background: rgba(50, 50, 50, 0.95); color: #fff; stroke: #fff; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.5); }}
  body.dark-mode .check-icon:hover {{ background: rgba(40, 150, 40, 0.95); color: #fff; }}
  body.dark-mode .cross-icon:hover {{ background: rgba(150, 40, 40, 0.95); stroke: #fff; }}
  .favorite-icon {{ bottom: 15px; left: 50%; transform: translateX(-50%); fill: #888; width: 30px; height: 30px; }}
  .favorite-icon.active {{ fill: #ffd700; }}
  .flashcard.show-answer .check-icon, .flashcard.show-answer .cross-icon, .flashcard.show-answer .favorite-icon {{ display: flex !important; }}
  .check-icon:hover {{ stroke: #27ae60; color: #27ae60; opacity: 1; }}
  .cross-icon:hover {{ stroke: #e74c3c; opacity: 1; }}
  .slide-left {{ animation: slideLeft 0.4s forwards; }}
  .slide-right {{ animation: slideRight 0.4s forwards; }}
  @keyframes slideLeft {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(-100%); opacity: 0; }} }}
  @keyframes slideRight {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(100%); opacity: 0; }} }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; }}
  body.dark-mode .progress-container {{ background-color: #34495e; border-color: #4a5568; }}
</style>

<div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>
<div class="flashcards-container" id="flashcards"></div>

<script>
const flashcardsData = [
{flashcards_js}
];

const container = document.getElementById("flashcards");
const progressBar = document.getElementById("progressBar");
const originalData = [...flashcardsData];
let flashcards = [...originalData];
const pageId = location.pathname.split("/").pop().replace(".html","");
const progressKey = "progress_" + pageId;
let currentIndex = parseInt(localStorage.getItem(progressKey)) || 0;
if (currentIndex >= originalData.length) {{ currentIndex = 0; localStorage.setItem(progressKey, currentIndex); }}

function updateProgress() {{
  const total = originalData.length;
  const progress = Math.min(currentIndex / total, 1);
  progressBar.style.width = `${{progress * 100}}%`;
}}

function createContent(content) {{
  if (typeof content === "string") {{
    const div = document.createElement("div");
    div.textContent = content;
    return div;
  }}
  if (typeof content === "object" && content.type === "image") {{
    const wrapper = document.createElement("div");
    wrapper.style.textAlign = "center";
    if (content.caption) {{
      const caption = document.createElement("div");
      caption.textContent = content.caption;
      caption.style.marginBottom = "6px";
      caption.style.fontStyle = "italic";
      caption.style.fontSize = "0.9em";
      wrapper.appendChild(caption);
    }}
    const img = document.createElement("img");
    img.src = content.src;
    img.alt = content.alt || "";
    img.style.maxWidth = "100%";
    img.style.height="auto"; img.style.maxHeight="150px"; img.style.objectFit="contain";
    wrapper.appendChild(img);
    return wrapper;
  }}
  return document.createElement("div");
}}

function showCard(index) {{
  container.innerHTML = "";
  if (flashcards[index]) {{
    const {{ question, answer }} = flashcards[index];
    const card = document.createElement("div");
    card.classList.add("flashcard", "show");
    const inner = document.createElement("div");
    inner.classList.add("flashcard-inner");
    const front = document.createElement("div");
    front.classList.add("flashcard-front");
    front.appendChild(createContent(question));
    const back = document.createElement("div");
    back.classList.add("flashcard-back");
    back.appendChild(createContent(answer));
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("flashcard-button");
    const toggleBtn = document.createElement("button");
    toggleBtn.classList.add("button", "large");
    toggleBtn.textContent = "Voir la réponse";
    const resetBtn = document.createElement("button");
    resetBtn.classList.add("button", "large");
    resetBtn.textContent = "Réinitialiser";
    resetBtn.id = "reset";
    resetBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);
    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = '<i class="fas fa-check"></i>';
    checkIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-right");
      setTimeout(() => {{
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }}, 400);
    }});
    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>`;
    crossIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-left");
      setTimeout(() => {{
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }}, 400);
    }});
    const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    function updateFav() {{
      if (isFavorite({{question, answer}})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }}
    favIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      toggleFavorite({{question, answer}});
      updateFav();
    }});
    updateFav();
    card.addEventListener("click", () => {{
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    card.appendChild(inner);
    card.appendChild(btnContainer);
    container.appendChild(card);
  }} else {{
    container.innerHTML = "";
    const endCard = document.createElement("div");
    endCard.classList.add("flashcard", "show", "show-answer");
    const inner = document.createElement("div");
    inner.classList.add("flashcard-inner");
    const back = document.createElement("div");
    back.classList.add("flashcard-back");
    back.innerHTML = "<p>Plus de flashcard disponible.</p>";
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("flashcard-button");
    const resetBtn = document.createElement("button");
    resetBtn.classList.add("button", "large");
    resetBtn.textContent = "Réinitialiser";
    resetBtn.id = "reset";
    resetBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(resetBtn);
    inner.appendChild(back);
    endCard.appendChild(inner);
    endCard.appendChild(btnContainer);
    container.appendChild(endCard);
    localStorage.setItem("completed_" + pageId, "true");
    updateProgress();
  }}
}}

showCard(currentIndex);
updateProgress();
</script>

</section>

</div>
</div>

<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>

{menu_html}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<script src="{asset_prefix}assets/js/jquery.min.js"></script>
<script src="{asset_prefix}assets/js/browser.min.js"></script>
<script src="{asset_prefix}assets/js/breakpoints.min.js"></script>
<script src="{asset_prefix}assets/js/util.js"></script>
<script src="{asset_prefix}assets/js/main.js"></script>
<script src="{asset_prefix}assets/js/darkmode.js"></script>
<script src="{asset_prefix}assets/js/favorites.js"></script>

</body>
</html>'''


def get_all_course_paths():
    """Get all course file paths for tracking."""
    paths = []
    for mat_dir, mat_info in STRUCTURE.items():
        if mat_info.get("sous_matieres"):
            for sm_dir, sm_info in mat_info["sous_matieres"].items():
                for c in sm_info["courses"]:
                    paths.append(f"{mat_dir}/{sm_dir}/{c['html']}")
        else:
            for c in mat_info["courses"]:
                paths.append(f"{mat_dir}/{c['html']}")
    return paths


def generate_index():
    """Generate the index.html page."""
    menu_html = build_menu_html(".")
    course_paths = get_all_course_paths()
    course_paths_js = ",\n".join([f"'{p}'" for p in course_paths])
    
    # Build features grid
    features = []
    for mat_dir, mat_info in STRUCTURE.items():
        first_course = None
        if mat_info.get("sous_matieres"):
            first_sm = list(mat_info["sous_matieres"].keys())[0]
            first_c = mat_info["sous_matieres"][first_sm]["courses"][0]
            first_course = f"{mat_dir}/{first_sm}/{first_c['html']}"
        else:
            first_course = f"{mat_dir}/{mat_info['courses'][0]['html']}"
        
        features.append(f'''<article>
<span class="icon solid {mat_info["icon"]}"></span>
<div class="content">
<h3>{mat_info["display"]}</h3>
<ul class="actions">
<li><a href="{first_course}" class="button big">Commencer</a></li>
</ul>
</div>
</article>''')
    
    features_html = "\n".join(features)
    
    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards - UPEC LSPS1 S2</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../images/diploma.jpeg" />
<script src="../security.js" defer></script>
<script src="../assets/js/favorites.js"></script>
</head>
<body class="is-preload index-page">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UPEC LSPS1 S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section id="banner">
<div class="content">
<header>
<h1>UPEC LSPS1 - Semestre 2</h1>
<p>Plateforme de Flashcards</p>
</header>
<p>Boostez vos révisions en santé avec des flashcards efficaces, spécialement pensées pour les étudiants de l'UPEC !</p>
<p id="courseSummary" style="color:#00aeef;"><span class="icon solid fa-star"></span> Cours complétés: <strong><span id="completedCourses"></span>/<span id="totalCourses"></span></strong></p>
</div>
<span class="image">
<img src="../images/pic01.jpg" alt="" />
</span>
</section>

<section>
<header class="major">
<h2>Explorez les matières disponibles</h2>
</header>
<div class="features">
{features_html}
</div>
</section>

</div>
</div>

<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>

{menu_html}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/darkmode.js"></script>
<script src="../assets/js/favorites.js"></script>
<script>
const COURSE_PATHS = [
{course_paths_js}
];

function getPageIdFromPath(path) {{
  return path.split('/').pop().replace(/\\.html$/, '');
}}

function updateCourseCount() {{
  const total = COURSE_PATHS.length;
  let completed = 0;
  COURSE_PATHS.forEach(function(coursePath) {{
    const pageId = getPageIdFromPath(coursePath);
    const key = 'completed_' + pageId;
    if (localStorage.getItem(key) === 'true') {{
      completed++;
    }}
  }});
  const completedEl = document.getElementById('completedCourses');
  const totalEl = document.getElementById('totalCourses');
  if (completedEl) completedEl.textContent = completed;
  if (totalEl) totalEl.textContent = total;
}}

document.addEventListener("DOMContentLoaded", function() {{
  updateCourseCount();
}});
</script>

</body>
</html>'''


def generate_favorites():
    """Generate the favorites.html page."""
    menu_html = build_menu_html(".")
    
    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../images/diploma.jpeg" />
<script src="../security.js" defer></script>
<script src="../assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UPEC LSPS1 S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section>
<header class="main"><div class="header-left"><h1>UPEC LSPS1 S2</h1><h2>Flashcards favorites</h2></div><span class="image main"><img src="../images/banner.png" alt="" /></span></header>

<style>
  #header {{ padding: 1rem 0; margin-bottom: 0.5rem; }}
  header.main {{ margin-top: 1.5rem !important; margin-bottom: 0.8rem !important; padding-bottom: 0.5rem !important; display: flex; align-items: center; gap: 2rem; }}
  header.main .header-left h1, header.main .header-left h2 {{ flex: 1; margin: 0 !important; }}
  header.main h1 {{ font-size: 2em !important; line-height: 1.3 !important; }}
  header.main h2 {{ font-size: 1.3em !important; color: #7f888f !important; }}
  header.main .header-left {{ flex: 1; display: flex; flex-direction: column; }}
  .image.main {{ flex: 1; max-height: none !important; overflow: visible !important; margin: 0 !important; display: flex; align-items: center; justify-content: center; }}
  .image.main img {{ width: 100% !important; height: auto !important; max-height: 120px !important; object-fit: contain !important; object-position: center; }}
  section {{ padding-top: 0 !important; }}
  .progress-container {{ width: 100%; max-width: 1000px; height: 20px; background-color: #eee; border-radius: 10px; overflow: hidden; margin: 0 auto 1rem; border: 1px solid #ddd; }}
  .progress-bar {{ height: 100%; background-color: #00aeef; width: 0%; transition: width 0.3s; }}
  .flashcards-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2rem; min-height: calc(100vh - 250px); padding: 1rem 0; }}
  .flashcard {{ width: 100%; max-width: 1000px; height: calc(100vh - 340px); min-height: 450px; perspective: 1500px; cursor: pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }}
  .flashcard-inner {{ position: relative; width: 100%; height: 100%; border-radius: 20px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25); background-color: white; transition: transform 0.6s; overflow: visible; transform-style: preserve-3d; }}
  .flashcard.show-answer .flashcard-inner {{ transform: rotateY(180deg); }}
  .flashcard-front, .flashcard-back {{ position: absolute; width: 100%; height: 100%; border-radius: 20px; backface-visibility: hidden; display: flex; justify-content: center; align-items: center; padding: 3rem; font-size: 2rem; text-align: center; }}
  .flashcard-front {{ background-color: white; color: #333; box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15); }}
  .flashcard-back {{ background-color: #73C3EC; color: white; overflow: visible; transform: rotateY(180deg); box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5); font-size: 2.2rem; text-shadow: 0 0 4px rgba(255, 255, 255, 0.3); }}
  .flashcard-button {{ margin-top: 1rem; display: flex; justify-content: center; align-items: center; gap: 1rem; width: 100%; flex-wrap: wrap; }}
  .check-icon, .cross-icon, .favorite-icon {{ display: none; position: absolute; cursor: pointer; z-index: 1000; transition: all 0.3s; opacity: 0.8; pointer-events: auto; }}
  .check-icon {{ top: 30px; left: 30px; align-items: center; justify-content: center; width: 45px; height: 45px; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); color: #888; font-size: 20px; }}
  .cross-icon {{ top: 30px; right: 30px; stroke: #888; align-items: center; justify-content: center; width: 45px; height: 45px; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); }}
  body.dark-mode .check-icon, body.dark-mode .cross-icon {{ background: rgba(50, 50, 50, 0.95); color: #fff; stroke: #fff; }}
  .favorite-icon {{ bottom: 15px; left: 50%; transform: translateX(-50%); fill: #888; width: 30px; height: 30px; }}
  .favorite-icon.active {{ fill: #ffd700; }}
  .flashcard.show-answer .check-icon, .flashcard.show-answer .cross-icon, .flashcard.show-answer .favorite-icon {{ display: flex !important; }}
  .check-icon:hover {{ color: #27ae60; }} .cross-icon:hover {{ stroke: #e74c3c; }}
  .slide-left {{ animation: slideLeft 0.4s forwards; }} .slide-right {{ animation: slideRight 0.4s forwards; }}
  @keyframes slideLeft {{ to {{ transform: translateX(-100%); opacity: 0; }} }}
  @keyframes slideRight {{ to {{ transform: translateX(100%); opacity: 0; }} }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; }}
  body.dark-mode .progress-container {{ background-color: #34495e; border-color: #4a5568; }}
</style>

<div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>
<div class="flashcards-container" id="flashcards"></div>

<script>
const favs = JSON.parse(localStorage.getItem("flashcard_favorites") || "[]");
const flashcardsData = favs;

const container = document.getElementById("flashcards");
const progressBar = document.getElementById("progressBar");
const originalData = [...flashcardsData];
let flashcards = [...originalData];
const pageId = "favorites_upec_lsps1_s2";
const progressKey = "progress_" + pageId;
let currentIndex = parseInt(localStorage.getItem(progressKey)) || 0;
if (currentIndex >= originalData.length) {{ currentIndex = 0; localStorage.setItem(progressKey, currentIndex); }}

function updateProgress() {{
  const total = originalData.length;
  if (total === 0) return;
  const progress = Math.min(currentIndex / total, 1);
  progressBar.style.width = `${{progress * 100}}%`;
}}

function createContent(content) {{
  if (typeof content === "string") {{
    const div = document.createElement("div");
    div.textContent = content;
    return div;
  }}
  return document.createElement("div");
}}

function showCard(index) {{
  container.innerHTML = "";
  if (flashcards.length === 0) {{
    container.innerHTML = '<div class="flashcard show show-answer"><div class="flashcard-inner"><div class="flashcard-back"><p>Aucune flashcard en favoris.</p></div></div></div>';
    return;
  }}
  if (flashcards[index]) {{
    const {{ question, answer }} = flashcards[index];
    const card = document.createElement("div");
    card.classList.add("flashcard", "show");
    const inner = document.createElement("div");
    inner.classList.add("flashcard-inner");
    const front = document.createElement("div");
    front.classList.add("flashcard-front");
    front.appendChild(createContent(question));
    const back = document.createElement("div");
    back.classList.add("flashcard-back");
    back.appendChild(createContent(answer));
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("flashcard-button");
    const toggleBtn = document.createElement("button");
    toggleBtn.classList.add("button", "large");
    toggleBtn.textContent = "Voir la réponse";
    const resetBtn = document.createElement("button");
    resetBtn.classList.add("button", "large");
    resetBtn.textContent = "Réinitialiser";
    resetBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);
    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = '<i class="fas fa-check"></i>';
    checkIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-right");
      setTimeout(() => {{
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }}, 400);
    }});
    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>`;
    crossIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-left");
      setTimeout(() => {{
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }}, 400);
    }});
    const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    function updateFav() {{
      if (isFavorite({{question, answer}})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }}
    favIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      toggleFavorite({{question, answer}});
      updateFav();
    }});
    updateFav();
    card.addEventListener("click", () => {{
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    card.appendChild(inner);
    card.appendChild(btnContainer);
    container.appendChild(card);
  }} else {{
    container.innerHTML = '<div class="flashcard show show-answer"><div class="flashcard-inner"><div class="flashcard-back"><p>Plus de flashcard disponible.</p></div></div></div>';
    updateProgress();
  }}
}}

showCard(currentIndex);
updateProgress();
</script>

</section>
</div>
</div>

<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>

{menu_html}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/darkmode.js"></script>
<script src="../assets/js/favorites.js"></script>

</body>
</html>'''


def main():
    print("=== Generating UPEC_LSPS1_S2 ===")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Track created files
    created = 0
    
    # Generate course files
    for mat_dir, mat_info in STRUCTURE.items():
        mat_display = mat_info["display"]
        
        if mat_info.get("sous_matieres"):
            for sm_dir, sm_info in mat_info["sous_matieres"].items():
                out_dir = OUTPUT_DIR / mat_dir / sm_dir
                os.makedirs(out_dir, exist_ok=True)
                
                for course in sm_info["courses"]:
                    src_path = SOURCE_DIR / sm_info["source_dir"] / course["src"]
                    if not src_path.exists():
                        print(f"WARNING: Source not found: {src_path}")
                        continue
                    
                    fc_content = read_js_flashcards(src_path)
                    # depth is 3: UPEC_LSPS1_S2/Mat/SM/file.html -> ../../../
                    menu_prefix = "../.."
                    html = get_course_html(
                        f"{mat_display} - {sm_info['display']}",
                        course["title"],
                        fc_content,
                        3,  # depth for asset prefix
                        menu_prefix
                    )
                    
                    out_file = out_dir / course["html"]
                    with open(out_file, 'w', encoding='utf-8') as f:
                        f.write(html)
                    created += 1
                    print(f"Created: {out_file.relative_to(BASE_DIR)}")
        else:
            out_dir = OUTPUT_DIR / mat_dir
            os.makedirs(out_dir, exist_ok=True)
            
            source_dir = mat_info.get("source_dir", "")
            for course in mat_info["courses"]:
                src_path = SOURCE_DIR / source_dir / course["src"]
                if not src_path.exists():
                    print(f"WARNING: Source not found: {src_path}")
                    continue
                
                fc_content = read_js_flashcards(src_path)
                # depth is 2: UPEC_LSPS1_S2/Mat/file.html -> ../../
                menu_prefix = ".."
                html = get_course_html(
                    mat_display,
                    course["title"],
                    fc_content,
                    2,  # depth for asset prefix
                    menu_prefix
                )
                
                out_file = out_dir / course["html"]
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                created += 1
                print(f"Created: {out_file.relative_to(BASE_DIR)}")
    
    # Generate index.html
    index_html = generate_index()
    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    created += 1
    print(f"Created: UPEC_LSPS1_S2/index.html")
    
    # Generate favorites.html
    fav_html = generate_favorites()
    with open(OUTPUT_DIR / "favorites.html", 'w', encoding='utf-8') as f:
        f.write(fav_html)
    created += 1
    print(f"Created: UPEC_LSPS1_S2/favorites.html")
    
    print(f"\n=== Total: {created} files created ===")


if __name__ == "__main__":
    main()
