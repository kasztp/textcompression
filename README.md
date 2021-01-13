# TextCompression
Basic Text compression service experiment with Flask. Work in progress! :)

Demo: https://k97lbf4hv8.execute-api.us-east-1.amazonaws.com/dev/compress


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
