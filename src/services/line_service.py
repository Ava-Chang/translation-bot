import os
import logging
from utils.helper import get_prompt_message
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from litellm import completion

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)
exist_line_user_id = os.getenv('LINE_USER_ID')

class LineService:
    def __init__(self):
        required_env_vars = {
            'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
            'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
        }
    
        missing_vars = [k for k, v in required_env_vars.items() if not v]
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.configuration = Configuration(
            access_token=required_env_vars['LINE_CHANNEL_ACCESS_TOKEN']
        )
        self.handler = WebhookHandler(required_env_vars['LINE_CHANNEL_SECRET'])
        
        logger.info("LineService initialization completed")
        self._register_handlers()

    def _register_handlers(self):
        """Register all message handlers"""
        logger.info("Registering message handlers...")
        
        @self.handler.add(MessageEvent, message=TextMessageContent)
        def handle_message(event):
            logger.info(f"Received text message: {event.message.text}")
            try:
                self.handle_text_message(event)
            except Exception as e:
                logger.error(f"Error occurred while processing message: {str(e)}")
                logger.exception(e)

    def handle_text_message(self, event: MessageEvent) -> None:
        """Handle text message"""
        try:
            text = event.message.text
            source = event.source
            source_type = source.type
            source_id = None
            user_id = None

            # Get the appropriate ID based on source type
            if source_type == 'user':
                source_id = source.user_id
                user_id = source_id
                logger.info(f"Received message from user {source_id}")
            elif source_type == 'group':
                source_id = source.group_id
                user_id = source.user_id
                logger.info(f"Received message from group {source_id}, user {user_id}")
            elif source_type == 'room':
                source_id = source.room_id
                user_id = source.user_id
                logger.info(f"Received message from chat room {source_id}, user {user_id}")

            logger.info(f"Message content: {text}")
            logger.debug(f"Complete event information: {event}")
            
            # Check if the user is authorized
            if exist_line_user_id and user_id != exist_line_user_id:
                logger.info(f"Unauthorized user {user_id} attempted to use the bot")
                return  # Skip processing for unauthorized users
            
            translated_text = self.translate_text(text)
            logger.info(f"Translation result: {translated_text}")
            
            self.reply_message(
                event.reply_token,
                translated_text
            )

            logger.info(f"Successfully replied to {source_type} ({source_id})")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)

    def reply_message(self, reply_token: str, text: str) -> None:
        """Reply message"""
        try:
            logger.debug(f"Preparing to reply message, token: {reply_token}, content: {text}")
            with ApiClient(self.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                response = line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=text)]
                    )
                )
                logger.info("Message reply successful")
                logger.info(f"API response: {response}")
        except Exception as e:
            logger.error(f"Failed to reply message: {e}", exc_info=True)

    def translate_text(self, text: str) -> str:
        """Translate text"""
        try:
            if not text:
                logger.warning("Received empty text")
                return "Please enter text to translate"

            logger.info(f"Preparing to translate text: {text}")
            response = completion(
                model = "gpt-4o-mini", 
                messages=[{
                    "content": get_prompt_message(text),
                    "role": "user"
                }], 
            )
            message_content = response.choices[0].message.content
            logger.info(f"Translation completed: {message_content}")

            return message_content

        except Exception as e:
            logger.error(f"Error occurred during translation: {e}", exc_info=True)
            return f"Translation error: {str(e)}"