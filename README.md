# GameEventHub
Game based event integrations for multiple systems

This is a rewrite of [misterobs](https://github.com/christopher-roelofs/misterobs) with an event based model. It removes the restriction for only one publisher (MiSTer) and one subscriber (OBS).

Config

```json
{
    "main":{
        "debug":false,
        "images_folder":"C:\\path\\to\\art",
        "fuzzy_match_images":true,
        "fuzzy_match_threshold": 90
    },
    "mister": {
        "ipaddress": "MiSTer",
        "username": "root",
        "password": "1",
        "port":"22",
        "refresh_rate": "1",
        "core_storage": "fat"
    },
    "obs": {
        "host": "localhost",
        "port": "4444",
        "password": ""
    },
    "discord": {
        "application_id":""
    },
    "dashboard": {
        "host":"0.0.0.0",
        "port":8080
    },
    "retroarch":{
        "install_path":"C:\\RetroArch-Win64"
    },
    "steam":{
        "api_key":"",
        "steam_id":""
    }
}
```


Main Config

|  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| debug| true or false   | if debug is enabled
| images_folder|  C:\\\path\\\to\\\art|  path to art folder. You need to escape backslashes.
| fuzzy_match_images| true or false  |  used if art image can't be matched to the filename. 
| fuzzy_match_threshold| 0 to 100  |  Used for fuzzy matching the art image tot he name. Lower than 90 may result in false positives 


```json
 "main":{
        "debug":false,
        "images_folder":"C:\\path\\to\\art",
        "fuzzy_match_images":true,
        "fuzzy_match_threshold": 90
    }
```

## Database

The database used is a slimmed down and modified version of the [OpenVGDB](https://github.com/OpenVGDB/OpenVGDB) database.

**Json Schema**

```json
{
   "uuid":"geberated uuid4",
   "release_name":"Game release name",
   "region":"Game region",
   "system":"Game system",
   "sha1":"Sha1 of rom file",
   "rom_extensionless_file_name":"Rom filename without extension",
   "developer":"Developer",
   "publisher":"Publisher",
   "genre":"Genre/s",
   "date":"Release or published date",
   "description":"Game description",
   "reference_url":"Website with game details",
   "manual_url":"Link to game manual"
}
```

# Publish/Subscribe Model

Any system can be a publisher as long as there is a way to get details out of the system ie scheduled ssh command, reading a local file or making an api call.

Publishers need to have strict events with a mimum of "publisher" and "event" fields. Other fields be added to a list in the tokens field to be used in the subscribers.

```json
{
   "publishers":{
      "publisher1":{
         "description":"connect to system and publish events",
         "status":"enabled",
         "type":"schedule"
      }
   },
   "subscribers":{
      "subscriber1":{
         "status":"enabled",
         "subscribed_events":[
            {
               "SubscribedEvent1":[
                  {
                     "description":"do something to subscribing system",
                     "action":"SubscriberAction1",
                     "status":"enabled",
                     "subscriber_specific_field":"subscriber_specific_value"
                  }
               ]
            },
            {
               "SubscribedEvent1":[
                  {
                    "description":"do something to subscribing system",
                     "action":"SubscriberAction2",
                     "status":"enabled",
                     "subscriber_specific_field":"subscriber_specific_value"
                  }
               ]
            }
         ]
      }
   }
}
```

# Publishers

## [MiSTer](https://github.com/MiSTer-devel/Main_MiSTer/wiki)

**MiSTer** is an open project that aims to recreate various classic **computers**, **game consoles** and **arcade machines**, using modern hardware. It allows software and game images to run as they would on original hardware, using peripherals such as mice, keyboards, joysticks and other game controllers.

The MiSTer publisher uses ssh to get the details on the current game and core.

MiSTer Config
|  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| ipaddress  | 192.168.1.34 or MiSTer   | ip address or hostname 
| username |  root  |  ssh username  
| password| 1  |  ssh password |ssh password for MiSTer
| port| 22  |  ssh port   
| refresh_rate  |  1 |  polling rate of checking the core and game 
| core_storage  | fat or usbx   |  where the cores are stored fat for sd card and usbX for usb 

```json
"mister": {
"ipaddress": "MiSTer",
"username": "root",
"password": "1",
"port": "22",
"refresh_rate": 1,
"core_storage": "fat"
}
```

mister.json

Any fields added to each core entry will be available in the subscriber actions. It will get added to the tokens field of the event. This allows you to customize keys/values for different actions

```json
{
"core_name": {
"system" : "name of the game system. Should match what is used by the database. This is an optional field. If not present, this is set to the core name"
}
}
```


**Events**

MisterGameChange

This event is triggered when a new game is loaded.

```json
"publisher": "MiSTer",
"event" : "MisterGameChange",
"system" : "MiSTer Core",
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```
MisterCoreChange

This event is triggered when a core is changed

```json
"publisher": "MiSTer",
"event" : "MisterGameChange",
"system" : "MiSTer Core or system matched in database",
"core" : "The mister core"
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```


## [Steam](https://store.steampowered.com/)
Steam is a video game digital distribution service by Valve. It was launched as a standalone software client in September 2003 as a way for Valve to provide automatic updates for their games, and expanded to include games from third-party publishers

**Events**

SteamGameChange

This event is triggered when a game is changed
```json
"publisher": "Steam",
"event" : "SteamGameChange",
"game" : "The name of the game",
"tokens": "Details of the game from Steam"
}
```
Game Details 

```json
"name": "Name of the game",
"game_id" : "Gameid of the game",
"description" : "Description of the game",
"reference_url" : "Website for the game",
"developer" : "Developer/s of the game",
"publisher" : "Publisher/s of the game",
"genre" : "Genre/s of the game",
}
```


## [Retroarch](https://www.retroarch.com/)

RetroArch is a frontend for emulators, game engines and media players.

It enables you to run classic games on a wide range of computers and consoles through its slick graphical interface. Settings are also unified so configuration is done once and for all.

In addition to this, you are able to run original game discs (CDs) from RetroArch.

RetroArch has advanced features like shaders, netplay, rewinding, next-frame response times, runahead, machine translation, blind accessibility features, and more!

**Events**

RetroarchGameChange

This event is triggered when a game is changed

```json
"publisher": "Retroarch",
"event" : "RetroarchGameChange",
"system" : "Retroarch Core or system matched in database",
"core" : "The retroarch core"
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```




# Subscribers

## [OBS](https://obsproject.com/)

## [Discord Rich Presense](https://discord.com/developers/docs/intro)

## Webapp Dashboard
 
 ## Custom Script
