from recman.examples.datasets.movie_lens_100k import get_data
from recman.xDeepFM import xDeepFM
from workspace.evaluations.v3.FM import FM
from workspace.evaluations.v3.DeepFM import DeepFM
from workspace.evaluations.v3.input import (
    FeatureDictionary,
    SparseFeat,
    DenseFeat,
    MultiValCsvFeat,
)
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

tf.compat.v1.logging.set_verbosity(20)

#%%
df_train, df_test, domains = get_data()

# samples_cnt = 5 * 1000
# df_train, df_test = df_train.sample(samples_cnt), df_test.sample(samples_cnt)

df_train.loc[df_train.rating < 4, "label"] = 0
df_train.loc[df_train.rating >= 4, "label"] = 1
df_test.loc[df_test.rating < 4, "label"] = 0
df_test.loc[df_test.rating >= 4, "label"] = 1

print(df_train[df_train.rating < 4].shape)
print(df_train[df_train.rating >= 4].shape)

#%%
feat_dict = FeatureDictionary()
feat_dict["user_id"] = SparseFeat(
    name="user_id", feat_size=len(np.unique(df_train.user_id.values)), dtype=tf.int64
)
feat_dict["item_id"] = SparseFeat(
    name="item_id", feat_size=len(np.unique(df_train.item_id.values)), dtype=tf.int64
)
feat_dict["gender"] = SparseFeat(
    name="gender", feat_size=len(np.unique(df_train.gender.values)), dtype=tf.int64
)
feat_dict["occupation"] = SparseFeat(
    name="occupation",
    feat_size=len(np.unique(df_train.occupation.values)),
    dtype=tf.int64,
)
feat_dict["zip"] = SparseFeat(
    name="zip", feat_size=len(np.unique(df_train.zip.values)), dtype=tf.int64
)
feat_dict["timestamp"] = DenseFeat(
    name="timestamp", dtype=tf.float32, scaler=MinMaxScaler()
)
feat_dict["age"] = DenseFeat(name="age", dtype=tf.float32, scaler=MinMaxScaler())
feat_dict["genres"] = MultiValCsvFeat(
    name="genres", tags=domains["genres"], dtype=tf.string
)

feat_dict.initialize(df_train)

#%%
model = xDeepFM(
    feat_dict,
    learning_rate=0.001,
    epoch=5,
    use_interactive_session=False,
    log_dir="../logs",
)
model.fit(df_train, df_train["label"].values.reshape((-1, 1)))

#%%
print(model.predict(df_train))
