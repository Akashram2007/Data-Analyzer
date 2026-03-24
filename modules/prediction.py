import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from sklearn.metrics import r2_score, accuracy_score


def prediction(data):

    data = data.dropna()

    target = st.selectbox("Select Target Column", data.columns, width=300)

    features = st.multiselect(
        "Select Feature Columns",
        [col for col in data.columns if col != target],
        width=300,
    )

    if target and features:

        X = data[features].copy()
        y = data[target]

        num_cols = X.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = X.select_dtypes(include=["object"]).columns

        encoders = {}

        for col in cat_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le

        st.session_state["encoders"] = encoders

        if y.dtype == "object" or y.nunique() < 10:
            problem_type = "Classification"
        else:
            problem_type = "Regression"

        st.info(f"Detected Problem Type: {problem_type}")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        if problem_type == "Regression":

            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
            }

        else:

            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
            }

        st.divider()

        if st.button("🚀 Train Models"):

            scores = {}

            for name, model in models.items():

                model.fit(X_train, y_train)

                predictions = model.predict(X_test)

                if problem_type == "Regression":
                    score = r2_score(y_test, predictions)
                else:
                    score = accuracy_score(y_test, predictions)

                scores[name] = score

            st.session_state["scores"] = scores

            best_model_name = max(scores, key=scores.get)
            best_model = models[best_model_name]
            best_score = scores[best_model_name]

            st.session_state["model"] = best_model
            st.session_state["features"] = features
            st.session_state["trained"] = True
            st.session_state["best_model_name"] = best_model_name
            st.session_state["best_score"] = best_score
            st.session_state["problem_type"] = problem_type
            st.session_state["cat_cols"] = cat_cols

        if "scores" in st.session_state:

            score_df = pd.DataFrame(
                {
                    "Model": list(st.session_state["scores"].keys()),
                    "Score": [i * 100 for i in st.session_state["scores"].values()],
                }
            )

            st.subheader("📊 Model Performance")
            st.caption("Comparison of ML Models based on Performance")
               
            st.bar_chart(
                score_df.set_index("Model"), horizontal=True, width=300, height=150
            )

        if st.session_state.get("trained", False):

            st.success(
                f"✅ Best Model Selected: "
                f"{st.session_state['best_model_name']} "
                f"with {st.session_state['best_score']*100:.2f}%"
            )

            st.divider()

            model = st.session_state["model"]
            features = st.session_state["features"]
            problem_type = st.session_state["problem_type"]
            cat_cols = st.session_state["cat_cols"]

            st.subheader("🔎 Enter values for prediction")

            inputs = []

            for col in features:

                if col in cat_cols:

                    le = st.session_state["encoders"][col]

                    selected = st.selectbox(
                        f"Enter {col}",
                        list(le.classes_),
                        accept_new_options=True,
                        width=300,
                    )

                    # Handle unseen categories
                    if selected in le.classes_:
                        val = le.transform([selected])[0]
                    else:
                        val = len(le.classes_)

                else:

                    val = st.number_input(f"Enter {col}", width=300)

                inputs.append(val)

            # Predict
            if st.button("🔮 Predict"):

                result = model.predict([inputs])

                if problem_type == "Regression":

                    st.success(f"Predicted {target} → {result[0]:.2f}")

                else:

                    st.success(f"Predicted Result → {result[0]}")

                    if hasattr(model, "predict_proba"):

                        prob = model.predict_proba([inputs])
                        confidence = prob.max() * 100

                        st.info(f"Confidence: {confidence:.2f}%")