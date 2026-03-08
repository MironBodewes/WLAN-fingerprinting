import copy
import time
import numpy as np
import pandas as pd
import sklearn.preprocessing as oh
from linux_scan import scan_func
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from sklearn import neighbors, neural_network, tree
from sklearn import naive_bayes
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

#########
INDEX = 0
INDEX_FINGERPRINT = 0
INDEX_XPOS = 1
INDEX_YPOS = 2
INDEX_BSSID = 4
INDEX_SIGNAL = 5
INDEX_LOCATION = 7


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def compute_naive_bayes(x_train, y_train, x_test, y_test):
    # var_smoothing can have a huge influence on the result!
    # smoothies=[1e-9,1e-8,1e-7,1e-6,1e-5,0.0001,0.001,0.01,0.1,0.2,0.4,0.7]
    # for sm in smoothies:
    clf = naive_bayes.GaussianNB(var_smoothing=0.001)
    clf.fit(x_train, y_train)

    train_accu = 100 * clf.score(x_train, y_train)
    test_accu = 100 * clf.score(x_test, y_test)
    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))
    return train_accu, test_accu


def compute_svm(x_train, y_train, x_test, y_test):
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    train_accu = []
    test_accu = []
    for kern in kernels:
        clf = svm.SVC(kernel=kern, cache_size=200, random_state=0)
        clf.fit(x_train, y_train)
        y_prediction_train = clf.predict(x_train)
        y_prediction_test = clf.predict(x_test)
        train_accu.append(100*accuracy_score(y_train, y_prediction_train))
        test_accu.append(100*accuracy_score(y_test, y_prediction_test))
        print("train accuracy: {} %".format(train_accu[-1]))
        print("test accuracy: {} %".format(test_accu[-1]))
    return kernels, train_accu, test_accu

# compute_svm()


def compute_nearest_neighbors(x_train, y_train, x_test, y_test):
    # unsupervised learning method that does NOT use y_train.
    clf = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')

    clf.fit(x_train)
    # indices
    distances, indices = clf.kneighbors(x_train)
    y_prediction_train = []

    # Also in indices sind die Indexe von x_ges/x_train/y_train, die am nähsten an den Features dran sind.
    # Natürlich bekommen wir dann auch 100% train_accuracy.
    #
    for i in indices[:, 0]:
        y_prediction_train.append(y_train[i])

    distances, indices2 = clf.kneighbors(x_test)
    y_prediction_test = []
    for i in indices2[:, 0]:
        y_prediction_test.append(y_train[i])

    train_accu = 100*accuracy_score(y_train, y_prediction_train)
    test_accu = 100*accuracy_score(y_test, y_prediction_test)
    # print(train_accu, train_accu2, test_accu, test_accu2)
    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))
    return train_accu, test_accu


def compute_KNeighbors_classifier(x_train, y_train, x_test, y_test):
    clf = KNeighborsClassifier(n_neighbors=1, algorithm="ball_tree")
    clf.fit(x_train, y_train)
    train_accu = 100*clf.score(x_train, y_train)
    test_accu = 100*clf.score(x_test, y_test)
    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))
    return train_accu, test_accu


def compute_nearest_centroid(x_train, y_train, x_test, y_test):
    from sklearn.neighbors import NearestCentroid
    centroid_metrics = ["euclidean", "manhattan", "l2"]
    print("x_test.shape=", x_test.shape)

    # return is in the loop right now so we only use euclidean
    for _metric in centroid_metrics:
        clf = NearestCentroid(metric=_metric)
        clf.fit(x_train, y_train)
        print(clf.score(x_train, y_train))
        y_prediction_train = clf.predict(x_train)
        y_prediction_test = clf.predict(x_test)

        train_accu = 100 * clf.score(x_train, y_train)
        test_accu = 100 * clf.score(x_test, y_test)
        train_accu2 = accuracy_score(y_train, clf.predict(x_train))  # same as train_accu
        print("train accuracy: {} %".format(train_accu))
        print("test accuracy: {} %".format(test_accu))
        return train_accu, test_accu


def compute_perceptron(x_train, y_train, x_test, y_test,
                       penalty="l2"):
    from sklearn.linear_model import Perceptron
    clf = Perceptron(penalty=penalty, random_state=0)
    # clf.partial_fit(x_train, y_train, classes=np.unique(y_train))
    clf.fit(x_train, y_train)
    print("x_test.shape=", x_test.shape)

    train_accu = 100*clf.score(x_train, y_train)
    test_accu = 100*clf.score(x_test, y_test)
    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))
    return train_accu, test_accu


