from setuptools  import find_packages, setup

setup(

    name='mcqgenerator',
    version='0.0.1',
    author='udara madhushan',
    install_requires = ['openai', 'langchain', 'streamlit', 'python-dotenv', 'PyPDF2'],
    packages=find_packages('src'),
    package_dir={'': 'src'},


)