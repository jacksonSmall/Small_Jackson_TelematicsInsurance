Insurity Driver Risk Scoring Platform

Folder Structure:
-----------------
insurity/
│
├─ bin/
├─ data/
│   ├─ clean_drivers.csv
│   ├─ driver_risk_scores.csv
│   └─ simulated_drivers.csv
├─ docs/
│   ├─ models.md
│   └─ requirements.txt
├─ models/
│   ├─ best_driver_risk_model.pkl
│   ├─ driver_risk_model.pkl
│   ├─ risk_model.pkl
│   └─ scaler.pkl
├─ src/
│   ├─ api.py
│   ├─ dashboard.py
│   ├─ data_processing.py
│   ├─ data_simulation.py
│   ├─ model_train.py
│   └─ pricing_engine.py
└─ venv/ 

Setup Instructions:
1. Activate the virtual environment:
   - macOS/Linux:
       $ source venv/bin/activate
   - Windows:
       > venv\Scripts\activate

2. Install required packages:
       (venv) $ pip install -r docs/requirements.txt

3. Run the following scripts in order:
    - **python src/data_simulation.py**
    - **python src/data_processing.py**
    - **python src/model_train.py**
    - **python src/pricing_engine.py**

4. Make a new terminal and run api using uvicorn:
uvicorn src.api:app --reload

5. In another terminal show the dashboard by:
streamlit run src/dashboard.py

The metrics as of now are printed after the model_train.py execution. Enjoy!

