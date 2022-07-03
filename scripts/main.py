import pandas as pd
import sys

sys.dont_write_bytecode = True

from util import yaml_param
from util import adjust
from util import plot

if __name__ == "__main__":

    argv = sys.argv
    ref_csv_dir = argv[1]
    result_csv_dir = argv[2]
    config_dir = argv[3]
    output_dir = argv[4]

    print("Loading yaml file ...", end="")
    ref_param = yaml_param.YamlParam()
    result_param = yaml_param.YamlParam()
    save_param = yaml_param.YamlParam()
    config = adjust.input_yaml_param(config_dir, ref_param, result_param)
    adjust.input_save_param(config, save_param)
    print("Completed!!")

    print("Loading csv files ...", end="")
    ref_df_org = pd.read_csv(ref_csv_dir)
    result_df_org = pd.read_csv(result_csv_dir)
    print("Completed!!")

    print("Adjusting unit ...", end="")
    adjust.unit_adjust(ref_param, ref_df_org)
    adjust.unit_adjust(result_param, result_df_org)
    del ref_df_org, result_df_org
    print("Completed!!")

    print("Adjusting the start time ...", end="")
    if adjust.adjust_start_time(ref_param, result_param) is -1:
        sys.exit(1)
    print("Completed!!")

    print("Adjusting the end time ...", end="")
    adjust.adjust_end_time(ref_param, result_param)
    print("Completed!!")

    print("Synchronizing time...", end="")
    ref_param.df, result_param.df = adjust.sync_time(ref_param, result_param)
    del ref_param.df_temp, result_param.df_temp
    print("Completed!!")

    print("Output graph ...", end="")
    plot.output_graph(ref_param, result_param, output_dir, save_param)
