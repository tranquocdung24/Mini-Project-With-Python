from models import Character, Warrior, Mage, ArenaTrap
from arena import BattleArena
from utils import read_combat_log

def seed_fighters(arena):
    w1 = Warrior("WR-001", "Arthur", 500, 60, armor=30)
    m1 = Mage("MG-002", "Veera", 350, 80, mana=60)
    boss = Warrior("BS-999", "Maloch", 800, 75, armor=50)

    arena.spawn_fighters(w1, m1, boss)

def main():
    arena = BattleArena()
    seed_fighters(arena)
    current_turn = 1

    while True:
        arena_name, max_turns = arena.ARENA_CONFIG

        print("\n" + "=" * 65)
        print(f"{arena_name:^65}")
        print(f"{f'Hiệp đấu: {current_turn}/{max_turns}':^65}")
        print("=" * 65)
        print("1. Xem Bảng Phong Thần")
        print("2. Triệu hồi Đấu sĩ mới")
        print("3. Phát động Tấn công")
        print("4. Đòn Hợp Kích & Bẫy Đấu Trường")
        print("5. Dùng Bình Thuốc / Cường hóa")
        print("6. Tìm kiếm & Lọc Đấu sĩ còn sống")
        print("7. Lưu Kết Quả & Xem Nhật Ký Chiến Đấu")
        print("0. Kết thúc trận đấu")
        print("-" * 65)

        choice = input("Chọn hành động của bạn (0-7): ").strip()

        match choice:
            case "1":
                print(f"\n[*] Tổng số đấu sĩ đã triệu hồi: {Character.get_fighter_count()}")
                print(f"[*] Danh sách tử trận: {arena.fallen_names if arena.fallen_names else 'Chưa có ai'}")

                arena.fighters.sort()
                print("\n--- DANH SÁCH ĐẤU SĨ TRÊN SÂN ---")
                for idx in range(len(arena.fighters)):
                    print(f"{idx + 1}. {arena.fighters[idx]}")

            case "2":
                print("\n--- TRIỆU HỒI ĐẤU SĨ MỚI ---")
                char_id = input("Nhập mã ID (Định dạng XX-123, VD: WR-105): ").strip().upper()

                if not Character.is_valid_id(char_id):
                    print("   [!] Lỗi: Mã ID sai định dạng! (Phải có 2 chữ cái, dấu '-' và 3 chữ số)")
                    continue

                name = input("Nhập tên Đấu sĩ: ").strip().title()
                role = input("Chọn hệ (1 - Đấu Sĩ / 2 - Pháp Sư): ").strip()

                try:
                    hp = float(input("Nhập lượng Máu (HP): "))
                    atk = float(input("Nhập Sức tấn công (ATK): "))

                    if hp <= 0 or atk <= 0:
                        print("   [!] Máu và Sức tấn công phải lớn hơn 0!")
                        continue

                    if role == "1":
                        armor = float(input("Nhập chỉ số Giáp (Armor): "))
                        new_hero = Warrior(char_id, name, hp, atk, armor)
                    else:
                        mana = float(input("Nhập chỉ số Năng lượng (Mana): "))
                        new_hero = Mage(char_id, name, hp, atk, mana)

                    arena.spawn_fighters(new_hero)
                    print(f"   [+] Đã triệu hồi thành công: {new_hero}")
                except ValueError:
                    print("   [!] Lỗi ValueError: Các chỉ số HP, ATK, Giáp/Mana bắt buộc phải là số!")
                finally:
                    print("   --> Hoàn tất nghi thức triệu hồi.")

            case "3":
                print("\n--- PHÁT ĐỘNG TẤN CÔNG ---")
                for idx, f in enumerate(arena.fighters):
                    print(f"{idx}. {f}")

                try:
                    atk_idx = int(input("Chọn STT người tấn công: "))
                    def_idx = int(input("Chọn STT mục tiêu bị đánh: "))

                    attacker = arena.fighters[atk_idx]
                    defender = arena.fighters[def_idx]

                    if not attacker.is_alive():
                        print(f"   [!] {attacker.name} đã gục, không thể tấn công!")
                    else:
                        attacker.special_skill(defender)
                        if not defender.is_alive():
                            arena.fallen_names.add(defender.name)
                        
                        current_turn += 1
                except (ValueError, IndexError):
                    print("   [!] Lỗi: Số thứ tự đấu sĩ không hợp lệ!")

            case "4":
                print("\n--- ĐÒN HỢP KÍCH & BẪY ĐẤU TRƯỜNG ---")
                alive_list = arena.get_alive_fighters()
                if len(alive_list) >= 2:
                    h1 = alive_list[0]
                    h2 = alive_list[1]
                    target = alive_list[-1]

                    combo_dmg = h1 + h2
                    print(f"🤝 [Hợp Kích] {h1.name} + {h2.name} hợp sức tung đòn gây {combo_dmg} sát thương lên {target.name}!")
                    target.hp -= combo_dmg

                    spike_trap = ArenaTrap("Bẫy Gai Địa Ngục", 100)
                    lightning_trap = ArenaTrap("Sấm Sét Phán Quyết", 150)

                    print(f"\n⚠️ Kích hoạt liên hoàn (Đấu sĩ {h1.name} cùng 2 Bẫy tấn công {target.name}):")
                    arena.execute_hazard_wave(target, h1, spike_trap, lightning_trap)

                    if not target.is_alive():
                        arena.fallen_names.add(target.name)
                    current_turn += 1
                else:
                    print("   [!] Cần ít nhất 2 đấu sĩ còn sống trên sân để thực hiện!")

            case "5":
                print("\n--- SỬ DỤNG BÌNH THUỐC & CƯỜNG HÓA ---")
                print(f"Các loại thuốc trong kho: {list(arena.potions.keys())}")
                char_id = input("Nhập mã ID đấu sĩ cần cường hóa (VD: WR-001): ").strip().upper()
                potion_code = input("Nhập mã bình thuốc (HEAL_S, HEAL_L, ATK_BUFF): ").strip().upper()

                val = arena.potions.get(potion_code, 0)
                if val == 0:
                    print("   [!] Mã bình thuốc không tồn tại!")
                else:
                    if "HEAL" in potion_code:
                        arena.buff_character(char_id, hp=val)
                        print(f"   [+] Đã hồi {val} HP cho đấu sĩ mã {char_id}!")
                    else:
                        arena.buff_character(char_id, base_atk=val)
                        print(f"   [+] Đã tăng {val} ATK cho đấu sĩ mã {char_id}!")

            case "6":
                print("\n--- TÌM KIẾM & LỌC ĐẤU SĨ CÒN SỐNG ---")
                alive = arena.get_alive_fighters()
                print(f"[*] Số đấu sĩ còn trụ vững trên sân ({len(alive)} người):")
                for f in alive:
                    print(f"   - Tên: {f['name']:<10} | Máu còn: {f['hp']:>4} | Công: {f['atk']:>3}")

                kw = input("\nNhập từ khóa tên đấu sĩ cần tìm: ").strip()
                found = arena.search_fighter(kw)
                print(f"--> Kết quả tìm kiếm cho '{kw}':")
                for f in found:
                    print("  ", f)

            case "7":
                print("\n--- TỔNG KẾT TRẬN ĐẤU & LỊCH SỬ LOG ---")
                arena.save_match_summary()
                print("[+] Đã xuất bảng tổng kết ra file 'match_result.txt'!")
                
                print("\n--- NHẬT KÝ CHIẾN ĐẤU ---")
                print(read_combat_log())

            case "0":
                print("Trận đấu kết thúc! Hẹn gặp lại tại Đấu Trường!")
                break

            case _:
                print("   [!] Lựa chọn không hợp lệ, vui lòng chọn từ 0 đến 7!")

if __name__ == "__main__":
    main()