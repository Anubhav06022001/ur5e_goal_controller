from setuptools import find_packages, setup

package_name = 'ur5e_goal_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='anubhav',
    maintainer_email='anubhav96022@gmail.com',
    description='ROS 2 controller for commanding a UR5e end effector to a user-specified pose using MoveIt inverse kinematics.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'move_ur5e = ur5e_goal_controller.move_ur5e:main',
        ],
    },
)
