#!/bin/bash

curl -X POST "https://api-nvaa.onrender.com/predict" -H "Content-Type: application/json" \
-d '{"appearance":1 , "highest_value":100000000}'
