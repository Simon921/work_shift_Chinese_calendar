import datetime
from collections import Counter
from chinese_calendar import is_holiday, get_holiday_detail

# 定义员工名单
employees = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
b_class_only = ['G', 'H']  # 只能值 B 班的员工

# 定义值班表
schedule = {}

# 初始化队列
a_class_queue = [emp for emp in employees if emp not in b_class_only]
b_class_queue = [emp for emp in employees if emp in b_class_only]

# 记录上次值班日期
last_duty = {emp: datetime.date(2023, 1, 1) for emp in employees}

# 遍历2024年每一天
start_date = datetime.date(2024, 4, 1)
end_date = datetime.date(2025, 1, 1)
current_date = start_date

while current_date < end_date:
    # 判断是否为周末或法定节假日
    if current_date.weekday() >= 5 or is_holiday(current_date):
        # 从队列尾部选择值A班和值B班的员工,优先选择上次值班时间最久远的员工
        a_class = min(a_class_queue, key=lambda x: last_duty[x])
        a_class_queue.remove(a_class)
        last_duty[a_class] = current_date

        b_class = min(b_class_queue, key=lambda x: last_duty[x])
        b_class_queue.remove(b_class)
        last_duty[b_class] = current_date

        # 如果员工只能值B班，交换A、B值班人员
        if a_class in b_class_only:
            a_class, b_class = b_class, a_class

        # 如果当天是法定节假日，支付3倍工资
        if is_holiday(current_date):
            holiday_detail = get_holiday_detail(current_date)
            if holiday_detail[1]:
                holiday_name = holiday_detail[1]
            else:
                holiday_name = ''
            print(f'{current_date}\t{"周" + "一二三四五六日"[current_date.weekday()]}\t{holiday_name}\t{a_class}\t{b_class}')
        else:
            print(f'{current_date}\t{"周" + "一二三四五六日"[current_date.weekday()]}\t\t{a_class}\t{b_class}')

        # 将值班安排添加到值班表中
        schedule[current_date] = (a_class, b_class)

        # 将本次值班员工加入相反队列的队首,确保下次轮到另一班
        a_class_queue.append(b_class)
        b_class_queue.append(a_class)

    current_date += datetime.timedelta(days=1)

# 统计每个人当年值班总数
duty_counts = Counter([employee for date, employees in schedule.items() for employee in employees])
print('\n每个人当年值班总数:')
for employee, count in sorted(duty_counts.items()):
    print(f'{employee}: {count}次')
