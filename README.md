<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="[https://github.com/ICIQ-DMP/iMarina-load](https://github.com/ICIQ-DMP/iMarina-load)">
    <img src="https://raw.githubusercontent.com/ICIQ-DMP/ICIQ-DMP.github.io/refs/heads/master/assets/images/logo-ICIQ-horizontal-catalan.png" alt="Logo" width="all" height="all">
  </a>

<h3 align="center">iMarina-load</h3>

  <p align="center">
    Scripts to obtain A3 data, transform it into iMarina load format, and upload it to iMarina server using SFTP
    <br />
    <a href="https://iciq-dmp.github.io/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ICIQ-DMP/iMarina-load">View Demo</a>
    &middot;
    <a href="https://github.com/ICIQ-DMP/iMarina-load/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ICIQ-DMP/iMarina-load/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

 
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#built-with">Built With</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li>
          <a href="#prerequisites">Prerequisites</a>
        </li>
        <li>
          <a href="#installation">Installation</a>
        </li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#roadmap">Roadmap</a>
    </li>
    <li>
      <a href="#contributing">Contributing</a>
    </li>
    <li>
      <a href="#license">License</a>
    </li>
    <li>
      <a href="#contact">Contact</a>
    </li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built with

* [![Python][Python]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
This repo is a project with Python.
Follow these steps to set up the project locally.

### Prerequisites

Install the version python 3.12.3

In my Ubuntu is:

```shell
sudo apt install python3.12-venv gcc build-essential -y
```

### Installation

Clone repository
```shell
git clone https://github.com/ICIQ-DMP/iMarina-load.git

```
Install git if you don't have it
```shell
sudo apt install git -y
```


Initialize venv

```shell
cd iMarina
python3 -m venv venv
./venv/bin/pip install -r requirements.txt 
```
Install the requirements
```shell
pip install --upgrade pip
```
```shell
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage
### Obtaining translations
First you will need to obtain the spreadsheets with the translations. By default, they are read from the `input/` 
folder, but 
you can change the location of these expected files with the following arguments:
* `--imarina-input /path/to/iMarina.xlsx`
* `--a3-input /path/to/A3.xlsx`
* `--countries-dict /path/to/countries.xlsx`
* `--jobs-dict /app/input/Job_Descriptions.xlsx`

You can either download them manually from Sharepoint, or you can use the Dockerized OneDrive service to sync files 
from Sharepoint to your host computer automatically in the background.

To do so you should do the following:
```shell
cd services/onedrive
bash run.sh
# The program will display a link and ask you to authenticate and paste the answered URL into the terminal
```

After following the steps, OneDrive will be syncing the folder 
`Institutional Strengthening/_Projects/iMarina_load_automation/input` from Sharepoint into `services/onedrive/data`. Add 
or change the necessary arguments to read from this new source, instead of `input/`, so that data consumed by the 
program is always updated. 

You can leave OneDrive running so that the files are always in sync. 

There are two configuration options active in `services/onedrive/conf/config` to make OneDrive delete things that have 
been deleted in Sharepoint `cleanup_local_files = "true"` and to only do downloads, not uploads (one-way sync) 
`download_only = "true"`. You may remove these two options to change the behaviour from one-way sync to two-way sync. 



### Executing program
To start the program execute this command:
```shell
./venv/bin/python src/main.py --step build
```

```
sudo docker build . -t aleixmt/imarina-load --progress=plain
```


## Unit Testing by Pytest

### Prerequisites
Install the pytest library for use to create and
run the tests.
```shell
pip install pytest
```

Creating tests:
Test functions are written that begin with test_ in files with the same
name.


Folder test for example test_main.py
All the tests we perform must be stored in this folder called tests.
And the tests folder must be located in the root directory Desktop/iMarina-load.

In the file called test_main.py, you must first import the classes needed for the test
For example:

```python
from datetime import date, datetime

from src.main import Researcher, is_visitor
```

The necessary classes are imported and, above all, the src.main is
important.
Our main is in the src folder.


## Usage Pytest

To use the library correctly and find our tests, we must create the following file and place it in the same root directory as Desktop/iMarina-load.

Create the pytest.ini file

With the following content

``` ini
[pytest]
pythonpath = .
```

Pytest uses the pytest.ini file to define global settings.
The option pythonpath = .
tells pytest to add the project root folder (.) to PYTHONPATH.
This allows Python to find the modules inside src/ without errors.

The test file must be in the project root (same folder as src/ and tests/).

Once this entire process is complete, we save it.


### Executing pytest

We have to be at the root of the project, otherwise we will get an error
```shell
cd ~/Desktop/iMarina-load
```

To ensure that Python sees the project root, you can manually add it to PYTHONPATH
Run this command:

```shell
export PYTHONPATH=$PYTHONPATH:/home/your_usersystem/Desktop/iMarina-load
```

This adds the project path to Python's module “search path.”


### Automation testing
In one command can perform unit testing

Run all the tests at the same time

```shell

pytest -v

```

Display prints or logs during tests

```shell
pytest -s -v
```

Stop at the first fail in the test
```shell
pytest -x

```

Run specific tests for example (by name) 

```shell

pytest -k "name"

```

<!-- ROADMAP for issues -->
## Roadmap (issues)

- [ ] [#3: Find out equivalence of job description for personal web](https://github.com/ICIQ-DMP/iMarina-load/issues/3)
      

See the [open issues](https://github.com/ICIQ-DMP/iMarina-load/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome and what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you’d like to report a bug, request a feature, or propose an improvement, please follow these steps:

**Creating an Issue**

Create a new Issue [in here](https://github.com/ICIQ-DMP/iMarina-load/issues/new).

* Title: A short, descriptive summary of the issue.
* Description: Provide as much context as possible.
* For bugs: steps to reproduce, expected vs. actual behavior, environment (OS, Python version, etc.).
* For features: explain the motivation and the expected outcome.
* Screenshots or logs (if applicable).

The maintainers will review it and may ask for further clarification.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/AleixMT">
   <img src="https://avatars.githubusercontent.com/AleixMT" width="80px" alt="usuario"/>
</a>

<a href="https://github.com/MARIO31XD">
   <img src="https://avatars.githubusercontent.com/MARIO31XD" width="80px" alt="usuario"/>
</a>


<!-- LICENSE -->
## License

Distributed under the GNU GPL v3. See [LICENSE](https://github.com/ICIQ-DMP/iMarina-load/blob/master/LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

* Mario Piqué - [mpique@iciq.es](mpique@iciq.es)
* Aleix Mariné - [amarine@iciq.es](amarine@iciq.es)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

 

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[contributors-url]: https://github.com/ICIQ-DMP/iMarina-load/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[forks-url]: https://github.com/ICIQ-DMP/iMarina-load/forks
[forks-url]: https://img.shields.io/badge/Forks-blue?style=for-the-badge&logo=github&logoColor=white
[stars-shield]: https://img.shields.io/github/stars/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[stars-url]: https://github.com/ICIQ-DMP/iMarina-load/stargazers
[issues-shield]: https://img.shields.io/github/issues/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[issues-url]: https://github.com/ICIQ-DMP/iMarina-load/issues
[issues-url]: https://img.shields.io/badge/Issues-red?style=for-the-badge&logo=github&logoColor=white
[license-shield]: https://img.shields.io/github/license/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[license-url]: https://github.com/ICIQ-DMP/iMarina-load/blob/master/LICENSE

[license-shield]: https://img.shields.io/github/license/ICIQ-DMP/iMarina-load.svg?style=for-the-badge
[license-url]:https://github.com/ICIQ-DMP/iMarina-load/blob/master

[linkedin-shield]: https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://es.linkedin.com/company/iciq

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
