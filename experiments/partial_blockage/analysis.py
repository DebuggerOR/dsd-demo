import json
import time
from random import seed

from planners.greedy.iterative_assignment_planner import IterativeAssignmentPlanner
from planners.partial_blockage.static_line_lack_planner import StaticLineLackPlanner
from planners.partial_blockage.static_line_lack_sampling_planner import StaticLineLackSamplingPlanner
from planners.planner import Planner
from utils.functions import *

with open('./config.json') as json_file:
    config = json.load(json_file)


def run(planner: Planner):
    agents = [FixedVelocityAgent(sample_point(config['x_buffer'], config['x_buffer'] + config['x_size'],
                                              config['y_buffer'], config['y_buffer'] + config['y_size_init']),
                                 config['agent_speed']) for _ in range(config['num_agents'])]

    robots = [BasicRobot(sample_point(0, config['x_size'] + 2 * config['x_buffer'], 0, config['y_buffer']),
                         config['robot_speed'], config['disablement_range'], has_mode=True)
              for _ in range(config['num_robots'])]

    env = Environment(agents=agents, robots=robots, border=config['y_size'] + config['y_buffer'])

    before = time.time()
    movement, active_time, completion_time, expected_damage, expected_num_disabled = planner.plan(env)
    planning_time = time.time() - before

    write_report(planner=str(planner),
                 num_agents=config['num_agents'],
                 num_robots=config['num_robots'],
                 f=config['robot_speed'] / config['agent_speed'],
                 d=config['disablement_range'],
                 active_time=active_time,
                 completion_time=completion_time,
                 planner_time=planning_time,
                 damage=expected_damage,
                 num_disabled=expected_num_disabled,
                 file_name='agents_results.csv')


if __name__ == '__main__':
    # planners = [StaticLineLackPlanner(), IterativeAssignmentPlanner()]
    planners = [StaticLineLackSamplingPlanner()]

    for planner in planners:
        for v in [50,100,200,300,400,500,600,700,800,900,1000]:
            print(f'running for v={v} ..')
            for s in range(4):
                seed(s)

                config['num_agents'] = v
                print(f'running {str(planner)} with seed {s} ..')
                run(planner)

    # for planner in planners:
    #     for v in [1.1, 1.3, 1.5, 1.7, 1.9, 2]:
    #         print(f'running for v={v} ..')
    #         for s in range(2):
    #             seed(s)
    #
    #             config['robot_speed'] = v
    #             config['num_agents'] = 100
    #             print(f'running {str(planner)} ..')
    #             run(planner)
