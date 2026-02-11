#!/usr/bin/env python3
"""
Script pour corriger le CSS des pages de flashcards USPN_S2
en copiant le CSS complet des pages SU_S2 qui fonctionnent.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USPN_S2_ROOT = ROOT / "USPN_S2"

# CSS complet copié de SU_S2/SHS/outils_pratiques_numeriques.html
FULL_CSS = """<style>  /* Header minimal avec contrôles accessibles */
  #header {
    padding: 1rem 0;
    margin-bottom: 0.5rem;
  }

  /* Section contenu compacte en 2 colonnes */
  header.main {
    margin-top: 1.5rem !important;
    margin-bottom: 0.8rem !important;
    padding-bottom: 0.5rem !important;
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  header.main .header-left h1,
  header.main .header-left h2 {
    flex: 1;
    margin: 0 !important;
  }
  
  header.main h1 {
    font-size: 2em !important;
    line-height: 1.3 !important;
  }
  
  header.main h2 {
    font-size: 1.3em !important;
    color: #7f888f !important;
  }
  header.main .header-left {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  header.main .header-left h1,
  header.main .header-left h2 {
    margin: 0 !important;
  }

  .image.main {
    flex: 1;
    max-height: none !important;
    overflow: visible !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .image.main img {
    width: 100% !important;
    height: auto !important;
    max-height: 120px !important;
    object-fit: contain !important;
    object-position: center;
  }
  
  section {
    padding-top: 0 !important;
  }

  /* Barre de progression cohérente */
  .progress-container {
    width: 100%;
    max-width: 1000px;
    height: 20px;
    background-color: #eee;
    border-radius: 10px;
    overflow: hidden;
    margin: 0 auto 1rem;
    border: 1px solid #ddd;
  }

  .progress-bar {
    height: 100%;
    background-color: #00aeef;
    width: 0%;
    transition: width 0.3s;
  }

  /* Flashcards plein écran optimisées */
  .flashcards-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    min-height: calc(100vh - 250px);
    padding: 1rem 0;
  }

  .flashcard {
    width: 100%;
    max-width: 1000px;
    height: calc(100vh - 340px);
    min-height: 450px;
    perspective: 1500px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
    background-color: white;
    transition: transform 0.6s;
    overflow: visible;
    transform-style: preserve-3d;
  }

  .flashcard.show-answer .flashcard-inner {
    transform: rotateY(180deg);
  }

  .flashcard-front,
  .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    backface-visibility: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    font-size: 2rem;
    text-align: center;
  }

  .flashcard-front {
    background-color: white;
    color: #333;
    box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15);
  }

  .flashcard-back {
    background-color: #73C3EC;
    color: white;
    overflow: visible;
    transform: rotateY(180deg);
    box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5);
    font-size: 2.2rem;
    text-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
  }

  .flashcard-button {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    width: 100%;
    flex-wrap: wrap;
  }

  /* Boutons repositionnés DANS flashcard-inner */
  .check-icon,
  .cross-icon,
  .favorite-icon {
    display: none;
    position: absolute;
    cursor: pointer;
    z-index: 1000;
    transition: all 0.3s;
    opacity: 0.8;
    pointer-events: auto;
  }

  .check-icon {
    top: 30px;
    left: 30px;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    overflow: visible;
    z-index: 1001;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50%;
    padding: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: all 0.3s;
    color: #888;
    font-size: 20px;
  }

  .check-icon i {
    pointer-events: none;
    transform: scaleX(-1);
  }

  .cross-icon {
    top: 30px;
    right: 30px;
    stroke: #888;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    overflow: visible;
    z-index: 1001;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50%;
    padding: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: all 0.3s;
  }

  body.dark-mode .check-icon,
  body.dark-mode .cross-icon {
    background: rgba(50, 50, 50, 0.95);
    color: #fff;
    stroke: #fff;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.5);
  }

  body.dark-mode .check-icon:hover {
    background: rgba(40, 150, 40, 0.95);
    color: #fff;
  }

  body.dark-mode .cross-icon:hover {
    background: rgba(150, 40, 40, 0.95);
    stroke: #fff;
  }

  .favorite-icon {
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    fill: #888;
    width: 30px;
    height: 30px;
  }

  .favorite-icon.active {
    fill: #ffd700;
  }

  .flashcard.show-answer .check-icon,
  .flashcard.show-answer .cross-icon,
  .flashcard.show-answer .favorite-icon {
    display: flex !important;
  }

  .check-icon:hover {
    stroke: #27ae60;
    color: #27ae60;
    opacity: 1;
  }

  .cross-icon:hover {
    stroke: #e74c3c;
    opacity: 1;
  }

  .favorite-icon:hover {
    opacity: 1;
    transform: translateX(-50%) scale(1.1);
  }

  .slide-left {
    animation: slideLeft 0.4s forwards;
  }

  .slide-right {
    animation: slideRight 0.4s forwards;
  }

  @keyframes slideLeft {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(-100%);
      opacity: 0;
    }
  }

  @keyframes slideRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }

  /* Dark mode support */
  body.dark-mode .flashcard-front {
    background-color: #2d3436;
    color: #e2e8f0;
  }

  body.dark-mode .flashcard-inner {
    background-color: #2d3436;
  }

  body.dark-mode .progress-container {
    background-color: #34495e;
    border-color: #4a5568;
  }

  @media screen and (max-width: 768px) {
    .flashcard {
      width: 95vw;
      height: calc(100vh - 180px);
      min-height: 450px;
    }
    
    ul.actions {
      padding-right: 0;
      text-align: center;
    }
  }
</style>"""

def fix_course_file(filepath: Path):
    """Remplace le bloc <style> existant par le CSS complet."""
    content = filepath.read_text(encoding='utf-8')
    
    # Pattern pour trouver le bloc style existant
    # Le style est entre </header> (de header.main) et <div class="progress-container">
    pattern = r'(<header class="main">.*?</header>\s*)\n<style>.*?</style>'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(
            pattern,
            r'\1\n' + FULL_CSS,
            content,
            flags=re.DOTALL
        )
        filepath.write_text(new_content, encoding='utf-8')
        return True
    else:
        print(f"  Pattern non trouvé dans {filepath}")
        return False

def main():
    fixed_count = 0
    error_count = 0
    
    # Parcourir tous les fichiers HTML dans USPN_S2 (sauf index et favorites)
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
                error_count += 1
    
    print(f"\n=== Résumé ===")
    print(f"Fichiers corrigés: {fixed_count}")
    print(f"Erreurs: {error_count}")

if __name__ == "__main__":
    main()
