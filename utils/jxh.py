import pandas as pd 


def preprocess_raw_for_modeling(dating:pd.DataFrame):
    # 删除每个值的无效字符
    def remove_xters(feature):
        return feature.replace("b'",'').replace("'","")

    for feature in dating.select_dtypes(include = ['object']).columns:
        dating[feature] = dating[feature].apply(lambda x: remove_xters(x))

    # 字段转化
    dating['samerace'] = dating['samerace'].astype('int')   # 是否同种族--转化为01整型变量
    for number in [3.0, 5.0, 6.0, 7.0, 8.0]:
        dating['met'] = dating['met'].replace(number, 0)  # 是否见过--转化为是否见过01变量

    # 字段创建
    dating['age_diff'] = dating['age'] - dating['age_o']

    # 字段删除
    dating.drop(['has_null','wave'], axis = 1, inplace= True)
    dating.drop(['age','age_o'], axis = 1, inplace = True)  # 已经转化为年龄差异
    dating.drop([column_name for column_name in dating.columns if column_name.startswith('d_')], axis = 1, inplace = True) # d_*将一些数字特征分类，但没啥意义
    dating.drop('field',axis = 1, inplace = True)                           # 包含价值观的重叠的职业，划分不够清晰
    dating.drop(['decision_o','decision'], axis = 1, inplace = True)        # 跟match字段过于相关
    dating.drop('expected_num_interested_in_me', axis = 1, inplace = True)   # NA过多

    return dating