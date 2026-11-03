from utils import combat_log
import os

class BattleArena:
    ARENA_CONFIG = ("ARENA OF VALOR", 10)

    def __init__(self):
        self.fighters = []
        self.fallen_names = set()
        self.potions = {
            "HEAL_S": 50, 
            "HEAL_L": 150, 
            "ATK_BUFF": 30
        }

    @combat_log
    def spawn_fighters(self,*args):
        for fighter in args:
            if fighter not in self.fighters:
                self.fighters.append(fighter)

    @combat_log
    def buff_character(self,char_id, **kargs):
        for fighter in self.fighters:
            if fighter.char_id == char_id:
                for key, value in kargs.items():
                    if key == "hp":
                        fighter.hp += value
                    if key == "base_atk":
                        fighter.base_atk += value

    @combat_log
    def get_alive_fighters(self):
        return [fighter for fighter in self.fighters if fighter.is_alive()]

    @combat_log
    def search_fighter(self, keyword):
        return [fighter for fighter in self.fighters if keyword in fighter.name ]

    @combat_log
    def execute_hazard_wave(self, target, *hazards):
        for hazard in hazards:
            hazard.special_skill(target)

    @combat_log
    def save_match_summary(self, filename="match_result.txt"):
        with open (filename,"w",encoding="utf-8") as file:
            file.write("===== TỔNG KẾT TRẬN ĐẤU =====\n")
            for fighter in self.fighters:
                file.write(f"{fighter.char_id:<10}{fighter.name:<10}{fighter.hp:<10}\n")
