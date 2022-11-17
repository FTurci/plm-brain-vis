import numpy as np
import matplotlib.pyplot as plt

trajecotries = np.load('../data/mc_data.npy')
print(trajecotries.shape)

trajectory = trajecotries[0, :, :]
plt.matshow(trajectory)
plt.show()

model = np.load('../data/plm_model.npy')
plt.matshow(model)
plt.show()