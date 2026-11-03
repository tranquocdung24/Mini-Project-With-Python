import os
import datetime

def activity(func):
    def wrapper(*args, ** kargs):
        now = datetime.datetime.now();
        format_now = now.strftime("%H-%M-%S %d-%m-%Y")

        log_dir = "logs"

        if not os.path.isdir(log_dir) or not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_path = os.path.join(log_dir,"logs_act.txt")

        with open(file_path,"a",encoding="utf-8") as file:
            file.write(f"[{format_now}] Đã thực thi: {func.__name__}\n")
        return func(*args, ** kargs)
    return wrapper

def read_activity():
    file_path = "logs/logs_act.txt"

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path,"r",encoding="utf-8") as file:
            content = file.read();
            return content
    else:
        return "Chưa có lịch sử hoạt động nào được ghi lại!"
        