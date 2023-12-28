import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def plot_tree(dtree, feature_names, class_names, figsize=(20, 10)):
    def plot_node(node, depth, parent_pos, node_pos, ax, dtree, feature_names, class_names):
        x, y = node_pos
        #color and style for decision and leaf nodes
        if dtree.children_left[node] != dtree.children_right[node]:  # Decision node
            node_style = dict(boxstyle="round,pad=0.3", fc="orange", ec="black", lw=2)
        #leaf node
        else:  
            node_style = dict(boxstyle="round,pad=0.3", fc="lightgreen", ec="black", lw=2)
        
        #properties of the node
        samples = dtree.n_node_samples[node]
        gini = dtree.impurity[node]
        value = dtree.value[node][0]
        predominant_class = class_names[np.argmax(value)]
        
        #the text for the node
        if dtree.children_left[node] != dtree.children_right[node]:  # Decision node
            feature = feature_names[dtree.feature[node]]
            threshold = dtree.threshold[node]
            text = f'{feature} <= {threshold:.4f}\ngini = {gini:.3f}\nsamples = {samples}\nvalue = {value}\nclass = {predominant_class}'
        #leaf node
        else: 
            text = f'gini = {gini:.3f}\nsamples = {samples}\nvalue = {value}\nclass = {predominant_class}'
        
        #text on the plot
        ax.text(x, y, text, horizontalalignment='center', verticalalignment='center', bbox=node_style)
        
        #connecting line
        if parent_pos is not None:
            ax.plot([parent_pos[0], x], [parent_pos[1], y], 'k-', lw=2)

    def recursive_plot_tree(dtree, ax, feature_names, class_names, depth=0, parent_pos=None, node=0, x=0.5, y=1, x_step=0.5):
        plot_node(node, depth, parent_pos, (x, y), ax, dtree, feature_names, class_names)
        
        #if node is not a leaf, draw its children
        if dtree.children_left[node] != dtree.children_right[node]:
            new_x_step = x_step / 2
            #left child
            recursive_plot_tree(dtree, ax, feature_names, class_names, depth+1, (x, y), dtree.children_left[node], x-new_x_step, y-0.2, new_x_step)
            #right child
            recursive_plot_tree(dtree, ax, feature_names, class_names, depth+1, (x, y), dtree.children_right[node], x+new_x_step, y-0.2, new_x_step)

    #figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    recursive_plot_tree(dtree.tree_, ax, feature_names, class_names)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    plt.show()

#decision tree classifier
decision_tree = DecisionTreeClassifier(max_depth=3)
decision_tree.fit(X_train, y_train)

#plot diagram
plot_tree(decision_tree, X_train.columns, class_names=['Fully Paid', 'Not Fully Paid'])