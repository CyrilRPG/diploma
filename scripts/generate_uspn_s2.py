import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USPN_S2_ROOT = ROOT / "USPN_S2"
FLASHCARDS_ROOT = ROOT / "flashcard uspn s2"

SUBJECTS = {
    "genetique": ("Genetique", "Génétique"),
    "histologie": ("Histologie", "Histologie"),
    "nutrition": ("Nutrition", "Nutrition"),
}

TYPE_MAP = {
    "app": ("APP", "APP"),
    "socle": ("SOCLE", "SOCLE"),
    "app spe": ("APP SPE", "APP_SPE"),
}


def slugify(name: str) -> str:
    base = re.sub(r"\.js$", "", name, flags=re.IGNORECASE)
    base = re.sub(r"^\s*\d+[^\w]+", "", base)
    base = re.sub(r"[^\w]+", "_", base, flags=re.UNICODE)
    base = base.strip("_").lower()
    return base or "cours"


def prettify_title(name: str) -> str:
    base = re.sub(r"\.js$", "", name, flags=re.IGNORECASE)
    base = re.sub(r"^\s*\d+[^\w]+", "", base)
    base = base.replace("_", " ")
    base = re.sub(r"\s+", " ", base).strip()
    # Capitalize first letter if needed
    if base:
        return base[0].upper() + base[1:]
    return "Cours"


class Course:
    def __init__(self, subject_key, type_key, src_js: Path, html_rel: Path, title: str):
        self.subject_key = subject_key
        self.type_key = type_key  # APP, SOCLE, APP SPE
        self.src_js = src_js
        self.html_rel = html_rel  # relative to USPN_S2_ROOT
        self.title = title


def collect_courses():
    courses = []
    for subject_key, (subject_folder, _subject_label) in SUBJECTS.items():
        for type_dir_name, (type_label, type_folder) in TYPE_MAP.items():
            js_dir = FLASHCARDS_ROOT / subject_key / type_dir_name
            if not js_dir.is_dir():
                continue
            for name in sorted(os.listdir(js_dir)):
                if not name.lower().endswith(".js"):
                    continue
                src_js = js_dir / name
                slug = slugify(name)
                html_name = f"{slug}.html"
                html_rel = Path(subject_folder) / type_folder / html_name
                title = prettify_title(name)
                courses.append(Course(subject_key, type_label, src_js, html_rel, title))
    return courses


def load_js_objects(src_js: Path) -> str:
    text = src_js.read_text(encoding="utf-8")
    # Ensure each line starting with "{" is kept as-is; wrap entire content in array
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


