#!/bin/bash

curl "https://lwapp-uks-prod-psearch-01.azurewebsites.net/api/v1/plants/search/advanced" ^
  -H "Accept: application/json, text/plain, */*" ^
  -H "Accept-Language: en-GB,en;q=0.9" ^
  -H "Authorization;" ^
  -H "Connection: keep-alive" ^
  -H "Content-Type: application/json" ^
  -H "DNT: 1" ^
  -H "Origin: https://www.rhs.org.uk" ^
  -H "Referer: https://www.rhs.org.uk/" ^
  -H "Sec-Fetch-Dest: empty" ^
  -H "Sec-Fetch-Mode: cors" ^
  -H "Sec-Fetch-Site: cross-site" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" ^
  -H ^"sec-ch-ua: ^\^"Chromium^\^";v=^\^"122^\^", ^\^"Not(A:Brand^\^";v=^\^"24^\^", ^\^"Google Chrome^\^";v=^\^"122^\^"^" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  --data-raw ^"^{^\^"startFrom^\^":20,^\^"pageSize^\^":20,^\^"includeAggregation^\^":false^}^"