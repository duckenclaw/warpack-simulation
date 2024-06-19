from shop import Player, Shop, item_database
import random
import pandas as pd

def apply_effect(player, effect, stacks):
    if effect == "Armor":
        player.armor += stacks
    elif effect == "Regeneration":
        player.regeneration += stacks
    elif effect == "Reflect":
        player.reflect += stacks
    elif effect == "Poison":
        player.poison += stacks
    elif effect == "Empower":
        player.empower += stacks
    elif effect == "Cleanse Poison":
        player.poison -= stacks
    elif effect == "Damage":
        player.received_damage = stacks
        if player.armor > 0 and player.armor > stacks:
            player.armor -= stacks
        elif player.armor < stacks:
            stacks -= player.armor
            player.armor = 0
            player.hp -= stacks
        else:
            player.hp -= stacks

def simulate_fight(player1, player2):
    print(f"Fight starts between Player 1 and Player 2")

    time = 0
    while player1.hp > 0 and player2.hp > 0:
        print(f"| {time} SECOND |")
        print(f"P1 HP: {player1.hp} | P2 HP: {player2.hp}")

        # Apply poison and regeneration effects
        if time % 2 == 0:
            if player1.poison > 0:  
                player1.hp -= player1.poison
                print(f"Player 1 suffered {player1.poison} poison damage")
            if player2.poison > 0:  
                player2.hp -= player2.poison
                print(f"Player 2 suffered {player2.poison} poison damage")
            if player1.regeneration > 0:  
                player1.hp += player1.regeneration
                print(f"Player 1 regenerated {player1.regeneration} health")
            if player2.regeneration > 0:  
                player2.hp += player2.regeneration
                print(f"Player 2 regenerated {player2.regeneration} health")

        # On start items
        if time == 0:
            for item in player1.items:
                if item.activation == "On start":
                    apply_effect(player1, item.effect, item.effect_stacks)
                    print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name}")
            for item in player2.items:
                if item.activation == "On start":
                    apply_effect(player2, item.effect, item.effect_stacks)
                    print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name}")

        # On cooldown items
        for item in player1.items:
            if (item.activation == "On cooldown") and (time % item.cooldown == 0):
                roll = random.randint(1, 100)
                if roll <= item.chance:
                    if item.effect in ["Armor", "Regeneration", "Reflect", "Empower", "Cleanse Poison"]:
                        apply_effect(player1, item.effect, item.effect_stacks)
                        print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name}")
                    elif item.effect in ["Poison", "Damage"]:
                        apply_effect(player2, item.effect, item.effect_stacks + player1.empower)
                        print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name} of Player 1")
                else:
                    print(f"{item.name} of Player 1 failed to work (Roll: {roll} > {item.chance})")
        
        for item in player2.items:
            if (item.activation == "On cooldown") and (time % item.cooldown == 0):
                roll = random.randint(1, 100)
                if roll <= item.chance:
                    if item.effect in ["Armor", "Regeneration", "Reflect", "Empower", "Cleanse Poison"]:
                        apply_effect(player2, item.effect, item.effect_stacks)
                        print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name}")
                    elif item.effect in ["Poison", "Damage"]:
                        apply_effect(player1, item.effect, item.effect_stacks + player2.empower)
                        print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name} of Player 2")
                else:
                    print(f"{item.name} of Player 2 failed to work (Roll: {roll} > {item.chance})")

        # On hit items
        if player1.received_damage > 0:
            for item in player1.items:
                if item.activation == "On hit":
                    roll = random.randint(1, 100)
                    if roll <= item.chance:
                        apply_effect(player1, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 1 failed to work (Roll: {roll} > {item.chance})")
            for item in player2.items:
                if item.activation == "On attack":
                    roll = random.randint(1, 100)
                    if roll <= item.chance:
                        apply_effect(player2, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 2 failed to work (Roll: {roll} > {item.chance})")

        if player2.received_damage > 0:
            for item in player2.items:
                if item.activation == "On hit":
                    roll = random.randint(1, 100)
                    if roll <= item.chance:
                        apply_effect(player2, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 2 failed to work (Roll: {roll} > {item.chance})")
            for item in player1.items:
                if item.activation == "On attack":
                    roll = random.randint(1, 100)
                    if roll <= item.chance:
                        apply_effect(player1, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 1 failed to work (Roll: {roll} > {item.chance})")

        # Reflect damage
        player1ReflectDMG = min(player1.received_damage, player1.reflect)
        player2ReflectDMG = min(player2.received_damage, player2.reflect)
        if player2.armor > 0 and player2.armor > player1ReflectDMG:
            player2.armor -= player1ReflectDMG
        elif player2.armor < player1ReflectDMG:
            player1ReflectDMG -= player2.armor
            player2.armor = 0
            player2.hp -= player1ReflectDMG
        else:
            player2.hp -= player1ReflectDMG
        
        if player2.armor > 0 and player2.armor > player2ReflectDMG:
            player2.armor -= player2ReflectDMG
        elif player2.armor < player2ReflectDMG:
            player2ReflectDMG -= player2.armor
            player2.armor = 0
            player2.hp -= player2ReflectDMG
        else:
            player2.hp -= player2ReflectDMG
        
        # Check if any player is dead

        if time >= 50:
            if player1.hp > player2.hp:
                print(f"Player 1 wins!")
                return "Player 1"
            elif player2.hp > player1.hp:
                print(f"Player 2 wins!")
                return "Player 2"
            elif player2.hp == player1.hp:
                print(f"DRAW")
                return "Draw"

        if player1.hp <= 0:
            print("Player 2 wins!")
            return "Player 2"
        if player2.hp <= 0:
            print(f"Player 1 wins!")
            return "Player 1"

        time += 1
        player1.received_damage = 0
        player2.received_damage = 0

def run_simulation(level_player1, level_player2, num_simulations=100):
    item_stats = {item.name: {"wins": 0, "losses": 0} for item in item_database}
    for _ in range(num_simulations):
        levels = random.randint(0, 10)
        player1 = Player(level=levels)
        player2 = Player(level=levels)
        
        shop = Shop(item_database)
        shop.sell_items(player1)
        shop.sell_items(player2)
        
        winner = simulate_fight(player1, player2)
        
        if winner == "Player 1":
            for item in player1.items:
                item_stats[item.name]["wins"] += 1
                item_stats[item.name]["win_rate"] = item_stats[item.name]["wins"]/max(item_stats[item.name]["losses"]+item_stats[item.name]["wins"], 1)
            for item in player2.items:
                item_stats[item.name]["losses"] += 1
                item_stats[item.name]["win_rate"] = item_stats[item.name]["wins"]/max(item_stats[item.name]["losses"]+item_stats[item.name]["wins"], 1)
        elif winner == "Player 2":
            for item in player2.items:
                item_stats[item.name]["wins"] += 1
                item_stats[item.name]["win_rate"] = item_stats[item.name]["wins"]/max(item_stats[item.name]["losses"]+item_stats[item.name]["wins"], 1)
            for item in player1.items:
                item_stats[item.name]["losses"] += 1
                item_stats[item.name]["win_rate"] = item_stats[item.name]["wins"]/max(item_stats[item.name]["losses"]+item_stats[item.name]["wins"], 1)
                

    return item_stats

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Usage: python fight.py <level_player2> <mode> ?<num_simulations>")
        sys.exit(1)

    level_player1 = int(sys.argv[1])
    level_player2 = int(sys.argv[1])
    mode = sys.argv[2]

    if mode == "single":
        player1 = Player(level=level_player1)
        player2 = Player(level=level_player2)
        
        shop = Shop(item_database)
        
        print("Player 1 is shopping...")
        shop.sell_items(player1)
        
        print("Player 2 is shopping...")
        shop.sell_items(player2)
        
        simulate_fight(player1, player2)
    elif mode == "simulate":
        num_simulations=int(sys.argv[3])
        item_stats = run_simulation(0, 0, num_simulations)
        df = pd.DataFrame(item_stats).T
        df.to_csv(f'item_stats{num_simulations}.csv')
        print(f"Simulation complete. Statistics written to item_stats{num_simulations}.csv.")