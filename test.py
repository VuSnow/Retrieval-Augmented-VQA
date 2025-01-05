python main.py ../configs/okvqa/DPR.jsonnet \
    --mode train \
    --experiment_name OKVQA_DPR_FullCorpus  \
    --modules exhaustive_search_in_testing \
    --opts train.epochs=10 \
            train.batch_size=8 \
            valid.step_size=1 \
            valid.batch_size=32 \
            train.additional.gradient_accumulation_steps=4 \
            train.lr=0.00001