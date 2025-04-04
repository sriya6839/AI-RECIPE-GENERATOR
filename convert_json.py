
import fitz  
import json
import re

def extract_recipes_from_pdf(pdf_path, output_json_path, start_page=6):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_number in range(start_page, len(doc)):
            page = doc.load_page(page_number)
            text += page.get_text() + "\n"
        print(" PDF text extracted successfully.")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return

    lines = text.split("\n")

    recipes = []
    current_recipe = None
    collecting_ingredients = False
    collecting_method = False

    for i in range(len(lines)):
        line = lines[i].strip()

        if not line:
            continue

     
        if (
            i + 1 < len(lines)
            and re.match(r"(?i)^ingredients[:\s]*$", lines[i + 1].strip())
            and not re.match(r"(?i)^(ingredients|method)[:\s]*$", line)
        ):
            if current_recipe:
                recipes.append(current_recipe)

            current_recipe = {"name": line, "Ingredients": [], "METHOD": []}
            collecting_ingredients = False
            collecting_method = False
            continue

        if re.match(r"(?i)^ingredients[:\s]*$", line):
            collecting_ingredients = True
            collecting_method = False
            continue

        if re.match(r"(?i)^method[:\s]*$", line):
            collecting_method = True
            collecting_ingredients = False
            continue

       
        if current_recipe:
            if collecting_ingredients:
                current_recipe["Ingredients"].append(line)
            elif collecting_method:
                steps=re.split(r'\.\s*',line)
                for step in steps:
                    clean_step=step.strip()
                    if clean_step:
                        current_recipe["METHOD"].append(clean_step + ".")
                

  
    if current_recipe and current_recipe.get("name"):
        recipes.append(current_recipe)

   
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(recipes, f, indent=4, ensure_ascii=False)
        print(f" {len(recipes)} recipes saved to '{output_json_path}'")
    except Exception as e:
        print(f" Error saving JSON: {e}")


extract_recipes_from_pdf("IndianRecipes.pdf", "recipes.json", start_page=6)