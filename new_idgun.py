def identify_gun(rle, lt4):

    a = lt4.pattern(rle)

    if a.empty():
        return []

    a = a[524288]
    x = lt4.pattern('', 'LifeHistory')
    x += a
    x = x[524288]
    p = x.population

    if (p < 1000000):
        return None

    if (p > 1500000):
        return None

    envelope = x.layers()[1]
    livecells = x[8].layers()[0]
    y = livecells - envelope
    envelope = x[256].layers()[1]

    if (y.population != 5):
        return None

    z = lt4.pattern("", "b3s23")
    z += y

    if (z.apgcode != 'xq4_153'):
        return None

    w = lt4.pattern("", "LifeHistory")
    w += z[-2097152]
    w = w[4194304]


    band = w.layers()[1]

    pbb = envelope - band
    r1 = z.getrect()
    r2 = z[1024].getrect()

    pbb += pbb(r1[0] - r2[0], r1[1] - r2[1])

    r = pbb.getrect()
    if (r is None) or (len(r) != 4):
        return None

    envelope = envelope[r[0] : r[0] + r[2], r[1] : r[1] + r[3]]
    r = envelope.getrect()

    geater = lt4.pattern("bo$2bo$3o4$5b2o$5bo$6b3o$8bo!", "b3s23")

    eater = z.replace(geater[:3, :3], geater[100], orientations='rotate4reflect', n_phases=2)

    if (eater.population != 7):
        return None

    x += eater

    x = x[128]

    multiple = x.oscar(eventual_oscillator=False, maxexp=20)['period']

    print('True period: %d' % multiple)

    if (multiple > 100000):
        print('Period too large')
        return []

    gun = lt4.pattern("", "b3s23")
    gun += livecells

    if ((gun - gun[multiple]).population > 0):
        return None

    salvo = gun[multiple] - gun

    if salvo.population != 5:
        y = z.destream(salvo)[1:-1]
        y.append(y[-1])
        print(y)

        if (len(set(y)) != 1) or (sum(y) != multiple):
            print('Warning: intermittent glider gun')
            return []

        period = y[-1]
    else:
        period = multiple

    print('Stream period: %d' % period)

    if (period > 10000):
        print('Period too large')
        return []

    for i in range(period):

        h = gun[1]
        g = gun & envelope
        if (g[1] == (h & envelope)):
            gun = g
            break
        gun = h
    else:
        print('Failure 1!')
        return None

    for i in range(period):

        h = gun[1]
        if (h - envelope).population > 0:
            break
        gun = h
    else:
        print('Failure 2!')
        return None

    thing = lt4.pattern("", "LifeHistory")
    thing += gun
    thing = thing[multiple]
    thing = thing[r[0] : r[0] + r[2], r[1] : r[1] + r[3]]
    thing = thing(-r[0], -r[1])

    res = '\n\n#CSYNTH gun_%d costs %d cells.\n#C period %d fullperiod %d bbox %d by %d\n' % (period, r[2] * r[3], period, multiple, r[2], r[3])
    print(res)
    res += thing.rle_string()

    to_update = [(('gun_%d' % period), r[2] * r[3], res)]

    if (period == multiple):
        to_update.append((('guntrue_%d' % period), r[2] * r[3], res.replace('gun_', 'guntrue_')))

    return to_update
