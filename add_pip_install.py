import json
import os
from datetime import datetime


def add_install_cell_to_notebook(notebook_path, output_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    new_cell_content = ["!pip install splink"]
    if "spark" in notebook_path:
        new_cell_content.append("\n!pip install pyspark")

    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": new_cell_content,
    }

    notebook["cells"].insert(0, new_cell)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=4)


def generate_colab_link(notebook_path):
    github_repo = "moj-analytical-services/splink_colab_links"
    return f"https://colab.research.google.com/github/{github_repo}/blob/main/{notebook_path}"


def process_directory(directory, base_directory):
    colab_links = {}
    for root, dirs, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)
        ipynb_files = [
            f
            for f in files
            if f.endswith(".ipynb") and "athena" not in relative_path.lower()
        ]

        if ipynb_files:
            colab_links[relative_path] = []
            for file in ipynb_files:
                notebook_path = os.path.join(root, file)
                output_path = notebook_path.replace(base_directory + "/", "")
                add_install_cell_to_notebook(notebook_path, output_path)

                colab_link = generate_colab_link(output_path)
                link_text = (
                    os.path.splitext(os.path.basename(file))[0]
                    .replace("_", " ")
                    .capitalize()
                )
                colab_links[relative_path].append(f"[{link_text}]({colab_link})")

    with open("links.md", "w", encoding="utf-8") as f:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Last updated: {current_datetime}\n\n")
        for directory, links in colab_links.items():
            if links:
                header_level = directory.count(os.sep) + 2
                f.write(f"{'#' * header_level} {directory}\n\n")
                for link in links:
                    f.write(link + "\n\n")


base_directory = "splink"
process_directory(f"{base_directory}/docs/demos", base_directory)
