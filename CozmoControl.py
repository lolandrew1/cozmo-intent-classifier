

from cozmo_fsm import *
from cozmo.util import degrees
import os
import re
from IntentClassifier import IntentClassifier

classifier = IntentClassifier()
query = ""
command_num = -1

class ComputePremise(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self,event):
        super().start(event)
 
        global query
        query = event.string

        world = robot.world.world_map.objects
        print("world: ", world)

        world_map_facts = [""]

        
        for obj_key in world:
            obj = world[obj_key]
            
            # visibility
            try:
                visibility = "visible" if obj.is_visible else "invisible"
                visibility_str = f"{obj_key} is {visibility}"
                world_map_facts.append(visibility_str)
            except:
                pass

            # orientation
            try:
                orientation = obj.orientation
                orientation_str = f"{obj_key} orientation is {orientation}"
                world_map_facts.append(orientation_str)
            except:
                pass

            # position
            try:
                x = obj.x
                y = obj.y
                pos_str = f"{obj_key} position is ({x}, {y})"
                world_map_facts.append(pos_str)
            except:
                pass

        # cozmo premise
        cozX = robot.pose.position.x
        cozY = robot.pose.position.y
        cozmo_visible = "Cozmo is visible"
        cozmo_position = f"Cozmo position is ({cozX}, {cozY})"
        world_map_facts.append(cozmo_visible)
        world_map_facts.append(cozmo_position)

        premise = "\n".join(world_map_facts)

        print("premise: ", premise)

        classifier.setPremise(premise)
        self.post_completion()

class Query(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        # set command_num
        global command_num

        command_num, info = classifier.classify(query)
        
        print("got the command num and info", command_num, info)
        

        self.post_completion()


class Check1(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("checking 1")
        if command_num == 1:
            self.post_success()
        else:
            self.post_failure()

class Check2(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("checking 2")
        if command_num == 2:
            self.post_success()
        else:
            self.post_failure()

class Check3(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("checking 3")
        if command_num == 3:
            self.post_success()
        else:
            self.post_failure()

class Check4(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("checking 4", command_num)
        if command_num == 4:
            self.post_success()
        else:
            self.post_failure()

class Check5(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("checking 5")
        if command_num == 5:
            self.post_success()
        else:
            self.post_failure()
        

class Command1(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set command_num
        global command_num
        print("1")
        self.post_completion()

class Command2(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("2")
        self.post_completion()

class Command3(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("3")
        self.post_completion()

class Command4(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("4")
        self.post_completion()

class Command5(StateNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def start(self, event=None):
        super().start(event)
        print("5")
        self.post_completion()

class CozmoControl(StateMachineProgram):
    def __init__(self):
        super().__init__(speech=True, speech_debug=True)

    def setup(self):
        #         loop: StateNode()
        #         loop =Hear('cozmo (.*)')=> ComputePremise() =C=> Query() =C=> execute1
        # 
        #         execute1: Check1()
        #         execute1 =S=> Command1() =C=> loop
        #         execute1 =F=> execute2
        # 
        #         execute2: Check2()
        #         execute2 =S=> Command2() =C=> loop
        #         execute2 =F=> execute3
        #         
        #         execute3: Check3()
        #         execute3 =S=> Command3() =C=> loop
        #         execute3 =F=> execute4
        # 
        #         execute4: Check4()
        #         execute4 =S=> Command4() =C=> loop
        #         execute4 =F=> execute5
        # 
        #         execute5: Check5()
        #         execute5 =S=> Command5() =C=> loop
        #         execute5 =F=> loop
        
        # Code generated by genfsm on Wed Apr 24 19:57:01 2024:
        
        loop = StateNode() .set_name("loop") .set_parent(self)
        computepremise1 = ComputePremise() .set_name("computepremise1") .set_parent(self)
        query1 = Query() .set_name("query1") .set_parent(self)
        execute1 = Check1() .set_name("execute1") .set_parent(self)
        command11 = Command1() .set_name("command11") .set_parent(self)
        execute2 = Check2() .set_name("execute2") .set_parent(self)
        command21 = Command2() .set_name("command21") .set_parent(self)
        execute3 = Check3() .set_name("execute3") .set_parent(self)
        command31 = Command3() .set_name("command31") .set_parent(self)
        execute4 = Check4() .set_name("execute4") .set_parent(self)
        command41 = Command4() .set_name("command41") .set_parent(self)
        execute5 = Check5() .set_name("execute5") .set_parent(self)
        command51 = Command5() .set_name("command51") .set_parent(self)
        
        heartrans1 = HearTrans('cozmo (.*)') .set_name("heartrans1")
        heartrans1 .add_sources(loop) .add_destinations(computepremise1)
        
        completiontrans1 = CompletionTrans() .set_name("completiontrans1")
        completiontrans1 .add_sources(computepremise1) .add_destinations(query1)
        
        completiontrans2 = CompletionTrans() .set_name("completiontrans2")
        completiontrans2 .add_sources(query1) .add_destinations(execute1)
        
        successtrans1 = SuccessTrans() .set_name("successtrans1")
        successtrans1 .add_sources(execute1) .add_destinations(command11)
        
        completiontrans3 = CompletionTrans() .set_name("completiontrans3")
        completiontrans3 .add_sources(command11) .add_destinations(loop)
        
        failuretrans1 = FailureTrans() .set_name("failuretrans1")
        failuretrans1 .add_sources(execute1) .add_destinations(execute2)
        
        successtrans2 = SuccessTrans() .set_name("successtrans2")
        successtrans2 .add_sources(execute2) .add_destinations(command21)
        
        completiontrans4 = CompletionTrans() .set_name("completiontrans4")
        completiontrans4 .add_sources(command21) .add_destinations(loop)
        
        failuretrans2 = FailureTrans() .set_name("failuretrans2")
        failuretrans2 .add_sources(execute2) .add_destinations(execute3)
        
        successtrans3 = SuccessTrans() .set_name("successtrans3")
        successtrans3 .add_sources(execute3) .add_destinations(command31)
        
        completiontrans5 = CompletionTrans() .set_name("completiontrans5")
        completiontrans5 .add_sources(command31) .add_destinations(loop)
        
        failuretrans3 = FailureTrans() .set_name("failuretrans3")
        failuretrans3 .add_sources(execute3) .add_destinations(execute4)
        
        successtrans4 = SuccessTrans() .set_name("successtrans4")
        successtrans4 .add_sources(execute4) .add_destinations(command41)
        
        completiontrans6 = CompletionTrans() .set_name("completiontrans6")
        completiontrans6 .add_sources(command41) .add_destinations(loop)
        
        failuretrans4 = FailureTrans() .set_name("failuretrans4")
        failuretrans4 .add_sources(execute4) .add_destinations(execute5)
        
        successtrans5 = SuccessTrans() .set_name("successtrans5")
        successtrans5 .add_sources(execute5) .add_destinations(command51)
        
        completiontrans7 = CompletionTrans() .set_name("completiontrans7")
        completiontrans7 .add_sources(command51) .add_destinations(loop)
        
        failuretrans5 = FailureTrans() .set_name("failuretrans5")
        failuretrans5 .add_sources(execute5) .add_destinations(loop)
        
        return self


