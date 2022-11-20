![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)   ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
# Progetto per l'esame di Visione e Percezione

- Installare le dipendenze necessarie tramite il file requirements.txt con il comando :

       <code>
            pip3 install -r requirements.txt
       </code>

  <br>

- **Creazione del dataset**:

  1.  Creazione del file <strong>assets/dataset/keypoint_label.csv</strong> per indicare le label per la classificazione

  2.  Run del file per la crezione del dataset <strong>assets/dataset/keypoint.csv</strong> :

        <code>
             python3 neuralnetwork/classification_gestures.py
             <br>
             python3 neuralnetwork/classification_gestures.py --point "X"
        </code>
        
        dove "X" è la posizione della label presente nel file : assets/dataset/keypoint_label.csv

- **Run Applicativo**:
  <code>python3 src/main.py</code>

<br>

- Classificatore:
[![Open In Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://ml.azure.com/fileexplorerAzNB?wsid=/subscriptions/0a5d55f8-7024-4c0a-b69d-504c05509490/resourcegroups/gruppo1/providers/Microsoft.MachineLearningServices/workspaces/visione&tid=c9881521-f12e-4b19-ad2f-a5d007efaf93)
