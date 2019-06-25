# ASU TAS Helper
This is a tool to submit hours worked requests to the ASU Time and Attendance
Support (TAS) system.

# Dependencies
- Python 3
- Python requests
- pycookiecheat

# Usage
It uses pycookiecheat to ~~work around~~ handle authentication. This requires one
to be logged into https://tas.asu.edu in Chrome when submitting a request. The
page is not required to be open.

To use it run `./submit_tas.py start_time end_time` to submit hours worked. It
will round the times to the nearest 15 minutes, then show the hours that it will
submit. The rounding is done in a smart way, to prevent double rounding rounding
(it rounds the start time and the duration, then calculates the correct end
time).

Example to submit a request for working from 9:05 to 12:40.
```
$ ./submit_tas.py 09:05 12:40

time worked: 3:35:00, rounded time worked: 3:30:00, residual: 0:05:00
Submitting start time: 2019-06-13 09:00:00 end time: 2019-06-13 12:30:00
<Response [200]> b'{"logout":false,"returntext":"","error":false} '
```

A failed request will usually returns
```
$ ./submit_tas.py 09:05 12:40
time worked: 3:35:00, rounded time worked: 3:30:00, residual: 0:05:00
Submitting start time: 2019-06-25 09:00:00 end time: 2019-06-25 12:30:00
<Response [200]> b'\r\n #serializeJSON(return_struct)#\r\n '
```

## Notes about how TAS handles authentication
Sometimes if one is logged into https://asu.edu, but has not visited
https://tas.asu.edu recently, submitting the request will fail. Opening
https://tas.asu.edu in Chrome fixes this.

It appears that tas.asu.edu only uses JSESSIONID cookie for authentication. I
think that visiting https://tas.asu.edu when the above issue occures fixes the
problem by gettng TAS to issue a new JSESSIONID cookie, using one's session from
https://asu.edu

# License
This is licensed under the 3-clause BSD license.
