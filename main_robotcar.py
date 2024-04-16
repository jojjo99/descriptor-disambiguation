import argparse

import dd_utils
from dataset import RobotCarDataset
from trainer import RobotCarTrainer


def run_function(
    ds_dir,
    local_desc_model,
    retrieval_model,
    local_desc_dim,
    global_desc_dim,
    using_global_descriptors,
    using_vae,
):
    encoder, conf_ns, encoder_global, conf_ns_retrieval = dd_utils.prepare_encoders(
        local_desc_model, retrieval_model, global_desc_dim
    )
    if using_global_descriptors:
        print(f"Using {local_desc_model} and {retrieval_model}-{global_desc_dim}")
    else:
        print(f"Using {local_desc_model}")
    train_ds_ = RobotCarDataset(ds_dir=ds_dir)
    test_ds_ = RobotCarDataset(ds_dir=ds_dir, train=False, evaluate=True)

    trainer_ = RobotCarTrainer(
        train_ds_,
        test_ds_,
        local_desc_dim,
        global_desc_dim,
        encoder,
        encoder_global,
        conf_ns,
        conf_ns_retrieval,
        using_global_descriptors,
        using_vae=using_vae,
    )
    trainer_.evaluate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        default="datasets/robotcar",
        help="Path to the dataset, default: %(default)s",
    )
    parser.add_argument("--use_global", type=int, default=1)
    parser.add_argument("--use_vae", type=int, default=0)

    parser.add_argument(
        "--local_desc",
        type=str,
        default="r2d2",
    )
    parser.add_argument(
        "--local_desc_dim",
        type=int,
        default=128,
    )
    parser.add_argument(
        "--global_desc",
        type=str,
        default="eigenplaces",
    )
    parser.add_argument(
        "--global_desc_dim",
        type=int,
        default=2048,
    )

    args = parser.parse_args()

    run_function(
        args.dataset,
        args.local_desc,
        args.global_desc,
        int(args.local_desc_dim),
        int(args.global_desc_dim),
        bool(args.use_global),
        bool(args.use_vae),
    )
