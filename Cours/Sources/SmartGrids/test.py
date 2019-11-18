""" Test des dictionnaires """

from datetime import datetime, date, time, timedelta
import Profile

def step(inputs):
    # Get inputs
    deltas = {}
    for eid, attrs in inputs.items():
        print(eid)
        print(attrs)
        for attr, values in attrs.items():
            print(attr)
            print(values)
            print(sum(values.values()))

def main():
    print("ok")
    dic = {'Model_0': {'delta': {'src_eid_0': 1, 'src_eid_1': 2}}, 'Model_1': {'delta': {'src_eid_1': 42}} }
    #step(dic)
    START = '2014-01-01 00:00:00'
    date = datetime(2014, 1, 1, 0, 0, 0, 0)
    print(date)
    i=3
    date2 = date+timedelta(minutes=(1*i))
    print("ok")
    print(date2)
    prof = Profile.Profile(1, 24, 0)
    print("Debut export")
    prof.exportCSV(START_DATE=date, step_size=60, filename="profile.csv", modelname='ModelProfil')
    print("Fin export")
if __name__ == "__main__":
    # execute only if run as a script
    main()
