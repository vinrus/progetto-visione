
# Progetto per l'esame di Visione e Percezione

- Installare le dipendenze necessarie tramite il file requirements.txt con il comando : 

     <code>
          pip3 install -r requirements.txt
     </code>
<br>

- Creazione del dataset: 
     1. Creazione del file <strong>assets/dataset/keypoint_label.csv</strong> per indicare le label per la classificazione

     2. Run del file per la crezione del dataset  <strong>assets/dataset/keypoint.csv</strong> : 

          <code>
               python3 neuralnetwork/classification_gestures.py
               <br>
               python3 neuralnetwork/classification_gestures.py --point "X"
          </code>
          
          dove "X" è la posizione della label presente nel file : assets/dataset/keypoint_label.csv



     
<br>

- Classificatore: 
[![Open In Azure](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Microsoft_Azure_Logo.svg/1024px-Microsoft_Azure_Logo.svg.png)](https://ml.azure.com/fileexplorerAzNB?wsid=/subscriptions/0a5d55f8-7024-4c0a-b69d-504c05509490/resourcegroups/gruppo1/providers/Microsoft.MachineLearningServices/workspaces/visione&tid=c9881521-f12e-4b19-ad2f-a5d007efaf93)
