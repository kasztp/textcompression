# TextCompression [![Pylint](https://github.com/kasztp/textcompression/actions/workflows/pylint.yml/badge.svg)](https://github.com/kasztp/textcompression/actions/workflows/pylint.yml)
Basic Text compression service experiment with Flask.

## Input example for text:
```
{ 
  "mode": "compress", 
  "payload": "input text"
}
```
--------------------------------------
## Input example for url:
```
{
  "mode": "compress",
  "payload": "url"
}
```
--------------------------------------
## Input example for compressed data:
```
{
  "mode": "extract",
  "original_length": original_length,
  "payload": {
    "dictionary": {
      "0": "data",
      "1": "compressed"
      }
    "text": "1 0"
  }
}
```
