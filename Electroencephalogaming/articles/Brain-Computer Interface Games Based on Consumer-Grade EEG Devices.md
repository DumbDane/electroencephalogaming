---
Title: Brain-Computer Interface Games Based on Consumer-Grade EEG Devices
Authors:
  - Gabriel Alves Mendes Vasiljevic
  - Leonardo Cunha de Miranda
DOI: https://doi.org/10.1080/10447318.2019.1612213
link: https://tandfonline.com/doi/full/10.1080/10447318.2019.1612213
tags:
  - literature-review
Read: true
---
# Brain-Computer Interface Games Based on Consumer-Grade EEG Devices: A Systematic Literature Review

### Abstract
>[!quote] Brain–Computer Interfaces (BCIs) are specialized systems that allow users to control computer applications using their brain waves. With the advent of consumer-grade electroencephalography (EEG) devices, brain-controlled systems started to find applications outside of the medical field, opening many research opportunities in the area of Human-Computer Interaction (HCI). One particular area that is gaining more evidence due to the arrival of consumer-grade devices is that of computer games, as it allows more user-friendly applications of BCI technology for the general public. In this paper, the results of a Systematic Literature Review (SLR) of BCI games using consumer-grade devices are presented. Papers published in a time span of 12 years were reviewed and their data collected using a rigid systematic process. Several analyses were made based on the gathered data, and a clear view of the current scenario and challenges for HCI of BCI-based games using consumer-grade devices is provided. The search shows that although many games were created with simplified controls for research purposes, there was an increasing number of more user-friendly BCI games, especially for entertainment. The most predominant control signals were the attention and meditation, followed by motor imagery and emotion recognition, being mainly captured by NeuroSky and Emotiv EEG devices. The results also show that there are still many open issues and research opportunities in the field of HCI for BCI-based games, as most evaluations investigated only quantitative aspects of the BCI systems, while very few studies analyzed usability and qualitative aspects of the users’ interaction with the games.



# 1 Introduction

This work focuses on the following researching questions:

- RQ1: What kinds of games are created using consumer-grade EEG technology? What are the characteristics of such games?
- RQ2: Which BCI control signals those consumer-grade EEG mind-controller games are based upon? Which are used more and why?
- RQ3: How are those games evaluated? Is there any effort to make those games more user-friendly and accessible for the players? And how difficult it is to play them?
- RQ4: What are the gaps and open topics in the field?

# 2 Background

The traditional applications for BCI systems mainly focus on improving interaction experience for disabled people, however, people without any disability are also potential users of solutions which promote interaction between humans and computer through cerebral signals.

## 2.1 Brain waves

The brain is composed of two types of specialised cells, i.e., neurons and neuroglia. The neuroglia’s function is to support the neurons, keeping them in place and providing them with nutrients and oxygen. The neurons are responsible for the transmission of information through chemical and electrical impulses, called nerve impulses.

This constant flow of electrical current in the brain, caused by the synaptic excitation of the dendrites in the neurons, generates electrical signals that propagate from the encephalic mass to the scalp, which are called brain waves.

EEG signals are weak since the they need to cross several layers of tissues.

Delta waves (below 4 Hz) are associated with deep, dreamless sleep. 

The theta waves (from 4 to 7 Hz) are generated during sleep and states of deep meditation. 

Alpha waves (from 8 to 12 Hz) are generated while the brain is in a resting state. They increase while the eyes are closed and the person is relaxed, and are found in the occipital and frontal areas, related to visual processing and mental activity. Alpha waves are suppressed when mental effort is done, allowing this signal to be used to measure the focused mental activity.

Beta waves (from 12 to 30 Hz) are related to motor activities . They are predominantly found in the frontal and parietal lobes, primarily in the pre-frontal cortex, and can be further subdivided into low-beta or beta-1 (12 to 16 Hz), (mid-)beta or beta-2 (16 to 20 Hz) and high-beta or beta-3 (20 to 30 Hz), with range definitions varying among studies. Beta waves are known to be synchronized and have a symmetrical distribution when there are no motor activities in progress, and become desynchronized and change its symmetry when the sight, the imagination or the performance of a motor activity occur. They are also related to intense cognitive activity. 

