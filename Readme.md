# Digital Dodgeball :running:

![Animation Gif](anim.gif)

**A new and improved website is available [here](https://jrembold.github.io/WUPhys-CodeComp/)**

## Coding Bots
Bots are written as simple python scripts and should reside in the Bots folder. Several example bots are provided for reference. Each bot should always include several things:
  1. Importing the library module
  2. Initialize the bot as the CBot class and pass the ```__file__``` so the server can identify bot to script
  3. For as long as the bot is active:
     * Get the current state of the map from the server
	 * Send a response for what action the bot should take for that round

And that's it! Bot moves are sent as a string, and currently include:

  Command | Description
  --- | ---
  'forward' | Takes one step forward in currently facing direction
  'rotCW' | Rotates 90 degrees clockwise
  'rotCCW' | Rotates 90 degrees counter-clockwise
  'ball' | Throws a dodgeball in the currently facing direction
  'ping' | Uses a turn to ping surroundings to get information

*Please note that the server enforces a timebomb mechanic where if your bot does not move from a square in 120 turns, it explodes!*

To influence these moves, each bot is given particular information each round from the server. All this information is saved in the bot CBot class and can be accessed via attributes. Information available at the moment includes:

  Attribute | Description
  --- | ---
  .active | Returns true if the bot is still alive and the round still ongoing
  .playercount | Returns current number of bots still in the round
  .ballcount | Returns the number of dodgeballs you currently have.
  .vision | A list of number values 'seen' by your bot in the direction in is facing. More details below
  .lastping | A dictionary of the last pinged information. More details below

#### Bot Vision
The .vision attribute will return a list of values depicting everything your bot see's in the direction it is looking. *This list will always begin with your bot itself!* The server keeps track of the map in the following fashion:
  * 0 - Nothing is here
  * 1 - There is a wall here
  * 2 digit number - Bot Identification number, there is a bot here
    * Bots will also have a decimal trailing after them which shows what direction they are facing. .0 is straight up, .1 is to the right, .2 is downwards, and .3 is to the left
  * 2 - A traveling dodgeball. *Dangerous!*
    * Like bots, dodgeballs have a trailing decimal indicating their direction of flight
	* Regardless of value, touching them will result in a loss!
  * 3 - A dodgeball that has struck something and fallen *Not dangerous*

#### Last Ping
The .lastping attribute will return a dictionary which has the below keys. Each key returns a list of locations where that object was located. All x and y positions *are relative to the bot itself!*

Key | Description
  --- | ---
  'Terrain' | Any walls or pillars in the bots ping range
  'ABall' | Any active moving dodgeballs in the ping range. Does not give direction
  'DBall' | Any inactive or fallen dodgeballs on the ground nearby
  'Enemy' | Any enemy bots in the nearby vicinity

Recall that the map coordinates have (0,0) in the upper left, so a relative coordinate of (-2,1) means the object is two spaces above you and one space to the right.

## Running the Server
The server is run from a command prompt or shell following normal python conventions. Bots to compete are added to the prompt following a -i option. For example, to run a competition between the RandomMan.py and SimpleMan.py, you'd write:
```Shell
python server.py -i RandomMan.py SimpleMan.py
```
There are several other server flags that may be of use:

  Flag | Default | Use
  --- | --- | ---
  -d *num* | 0 | Playback multiplier to be passed to the viewer. Values of 1-5 will speed up, fractional values will slow down
  -s *num* | 20 | Sets the square size of the arena
  -o *num* | 10 | Sets the maximum number of obstacles scattered about the map
  -v | | Using this flag will suppress the viewer from auto-playing after the battle is over

Running the server with the -h option will output a help file showing these same flags.

## Running the Viewer
The viewer script will by default load the last game replay and _play_ it using a matplotlib interface. It is called automatically if the -v server flag is used, or can be run anytime standalone to rewatch a match. It has a few options:

Flag | Default | Use
--- | --- | ---
-i | lastgame.pickle | If you've saved a game replay under a different name, you can load it with the -i flag
-d | 1 | Speed multiplier of default playback. Matplotlib seems to max out on a multiplier of >5. Fractional values will give slower playback

Again, running the viewer with the -h option will output a help file showing the above flags if you forget.
