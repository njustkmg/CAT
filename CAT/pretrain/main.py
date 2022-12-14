

import os
import logging

from pretrain.utils.hydra_utils import print_cfg
from pretrain.utils.main_utils import (
    apply_random_seed,
    init_data_loader,
    init_hydra_config,
    init_model,
    init_trainer,
)
import warnings
warnings.filterwarnings('ignore')

def main():
    # init cfg
    cfg = init_hydra_config(mode="pretrain")
    apply_random_seed(cfg)
    print_cfg(cfg)

    # init dataloader
    loaders = []
    cfg, train_loader = init_data_loader(cfg, mode="pretrain", is_train=True)
    loaders.append(train_loader)
    if cfg.TEST.KNN_VALIDATION:
        _, val_loader = init_data_loader(cfg, mode="pretrain", is_train=False)
        loaders.append(val_loader)

    # init model
    cfg, model = init_model(cfg)
    # init trainer
    cfg, trainer = init_trainer(cfg)
    
    # train
    logging.info(
        f"Start Training: Total Epoch - {cfg.TRAINER.max_epochs}, Precision: {cfg.TRAINER.precision}"
    )
    trainer.fit(model, *loaders)


if __name__ == "__main__":
    main()
