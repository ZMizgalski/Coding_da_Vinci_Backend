# Coding_da_Vinci_FrontEnd
> Coding_da_Vinci project website made with Angular

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)
* [License](#license)

## Coding_da_Vinci_Backend
- This project was made for _Coding_da_Vinci_ competition [Link](https://codingdavinci.de/)

## Technologies Used
- Python
- OpenCv

## Features
List the ready features here:
- Ai image mixer
- Flask backend
- Museum database

## Setup
- Install Python 
- Install requirements.txt

## Usage
1. Create a folder named you like.
2. Inside your folder, open console and paste: `git clone https://github.com/ZMizgalski/Coding_da_Vinci_Backend.git`
3. Then you are ready to go just open it in any Editor. (We prefer Pycharm) [Download here](https://www.jetbrains.com/pycharm/)

## Project Status
Project is:  _complete_ .

# Blending algorithm overview:
#### 1. Input are two images.
<div style="display: flex">
  <img src="https://user-images.githubusercontent.com/61599048/164991130-a6e60cd7-7671-4ac8-9c92-01027cb57fca.jpg" style="width: 400px"/>
  <img src ="https://user-images.githubusercontent.com/61599048/164991142-5c165050-c5fd-4026-85c6-955dd43beedf.jpg" style="width: 400px"/>
</div>

#### 2. Both images are slightly zoomed in and threshold operations are performed.
#### 3. Threshold results are combined together.
<img src="https://user-images.githubusercontent.com/61599048/164991229-7bc771f0-5293-43f5-951a-46541e268137.jpg" style="height: 500px"/>

#### 4. Neural style transfer is used (https://github.com/moritztng/prism MIT Licence), color is based on second image.
#### 5. Result after running 50 iteration of style transfer using 800x800 resolution setting.
<img src="https://user-images.githubusercontent.com/61599048/164991363-390933b6-ee94-400a-be3f-b15dde0dc5db.jpg" style="height: 500px"/>  

## Room for Improvement
- Security
- Blending algorithm

## Contact
Created by [@zmizgalski](https://zmizgalski.github.io/), [@krzysztofprogramming](https://krzysztofprogramming.github.io/)


## License
This project is open source and available under the [... License](https://github.com/ZMizgalski/Coding_da_Vinci_Backend/blob/master/LICENSE).
