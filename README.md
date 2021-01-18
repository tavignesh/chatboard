# chatboard

## Description

A Discord bot to keep track of user chat activity.

## Self-Hosting/Setup

This guide will help you setup ChatBoard on a server.

### Prerequisites

In order to run ChatBoard, you'll need a server with the following:

* Python 3.0 or higher
* The following modules: discord, asyncio, pymongo, datetime
* A MongoDB Community Server
* A Discord bot token
* An IQ of 5 or higher

### Clone

Clone this repository to your server.

### Config.json

Create a new file in ChatBoard's directory called "config.json" (case-sensitive). In this file add the following (pseudo-json is marked with <>):

```
{
	"token":"<bot token>",
	"prefix":["<desired prefix>"],
	"mongo_url":"<MongoDB URL>"
}```

### Run

Go to the ChatBoard directory and use `python main.py`. 
