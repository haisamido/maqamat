#f2=frequency_from_cents(110,0,1200)


#print(frequency_from_cents(293.665,200,1200))
# print(cents_from_frequency(293.665,329.628 ,1200))
# print(frequency_from_cents(293.665,200,1200))
# c=0
# cu=np.array([c])
# cs=np.array([c])

# for key in maqam:
#     c=c+key
#     cu=np.append(cu,c)
#     cs=np.append(cs,key)

# maqam_def[maqam_argv].update({ "cents":cu })

# print(maqam_def[maqam_argv]['cents'])
#maqam_cents = maqam_def[maqam_argv]['cents']

tones = {
    "cents": {
        200: {"interval": 1,    "string": "1",   "tone_name": "tone"},
        100: {"interval": 0.5,  "string": "1/2", "tone_name": "semi-tone"},
        50:  {"interval": 0.25, "string": "1/4", "tone_name": "quarter-tone"}
    },
    "intervals": {
        1:    {"cents": 200, "text": "1",     "tone_name": "tone"},
        1.5:  {"cents": 300, "text": "1 1/2", "tone_name": "tone"},
        0.5:  {"cents": 100, "text": "1/2",   "tone_name": "semi-ttone"},
        0.25: {"cents": 50,  "text": "1/4",   "tone_name": "quarter-tone"},
        0.75: {},
        1.25: {}
    },
    "text_intervals": {
        "1": 1,
        "1/2": 0.5,
        "1 1/4": 1.25,
        "1 1/2": 1.5,
        "3/4": 0.75,
        "1/4": 0.25
    }
}

# print(tones)

frequencies = {
    "D4": 293.665
}

jins = {
    "Ajam": {
        "cents": [200, 200, 100],
        "qarar": {},
        "hassas": {}
    },
    "Bayat": {
        "cents": [150, 150, 200],
        "qarar": {},
        "tonics": ["D4", "G4", "A4", "E4", "C4"],
        "modulation_from_ghammaz": ["Nahwand", "Rast", "Hijaz"],
        "hassas": {}
    },
    "Hijaz": {},
    "Kurd": {},
    "Nawa-Athar": {},
    "Sikah": {},
    "Nahwand": {
        "cents": [200, 200, 100, 200],
        "qarar": {},
        "hassas": {}},
    "Rast": {},
    "Saba": {},
    "Zamzam": {},
    "Must'ar": {},
    "Spare":{
        "cents":[200]
    }
}

maqam_def = {
    "Bayat": {"tonic": "D4", "ajnas": ["Bayat", "Nahwand", "Spare"]},
    "Ajam" :{"ajnas": ["Ajam","Spare"]} 
}

i=0
maqam_argv='Bayat'

for key in maqam_def[maqam_argv]['ajnas']:
    print(key)
    l=len(jins[key]['cents'])
    if i == 0:
        maqam = np.array(jins[key]['cents'])
    else:
        # maqam = np.append(maqam,jins[key]['cents'][1:l])
        maqam = np.append(maqam,jins[key]['cents'])
    i=i+1

