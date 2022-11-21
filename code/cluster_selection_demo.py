# I use pd datafram to do selection as this is cleanest.
# This script shows examples of how to select a sub model by a given cluster
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_model_cluster(cluster_name):
    df = pd.read_csv('../data/roi_clusters.csv')
    whole_brain_model = np.load('../data/plm_model.npy')
    cluster_rois = df[df['cluster_name'] == cluster_name]

    indicesL = cluster_rois['roi_index'].to_numpy()
    indicesR = np.copy(indicesL)
    indicesR += 180
    indices = np.hstack((indicesL, indicesR))

    cluster_model = whole_brain_model[indices, :]
    cluster_model = cluster_model[:, indices]
    return cluster_model

def get_model_type(cluster_type):
    df = pd.read_csv('../data/roi_clusters.csv')
    allowed_types = df['cluster_type'].unique()
    print('allowed cluster_types are:', allowed_types)

    whole_brain_model = np.load('../data/plm_model.npy')
    rois = df[df['cluster_type'] == cluster_type]
    indicesL = rois['roi_index'].to_numpy()

    indicesR = np.copy(indicesL)
    indicesR += 180
    indices = np.hstack((indicesL, indicesR))

    cluster_model = whole_brain_model[indices, :]
    cluster_model = cluster_model[:, indices]
    return cluster_model


def get_model_arranged_by_cluster_type():
    df = pd.read_csv('../data/roi_clusters.csv')
    df = df.sort_values(by=['cluster_type'])
    indicesL = df['roi_index'].to_numpy()
    indicesR = np.copy(indicesL)
    indicesR += 180
    indices = np.hstack((indicesL, indicesR))

    # let's try and sort the whole thingy in a second!
    whole_brain_model = np.load('../data/plm_model.npy')
    sorted_model = whole_brain_model[indices, :]
    sorted_model = sorted_model[:, indices]
    return sorted_model

df = pd.read_csv('../data/roi_clusters.csv')
print(df)

model = get_model_cluster('early visual cortex')
plt.matshow(model)
plt.title('Model of the early visual cortex cluster')
plt.show()

model = get_model_type('Visual')
plt.matshow(model)
plt.title('Model of all visual clusters')
plt.show()


whole_brain_model = np.load('../data/plm_model.npy')
sorted_model = get_model_arranged_by_cluster_type()
fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
ax = ax.ravel()
ax[0].matshow(whole_brain_model)
ax[1].matshow(sorted_model)
fig.suptitle('Comparing raw model vs sorted-by-type model')
plt.show()

# shows symmetry
fig, ax = plt.subplots(1, 3, sharex=True, sharey=True)
LL_model = sorted_model[0:180, 0:180]
RR_model = sorted_model[180:, 180:]
LR_model = sorted_model[0:180, 180:]
np.fill_diagonal(LR_model, 0)
ax = ax.ravel()
ax[0].matshow(LL_model)
ax[0].set(title='L-L')
ax[1].matshow(RR_model)
ax[1].set(title='R-R')
ax[2].matshow(LR_model)
ax[2].set(title='L-R')
fig.suptitle('Showing model symmetry for sorted-by-type model')
plt.show()
