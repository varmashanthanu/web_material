## Wrod Fxier

This is a spin-off of the Daily Jumble games available in newspapers.

#### How To:
##### Setup
###### Environment
- Python3
- `pip install -r requirements.txt` for packages
- Get PostgreSQL
- Create a Database named `YOUR_DB_NAME`
- Export `SECRET_KEY` environment variable after generating a SECRET KEY
- Export PostgreSQL `DATABASE_URL` envrionment variable as "`postgresql://localhost/YOUR_DB_NAME`"
- Export `HOST` and `PORT` variables as convenient. (`localhost` and `5000` in my case.)
###### Run
- `python3 app.py`
###### Play
- You need to make sure you have a collection of words in your dictionary.
- Add words by going to "Add Words" tab and adding individual words, or uploading a CSV file with a column titled "Word" having all the words you like
- Go to "Create Puzzle" and enter the Question - Answer combination with a difficulty setting to create the puzzle.
- Share the URL for the puzzle and you are done!

---
#### Coming Up:
- Custom/Personal Dictionaries
- Timer and Scorekeeping
- Arcade Mode
