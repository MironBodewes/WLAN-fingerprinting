import copy
import numpy as np
from sklearn import neighbors
import pandas as pd
import sklearn.preprocessing as oh
from scan import scan_func
#########


def calculate_something():
    pass


def knn_func(amount_of_fingerprints: int):
    HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT = 17  # TODO
    HIGH = HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT

    df = pd.read_csv('accesspoints.csv', sep=';',
                     encoding='ascii', engine='python')
    df_len = len(df)
    print("df.head()=", df.head())
    twenty_percent = int(0.2*df_len)
    # df = pd.DataFrame.sample(df, leny)
    # print(twenty_percent)
    # print(df.iloc[:, 0])
    current_position_scan = scan_func(amount_of_fingerprints, locate=True)
    current_pos_dict = {}
    for ap in current_position_scan:
        current_pos_dict[ap[4]] = ap[5]
    print("current_pos_dict=", current_pos_dict)


    list_of_dicts = []
    for i in range(amount_of_fingerprints):
        list_of_dicts.append({})

    # filling the list of dicts
    for i in range(df_len):
        index = df.iloc[i, 1]
        keyname = df.iloc[i, 5]
        value = df.iloc[i, 6]
        print(type(list_of_dicts[1]))
        # list_of_dicts[index][keyname] = value
        foobar = list_of_dicts[index]
        foobar[keyname] = value
        print(df.iloc[i, 1], " ", df.iloc[i, 5], " ", df.iloc[i, 6])
    # for i in range(df_len):
    #     if (df.iloc[i, 1] == 1):
    #         # column 5 has bssidd, 6 has signal strength
    #         mydict[df.iloc[i, 5]] = df.iloc[i, 6]

    # TODO only use 2.4 GHz (802.11n)
    # TODO use knn instead of mean square?
    # "knn" or just mean square right now
    myndarray = np.zeros((amount_of_fingerprints, HIGH))
    mylist = []

    # calculation of the "distance" of the current position to the fingerprints
    # possible algorithms: sum/mean of:
    # with "a" being the fingerprint of the location which position has to be determined and "b" being another fingerprint
    # a-b
    # (a^2-b^2)
    #
    #
    #
    print(list_of_dicts)
    for i in range(len(list_of_dicts)):
        print(list_of_dicts[i])
    for i in range(len(list_of_dicts)):
        j = 0
        for key in current_pos_dict:
            try:
                myndarray[i, j] = current_pos_dict[key]-list_of_dicts[i][key]
                mylist.append(current_pos_dict[key]-list_of_dicts[i][key])
            except KeyError:  # "tis fine, trust me"
                pass
            j += 1

    # for key in current_pos_dict:
    #     try:
    #         mylist.append(current_pos_dict[key]-mydict[key])
    #     except KeyError:
    #         pass
    print("meansquarebla=\n", myndarray)
    print("mylist=", mylist)

    training_data = df.iloc[:, :]  # 20% used as training data
    x_train = training_data.iloc[:, 6]
    y_train = training_data.iloc[:, 2:4]
    # print(x_train)
    # print(y_train)

    # knn = neighbors.KNeighborsClassifier(
    #     n_neighbors=1).fit(X_train, Y_train)
if __name__ == "__main__":
    knn_func(3)