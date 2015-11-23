import collections
import numpy as np
import pandas as pd
import time

# for human-readable cards
cardRepr = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

# returns full deck of card counts
allCards = lambda: {card: 4 for card in xrange(13)}

# returns empty deck of card counts
noCards = lambda: {card: 0 for card in xrange(13)}

def swapCards(hand1, hand2, k):
    """Does the initial card swapping for Presidents by swapping the worst k
    cards in hand1 with the best k cards in hand2. Note that the card swap is
    done in place, so nothing is returned by this function.

    :hand1: The (vice) president's hand.
    :hand2: The (vice) scum's hand.
    :k: The number of cards to swap.
    """
    for t in xrange(k):
        # find the best and worst cards to swap
        worst = min(hand1.iterkeys(), key=lambda c: (1 - hand1[c] > 0, c))
        best = max(hand2.iterkeys(), key=lambda c: (hand2[c] > 0, c))
        # swap the cards by modifying the hands
        hand1[worst] -= 1
        hand2[worst] += 1
        hand1[best] += 1
        hand2[best] -= 1

def dealHands(cardsLeft, handSizes):
    """Deals the remaining cards randomly, respecting the number of cards each
    player has left. If there are cards remaining, don't deal them to anyone.

    :cardsLeft: A dictionary representing how many of each card there is yet to
    be played.
    :handSizes: An int for the hand size of all players or a list of length
    numPlayers with the hand sizes for each player.
    :returns: A list of hand dictionaries.

    """
    if not isinstance(handSizes, collections.Iterable):
        handSizes = [handSizes]*int(52./handSizes)
    allCards = cardDictToList(cardsLeft)
    np.random.shuffle(allCards)
    cumHandSizes = np.cumsum(handSizes)[:-1]
    hands = map(list, np.split(allCards, cumHandSizes))
    # deal with leftover cards
    if len(hands[-1]) != handSizes[-1]:
        hands[-1] = hands[-1][:handSizes[-1]]
    # convert hands back to dictionaries
    handDicts = map(cardListToDict, hands)
    return handDicts

def cardDictToList(cardDict):
    """Converts dictionary of card counts to list of all cards (with cards
    repeated corresponding to the number of those cards in the dict. Inverse
    function of cardListToDict.

    :cardDict: Dict of card counts.
    :returns: List of all cards.
    """
    return [item for lst in ([k]*v for k, v in cardDict.iteritems())
            for item in lst]

def cardListToDict(cardList):
    """Converts list of cards to dictionary of card counts. Inverse function of
    cardDictToList.

    :cardList: List of cards.
    :returns: Dictionary of card counts.
    """
    return {c: cardList.count(c) for c in xrange(13)}

def diff(cards1, cards2):
    """Removes the cards present in cards2 from cards1.

    :cards1: The master dict of card counts.
    :cards2: The dict of card counts with which to update cards1.
    :returns: The updated dict of card counts.
    """
    result = dict(cards1)
    for k in result.iterkeys():
        if k in cards2:
            result[k] -= cards2[k]
    return result

def add(cards1, cards2):
    """Adds two dictionaries of card counts and returns the result."""
    result = {c: 0 for c in xrange(13)}
    for c, v in cards1.iteritems():
        result[c] += v
    for c, v in cards2.iteritems():
        result[c] += v
    return result

def divideAll(cards, d):
    """Returns a copy of cards with all values divided by d.

    :cards: A dictionary of card counts.
    :d: Value by which to divide the values of cards.
    :returns: Copy of cards with all values divided by d.
    """
    result = dict(cards)
    for k in result.iterkeys():
        result[k] /= float(d)
    return result

def normalize(cards):
    """Converts card counts to card proportions.

    :cards: A dictionary of card counts.
    :returns: A dictionary of card frequencies.
    """
    tot = sum(v for v in cards.itervalues())
    return divideAll(cards, tot)


if __name__ == '__main__':

    presTot = noCards()
    regTot = noCards()
    assTot = noCards()
    vpTot = noCards()
    vaTot = noCards()
    time1 = time.time()
    numTrials = 1000
    numPlayers = 6
    for trial in xrange(numTrials):
        hands = dealHands(allCards(), [52/numPlayers]*numPlayers)
        pres = hands[0]
        ass = hands[1]
        vp = hands[2]
        va = hands[3]
        swapCards(pres, ass, 2)
        swapCards(vp, va, 1)
        presTot = add(presTot, pres)
        vpTot = add(vpTot, vp)
        for hand in hands[4:]:
            regTot = add(regTot, hand)
        vaTot = add(vaTot, va)
        assTot = add(assTot, ass)

    totTime = round(time.time() - time1, 3)

    print

    print 'Sampling {} hands for {} players took <= {} seconds'.format(
        numTrials, numPlayers, totTime
    )

    print

    presExp = divideAll(presTot, numTrials)
    regExp = divideAll(regTot, (numPlayers-2)*numTrials)
    assExp = divideAll(assTot, numTrials)
    vpExp = divideAll(vpTot, numTrials)
    vaExp = divideAll(vaTot, numTrials)
    df = pd.DataFrame([presExp, vpExp, regExp, vaExp, assExp],
                      index=['President', 'VP', 'Regular', 'VA', 'Asshole']
                      ).T
    df.index = cardRepr
    print 'Expected number of each card in each type of hand:'
    print df

    print

    presProb = normalize(presTot)
    regProb = normalize(regTot)
    assProb = normalize(assTot)
    vpProb = normalize(vpTot)
    vaProb = normalize(vaTot)
    probdf = pd.DataFrame([presProb, vpProb, regProb, vaProb, assProb],
                          index=['President', 'VP', 'Regular', 'VA', 'Asshole']
                          ).T
    probdf.index = cardRepr
    print 'Probability of each card in each type of hand:'
    print probdf

    print
