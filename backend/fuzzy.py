import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def compute_score(clarity, confidence, eye):

    clar = ctrl.Antecedent(np.arange(0,101,1),'clar')
    conf = ctrl.Antecedent(np.arange(0,101,1),'conf')
    eye_c = ctrl.Antecedent(np.arange(0,101,1),'eye')
    score = ctrl.Consequent(np.arange(0,101,1),'score')

    for v in [clar, conf, eye_c, score]:
        v['low'] = fuzz.trimf(v.universe,[0,0,50])
        v['med'] = fuzz.trimf(v.universe,[25,50,75])
        v['high'] = fuzz.trimf(v.universe,[50,100,100])

    rules = [
        ctrl.Rule(conf['high'] & clar['high'], score['high']),
        ctrl.Rule(conf['med'] & clar['med'], score['med']),
        ctrl.Rule(conf['low'] | clar['low'], score['low']),
    ]

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)

    sim.input['clar'] = clarity
    sim.input['conf'] = confidence
    sim.input['eye_c'] = eye

    sim.compute()

    return int(sim.output['score'])