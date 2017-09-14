#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
import sys
from config import Config
reload(sys)
sys.setdefaultencoding('utf8')

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6210,threaded=True,debug=Config.DEBUG)
