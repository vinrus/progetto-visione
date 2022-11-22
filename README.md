# Progetto per l'esame di Visione e Percezione
- Linguaggio di programmazione: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

- Librerie: ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)   ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

- Hardware: ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)

- Strumenti di sviluppo: ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

- Installare le dipendenze necessarie tramite il file requirements.txt con il comando : <br><br>
        <code>
             pip3 install -r requirements.txt
        </code>

- **Creazione del dataset**:

  1.  Creazione dei file di label <strong>assets/dataset/keypoint_label.csv</strong> per indicare le label per la classificazione degli hand sign e <strong>assets/dataset/keypoint_history_label.csv</strong> per la classificazione delle hand gestures

  2.  Run del file per la crezione dei dataset <strong>assets/dataset/keypoint.csv</strong>, <strong>assets/dataset/keypoint_history.csv</strong>  :

       <code>
            python3 neuralnetwork/classification_gestures.py --mode "X"
       </code>
        
        dove "X" è uguale a 1 per registrare gli hand sign 2 per i punti delle hand gestures.

- **Train dei Modelli**:

     l'addestramento dei modelli viene effettuato eseguendo le celle dei due notebook:<br><br>
              <code>
                     neuralnetwork/hand_classificator.ipynb
              </code>
              <br>
              <code>
                     neuralnetwork/hand_history_classificator.ipynb
              </code>

- **Run Applicativo**:<br><br>
  <code>python3 src/main.py</code>

<br>

 

