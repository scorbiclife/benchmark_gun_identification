def clip(pattern, rect):
    return pattern[rect[0]:rect[0]+rect[2], rect[1]:rect[1]+rect[3]]

def is_gun(pattern, true_period):
    """Test if the given pattern is a gun.

    A pattern is a gun only if the pattern and the resulting gliders after `true_period`
    are separately evolvable. This filters out non-guns having heisenburp-like reactions.
    """
    gliders = pattern[true_period] - pattern
    for phase in range(true_period):
        if (pattern[true_period + phase] == pattern[phase] + gliders[phase]
                and (pattern[phase] & gliders[phase]).population == 0):
            continue
        return False
    return True

def get_bounding_box_naive(gun, true_period, period, naive_envelope, unclipped_envelope):
    """Get the bounding box with a naive algorithm or throw an error
    if the naive algorithm cannot be applied.

    We iterate the gun, remove the gliders whenever it crosses
    our minimal bounding box, and hope that the resulting phases
    match the actual phases of the gun.
    The phases would not match when there is a heisenburp-like reaction
    at the edge of the envelope.
    """
    envelope = naive_envelope
    gun_phases = [gun[i] for i in range(true_period)]
    output_gliders = gun[true_period] - gun
    to_be_glider = output_gliders[-period] - output_gliders

    for i in range(true_period):
        if (gun - gun_phases[i]).population != 0:
            raise Error("Naive bounding box algorithm failed.")
        # Remove gliders until there isn't or the gun fits inside envelope
        while (gun - envelope).population != 0:
            if (to_be_glider - gun).population != 0:
                envelope = clip(unclipped_envelope, (envelope + gun).getrect())
                break
            gun -= to_be_glider
            to_be_glider = to_be_glider[-period]
        gun = gun[1]
        to_be_glider = to_be_glider[1]
    return envelope.getrect()

def get_bounding_box(gun, true_period, period, envelope_lower_bound):
    """Get the bounding box with a slower but always succeeding algorithm. """
    output_gliders = gun[true_period] - gun
    to_be_glider = output_gliders[-period] - output_gliders
    envelope = gun
    for i in range(true_period):
        # For each phase, delete gliders while the resulting pattern is a gun
        # until the pattern fits in the known lower bound of the bounding box
        # or there isn't a glider to delete.
        while (gun - envelope_lower_bound).population != 0:
            if (to_be_glider - gun).population != 0:
                break
            if not is_gun(gun - to_be_glider, true_period):
                break
            gun -= to_be_glider
            to_be_glider = to_be_glider[-period]
        envelope += gun
        gun = gun[1]
        to_be_glider = to_be_glider[1]
    return envelope.getrect()

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

    geater = lt4.pattern("bo$2bo$3o4$5b2o$5bo$6b3o$8bo!", "b3s23")

    eater = z.replace(geater[:3, :3], geater[100], orientations='rotate4reflect', n_phases=2)

    if (eater.population != 7):
        return None

    x += eater

    x = x[128]

    true_period = x.oscar(eventual_oscillator=False, maxexp=20)['period']

    print('True period: %d' % true_period)

    if (true_period > 100000):
        print('Period too large')
        return []

    gun = lt4.pattern("", "b3s23")
    gun += livecells

    if ((gun - gun[true_period]).population > 0):
        return None

    salvo = gun[true_period] - gun

    if salvo.population != 5:
        y = z.destream(salvo)[1:-1]
        y.append(y[-1])
        print(y)

        if (len(set(y)) != 1) or (sum(y) != true_period):
            print('Warning: intermittent glider gun')
            return []

        period = y[-1]
    else:
        period = true_period

    print('Stream period: %d' % period)

    if (period > 10000):
        print('Period too large')
        return []

    w = lt4.pattern("", "LifeHistory")
    w += z[-2097152]
    w = w[4194304]


    band = w.layers()[1]

    pbb = envelope - band
    r1 = z.getrect()
    r2 = z[1024].getrect()

    pbb += pbb(r1[0] - r2[0], r1[1] - r2[1])

    # The bounding box related to `r` is a lower bound but is not exact.
    # It does not take into account the sparks at the output glider lane.
    r = pbb.getrect()
    if (r is None) or (len(r) != 4):
        return None

    envelope_lower_bound = clip(envelope, r)
    r = envelope_lower_bound.getrect()

    # Find and use the phase where the gun is totally inside the
    # lower bound of the bounding box.
    # There is a possibility that this test could fail,
    # but this doesn't seem to occur in practice.
    for _ in range(true_period):
        gun_clipped = gun & envelope_lower_bound
        if is_gun(gun_clipped, true_period):
            gun = gun_clipped
            break
        gun = gun[1]
    else:
        print('Failure 1!')
        return None

    # Performance optimization:
    # we try the naive but fast algorithm first
    # and then try the slow but accurate one
    try:
        bounding_box = get_bounding_box_naive(
                gun,
                true_period,
                period,
                naive_envelope=envelope_lower_bound,
                unclipped_envelope=envelope)
    except:
        bounding_box = get_bounding_box(
                gun,
                true_period,
                period,
                envelope_lower_bound=envelope_lower_bound)
    true_envelope = clip(envelope, bounding_box)

    gun_canonical_phase = gun
    for _ in range(true_period):
        if (gun[1] - true_envelope).population > 0:
            gun_canonical_phase = gun
            break
        gun = gun[1]
    else:
        print('Failure 2!')
        return None

    r = bounding_box
    multiple = true_period
    thing = lt4.pattern("", "LifeHistory")
    thing += gun_canonical_phase
    thing = thing[multiple]
    thing = clip(thing, bounding_box)
    thing = thing(-r[0], -r[1])

    res = '\n\n#CSYNTH gun_%d costs %d cells.\n#C period %d fullperiod %d bbox %d by %d\n' % (period, r[2] * r[3], period, multiple, r[2], r[3])
    print(res)
    res += thing.rle_string()

    to_update = [(('gun_%d' % period), r[2] * r[3], res)]

    if (period == multiple):
        to_update.append((('guntrue_%d' % period), r[2] * r[3], res.replace('gun_', 'guntrue_')))

    return to_update
