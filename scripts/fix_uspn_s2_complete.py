#!/usr/bin/env python3
"""
Script pour corriger les fichiers USPN_S2:
1. Ajouter les icônes check/cross/favorite dans le JavaScript
2. Corriger les noms des cours (enlever chiffres, corriger orthographe)
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# Mapping des corrections de noms de cours
NAME_CORRECTIONS = {
    # Histologie SOCLE
    "1 Tissu éphitelial": "Tissu épithélial",
    "1 tissu éphitelial": "Tissu épithélial",
    "2 Tissus éphitelial": "Tissu épithélial (suite)",
    "2 tissus éphitelial": "Tissu épithélial (suite)",
    "1 tissus conjonctif": "Tissu conjonctif",
    "1 Tissus conjonctif": "Tissu conjonctif",
    "2 tissus conjonctif": "Tissu conjonctif (cellules)",
    "2 Tissus conjonctif": "Tissu conjonctif (cellules)",
    "3 Tissus conjonctif": "Tissu conjonctif (MEC)",
    "3 tissus conjonctif": "Tissu conjonctif (MEC)",
    "1 Tissus cartilagineux": "Tissu cartilagineux",
    "1 tissus cartilagineux": "Tissu cartilagineux",
    "2 Tissus osseux": "Tissu osseux",
    "2 tissus osseux": "Tissu osseux",
    "1 Tissus musculaire": "Tissu musculaire",
    "1 tissus musculaire": "Tissu musculaire",
    "2 Leiomyocyte": "Léiomyocyte",
    "2 leiomyocyte": "Léiomyocyte",
    "Tissus Nerveux": "Tissu nerveux",
    "tissus nerveux": "Tissu nerveux",
    "Méthode d étude": "Méthodes d'étude",
    "me_thode_d_e_tude": "Méthodes d'étude",
    
    # Histologie APP
    "2 Tissus squelettique": "Tissu squelettique",
    "2 tissus squelettique": "Tissu squelettique",
    "App parenchyme nerveux": "Parenchyme nerveux",
    "app parenchyme nerveux": "Parenchyme nerveux",
    "Ephitelium glandulaires": "Épithéliums glandulaires",
    "ephitelium glandulaires": "Épithéliums glandulaires",
    "Tissus conjonctif": "Tissu conjonctif",
    "tissus conjonctif": "Tissu conjonctif",
    "Tissus musculaire cardiaque": "Tissu musculaire cardiaque",
    "tissus musculaire cardiaque": "Tissu musculaire cardiaque",
    
    # Histologie APP SPE
    "1 Appareil cardio": "Appareil cardiovasculaire",
    "1 appareil cardio": "Appareil cardiovasculaire",
    "2 Appareil cardiovasculaire": "Appareil cardiovasculaire (suite)",
    "2 appareil cardiovasculaire": "Appareil cardiovasculaire (suite)",
    "Appareil urinaire": "Appareil urinaire",
    
    # Génétique
    "Anomalies de caryotype om": "Anomalies du caryotype",
    "anomalies de caryotype om": "Anomalies du caryotype",
    "Caryotype humain om": "Caryotype humain",
    "caryotype humain om": "Caryotype humain",
    "Diagnostic prénatal et diagnostique pré implanmatoire": "Diagnostic prénatal et préimplantatoire",
    "diagnostic prénatal et diagnostique pré implanmatoire": "Diagnostic prénatal et préimplantatoire",
    "Modes de transmission": "Modes de transmission",
    
    # Nutrition SOCLE
    "1 introduction": "Introduction à la nutrition",
    "1 Introduction": "Introduction à la nutrition",
    "1 étabolisme des acides aminés": "Métabolisme des acides aminés",
    "1 e tabolisme des acides amine s": "Métabolisme des acides aminés",
    "2 étabolisme des acides aminés": "Métabolisme des acides aminés (suite)",
    "2 e tabolisme des acides amine s": "Métabolisme des acides aminés (suite)",
    "Métabolisme lipidique": "Métabolisme lipidique",
    "me tabolisme lipidique": "Métabolisme lipidique",
    "Métabolisme glucides": "Métabolisme des glucides",
    "me tabolisme glucides": "Métabolisme des glucides",
    "Substrats énergétique": "Substrats énergétiques",
    "substrats e nerge tique": "Substrats énergétiques",
    
    # Nutrition APP
    "App Relations nutrition-santé": "Relations nutrition-santé",
    "app relations nutrition sante": "Relations nutrition-santé",
    "Approfondissement introduction au diabète": "Introduction au diabète",
    "approfondissement introduction au diabe te": "Introduction au diabète",
    "Dyslépiudemie": "Dyslipidémie",
    "dysle piudemie": "Dyslipidémie",
    "Obésité actu": "Obésité",
    "obe site actu": "Obésité",
    
    # Pour les h2 avec préfixes SOCLE/APP
    "SOCLE - 1 tissu éphitelial": "SOCLE - Tissu épithélial",
    "SOCLE - 2 tissus éphitelial": "SOCLE - Tissu épithélial (suite)",
    "SOCLE - 1 tissus conjonctif": "SOCLE - Tissu conjonctif",
    "SOCLE - 2 tissus conjonctif": "SOCLE - Tissu conjonctif (cellules)",
    "SOCLE - 3 tissus conjonctif": "SOCLE - Tissu conjonctif (MEC)",
    "SOCLE - 1 tissus cartilagineux": "SOCLE - Tissu cartilagineux",
    "SOCLE - 2 tissus osseux": "SOCLE - Tissu osseux",
    "SOCLE - 1 tissus musculaire": "SOCLE - Tissu musculaire",
    "SOCLE - 2 leiomyocyte": "SOCLE - Léiomyocyte",
    "SOCLE - Tissus nerveux": "SOCLE - Tissu nerveux",
    "SOCLE - Me thode d e tude": "SOCLE - Méthodes d'étude",
    "APP - 2 tissus squelettique": "APP - Tissu squelettique",
    "APP - App parenchyme nerveux": "APP - Parenchyme nerveux",
    "APP - Ephitelium glandulaires": "APP - Épithéliums glandulaires",
    "APP - Tissus conjonctif": "APP - Tissu conjonctif",
    "APP - Tissus musculaire cardiaque": "APP - Tissu musculaire cardiaque",
    "APP SPE - 1 appareil cardio": "APP SPE - Appareil cardiovasculaire",
    "APP SPE - 2 appareil cardiovasculaire": "APP SPE - Appareil cardiovasculaire (suite)",
    "APP SPE - Appareil urinaire": "APP SPE - Appareil urinaire",
    "APP - Anomalies de caryotype om": "APP - Anomalies du caryotype",
    "APP - Diagnostic pre natal et diagnostique pre implanmatoire": "APP - Diagnostic prénatal et préimplantatoire",
    "SOCLE - Caryotype humain om": "SOCLE - Caryotype humain",
    "SOCLE - Modes de transmission": "SOCLE - Modes de transmission",
    "SOCLE - 1 introduction": "SOCLE - Introduction à la nutrition",
    "SOCLE - 1 e tabolisme des acides amine s": "SOCLE - Métabolisme des acides aminés",
    "SOCLE - 2 e tabolisme des acides amine s": "SOCLE - Métabolisme des acides aminés (suite)",
    "SOCLE - Me tabolisme lipidique": "SOCLE - Métabolisme lipidique",
    "SOCLE - Me tabolisme glucides": "SOCLE - Métabolisme des glucides",
    "SOCLE - Substrats e nerge tique": "SOCLE - Substrats énergétiques",
    "APP - App relations nutrition sante": "APP - Relations nutrition-santé",
    "APP - Approfondissement introduction au diabe te": "APP - Introduction au diabète",
    "APP - Dysle piudemie": "APP - Dyslipidémie",
    "APP - Obe site actu": "APP - Obésité",
}

# JavaScript complet avec les icônes check/cross/favorite (copié de SU_S2)
JS_SHOW_CARD_WITH_ICONS = '''function showCard(index) {
  container.innerHTML = "";

  if (flashcards[index]) {
    const { question, answer } = flashcards[index];
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
    resetBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    });

    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);

    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = '<i class="fas fa-check"></i>';
    checkIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      card.classList.add("slide-right");
      setTimeout(() => {
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }, 400);
    });

    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    `;
    crossIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      card.classList.add("slide-left");
      setTimeout(() => {
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }, 400);
    });

    const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    function updateFav() {
      if (isFavorite({question, answer})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }
    favIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleFavorite({question, answer});
      updateFav();
    });
    updateFav();

    card.addEventListener("click", () => {
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    });

    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    card.appendChild(inner);
    card.appendChild(btnContainer);

    container.appendChild(card);
  } else {
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
    resetBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    });

    btnContainer.appendChild(resetBtn);

    inner.appendChild(back);
    endCard.appendChild(inner);
    endCard.appendChild(btnContainer);

    container.appendChild(endCard);

    localStorage.setItem("completed_" + pageId, "true");
    updateProgress();
  }
}'''

def fix_course_file(filepath: Path):
    """Corrige un fichier de cours USPN_S2."""
    content = filepath.read_text(encoding='utf-8')
    original_content = content
    
    # 1. Corriger les noms dans le h2 du header
    for old_name, new_name in NAME_CORRECTIONS.items():
        # Dans les balises h2
        content = re.sub(
            rf'(<h2>)({re.escape(old_name)})(</h2>)',
            rf'\g<1>{new_name}\g<3>',
            content,
            flags=re.IGNORECASE
        )
        # Dans les liens du menu
        content = re.sub(
            rf'(<a[^>]*>)({re.escape(old_name)})(</a>)',
            rf'\g<1>{new_name}\g<3>',
            content,
            flags=re.IGNORECASE
        )
    
    # 2. Remplacer la fonction showCard par la version complète avec icônes
    # Pattern pour trouver la fonction showCard existante
    pattern = r'function showCard\(index\) \{[\s\S]*?\n\}\n\nshowCard\(currentIndex\);'
    
    if re.search(pattern, content):
        content = re.sub(
            pattern,
            JS_SHOW_CARD_WITH_ICONS + '\n\nshowCard(currentIndex);',
            content
        )
    
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

def fix_menu_names_globally():
    """Corrige les noms dans le menu de tous les fichiers."""
    for root, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            
            filepath = Path(root) / filename
            content = filepath.read_text(encoding='utf-8')
            original = content
            
            for old_name, new_name in NAME_CORRECTIONS.items():
                content = re.sub(
                    rf'(<a[^>]*>)({re.escape(old_name)})(</a>)',
                    rf'\g<1>{new_name}\g<3>',
                    content,
                    flags=re.IGNORECASE
                )
            
            if content != original:
                filepath.write_text(content, encoding='utf-8')

def main():
    fixed_count = 0
    
    # Corriger tous les fichiers de cours
    for root, dirs, files in os.walk(USPN_S2_ROOT):
        for filename in files:
            if not filename.endswith('.html'):
                continue
            if filename in ('index.html', 'favorites.html'):
                continue
            
            filepath = Path(root) / filename
            print(f"Traitement de {filepath.relative_to(ROOT)}...")
            
            if fix_course_file(filepath):
                fixed_count += 1
                print(f"  ✓ Corrigé")
            else:
                print(f"  - Pas de changement")
    
    # Corriger les noms dans les menus de tous les fichiers (y compris index et favorites)
    print("\nCorrection des menus...")
    fix_menu_names_globally()
    
    print(f"\n=== Résumé ===")
    print(f"Fichiers de cours corrigés: {fixed_count}")

if __name__ == "__main__":
    main()
