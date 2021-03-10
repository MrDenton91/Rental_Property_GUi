def dollar_per_sqrt(price,sqrfeet):
    dps = []
    for key, val in enumerate(price):
        dps.append( float((price[key].replace('$','').replace(',',''))) / float((sqrfeet[key]) ))
    
    return max(dps), sum(dps)/len(dps), min(dps), dps[int(len(dps)/2)]
