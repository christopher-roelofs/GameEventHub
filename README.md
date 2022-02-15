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
**Database Manager**

The database manager allows you to edit and add new records to the database.

![image](https://user-images.githubusercontent.com/1930031/153929043-f7e45342-d802-4faf-acbd-b4dcf05c1f9a.png)


-   To create a new record make sure the fields have been cleared. add your new record details and click submit.
-   To edit a record, select the record from the table, edit the fields and then submit.
-   To create a new record based on an existing record, select the record from the table, click duplicate, edit the fields and then submit. A new record with a new uuid will be created. The new record should have a different sha1 or rom name or you will get an error and the record will not be created. 

**Database Tool**

Create Patch.bat (DatabaseTool.exe -c or -createpatch) - This will take a while bceause there are a lot of records and it has to iterate over both databases.

This allows you to create a patch that is a comparison of your current database.json file to an existing database.json file (database.old). Any record that is new or different from the current to the other will be added to a database.patch file that can be used as a backup of changes. This could be applied over a new database.json file after an update to maintain your local changes.

Import Patch.bat (DatabaseTool.exe -i or -import)

This allows you to import a patch

## Images

Some subscriber actions can use an image. See below for more details on the configuration.

**folder_map.json**

This is where the name of the system from the database and the system field in the publishers core json file will be mapped to an art folder per system. The folder names can be custom but the system name needs to match the database. By default the folder names match the  [libretro-thumbnails](https://github.com/libretro-thumbnails)  folders.

The boxart,snap,title, and system folders are the subfolder in each system folder including base art folder Example c:\path\to\art\SNK_-_Neo_Geo\Named_Boxarts

the image names in the systems folder need to match the system names below. if the name has a "/" in it, you need to place it with "-". Example "Sega CD/Mega-CD" becomes "Sega Genesis-Mega Drive.png"

```json
{
   "boxart_folder":"Named_Boxarts",
   "snap_folder":"Named_Snaps",
   "title_folder":"Named_Titles",
   "system_folder":"systems",
   "Atari 2600":"Atari_-_2600",
   "Atari 5200":"Atari_-_5200",
   "Atari 7800":"Atari_-_7800",
   "Atari Lynx":"Atari_-_Lynx",
   "Bandai WonderSwan":"Bandai_-_WonderSwan",
   "Bandai WonderSwan Color":"Bandai_-_WonderSwan_Color",
   "Coleco ColecoVision":"Coleco_-_ColecoVision",
   "GCE Vectrex":"GCE_-_Vectrex",
   "Intellivision":"Mattel_-_Intellivision",
   "NEC PC Engine/TurboGrafx-16":"NEC_-_PC_Engine_-_TurboGrafx_16",
   "NEC PC Engine CD/TurboGrafx-CD":"NEC_-_PC_Engine_CD_-_TurboGrafx-CD",
   "NEC SuperGrafx":"NEC_-_PC_Engine_SuperGrafx",
   "Nintendo Famicom Disk System":"Nintendo_-_Family_Computer_Disk_System",
   "Nintendo Game Boy":"Nintendo_-_Game_Boy",
   "Nintendo Game Boy Color":"Nintendo_-_Game_Boy_Color",
   "Nintendo Game Boy Advance":"Nintendo_-_Game_Boy_Advance",
   "Nintendo Entertainment System":"Nintendo_-_Nintendo_Entertainment_System",
   "Nintendo Super Nintendo Entertainment System":"Nintendo_-_Super_Nintendo_Entertainment_System",
   "Sega Game Gear":"Sega_-_Game_Gear",
   "Sega Master System":"Sega_-_Master_System_-_Mark_III",
   "Sega CD/Mega-CD":"Sega_-_Mega-CD_-_Sega_CD",
   "Sega Genesis/Mega Drive":"Sega_-_Mega_Drive_-_Genesis",
   "Sega Saturn":"Sega_-_Saturn",
   "Sega SG-1000":"Sega_-_SG-1000",
   "SNK Neo Geo":"SNK_-_Neo_Geo",
   "SNK Neo Geo Pocket":"SNK_-_Neo_Geo_Pocket",
   "SNK Neo Geo Pocket Color":"SNK_-_Neo_Geo_Pocket_Color",
   "Magnavox Odyssey2":"Magnavox_-_Odyssey2",
   "Commodore 64":"Commodore_-_64",
   "Microsoft MSX":"Microsoft_-_MSX",
   "Microsoft MSX2":"Microsoft_-_MSX2",
   "Sony PlayStation":"Sony_-_PlayStation",
   "Arcade":"Arcade"
}
```

# Publish/Subscribe Model

Any system can be a publisher as long as there is a way to get details out of the system ie scheduled ssh command, reading a local file or making an api call.

Publishers need to have strict events with a mimum of "publisher" and "event" fields. Other fields be added to a list in the tokens field to be used in the subscribers.

by default pubsub.json is used but you can pass a different file as a command line parameter. This allows you to have multiple setups with different defined publishers and subscribers

pubsub.json
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

**You must enable the recents setting in your .ini file on the MiSTer** : recents=1 ; set to 1 to show recently played games

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
{
"publisher": "MiSTer",
"event" : "MisterGameChange",
"system" : "MiSTer Core",
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```
MisterCoreChange

This event is triggered when a core is changed

```json
{
"publisher": "MiSTer",
"event" : "MisterGameChange",
"system" : "MiSTer Core or system matched in database",
"core" : "The mister core"
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```


## [Steam](https://store.steampowered.com/)
Steam is a video game digital distribution service by Valve. It was launched as a standalone software client in September 2003 as a way for Valve to provide automatic updates for their games, and expanded to include games from third-party publishers

Steam Config

|  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| api_key| FAA4E45BE04FEEDE7FA388BZZD2B   | Steam API key. Following this [link](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey) and sign in with your Steam Account Name and Password. 
| steam_id |  12345678|  numeric steam id. Use [this](https://www.steamidfinder.com/) link to find your steam id.

```json
 "steam":{
        "api_key":"",
        "steam_id":""
    }
```

**Events**

SteamGameChange

This event is triggered when a game is changed
```json
{
"publisher": "Steam",
"event" : "SteamGameChange",
"game" : "The name of the game",
"tokens": "Details of the game from Steam"
}
```
Game Details 

```json
{
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

|  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| install_path| C:\\\RetroArch-Win64 | Install path to Retroarch. You must escape backslashes.

Retroarch Config

```json
 "retroarch":{
        "install_path":"C:\\RetroArch-Win64"
    }
```

retroarch.json

Any fields added to each core entry will be available in the subscriber actions. It will get added to the tokens field of the event. This allows you to customize keys/values for different actions

```json
{
"core_name": {
"system" : "name of the game system. Should match what is used by the database. This is an optional field. If not present, this is set to the core name"
}
}
```

**Events**

RetroarchGameChange

This event is triggered when a game is changed

```json
{
"publisher": "Retroarch",
"event" : "RetroarchGameChange",
"system" : "Retroarch Core or system matched in database",
"core" : "The retroarch core"
"tokens": "Optional fields added to the mister.json file to be used by subriber actions"
}
```




# Subscribers

## [OBS](https://obsproject.com/)

OBS Studio is a free, open-source, and cross-platform screencasting and streaming app. It is available for Windows, macOS, Linux distributions, and BSD.

you need to install obs-websocket which can be found here: [https://github.com/Palakis/obs-websocket/releases](https://github.com/Palakis/obs-websocket/releases).

**Note! The OBS subscriber currently only supports obs-websocket v4.x.x**

![image](https://user-images.githubusercontent.com/1930031/153928910-79a8aab7-4f48-4724-b51d-8f09e6074a22.png)


  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| host  |  localhost  | obs websocket host/ip address  |
| port  | 4444  |  obs websocket port |
|  password | P@ssword | obs websocket password |

OBS Config

```json
 "obs": {
        "host": "localhost",
        "port": "4444",
        "password": ""
    }
```

**Actions**

ObsChangeScene

This actions allows you to change the obs scene based on an event. You can use tokens from the even with {token} for dynamic values. The following is an example of changing the scene based on a MiSter core change. In this scenario, the scene  has the core name with "scene".
```json
{
"description": "Change scene on mister core change",
"action": "ObsChangeScene",
"status": "enabled",
"scene": "{core} Scene"
}
```

ObsChangeSourceText

This actions allows you to change the text of a source based on an event. You can use tokens from the even with {token} for dynamic values.  The following is an example of changing the text of a source when a new game game has been loaded. In this scenario, the source name is using dynamic tokens and the value is also using dynamic tokens. 
```json
{
   "description":"Change source text on game change",
   "action":"ObsChangeSourceText",
   "status":"enabled",
   "sources":{
      "{core} Game":"{release_name}      [{system}]"
   }
}
```

ObsChangeSourceImage

This actions allows you to change the image of a source based on an event. The following is an example of changing the image of a source when a new game game has been loaded. In this scenario, the source name is hard coded based on the type. The keywords boxart, title,snap, and system can be used for the value to get those specific image types. See the Images section above for more details. A filepath can also be use instead of the keywords to use a static image.
```json
{
   "description":"Change source image on game change",
   "action":"ObsChangeSourceImage",
   "status":"enabled",
   "sources":{
      "Boxart":"boxart",
      "Title":"title",
      "Snap":"snap",
      "System":"system"
   }
}
```

ObsSetItemProperty

This actions allows you to change a property of a source based on an event.  The following is an example of setting the visibility property of a source. The source name can use {tokens} to make it dynamic.
```json
{
   "description":"Change source property to not visible",
   "action":"ObsSetItemProperty",
   "status":"enabled",
   "source":"System",
   "property":"visible",
   "value":false
}
```

ObsSetSourceVolume

This actions allows you to change the volume of a source based on an event. This action can use {tokens} for dynamic source names. Volume is in db and is a float (needs t be a string in json). you can add a "type" field and set it to "amp" ie "type":"amp" to use amplitude/mul.

```json
{
   "description":"",
   "status":"enabled",
   "action":"ObsSetSourceVolume ",
   "source":"source name",
   "volume":"-12"
}
```

ObsSetBrowserSourceUrl 

This action allows you to set the url of a browser source. The url and source values can use {tokens} to set them dynamically.
 
```json
{
   "description":"",
   "status":"enabled",
   "action":"ObsSetBrowserSourceUrl ",
   "source":"{}",
   "url":"{}"
}
```

## [Discord Rich Presense](https://discord.com/developers/docs/intro)

![image](https://user-images.githubusercontent.com/1930031/153929599-6ceeb88a-c99e-47cb-9f7b-aa75468b6e49.png)


For the Discord subcriber to work, you need to have the discord application install on the same machine the script is running on. This uses the RPC protocol.

**Setup an appication in Discord that will be used for this integration**

-   Navigate to  [https://discordapp.com/developers/](https://discordapp.com/developers/)
-   Click “Create an Application.”
-   Setup the application how you want, name in MiSTer , and give it a good image.
-   Right under the name of your application, locate your Client ID. You will need this later.
-   Lastly, save your application.

Discord Config

 Config | Example  | Details   |
| ------------ | ------------ | ------------ 
| application_id|  1234567890| Discord application id 

```json
  "discord": {
        "application_id":""
    }
```

**Setup an application in Discord that will be used for this integration**

-   Navigate to  [https://discordapp.com/developers/](https://discordapp.com/developers/)
-   Click “Create an Application.”
-   Setup the application how you want, name in MiSTer , and give it a good image.
-   Right under the name of your application, locate your Client ID. You will need this later.
-   Lastly, save your application.

in the pubsub.json file this requires an extra field for *type* because the library being use is async. 

```json
"Discord":{
   "status":"enabled",
   "type":"async",
   "subscribed_events":[]
}
```
Discord subscriber only has one action so it does not need to be defined. State and details are require, the rest can be left as "" if not wanted. The images are the names of the images uploaded in the developer portal. {tokens} can be used as the values to set them dynamically based on the event. The names will be set to lowercase automatically because discord makes the image names lowercase when uploading. Values for button links can't use {tokens} because discord does not seem to actually apply the change. It is best to use these for links that will not change like a twitch or youtube channel. You can max a max of 2 buttons and if no buttons are wanted remove the buttons field from the json object.

```json
{
   "description":"Set the Discord status for the current game",
   "status":"enabled",
   "state_text":"{release_name}",
   "details_text":"{system}",
   "small_text":"",
   "small_image":"misterkun",
   "large_text":"",
   "large_image":"{core}",
   "buttons":[
      {
         "label":"Button 1",
         "url":"https://www.google.com"
      },
      {
         "label":"Button 2",
         "url":"https://www.google.com"
      }
   ]
}
```



## Webapp Dashboard

This is a simple webserver that will show the game and details. It is a live dashboard. This is a work in progress and is a little rough

![image](https://user-images.githubusercontent.com/1930031/153929170-cc023a9c-f4c2-4394-8f7c-d6c0ebbe2628.png)


Dashboard Config

 Config | Example  | Details   |
| ------------ | ------------ | ------------ 
| host|  0.0.0.0 will use localhost | ip address
| port|  8080| port used
| refresh_rate|  1| how long in between data refresh on page

```json
"dashboard":{
   "host":"0.0.0.0",
   "port":8080,
   "refresh_rate":1
}
```

Action

```json
"dashboard":{
   "host":"0.0.0.0",
   "port":8080,
   "refresh_rate":1
}
```
 
 ## Custom Script
This allows you to write a custom python script that will be used as an action. This can be used if you want a more complicated action. You will not be able to use external libraries not already being used but all standard libraries can be used.  The event class object and the action json object are available to the script. The path to the script can be anywhere and you need to escape backslashes. There is an example in the script github directory.


Action

```json
{
   "description":"custom script on game change",
   "status":"enabled",
   "script":"scripts/custom_script.py"
}
```

Example

In this example, the game details will be written to details.txt in a a specific format for another system to read and act on.

```json
{
   "description":"custom script on game change",
   "status":"disabled",
   "file":"details.txt",
   "script":"scripts/write_details_kruizcontrol.py",
   "format":"KruizControl"
}
```

**The following files are independent of the main program and need to be copied to the scripts folder on the MiSTer and run manually.**

**splitcores.py** - This is used for cores that have multiples systems ie SMS can play Game Gear and SG1000 games. You can use this to create copies of those rbf files named differently so you can have different scenes.

**splitcores.json** - This is used to setup which cores you will copy.

```json
{
    "SMS": ["GAMEGEAR","SG-1000"],
    "ColecoVision": ["SG-1000C"],
    "Gameboy": ["GBC"],
    "Turbografx16": ["TGFX-CD"]
}
```

**splitcores.sh** - Copy this to the scripts folder on the MiSTer to run the splitcores.py script.

**update_and_copy.sh** - Copy this to the scripts folder on the MiSTer to run the update_all script and then run the splitcores.py script
