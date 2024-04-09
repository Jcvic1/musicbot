# Musicbot
Musicbot is a telegram bot written in python using aiogram. It generates music data including track based on user search.
Working sample [Musicbot](https://t.me/MuzikwithLyricsbot)

## Usage
* Install all requirements.
* Create an env file. Add telegram bot token and yandex_token to sync with yandex for music data. Note that account with subscription will have full access to music data.
* Execute main.py file to run.



## Documentation
```
COMMANDS
    Start -  Starts bot.
    Refresh - Resets bot for new search if reply is delayed from server or for new search.
    Cancel - Cancel current state of bot.

BUTTONS

    Track - Retrieves track details of current search text.
    Get Track - Retrieves track file.
    Get Lyrics - Retrieves lyrics of current track if exist.

    Album - Retrieves album details of current search text.
    Get Track List - Retrieves button for each track in album.
    Get Album Track - Retrieves all track files in album.

    Artist - Retrieves artist details of current search text.
    Social Buttons - Redirects to repective links.
    Get Albums by *Artist name* - Retrieves all albums of current artist.

    Similar Suggestions - Retrieves list of possible similar search text. It is useful when current search result isnt accurate. Retry search with closest from suggestion text.

HINT

    For more accurate search, add artist name and track title in search text.

```

## Disclaimer
This project is developed for educational purpose only. The author does not encourage anyone to
use this for any illegal or un-ethical purpose.
