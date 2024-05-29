import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.preprocess import *

features_name = ["gender", "age", "income", "goal", "career"]


# 基本特征对最终得分的箱线图
def base_feature_boxplot(noincome_data: pd.DataFrame, income_data: pd.DataFrame):
    for idx, feature_name in enumerate(features_name):
        if feature_name == 'income':
            feature = income_data[feature_name].to_numpy()
            like = income_data['like'].to_numpy()
        else:
            feature = np.concatenate([income_data[feature_name].to_numpy(), noincome_data[feature_name].to_numpy()])
            like = np.concatenate([income_data['like'].to_numpy(), noincome_data['like'].to_numpy()])

        if feature_name == 'age' or feature_name == 'goal':
            feature = feature.astype(int)
        elif feature_name == 'gender':
            def replace_value(x):
                return 'female' if x == 0 else 'male'

            # 使用np.vectorize替换值
            vectorized_replace = np.vectorize(replace_value)
            feature = vectorized_replace(feature)
        elif feature_name == 'career':
            like = like[feature != 'nan']
            feature = feature[feature != 'nan']

            def replace_value(x):
                if x == "economist/business":
                    return 'economist/\nbusiness'
                elif x == "social workers":
                    return "social\nworkers"
                else:
                    return x

            # 使用np.vectorize替换值
            vectorized_replace = np.vectorize(replace_value)
            feature = vectorized_replace(feature)
        else:
            def replace_value(x):
                multiple = x // 10000
                from_income = int(multiple)
                to_income = int(multiple + 1)
                return f"{from_income:02d}w-\n{to_income:02d}w"

            # 使用np.vectorize替换值
            vectorized_replace = np.vectorize(replace_value)
            feature = vectorized_replace(feature)

        data = pd.DataFrame({
            'Feature': feature,
            'Like': like
        })

        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Feature', y='Like', data=data, order=sorted(np.unique(feature)))

        # 添加标题和标签
        plt.title('Box Plot of Like by Feature')
        plt.xlabel(feature_name)
        plt.ylabel('like')

        if feature_name == 'career' or features_name == 'income':
            plt.xticks(fontsize=6)

        # 显示图形
        plt.savefig(f'output/boxplots/like-{feature_name}.png', format='png', dpi=300)


if __name__ == "__main__":
    # 1. Load the raw data.
    data = load_data()
    data = combine_career(data, json_path="./data/career.json")
    # 2. Divide the data into two parts: with income and w/o income.
    no_income_data, income_data = partial_by_income(data)
    # 3. Drop the na records.
    no_income_data, income_data = truncate_nan(no_income_data), truncate_nan(income_data)
    # 4. Aggregate the data.
    aggr_no_income_data, aggr_income_data = aggregate(no_income_data), aggregate(income_data)

    base_feature_boxplot(aggr_no_income_data, aggr_income_data)
