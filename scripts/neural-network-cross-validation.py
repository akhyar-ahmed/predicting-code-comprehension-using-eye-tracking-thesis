from sklearn.model_selection import KFold, StratifiedKFold, LeaveOneOut
import wandb
import numpy as np
import pandas as pd
from tensorflow import keras, metrics
from keras import layers
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow
import random
import os

# split into input variables X, output variables y
X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_all_features.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_all_features_participant_segmented.csv")

#CurFix+NxtDis
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pos_nxt_dis.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pos_nxt_dis_participant_segmented.csv")

#CurFix w/ pupil size
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pup.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pup_participant_segmented.csv")

#CurFix w/o duration
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pos.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_pos_participant_segmented.csv")

#CurFix
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_participant_segmented.csv")

#add
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_nxt_dis.csv")
#X = pd.read_csv("./data_public/final_preprocessing/preprocessed_9_cs_25_participants_current_fix_nxt_dis_participant_segmented.csv")


participant_amount = len(X["RECORDING_SESSION_LABEL"].unique())
codesnippet_amount = 9

X.pop("RECORDING_SESSION_LABEL") # remove identifiers
X.pop('precision')
X.pop('code_snippet_id')

# select what to predict (i.e. task outcome => precision, or subj_difficulty)
# y = X.pop('precision')
y = X.pop('subj_difficulty')

input_shape = [X.shape[1]]

# reproducibility
seed = 42 # fix random seed for reproducibility
os.environ['PYTHONHASHSEED']=str(seed)
random.seed(seed)
np.random.seed(seed)
tensorflow.random.set_seed(seed)

# define k-fold cross validation
n = participant_amount
#n = codesnippet_amount

kfold = KFold(n_splits=n) # StratifiedKFold(n_splits=n, shuffle=True, random_state=seed)

# local score computations array initialization
cvscores = []
aucscores = []
y_prediction = []
y_true = []
group_id = wandb.util.generate_id() #"first-run"

# train and evaluate neural network
i = 0
for train, test in kfold.split(X,y):
    # clear tensorflow keras global state memory to start with blank state at each iteration
    keras.backend.clear_session()

    # weights & biases initialization
    #wandb.init(project="cc_fixation_models", group=group_id, tags=["public", "cs_fix", "participant-fold", "26_participants"],
    config = {
        "k_fold_cross_validation": n,
        "random_seed": seed,
        "loss": "mae",
        "optimizer": "adam",
        "epochs": 56,
        "batch_size": 32,
        "early_stopping_min_delta": 0.001,
        "early_stopping_patience": 10,
        "early_stopping_restore_best": True,
        "layers": 4,
        "hidden_layer_1_size": 56,
        "hidden_layer_2_size": 32,
        "hidden_layer_3_size": 16,
        "hidden_layer_4_size": 8,
        "dropout_rate": 0.5,
        "notes": "using unshuffled kFold Cross Validation, testing on new participant, using all 26 participants"
    }#)

    #config = wandb.config

    # define early stopping call back
    early_stopping = EarlyStopping(
        min_delta=config["early_stopping_min_delta"], # minimium amount of change to count as an improvement
        patience=config["early_stopping_patience"], # how many epochs to wait before stopping
        restore_best_weights=config["early_stopping_restore_best"],
    )

    # define model
    model = keras.Sequential([
        layers.Dropout(config["dropout_rate"], input_dim=input_shape[0]),
        layers.BatchNormalization(),
        layers.Dense(config["hidden_layer_1_size"], activation="relu"),

        layers.Dropout(config["dropout_rate"]),
        layers.BatchNormalization(),
        layers.Dense(config["hidden_layer_2_size"], activation="relu"),

        layers.Dropout(config["dropout_rate"]),
        layers.BatchNormalization(),
        layers.Dense(config["hidden_layer_3_size"], activation="relu"),

        layers.Dropout(config["dropout_rate"]),
        layers.BatchNormalization(),
        layers.Dense(config["hidden_layer_4_size"], activation="relu"),

        #layers.Dropout(config["dropout_rate"]),
        #layers.BatchNormalization(),
        #layers.Dense(config["hidden_layer_5_size"], activation="relu"),

        layers.Dropout(config["dropout_rate"]),
        layers.BatchNormalization(),
        layers.Dense(1) # activation="sigmoid")
    ])

    # compile model
    model.compile(
        loss=config["loss"],
        optimizer=config["optimizer"],
        metrics=['mae', tensorflow.keras.metrics.MeanAbsolutePercentageError()]
    )

    # fit the model
    history = model.fit(
        X.values[train], y.values[train],
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        verbose=0,
        validation_data=(X.values[test], y.values[test]),
        callbacks=[
            early_stopping,
            #WandbCallback(
            #    training_data=(X.values[train], y.values[train]),
            #    validation_data=(X.values[test], y.values[test])
            #)
        ]
    )

    # evaluate the model
    # log loss function graph to compare loss and value loss over epochs to visualize under/over-fitting of model
    history_df = pd.DataFrame(history.history)
    #wandb.log({
    #    "loss_val_loss_history": wandb.Image(history_df.loc[:, ['loss', 'val_loss']].plot())
    #})

    scores = model.evaluate(X.values[test], y.values[test], verbose=0)
    print(f"{model.metrics_names[1]} {scores[1]*100:.2f}    {model.metrics_names[2]} {scores[2]*100}")
    cvscores.append(scores[1] * 100)
    aucscores.append(scores[2] * 100)

    #wandb.log({"best_epoch_accuracy_c": scores[1]})
    #wandb.log({"best_epoch_AUC_c": scores[2]})

    # get predictions and log them (y_p => predictions, y_t => truth)
    predictions = model.predict(X.values[test])
    predictions = predictions.round().astype(int).tolist()
    y_p = [item for sublist in predictions for item in sublist]
    y_prediction += y_p
    y_t =  y.values[test].round().astype(int).tolist()
    y_true += y_t

    #wandb.log({"predictions": y_p})
    #wandb.log({"truth": y_t})

    # last run
    #if i == n-1:
        #result = confusion_matrix(y_true, y_prediction) # , normalize='pred')
        #font = {'weight': 'normal', 'size': 15}
        #plt.rc('font', **font)
        #cm_display = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix = result, display_labels = [0, 1])
        #cm_display.plot(cmap=plt.cm.Blues)
        #plt.savefig('foo.png')
        #wandb.log({"confusion_matrix": result})
        #wandb.log({"confusion_matrix_plot": plt})

    #wandb.finish()
    i += 1

print("accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores) / np.sqrt(np.size(cvscores))))
print("AUC: %.2f%% (+/- %.2f%%)" % (np.mean(aucscores), np.std(aucscores) / np.sqrt(np.size(aucscores))))