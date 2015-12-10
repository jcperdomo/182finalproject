import game, dummyAgent
import operator

numGames = 50
numPlayers = 4
for i in xrange(3):
    gm = game.Game([dummyAgent.DummyAgent for i in xrange(numPlayers)])
    res = gm.playMultGames(verbose=False, restarts=10, n=numGames)
    rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
    print '--------------------------------'
    print 'Average rankings after {0} games'.format(numGames)
    print '--------------------------------'
    for player in xrange(numPlayers):
            print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),
