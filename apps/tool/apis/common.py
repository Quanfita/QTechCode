import requests
import base64
import os

class OpenCode:
    # 函数执行超时，例如函数执行 requests 请求超时
    error_50000 = 50000
    # 函数执行错误，一般是未知异常，此时可以打印异常去定位原因
    error_50001 = 50001
    # 函数返回内容不合法，例如请求到的内容不符合返回体结构
    error_50002 = 50002


class OpenApi(OpenCode):
    code = 0
    error = ""
    message = ""
    data = {}

    @property
    def body(self):
        resp = {
            "code": self.code,  # 业务返回码，非0失败
            "error": self.error,  # 错误提示，面向用户
            "message": self.message,  # 错误提示，面向开发者
            "data": self.data  # 返回数据，字典
        }
        return resp

class GiteeImageCloud():
    ACCESS_TOKEN = "9f96d83a7f62b25d1a5c35545476293f"
    OWNER = "Quanfita"
    REPO = "qimage-git"
    BASE_URL = "https://gitee.com/api/v5/repos/{}/{}/contents/{}"

    @staticmethod
    def encode_base64(file):
        with open(file,'rb') as f:
            img_data = f.read()
            base64_data = base64.b64encode(img_data)
            print(type(base64_data))
            #print(base64_data)
            # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
            base64_str = str(base64_data, 'utf-8')
            return base64_data, base64_str

    def uploadImage(self, imagepath, s_type):
        imagename = os.path.basename(imagepath)
        upload_url = self.BASE_URL.format(self.OWNER, self.REPO, s_type+'/'+imagename)
        bs64 = self.encode_base64(imagepath)
        data = {
            "access_token": self.ACCESS_TOKEN,
            "content": bs64,
            "message": 'upload file ' + imagename
        }
        response = requests.post(upload_url, data=data)
        js = response.json()
        print(js)
        return js['content']

if __name__ == '__main__':
    GIC = GiteeImageCloud()
    GIC.uploadImage('qrcode.png','qrcode')
