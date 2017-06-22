# Stabby Bot!

Things are finally reasonably functional! Much more work will be added and tweaked over the coming days, but for now the core code functions properly and bots can be coded.

## Coding Bots
Bots are written as simple python scripts and should reside in the same folder as server.py. Two example bots are provided for reference. Each bot should always include several things:
  1. Importing the library module
  2. Initialize the bot as the CBot class, giving in a fun name 
  3. For as long as the bot is active:
     * Get the current state of the map from the server
	 * Send a response for what action the bot should take for that round
And that's it! Bot moves are sent as a string, and currently include:
  * 'forward' - To take one step forward
  * 'rotCW' - To rotate clockwise 90 degrees
  * 'rotCCW' - To rotate counterclockwise 90 degrees
(Things are rather simple at the moment!)
