import copy
import numpy as np
from sklearn import neighbors
import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn.preprocessing as oh
from scan import scan_func
#########
INDEX = 0
INDEX_FINGERPRINT = 0
INDEX_XPOS = 1
INDEX_YPOS = 2
INDEX_BSSID = 4
INDEX_SIGNAL = 5
INDEX_LOCATION = 7


def calculate_something():
    pass


def knn_func(path: str, amount_of_fingerprints: int):
    HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT = 100  # TODO
    HIGH = HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT

    df = pd.read_pickle(path)
    df_len = len(df)
    print("df.head()=\n", df.head(500))
    twenty_percent = int(0.2*df_len)
    current_position_scan = scan_func(amount_of_fingerprints, locate=True)
    current_pos_dict = {}
    for ap in current_position_scan:
        current_pos_dict[ap[INDEX_BSSID]] = ap[INDEX_SIGNAL]
    print("current_pos_dict=", current_pos_dict)

    list_of_dicts = []  # make sure this is filled at index 1 with fingerprint 1. It might be necessary to sort the fingerprints in the dataframe

    fingerprint_location_map = {}
    for i in range(amount_of_fingerprints):
        list_of_dicts.append({})

    # filling the list of dicts and the fingerprint_location_map
    for i in range(df_len):
        fingerprint_location_map[df.iloc[i, INDEX_FINGERPRINT]] = df.iloc[i,
                                                                          INDEX_XPOS], df.iloc[i, INDEX_YPOS], df.iloc[i, INDEX_LOCATION]
        index = df.iloc[i, INDEX_FINGERPRINT]
        keyname = df.iloc[i, INDEX_BSSID]
        value = df.iloc[i, INDEX_SIGNAL]
        list_of_dicts[index][keyname] = value
        # print(df.iloc[i, INDEX_FINGERPRINT], " ",
        #   df.iloc[i, INDEX_BSSID], " ", df.iloc[i, INDEX_SIGNAL], df.iloc[i, INDEX_LOCATION])

    # TODO only use 2.4 GHz (802.11n)
    # TODO use knn instead of mean square?
    # "knn" or just mean square right now
    score_array = np.zeros((amount_of_fingerprints, HIGH))
    mylist = []
    score_array2 = np.zeros((amount_of_fingerprints, HIGH))
    # key is the fingerprint_number, value is how many APs are in BOTH the current_position_scan and the fingerprint scan
    accesspoint_matches = {}
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
                score_array[i, j] = abs(
                    current_pos_dict[key]-list_of_dicts[i][key])
                score_array2[i, j] = abs((
                    current_pos_dict[key]-list_of_dicts[i][key])**2)
                mylist.append(current_pos_dict[key]-list_of_dicts[i][key])
                if(i not in accesspoint_matches):
                    accesspoint_matches[i] = 1
                else:
                    accesspoint_matches[i] +=1
            except KeyError:  # "tis fine, trust me" # TODO
                pass
                # accesspint_nonmatches[i]+=1
            j += 1
    print("ap matches=", accesspoint_matches)
    #print("scores=\n", score_array)
    #print("scores2=\n", score_array2)
    means = []

    for score in score_array:
        means.append(np.mean(score))
    minimum = abs(means[0])
    minindex = 0

    for i in range(len(means)):
        if (abs(means[i]) < minimum):
            minimum = abs(means[i])
            minindex = i

    print(means)
    print("minimum=", minimum, "minindex=", minindex)
    print("current location=", fingerprint_location_map[minindex])
    # print("mylist=", mylist)

    # knn
    # TODO reshape this so that every accesspoint-signal_strength is a new feature
    # x_train, x_test, y_train, y_test = train_test_split(
    #     df.iloc[INDEX_FINGERPRINT], df.iloc[INDEX_LOCATION])

    # print(x_train)
    # print(y_train)
    # knn = neighbors.KNeighborsClassifier(
    #     n_neighbors=1).fit(x_train, y_train)


if __name__ == "__main__":
    config_df = pd.read_csv("config.csv")
    fingerprint_number = config_df.loc[:, 'fingerprint_id'][0]
    knn_func("accesspoints.pkl", fingerprint_number)
