## low dim setup
Input: cube orientations (T, 12), cube positions (T, 9), eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2), joint pos (T, 9), joint vel (T, 9) => (T, 48)

Output: actions (T, 7)

## low dim result
<img width="690" height="525" alt="image" src="https://github.com/user-attachments/assets/fd2511dd-fa99-44af-b9f8-877e9d5aa4f5" />
<img width="682" height="525" alt="image" src="https://github.com/user-attachments/assets/2ce0c8d5-c097-4560-8204-526fba33359d" />

## RGB setup
Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / table cam (T, 3, 84, 84), wrist cam (T, 3, 84, 84)

Output: actions (T, 7)

전체 table 구성, wrist cam RGB, table cam RGB

<img width="525" height="400" alt="image" src="https://github.com/user-attachments/assets/6b2e5214-ebfb-4379-a176-82d94e6aeb69" />
<img width="533" height="400" alt="image" src="https://github.com/user-attachments/assets/15490179-d4c6-4642-a3d8-124731640603" />
<img width="399" height="400" alt="image" src="https://github.com/user-attachments/assets/2226ae64-88d7-41d1-80e9-485af9a3baf6" />

## RGB result
<img width="400" height="400" alt="RGB1" src="https://github.com/user-attachments/assets/a47ba413-de84-41fe-bf8a-f1ce45cc9329" />
<img width="400" height="400" alt="RGB2" src="https://github.com/user-attachments/assets/899fd666-6410-4274-8729-54c357e30901" />
<img width="400" height="400" alt="RGB3" src="https://github.com/user-attachments/assets/017c7e46-afff-43b1-a977-f12fdd0f8c49" />

## RGBD setup
Input: eef pos (T, 3), eef quat (T, 4), gripper pos (T, 2) => (T, 9) / table cam (T, 4, 84, 84), wrist cam (T, 4, 84, 84)

Output: actions (T, 7)

<img width="641" height="480" alt="image" src="https://github.com/user-attachments/assets/65f4e1f9-d66e-48d5-b793-d2027c73e0bc" />
<img width="641" height="480" alt="image" src="https://github.com/user-attachments/assets/5f42ecdc-a561-40eb-b559-335bcc905212" />

## RGBD result
<img width="400" height="400" alt="RGBD1" src="https://github.com/user-attachments/assets/5118cdab-297e-4eeb-a66b-89e770dd7bcd" />
<img width="400" height="400" alt="RGBD2" src="https://github.com/user-attachments/assets/5ac961c2-5ebd-43f9-a5ec-d7ed3fba8ef1" />
<img width="400" height="400" alt="RGBD3" src="https://github.com/user-attachments/assets/4653a4db-4f8b-4180-9010-c650c250f482" />
<img width="400" height="400" alt="RGBD4" src="https://github.com/user-attachments/assets/6cbcb630-215e-453d-ac9e-4781136bce6b" />
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



