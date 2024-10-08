# zh_recogn 识别
from typing import Union, List, Dict

import requests

from videotrans.configure import config
from videotrans.configure._except import LogExcept
from videotrans.recognition._base import BaseRecogn
from videotrans.util import tools


class ZhRecogn(BaseRecogn):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        api_url = config.params['zh_recogn_api'].strip().rstrip('/').lower()
        if not api_url:
            raise LogExcept('必须填写地址')
        if not api_url.startswith('http'):
            api_url = f'http://{api_url}'
        if not api_url.endswith('/api'):
            api_url += '/api'
        self.api_url = api_url

    def _exec(self) -> Union[List[Dict], None]:
        if self._exit():
            return
        files = {"audio": open(self.audio_file, 'rb')}
        self._signal(text=f"识别可能较久，请耐心等待，进度可查看zh_recogn终端")
        try:
            res = requests.post(f"{self.api_url}", files=files, proxies={"http": "", "https": ""}, timeout=3600)
            config.logger.info(f'zh_recogn:{res=}')
            res = res.json()
            if "code" not in res or res['code'] != 0:
                raise LogExcept(f'{res["msg"]}')
            if "data" not in res or len(res['data']) < 1:
                raise LogExcept(f'识别出错{res=}')
            return res['data']
        except Exception as e:
            raise