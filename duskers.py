

import sys
import random
import time
from datetime import datetime

args = sys.argv
arg1 = args[1] if len(args) > 1 else "42"
arg2 = args[2] if len(args) > 2 else "0"
arg3 = args[3] if len(args) > 3 else "0"
arg4 = args[4] if len(args) > 4 else "GreenPark,NuclearPlantWreckage,HighStreet,BrokenOverpass,ControlBunker"


random.seed(arg1)

# Centralized game state
game_state = {
    "titanium": 0,
    "robots": 3,  # Starting with 3 robots
    "player_name": "",
    "show_titanium": False,
    "show_encounter_rate": False,
    "high_scores": []
}

title = """+====================================================+
██████╗░██╗░░░██╗░██████╗██╗░░██╗███████╗██████╗░░██████╗
██╔══██╗██║░░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗██╔════╝
██║░░██║██║░░░██║╚█████╗░█████═╝░█████╗░░██████╔╝╚█████╗░
██║░░██║██║░░░██║░╚═══██╗██╔═██╗░██╔══╝░░██╔══██╗░╚═══██╗
██████╔╝╚██████╔╝██████╔╝██║░╚██╗███████╗██║░░██║██████╔╝
╚═════╝░░╚═════╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░
+====================================================+"""

def get_validated_input(prompt, valid_options, error_message="Invalid input"):
    while True:
        print()
        user_input = input(f"{prompt}\n> ").lower()
        if user_input in valid_options:
            return user_input
        print(error_message)
        print()

def main():
    while True:
        print(title)
        print()
        print("[New] Game\n[Load] Game\n[High] Scores\n[Help]\n[Exit]")
        print()
        cmd = get_validated_input("Your command:", ["new", "load", "high", "help", "exit"])
        if cmd == "new":
            decision = new(game_state, True)
            if decision == "break":
                break
            elif decision == "main_menu":
                continue
        elif cmd == "load":
            load(game_state)
            continue
        elif cmd == "high":
            high(game_state)
            continue
        elif cmd == "help":
            help()
            continue
        else:
            print("Exiting the game. Goodbye!")
            break

def new(game_state, flag=True):
    def get_robot_display(robot_count):
        robot = [
            "  $   $$$$$$$   $  ",
            "  $$$$$     $$$$$  ",
            "      $$$$$$$      ",
            "     $$$   $$$     ",
            "     $       $     "
        ]

        return "\n".join([" | ".join([line for _ in range(robot_count)]) for line in robot])


    slot1, slot2, slot3 = "empty", "empty", "empty"
    print()
    ready = 'yes'
    name = ''
    if flag:
        game_state["titanium"] = 0
        game_state["robots"] = 3
        game_state["show_titanium"] = False
        game_state["show_encounter_rate"] = False
        name = input("Enter your name:\n> ")
        print()
        print(f"Greetings, commander {name}!")
        game_state["player_name"] = name
        print("Are you ready to begin?\t\n[Yes] [No] Return to Main[Menu]")
        ready = get_validated_input("Your command:", ["yes", "no", "menu"])
        while ready == "no":
            print("What About Now?\t\n[Yes] [No] [Back]")
            ready = input("Your command:\n> ").lower()
            if ready == "back":
                return "main_menu"
            while ready not in ["yes", "no"]:
                print("Invalid input")
                print()
                ready = input("Your command:\n> ").lower()
    if ready == "yes" :
        while True:
            if game_state["robots"] == 0:
                print("""                        |==============================|
                        |          GAME OVER!          |
                        |==============================|
""")
                with open("high_scores.txt", "a") as fh:
                    fh.write(f"{game_state['player_name']} {game_state['titanium']}\n")
                return "main_menu"
            hub = f"""+==============================================================================+
{get_robot_display(game_state["robots"])}
+==============================================================================+
| Titanium: {game_state['titanium']}   Robots: {game_state['robots']}   Commander: {game_state['player_name']:10}                              |
+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+"""
            print(hub)
            cmd = get_validated_input("Your command:", ['m', 'ex', 'up', 'save'])
            if cmd == 'm':
                decision = menu()
                if decision == "back":
                    continue
                elif decision == "break":
                    return "break"
                else:
                    return "main_menu"
            elif cmd == 'ex':
                output = explore(game_state)
                if output == "back":
                    continue
            elif cmd == 'up':
                upgrade(game_state)
                continue
            elif cmd == 'save':
                slot1, slot2, slot3 = save(game_state)
                continue
            return "break"
    elif ready == "menu":
        return "main_menu"

