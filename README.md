# Foobar

Library allows quick and convenient flection finding.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install flection-dict
```

## Usage

```python
from flection_dictionary.DictLib import *

if __name__ == "__main__":
    files = ["files/pospolite (1).txt", "files/adj.txt", "files/WS_tylko_rzecz.txt", "files/adv.txt", "files/im_nom.txt"]
    file_types = [0, 1, 2, 1, 1]
    bt = DictLib(files, file_types)  # creates WordLib structure
    
    print("Loaded")
    while True:
        input_ = input()
        if input_ == "exit":
            break
        lexemes = bt.find(input_)
        if lexemes:
            for b in lexemes:
                print(b)
```

To open different files simply place there their paths. 
File types are as follows: 
    0 - Regular file
    1 - Filter file
    2 - Multi Segment Words file

To see how these files are suppose to be written see files in example.
After Loading you will ba able to type a word you wish to find, if you wish to exit write "exit".

For full documentation in Polish see **flection-lib-dokumentacja.pdf** file

## Creators
**Grzegorz Janosz & Michał Szczepaniak**

## License
[MIT](https://choosealicense.com/licenses/mit/)
