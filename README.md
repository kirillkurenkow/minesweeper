# minesweeper
Minesweeper game

## Usage
### Install requirements
```powershell
python -m pip install -r requirements.txt
```
### Start game
```powershell
usage: minesweeper.py [-h] [-g {easy,normal,hard,custom}] [--height [9-100]]
                      [--width [9-100]] [--mines-count [10-200]] [--debug]

options:
  -h, --help            show this help message and exit
  -g {easy,normal,hard,custom}, --game-mode {easy,normal,hard,custom}
                        Game mode
  --height [9-100]      Cells in column
  --width [9-100]       Cells in row
  --mines-count [10-200]
                        Mines on field
  --debug               Debug
```
#### Examples
```powershell
python minesweeper.py
```
```powershell
python minesweeper.py -g hard
```
```powershell
python minesweeper.py -g custom --width 30 --height 30 --mines-count 30
```