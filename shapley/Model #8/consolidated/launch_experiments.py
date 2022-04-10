import subprocess
import os
import csv
from rollout import rollout
import time


def save_rewards(N, M, folder_name, agent_speeds):
    runs = ["run_x1"]
    missing_agents_behaviours = ["idle", "random_player", "random"]
    processes = []
    for n in range(N):
        for run in runs:
            for behaviour in missing_agents_behaviours:
                for speeds in agent_speeds:
                    # Replace is here to avoid 'error: unrecognized arguments:' at execution
                    exp_name = f"{run}_{behaviour}_{str(speeds).replace(' ', '_')}_{n}"
                    fname = f"{folder_name}/{exp_name}.csv"
                    if not os.path.exists(fname):
                        command = f'python run.py --load-dir "saves/{run}/episode_2000/model" --missing-agents-behaviour {behaviour} --exp-name {exp_name} --save-dir {folder_name} --shapley-M {M} --num-episodes 1 --agent-speeds'
                        for speed in speeds:
                            command += f" {speed}"
                        processes.append(subprocess.Popen(command, shell=True))
    for p in processes:
        p.wait()


def save_rewards_true_shapley(N, n_episodes, folder_name, agent_speeds):
    runs = ["run_x1"]
    missing_agents_behaviours = ["idle", "random_player", "random"]
    for n in range(N):
        for run in runs:
            for behaviour in missing_agents_behaviours:
                for speeds in agent_speeds:
                    # Replace is here to avoid 'error: unrecognized arguments:' at execution
                    exp_name = f"{run}_{behaviour}_{str(speeds).replace(' ', '_')}_{n}"
                    fname = f"{folder_name}/{exp_name}.csv"
                    if not os.path.exists(fname):
                        print(fname)
                        command = f'python run.py --load-dir "saves/{run}/episode_2000/model" --missing-agents-behaviour {behaviour} --exp-name {run}_{behaviour}_{n} --true-shapley --save-dir {folder_name} --num-episodes {n_episodes} --agent-speeds'
                        for speed in speeds:
                            command += f" {speed}"
                        subprocess.run(command, shell=True)


def save_goal_agents(N, folder_name, agent_speeds):
    runs = ["run_x1"]
    missing_agents_behaviours = ["idle", "random_player", "random"]    
    for run in runs:
            exp_name = f"{folder_name}/{run}"
            fname = f"{exp_name}.csv"

            if not os.path.exists(fname):
                command = f'python run.py --load-dir "saves/{run}/episode_2000/model" --exp-name {exp_name} --save-dir {folder_name} --rollout --num-episodes {N} --agent-speeds'
                for speed in agent_speeds:
                    command += f" {speed}"
                subprocess.run(command, shell=True)


if __name__ == "__main__":
    SPEEDS_EXP1 = [[1.0, 1.0, 1.0, 1.3]] #default
    SPEEDS_EXP12 = [1.0, 1.0, 1.0, 1.3] #default    
    #SPEEDS_EXP2_3VS9 = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.5, 0.5, 0.5]]
    # SPEEDS = []
    #for speed_a1 in range(0, 22, 2):
     #    SPEEDS.append([speed_a1/10, 1.0, 1.0, 1.3])
    start_time = time.time()

    save_rewards(N=1, M=500, folder_name="rewards/exp_x1",
                 agent_speeds=SPEEDS_EXP1)
    mc_time = time.time() - start_time    
    save_goal_agents(2000, "goal_agents/exp_x1",
                      agent_speeds=SPEEDS_EXP12)
    start_time = time.time()        
    save_rewards_true_shapley(N=1, n_episodes=2000, folder_name="rewards/true-shap-exp_x1",
                               agent_speeds=SPEEDS_EXP1)
    true_time = time.time() - start_time
    print("--- %s mc seconds ---" % (mc_time))
    print("--- %s mc seconds ---" % (true_time))

