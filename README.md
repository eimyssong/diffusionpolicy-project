## low dim setup
Input: cube orientations (T, 12), cube positions (T, 9), eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2), joint pos (T, 9), joint vel (T, 9) => (T, 48)

Output: actions (T, 7)

## low dim result

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/53781f30-2966-44b3-8c32-3934d1d2652d" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/64a01a92-778c-4b3c-939d-63556c3cfbd9" width="300"></img>
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
      <img src="https://github.com/user-attachments/assets/ffb71ae3-dbb2-408d-bb6c-744e37f30d09" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/a95397ec-91ea-4fd2-998a-b83548feb974" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/abad4416-b1dd-42ac-909c-f44846d3fbf2" width="300"></img>
    </td>
  </tr>
</table>


## RGB result

<img width="300" height="300" alt="RGB1" src="https://github.com/user-attachments/assets/cfb5a3ef-e9ef-40b9-adda-2d206489ac0c" />
<img width="300" height="300" alt="RGB2" src="https://github.com/user-attachments/assets/61011611-b37f-4036-857b-524f736e8aa7" />
<img width="300" height="300" alt="RGB3" src="https://github.com/user-attachments/assets/006f5c20-a886-44db-b9b2-09c3b13648aa" />

## RGBD setup
Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / table cam (T, 4, 84, 84), wrist cam (T, 4, 84, 84)

Output: actions (T, 7)


<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/de6f4bee-6487-4bf3-9658-6205eea7e158" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/6f25c923-3a7a-4e92-bc2e-8b8ed2d9b436" width="300"></img>
    </td>
  </tr>
</table>



## RGBD result
<img width="300" height="300" alt="RGBD1" src="https://github.com/user-attachments/assets/3b1819f5-fe06-49c1-b6a6-7c0ef1929947" />
<img width="300" height="300" alt="RGBD2" src="https://github.com/user-attachments/assets/5017f5c5-6d5b-40b4-9535-245722dc1db6" />
<img width="300" height="300" alt="RGBD3" src="https://github.com/user-attachments/assets/60beae7c-1adf-415f-b36c-082fedb1c1cd" />
<img width="300" height="300" alt="RGBD4" src="https://github.com/user-attachments/assets/6720800b-b5a5-4ad0-b778-50f49be4907f" />
<img width="577" height="304" alt="image" src="https://github.com/user-attachments/assets/1a514919-eb84-4873-9384-ab6fc5e7a999" />

## DP3 setup
Point cloud, no color

Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / point cloud (T, 2048, 6)

Output: actions (T, 7)

<img width="400" height="400" alt="pointcloud" src="https://github.com/user-attachments/assets/f18c3f74-75cf-4fe6-96a4-bac3ae449687" />

## DP3, no color result
<img width="400" height="200" alt="dp3,nocolor1" src="https://github.com/user-attachments/assets/71c7b1ae-dae7-4652-8341-8d7c436a760e" />
<img width="400" height="200" alt="dp3,nocolor2" src="https://github.com/user-attachments/assets/c697bd78-45f4-4d2f-b3ad-f3eb8b61097b" />
<img width="400" height="200" alt="dp3,nocolor3" src="https://github.com/user-attachments/assets/c2ffc3c9-2e04-4ceb-9cf1-121e67e236a4" />
<img width="400" height="200" alt="dp3,nocolor4" src="https://github.com/user-attachments/assets/4a3b36a7-5e0b-4fae-8387-f374d192c4cd" />

## DP3, use color result
<img width="400" height="200" alt="dp3,color1" src="https://github.com/user-attachments/assets/724d7155-963b-4771-8edf-4f4520003674" />
<img width="400" height="200" alt="dp3,color2" src="https://github.com/user-attachments/assets/a60e4437-07b1-4e13-95e5-b396e707ff7e" />
<img width="400" height="200" alt="dp3,color3" src="https://github.com/user-attachments/assets/b005de55-7fd9-423f-982c-de98ed222aa0" />
<img width="400" height="200" alt="dp3,color4" src="https://github.com/user-attachments/assets/554bb06d-d697-414e-b2ab-a3deb851f955" />



## Lab Seminar

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

```
@article{chi2024diffusionpolicy,
	author = {Cheng Chi and Zhenjia Xu and Siyuan Feng and Eric Cousineau and Yilun Du and Benjamin Burchfiel and Russ Tedrake and Shuran Song},
	title ={Diffusion Policy: Visuomotor Policy Learning via Action Diffusion},
	journal = {The International Journal of Robotics Research},
	year = {2024},
}
```

```
@inproceedings{Ze2024DP3,
	title={3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations},
	author={Yanjie Ze and Gu Zhang and Kangning Zhang and Chenyuan Hu and Muhan Wang and Huazhe Xu},
	booktitle={Proceedings of Robotics: Science and Systems (RSS)},
	year={2024}
}
```
