* You'll need an instagram client: http://instagram.com/developer/clients/manage/
* Config is done with env variables
* I deploy to heroku and I use a script like this to manage config locally:

```bash
#!/usr/bin/env bash

INSTAGRAM_CLIENT_ID=...
export INSTAGRAM_CLIENT_ID
INSTAGRAM_CLIENT_SECRET=...
export INSTAGRAM_CLIENT_SECRET
BASE_URL=...
export BASE_URL
REDISTOGO_URL=...
export REDISTOGO_URL

python partysupply.py $*;
```

* Subscribe to a tag with: `python partysupply.py subscription add tag starbucks`
* List subscriptions with `python partysupply.py subscription list`
