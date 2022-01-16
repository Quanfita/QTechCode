import qrcode
from PIL import Image
import numpy as np
from .common import OpenApi

def Multiply(img1,img2):
	img1 = img1 / 255.0
	img2 = img2 / 255.0
	res = np.multiply(img1,img2)
	res = (res*255).astype(np.uint8)
	return res

def get_qrcode(info):
	qr = qrcode.QRCode(
		version=3,
		error_correction=qrcode.constants.ERROR_CORRECT_Q,
		box_size=10,
		border=4
	)
	qr.add_data(info)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	img = img.convert("RGBA")
	return img

def get_logo_qrcode(info, logo_path):
	img = get_qrcode(info)
	logo = Image.open(logo_path)
	img_w, img_h = img.size
	factor = 4
	size_w = int(img_w / factor)
	size_h = int(img_h / factor)

	logo_w, logo_h = logo.size
	if logo_w > size_w:
		logo_w = size_w
	if logo_h > size_h:
		logo_h = size_h
	logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)

	w = int((img_w - logo_w) / 2)
	h = int((img_h - logo_h) / 2)
	logo = logo.convert("RGBA")
	img.paste(logo, (w, h), logo)
	return img

def get_bg_qrcode(info, bg_path):
	img = get_qrcode(info)
	bg = Image.open(bg_path)
	img = img.convert("RGB")
	img_w, img_h = img.size
	size_w = img_w
	size_h = img_h

	np_img = np.array(img)
	np_mask = 1 - np_img / 255.0

	bg = bg.resize((size_w, size_h), Image.ANTIALIAS)
	bg = bg.convert("RGB")

	np_bg = np.array(bg)

	np_res = Multiply(np_img, np_bg)
	return Image.fromarray(np_res)

def save_qrcode(qr_code, image_name):
	qr_code.save(image_name)
	return image_name

def get_qrcode_return_info(username, info):
	op = OpenApi()
	try:
		qr_code = get_qrcode(info)
		image_name = "simple.png"
		qr_code.save(image_name)
		op.data = {"imgURL":""}
	except Exception as e:
		op.code = op.error_50001
		op.error = "请求错误，未获得词频统计"
		op.message = e
	return op.body

if __name__ == '__main__':
	save_qrcode(get_bg_qrcode("https://quanfita.cn", 'tmp.jpg'), 'bg_qr.png')
	save_qrcode(get_logo_qrcode("https://quanfita.cn", 'tmp.jpg'), 'logo_qr.png')
	save_qrcode(get_qrcode("https://quanfita.cn"), 'qr.png')