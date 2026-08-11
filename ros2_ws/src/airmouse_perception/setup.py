from setuptools import find_packages, setup
import os
from glob import glob

package_name = "airmouse_perception"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="aaryahi",
    maintainer_email="garvitgothwalofficial@gmail.com",
    description="Role 3 — RGB-D person detection via YOLOv8n with temporal confirmation",
    license="MIT",
    entry_points={
        "console_scripts": [
            "detector_node = airmouse_perception.detector_node:main",
        ],
    },
)