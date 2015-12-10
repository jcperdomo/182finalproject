import game, maxN, dummyAgent

numGames = 10
numPlayers = 4
gm = game.Game([maxN.MaxNAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers-1)])

res = gm.playMultGames(verbose=False, n=numGames)
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]

print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),
