# Project Proposals

## Simple Conway's Game of Life
This project is an implementation of the cellular automaton Conway's Game of
Life. MVP is just a standard bare-bones implementation where people can set the
starting condition and rules. A stretch goal would be using the output to create/modulate sound/pictures and/or using pictures/audio as an input

Our audience would be artsy people probably, or people who enjoy playing the game of life.

The libraries we would need would likely be pygame and numpy.

For the mid project check-in it would be good to have classes for each different type of cells done.

The biggest risk with this project is that there are a lot of moving parts and it doesn't really look like anything if we don't successfully combine it all well.



## Music Visualizer from Mic Input
This project is a music visualizer based on microphone input. The exact visual
details of the visualizer are to be determined, but it will probably be
modulated on some combination of volume and frequency of sound input. Our MVP is
as written above, and stretch goals include added complexity in visual output
(fancy shapes, different modes, etc.) and more granular sound input.

Since our proposal is art-based, the communities of people who would be
interested in it includes people who are interested in computational art in the
visual and music spheres. With this in mind, it'll be centered on ease of use to
make displaying the art easier.

In terms of libraries, this project will probably need some sort of numerical
data structures (perhaps `numpy` or similar), a library that handles
graphics (`graphics`, `pygame`, or something else), a library that
handles sound (specifically sound input).

We will have a concrete framework of specific libraries used before the mid-project
check-in. By then, we should also have some sort of input data stream from the
microphone that we can then process later. We should also have a UML diagram on
a somewhat granular level, and a division of future work that enables us to
complete the project efficiently.


## Music/Sound Generation from Camera Input
Generating music/sounds based on the average color taken from a camera. It would change between different pitches based on what is in the frame, and as a stretch goal create different chords based on the colors.

This project would be designed for people who are interested in music generation and the interaction between colors and music, or people who are interested in hearing some trippy sounds.

In terms of libraries that we will use - opencv will probably be pretty useful for getting a camera input and then interpreting it, numpy for dealing with numerical evaluation and things, and we will have to do some research on different libraries that we can use for music generation.

For the mid-project check-in we hope to be able to get a camera input and interpret it, and deal with the music generating part after.

The biggest risks to our success on this project are likely coordinating work between three people and ensuring that we don't have a ton of merge issues.

## Shift in game due to recent events
Instead of Conway's game of life, we decided to do a game in which a person is living through the covid-19 pandemic. The main character has to go through the game avoiding sick people and finding activities to do to keep busy (as not being bored is one of the objectives of the game). If health level is lowered, they must go to a doctor that can help restore health. 

The character must also collect "essential" items such as toilet paper and face masks to survive the game. Though these aren't actually crucial for survival, it is meant to bring a sense of humor to the game.

## Learning Goals:
Aydin - I'd like to have more experience with git as a tool, and working on
larger-scale projects with multiple people in general. Prior to now, I've only
worked on individual projects, so working with more people than just myself is
something I should get used to.

Gian - I’d like to better my collaboration with people when it comes to python (or just software in general). I also want to understand how to use python better through seeing potentially easier ways of accomplishing the same task.

Kate - I'd like to get better at using git and also figuring out how to work with other people on a software project since I haven't had a ton of experience with that. In terms of the actual project that we work on, I'm really open to anything since I feel like I'm going to learn a decent amount no matter what.
