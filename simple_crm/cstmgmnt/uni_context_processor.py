from datetime import datetime

def application_info(request):
  ctx = {
    "application_name" : "simple crm",
    "now": datetime.now(),
    "version": "1.0",
    "copyrights": "Karol Zalecki",
    "contact": "karolzalecki@gmail.com",
  }
  return ctx
