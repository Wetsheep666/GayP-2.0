from linebot.models import TextSendMessage
from message_templates import (
    welcome_message,
    cancel_success_message,
    reservation_instruction_message,
    confirm_match_message
)
from database import add_reservation, cancel_reservation
from matcher import try_match
from utils import format_currency

def handle_event(event, line_bot_api):
    text = event.message.text.strip()
    user_id = event.source.user_id

    if text.startswith("預約"):
        parts = text.split(" ")
        if len(parts) != 6 or "->" not in parts[1]:
            # 格式錯誤，回傳教學訊息
            reply = reservation_instruction_message
        else:
            try:
                start, end = parts[1].split("->")
                time = parts[2] + " " + parts[3]
                is_shared = 1 if parts[4] == "共乘" else 0
                payment = parts[5]

                # 寫入資料庫
                add_reservation((user_id, start, end, time, is_shared, payment))

                # 嘗試配對
                matched_info = try_match()
                if matched_info:
                    group_id, price = matched_info
                    reply = confirm_match_message(group_id, format_currency(price))
                else:
                    reply = TextSendMessage(text="已收到共乘資訊，暫時還沒配對到人，請稍等。")
            except Exception as e:
                reply = TextSendMessage(text=f"系統錯誤：{e}")

    elif text == "取消":
        cancel_reservation(user_id)
        reply = cancel_success_message

    elif text in ["開始", "start"]:
        reply = welcome_message

    else:
        reply = reservation_instruction_message

    line_bot_api.reply_message(event.reply_token, reply)
