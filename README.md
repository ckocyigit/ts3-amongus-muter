<!-- ABOUT THE PROJECT -->
## About The Project

This bot is a little project I've started to automize muting for Teamspeak3 when playing among us. There are a lot of bots for discord but we do like to use Teamspeak thats why I tried to come up with this bot.

This bot works with the AmongUsCapture and uses it's WebSocket to gather Among Us game events.
Check out: https://github.com/denverquane/amonguscapture

<!-- GETTING STARTED -->
## Getting Started

This bot connects to the server query from Teamspeak3.
It needs a server group and a channel to organize everything.

An example:

- Among Us(Servergroup) with negative talk power
- Among Us(Channel) with 0 talk power

everyone with the servergroup will be muted and that's how to bot manages to mute people

### Prerequisites

- config.json configured
- Teamspeak3 Servergroup and channel
- AmongUs Capture working and running

### Installation

Download config and exe and run it after starting among us capture
These exe's does not have to be in the same location.

### Upcoming features?

- Manage muting dead people and persisting mutes
