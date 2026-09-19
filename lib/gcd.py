def gcd(a, b):
    while not b.is_zero():
        a, b = b, a % b

    if a.is_zero():
        return a

    lead = a.coefficients[-1]
    inv_lead = a.field.inverse(lead)

    return a.scalar_mul(inv_lead)

def extended_gcd(a, b):
    zero = a.field_zero()
    one = a.field_one()

    old_r = a
    r = b

    old_s = one
    s = zero

    old_t = zero
    t = one

    while not r.is_zero():
        q = old_r // r

        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    if not old_r.is_zero():
        lead = old_r.coefficients[-1]
        inv_lead = old_r.field.inverse(lead)

        old_r = old_r.scalar_mul(inv_lead)
        old_s = old_s.scalar_mul(inv_lead)
        old_t = old_t.scalar_mul(inv_lead)

    return old_r, old_s, old_t