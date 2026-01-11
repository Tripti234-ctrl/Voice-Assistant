Project: Garhwali–Kumaoni Voice Assistant

##Current Implementation Status

- ASR module implemented using OpenAI Whisper (prototype level)
- Sample audio-based transcription tested locally
- Modular design allows replacement with trained regional models
- Output screenshots added for validation

1. System Overview

The Garhwali–Kumaoni Voice Assistant is a voice-based system designed to understand and respond to user commands in regional Himalayan languages (Garhwali and Kumaoni).
The goal of this project is to make technology more accessible for local users who are not comfortable using English or Hindi-based voice assistants.

 Objectives

1. Accept voice input in Garhwali/Kumaoni

2. Convert speech to text

3. Process user intent

4. Respond back in voice form

5. Preserve and promote regional languages


2. High-Level System Architecture
🔹 Architecture Description

The system follows a client–server architecture:

User speaks a command

Microphone/Input Device captures audio

Speech-to-Text (STT) converts audio to text

Language Processing Module interprets intent

Backend Logic processes the request

Database stores commands, responses, logs

Text-to-Speech (TTS) converts response to voice

Speaker outputs response in Garhwali/Kumaoni

🔹 Components Explanation
Component	Description
Frontend	Captures user voice input
STT Module	Converts voice → text
NLP Engine	Understands intent
Backend Server	Handles logic & routing
Database	Stores commands & responses
TTS Module	Converts text → voice

3.  Data Flow Diagrams (DFD)
3.1 DFD Level 0 (Context Diagram)

Explanation:

DFD Level 0 represents the system as a single process interacting with external entities.

Entities:

User

Voice Assistant System

Data Flow:

User → Voice Input

System → Voice Output

3.2 DFD Level 1

Explanation:

DFD Level 1 breaks the system into internal processes:

Voice Capture

Speech-to-Text Conversion

Command Processing

Database Interaction

Text-to-Speech Conversion

4. Database Schema
🔹 Database Description

The database stores:

User commands

Language mappings

Responses

System logs

🔹 Tables
🗂 User_Command Table
Field	         Description
command_id	     Primary Key
command_text	 User spoken command
language	     Garhwali / Kumaoni
timestamp	     Time of command
🗂 Response Table
Field	         Description
response_id	     Primary Key
response_text	 Assistant reply
audio_path     	Path to voice file
🗂 Logs Table
Field        	Description
log_id	        Primary Key
event_type	    Error / Info
message     	Log message
5️⃣ Scalability & Future Growth
a. Scalability Handling

The system is designed to scale by:

Adding multiple backend servers

Using cloud-based speech APIs

Separating STT and TTS services

Optimizing database queries with indexing

b. Future Enhancements

Add more regional languages

Offline voice processing

Mobile application version

AI-based intent prediction

User personalization

6. Failure Handling & Reliability
a. Failure Scenarios

Speech recognition failure

Server downtime

Database unavailability

Network interruption

b.Solutions

Retry mechanism for voice input

Error handling with fallback responses

Regular database backups

Logging and monitoring system

7. Git Workflow & Team Contributions
a.  Git Workflow Followed

Feature branches created for each module

Pull Requests raised for merging

Code review before merge

Main branch kept stable

b. Individual Contributions

Each team member worked on:

Speech-to-text module

Language dataset preparation

Backend API development

Database & documentation

Only code contributions are counted for evaluation