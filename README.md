# Anti-cheat Exam
# Library
Idea: use training algorithms to classification exam cheating behaviors, for example: SVC, RandomForest, RNN, Logic Regression.
Data collection: 5 photos will be taken every second, by default, each data collection is 30s -> 150 images. Since each image will take 4 values (x, y, w, h) -> each sample will have 600 features. Before the data collection test, we have to default to the previous abnormal or non-abnormal action. If label = F, we will perform unusual actions (leave the frame, move the face many times, view documents, ...), otherwise, we will perform the exercise focusing on doing less movement, sitting in the main seat screen surface.

Run getTrainingData.py to collecting data

![image](https://user-images.githubusercontent.com/75513398/183009798-48e40510-4af8-437f-b8b2-2cc12e2e703d.png)

# Train model
See Classifier.py
Run managerExam.py to select model and training
![image](https://user-images.githubusercontent.com/75513398/183010293-faff3c3c-b537-49e6-a723-9bdba277cda6.png)

# User do test
The application sends data to the server once every 30s with information like name, mssv, phone and 150 pictures converted into 600 features. Then the server will predict the results, the exam manager will go to the management application and track the results.

![image](https://user-images.githubusercontent.com/75513398/183010865-2bc66a78-7a2c-4be3-9482-d63307012780.png)

![image](https://user-images.githubusercontent.com/75513398/183011762-775b0fc3-da63-4f97-9ff0-e41e5f1d5f44.png)

