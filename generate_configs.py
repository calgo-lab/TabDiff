import json
from pathlib import Path

import pandas as pd

DATA_INFO_PATH = Path("data/Info/")


ID_COLS = {
    "MIMIC": "subject_id"
}


DATASETS = {
    "MIMIC": {
        "data_path": Path("data/MIMIC/"),
        "task": "binclass",
        "label": "fall"
    },
}

CONFIG = {
    "name": "<NAME_OF_YOUR_DATASET>",
    "task_type": "[NAME_OF_TASK]",  # binclass or regression
    "header": "infer",
    "column_names": [],
    "num_col_idx": [],  # list of indices of numerical columns
    "cat_col_idx": [],  # list of indices of categorical columns
    "target_col_idx": [],  # list of indices of the target columns (for MLE)
    "val_num": 0,
    "val_path": None,
    "file_type": "csv",
    "data_path": "data/<NAME_OF_YOUR_DATASET>/<NAME_OF_YOUR_DATASET>.csv",  # train
    "test_path": "data/<NAME_OF_YOUR_DATASET>/<NAME_OF_YOUR_DATASET>.csv",  # tst
    "id_col": None,
}

if __name__ == '__main__':
    for dataset, data_info in DATASETS.items():
        config = CONFIG.copy()

        data_path = data_info["data_path"]
        train_csv = data_path / "train.csv"
        test_csv = data_path / "test.csv"
        df = pd.read_csv(train_csv)

        config["id_col"] = ID_COLS.get(dataset, None)
        if config["id_col"] is not None:
            try:
                df = df.drop([config["id_col"]], axis=1)
                print("Dropping the id column")
            except Exception as e:
                print(e, "Skipping id drop")

        columns = df.columns.to_list()

        # Name, task and paths
        config["name"] = dataset
        config["task_type"] = data_info["task"]
        config["data_path"] = str(train_csv)
        config["test_path"] = str(test_csv)

        # Columns
        config["column_names"] = columns
        config["target_col_idx"] = [columns.index(data_info["label"])]

        num_idx = df.select_dtypes(include=["number"]).columns
        num_positions = [df.columns.get_loc(c) for c in num_idx if c != data_info["label"]]

        cat_idx = df.select_dtypes(include=["object", "category", "bool"]).columns
        cat_positions = [df.columns.get_loc(c) for c in cat_idx if c != data_info["label"]]

        config["num_col_idx"] = num_positions
        config["cat_col_idx"] = cat_positions

        with open(DATA_INFO_PATH / f"{dataset}.json", "w") as f:
            print(dataset)
            json.dump(config, f, indent=4)
