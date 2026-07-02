<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/03004fbd-ce52-49b4-be6d-a54b6bfd7a3b" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/1ecf7441-7b8b-4991-858b-af5295ae5eb0" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/b564f09b-8903-4c58-bc94-209a86257732" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/d2d49e1b-545c-41d1-994c-9a8f2a8dc752" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/13b2e703-b6f1-4105-bb75-08c535cd6c9f" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/a31c3031-2c76-4030-b8ee-746c04bce508" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/ea79ea5d-b7ea-4bdb-8c3f-a07f4d1bc338" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/d0b691f4-46d1-4221-860b-58818b5f0251" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/cb2cc920-b761-4b67-92ef-50abc51dc604" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/84c201f8-e849-4484-98e4-098a0e07a18b" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/8276e414-77a0-4a44-a434-a0c5cc8dfd33" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/dedf79d9-223b-4406-930e-a9074ef32a74" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/f269cc67-c0a5-4f3e-9a3e-5706056db9de" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/3763c969-62db-431b-8d2e-35bff418b544" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/1169abdd-948a-4e09-bb45-ded0e8196e79" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/86afa0cb-8c59-4f9b-b3d0-2d222937fc2d" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/9da5e657-b452-42a8-84fd-10e55d823143" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/8c457064-b3ca-48f9-94b0-1522cb48f2f0" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/b30eab8a-7fd5-4c22-bec3-f1f40c7dd56a" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/e0e0aaaa-99ce-4246-9794-c0d387720564" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/a41b4e01-4bb2-42ac-8271-d700cb51a05e" />
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/b752f202-259e-4351-9a40-492e62c96785" />



## low dim setup
Input: cube orientations (T, 12), cube positions (T, 9), eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2), joint pos (T, 9), joint vel (T, 9) => (T, 48)

Output: actions (T, 7)

## low dim result

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/fd2511dd-fa99-44af-b9f8-877e9d5aa4f5" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/2ce0c8d5-c097-4560-8204-526fba33359d" width="300"></img>
    </td>
  </tr>
</table>


## RGB setup
Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / table cam (T, 3, 84, 84), wrist cam (T, 3, 84, 84)

Output: actions (T, 7)

전체 table 구성, wrist cam RGB, table cam RGB


<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/6b2e5214-ebfb-4379-a176-82d94e6aeb69" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/15490179-d4c6-4642-a3d8-124731640603" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/2226ae64-88d7-41d1-80e9-485af9a3baf6" width="300"></img>
    </td>
  </tr>
</table>


## RGB result

<img width="300" height="300" alt="RGB1" src="https://github.com/user-attachments/assets/a47ba413-de84-41fe-bf8a-f1ce45cc9329" />
<img width="300" height="300" alt="RGB2" src="https://github.com/user-attachments/assets/899fd666-6410-4274-8729-54c357e30901" />
<img width="300" height="300" alt="RGB3" src="https://github.com/user-attachments/assets/017c7e46-afff-43b1-a977-f12fdd0f8c49" />

## RGBD setup
Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / table cam (T, 4, 84, 84), wrist cam (T, 4, 84, 84)

Output: actions (T, 7)


<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/65f4e1f9-d66e-48d5-b793-d2027c73e0bc" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/5f42ecdc-a561-40eb-b559-335bcc905212" width="300"></img>
    </td>
  </tr>
</table>



## RGBD result
<img width="300" height="300" alt="RGBD1" src="https://github.com/user-attachments/assets/5118cdab-297e-4eeb-a66b-89e770dd7bcd" />
<img width="300" height="300" alt="RGBD2" src="https://github.com/user-attachments/assets/5ac961c2-5ebd-43f9-a5ec-d7ed3fba8ef1" />
<img width="300" height="300" alt="RGBD3" src="https://github.com/user-attachments/assets/4653a4db-4f8b-4180-9010-c650c250f482" />
<img width="300" height="300" alt="RGBD4" src="https://github.com/user-attachments/assets/6cbcb630-215e-453d-ac9e-4781136bce6b" />
<img width="577" height="304" alt="image" src="https://github.com/user-attachments/assets/af8a3fe9-7e09-409e-9070-365a120dad18" />

## DP3 setup
Point cloud, no color

Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / point cloud (T, 2048, 6)