def build_nav_html(courses, current_rel: Path) -> str:
    """
    Build the full <nav id="menu"> HTML for a given page.
    Links are made relative to current_rel (path from USPN_S2_ROOT).
    """
    current_dir = (USPN_S2_ROOT / current_rel).parent

    # Build mapping subject -> type -> list of courses
    tree = {}
    for c in courses:
        sub_folder, sub_label = SUBJECTS[c.subject_key]
        subject_key = sub_folder
        if subject_key not in tree:
            tree[subject_key] = {"label": sub_label, "types": {}}
        if c.type_key not in tree[subject_key]["types"]:
            tree[subject_key]["types"][c.type_key] = []
        tree[subject_key]["types"][c.type_key].append(c)

    def rel_href(target_rel: Path) -> str:
        target_abs = USPN_S2_ROOT / target_rel
        href = os.path.relpath(target_abs, current_dir)
        return href.replace(os.sep, "/")

    lines = []
    lines.append('<nav id="menu">')
    lines.append('\t\t\t\t\t\t\t<header class="major">')
    lines.append('\t\t\t\t\t\t\t\t<h2>Menu</h2>')
    lines.append('\t\t\t\t\t\t\t</header>')
    lines.append('\t\t\t\t\t\t\t<ul>')
    # Accueil & Favoris
    lines.append(f'\t\t\t\t\t\t\t\t<li><a href="{rel_href(Path("index.html"))}">Accueil</a></li>')
    lines.append(f'\t\t\t\t\t\t\t\t<li><a href="{rel_href(Path("favorites.html"))}">Favoris</a></li>')

    # Subjects
    for subject_folder, subject_info in tree.items():
        lines.append("\t\t\t\t\t\t\t\t<li>")
        lines.append(f'\t\t\t\t\t\t\t\t\t<span class="opener">{subject_info["label"]}</span>')
        lines.append("\t\t\t\t\t\t\t\t\t<ul>")
        # Types: APP, SOCLE, APP SPE
        for type_label in ["APP", "SOCLE", "APP SPE"]:
            if type_label not in subject_info["types"]:
                continue
            lines.append("\t\t\t\t\t\t\t\t\t\t<li>")
            lines.append(f'\t\t\t\t\t\t\t\t\t\t\t<span class="opener">{type_label}</span>')
            lines.append("\t\t\t\t\t\t\t\t\t\t\t<ul>")
            for c in sorted(subject_info["types"][type_label], key=lambda cc: cc.title):
                href = rel_href(c.html_rel)
                safe_title = c.title
                lines.append(f'\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="{href}">{safe_title}</a></li>')
            lines.append("\t\t\t\t\t\t\t\t\t\t\t</ul>")
            lines.append("\t\t\t\t\t\t\t\t\t\t</li>")
        # Embryologie will be handled separately in index + nav if needed
        lines.append("\t\t\t\t\t\t\t\t\t</ul>")
        lines.append("\t\t\t\t\t\t\t\t</li>")

    # Embryologie (sans cours)
    lines.append("\t\t\t\t\t\t\t\t<li>")
    lines.append('\t\t\t\t\t\t\t\t\t<span class="opener">Embryologie</span>')
    lines.append("\t\t\t\t\t\t\t\t\t<ul>")
    for label in ["APP", "SOCLE", "APP SPE"]:
        lines.append("\t\t\t\t\t\t\t\t\t\t<li>")
        lines.append(f'\t\t\t\t\t\t\t\t\t\t\t<span class="opener">{label}</span>')
        lines.append("\t\t\t\t\t\t\t\t\t\t\t<ul>")
        lines.append("\t\t\t\t\t\t\t\t\t\t\t\t<!-- Aucun cours pour l\'instant -->")
        lines.append("\t\t\t\t\t\t\t\t\t\t\t</ul>")
        lines.append("\t\t\t\t\t\t\t\t\t\t</li>")
    lines.append("\t\t\t\t\t\t\t\t\t</ul>")
    lines.append("\t\t\t\t\t\t\t\t</li>")

    lines.append("\t\t\t\t\t\t\t</ul>")
    lines.append("\t\t\t\t\t\t</nav>")
    return "\n".join(lines)


