#DSPE_2016706018_박건희_11
import numpy as np
from PIL import Image

#이미지 불러오기
with open("Lena(512x512).RGB", 'rb') as fid:
    data_array = np.fromfile(fid, np.uint8,count=512*512*3)

print(data_array.shape)
# 262144 x 3 크기 텐서 생성 및 데이터 입력
RGB = np.zeros(shape=(512 * 512, 3))
for i in range(0, 512 * 512):
 RGB[i][0] = data_array[i]
 RGB[i][1] = data_array[512 * 512 + i]
 RGB[i][2] = data_array[512 * 512 * 2 + i]

#텐서 모양 확인
print(RGB.shape)

# 512 x 512 x 3 텐서 생성 및 데이터 입력
RGB3D = np.zeros(shape=(512, 512, 3))
for i in range(0, 512):
    for j in range(0, 512):
     RGB3D[i][j][0] = RGB[(512 * i) + j][0]
     RGB3D[i][j][1] = RGB[(512 * i) + j][1]
     RGB3D[i][j][2] = RGB[(512 * i) + j][2]

#텐서 모양 확인
print(RGB3D.shape)

#변환된 텐서 JPG 파일로 출력해서 확인
Image.fromarray(RGB3D.astype('uint8'), mode='RGB').save('./RGB3D.png')

#RGB 분할 및 RGBtoYUV 및 YUVtoRGB 계산
RGB3D = RGB3D.transpose(2, 0, 1)

r = RGB3D[0]
g = RGB3D[1]
b = RGB3D[2]

#rgb 와 yuv간 매트릭스 결과
y = ((66 * r + 129 * g + 25 * b + 128) / 256) + 16
cb = ((-38 * r - 74 * g + 112 * b + 128) / 256) + 128
cr = ((112 * r - 94 * g - 18 * b + 128) / 256) + 128
c = y - 16
d = cb - 128
e = cr - 128
r2 = (298 * c + 409 * e + 128) / 256
g2 = (298 * c - 100 * d - 208 * e + 128) / 256
b2 = (298 * c + 516 * d + 128) / 256
#rgb to yuv
RGBtoYUV = np.zeros(shape=(3, 512, 512))

RGBtoYUV[0] = y
RGBtoYUV[1] = cb
RGBtoYUV[2] = cr
#yuv to rgb
YUVtoRGB = np.zeros(shape=(3, 512, 512))

YUVtoRGB[0] = r2
YUVtoRGB[1] = g2
YUVtoRGB[2] = b2
# 텐서 모양 변환 및 출력
RGBtoYUV = RGBtoYUV.transpose(1, 2, 0)
YUVtoRGB = YUVtoRGB.transpose(1, 2, 0)

RGBtoYUV[RGBtoYUV < 0] = 0
RGBtoYUV[RGBtoYUV > 255] = 255

YUVtoRGB[YUVtoRGB < 0] = 0
YUVtoRGB[YUVtoRGB > 255] = 255

print(RGBtoYUV.shape)
print(YUVtoRGB.shape)

Image.fromarray(RGBtoYUV.astype('uint8'), mode='RGB').save('./RGBtoYUV.png')
Image.fromarray(YUVtoRGB.astype('uint8'), mode='RGB').save('./YUVtoRGB.png')