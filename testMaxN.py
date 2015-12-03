import game, maxN, dummyAgent

gm = game.Game([dummyAgent.DummyAgent]*4)
print [sum(k*v for k, v in agent.hand.items()) for agent in gm.agents]
print gm.agents[gm.initialState.whosTurn].hand
print gm.playGame()
