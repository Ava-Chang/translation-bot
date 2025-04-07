import os
from flask import Flask, request, jsonify, abort
import logging
from services.line_service import LineService
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

server_port = int(os.getenv('PORT'))


# add logging with level INFO and Debug and Error
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    line_service = LineService()
except ValueError as e:
    logger.error(f"初始化 LineService 失敗: {e}")
    raise


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route("/callback", methods=['POST'])
def callback():
    logger.info("=== 開始處理 webhook 請求 ===")
    logger.info(f"請求方法: {request.method}")
    logger.info(f"Content-Type: {request.headers.get('Content-Type')}")
    logger.info(f"X-Line-Signature: {request.headers.get('X-Line-Signature')}")
    
    # 獲取 X-Line-Signature header
    if 'X-Line-Signature' not in request.headers:
        logger.error("缺少 X-Line-Signature")
        abort(400)
        
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logger.info(f"Request body: {body}")
    
    try:
        line_service.handler.handle(body, signature)
        logger.debug("webhook 處理完成")
    except InvalidSignatureError as e:
        logger.error(f"簽名驗證失敗: {e}")
        abort(400)
    except Exception as e:
        logger.error(f"處理 webhook 時發生錯誤: {e}", exc_info=True)
        abort(500)
    
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_port)