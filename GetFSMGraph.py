from app import machine

graph = machine.get_graph()
graph.draw('fsm.png', prog='dot', format='png')