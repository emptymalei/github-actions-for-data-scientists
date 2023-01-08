# %% [markdown]
# # Jupyter Notebook Demo

# %% [markdown]
# We can run simple jupyter notebooks automatically.

# %%
import matplotlib.pyplot as plt

x = range(10)
y = [i**2 for i in x]

plt.plot(x, y)
# %%
