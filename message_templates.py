# message_templates.py
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction

def welcome_message():
    return TextSendMessage(
        text="歡迎使用共乘計程車服務！請輸入：\n預約 起點->終點 日期 時間 是否共乘 付款方式"
    )

def cancel_success_message():
    return TextSendMessage(text="你的預約已成功取消！")

def reservation_instruction_message():
    return TextSendMessage(
        text="請依以下格式輸入：\n預約 起點->終點 日期 時間 是否共乘 付款方式\n範例：預約 台北車站->中壢 2025-05-30 15:00 共乘 街口"
    )

def confirm_match_message(group_id, price):
    return TextSendMessage(
        text=f"已幫你找到共乘對象！群組ID: {group_id}\n預估每人花費：{price}"
    )