def load(game_state):
    load_banner = f"""                        |==============================|
                        |    GAME LOADED SUCCESSFULLY  |
                        |==============================|"""
    file_wise_data = {}
    files = ["save_file1.txt", "save_file2.txt", "save_file3.txt"]
    for file in files:
        try:
            with open(file, "r") as fh:
                data = fh.readlines()
                file_wise_data[file] = [string.strip() for string in data]
        except FileNotFoundError:
            file_wise_data[file] = ["empty"]
    def slot_info(slot1, slot2, slot3):
        print(f"""   Select save slot:
            [1] {slot1}
            [2] {slot2}
            [3] {slot3}""")
    if len(file_wise_data["save_file1.txt"]) != 1:
        slot1 = f"{file_wise_data['save_file1.txt'][0]} Titanium: {file_wise_data['save_file1.txt'][1]} Robots: {file_wise_data['save_file1.txt'][2]} Last save: {file_wise_data['save_file1.txt'][3]}"
    else:
        slot1 = "empty"
    if len(file_wise_data["save_file2.txt"]) != 1:
        slot2 = f"{file_wise_data['save_file2.txt'][0]} Titanium: {file_wise_data['save_file2.txt'][1]} Robots: {file_wise_data['save_file2.txt'][2]} Last save: {file_wise_data['save_file2.txt'][3]}"
    else:
        slot2 = "empty"
    if len(file_wise_data["save_file3.txt"]) != 1:
        slot3 = f"{file_wise_data['save_file3.txt'][0]} Titanium: {file_wise_data['save_file3.txt'][1]} Robots: {file_wise_data['save_file3.txt'][2]} Last save: {file_wise_data['save_file3.txt'][3]}"
    else:
        slot3 = "empty"
    slot_info(slot1, slot2, slot3)
    cmd = get_validated_input("your command:", ['1', '2', '3', 'back'])
    if cmd in ['1', '2', '3']:
        while file_wise_data[f"save_file{cmd}.txt"][0] == "empty":
            print("No saved game found in this slot.")
            print("Please select another slot or go back.")
            slot_info(slot1, slot2, slot3)
            cmd = get_validated_input("your command:", ['1', '2', '3', 'back'])
            if cmd == "back":
                return "main_menu"
    else:
        return "main_menu"
    game_state["player_name"] = file_wise_data[f"save_file{cmd}.txt"][0]
    game_state["titanium"] = int(file_wise_data[f"save_file{cmd}.txt"][1])
    game_state["robots"] = int(file_wise_data[f"save_file{cmd}.txt"][2])
    game_state['show_titanium'] = file_wise_data[f"save_file{cmd}.txt"][4] == 'True'  # At index 3 save_time is there !!
    game_state['show_encounter_rate'] = file_wise_data[f"save_file{cmd}.txt"][5] == 'True'
    # robots always 3 for now
    print(load_banner)
    print()
    print(f"Welcome back, commander {game_state['player_name']}!")
    new(game_state, flag=False)


def menu():
    print("""       |==========================|
        |          MENU            |
        |                          |
        | [Back] to game           |
        | Return to [Main] Menu    |
        | [Save] and exit          |
        | [Exit] game              |
        |==========================|""")
    menu_cmd = get_validated_input("Your command:", ['back', 'main', 'save', 'exit'])
    if menu_cmd == 'back':
        return "back"
    elif menu_cmd == 'main':
        return "main_menu"
    elif menu_cmd == 'save':
        print("Coming SOON! Thanks for playing!")
        return "break"
    elif menu_cmd == 'exit':
        print("Exiting the game. Goodbye!")
        return "break"

