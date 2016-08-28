This repository contains additional plugins, and static configuration files, that may be used to customise [PageBot](//github.com/joodicator/PageBot).

## Contents
1. [Installation and Usage](#installation-and-usage)
2. [Available Plugins](#available-plugins)

## Installation and Usage

1. Install [PageBot](//github.com/joodicator/PageBot) as usual, for example into `~/PageBot`.

2. Clone this repository, or download an archive and extract it, into a separate directory, for example `~/fto-PageBot`.

3. For each file in `~/fto-PageBot/conf`, create a symbolic link in `~/PageBot/conf`. For example:

   ```bash
   cd ~/PageBot/conf
   ln -s ../../fto-PageBot/conf/* .
   ```   

4. For each module in `~/fto-PageBot/page`, create a symbolic link in `~/PageBot/page`. For example:

   ```bash
   cd ~/PageBot/page
   ln -s ../../fto-PageBot/page/*.py .
   ```

5. For each symbolic link created in `~/PageBot/page`, add a corresponding entry to `~/PageBot/git/info/exclude`. For example:
   
   ```
    # git ls-files --others --exclude-from=.git/info/exclude
    # Lines that start with '#' are comments.
    # For a project mostly in C, the following would be a good set of
    # exclude patterns (uncomment them if you want to use them):
    # *.[oa]
    # *~
    page/fto.py
   ```
    
   Do not add these entries to any versioned `.gitignore` file in `~/PageBot`. Do not commit any such symbolic links to the main PageBot repository.

6. Add any modules from `~/fto-PageBot/page`, that you wish to use with PageBot, to the `plugins` section of `~/PageBot/conf/bot.py`, and run PageBot as usual.

If new files are added after receiving updates from this repository, you may need to repeat some of the above steps for the new files.

## Available Plugins

#### `fto`
For channels not in `conf/quiet_channels.txt`, gives automatic responses to certain messages; and adds the following commands:
* `!nuke` - kicks the user issuing this command from the channel.

#### `tell_fto`
Modifies the `tell` module with customised messages for some users. (This module automatically loads `tell` when loaded.)