Output: actions (T, 7)

<img width="400" height="400" alt="pointcloud" src="https://github.com/user-attachments/assets/ff32f7f2-19c1-4c9d-8876-464e843fcb4f" />

## DP3, no color result
<img width="400" height="200" alt="dp3,nocolor1" src="https://github.com/user-attachments/assets/4811b680-c805-4e3e-81c8-278e312c2aa4" />
<img width="400" height="200" alt="dp3,nocolor2" src="https://github.com/user-attachments/assets/733dd35b-0fde-4e8e-9b4c-01beb63016c4" />
<img width="400" height="200" alt="dp3,nocolor3" src="https://github.com/user-attachments/assets/817cb098-905f-4b9f-a697-ec9ba51fff9b" />
<img width="400" height="200" alt="dp3,nocolor4" src="https://github.com/user-attachments/assets/642c1eac-fd9e-49d4-9a0d-b748300b3f2e" />

## DP3, use color result
<img width="400" height="200" alt="dp3,color1" src="https://github.com/user-attachments/assets/a8a7c9b8-94a4-40c4-99d4-1f994a070d6d" />
<img width="400" height="200" alt="dp3,color2" src="https://github.com/user-attachments/assets/e4a5203d-1a29-4b5f-be52-64da592dc36e" />
<img width="400" height="200" alt="dp3,color3" src="https://github.com/user-attachments/assets/2562f985-fa88-4e42-b354-ded1dec54c00" />
<img width="400" height="200" alt="dp3,color4" src="https://github.com/user-attachments/assets/de061df8-af81-4ddb-ae7a-a898c63a63f9" />



## Citation
```
@article{mittal2025isaaclab,
  title={Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning},
  author={Mayank Mittal and Pascal Roth and James Tigue and Antoine Richard and Octi Zhang and Peter Du and Antonio Serrano-Muñoz and Xinjie Yao and René Zurbrügg and Nikita Rudin and Lukasz Wawrzyniak and Milad Rakhsha and Alain Denzler and Eric Heiden and Ales Borovicka and Ossama Ahmed and Iretiayo Akinola and Abrar Anwar and Mark T. Carlson and Ji Yuan Feng and Animesh Garg and Renato Gasoto and Lionel Gulich and Yijie Guo and M. Gussert and Alex Hansen and Mihir Kulkarni and Chenran Li and Wei Liu and Viktor Makoviychuk and Grzegorz Malczyk and Hammad Mazhar and Masoud Moghani and Adithyavairavan Murali and Michael Noseworthy and Alexander Poddubny and Nathan Ratliff and Welf Rehberg and Clemens Schwarke and Ritvik Singh and James Latham Smith and Bingjie Tang and Ruchik Thaker and Matthew Trepte and Karl Van Wyk and Fangzhou Yu and Alex Millane and Vikram Ramasamy and Remo Steiner and Sangeeta Subramanian and Clemens Volk and CY Chen and Neel Jawale and Ashwin Varghese Kuruttukulam and Michael A. Lin and Ajay Mandlekar and Karsten Patzwaldt and John Welsh and Huihua Zhao and Fatima Anes and Jean-Francois Lafleche and Nicolas Moënne-Loccoz and Soowan Park and Rob Stepinski and Dirk Van Gelder and Chris Amevor and Jan Carius and Jumyung Chang and Anka He Chen and Pablo de Heras Ciechomski and Gilles Daviet and Mohammad Mohajerani and Julia von Muralt and Viktor Reutskyy and Michael Sauter and Simon Schirm and Eric L. Shi and Pierre Terdiman and Kenny Vilella and Tobias Widmer and Gordon Yeoman and Tiffany Chen and Sergey Grizan and Cathy Li and Lotus Li and Connor Smith and Rafael Wiltz and Kostas Alexis and Yan Chang and David Chu and Linxi "Jim" Fan and Farbod Farshidian and Ankur Handa and Spencer Huang and Marco Hutter and Yashraj Narang and Soha Pouya and Shiwei Sheng and Yuke Zhu and Miles Macklin and Adam Moravanszky and Philipp Reist and Yunrong Guo and David Hoeller and Gavriel State},
  journal={arXiv preprint arXiv:2511.04831},
  year={2025},
  url={https://arxiv.org/abs/2511.04831}
}
```
