from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from config import N_COMPONENTS, COVARIANCE_TYPE, RANDOM_STATE


def train(features_df):
    scaler = StandardScaler()
    # Fit the scaler on the training data
    train_scaler = scaler.fit_transform(features_df)
    
    train_model = GaussianMixture(n_components=N_COMPONENTS, covariance_type=COVARIANCE_TYPE, random_state=RANDOM_STATE, n_init=10)
    train_model.fit(train_scaler)
    
    return train_model, scaler

def predict(model, scaler, features_df):
    # Scale the features using the fitted scaler
    scaled_features = scaler.transform(features_df)
    
    # Predict the regime labels
    regimes = model.predict(scaled_features)
    probabilities = model.predict_proba(scaled_features)
    
    return regimes, probabilities

def interpret(regime_number):
    regime_mapping = {
        0: 'Bull/Trending',
        1: 'Sideways/Neutral',
        2: 'High Volatility',
        3: 'Crisis/Bear'
    }
    return regime_mapping.get(regime_number, 'Unknown Regime')