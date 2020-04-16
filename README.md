# Yara file analyzer

This is a simple flask app that when run, only accepts certain files types at the endpoint `http://localhost:5000/file-upload`, then runs them against yara. 

A http response will be served depending on the result of the Yara scanner. 

### Running
```
First create your config.json file. 
$ docker build -t simple-file-analyzer:latest .
$ docker run -p 5000:5000 simple-file-analyzer
```

Use postman to test with different file types and to view the response. Post files to `http://localhost:5000/file-upload`.
 Or test via cli: `curl -d 'test' -H 'x-api-key: thisisnotprod' http://localhost:5000/file-upload`