def compute_mlp(x_train, y_train, x_test, y_test, max_iter=2000):
    mlp = neural_network.MLPClassifier(max_iter=max_iter)
    mlp.fit(x_train, y_train)
    train_accu = 100*mlp.score(x_train, y_train)
    test_accu = 100*mlp.score(x_test, y_test)
    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))
    return train_accu, test_accu


def compute_decisiontree_classifier(x_train, y_train, x_test, y_test, max_depth=None, random_state=23):
    clf = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    clf.fit(x_train, y_train)
    y_prediction_train = clf.predict(x_train)
    y_prediction_test = clf.predict(x_test)
    # End of your Code

    train_accu = 100*clf.score(x_train, y_train)
    test_accu = 100*clf.score(x_test, y_test)

    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))

    cm = confusion_matrix(y_test, y_prediction_test)
    print(cm)
    plt.show()
    return train_accu, test_accu


def compute_randomforest_classifier(x_train, y_train, x_test, y_test, n_estimators=100, max_depth=None, random_state=56, plot_decisionboundary=True):
    clf = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    clf.fit(x_train, y_train)

    train_accu = 100*clf.score(x_train, y_train)
    test_accu = 100*clf.score(x_test, y_test)

    print("train accuracy: {} %".format(train_accu))
    print("test accuracy: {} %".format(test_accu))

    return train_accu, test_accu


def compute_all_small_data(x_train, y_train, x_test, y_test):
    # print(x_train.shape)
    accs = []
    print("randomforest")
    accs.append(compute_randomforest_classifier(x_train, y_train, x_test, y_test,
                n_estimators=100, max_depth=None, random_state=56, plot_decisionboundary=True))
    print("decision_tree")
    accs.append(compute_decisiontree_classifier(x_train, y_train, x_test, y_test))
    print("naive_bayes")
    accs.append(compute_naive_bayes(x_train, y_train, x_test, y_test))
    print("svm")
    accs.append(compute_svm(x_train, y_train, x_test, y_test))
    print("nearest_neighbors")
    accs.append(compute_nearest_neighbors(x_train, y_train, x_test, y_test))
    print("nearest_centroid")
    accs.append(compute_nearest_centroid(x_train, y_train, x_test, y_test))
    print("perceptron")
    accs.append(compute_perceptron(x_train, y_train, x_test, y_test))
    print("mlp")
    accs.append(compute_mlp(x_train, y_train, x_test, y_test))
    return accs

