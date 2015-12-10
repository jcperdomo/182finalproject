import game, maxN, dummyAgent

numGames = 20
numPlayers = 4
gm = game.Game(
    [maxN.MaxNAgent, dummyAgent.DummyAgent, dummyAgent.DummyAgent,
     dummyAgent.DummyAgent
    ]
)

res = gm.playMultGames(verbose=True, restarts=10, n=numGames)
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]

print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),
