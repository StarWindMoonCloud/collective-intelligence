import math

from data import critics
import sys


def distance(p1, p2):
    d = 0
    for (k, v) in p1.items():
        if k in p2:
            d += math.pow(p1[k] - p2[k], 2)
    return d
    #return math.sqrt(d)


def sim(p1, p2):
    overlap = set()
    for (k, v) in p1.items():
        if k in p2:
            overlap.add(k)
    ret = 0
    if len(overlap) > 0:
        ret = 1 / (1 + distance(p1, p2))
    return ret


def sim_pear(perf, u1, u2):
    p1 = perf[u1]
    p2 = perf[u2]
    overlap = set()
    for (k, v) in p1.items():
        if k in p2:
            overlap.add(k)
    ret = 0
    if len(overlap) > 0:
        sp = sum(p1[k]*p2[k] for k in overlap)
        s1 = sum(p1[k] for k in overlap)
        s2 = sum(p2[k] for k in overlap)
        ss1 = sum(p1[k] * p1[k] for k in overlap)
        ss2 = sum(p2[k] * p2[k] for k in overlap)
        n = len(overlap)
        ret = (sp - s1 * s2 / n)/math.sqrt((ss1 - s1 * s1 / n)*(ss2 - s2 * s2 / n))
    return ret


def top_matches(pref, person, n=5, similarity=sim_pear):
    sim_users = [(similarity(pref, person, other), other) for other in pref if other != person]
    sim_users.sort()
    sim_users.reverse()
    return sim_users[0:n]


def recommend(pref, u, similarity=sim_pear):
    score_sum = {}
    sim_sum = {}
    for user in pref:
        if user == u:
            continue
        for m in pref[user]:
            if m in pref[u]:
                continue
            sim_score = similarity(pref, u, user)
            score = sim_score * pref[user][m]
            if sim_score < 0:
                continue
            if m in score_sum:
                score_sum[m] += score
                sim_sum[m] += sim_score
            else:
                score_sum[m] = score
                sim_sum[m] = sim_score
    ranks = [(score_sum[m]/s, m) for (m, s) in sim_sum.items()]
    ranks.sort()
    ranks.reverse()
    return ranks


def convert(perf):
    result = {}
    for user in perf:
        for m in perf[user]:
            if m in result:
                result[m][user] = perf[user][m]
            else:
                result[m] = {user: perf[user][m]}
    return result

if __name__ == "__main__":
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    movie = sys.argv[3]
    if name1 in critics and name2 in critics:
        print "sim euc " + str(sim(critics[name1], critics[name2]))
        print "sim pearson " + str(sim_pear(critics, name1, name2))
    else:
        if name1 not in critics:
            print str(name1) + "is not in db"
        if name2 not in critics:
            print str(name2) + "is not in db"
    print sim_pear(critics, name1, name2)
    print top_matches(critics, name1, 10)
    print recommend(critics, name1)
    print convert(critics)
    print top_matches(convert(critics), movie)
    print recommend(convert(critics), movie)
