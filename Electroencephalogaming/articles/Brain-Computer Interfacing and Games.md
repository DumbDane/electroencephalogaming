---
Title: Brain-Computer Interfacing and Games
Authors:
  - Danny Plass-Oude Bos
  - Boris Reuderink
  - Bram van de Laar
  - Hayrettin Gürkök
DOI: 10.1007/978-1-84996-272-8_10
link: https://www.researchgate.net/publication/225992971_Brain-Computer_Interfacing_and_Games
tags:
  - games
---
# Brain-Computer Interfacing and Games

### Abstract
> [!quote] Recently research into Brain-Computer Interfacing (BCI) applications for healthy users, such as games, has been initiated. But why would a healthy person use a still-unproven technology such as BCI for game interaction? BCI provides a combination of information and features that no other input modality can offer. But for general acceptance of this technology, usability and user experience will need to be taken into account when designing such systems. Therefore, this chapter gives an overview of the state of the art of BCI in games and discusses the consequences of applying knowledge from Human-Computer Interaction (HCI) to the design of BCI for games. The integration of HCI with BCI is illustrated by research examples and showcases, intended to take this promising technology out of the lab. Future research needs to move beyond feasibility tests, to prove that BCI is also applicable in realistic, real-world settings.

# 1 Introduction

BCI research has been motivated for years by the wish to provide paralysed people with new communication and motor abilities. BCI has recently been moving into applications for healthy people.

Gamers are often among the first to adopt any new technology (Nijholt and Tan).

Current BCI games are often just proofs of concept and a weak replacement for traditional input devices such as the mouse and keyboard; they cannot achieve the same speed and precision. 

If the user’s mental state can be derived from brain activity, it can be manipulated via the game (keep the user in equilibrium by matching skill and challenge). 

BCI should enhance the user experience for healthy users by offering something that current interaction modalities don’t have. The use of specific BCI paradigms “could make you more relaxed and focused”.

# 2 The State of the Art

Neurofeedback games focus on having the user control some aspect of their brain activity in order to play the game (for example relaxation or focus). 

Motor-control based BCIs are often used as input devices. 

# 3 Human-Computer Interaction for BCI

The main concepts of usability (according to Nielsen): learnability, memorability, efficiency and effectiveness, error handling, and satisfaction. 

## 3.1 Learnability and Memorability

How intuitive is the usage? For example, when hearing “imagine hand movement” people might think of different things.

## 3.2 Efficiency and Effectiveness

BCI should have an advantage that is not efficiency since it is not yet comparable to the efficiency of other input sources. 

## 3.3 Error Handling

This consists of two parts: error prevention and error correction. 

BCI can make use of error related negativity (ERN) to undo a previous movement based on the detection that a user is conscious of their error. 

## 3.4 Satisfaction

Satisfaction is often seen in connection to how effective the system is, meaning an effective system leads to higher user satisfaction. 

> In the context of BCI games we can consider satisfaction to be the end result of all of the design choices that were made, the functionality of the game, the ease with which the user could learn and memorize the control of the BCI and with what accuracy they could control the game. In other words, satisfaction can be seen as everything the user experienced during the game.
> 

# 4 BCI for Controlling and Adapting Games

## 4.3 BCI as Game Controller

### 4.3.1 The Time Scale of a BCI

The time scale at which commands are issued needs to make sense in the context of the game. 

### 4.3.2 Influence of Mental State on BCI

BCI can be influenced by frustration or boredom. 

> During the start-up phase of the game, players can start playing using more traditional modalities such as key- board and mouse. During this phase, the BCI collects training data, with ground- truth based on events in the game. A simple approach would be to use the key presses as ground truth for an actual-movement paradigm. The computer collects training data until a BCI can be trained with sufficient performance. BCI control is then en- abled, while still allowing the user to continue playing with the keyboard. Slowly the influence of the keyboard can be decreased, until the player is playing using only the BCI.
>