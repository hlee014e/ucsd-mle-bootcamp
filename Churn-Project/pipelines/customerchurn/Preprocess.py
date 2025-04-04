
import os
import numpy as np
import pandas as pd
import datetime as dt

if __name__ == "__main__":

    base_dir = "/opt/ml/processing"

    # Load raw data
    df = pd.read_csv(f"{base_dir}/input/churndata.csv")


    # Convert date columns
    df["created"] = pd.to_datetime(df["created"])
    df["firstorder"] = pd.to_datetime(df["firstorder"], errors="coerce")
    df["lastorder"] = pd.to_datetime(df["lastorder"], errors="coerce")

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Feature engineering
    df['first_last_days_diff'] = (df['lastorder'] - df['firstorder']).dt.days
    df['created_first_days_diff'] = (df['created'] - df['firstorder']).dt.days

    # Drop unused columns
    df.drop(['custid', 'created', 'firstorder', 'lastorder'], axis=1, inplace=True)

    # One-hot encode 'favday' and 'city'
    df = pd.get_dummies(df, prefix=['favday', 'city'], columns=['favday', 'city'])

    # Pop the label
    y = df.pop("retained")
    y = y.to_numpy().reshape(len(y), 1)

    # Combine label + features
    X = np.concatenate((y, df.to_numpy()), axis=1)
    np.random.shuffle(X)

    # Split
    train, val, test = np.split(X, [int(0.7 * len(X)), int(0.85 * len(X))])

    # Convert to DataFrames
    train_df = pd.DataFrame(train)
    val_df = pd.DataFrame(val)
    test_df = pd.DataFrame(test)

    # Ensure label column is integer
    train_df[0] = train_df[0].astype(int)
    val_df[0] = val_df[0].astype(int)
    test_df[0] = test_df[0].astype(int)

    # Save to CSVs without headers
    os.makedirs(f"{base_dir}/train", exist_ok=True)
    os.makedirs(f"{base_dir}/validation", exist_ok=True)
    os.makedirs(f"{base_dir}/test", exist_ok=True)

    train_df.to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    val_df.to_csv(f"{base_dir}/validation/validation.csv", header=False, index=False)
    test_df.to_csv(f"{base_dir}/test/test.csv", header=False, index=False)
