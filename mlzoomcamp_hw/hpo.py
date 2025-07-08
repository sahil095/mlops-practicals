import os
import math
import pickle
import click
import mlflow
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Connect to local MLflow tracking server
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("random-forest-hyperopt")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="../output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--num_trials",
    default=15,
    help="The number of parameter evaluations for the optimizer to explore"
)
def run_optimization(data_path: str, num_trials: int):

    # Load training and validation data
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    # Define the objective function
    def objective(params):
        with mlflow.start_run():
            # Convert hyperopt float values to int where needed
            rf = RandomForestRegressor(
                max_depth=int(params['max_depth']),
                n_estimators=int(params['n_estimators']),
                min_samples_split=int(params['min_samples_split']),
                min_samples_leaf=int(params['min_samples_leaf']),
                random_state=params['random_state'],
                n_jobs=-1
            )

            # Fit and predict
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)
            rmse = math.sqrt(mean_squared_error(y_val, y_pred))

            # Log parameters and RMSE to MLflow manually
            mlflow.log_params({
                "max_depth": int(params['max_depth']),
                "n_estimators": int(params['n_estimators']),
                "min_samples_split": int(params['min_samples_split']),
                "min_samples_leaf": int(params['min_samples_leaf']),
                "random_state": params['random_state']
            })
            mlflow.log_metric("rmse", rmse)

            return {"loss": rmse, "status": STATUS_OK}

    # Define hyperparameter search space
    search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 50, 1)),
        'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 10, 1)),
        'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 4, 1)),
        'random_state': 42
    }

    # Run hyperparameter optimization
    rstate = np.random.default_rng(42)  # for reproducibility
    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=Trials(),
        rstate=rstate
    )


if __name__ == '__main__':
    run_optimization()
