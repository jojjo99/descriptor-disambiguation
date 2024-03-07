from pathlib import Path
from pprint import pformat
import argparse

from hloc import extract_features, match_features, triangulation
from hloc import pairs_from_covisibility, pairs_from_retrieval, localize_sfm


parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset",
    type=Path,
    default="datasets/aachen_v1.1",
    help="Path to the dataset, default: %(default)s",
)
parser.add_argument(
    "--outputs",
    type=Path,
    default="outputs/aachen_v1.1",
    help="Path to the output directory, default: %(default)s",
)
parser.add_argument(
    "--num_covis",
    type=int,
    default=20,
    help="Number of image pairs for SfM, default: %(default)s",
)
parser.add_argument(
    "--num_loc",
    type=int,
    default=50,
    help="Number of image pairs for loc, default: %(default)s",
)
args = parser.parse_args()

# Setup the paths
dataset = args.dataset
images = dataset / "images_upright/"
sift_sfm = dataset / "3D-models/aachen_v_1_1"

outputs = args.outputs  # where everything will be saved
reference_sfm = outputs / "sfm_superpoint+superglue"  # the SfM model we will build
sfm_pairs = (
    outputs / f"pairs-db-covis{args.num_covis}.txt"
)  # top-k most covisible in SIFT model
loc_pairs = (
    outputs / f"pairs-query-netvlad{args.num_loc}.txt"
)  # top-k retrieved by NetVLAD
results = outputs / f"Aachen-v1.1_hloc_superpoint+superglue_netvlad{args.num_loc}.txt"

# list the standard configurations available
print(f"Configs for feature extractors:\n{pformat(extract_features.confs)}")
print(f"Configs for feature matchers:\n{pformat(match_features.confs)}")

# pick one of the configurations for extraction and matching
retrieval_conf = extract_features.confs["netvlad"]
feature_conf = extract_features.confs["superpoint_max"]
matcher_conf = match_features.confs["superglue"]

features = extract_features.main(feature_conf, images, outputs)

pairs_from_covisibility.main(sift_sfm, sfm_pairs, num_matched=args.num_covis)
sfm_matches = match_features.main(
    matcher_conf, sfm_pairs, feature_conf["output"], outputs
)

triangulation.main(reference_sfm, sift_sfm, images, sfm_pairs, features, sfm_matches)

global_descriptors = extract_features.main(retrieval_conf, images, outputs)
pairs_from_retrieval.main(
    global_descriptors,
    loc_pairs,
    args.num_loc,
    query_prefix="query",
    db_model=reference_sfm,
)
loc_matches = match_features.main(
    matcher_conf, loc_pairs, feature_conf["output"], outputs
)

localize_sfm.main(
    reference_sfm,
    dataset / "queries/*_time_queries_with_intrinsics.txt",
    loc_pairs,
    features,
    loc_matches,
    results,
    covisibility_clustering=False,
)  # not required with SuperPoint+SuperGlue
