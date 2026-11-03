from abc import ABC, abstractmethod

class Character(ABC):
    total_fighters = 0
    def __init__(self, char_id, name, hp, base_atk):
        self.char_id = char_id
        self.name = name
        self._hp = hp
        self.base_atk = base_atk
        Character.total_fighters += 1

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, new_hp):
        if new_hp <= 0: 
            self._hp = 0
            print(f"   [!] {self.name} đã bị hạ gục (HP = 0)!")
        else: self._hp = new_hp

    @hp.deleter
    def hp(self):
        del self._hp

    def is_alive(self):
        return self.hp > 0

    @abstractmethod
    def special_skill(self, target):
        pass

    @classmethod
    def get_fighter_count(cls):
        return cls.total_fighters

    @staticmethod
    def is_valid_id(char_id):
        if len(char_id) != 6:
            return False
        gach_ngang = char_id[2]=="-"
        chu_cai = char_id[0:2].isalpha()
        so = char_id[3:6].isdigit()
        return gach_ngang and chu_cai and so

    def __str__(self):
        status = "Còn sông" if self._hp > 0 else "Đã gục"
        return f"[{self.char_id}] {self.name:<12} | HP: {self._hp:>5,.0f} | ATK: {self.base_atk:>4} | {status}"

    def __eq__(self, other):
        return self.char_id == other.char_id

    def __lt__(self, other):
        return self.base_atk < other.base_atk

    def __gt__(self, other):
            return self.base_atk > other.base_atk

    def __add__(self, other):
        return self.base_atk + other.base_atk

    def __contains__(self, keyword):
        return keyword in self.name

    def __getitem__(self, key):
        match key:
            case "hp": return self._hp
            case "atk": return self.base_atk
            case "name": return self.name


class Warrior(Character):
    def __init__(self, char_id, name, hp, base_atk, armor):
        super().__init__(char_id, name, hp, base_atk)
        self.armor = armor

    def special_skill(self, target):
        damage = self.base_atk*2
        print(f"   ⚔️ [Chiến Binh] {self.name} tung 'Chém Chí Mạng' gây {damage} sát thương lên {target.name}!")
        target.hp -= damage

class Mage(Character):
    def __init__(self, char_id, name, hp, base_atk, mana):
        super().__init__(char_id, name, hp, base_atk)
        self.mana = mana

    def special_skill(self, target):
        if self.mana >= 20:
            dmg = self.base_atk*1.5
            target.hp -= dmg
            self.hp += 30
            print(f"   🔥 [Pháp Sư] {self.name} tung 'Cầu Lửa' gây {dmg} sát thương lên {target.name} và tự hồi 30 HP!")
        else: 
            target.hp -= self.base_atk
            print(f"   🪄 [Pháp Sư] {self.name} hết Mana, đánh thường gây {self.base_atk} sát thương lên {target.name}!")


class ArenaTrap: 
    def __init__(self, trap_name, damage):
        self.trap_name = trap_name
        self.damage = damage

    def special_skill(self, target):
        print(f"   ⚡ [Bẫy Đấu Trường] '{self.trap_name}' kích hoạt! Gây {self.damage} sát thương lên {target.name}!")
        target.hp -= self.damage


        