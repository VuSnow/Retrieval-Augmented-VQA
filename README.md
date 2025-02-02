## Environments 
Create virtualenv:
```
conda create -n RAVQA python=3.11.5
conda activate RAVQA
```

Install required libraries:
```
pip install -r requirements.txt
```

Install other libraries:
```
conda install -c pytorch faiss-gpu -y
```

After that you should install `libjpeg-dev`, `libpng-dev`, `libtiff-dev`, `libavcodec-dev`, `libavformat-dev`, `libswscale-dev`, `libgl1`, `libgl1-mesa-glx` so that CV2 can read image by the above command line:
```
sudo apt update
sudo apt install libjpeg-dev libpng-dev libtiff-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libgl1-mesa-dev libglu1-mesa
```

## Download datasets
All required dataset for running the training and testing step is in Huggingface. And to download:
```
wget https://huggingface.co/datasets/BByrneLab/RAVQAV2Data/resolve/main/RAVQA_v2_data.tar.gz?download=true
```

After downloading and extracting the `tar.gz`, you need to unzip all `.zip` files under `okvqa` folder and `okvqa/pre-extracted/OCR.zip`. By running this terminal:
```
cd /path/to/okvqa/folder
for file in *.zip; do unzip "$file" && rm "$file"; done
```

After obtaining all these file, you should:
- Change the data paths in `configs/okvqa/base_env.jsonnet`. Note that you should change to absolute path to the data file.

## Setup WanDB 
After login your wandb by API key, you should change the `WANDB` in `configs/okvqa/base_env.jsonnet`:
```
"WANDB": {
    "CACHE_DIR": wandb_cache_dir (you can change this to save wandb cache dir in another folder),
    "entity": "change this to your wandb username with no '-org' string",
    "project": "change this to your wandb name project",    
    "tags": "anything you want"
}
```

## Running training models
To run the training step:
```
cd path/to/your/project/folder
python src/main.py config/okvqa/DPR.jsonnet \
        --mode train \ 
        --experiment_name OKVQA_DPR_FullCorpus \
        --modules exhaustive_search_in_testing \
        --opts train.epochs=10 \
                train.batch_size=16 \
                valid.step_size=1 \
                valid.batch_size=16 \
                train.additional.gradient_accumulation_steps=4 \
                train.lr=0.00001
```

## Running testing models
To run the testing step:
```
python main.py ../configs/okvqa/DPR.jsonnet \
    --mode test \
    --experiment_name OKVQA_DPR_FullCorpus \
    --accelerator auto --devices 1 \
    --test_evaluation_name generate_test_set \
    --opts train.batch_size=64 \
            valid.batch_size=64 \
            test.load_epoch=06
```

## Some note:
- If you dont have GPU for running the training step, you should change accelerator and devices of the following lines in main.py file: 
```
additional_args = {
    'accumulate_grad_batches': config.train.additional.gradient_accumulation_steps,
    "default_root_dir": config.saved_model_path,
    'max_epochs': config.train.epochs,
    # 'limit_train_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    # 'limit_val_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    # 'limit_test_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    'logger': [tb_logger, wandb_logger, metrics_history_logger],
    'callbacks': [checkpoint_callback],
    'plugins': plugins,
    'log_every_n_steps': 10,
    'accelerator': "gpu", 
    'devices': "auto",
    # 'strategy': "ddp",
}
```

to
```
additional_args = {
    'accumulate_grad_batches': config.train.additional.gradient_accumulation_steps,
    "default_root_dir": config.saved_model_path,
    'max_epochs': config.train.epochs,
    # 'limit_train_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    # 'limit_val_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    # 'limit_test_batches': 2 if config.data_loader.dummy_dataloader else 1.0,
    'logger': [tb_logger, wandb_logger, metrics_history_logger],
    'callbacks': [checkpoint_callback],
    'plugins': plugins,
    'log_every_n_steps': 10,
    'accelerator': "cpu", 
    # 'devices': "auto",
    # 'strategy': "ddp",
}
```

- If you have some error when running training step like `AttributeError: module 'numpy' has no attribute 'ndarray'` or `AttributeError: type object 'Trainer' has no attribute 'add_argparse_args'"` you should re-check the version of numpy and pytorch-lightning in your system. The version of numpy and pytorch-lightning should be `numpy<2.0` and `pytorch-lightning<2.0` because from the version 2.0, pytorch-lightning has no attribute `add_argparse_args`.
    