from shop import Player, Shop, item_database
import random

def apply_effect(player, effect, stacks):
    if effect == "Armor":
        player.hp += stacks
    elif effect == "Regeneration":
        player.regeneration += stacks
    elif effect == "Reflect":
        player.reflect += stacks
    elif effect == "Poison":
        player.poison += stacks
    elif effect == "Damage":
        player.hp -= stacks
        player.received_damage = stacks

def simulate_fight(player1, player2):
    print(f"Fight starts between Player 1 and Player 2")
    print(f"Player 1: {player1}")
    print(f"Player 2: {player2}")
    
    time = 0

    while player1.hp > 0 and player2.hp > 0:
        print(f"| {time} SECOND |")

        # On start items
        if time == 0:
            for item in player1.items:
                if item.activation == "On start":
                    print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name}")
                    apply_effect(player1, item.effect, item.effect_stacks)
            for item in player2.items:
                if item.activation == "On start":
                    print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name}")
                    apply_effect(player2, item.effect, item.effect_stacks)

        # On cooldown items
        for item in player1.items:
            if (item.activation == "On cooldown") and (time % item.cooldown == 0):
                roll = random.randint(1, 100)
                print(f"Player 1 - {item.name} - Roll: {roll}")
                if roll <= item.chance:
                    if item.effect in ["Armor", "Regeneration", "Reflect"]:
                        print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name}")
                        apply_effect(player1, item.effect, item.effect_stacks)
                    elif item.effect in ["Poison", "Damage"]:
                        print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name} of Player 1")
                        apply_effect(player2, item.effect, item.effect_stacks)
                else:
                    print(f"{item.name} of Player 1 failed to work (Roll: {roll} > {item.chance})")
        
        for item in player2.items:
            if (item.activation == "On cooldown") and (time % item.cooldown == 0):
                roll = random.randint(1, 100)
                print(f"Player 2 - {item.name} - Roll: {roll}")
                if roll <= item.chance:
                    if item.effect in ["Armor", "Regeneration", "Reflect"]:
                        print(f"Player 2 received {item.effect}: {item.effect_stacks} from {item.name}")
                        apply_effect(player2, item.effect, item.effect_stacks)
                    elif item.effect in ["Poison", "Damage"]:
                        print(f"Player 1 received {item.effect}: {item.effect_stacks} from {item.name} of Player 2")
                        apply_effect(player1, item.effect, item.effect_stacks)
                else:
                    print(f"{item.name} of Player 2 failed to work (Roll: {roll} > {item.chance})")
        
        # Apply poison and regeneration effects
        if time % 2 == 0:
            player1.hp -= player1.poison
            player2.hp -= player2.poison
            player1.hp += player1.regeneration
            player2.hp += player2.regeneration

        # On hit items
        if player1.received_damage > 0:
            for item in player1.items:
                if item.activation == "On hit":
                    roll = random.randint(1, 100)
                    print(f"Player 1 - {item.name} (On hit) - Roll: {roll}")
                    if roll <= item.chance:
                        apply_effect(player2, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 1 failed to work (Roll: {roll} > {item.chance})")
        if player2.received_damage > 0:
            for item in player2.items:
                if item.activation == "On hit":
                    roll = random.randint(1, 100)
                    print(f"Player 2 - {item.name} (On hit) - Roll: {roll}")
                    if roll <= item.chance:
                        apply_effect(player1, item.effect, item.effect_stacks)
                    else:
                        print(f"{item.name} of Player 2 failed to work (Roll: {roll} > {item.chance})")

        # Reflect damage
        player2.hp -= min(player1.received_damage, player1.reflect)
        player1.hp -= min(player2.received_damage, player2.reflect)
        
        # Check if any player is dead
        if player1.hp <= 0:
            print("Player 2 wins!")
            break
        if player2.hp <= 0:
            print("Player 1 wins!")
            break

        time += 1
        player1.received_damage = 0
        player2.received_damage = 0

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python fight.py <level_player1> <level_player2>")
        sys.exit(1)

    level_player1 = int(sys.argv[1])
    level_player2 = int(sys.argv[2])

    player1 = Player(level=level_player1)
    player2 = Player(level=level_player2)
    
    shop = Shop(item_database)
    
    print("Player 1 is shopping...")
    shop.sell_items(player1)
    
    print("Player 2 is shopping...")
    shop.sell_items(player2)
    
    simulate_fight(player1, player2)