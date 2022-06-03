from planners.planner import Planner
from utils.algorithms import static_lack_moves, stochastic_lack_moves
from utils.functions import *


class StochasticStaticLackPlanner(Planner):
    def plan(self, env: Environment):
        robots = env.robots
        agents = env.agents
        b = env.border
        v = agents[0].v

        H = [meeting_height(robot, agent) for agent in agents for robot in robots if meeting_height(robot, agent) < b]
        if len(H) == 0:
            return {robot: [robot.loc] for robot in robots}, \
                   0, \
                   sum([b - agent.y for agent in agents]), \
                   0,\
                   {robot: [0] for robot in robots}

        flow_per_h = {h: stochastic_lack_moves(robots, agents, h) for h in H}
        disabled_per_h = {h: flow_per_h[h]['disabled'] for h in H}
        movement_per_h = {h: flow_per_h[h]['movement'] for h in H}
        exp_disabled_per_h = {h: flow_per_h[h]['exp_disabled'] for h in H}

        # timing_per_h = {h: flow_per_h[h]['timing'] for h in H}

        # calculate line score
        def damage_score(h):
            return sum([b - agent.y for agent in agents]) - exp_disabled_per_h[h] * (b - h)

        damage_score_per_h = {h: damage_score(h) for h in H}
        h_opt = min(H, key=lambda h: damage_score_per_h[h])

        completion_time = 0
        if exp_disabled_per_h[h_opt] > 0:
            completion_time = (h_opt - min([agent.y for agent in disabled_per_h[h_opt]])) / v

        return movement_per_h[h_opt], \
               completion_time, \
               damage_score_per_h[h_opt], \
               exp_disabled_per_h[h_opt],\
            None
               # timing_per_h[h_opt]

    def __str__(self):
        return 'StochasticStaticLackPlanner'
