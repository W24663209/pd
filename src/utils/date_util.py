import datetime


def dmy(seconds_to_add):
    # 获取当前日期时间
    now = datetime.datetime.now() + datetime.timedelta(seconds=60 * seconds_to_add)

    # 将日期格式化为"06/05/2024"的格式
    formatted_date = now.strftime("%d/%m/%Y")

    print(formatted_date)
    return formatted_date


if __name__ == '__main__':
    mdy(-24*60)
