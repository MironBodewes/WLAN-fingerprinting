import copy
import numpy as np
from sklearn import neighbors
import pandas as pd
import sklearn.preprocessing as oh
from scan import scan_func
#########
INDEX = 0
INDEX_FINGERPRINT = 0
INDEX_XPOS = 1
INDEX_YPOS = 2
INDEX_BSSID = 4
INDEX_SIGNAL = 5


def calculate_something():
    pass


def knn_func(path: str, amount_of_fingerprints: int):
    HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT = 17  # TODO
    HIGH = HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT

    df = pd.read_pickle(path)
    df_len = len(df)
    print("df.head()=", df.head())
    twenty_percent = int(0.2*df_len)
    current_position_scan = scan_func(amount_of_fingerprints, locate=True)
    current_pos_dict = {}
    for ap in current_position_scan:
        current_pos_dict[ap[INDEX_BSSID]] = ap[INDEX_SIGNAL]
    print("current_pos_dict=", current_pos_dict)

    list_of_dicts = []
    fingerprint_location_map = {}
    for i in range(amount_of_fingerprints):
        list_of_dicts.append({})

    # filling the list of dicts and the fingerprint_location_map
    for i in range(df_len):
        fingerprint_location_map[df.iloc[i, INDEX_FINGERPRINT]] = df.iloc[i,
                                                                          INDEX_XPOS], df.iloc[i, INDEX_YPOS]
        index = df.iloc[i, INDEX_FINGERPRINT]
        keyname = df.iloc[i, INDEX_BSSID]
        value = df.iloc[i, INDEX_SIGNAL]
        list_of_dicts[index][keyname] = value
        print(df.iloc[i, INDEX_FINGERPRINT], " ",
              df.iloc[i, INDEX_BSSID], " ", df.iloc[i, INDEX_SIGNAL])

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
    # print(list_of_dicts)
    # for i in range(len(list_of_dicts)):
    # print(list_of_dicts[i])
    for i in range(len(list_of_dicts)):
        j = 0
        for key in current_pos_dict:
            try:
                myndarray[i, j] = current_pos_dict[key]-list_of_dicts[i][key]
                mylist.append(current_pos_dict[key]-list_of_dicts[i][key])
            except KeyError:  # "tis fine, trust me" # TODO
                pass
            j += 1

    print("meansquarebla=\n", myndarray)
    means = []

    for thing in myndarray:
        means.append(np.mean(thing))
    minimum = abs(means[0])

    for i in range(len(means)):
        if (abs(means[i]) < minimum):
            minimum = means[i]
            minindex = i
    print(means)
    print(minimum)
    print("current location=", fingerprint_location_map[minindex])
    # print("mylist=", mylist)

    training_data = df.iloc[:, :]  # 20% used as training data
    x_train = training_data.iloc[:, 6]
    y_train = training_data.iloc[:, 2:4]
    # print(x_train)
    # print(y_train)


    # knn = neighbors.KNeighborsClassifier(
    #     n_neighbors=1).fit(X_train, Y_train)
if __name__ == "__main__":
    knn_func("accesspoints.pkl", 2)
