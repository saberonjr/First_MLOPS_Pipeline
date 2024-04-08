from clearml.automation import HyperParameterOptimizer, UniformParameterRange
from clearml.automation.optuna import OptimizerOptuna
from clearml import Task
import argparse


def hpo(base_task_id, queue_name):
    # Initialize ClearML Task for HPO
    task = Task.init(
        project_name="CIFAR-10 Project",
        task_name="HPO CIFAR-10 Training",
        task_type=Task.TaskTypes.optimizer,
    )

    # Define Hyperparameter Space
    param_ranges = [
        UniformParameterRange("epochs", min_value=5, max_value=50, step_size=5),
    ]

    # Setup HyperParameter Optimizer
    optimizer = HyperParameterOptimizer(
        base_task_id=base_task_id,
        hyper_parameters=param_ranges,
        objective_metric_title="accuracy",
        objective_metric_series="validation",
        objective_metric_sign="max",  # or 'min' for loss
        optimizer_class=OptimizerOptuna,
        execution_queue=queue_name,
        max_number_of_concurrent_tasks=1,
        optimization_time_limit=60.0,
    )

    # Start the Optimization
    optimizer.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Hyperparameter Optimization for CIFAR-10 Pipeline"
    )
    parser.add_argument(
        "--base_task_id",
        type=str,
        required=True,
        help="Base Task ID for the CIFAR-10 Pipeline",
    )
    parser.add_argument(
        "--queue_name",
        type=str,
        default="default",
        help="Execution queue name in ClearML",
    )

    args = parser.parse_args()
    hpo(args.base_task_id, args.queue_name)