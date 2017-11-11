from setuptools import setup, find_packages

setup(
    name='openweathermap-mqtt',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='https://github.com/larsks/openweathermap-mqtt',
    packages=find_packages(),
    install_requires=[
        'requests',
        'paho_mqtt',
    ],
    entry_points={
        'console_scripts': [
            'owm-export-mqtt = owm_mqtt.main:main',
        ],
    }
)
