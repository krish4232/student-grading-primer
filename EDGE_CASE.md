# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
**1) The edge case you identified:**
The primer specification states that the `mark` field is optional when creating a new student via the `POST /students` route. Furthermore, a database might be entirely empty. If a `GET /stats` request is made under these conditions, attempting to calculate the average mark will result in a `ZeroDivisionError` (dividing the sum of marks by a length of 0). This would crash the server and return an unhandled 500 Internal Server Error instead of a successful response.

**2) How you have accounted for this in your implementation:**
In `backend/app.py` under the `/stats` route, I implemented a data filtering step before calculating statistics. 
First, I extract only the valid integers by filtering out `None` values. Then, I check if this filtered list of marks is empty. If it is, the API gracefully returns `None` for the average, min, and max, while still accurately reporting the total `count` of students in the system. This ensures the endpoint always returns a stable 200 OK status without crashing.