def explore(game_state):


    def format_location_display(loc_num, loc_name, titanium, encounter_rate, game_state):
        display = f"[{loc_num}] {loc_name}"
        if game_state["show_titanium"]:
            display += f" | Titanium: {titanium}"
        if game_state["show_encounter_rate"]:
            percent = round(encounter_rate * 100)
            display += f" | Encounter: {percent}%"
        return display

    def animation_time(min=0, max=1):
        curr_time_secs = time.time()
        time_limit = abs(max - min)
        value = min + (curr_time_secs % time_limit)
        return value
    if (int(arg2) - int(arg3)) != 0:
        rep_arg_value = animation_time(int(arg2), int(arg3))
    else:
        rep_arg_value = animation_time()
    def dot_animation(starting_text, rep=rep_arg_value):
        print(starting_text, end='', flush=True)
        for i in range(int(rep)):
            time.sleep(1)
            print(".", end='', flush=True)
    number_locations = random.randint(1, 9)
    loc_num = 1
    print()
    map_num_loc = {}
    titanium_rewards = {}
    encounter_rate = {}

    map_num_loc[loc_num] = random.choice(arg4.split(','))
    titanium_rewards[loc_num] = random.randint(10, 100)
    encounter_rate[loc_num] = random.random()
    locations = []

    dot_animation("Searching")
    print()
    locations.append(format_location_display(loc_num, map_num_loc[loc_num], titanium_rewards[loc_num], encounter_rate[loc_num], game_state))
    for place in locations:
        print(place)
    print()
    print("[S] to continue searching.")
    print()

    valid_options = ['s', str(loc_num), 'back']

    while number_locations >= loc_num:
        ex_cmd = get_validated_input("your command:", valid_options)
        if ex_cmd == "s" and number_locations != loc_num:
            loc_num += 1

            valid_options.append(str(loc_num))

            map_num_loc[loc_num] = random.choice(arg4.split(','))
            titanium_rewards[loc_num] = random.randint(10, 100)
            encounter_rate[loc_num] = random.random()

            locations.append(format_location_display(loc_num, map_num_loc[loc_num], titanium_rewards[loc_num], encounter_rate[loc_num], game_state))
            dot_animation("Searching")
            print()
            for place in locations:
                print(place)
        elif ex_cmd == "back":
            return "back"
        elif ex_cmd != "s":
            dot_animation("Deploying Robots")
            print()
            encounter_decision = random.random()
            if encounter_decision < encounter_rate[int(ex_cmd)]:
                dot_animation("Enemy Encounter")
                if game_state['robots'] != 1:
                    print(f"{map_num_loc[int(ex_cmd)]} explored successfully, 1 robot lost..")
                else:
                    print("\nMission aborted, the last robot lost...")
                    game_state['robots'] -= 1
                    return "back"
                game_state["robots"] -= 1
            else:
                print(f"{map_num_loc[int(ex_cmd)]} explored successfully, with no damage taken.")
            titanium_aquired = titanium_rewards[int(ex_cmd)]
            game_state["titanium"] += titanium_aquired
            print(f"Acquired {titanium_aquired} lumps of titanium")
            return "back"
        else:
            number_locations -= 2
    else:
        valid_options = valid_options[1:]
        print("Nothing more in sight.")
        print("    [Back]    ")
        ex_cmd = get_validated_input("your command:", valid_options)
        if ex_cmd == "back":
            return "back"
        else:
            dot_animation("Deploying Robots")
            print()
            encounter_decision = random.random()
            if encounter_decision < encounter_rate[int(ex_cmd)]:
                dot_animation("Enemy Encounter")
                if game_state['robots'] != 1:
                    print(f"{map_num_loc[int(ex_cmd)]} explored successfully, 1 robot lost..")
                else:
                    print("\nMission aborted, the last robot lost...")
                    game_state['robots'] -= 1
                    return "back"
                game_state["robots"] -= 1
            else:
                print(f"{map_num_loc[int(ex_cmd)]} explored successfully, with no damage taken.")
            titanium_aquired = titanium_rewards[int(ex_cmd)]
            game_state["titanium"] += titanium_aquired
            print(f"Acquired {titanium_aquired} lumps of titanium")
            return "back"
