"""Main module."""

# %%
import pandas as pd
import numpy as np
import plotly.express as px

# %%
def rfm_score_generator(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57):
    
    if invoiceNo == "":
        invoiceNo = day_bought
    
    
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)
    RFM.drop(columns = day_bought, inplace = True)
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2)
    RFM["Customer_segment"] = np.where(RFM['RFM_Score'] >
                                      4.5, "Top",
                                      (np.where(
                                        RFM['RFM_Score'] > 4,
                                        "High value",
                                        (np.where(
    RFM['RFM_Score'] > 3,
                             "Medium Value",
                             np.where(RFM['RFM_Score'] > 1.6,
                            'Low Value', 'Lost'))))))

    
    
    
    return(RFM)

# %%
def rfm_tree_map(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57):
    
    if invoiceNo == "":
        invoiceNo = day_bought
    
    
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)
    RFM.drop(columns = day_bought, inplace = True)
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2)
    RFM["Customer_segment"] = np.where(RFM['RFM_Score'] >
                                      4.5, "Top",
                                      (np.where(
                                        RFM['RFM_Score'] > 4,
                                        "High value",
                                        (np.where(
    RFM['RFM_Score'] > 3,
                             "Medium Value",
                             np.where(RFM['RFM_Score'] > 1.6,
                            'Low Value', 'Lost'))))))
    
    RFM_1 = RFM.groupby("Customer_segment")[[customerID]].count().reset_index()
    RFM_1.rename(columns = {customerID: "Size Segment"}, inplace = True)
    
    fig1 = px.treemap(
      RFM_1,
      path=[px.Constant("<br>"), 'Customer_segment'],
      values='Size Segment',  
      color='Size Segment',
      color_continuous_scale=px.colors.sequential.matter,
      custom_data=RFM_1[['Customer_segment', 'Size Segment']],
        
    )
    
   

    fig1.show()
    
    
    
    return

# %%
def rfm_pie_chart(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57):
    
    if invoiceNo == "":
        invoiceNo = day_bought
    
    
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)
    RFM.drop(columns = day_bought, inplace = True)
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2)
    RFM["Customer_segment"] = np.where(RFM['RFM_Score'] >
                                      4.5, "Top",
                                      (np.where(
                                        RFM['RFM_Score'] > 4,
                                        "High value",
                                        (np.where(
    RFM['RFM_Score'] > 3,
                             "Medium Value",
                             np.where(RFM['RFM_Score'] > 1.6,
                            'Low Value', 'Lost'))))))
    
    RFM_1 = RFM.groupby("Customer_segment")[[customerID]].count().reset_index()
    RFM_1.rename(columns = {customerID: "Size Segment"}, inplace = True)
    
    
    fig = px.pie(RFM_1, values='Size Segment', names='Customer_segment', title='Customer Segment Pie Chart', color_discrete_sequence=px.colors.sequential.matter)
    
    
   
    fig.show()
    
    
    return



