import fnmatch
import os
import shutil
import subprocess


def matches_pattern(file_name, pattern):
    return fnmatch.fnmatch(file_name, pattern)


def remove_unnecessary_files(directory):
    patterns_to_remove = [
        "*.dist-info",
        "*.egg-info",
        "tests",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "_distutils_hack",  # Non essential
        "README.txt",  # Non essential
        "distutils-precedence.pth",  # Non essential
        "pip",  # Optional
        "setuptools",  # Optional
        "wheel",  # Optional
        "pkg_resources",  # Optional
    ]
    # Optionals
    is_necessary_setuptools = input("Se usará setuptools? (y/n) ")
    if is_necessary_setuptools == "y":
        patterns_to_remove.remove("setuptools")
    is_necessary_wheel = input("Se usará wheel? (y/n) ")

    if is_necessary_wheel == "y":
        patterns_to_remove.remove("wheel")
    is_necessary_pkg_resources = input("Se usará pkg_resources? (y/n) ")

    if is_necessary_pkg_resources == "y":
        patterns_to_remove.remove("pkg_resources")
    # Remove unnecessary files

    for root, dirs, files in os.walk(directory):
        for pattern in patterns_to_remove:
            for dir_name in dirs:
                if matches_pattern(dir_name, pattern):
                    shutil.rmtree(os.path.join(root, dir_name), ignore_errors=True)
            for file_name in files:
                if pattern in file_name:
                    os.remove(os.path.join(root, file_name))


def create_layer(layer_name, requirements_file):
    # Step 1: Create a project directory for the layer
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file_abs = os.path.join(current_dir, requirements_file)

    project_dir = layer_name
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)

    # Step 2: Copy the requirements.txt file to the project directory
    shutil.copy(requirements_file_abs, "requirements.txt")

    # Step 3: Install dependencies in a minimal environment using Docker
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/lambda-layer",
            "-w",
            "/lambda-layer",
            "lambci/lambda:build-python3.11",
            "pip",
            "install",
            "-r",
            "requirements.txt",
            "-t",
            "python",
        ],
        check=True,
    )

    # Step 4: Remove unnecessary files

    remove_unnecessary_files("python")

    # Step 5: Compress the layer
    shutil.make_archive("layer", "zip", "python")

    # Step 6: Upload the layer to AWS Lambda (commented out for security, ensure AWS CLI is configured)
    # subprocess.run([
    #     'aws', 'lambda', 'publish-layer-version',
    #     '--layer-name', layer_name,
    #     '--zip-file', 'fileb://layer.zip'
    # ], check=True)

    print(f"Lambda layer '{layer_name}' created successfully!")

    # Step 7: Clean up and move back to the parent directory
    os.chdir("..")
    shutil.rmtree(project_dir)


if __name__ == "__main__":
    # Layer 1: PyMySQL and scipy
    # create_layer("pymysql_scipy_layer", "requirements_full.txt")
    remove_unnecessary_files("./site-packages")

    # Layer 2: matplotlib
    # screate_layer("matplotlib_layer", "requirements_matplotlib.txt")
