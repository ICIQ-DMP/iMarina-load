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
  <a href="[https://github.com/github_username/repo_name](https://github.com/ICIQ-DMP/iMarina-load)">
    <img src="images/logo-ICIQ-horizontal-catalan.png" alt="Logo" width="all" height="all">
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
To start the program them execute this command
```shell
./venv/bin/python src/main.py -- step build

```

<!-- ROADMAP for issues -->
## Roadmap (issues)

- [ ] [#1: Implement awesome README template](https://github.com/ICIQ-DMP/iMarina-load/issues/1) 
- [x] [#2: Finish arguments for flexible location of paths](https://github.com/ICIQ-DMP/iMarina-load/issues/2)
- [ ] [#3: Find out equivalence of job description for personal web](https://github.com/ICIQ-DMP/iMarina-load/issues/3)
- [x] [#4:Configure IP connection over imarina #4 ](https://github.com/ICIQ-DMP/iMarina-load/issues/4)
- [ ] [#5:]()

See the [open issues](https://github.com/ICIQ-DMP/iMarina-load/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome and what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you’d like to report a bug, request a feature, or propose an improvement, please follow these steps:

**Creating an Issue
**
1.Go to the Issues tab
Navigate to the Issues section of the repository.

2.Click on “New Issue”
Press the New Issue button to start creating one.

3.Fill in the details

Title: A short, descriptive summary of the issue.

Description: Provide as much context as possible.

For bugs: steps to reproduce, expected vs. actual behavior, environment (OS, Python version, etc.).

For features: explain the motivation and the expected outcome.

Screenshots or logs (if applicable).

4.Publish the issue
Once completed, click Submit new issue. The maintainers will review it and may ask for further clarification.


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

Mario Piqué - (mpique@iciq.es) [mpique@iciq.es]

Aleix Mariné - (amarine@iciq.es) [amarine@iciq.es]
  


Project Link: [https://github.com/ICIQ-DMP/iMarina-load](https://github.com/github_username/repo_name)

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

[product-screenshot]: images/screenshot.png

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
