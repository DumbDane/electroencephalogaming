---
Title: Machine-Learning-Based Co-adaptive Calibration for Brain-Computer Interfaces
Authors:
  - Carmen Vidaurre
  - Claudia Sannelli
  - Klaus-Robert Müller
  - Benjamin Blankertz
DOI: https://doi.org/10.1162/NECO_a_00089
link: https://doc.ml.tu-berlin.de/bbci/publications/VidSanMueBla10.pdf
tags:
  - calibration
  - motor-imagery
Read: false
---

# Machine-Learning-Based Co-adaptive Calibration for Brain-Computer Interfaces

### Abstract
>[!quote] Brain-computer interfaces (BCIs) allow users to control a computer application by brain activity as acquired (e.g., by EEG). In our classic machine learning approach to BCIs, the participants undertake a calibration measurement without feedback to acquire data to train the BCI system. After the training, the user can control a BCI and improve the operation through some type of feedback. However, not all BCI users are able to perform sufficiently well during feedback operation. In fact, a nonnegligible portion of participants (estimated 15%–30%) cannot control the system (a BCI illiteracy problem, generic to all motor-imagery-based BCIs). We hypothesize that one main difficulty for a BCI user is the transition from offline calibration to online feedback. In this work, we investigate adaptive machine learning methods to eliminate offline calibration and analyze the performance of 11 volunteers in a BCI based on the modulation of sensorimotor rhythms. We present an adaptation scheme that individually guides the user. It starts with a subject-independent classifier that evolves to a subject-optimized state-of-the-art classifier within one session while the user interacts continuously. These initial runs use supervised techniques for robust coadaptive learning of user and machine. Subsequent runs use unsupervised adaptation to track the features’ drift during the session and provide an unbiased measure of BCI performance. Using this approach, without any offline calibration, six users, including one novice, obtained good performance after 3 to 6 minutes of adaptation. More important, this novel guided learning also allows participants with BCI illiteracy to gain significant control with the BCI in less than 60 minutes. In addition, one volunteer without sensorimotor idle rhythm peak at the beginning of the BCI experiment developed it during the course of the session and used voluntary modulation of its amplitude to control the feedback application.

