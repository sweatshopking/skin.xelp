# Attribution and changes

**xelp** is a modified version of the **fTV** skin for Kodi by **Hitcher**
(`skin.ftv`, https://kodi.tv/ — licensed Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported,
http://creativecommons.org/licenses/by-nc-sa/3.0/).

As the licence requires, this notice credits the original author and states that changes were made.
xelp is released under the **same licence (CC BY-NC-SA 3.0)**. You may share and adapt it for
**non-commercial** use, with attribution, and any adaptation must carry the same licence.

## What was changed from fTV

- Added `xml/Viewtype57.xml`: a "Poster Grid" library view, registered as the only view for movies, sets,
  TV shows and seasons (`shortcuts/skinviewtypes.json`).
- Replaced the home-page widget template (`ParamWidgetInclude` in `xml/Includes_Parameters.xml`) with real
  scrolling rows; the old six-poster teaser rows and their focus rules were removed from `xml/Home.xml`.
- Added a dimmed backdrop, clock and greeting to the Home window; dimmed unfocused posters.
- Film page default focus, "Watch Now/Resume" first; context-menu hint; title cards for items without art.
- New icon, fanart and screenshots; new name and metadata.

Unchanged parts (fonts, most dialogs, translations, textures, the rest of the XML) are fTV's.
The remaining strings in `language/` are fTV's translations.

## Not included

The author's personal menu, widget choices and Plex settings are *not* in this repository. They live in
your Kodi user data, not in the skin.
