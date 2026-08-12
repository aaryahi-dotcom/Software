from setuptools import find_packages, setup

package_name = 'airmouse_autonomy'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Harshita Joshi',
    maintainer_email='hiyaj8323@gmail.com',
    description='Autonomous exploration and mission management',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mission_manager = airmouse_autonomy.mission_manager:main',
            'frontier_explorer = airmouse_autonomy.frontier_explorer:main',
            'return_to_entry = airmouse_autonomy.return_to_entry:main',
        ],
    },
)
