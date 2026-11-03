import os
import datetime

def combat_log(func):
    def wrapper(*args, **kargs):
        now = datetime.datetime.now().strftime("%H-%M-%S %d-%m-%Y");

        directory = "battle_logs"

        if not os.path.exists(directory) or not os.path.isdir(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory,"history.txt")

        with open(file_path,"a",encoding="utf-8") as file:
            file.write(f"[{now}] Đã thực hiện hàm: {func.__name__}\n")              
        return func(*args ,**kargs)
    return wrapper

def read_combat_log():
    path = "battle_logs/history.txt"
    if os.path.exists(path) and os.path.isfile(path):
        with open(path,"r",encoding="utf-8") as file:
            return file.read()
    return "Chưa có nhật ký chiến đấu nào!"
    