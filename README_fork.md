1. Place your datasets in the `data` folder (train.csv and test.csv). e.g data/MIMIC/train.csv and data/MIMIC.test.csv
2. In `generate_config.py` add your datasets in `DATASETS` with the following format:
```python
"MIMIC": {
    "data_path": Path("data/MIMIC/"),
    "task": "binclass",
    "label": "fall"
},
```
and if there's an id column, add it to `ID_COLS` dictionary as such: 
where the key should correspond to the key for the dataset that was used in `DATASETS`

```python
ID_COLS = {
    "MIMIC": "subject_id"
}
```

3. In the root of the project run 

```
python generate_configs.py
```
and then for each dataset run:
```
python process_dataset.py --dataname <NAME_OF_YOUR_DATASET>
```
4. Finally, to generate the synthetic data, for each dataset run
```
python main.py --dataname <NAME_OF_DATASET> --mode train --no_wandb
```

This fork:
- Adds automatic info.json generation
- Adds median as an imputation method
- Reintroduces NaNs in the generated data
- Generated IDs (if any were specified in the dataset)