def upgrade(game_state):
    while True:
        print("""                       |================================|
                       |          UPGRADE STORE         |
                       |                         Price  |
                       | [1] Titanium Scan         250  |
                       | [2] Enemy Encounter Scan  500  |
                       | [3] New Robot            1000  |
                       |                                |
                       | [Back]                         |
                       |================================|
""")
        cmd = get_validated_input("your command:", ["1", "2", "3", "back"])
        if cmd == "back":
            return None
        elif cmd == "1":
            if game_state["show_titanium"]:
                print("Already purchased this upgrade.")
                return None
            if game_state["titanium"] >= 250:
                game_state["show_titanium"] = True
                game_state["titanium"] -= 250
                print("Titanium scan upgrade successful!")
                return None
            else:
                print("Not enough titanium for this upgrade.")
                continue
        elif cmd == "2":
            if game_state["show_encounter_rate"]:
                print("Already purchased this upgrade.")
                return None
            if game_state["titanium"] >= 500:
                game_state["show_encounter_rate"] = True
                game_state["titanium"] -= 500
                print("Enemy encounter scan upgrade successful!")
                return None
            else:
                print("Not enough titanium for this upgrade.")
                continue
        elif cmd == "3":
            if game_state['robots'] > 4:
                print("Maximum number of robots reached.")
                return None
            if game_state["titanium"] >= 1000:
                game_state["robots"] += 1
                game_state["titanium"] -= 1000
                print(f"New robot added! Total robots: {game_state['robots']}")
                return None
            else:
                print("Not enough titanium for this upgrade.")
                continue

def high(game_state):
    try:
        with open("high_scores.txt", "r") as fh:
            high_scores = [line.strip() for line in fh.readlines()]
    except FileNotFoundError:
        print("No high scores available.")
        return None
    # Sort and display up to 10
    high_scores.sort(key=lambda x: int(x.split()[1]), reverse=True)
    print()
    print("  HIGH SCORES")
    print()
    for i, score in enumerate(high_scores[:10], start=1):
        print(f"({i}) {score}")
    print()
    print("  [Back]")
    cmd = get_validated_input("your command:", ["back"])
    return None



