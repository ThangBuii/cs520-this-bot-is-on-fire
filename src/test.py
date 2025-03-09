import numpy as np
import matplotlib.pyplot as plt
from game import Game
from bot import Bot1, Bot2, Bot3, Bot4
from ship import Ship
from utils import Utils
from fire import Fire
import copy
from collections import deque
from model import CellType
import time

def run_tests(q_values, num_runs=100, size = 40):
    bot_names = ["Bot 1", "Bot 2", "Bot 3", "Bot 4"]
    success_probs_all = {name: [] for name in bot_names}
    success_probs_winnable = {name: [] for name in bot_names}
    winnable_probs = []

    for q in q_values:
        print(f"Testing q = {q:.2f}")
        successes = {name: 0 for name in bot_names}
        winnable_count = 0
        for _ in range(num_runs):
            # Generate ship
            ship_size = size
            ship = Ship()
            ship_grid = ship.generate_ship(ship_size)
            
            # Generate 3 initial points for bot, button, fire
            bot_pos, button_pos, fire_pos = Utils.select_random_positions(ship_grid, num_positions=3)

            # Initialize fire, get mazes
            fire = Fire(copy.deepcopy(ship_grid), q, fire_pos)
            mazes = fire.get_mazes_until_button_on_fire(button_pos)

            # Check winnability
            is_simulation_winnable = Utils.is_winnable(mazes, button_pos, bot_pos)
            if is_simulation_winnable:
                winnable_count += 1
                bots = [
                    Bot1(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
                    Bot2(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
                    Bot3(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
                    Bot4(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos, q)
                ]   
                # Set up game
                game = Game(q, ship_grid,fire,bots,bot_pos,button_pos,fire_pos,None)
                results = game.simulate()

                # Count successes from results
                for i, (bot_num, moves, reason) in enumerate(results):
                    if reason == "success":
                        successes[bot_names[i]] += 1
        
        #Calculate winnability for this q
        winnable_prob = winnable_count / num_runs
        winnable_probs.append(winnable_prob)
        print(f"  Winnability: {winnable_prob:.3f}")

        # Calculate probs to win for each bot for this q
        for bot_name in bot_names:
            # Probs over all simulations
            prob_all = successes[bot_name] / num_runs
            success_probs_all[bot_name].append(prob_all)

            # Probs over only winnable simulations
            prob_winnable = (successes[bot_name] / winnable_count) if winnable_count > 0 else 0
            success_probs_winnable[bot_name].append(prob_winnable)

            print(f"  {bot_name}: {prob_all:.3f} (All), {prob_winnable:.3f} (Winnable)") 

    return success_probs_all,winnable_probs,success_probs_winnable

#Plot the result of winnability over q
def plot_results_winnability(q_values, winnable_probs):
    """Graph success probs for all bots."""
    plt.figure(figsize=(10, 6))

    plt.plot(q_values, winnable_probs, label="Winnability", marker='o')
    
    plt.xlabel("Flammability (q)")
    plt.ylabel("Winnability")
    plt.title("Winnability vs. Fire Flammability")
    plt.legend()
    plt.grid(True)
    plt.xticks(q_values)
    plt.yticks(np.arange(0.1, 1.1, 0.1))
    plt.savefig("winnable_rates.png")
    plt.show()

#Plot the result of bots performance over q
def plot_bot_success_rates(q_values, success_probs_all, success_probs_winnable):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    #Left subplot: Success over all simulations
    for bot_name, probs in success_probs_all.items():
        ax1.plot(q_values, probs, label=bot_name, marker='o')
        ax1.set_xlabel("Flammability (q)")
        ax1.set_ylabel("Success Probability (All Simulations)")
        ax1.set_title("Bot Success Rates (All Simulations)")
        ax1.legend()
        ax1.grid(True)
        ax1.set_xticks(q_values)
        ax1.set_yticks(np.arange(0, 1.1, 0.1))
    
    #Right subplot: Success over winnable simulations
    for bot_name, probs in success_probs_winnable.items():
        ax2.plot(q_values, probs, label=bot_name, marker='o')
        ax2.set_xlabel("Flammability (q)")
        ax2.set_ylabel("Success Probability (Winnable Simulations)")
        ax2.set_title("Bot Success Rates (Winnable Simulations Only)")
        ax2.legend()
        ax2.grid(True)
        ax2.set_xticks(q_values)
        ax2.set_yticks(np.arange(0, 1.1, 0.1))
    
    plt.tight_layout()
    plt.savefig("bot_success_rates_combined.png")
    plt.show()


def run_full_test():
    start_time = time.time()

    q_values = np.arange(0.1, 1.1, 0.1)  # Fire spread probabilities from 0.1 to 1.0
    success_probs_all, winnable_probs, success_probs_winnable = run_tests(q_values, num_runs=100, size=40)
    
    # Generate plots
    plot_results_winnability(q_values, winnable_probs)
    plot_bot_success_rates(q_values, success_probs_all, success_probs_winnable)

    end_time = time.time()  # Record end time
    runtime = end_time - start_time  # Calculate runtime
    print(f"\nTotal runtime: {runtime:.2f} seconds")

if __name__ == "__main__":
    run_full_test()
