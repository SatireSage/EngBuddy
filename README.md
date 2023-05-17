# EngBuddy

Authors: [Sahaj Singh](https://github.com/SatireSage)

EngBuddy is your personal engineering assistant available 24/7 on the ESSS Discord server. With its advanced AI capabilities, EngBuddy provides personalized support to help you succeed in your studies and build meaningful connections with your peers.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Key Features](#key-features)
  - [Question and Answer](#question-and-answer)
  - [Custom Image Generation](#custom-image-generation)
  - [Course Information and Outline](#course-information-and-outline)
  - [Professor Ratings](#professor-ratings)
  - [Course Ratings](#course-ratings)
  - [RetroPie Arcade Integration](#retropie-arcade-integration)
- [Additional Features](#additional-features)
  - [Ephemeral Messages](#ephemeral-messages)
  - [Direct Messaging (DM) with EngBuddy](#direct-messaging-dm-with-engbuddy)

Follow these steps to set up the project on your local machine for development and testing purposes. To start using EngBuddy on the ESSS Discord server, simply join the server and start using the slash commands to access the features described above.

### Prerequisites

Ensure that you have the following software installed on your machine:

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. Clone the repo

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span></span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/your_username/Algorithm-Visualizer.git
</code></div></div></pre>

2. Install the required packages

Navigate to the project directory and run:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg></button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install -r requirements.txt</code></div></div></pre>

## Key Features

EngBuddy offers the following features to help you with your engineering studies:

### 1. Question and Answer (/ask \*args)

Have a question about engineering or your studies? EngBuddy can provide you with detailed answers using the ChatGPT integration. Just ask your question using the slash command and EngBuddy will respond with an answer.

### 2. Custom Image Generation (/imagine \*args)

Need a visual representation of a concept or idea? EngBuddy can generate images based on your description using DALL-E v2 integration. Describe what you want, and EngBuddy will create an image to match your request.

### 3. Course Information and Outline (/sfu \*args and /outline \*args)

Looking for information on specific SFU courses? EngBuddy can provide you with course details and outlines using the Course Outlines REST API. You'll have access to important course information with just a simple slash command.

### 4. Professor Ratings (/rate_prof \*args)

Want to know how other students rate a particular professor? EngBuddy can retrieve ratings for SFU professors by scraping data from ratemyprofessors.com, giving you insights into the professor's teaching style and effectiveness.

### 5. Course Ratings (/rate_course \*args)

Curious about the overall rating of a specific course? EngBuddy can provide you with course ratings by scraping data from the coursediggers website and extracting information from an SQLite database. This helps you make more informed decisions about your course selections.

### 6. RetroPie Arcade Integration (In Progress)

EngBuddy is working on a new feature to show active games running on RetroPie arcade systems. This will inform users about the currently played game and whether or not the arcade is in use, allowing you to join in on the fun or know when it's available.

## Additional Features

### Ephemeral Messages

To reduce bot clutter in the server, EngBuddy uses ephemeral messages. These messages are only visible to the user who invoked the command, ensuring a cleaner chat experience for everyone.

### Direct Messaging (DM) with EngBuddy

Need more personalized assistance or prefer a one-on-one conversation? You can directly message EngBuddy on Discord and chat with it using the ChatGPT integration. Just send a DM to EngBuddy and start asking your questions.

## Contributing

If you would like to contribute to the development of EngBuddy, please feel free to fork the repository and submit a pull request. We welcome any ideas and improvements to make EngBuddy even more useful for engineering students.