The gamma waves (over 30 Hz) are related to the simultaneous processing of information from various regions of the brain, such as the perception of auditory and visual stimuli, and motor functions.

## 2.2 BCI control signals

Some physiological phenomena related to specific brain signals have been decoded and can be used as control signals, as users can learn how to modulate them at will.

The theta, alpha and beta waves, for example, are related to certain brain states. Theta and alpha rhythms are stronger and beta waves are weaker when the user is in a relaxation or meditation state, while beta rhythms are stronger and alpha and theta rhythms are weaker when the user is in a state of concentration or attention. These changes in the brain waves can be used to measure the user’s brain state and are frequently employed as a control signal to BCI systems, as the user can learn to self-regulate their brain state through a process known as neurofeedback. Metrics that could be used for such measure are beta/alpha and theta/beta ratios, the wave’s entropy, or the wave’s raw power spectrum. 

The Sensorimotor Rhythms (SMR) are related to the motor imagery, and comprise the beta and the mu rhythms (i.e., oscillations in the brain activity in the respective bands). The mu band has the same frequency as the alpha band, but is related to different physiological phenomena, as the amplitude of such rhythms is modulated according to mental tasks related to motor activities without necessarily needing an actual physical movement. This amplitude modulation can either be an Event-Related Desynchronisation (ERD) or an Event-Related Synchronisation (ERS).

Visual stimulations are processed in the visual cortex, located at the occipital lobe. There are specific signal modulations that occur in the visual cortex when certain visual stimuli are perceived, and these modulations, known as VEP (Visually Evoked Potentials), are easily detected, especially as
the stimuli moves closer to the visual field, as the VEP amplitude increases. SSVEP (Steady-State VEP) is a particular type of VEP that is elicited when the visual stimulus changes at a frequency higher than 6 Hz. This stimulus can be either a pattern or a flashing light or image. SSVEP can be used as a control signal for BCI, for example by means of eye-gaze where the user focuses their gaze onto one visual stimulus.

Other forms of evoked potentials are possible, such as AEP (Auditory-Evoked Potentials) and SEP (Somatosensory-Evoked Potentials), with their corresponding SSAEP (Steady-State AEP) and SSSEP (Steady-State SEP). 

Emotion can be recognised by a BCI system through an EEG. 

When attending to an infrequent stimulus among several frequent stimuli, a positive peak in the EEG is elicited. This positive evoked potential occurs approximately 300 ms after the oddball stimulus, and is called P300 (‘P’ for “Positive”, 300 for 300 ms).

### 2.2.1 Notes on eye tracking and blink detection

The movement of the eyes and eyelids can be employed as control signals, as they generate voltage peaks and fluctuations in the captured brain waves. 

Eye tracking generates specific voltage peaks that can be captured by electrodes. Being able to
distinguish the top/down, left/right and center gazes of the user allows using the same controls as a motor imagery or SSVEP system would, for example. Eye tracking and blink detection can also be done using computational vision algorithm and technologies, or by directly reading the cornea-retinal potential in the human eye, which is known as Electrooculogram (EOG).

However, although these signals can be acquired using EEG, they are not generated in the brain itself, but rather by the eye and face muscles (the latter known as Electromyogram or EMG). Therefore, both techniques are generally not considered as being BCI; in fact, EOG and
EMG artefacts in EEG signals are a known issue in EEG-based applications, especially in those with sensors placed near the face or eye muscles, and are often filtered in the processing of brain waves in BCI applications.

## 2.3 BCI paradigms

A BCI system can be classified according to the application of the employed control signal. The classifications are “active”, “passive” and “reactive”. An active BCI uses an active control mode, i.e., an action is required from the user to activate or modulate the signal. An example of this type of control is the motor imagery, which requires the user to actively imagine an action or movement
to perform an action in the system. The passive BCI, on the other hand, does not require a specific action from the user, as the signals are modulated in a passive manner.

