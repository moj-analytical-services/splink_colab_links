import json
import os


def add_install_cell_to_notebook(notebook_path, output_path):
    # Load the notebook as JSON
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Define the new cell
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": ["!pip install splink"],
    }

    # Insert the new cell at the beginning of the notebook
    notebook["cells"].insert(0, new_cell)

    # Save the modified notebook
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
        ipynb_files = [f for f in files if f.endswith(".ipynb")]

        if ipynb_files:
            colab_links[relative_path] = []
            for file in ipynb_files:
                notebook_path = os.path.join(root, file)
                output_path = notebook_path.replace(base_directory + "/", "")
                add_install_cell_to_notebook(notebook_path, output_path)

                # Generate and store the Colab link
                colab_link = generate_colab_link(output_path)
                link_text = (
                    os.path.splitext(os.path.basename(file))[0]
                    .replace("_", " ")
                    .capitalize()
                )
                colab_links[relative_path].append(f"[{link_text}]({colab_link})")

    # Write the links to links.md
    with open("links.md", "w", encoding="utf-8") as f:
        for directory, links in colab_links.items():
            if links:
                header_level = directory.count(os.sep) + 2
                f.write(f"{'#' * header_level} {directory}\n\n")
                for link in links:
                    f.write(link + "\n\n")


base_directory = "splink"
process_directory(f"{base_directory}/docs/demos", base_directory)
