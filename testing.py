from utils import Caller

make = Caller()
print(make.request(endpoint="/learn/api/public/v1/courses/{courseId}/users",
              method="get",
              courseId="_912_1"))

print("*****","\n","*****")

print(make.request(endpoint="/learn/api/public/v1/announcements",
              method="get"))

# print(course_memberships.rate_limits())0
