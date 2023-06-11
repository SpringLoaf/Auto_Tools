# Auto_Tools

### Table Of Contents
1. [Auto_Move](#auto_move)
2. [Map_Extractor](#map_extractor)
3. [TPS_Extractor](#tps_extractor)

Tree:
```
Auto_Tools
    |- Auto_Move
    |   |- main.py
    |
    |- Map_Extractor
    |   |- main.py
    |   |- ublock_origin-1.49.2.xpi
    |
    |- TPS_Extractor
    |   |- main.py
    |   |- ublock_origin-1.49.2.xpi
```

### Requirements:

Python 3.x.x:
```python -V```

Dependencies:
```pip install pyautogui selenium json csv```

---
## Auto_Move
Functions:
- Automatically moves the cursor and presses the shift key to avoid sleep timer every minute

## Map_Extractor 

Function:
 - Copies the address line of selected map point and the city.
 - Outputs to scraper.csv

Sample (No Headers):
| Address | City |
|------|------|
|1201 Joy Trl|Clermont|
|1202 Joy Trl|Clermont|

## TPS_Extractor


Configuration[^1]:
| Param | Defaults |
|------|------|
|output_filename|output.csv|
|input_filename|scraper.csv|
|max_numbers|3|
|max_names|1|
|city|Saint Cloud|

## Roadmap
 - [x] Drink Coffee
 - [ ] Integration of 3 scripts to a single script

[^1]: Will appear once script has been run once