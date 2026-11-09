# xelp: mark a film / show / season / episode watched or unwatched from the info page button.
# RunScript(special://skin/extras/xelp_watched.py,<dbtype>,<dbid>,<watched 0|1>[,<season>[,<tvshowid>]])
# watched = the item's CURRENT state; the script flips it. Uses the Kodi library (JSON-RPC), so PlexKodiConnect
# sees the playcount changes and passes them on to Plex.
import json, sys, time
import xbmc


def rpc(method, **params):
    r = json.loads(xbmc.executeJSONRPC(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})))
    return r.get("result", {})


def stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def set_episodes(ids, watch):
    for i in ids:
        if watch:
            rpc("VideoLibrary.SetEpisodeDetails", episodeid=i, playcount=1, lastplayed=stamp(), resume={"position": 0, "total": 0})
        else:
            rpc("VideoLibrary.SetEpisodeDetails", episodeid=i, playcount=0, resume={"position": 0, "total": 0})


def main(a):
    dbtype, dbid, watched = a[0], int(a[1]), a[2] in ("1", "true", "True")
    watch = not watched
    if dbtype == "movie":
        if watch:
            rpc("VideoLibrary.SetMovieDetails", movieid=dbid, playcount=1, lastplayed=stamp(), resume={"position": 0, "total": 0})
        else:
            rpc("VideoLibrary.SetMovieDetails", movieid=dbid, playcount=0, resume={"position": 0, "total": 0})
    elif dbtype == "episode":
        set_episodes([dbid], watch)
    elif dbtype == "tvshow":
        eps = rpc("VideoLibrary.GetEpisodes", tvshowid=dbid, properties=["playcount"]).get("episodes", [])
        set_episodes([e["episodeid"] for e in eps if (e.get("playcount", 0) > 0) != watch], watch)
    elif dbtype == "season":
        show = int(a[4]) if len(a) > 4 and a[4] not in ("", "-1") else None
        season = int(a[3]) if len(a) > 3 and a[3] != "" else None
        if show is None or season is None:
            d = rpc("VideoLibrary.GetSeasonDetails", seasonid=dbid, properties=["season", "tvshowid"]).get("seasondetails", {})
            show, season = d.get("tvshowid"), d.get("season")
        eps = rpc("VideoLibrary.GetEpisodes", tvshowid=show, season=season, properties=["playcount"]).get("episodes", [])
        set_episodes([e["episodeid"] for e in eps if (e.get("playcount", 0) > 0) != watch], watch)
    else:
        return
    xbmc.executebuiltin("Container.Refresh")
    xbmc.executebuiltin('Notification(%s,%s,2500)' % ("Marked as watched" if watch else "Marked as unwatched", xbmc.getInfoLabel("ListItem.Label")))


if __name__ == "__main__":
    main(sys.argv[1:])
