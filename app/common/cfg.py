import os
import json

# 文件名
filename = 'cfg.json'


class Config(object):
    def init(self):
        # 检查文件是否存在
        if not os.path.isfile(filename):
            # 如果文件不存在，创建文件并写入默认配置
            default_config = {
                "date": "45",
            }
            with open(filename, 'w') as file:
                json.dump(default_config, file, indent=4)
            print(f"{filename} 创建并写入默认配置。")
        else:
            print(f"{filename} 已经存在。")
