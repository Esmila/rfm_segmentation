"""Main module."""

# %%
import pandas as pd
import numpy as np
import plotly.express as px

# %%
def rfm_score_generator(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57):
   
    """

    Parameters
    ----------
    data : the data of customers you want to segment
        
    totalPaid : the monetary value (quantity * unit_price)
        
    day_bought : the date of the purchase
        
    customerID : unique identifier for  each customer
        
    invoiceNo : unique identifier for each purchase
         (Default value = ""), if missing take date of each purchase
    format_ : the date format for day_bought column
         (Default value = '%d.%m.%Y')
    R_w : the weight given to Recency to calculate RFM Score
         (Default value = 0.15)
    F_w : the weight given to Frequency to calculate RFM Score
         (Default value = 0.28)
    M_w : the weight given to Monetary value to calculate RFM Score
         (Default value = 0.57)

    Returns
    The RFM (dataframe) with added columns of Recency, Freqency, Monetary Ranks both normalized and not normalized, RFM Score, and the Segment the Customer belongs to, e.g Loyal customer.
    The Maximum RFM Score is 5.

    """
    
    #if we don't have unique numbers that differentiate each purchase we take the day of the purchase as invoice number for calculating the frequency
    #how many days the customer vistied to the store
    if invoiceNo == "":
        invoiceNo = day_bought
    
    #changing the type of date column  to datetime
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    
    #Calculating the unique number of days/purchases for frequency
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    
    #choosing max day_bought to calculate recency later, summing total_paid to calculate total monetary value for each customer, taking already calculated frequency value,
    # as all the values of frequency are the same for each customer we can take max/min/first doesn't matter
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    
    #taking the last day occuring in the date column and calculating recency from that date
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)

    #ranking Recency, Frequency, Monetary Values, recency from largest to smallest, as the smaller the batter 
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    #normalizing the ranks
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    
    #calculating the rfm score
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2) #rounding the everything in RFM to 2 decimals
    
    
    #segmenting customers 
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
def rfm_tree_map(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57, color_ = px.colors.sequential.matter):
    
    """

    Parameters
    ----------
    data : the data of customers you want to segment
        
    totalPaid : the monetary value (quantity * unit_price)
        
    day_bought : the date of the purchase
        
    customerID : unique identifier for  each customer
        
    invoiceNo : unique identifier for each purchase
         (Default value = ""), if missing take date of each purchase
    format_ : the date format for day_bought column
         (Default value = '%d.%m.%Y')
    R_w : the weight given to Recency to calculate RFM Score
         (Default value = 0.15)
    F_w : the weight given to Frequency to calculate RFM Score
         (Default value = 0.28)
    M_w : the weight given to Monetary value to calculate RFM Score
         (Default value = 0.57)
    color_ : the colors for treemap
         (Default value = px.colors.sequential.matter)

    Returns
    The RFM tree map 

    """
    
    #if we don't have unique numbers that differentiate each purchase we take the day of the purchase as invoice number for calculating the frequency
    #how many days the customer vistied to the store
    if invoiceNo == "":
        invoiceNo = day_bought
    
    #changing the type of date column  to datetime
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    
    #Calculating the unique number of days/purchases for frequency
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    
    #choosing max day_bought to calculate recency later, summing total_paid to calculate total monetary value for each customer, taking already calculated frequency value,
    # as all the values of frequency are the same for each customer we can take max/min/first doesn't matter
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    
    #taking the last day occuring in the date column and calculating recency from that date
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)

    #ranking Recency, Frequency, Monetary Values, recency from largest to smallest, as the smaller the batter 
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    #normalizing the ranks
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    
    #calculating the rfm score
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2) #rounding the everything in RFM to 2 decimals
    
    
    #segmenting customers 
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

    
    #calculating the size of each segment based on how many customers it has
    RFM_1 = RFM.groupby("Customer_segment")[[customerID]].count().reset_index()
    #renaming the cutsomer id to size segment
    RFM_1.rename(columns = {customerID: "Size Segment"}, inplace = True)
    
    #creating the tree map
    fig1 = px.treemap(
      RFM_1,
      path=[px.Constant("<br>"), 'Customer_segment'],
      values='Size Segment',  
      color='Size Segment',
      color_continuous_scale=color_,
      custom_data=RFM_1[['Customer_segment', 'Size Segment']],
        
    )
    
   

    fig1.show()
    
    
    
    return

