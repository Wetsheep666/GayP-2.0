from database import get_active_reservations, assign_group
import datetime, uuid

def parse_time(t):
    return datetime.datetime.strptime(t, '%Y-%m-%d %H:%M')

def try_match():
    reservations = get_active_reservations()
    matched = set()
    for i, r1 in enumerate(reservations):
        if r1[8] != 'active' or r1[5] == 0: continue  # 不是共乘的跳過
        for j, r2 in enumerate(reservations[i+1:], i+1):
            if r2[8] != 'active' or r2[5] == 0: continue
            if r1[2] == r2[2] and r1[3] == r2[3]:  # 起終點一樣
                t1, t2 = parse_time(r1[4]), parse_time(r2[4])
                if abs((t1 - t2).total_seconds()) <= 600:
                    group_id = str(uuid.uuid4())
                    assign_group([r1[1], r2[1]], group_id, "分攤後100元")
                    matched.update([r1[0], r2[0]])
                    break
