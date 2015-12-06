import game, maxN, dummyAgent

gm = game.Game([maxN.MaxNAgent] + [dummyAgent.DummyAgent for i in xrange(3)])
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
print gm.playGame(verbose=True)