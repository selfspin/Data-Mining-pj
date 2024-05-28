import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

current_dir = os.getcwd()
sys.path.append(os.path.dirname(os.path.join(current_dir, "..")))
from utils.preprocess import *

def age_stats(data: pd.DataFrame):
    
    fig, (ax1, ax2) = plt.subplots(2, 1, constrained_layout=True)
    boys = data[data["gender"] == 1]
    girls = data[data["gender"] == 0]
    
    max_age = max(boys["age"].max(), girls["age"].max())
    print("The oldest one: %d years old..." % max_age)
    
    bins = list(range(15, 41))
    
    ax1.hist(boys["age"], bins, label="boys")
    # ax1.set_title("Age of boys")
    ax1.set_xlabel("Age")
    ax1.set_ylabel("Count")
    ax1.legend()
    ax2.hist(girls["age"], bins, color="pink", label="girls")
    # ax2.set_title("Age of girls")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Count")
    ax2.legend()
    
    fig.suptitle("Age Distribution")
    plt.savefig("./output/age_dist.pdf")
    # plt.show()
    

def income_stats(data: pd.DataFrame):
    
    career_counts = data["career"].value_counts()
    top_careers = career_counts.head(7)
    top_careers_list = top_careers.index.tolist()
    if "nan" in top_careers_list:
        top_careers_list.remove('nan')
    
    filtered_df = data[data['career'].isin(top_careers_list)]
    filtered_df['career'] = pd.Categorical(filtered_df['career'], categories=top_careers_list, ordered=True)
    filtered_df.sort_values(by='career', inplace=True)
    
    filtered_df.boxplot(column='income', by='career', figsize=(12, 8))
    plt.suptitle("")
    
    plt.title('Income Distribution by Career')
    # plt.xlabel('Career')
    plt.ylabel('Income')

    plt.tight_layout()
    # plt.show()
    plt.savefig("./output/income_stat.pdf")


def career_stats(data: pd.DataFrame):
    
    career_counts = data["career"].value_counts()
    top_careers = career_counts.head(7)
    top_careers_list = top_careers.index.tolist()
    if "nan" in top_careers_list:
        top_careers_list.remove('nan')

    filtered_df = data[data['career'].isin(top_careers_list)]
    filtered_df['career'] = pd.Categorical(filtered_df['career'], categories=top_careers_list, ordered=True)
    filtered_df.sort_values(by='career', inplace=True)
    
    grouped_df = filtered_df.groupby(['career', 'gender']).size().unstack()
    
    grouped_df.plot(kind='bar', stacked=False, color=["pink", "C0"], figsize=(9, 6))
    plt.legend(title='Gender', labels=['Female', 'Male'])
    
    plt.xticks(rotation=30)
    plt.xlabel("")
    plt.ylabel("Count")
    # plt.show()
    plt.title("Career Stats")
    plt.tight_layout()
    plt.savefig("./output/career_stat.png")


def score_stats(data: pd.DataFrame):
    
    score_df = data[["attr", "sinc", "intel", "fun", "amb", "shar"]]
    
    sns.heatmap(
        score_df.corr(),
        annot=True,
        cmap="YlOrRd",
        fmt=".2f"
    )
    
    plt.title("Score Corr Matrix")
    # plt.show()
    plt.savefig("./output/score_stat.pdf")


if __name__ == '__main__':
    
    # 1. Load the raw data.
    data = load_data("./data/speed_data_data.csv")
    data = combine_career(data, json_path="./data/career.json")
    # 2. Divide the data into two parts: with income and w/o income.
    no_income_data, income_data = partial_by_income(data)
    # 3. Drop the na records.
    no_income_data, income_data = truncate_nan(no_income_data), truncate_nan(income_data)
    # 4. Aggregate the data.
    aggr_no_income_data, aggr_income_data = aggregate(no_income_data), aggregate(income_data)
    aggr_data = pd.concat([aggr_no_income_data, aggr_income_data], axis=0)
    
    age_stats(aggr_data)
    career_stats(aggr_data)
    income_stats(aggr_income_data)
    score_stats(aggr_data)