def call_functions(x_train, y_train, x_test, y_test):
    trainaccs_dict = {}
    testaccs_dict = {}
    kernels = []
    functions = [compute_randomforest_classifier, compute_decisiontree_classifier,
             compute_decisiontree_classifier, compute_naive_bayes, compute_svm, compute_nearest_neighbors,
             compute_nearest_centroid, compute_perceptron, compute_mlp, compute_KNeighbors_classifier]
    for function in functions:
        print(function.__name__)
        start = time.time()
        if function == compute_svm:
            kernels, trainaccs_svm, testaccs_svm = compute_svm(x_train, y_train, x_test, y_test)
            for i in range(len(kernels)):
                print("kernel=", kernels[i], "\ntrainacc=",
                      trainaccs_svm[i], "testacc=", testaccs_svm[i])
                trainaccs_dict[function.__name__+" "+kernels[i]] = trainaccs_svm[i]
                testaccs_dict[function.__name__+" "+kernels[i]] = testaccs_svm[i], ((time.time()-start)/4)
        else:
            returned_tuple = function(x_train, y_train, x_test, y_test)
            trainaccs_dict[function.__name__] = returned_tuple[-2]
            testaccs_dict[function.__name__] = returned_tuple[-1], time.time()-start
            print(time.time()-start)
    amount_of_rows=100
    TIME_IN_SECONDS_STRING = "time in seconds"
    # sorting the testaccs by value... there has to be a better way...
    sorted_list = sorted(testaccs_dict.items(), key=lambda x: x[1][0])
    testacc_dict_sorted = {}
    values0 = []
    values1 = []
    names = []
    for key, values in sorted_list:
        names.append(key)
        values0.append(values[0])
        values1.append(values[1])
    values0_tuple = tuple(values0)
    testacc_dict_sorted = {"test_accuracy in %": tuple(values0), TIME_IN_SECONDS_STRING: tuple(values1)}

    # GROUPED PLOTS from https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    # Plot 1
    x = np.arange(len(testaccs_dict))  # the label locations
    height = 0.4  # the width of the bars
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')
    ax: Axes = ax  # this line is necessary for code recommendations (seeing what methods the class has)..
    for attribute, measurement in testacc_dict_sorted.items():
        offset = height * multiplier
        barContainers = ax.barh(x + offset, measurement, height, label=attribute)
        ax.bar_label(barContainers, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # plt.title("accuracy_score of select classifiers for a sample size of "+str(amount_of_rows))
    ax.set_title("accuracy_score of select classifiers for a sample size of "+str(amount_of_rows))
    ax.set_yticks(x + height, names)
    ax.legend(loc='upper right', ncols=1)
    plt.show()

    # Plot 2 with zoom in
    fig, ax = plt.subplots(layout='constrained')
    ax: Axes = ax  # this line is necessary for code recommendations (seeing what methods the class has)..
    for attribute, measurement in testacc_dict_sorted.items():
        if (attribute == TIME_IN_SECONDS_STRING):
            continue
        offset = height * multiplier
        barContainers = ax.barh(x + offset, measurement, height, label=attribute)
        ax.bar_label(barContainers, padding=3)
        multiplier += 1
    # Add some text for labels, title and custom x-axis tick labels, etc.
    # plt.title("accuracy_score of select classifiers for a sample size of "+str(amount_of_rows))
    ax.set_title("accuracy_score of select classifiers for a sample size of "+str(amount_of_rows))
    ax.set_xlabel('test accuracy in %')
    ax.set_yticks(x + height, names)
    # plt.legend(loc='upper left', ncols=3)
    ax.legend(loc='lower right', ncols=1, labels=["test_accuracy in %"])
    ax.set_xlim(90, 100)
    plt.show()
    return trainaccs_dict, testaccs_dict

# currently used for comparing two datasets with different machine learning algorithms. the name is missleading


def knn_func2(path: str, path2: str, amount_of_fingerprints: int):
    HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT = 100  # TODO
    HIGH = HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT
    UNIQUE_APS_TOTAL = 120  # TODO remove magic numbers
    df = pd.read_pickle(path)
    df2 = pd.read_pickle(path2)
    bssid_map = {}
    """bssid_map key: bssid, value: index of that bssid
    """
    fingerprint_count = df.loc[:, "fingerprint"].max()+1
    fingerprint_count2 = df2.loc[:, "fingerprint"].max()+1
    print("fingerprint_count=", fingerprint_count, "fingerprint_count2=", fingerprint_count2)
    x_train = np.zeros((fingerprint_count, HIGH))
    y_train = np.zeros(fingerprint_count)
    x_test = np.zeros((fingerprint_count2, HIGH))
    y_test = np.zeros(fingerprint_count2)

    # train
    print("unique locations=", df.loc[:, "location_name"].unique())
    print("type", type(df.loc[:, "location_name"].unique()[0]))
    le = LabelEncoder().fit(df.loc[:, "location_name"].unique())
    fingerprint_location_map = {}
    for i in range(len(df)):
        fingerprint_location_map[df.iloc[i, INDEX_FINGERPRINT]] = df.iloc[i, INDEX_XPOS], df.iloc[i, INDEX_YPOS], df.iloc[i, INDEX_LOCATION]
        bssid = df.iloc[i, INDEX_BSSID]
        if bssid not in bssid_map:
            # TODO lookup table [O(1)] should be faster than a map [O(log n)] ? idk
            bssid_map[bssid] = len(bssid_map)

        signal = df.iloc[i, INDEX_SIGNAL]
        fingerprint_id = df.iloc[i, INDEX_FINGERPRINT]
        x_train[fingerprint_id, bssid_map[bssid]] = signal
        location = df.iloc[i, INDEX_LOCATION]
        y_train[fingerprint_id] = le.transform([location])[0]

    # test
    print("shapes=", x_train.shape,
          y_train.shape, x_test.shape)
    fingerprint_location_map_test = {}
    for i in range(len(df2)):
        fingerprint_location_map_test[df2.iloc[i, INDEX_FINGERPRINT]] = df2.iloc[i, INDEX_XPOS], df2.iloc[i, INDEX_YPOS], df2.iloc[i, INDEX_LOCATION]
        bssid = df2.iloc[i, INDEX_BSSID]
        if bssid not in bssid_map:
            # TODO lookup table should be faster than a map? idk
            continue
        signal = df2.iloc[i, INDEX_SIGNAL]
        fingerprint_id = df2.iloc[i, INDEX_FINGERPRINT]
        location = df2.iloc[i, INDEX_LOCATION]
        x_test[fingerprint_id, bssid_map[bssid]] = signal
        y_test[fingerprint_id] = le.transform([location])[0]

    knn: neighbors.KNeighborsClassifier = neighbors.KNeighborsClassifier(
        n_neighbors=1).fit(x_train, y_train)
    predict = knn.predict(x_test)
    print("predict=", predict)
    predict = predict.astype(int)
    print(type(predict[0]))
    print("inverse transform of predict:", le.inverse_transform(predict.tolist()))
    print("Testdaten (nicht Traningsdaten) Signalwerte (ersten 10):\n", x_test[:, :10])

    j = 0
    correct_predictions = 0
    for i in predict:
        print(bcolors.WARNING, "predict=", i, "predicted location is ",
              le.inverse_transform([i])[0], bcolors.ENDC, "real location is ", fingerprint_location_map_test[j][2])

        if le.inverse_transform([i])[0] == fingerprint_location_map_test[j][2]:
            correct_predictions += 1
        j += 1
    print("knn accuracy=", correct_predictions*100/len(predict), "%")
    call_functions(x_train, y_train, x_test, y_test)
    #accs = compute_all_small_data(x_train, y_train, x_test, y_test)

    pass


def knn_func(path: str, fingerprint_count: int, verbose_level: int = 0):
    """this function compares the signal strengths at the current position with all other fingerprints previously made and spits out the nearest fingerprint(s)"""
    HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT = 100  # TODO
    HIGH = HIGHEST_AMOUNT_OF_ACCESSPOINTS_IN_A_FINGERPRINT
    UNIQUE_APS_TOTAL = 120  # TODO remove magic numbers

    df = pd.read_pickle(path)
    df_len = len(df)
    # print("df.head()=\n", df.head(11))
    twenty_percent = int(0.2*df_len)
    current_position_scan = scan_func(fingerprint_count, locate=True)
    current_pos_dict = {}
    for ap in current_position_scan:
        current_pos_dict[ap[INDEX_BSSID]] = ap[INDEX_SIGNAL]
    # print("current_pos_dict=", current_pos_dict)

    list_of_dicts = []  # make sure this is filled at index 1 with fingerprint 1. It might be necessary to sort the fingerprints in the dataframe

    fingerprint_location_map = {}
    for i in range(fingerprint_count):
        list_of_dicts.append({})

    # filling the list of dicts and the fingerprint_location_map
    # key is fingerprint_id, value is xpos etc.
    for i in range(df_len):
        fingerprint_location_map[df.iloc[i, INDEX_FINGERPRINT]] = df.iloc[i, INDEX_XPOS], df.iloc[i, INDEX_YPOS], df.iloc[i, INDEX_LOCATION]
        index = df.iloc[i, INDEX_FINGERPRINT]
        keyname = df.iloc[i, INDEX_BSSID]
        value = df.iloc[i, INDEX_SIGNAL]
        list_of_dicts[index][keyname] = value
        # print(df.iloc[i, INDEX_FINGERPRINT], " ",
        #   df.iloc[i, INDEX_BSSID], " ", df.iloc[i, INDEX_SIGNAL], df.iloc[i, INDEX_LOCATION])

    # TODO only use 2.4 GHz (802.11n)
    # TODO use knn instead of mean square?
    # "knn" or just mean square right now
    # 'score_arrays' is a matrix
    score_arrays = np.zeros((fingerprint_count, HIGH))
    """
    score_arrays
    The signal strengths are compared with all other fingerprints
    Every array is filled by iterating over all APs at the current location and getting the difference between the current signal_strength and the signal strength from a fingerprint
    """
    accesspoint_nonmatches = np.zeros((fingerprint_count, HIGH))
    mylist = []
    score_array2 = np.zeros((fingerprint_count, HIGH))
    # key is the fingerprint_number, value is how many APs are in BOTH the current_position_scan and the fingerprint scan
    accesspoint_matches = {}  # TODO make this an array!?
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
    #     print(list_of_dicts[i])
    print("size=", len(current_pos_dict))
    print(current_pos_dict)
    for i in range(len(list_of_dicts)):
        j = 0
        for key in current_pos_dict:
            try:
                score_arrays[i, j] = abs(
                    current_pos_dict[key]-list_of_dicts[i][key])
                score_array2[i, j] = abs((
                    current_pos_dict[key]-list_of_dicts[i][key])**2)
                mylist.append(current_pos_dict[key]-list_of_dicts[i][key])
                if (i not in accesspoint_matches):
                    accesspoint_matches[i] = 1
                else:
                    accesspoint_matches[i] += 1
            except KeyError:  # "tis fine, trust me" # TODO
                pass
                accesspoint_nonmatches[i] += 1
            j += 1
    # print("ap matches=", accesspoint_matches)
    # print("scores=\n", score_arrays)
    # print("scores2=\n", score_array2)
    means = []
    i = 0
    for score in score_arrays:
        means.append(np.sum(score)/accesspoint_matches[i])
        i += 1

    lowest_found_score = abs(means[0])
    minindex = 0
    for i in range(len(means)):
        if (abs(means[i]) < lowest_found_score):
            lowest_found_score = abs(means[i])
            minindex = i
    if (verbose_level >= 1):
        print("Errors to other fingerprints are:\n")
        print(means)
        print("minimum=", lowest_found_score, "minindex=", minindex)
    print("current location=", fingerprint_location_map[minindex])
    # print("mylist=", mylist)
    """change the format of the df to use it with knn.
    format should be bssidd -> list[fingerprint_ID,signal_strength]
    format in df is currently: 
    fingerprint_ID, bssid, signalstrengthc
    ...
    """
    x_train = np.zeros((fingerprint_count, UNIQUE_APS_TOTAL))
    y_train = np.zeros(fingerprint_count)
    # print(x_train.shape)
    # print(y_train.shape)
    """ We need to map bssids to integers so we can use the integers as index for our ndarray.
        algorithm: for every bssid, check if it's already in the map. if not, add it to the map.
    
    """
    bssid_map = {}
    """bssid_map key: bssid, value: index of that bssid
    """
    from sklearn import preprocessing
    for i in range(len(df)):
        bssid = df.iloc[i, INDEX_BSSID]
        if bssid not in bssid_map:
            # TODO lookup table should be faster than a map? idk
            bssid_map[bssid] = len(bssid_map)
        signal = df.iloc[i, INDEX_SIGNAL]
        fingerprint_id = df.iloc[i, INDEX_FINGERPRINT]
        location = df.iloc[i, INDEX_LOCATION]
        # print(type(fingerprint_id))
        # print(type(bssid))
        x_train[fingerprint_id, bssid_map[bssid]] = signal

        y_train[fingerprint_id] = fingerprint_id
        # TODO make sure this doesn't copy the whole array for every step
        # np.append(x_train, (df.loc[INDEX_SIGNAL],df.loc[INDEX_FINGERPRINT]))
    """LabelBinarizer
        currently not in use...
    """
    # lb=preprocessing.LabelBinarizer()
    # lb.fit(y_train)
    # print("x_train=",x_train)
    # knn
    # TODO reshape this so that every accesspoint-signal_strength is a new feature
    # x_train, x_test, y_train, y_test = train_test_split(
    #     df.iloc[INDEX_FINGERPRINT], df.iloc[INDEX_LOCATION])

    # print(x_train)
    # print(y_train)
    # should be unique aps total PLUS current scan
    x_test = np.zeros(UNIQUE_APS_TOTAL)
    knn = neighbors.KNeighborsClassifier(
        n_neighbors=1).fit(x_train, y_train)
    for bssid in current_pos_dict:
        try:
            x_test[bssid_map[bssid]] = current_pos_dict[bssid]
        except KeyError:
            print("bssid ", bssid,
                  "of the current scan was not found in a previous scan.")

    predict = knn.predict(x_test.reshape(1, -1))
    predict = int(predict[0])
    print(bcolors.WARNING, "predict=", predict, "location is ",
          fingerprint_location_map[predict], bcolors.ENDC)
    return "current location="+str(fingerprint_location_map[minindex])


if __name__ == "__main__":
    config_df = pd.read_csv("data/config.csv")
    # fingerprint_count formerly fingerprint_number is the count of
    # fingerprints. fingerprint_id should be the individual id of a fingerprint
    amount_of_fingerprints = config_df.loc[:, 'fingerprint_id'][0]
    knn_func2("data/accesspoints.pkl0", "data/accesspoints.pkl2", amount_of_fingerprints)
