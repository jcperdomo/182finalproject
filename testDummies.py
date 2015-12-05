import game, dummyAgent

gm = game.Game([dummyAgent.DummyAgent for i in xrange(4)], verbose=True)
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
print gm.playGame(verbose=True)
