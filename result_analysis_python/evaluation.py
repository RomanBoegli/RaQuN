import os

from eval.visualization import bar_plots
from eval.data.result_loading import load_results
from eval.visualization.tables import create_tabular_overview, create_num_of_comp_overview, \
    create_model_stats_overview, create_argo_subset_stats_overview

# Run the following in your terminal, if you do not have matplotlib installed
# python -m pip install -U pip
# python -m pip install -U matplotlib

# Change the path to evaluate different results
data_directory = "./../results"
experiment_subject_dir = "../experimental_subjects"
argo_dir = data_directory + "/argouml"
save_dir = "./../results/eval-results/tables/"
print(os.listdir("eval"))


def main():
    all_methods = os.listdir(data_directory)
    results_per_method = load_results(all_methods, data_directory)

    datasets_part_1 = [
        "hospitals"
        , "warehouses"
        , "random"
        , "randomLoose"
        , "randomTight"
        , "Apogames"
    ]
    datasets_part_2 = [
        "ppu"
        , "ppu_statem"
        , "bcms"
        , "bcs"
        , "argouml"
    ]

    datasets_part_3 = [
        "DEFLT.slx"
        , "Driving_ACC_CACC.slx"
        , "Driving_ACC_CACC_TL.slx"
        , "simulink_family_1"
        , "simulink_family_2"
    ]

    all_datasets = []
    all_datasets.extend(datasets_part_1)
    all_datasets.extend(datasets_part_2)
    all_datasets.extend(datasets_part_3)

    rq1_methods = ["RaQuN-Property-Vec",
                   "RaQuN-Character-Vec",
                   ]
    rq3_methods = ["RaQuN-Character-Vec",
                   "RaQuN-Jaccard-25",
                   "RaQuN-Jaccard-50",
                   "RaQuN-Jaccard-75",
                   "RaQuN-Jaccard-100"
                   ]
    rq4_methods = ["RaQuN-Property-Vec",
                   "NwM",
                   "PairwiseAsc",
                   "PairwiseDesc"
                   ]
    rq5_methods = ["RaQuN-Property-Vec",
                   "NwM",
                   "PairwiseAsc",
                   "PairwiseDesc",
                   "RaQuN-Character-Vec"
                   ]
    incremental_k_methods = ["RaQuN_k"]

    argo_datasets = ["argouml_p001", "argouml_p005", "argouml_p010", "argouml_p015", "argouml_p020", "argouml_p025",
                     "argouml_p030", "argouml_p035", "argouml_p040", "argouml_p045", "argouml_p050", "argouml_p055",
                     "argouml_p060", "argouml_p065", "argouml_p070", "argouml_p075", "argouml_p080", "argouml_p085",
                     "argouml_p090", "argouml_p095", "argouml"]

    from pathlib import Path
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    # RQ1 Tables
    create_comparison_table(datasets_part_1, rq1_methods, results_per_method, "table_rq1_1.tex")
    create_comparison_table(datasets_part_2, rq1_methods, results_per_method, "table_rq1_2.tex")
    create_comparison_table(datasets_part_3, rq1_methods, results_per_method, "table_rq1_3.tex")

    # Plotting number of required comparisons table
    if "RaQuN-Character-Vec" in results_per_method:
        tabular = create_num_of_comp_overview("RaQuN-Character-Vec", all_datasets, results_per_method)
        save_table(save_dir + "table_comp.tex", tabular)
        print(tabular)
        print()
        print()
    else:
        print("No data for RaQuN, skipping creation of TABLE III")

    # RQ2 Figures
    bar_plots.create_runtime_plots(incremental_k_methods,
                                   list({"ppu", "bcms"} & set(datasets_part_2)),
                                   results_per_method, "Weight")

    # RQ4 Tables
    create_comparison_table(datasets_part_1, rq4_methods, results_per_method, "table_rq4_1.tex")
    create_comparison_table(datasets_part_2, rq4_methods, results_per_method, "table_rq4_2.tex")
    create_comparison_table(datasets_part_3, rq4_methods, results_per_method, "table_rq4_3.tex")
    if "argouml" in datasets_part_2:
        try:
            all_methods_argo = os.listdir(argo_dir)
            results_per_method_argo = load_results(all_methods_argo, argo_dir)

            # RQ2 ArgoUML Figure
            bar_plots.create_runtime_plots(incremental_k_methods,
                                           ["argouml"],
                                           results_per_method_argo, "Weight")

            # RQ3 Figures
            bar_plots.create_generic_plot_argouml("fig_rq3_precision", rq3_methods,
                                                  argo_datasets, results_per_method_argo, "Precision", use_legend=True)

            bar_plots.create_generic_plot_argouml("fig_rq3_recall", rq3_methods,
                                                  argo_datasets, results_per_method_argo, "Recall", use_legend=True)

            bar_plots.create_generic_plot_argouml("fig_rq3_f1", rq3_methods,
                                                  argo_datasets, results_per_method_argo, "F-Measure", use_legend=True)

            # RQ4 & 5 argouml figures
            bar_plots.create_generic_plot_argouml("fig_rq4_precision", rq4_methods,
                                                  argo_datasets, results_per_method_argo, "Precision", use_legend=True)

            bar_plots.create_generic_plot_argouml("fig_rq4_recall", rq4_methods,
                                                  argo_datasets, results_per_method_argo, "Recall", use_legend=True)

            bar_plots.create_generic_plot_argouml("fig_rq4_f1", rq4_methods,
                                                  argo_datasets, results_per_method_argo, "F-Measure", use_legend=True)

            bar_plots.create_runtime_plot_argouml("fig_rq5_runtime", rq5_methods,
                                                  argo_datasets, results_per_method_argo, use_legend=True)

            bar_plots.create_runtime_plot_argouml("fig_rq5_runtime2", rq5_methods,
                                                              argo_datasets, results_per_method_argo, use_legend=True, use_log=False)
        except FileNotFoundError:
            "No ArgoUML results found"

    # Experimental Subject Overview
    tabular = create_model_stats_overview(experiment_subject_dir, all_datasets)
    save_table(save_dir + "table_datasets.tex", tabular)
    print(tabular)
    tabular = create_argo_subset_stats_overview(experiment_subject_dir + "/argouml", argo_datasets)
    save_table(save_dir + "table_argo_sets.tex", tabular)
    print(tabular)
    print()
    print()
    print("Result evaluation done. Saved all plots and tables under ./results/eval-results")


def create_comparison_table(datasets, methods, results_per_method, file_name):
    tabular = create_tabular_overview(methods, datasets, results_per_method)
    save_table(save_dir + file_name, tabular)
    print(tabular)
    print()
    print()


def save_table(path, table):
    with open(path, 'w') as file:
        file.writelines(table)


if __name__ == "__main__":
    main()
