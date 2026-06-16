# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
**1) The edge case you identified:**
The primer specification states that the mark field is not necessary when creating a new student via the `POST /students` route. Also, a database could be empty. If a `GET /stats` request is made under these conditions, attempting to calculate the average mark will result in a `ZeroDivisionError` (dividing the sum of marks by a length of 0). This would crash the server and return an unhandled 500 Internal Server Error instead of a successful response.

**2) How you have accounted for this in your implementation:**
In `backend/app.py` under the `/stats` route, I implemented a data filtering step before calculating statistics. 
Firstly, extract the valid integers by filtering out `None` values. Then, check if this filtered list of marks is empty. If it is, the API returns `None` for the average, min, and max, while still reporting the total `count` of students in the system. This ensures the endpoint always returns a stable 200 OK status without crashing.