# %%
def rfm_pie_chart(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57, color_ = px.colors.sequential.matter):
    
    """

    Parameters
    ----------
    data : the data of customers you want to segment
        
    totalPaid : the monetary value (quantity * unit_price)
        
    day_bought : the date of the purchase
        
    customerID : unique identifier for  each customer
        
    invoiceNo : unique identifier for each purchase
         (Default value = ""), if missing take date of each purchase
    format_ : the date format for day_bought column
         (Default value = '%d.%m.%Y')
    R_w : the weight given to Recency to calculate RFM Score
         (Default value = 0.15)
    F_w : the weight given to Frequency to calculate RFM Score
         (Default value = 0.28)
    M_w : the weight given to Monetary value to calculate RFM Score
         (Default value = 0.57)
    color_ : the colors for treemap
         (Default value = px.colors.sequential.matter)

    Returns
    The RFM pie chart

    """
    
    #if we don't have unique numbers that differentiate each purchase we take the day of the purchase as invoice number for calculating the frequency
    #how many days the customer vistied to the store
    if invoiceNo == "":
        invoiceNo = day_bought
    
    #changing the type of date column  to datetime
    data[day_bought] = pd.to_datetime(data[day_bought],format= format_)
    
    #Calculating the unique number of days/purchases for frequency
    data["Frequency"]= data.groupby(customerID)[invoiceNo].transform('nunique')
    
    #choosing max day_bought to calculate recency later, summing total_paid to calculate total monetary value for each customer, taking already calculated frequency value,
    # as all the values of frequency are the same for each customer we can take max/min/first doesn't matter
    RFM = data.groupby(customerID).agg({day_bought: "max", "Frequency": "max", totalPaid : "sum"}).reset_index()
    
    #taking the last day occuring in the date column and calculating recency from that date
    recent_date = RFM[day_bought].max()
    RFM['Recency'] = RFM[day_bought].apply(lambda x: (recent_date - x).days)

    #ranking Recency, Frequency, Monetary Values, recency from largest to smallest, as the smaller the batter 
    RFM['R_rank'] = RFM['Recency'].rank(ascending=False)
    RFM['F_rank'] = RFM['Frequency'].rank(ascending=True)
    RFM['M_rank'] = RFM[totalPaid].rank(ascending=True)
    #normalizing the ranks
    RFM['R_rank_norm'] = (RFM['R_rank']/RFM['R_rank'].max())*100
    RFM['F_rank_norm'] = (RFM['F_rank']/RFM['F_rank'].max())*100
    RFM['M_rank_norm'] = (RFM['F_rank']/RFM['M_rank'].max())*100
    
    #calculating the rfm score
    RFM['RFM_Score'] = R_w * RFM['R_rank_norm']+ F_w * RFM['F_rank_norm']+ M_w * RFM['M_rank_norm']
    RFM['RFM_Score'] *= 0.05 #rank 5 is the top 
    RFM = RFM.round(2) #rounding the everything in RFM to 2 decimals
    
    
    #segmenting customers 
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

    
    #calculating the size of each segment based on how many customers it has
    RFM_1 = RFM.groupby("Customer_segment")[[customerID]].count().reset_index()
    #renaming the cutsomer id to size segment
    RFM_1.rename(columns = {customerID: "Size Segment"}, inplace = True)


    
    fig = px.pie(RFM_1, values='Size Segment', names='Customer_segment', title='Customer Segment Pie Chart', color_discrete_sequence=color_)
    
    
   
    fig.show()
    
    
    return



