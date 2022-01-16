#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops


def add_mark(imagePath, mark, out, quality):
    '''
    添加水印，然后保存图片
    '''
    im = Image.open(imagePath)

    image = mark(im)
    name = os.path.basename(imagePath)
    if image:
        new_name = out
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name, quality=quality)

        print(name + " Success.")
    else:
        print(name + " Failed.")


def set_opacity(im, opacity):
    '''
    设置水印透明度
    '''
    assert opacity >= 0 and opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def crop_image(im):
    '''裁剪图片边缘空白'''
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    del bg
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def gen_mark(font_height_crop, mark, size, color, font_family, opacity, space, angle):
    '''
    生成mark图片，返回添加水印的函数
    '''
    # 字体宽度、高度
    is_height_crop_float = '.' in font_height_crop  # not good but work
    width = len(mark) * size
    if is_height_crop_float:
        height = round(size * float(font_height_crop))
    else:
        height = int(font_height_crop)

    # 创建水印图片(宽度、高度)
    mark_ = Image.new(mode='RGBA', size=(width, height))

    # 生成文字
    draw_table = ImageDraw.Draw(im=mark_)
    draw_table.text(xy=(0, 0),
                    text=mark,
                    fill=color,
                    font=ImageFont.truetype(font_family, size=size))
    del draw_table

    # 裁剪空白
    mark_ = crop_image(mark_)

    # 透明度
    set_opacity(mark_, opacity)

    def mark_im(im):
        ''' 在im图片上添加水印 im为打开的原图'''

        # 计算斜边长度
        c = int(math.sqrt(im.size[0] * im.size[0] + im.size[1] * im.size[1]))

        # 以斜边长度为宽高创建大图（旋转后大图才足以覆盖原图）
        mark2 = Image.new(mode='RGBA', size=(c, c))

        # 在大图上生成水印文字，此处mark为上面生成的水印图片
        y, idx = 0, 0
        while y < c:
            # 制造x坐标错位
            x = -int((mark_.size[0] + space) * 0.5 * idx)
            idx = (idx + 1) % 2

            while x < c:
                # 在该位置粘贴mark水印图片
                mark2.paste(mark_, (x, y))
                x = x + mark_.size[0] + space
            y = y + mark_.size[1] + space

        # 将大图旋转一定角度
        mark2 = mark2.rotate(angle)

        # 在原图上添加大图水印
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2,  # 大图
                 (int((im.size[0] - c) / 2), int((im.size[1] - c) / 2)),  # 坐标
                 mask=mark2.split()[3])
        del mark2
        return im

    return mark_im

def marker(file,mark,out,
        color="#dddddd",
        space=200,
        angle=30,
        font_family="arial.ttf",
        font_height_crop="1.2",
        size=50,
        opacity=0.05,
        quality=80):
    marker = gen_mark(font_height_crop, mark, size, color, font_family, opacity, space, angle)
    add_mark(file, marker, out, quality)

if __name__ == '__main__':
    marker('simple.jpg','QTechCode','test.jpg')