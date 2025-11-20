import pickle
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, confusion_matrix

def train_model(X, y):
    # Detect classification or regression
    is_classification = len(set(y)) < 30 and y.dtype.kind in 'iu'  # int category
    if is_classification:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metrics = {}
    if is_classification:
        metrics['accuracy'] = accuracy_score(y_test, y_pred)
        metrics['confusion_matrix'] = confusion_matrix(y_test, y_pred)
    else:
        metrics['r2'] = r2_score(y_test, y_pred)
    return model, metrics

def predict(model, x):
    return model.predict([x])[0]

def save_model(model, encoders, target_encoder):
    with open('model.pkl', 'wb') as f:
        pickle.dump({'model': model, 'encoders': encoders, 'target_encoder': target_encoder}, f)

def load_model():
    with open('model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['encoders'], data['target_encoder']