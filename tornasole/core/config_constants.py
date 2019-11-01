import os

TORNASOLE_CONFIG_DEFAULT_WORKER_NAME = "worker_0"
TORNASOLE_CONFIG_FILE_PATH_ENV_STR = "TORNASOLE_CONFIG_FILE_PATH"
DEFAULT_CONFIG_FILE_PATH = "/opt/ml/input/config/debughookconfig.json"
TORNASOLE_CONFIG_REDUCTION_CONFIGS_KEY = "reduction_configs"
TORNASOLE_CONFIG_SAVE_CONFIGS_KEY = "save_configs"
TORNASOLE_CONFIG_OUTDIR_KEY = "LocalPath"
TORNASOLE_CONFIG_DRYRUN_KEY = "dry_run"
TORNASOLE_CONFIG_RDN_CFG_KEY = "reduction_config"
TORNASOLE_CONFIG_INCLUDE_REGEX_KEY = "include_regex"
TORNASOLE_CONFIG_SAVE_ALL_KEY = "save_all"
DEFAULT_SAGEMAKER_TORNASOLE_PATH = "/opt/ml/output/tensors"
TORNASOLE_DEFAULT_COLLECTIONS_FILE_NAME = "worker_0_collections.json"
"""
TORNASOLE_CONFIG_MAX_WAIT_STEPS is used in trial.py

It defines the maximum number of steps that the trial will watch as incomplete,
before marking half of them as complete.
"""
TORNASOLE_CONFIG_MAX_WAIT_STEPS = int(os.getenv("TORNASOLE_CONFIG_MAX_WAIT_STEPS", 1000))
