To test the server, you can use [httpie](http://httpie.org), e.g.:

```bash
$ http --json localhost:5000/api/v1.0/player name=Moose password=a
HTTP/1.0 200 OK
Content-Length: 116
Content-Type: application/json
Date: Sun, 06 Sep 2015 11:25:49 GMT
Server: Werkzeug/0.10.4 Python/2.7.8

{
    "id": 1,
    "name": "Moose",
    "password": "pbkdf2:sha1:1000$QE5x2teU$fc1526d71bf14c03b4a0023d162a1b81f90c3667"
}

$
```