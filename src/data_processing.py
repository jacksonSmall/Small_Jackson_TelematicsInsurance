import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def load_data(filepath='data/simulated_drivers.csv'):
    return pd.read_csv(filepath, parse_dates=['start'])

def encode_categorical(df):
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    categorical_cols = ['weather_conditions', 'traffic_conditions']
    encoded_data = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols), index=df.index)
    df = df.drop(columns=categorical_cols).reset_index(drop=True)
    return pd.concat([df, encoded_df], axis=1)

def aggregate_driver_data(df):
    agg_funcs = {
        'duration': 'mean',
        'avg_speed': 'mean',
        'extreme_brakes': 'sum',
        'extreme_accels': 'sum',
        'late_driving': 'mean',
        'mileage': 'sum'
    }
    categorical_cols = [col for col in df.columns if col.startswith('weather_conditions_') or col.startswith('traffic_conditions_')]
    for col in categorical_cols:
        agg_funcs[col] = 'mean'
    
    aggregated_df = df.groupby('driver_id').agg(agg_funcs).reset_index()
    return aggregated_df

def process_data(filepath='data/simulated_drivers.csv', output_filepath='data/clean_drivers.csv'):
    df = load_data(filepath)
    df = encode_categorical(df)
    driver_df = aggregate_driver_data(df)
    driver_df.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    process_data()
