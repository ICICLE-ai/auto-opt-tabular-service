# Auto Opt Tabular Service

This is an entry point for AutoDL. This service automates the development of deep learning pipelines through optimization proceses for tabular datasets. The input is a raw dataset and the output is the parameters associated with preprocessing of the data and the network, as well as, a dictionary representing the error produced by the network.

**Tags:** Foundation-AI

### License

[![License](https://img.shields.io/badge/License-{{LICENSE_NAME}}-yellow.svg)]({{LICENSE_URL}})

<!-- Add any other licenses you want to include. -->

## References

AutoOpt package (AutoDL framework used by the service): https://pypi.org/project/auto-opt/

## Acknowledgements

_National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)_

## Issue reporting

To report issues please use this link: https://github.com/ICICLE-ai/auto-opt-tabular-service/issues.

---

# Tutorials

<!--
Learning-oriented walkthroughs. (Diátaxis: tutorials)

What can be included:
- A high-level introduction to the task or workflow.
- A list of prerequisites (software requirements, configurations).
- A sequence of steps that guide users through accomplishing a goal.
- Visual aids such as screenshots or GIFs, if necessary.
- End results, showcasing the outcome of following the tutorial.
-->

The AutoOpt framework this serivce is built on top of requires data to be stored as a dictionary of pytorch tensors. The dictionary must have at least 2 key value pairs with one of the key value pairs must have the "labels" key. Examples of valid data dictionaries:
{
"labels":pytorch.Tensor,
"x":pytorch.Tensor
}

    {
    	"labels":pytorch.Tensor,
    	"x1":pytorch.Tensor,
    	"x2":pytorch.Tensor
    }

Use the /run_job endpoint to run this workflow.
The run_job endpoint requires the following inputs:

1. name: how to name the job ran on HPC hardware

2. exec-system-id: The tapis system to execute the job on.

3. cores_per_node: The number of cores to parallelize the training and evaluating of networks across (this number can not exceed the maximum number of cores set on the execution system).

4. memory_mb: Amount of memory to allocate to the job (this number can not exceed the maximum amount of memory available based on the execution system). The more memory provided the more networks that can be simultaneously trained and evaluated.

5. max_minutes: How long the job has to run.

6. billing_account: Account identifier used to bill the run to.

7. ds_path_name: The name of the dataset where it is currently located.

8. ds_path_source_url: The url for where the dataset is curretly located. Used to move the dataset to where the computational resources are. This pathway must be reachable by tapis.

9. ds_path: The name of the dataset once it is transferred to where the run will occur.

10. task_type: The type of prediction being made. The acceptable values are "reg" and "class". "reg" is used for regression based tasks and "class" is used for classification based tasks. When "class" is passed as the task_type the number of classes will automatically be detected based on the dataset labels.

11. split_func: This is the function used to split the dataset into train, evaluation, and test datasets. The possible values are "split_15", "split_20", "split_30", "split_index_15", "split_index_20", "split_index_30".
    split_15: split function produces a random 70, 15, 15 train, eval, test split.
    split_20: split function produces a random 60, 20, 20 train, eval, test split.
    split_30: split function produces a random 40, 30, 30 train, eval, test split.
    split_index_15: split function produces a 70, 15, 15 train, eval, test split with the lower index rows of data being in the train dataset and the higher index rows of data being in the test dataset.
    split_index_20: split function produces a 60, 20, 20 train, eval, test split with the lower index rows of data being in the train dataset and the higher index rows of data being in the test dataset.
    split_index_30: split function produces a 40, 30, 30 train, eval, test split with the lower index rows of data being in the train dataset and the higher index rows of data being in the test dataset.

12. eval_type: The strategy used for evaluating a given network. The available evaluation strategies are "avg", "bag", and "avg_bag".
    avg: evaluation strategy runs the evaluation n times and averages the error metrics produced. The n value is controlled through the "eval_iterations" parameter.
    bag: evaluation strategy averages the predictions made by n seperately trained identical models and calculates error metrics based on those n predictions. THe bagging factor can be controlled by the "bags" parameter.
    avg_bag: evaluation strategy combines both the "avg" and "bag" evaluation strategy. Meaning that the error dictionaries generated using n bags (set by the bags parameter) are averaged over e evaluation itertaions (set by the eval_iterations parameter).

13. gen_strat: The strategy used for sampeling the next parameter set to futher optimize. The two available generation strategies are "best" and "mean".
    best: selects the parameter set that performs the best of all parameter sets
    mean: selects the parameter set that produces the best mean performance

14. metric: The metric to optimize for. !!All optimization process minimize the metric!! The available metrics to choose from are based on the given task type.
    binary classification: acc, roc_auc, precision, recall, f1
    multiclass classification: acc, ebr, roc_auc, precision, recall, f1
    regression: mse, mae, rmse, mape, r2

15. err_path: The path to write the produce dictionary of errs to

16. params_path: The path to write the parameters representing the generated model to.

17. bags: The number of bags used when evaluating networks.

18. eval_iterations: The number of splits to evaluate against when evaluating networks.

---

# How-To Guides

<!--
Task-oriented recipes. (Diátaxis: how-to)

What can be included:
- Problem description: a brief overview of the task or issue.
- Step-by-step instructions on how to complete the task.
- Variations or advanced tips.
- Troubleshooting advice for common pitfalls.
- Relevant code snippets, commands, or configuration examples.
-->

NA

---

# Explanation

<!--
Conceptual / "why and how it works". (Diátaxis: explanation)

What can be included:
- High-level overview of core concepts and principles.
- How the system works and why specific design choices were made.
- Diagrams, flowcharts, or illustrations.
- Background to help users grasp the project's design and architecture.
- Suggested readings or further resources.
-->

The AutoOpt framework generates deep learning pipelines through optimizaiton processes. The optimization process is used to update the parameters that define the data preprocessing, aritifical neural network structure, and artirifical neural network training. This is accomplished by initializing a randomly selected starting point evaluating the performance of that starting point and moving in the direction/directions that improve the performance of the initial starting point. To accelerate this process high performance computing systems are utilized to reduce the wait time for evaluating network parameters.
