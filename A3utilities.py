import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
import graphviz 

def plot_decision_boundary(predict, X, y):
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    delta = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, delta), np.arange(y_min, y_max, delta))
    # Predict the function value for the whole grid
    Z = (predict(np.c_[xx.ravel(), yy.ravel()]) >= 0.5 ) * 1
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[:, 0], X[:, 1], c=y,s=20, cmap=plt.cm.Spectral)
    plt.show()
    
def export_decisiontreegraph(decisiontree,name,depth,_feature_names):
    
    dot_data = tree.export_graphviz(decisiontree, out_file=None,   
                      filled=True, rounded=True,  
                      special_characters=True,feature_names=_feature_names)
    graph = graphviz.Source(dot_data) 
    graph.render(name+ "_depth_" + str(depth))
    
