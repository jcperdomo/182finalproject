import game, paranoid, dummyAgent

gm = game.Game([paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(3)])
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
print gm.playGame(verbose=True)
