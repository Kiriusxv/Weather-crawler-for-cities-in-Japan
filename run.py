import sys
import os

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask_app.app import app

if __name__ == '__main__':
    app.run(debug=True)
