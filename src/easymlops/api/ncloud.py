import base64
import hashlib
import hmac
import os
import requests
import sys
import time

from easymlops import constants as C

class NCloudAPI(object):
    NKS_HOST = "https://nks.apigw.ntruss.com"

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def get_timestamp(self):
        return str(int(time.time() * 1000))

    def assemble_message(self, method, uri, timestamp):
        return method + " " + uri + "\n" + timestamp + "\n" + self.access_key

    def sign(self, msg):
        msg = bytes(msg, 'UTF-8')
        key = bytes(self.secret_key, 'UTF-8')
        return base64.b64encode(hmac.new(key, msg, digestmod=hashlib.sha256).digest())

    def common_header(self, timestamp, signature):
        return {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signature
        }

    def cluster_listing(self):
        uri = "/vnks/v2/clusters"
        ts = self.get_timestamp()
        msg = self.assemble_message("GET", uri, ts)
        signature = self.sign(msg)
        http_header = self.common_header(ts, signature)
        response = requests.get(self.NKS_HOST + uri, headers=http_header)
        print(response.text)

api = NCloudAPI(
    C.config.get_config_value("NCLOUD_ACCESS_KEY"),
    C.config.get_config_value("NCLOUD_SECRET_KEY")
)
api.cluster_listing()
