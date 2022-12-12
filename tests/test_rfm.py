# %%
import pandas as pd
from rfm_segmentation import rfm_segmentation as rfm 
import warnings
warnings.filterwarnings("ignore")

# %%
dt = pd.read_csv("/Users/esmilasahakyan/Desktop/Marketing Analytics/Marketing project/Data/Bonus/BonusCustomersales_New.csv")

# %%
rfm.rfm_score_generator(dt, "Totalcost", "Day Bought", "Customer Name", "Unnamed: 0")

# %%
rfm.rfm_tree_map(dt, "Totalcost", "Day Bought", "Customer Name",  "Unnamed: 0")

# %%
rfm.rfm_pie_chart(dt, "Totalcost", "Day Bought", "Customer Name", "Unnamed: 0")


