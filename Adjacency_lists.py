# Storage costs per day

storage_costs = {
    "ATL": 620,
    "LAX": 710,
    "ORD": 680,
    "DFW": 650,
    "DEN": 490,
    "JFK": 780,
    "SFO": 730,
    "SEA": 510,
    "MIA": 570,
    "BOS": 660,
    "LAS": 430,
    "PHX": 440,
    "MSP": 470,
    "DTW": 455,
    "CLT": 395,
}

# Airport info

airport_info = {
    "ATL": {"name": "Hartsfield-Jackson",       "city": "Atlanta, GA"},
    "LAX": {"name": "Los Angeles Intl",          "city": "Los Angeles, CA"},
    "ORD": {"name": "O'Hare Intl",               "city": "Chicago, IL"},
    "DFW": {"name": "Dallas/Fort Worth Intl",    "city": "Dallas, TX"},
    "DEN": {"name": "Denver Intl",               "city": "Denver, CO"},
    "JFK": {"name": "John F. Kennedy Intl",      "city": "New York, NY"},
    "SFO": {"name": "San Francisco Intl",        "city": "San Francisco, CA"},
    "SEA": {"name": "Seattle-Tacoma Intl",       "city": "Seattle, WA"},
    "MIA": {"name": "Miami Intl",                "city": "Miami, FL"},
    "BOS": {"name": "Logan Intl",                "city": "Boston, MA"},
    "LAS": {"name": "Harry Reid Intl",           "city": "Las Vegas, NV"},
    "PHX": {"name": "Phoenix Sky Harbor",        "city": "Phoenix, AZ"},
    "MSP": {"name": "Minneapolis-St. Paul Intl", "city": "Minneapolis, MN"},
    "DTW": {"name": "Detroit Metro",             "city": "Detroit, MI"},
    "CLT": {"name": "Charlotte Douglas Intl",    "city": "Charlotte, NC"},
}

# List of weights + adjacent airports

adjacency = {
    "ATL": {
        "LAX": 28400, "ORD": 11200, "DFW": 13500, "DEN": 17800,
        "JFK": 14100, "SFO": 31200, "SEA": 32600, "MIA":  9800,
        "BOS": 15300, "LAS": 25700, "PHX": 22900, "MSP": 14600,
        "DTW": 10700, "CLT":  4100,
    },
    "LAX": {
        "ATL": 27900, "ORD": 26500, "DFW": 21300, "DEN": 16100,
        "JFK": 35800, "SFO":  6200, "SEA": 11400, "MIA": 33700,
        "BOS": 36900, "LAS":  5300, "PHX":  7800, "MSP": 24100,
        "DTW": 27600, "CLT": 29500,
    },
    "ORD": {
        "ATL": 10900, "LAX": 25800, "DFW": 14700, "DEN": 15200,
        "JFK": 13400, "SFO": 27100, "SEA": 24600, "MIA": 19800,
        "BOS": 11900, "LAS": 22300, "PHX": 20700, "MSP":  5600,
        "DTW":  4800, "CLT":  9200,
    },
    "DFW": {
        "ATL": 13100, "LAX": 20800, "ORD": 14300, "DEN": 10400,
        "JFK": 22700, "SFO": 23500, "SEA": 25900, "MIA": 17600,
        "BOS": 24200, "LAS": 13800, "PHX":  9600, "MSP": 14100,
        "DTW": 16200, "CLT": 12500,
    },
    "DEN": {
        "ATL": 17400, "LAX": 15700, "ORD": 14900, "DFW": 10100,
        "JFK": 24300, "SFO": 14200, "SEA": 13600, "MIA": 25100,
        "BOS": 25800, "LAS":  7900, "PHX":  8300, "MSP": 11700,
        "DTW": 16800, "CLT": 18400,
    },
    "JFK": {
        "ATL": 13800, "LAX": 36100, "ORD": 13100, "DFW": 22400,
        "DEN": 24600, "SFO": 37500, "SEA": 36800, "MIA": 16200,
        "BOS":  3700, "LAS": 31900, "PHX": 28600, "MSP": 18300,
        "DTW": 12100, "CLT": 11600,
    },
    "SFO": {
        "ATL": 30700, "LAX":  6500, "ORD": 26800, "DFW": 23100,
        "DEN": 14600, "JFK": 37200, "SEA":  9800, "MIA": 34600,
        "BOS": 37800, "LAS":  7400, "PHX": 10200, "MSP": 23500,
        "DTW": 27900, "CLT": 31400,
    },
    "SEA": {
        "ATL": 32100, "LAX": 11900, "ORD": 24300, "DFW": 25600,
        "DEN": 13900, "JFK": 35700, "SFO":  9600, "MIA": 36200,
        "BOS": 36500, "LAS": 10300, "PHX": 13700, "MSP": 18600,
        "DTW": 26100, "CLT": 30800,
    },
    "MIA": {
        "ATL":  9500, "LAX": 33200, "ORD": 19400, "DFW": 17200,
        "DEN": 24800, "JFK": 15900, "SFO": 35100, "SEA": 36700,
        "BOS": 17400, "LAS": 27600, "PHX": 24300, "MSP": 21900,
        "DTW": 18700, "CLT":  8200,
    },
    "BOS": {
        "ATL": 14900, "LAX": 36400, "ORD": 11600, "DFW": 23800,
        "DEN": 25300, "JFK":  3400, "SFO": 37600, "SEA": 36300,
        "MIA": 17100, "LAS": 32700, "PHX": 29400, "MSP": 17800,
        "DTW": 11400, "CLT": 12800,
    },
    "LAS": {
        "ATL": 25300, "LAX":  5100, "ORD": 21800, "DFW": 13500,
        "DEN":  8100, "JFK": 31600, "SFO":  7200, "SEA": 10700,
        "MIA": 27900, "BOS": 32400, "PHX":  4600, "MSP": 20100,
        "DTW": 23700, "CLT": 23900,
    },
    "PHX": {
        "ATL": 22500, "LAX":  7600, "ORD": 20400, "DFW":  9300,
        "DEN":  8600, "JFK": 28300, "SFO": 10400, "SEA": 14200,
        "MIA": 24100, "BOS": 29100, "LAS":  4400, "MSP": 19700,
        "DTW": 21800, "CLT": 20600,
    },
    "MSP": {
        "ATL": 14200, "LAX": 23700, "ORD":  5400, "DFW": 13900,
        "DEN": 11500, "JFK": 17900, "SFO": 23200, "SEA": 18900,
        "MIA": 21500, "BOS": 17600, "LAS": 19800, "PHX": 19400,
        "DTW":  6700, "CLT": 13100,
    },
    "DTW": {
        "ATL": 10400, "LAX": 27200, "ORD":  4600, "DFW": 15900,
        "DEN": 16500, "JFK": 11800, "SFO": 27700, "SEA": 25800,
        "MIA": 18400, "BOS": 11100, "LAS": 23400, "PHX": 21600,
        "MSP":  6900, "CLT":  9800,
    },
    "CLT": {
        "ATL":  3900, "LAX": 29200, "ORD":  9000, "DFW": 12300,
        "DEN": 18100, "JFK": 11300, "SFO": 31100, "SEA": 30500,
        "MIA":  7900, "BOS": 12600, "LAS": 23600, "PHX": 20300,
        "MSP": 13400, "DTW":  9600,
    },
}
