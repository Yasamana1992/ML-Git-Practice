import pandas as pd

def statistics(df, features_list):
    opr_list = ["sum", "mean", "max", "min", "count"]
    features = df.columns
    seri = []
    not_found = 0
    for feature in features_list:
        if feature in features:
            column = df[feature]
            for opr in opr_list:
                tool = getattr(column, opr)()
                seri.append({"feature" : feature, "operation" : opr, "value" : tool})
        else:
            not_found += 1
    if not_found == len(features_list):
        return "feature not found"
    else:
        sts_df = pd.DataFrame(seri)
        return sts_df