def save(game_state):
    save_banner = """                        |==============================|
                        |    GAME SAVED SUCCESSFULLY   |
                        |==============================|"""
    file_wise_data = {}
    files = ["save_file1.txt", "save_file2.txt", "save_file3.txt"]
    for file in files:
        try:
            with open(file, "r") as fh:
                data = fh.readlines()
                file_wise_data[file] = [string.strip() for string in data]
        except FileNotFoundError:
            file_wise_data[file] = ["empty"]

    def slot_info(slot1, slot2, slot3):
        print(f"""   Select save slot:
                [1] {slot1}
                [2] {slot2}
                [3] {slot3}""")

    if len(file_wise_data["save_file1.txt"]) != 1:
        slot1 = f"{file_wise_data['save_file1.txt'][0]} Titanium: {file_wise_data['save_file1.txt'][1]} Robots: {file_wise_data['save_file1.txt'][2]} Last save: {file_wise_data['save_file1.txt'][3]}"
    else:
        slot1 = "empty"
    if len(file_wise_data["save_file2.txt"]) != 1:
        slot2 = f"{file_wise_data['save_file2.txt'][0]} Titanium: {file_wise_data['save_file2.txt'][1]} Robots: {file_wise_data['save_file2.txt'][2]} Last save: {file_wise_data['save_file2.txt'][3]}"
    else:
        slot2 = "empty"
    if len(file_wise_data["save_file3.txt"]) != 1:
        slot3 = f"{file_wise_data['save_file3.txt'][0]} Titanium: {file_wise_data['save_file3.txt'][1]} Robots: {file_wise_data['save_file3.txt'][2]} Last save: {file_wise_data['save_file3.txt'][3]}"
    else:
        slot3 = "empty"
    slot_info(slot1, slot2, slot3)
    cmd = get_validated_input("your command:", ['1', '2', '3', 'back'])
    if cmd == '1':
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        slot1 = f"{game_state['player_name']} Titanium: {game_state['titanium']} Robots: {game_state['robots']} Last save: {save_time}"
        with open('save_file1.txt', 'w') as fh:
            fh.write(f"{game_state['player_name']}\n{game_state['titanium']}\n"
                     f"{game_state['robots']}\n{save_time}\n{game_state['show_titanium']}\n"
                     f"{game_state['show_encounter_rate']}")
        print(save_banner)
    elif cmd == '2':
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        slot2 = f"{game_state['player_name']} Titanium: {game_state['titanium']} Robots: {game_state['robots']} Last save: {save_time}"
        with open('save_file2.txt', 'w') as fh:
            fh.write(f"{game_state['player_name']}\n{game_state['titanium']}\n"
                     f"{game_state['robots']}\n{save_time}\n{game_state['show_titanium']}\n"
                     f"{game_state['show_encounter_rate']}")
        print(save_banner)
    elif cmd == '3':
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        slot3 = f"{game_state['player_name']} Titanium: {game_state['titanium']} Robots: {game_state['robots']} Last save: {save_time}"
        with open('save_file3.txt', 'w') as fh:
            fh.write(f"{game_state['player_name']}\n{game_state['titanium']}\n"
                     f"{game_state['robots']}\n{save_time}\n{game_state['show_titanium']}\n"
                     f"{game_state['show_encounter_rate']}")
        print(save_banner)
    print(game_state['robots'])
    return slot1, slot2, slot3

def help():
    print("""
                       |================================|
                       |              HELP              |
                       |================================|
                       |                                |
                       |  Welcome, Commander! Here's    |
                       |  a quick guide to your mission.|
                       |                                |
                       |  MAIN MENU:                    |
                       |  [New] Game: Start a fresh     |
                       |              adventure.        |
                       |  [Load] Game: Continue a saved |
                       |               mission.         |
                       |  [High] Scores: See the best   |
                       |                commanders.     |
                       |  [Help]: Display this guide.   |
                       |  [Exit]: Leave the game.       |
                       |                                |
                       |  GAME HUB:                     |
                       |  [Ex]plore: Send your robots   |
                       |             to new locations   |
                       |             to gather titanium.|
                       |             Be warned:         |
                       |             Encounters can cost|
                       |             you robots!        |
                       |  [Up]grade: Improve your       |
                       |             operations in the  |
                       |             Upgrade Store.     |
                       |  [Save]: Save your current     |
                       |          game progress.        |
                       |  [M]enu: Return to the main    |
                       |          menu (you can also    |
                       |          save from here).      |
                       |                                |
                       |  UPGRADE STORE:                |
                       |  [1] Titanium Scan: Reveals    |
                       |                  titanium      |
                       |                  amounts in    |
                       |                  explore areas.|
                       |  [2] Enemy Encounter Scan:     |
                       |                  Shows the     |
                       |                  chance of     |
                       |                  enemy         |
                       |                  encounters.   |
                       |  [3] New Robot: Replenish your |
                       |               robot forces.    |
                       |  [Back]: Exit the store.       |
                       |                                |
                       |  Your goal is to gather as much|
                       |  titanium as possible while    |
                       |  keeping your robots safe. If  |
                       |  all robots are lost, it's     |
                       |  game over!                    |
                       |                                |
                       |================================|
                       |         Good luck, Commander!  |
                       |================================|
""")
    print()
    get_validated_input("Press [Back] to return to the Main Menu:", ["back"])


main()