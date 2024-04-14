# RSS to Fax Gateway

## Requirements

1. You will need a CUPS enabled Fax printer (or any other printer if you just want a hard copy)
   This was tested with a AVM Fritzbox and [RogerRouter](https://gitlab.com/tabos/rogerrouter) installed
   and configured correctly. The script defaults to the `Roger-Router-Fax` printer.
2. Rendering is done with selenium on a chrome webdriver backend. If something errors out please check if
   you need to install a `chromedriver` package for your distribution.
3. For converting from PDF to PostScript you need `pdftops` which is usually part of `poppler_utils`
4. To run this you need a modern Python 3 installation (Tested with 3.11.8 on NixOS)
5. I use `poetry` for dependency management, so either install it globally or follow the virtual
   environment instructions below

## Installation

1. Create a python venv: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install poetry: `pip install poetry`
4. Install dependencies: `poetry install --no-root`

(If you're on NixOS, you can use the provided `shell.nix` by typing `nix-shell` in this directory)

## Running

1. Make sure the correct venv is activated:
   ```bash
   deactivate
   source .venv/bin/activate
   ```
2. Run `rss2fax.py`: `python rss2fax.py`

If you're not running with any parameters you will get the help screen.

### Changing settings

You basically only have two settings:

- `fax-printer` which should point to your softfax printer (or any other printer if you
  just want a hardcopy)
- `max-items` which defines how many items per feed should be included at maximum

All settings will be saved automatically when changed.

### Listing subscribed feeds

Run with `--list-feeds` to get a list of subscribed feeds:

```
Loading config from /home/dark/.config/kdedefaults/rss2fax.json
0: Dunkelstern (https://dunkelstern.de/atom.xml)
1: Golem.de (https://rss.golem.de/rss.php?feed=ATOM1.0)
```

You can use the ID numbers in front to unsubscribe a feed

### Unsubscribing from a feed

Run with `--remove-feed <id>` with any ID from the `--list-feeds` command
to unsubscribe from a feed.

### Adding feeds

By default the configuration will contain two feeds, the german tech-news page
golem.de and my blog. To add another just run with `--add-feed <url>`.

If you're not sure if the page you want to subscribe to has a feed URL you
can use the `--discover-feeds <url>` command to search the header metadata for
feed links.

For example if you run this on my blog: 

```
# python rss2fax.py --discover-feeds https://dunkelstern.de
Loading config from /home/dark/.config/kdedefaults/rss2fax.json
https://dunkelstern.de/feed.rss
https://dunkelstern.de/atom.xml
```

You can use one of the URLs to subscribe to.

### Generating a PDF

If you run in `--pdf`-mode the script will output a `render.pdf` with the content
and will not send anything to a printer

### Printing/Sending a Fax

Run in `--fax`-mode to send the generated pages off to the Fax printer you set up.

If you're using Roger Router, make sure it is running in the Background. The Tool
will then pick up the print job from the spooler and pop up with a dialing dialog
where you can specify the phone number to dial up.

