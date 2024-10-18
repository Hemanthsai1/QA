import pandas as pd

def read_csv(file):
    """Read a CSV file and return its content as a string."""
    df = pd.read_csv(file)
    return df.to_string()  # Convert the DataFrame to string
