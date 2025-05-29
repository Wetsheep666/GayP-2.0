from linebot.models import TextSendMessage

welcome_message = TextSendMessage(
    text=(
        "歡迎使用共乘計程車預約系統！\n"
        "請輸入預約資訊。\n"
        "格式：預約 起點->終點 日期 時間 是否共乘 付款方式\n"
        "範例：預約 台北車站->中壢 2025-05-30 15:00 共乘 街口"
    )
)

cancel_success_message = TextSendMessage(text="您的預約已成功取消。")

reservation_instruction_message = TextSendMessage(
    text=(
        "請依以下格式輸入：\n"
        "預約 起點->終點 日期 時間 是否共乘 付款方式\n"
        "範例：預約 台北車站->中壢 2025-05-30 15:00 共乘 街口"
    )
)

def confirm_match_message(group_id, price):
    return TextSendMessage(
        text=f"已成功配對共乘！\n共乘代碼：{group_id}\n平均分攤費用：約 {price}"
    )
