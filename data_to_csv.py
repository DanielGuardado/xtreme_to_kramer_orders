import os
from datetime import datetime
import pandas as pd


def data_to_csv(orders):
    df = pd.DataFrame(orders)

    # Generate directory and file names based on current datetime
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    dir_path = os.path.join("tmp", current_datetime)

    # Create directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Save the DataFrame to a CSV in the directory with datetime in filename
    csv_path = os.path.join(dir_path, f"orders_{current_datetime}.csv")

    df.to_csv(csv_path, index=False)

    return csv_path