Examples of this type of BCI are the concentration and meditation levels of the user and their emotional state. Those specific signals may also be used in an active manner according to the application, if the user is required to achieve a certain meditation level or a specific emotion, for example, especially through neurofeedback.

The third type, reactive BCI, requires a reaction from the user, i.e., a stimulus is provided and the reaction from the user to that stimulus is captured. Examples of this type are the SSVEP, in which the user must focus his/her gaze in a specific stimulus, and the P300, in which the user passively generates a positive voltage peak approximately 300 ms after an oddball stimulus. The reactive classification can also be seen as a subgroup of the other two types, as in some cases the user must “actively” (e.g., in the SSVEP control signal) or “passively” (e.g., in the P300 control signal) produce the modulation.

## 2.4 BCI consumer-grade EEG devices

### 2.4.1 The 10-20 and 10-10 international systems

The positions of the devices’ sensors follow the international 10-20 system, which defines standard electrode placement positions based on two reference points, i.e., the nasion, located at the top of the nose, and the inion, located at the back of the skull.

![[BCI Games 1.png]]

## 2.5 Game platform, purpose, and genre

Similar to BCI systems, a computer game can be classified according to many of its characteristics:

- Platform it is played on (PC, console, mobile)
    - PC could have the subcategory of web games
- Purpose (entertainment, serious)
- Game genre (common challenges and gameplay characteristics)
    - action (fast-paced with time-critical challenges, tests hand-eye coordination and reaction time of the player)
    - adventure (central story that develops, elements of exploration)
    - RPG (central story but the player takes the role of a specialised character)
    - strategy (planning a series of actions to win the game)
    - puzzle (problem-solving)
    - simulation (simulate aspects of a real or imaginary activity or situation)
    - sports (simulate real or imaginary sport)

# 4 Method

This paper reviewed the other papers based on the Preferred Reporting Items for Systematic Reviews and Meta-Analyses methodology.

## 4.2 Eligibility criteria

BCI games that use consumer-grade EEG devices as a control channel is the criteria. It does not exclude works that used BCI as a complementary or secondary control. 

## 4.5 Study selection

Selection criteria: 

- articles in English
- articles published in peer-reviewed scientific journals or peer-reviewed scientific conferences
- articles published during the period of 2007 to 2018
- the title or the abstract explicitly states that the main focus of the research is BCI-based games

Quality criteria:

- are the goals of the research clearly stated? Are they related to the development, use, evaluation or applications of the game or the BCI?
- Is the developed or presented BCI-based game the primary focus of the research?
- The interaction, methods, paradigms, tools, and technologies are clearly described?
- An experiment or case study was conducted to evaluate the game or validate the adopted methods? Is this evaluation well described?
- Are there any conclusive results regarding the use of the adopted technologies/methods? Are the main findings clearly described?

![[BCI Games 2.png]]

## 4.7 Data classification

The classification of the BCI paradigm was performed according to how the BCI control was employed in the game. The game was classified as being a passive BCI when the player does not need to actively focus on (or even be aware of) their mental state while playing the game, e.g., when a game employed a mental state of the player to alter the game’s background music or adjust its difficulty. Alternatively, if the game requires the player to modulate their cognitive state or to generate a specific mental command to progress, the game was classified as an active BCI instead, since the player must actively generate the required control signal. In addition, if the player can choose to play actively or passively, then the game was classified as “Both”.

# 5 Results

## 5.1 Study selection

![[BCI Games 3.png]]

## 5.2 Study characteristics

The selected studies and their respective games were classified according to the data collection process specifically to the technical aspects of the game(s), such as which headset was used, the control signal(s) employed, how the brain signals were used as a controller and the game(s) genre.

## 5.3 Individual studies

### 5.3.1 Attention

Together with the games using the meditation control signal, the games using attention, i.e., in which the player’s mental level of attention/concentration is used as input control to the game, compose almost three-quarters of the reviewed games.