def build_course_html(course: Course, courses):
    subject_folder, subject_label = SUBJECTS[course.subject_key]
    type_label = course.type_key  # APP, SOCLE, APP SPE

    html_abs = USPN_S2_ROOT / course.html_rel
    html_abs.parent.mkdir(parents=True, exist_ok=True)

    # Compute relative paths for assets from this course file
    course_dir = html_abs.parent
    def rel_to(path: Path) -> str:
        return os.path.relpath(path, course_dir).replace(os.sep, "/")

    css_href = rel_to(ROOT / "assets" / "css" / "main.css")
    icon_href = rel_to(ROOT / "images" / "diploma.jpeg")
    security_src = rel_to(ROOT / "security.js")
    favorites_src = rel_to(ROOT / "assets" / "js" / "favorites.js")
    jquery_src = rel_to(ROOT / "assets" / "js" / "jquery.min.js")
    browser_src = rel_to(ROOT / "assets" / "js" / "browser.min.js")
    breakpoints_src = rel_to(ROOT / "assets" / "js" / "breakpoints.min.js")
    util_src = rel_to(ROOT / "assets" / "js" / "util.js")
    main_js_src = rel_to(ROOT / "assets" / "js" / "main.js")
    darkmode_src = rel_to(ROOT / "assets" / "js" / "darkmode.js")

    title_text = course.title
    h1 = f"USPN S2 - {subject_label}"
    h2 = f"{type_label} - {title_text}"

    flashcards_body = load_js_objects(course.src_js)
    nav_html = build_nav_html(courses, course.html_rel)

    html = f"""<!DOCTYPE HTML>
<html>
<head>
\t<title>Diploma Santé - Plateforme de Flashcards</title>
\t<meta charset="utf-8" />
\t<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
\t<link rel="stylesheet" href="{css_href}" />
\t<link rel="icon" type="image/jpeg" href="{icon_href}" />
\t<script src="{security_src}" defer></script>
\t<script src="{favorites_src}"></script>
</head>
<body class="is-preload">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
\t<a href="{rel_to(USPN_S2_ROOT / 'index.html')}" class="logo"><strong>Diploma Santé</strong>- USPN S2</a>
\t<ul class="icons">
\t\t<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
\t\t<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
\t\t<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
\t</ul>
</header>

<section>
<header class="main"><div class="header-left"><h1>{h1}</h1><h2>{h2}</h2></div><span class="image main"><img src="{rel_to(ROOT / 'images' / 'banner.png')}" alt="" /></span></header>

<style>
  /* Header compact pour laisser la place aux flashcards */
  #header {{
    padding: 1rem 0;
    margin-bottom: 0.5rem;
  }}

  header.main {{
    margin-top: 1.5rem !important;
    margin-bottom: 0.8rem !important;
    padding-bottom: 0.5rem !important;
    display: flex;
    align-items: center;
    gap: 2rem;
  }}

  header.main .header-left h1,
  header.main .header-left h2 {{
    flex: 1;
    margin: 0 !important;
  }}

  header.main h1 {{
    font-size: 2em !important;
    line-height: 1.3 !important;
  }}

  header.main h2 {{
    font-size: 1.3em !important;
    color: #7f888f !important;
  }}

  header.main .header-left {{
    flex: 1;
    display: flex;
    flex-direction: column;
  }}

  .image.main {{
    flex: 1;
    max-height: none !important;
    overflow: visible !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .image.main img {{
    width: 100% !important;
    height: auto !important;
    max-height: 120px !important;
    object-fit: contain !important;
    object-position: center;
  }}

  section {{
    padding-top: 0 !important;
  }}

  /* Barre de progression cohérente */
  .progress-container {{
    width: 100%;
    max-width: 1000px;
    height: 20px;
    background-color: #eee;
    border-radius: 10px;
    overflow: hidden;
    margin: 0 auto 1rem;
    border: 1px solid #ddd;
  }}

  .progress-bar {{
    height: 100%;
    background-color: #00aeef;
    width: 0%;
    transition: width 0.3s;
  }}

  /* Flashcards plein écran optimisées */
  .flashcards-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 2rem;
    padding: 1rem 0 3rem 0;
    min-height: auto;
  }}

  .flashcard {{
    width: 95% !important;
    max-width: 900px !important;
    height: auto !important;
    min-height: 450px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
  }}
</style>

<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>
<div class="flashcards-container" id="flashcards"></div>

<script>
const flashcardsData =
[
{flashcards_body}
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
    card.addEventListener("click", () => {{
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    toggleBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    inner.appendChild(front);
    inner.appendChild(back);
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
{nav_html}
</div>
</div>

</div>

<script src="{jquery_src}"></script>
<script src="{browser_src}"></script>
<script src="{breakpoints_src}"></script>
<script src="{util_src}"></script>
<script src="{main_js_src}"></script>
<script src="{darkmode_src}"></script>
</body>
</html>
"""
    html_abs.write_text(html, encoding="utf-8")


def update_index_and_favorites(courses):
    # Update index.html
    index_path = USPN_S2_ROOT / "index.html"
    if index_path.exists():
        text = index_path.read_text(encoding="utf-8")
        text = text.replace("USPN S1", "USPN S2")
        text = text.replace("USPN - Semestre 1", "USPN - Semestre 2")
        # Insérer/mettre à jour le menu sans toucher à la section des matières (déjà corrigée à la main)
        nav_html = build_nav_html(courses, Path("index.html"))
        text = re.sub(r"<nav id=\"menu\">.*?</nav>", nav_html, text, flags=re.DOTALL)
        index_path.write_text(text, encoding="utf-8")

    # Update favorites.html
    fav_path = USPN_S2_ROOT / "favorites.html"
    if fav_path.exists():
        text = fav_path.read_text(encoding="utf-8")
        text = text.replace("USPN S1", "USPN S2")
        nav_html = build_nav_html(courses, Path("favorites.html"))
        text = re.sub(r"<nav id=\"menu\">.*?</nav>", nav_html, text, flags=re.DOTALL)
        fav_path.write_text(text, encoding="utf-8")


def main():
    courses = collect_courses()
    if not courses:
        print("No courses found.")
        return
    for c in courses:
        build_course_html(c, courses)
    update_index_and_favorites(courses)
    print(f"Generated {len(courses)} USPN S2 course pages.")


if __name__ == "__main__":
    main()

