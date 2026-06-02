"""Quick POST test for domain verification."""
import re
import requests

s = requests.Session()
r = s.get("http://localhost:8000/dominios/")
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
csrf = m.group(1) if m else ""
r2 = s.post(
    "http://localhost:8000/dominios/",
    data={"csrfmiddlewaretoken": csrf, "url": "eo01testchibcha99999.com"},
    headers={"Referer": "http://localhost:8000/dominios/"},
)
print("status", r2.status_code)
if "no está siendo ocupada" in r2.text:
    print("PASS: available message")
elif "utilizada" in r2.text or "existe" in r2.text:
    print("NOT available / in use")
else:
    print("UNKNOWN - snippet:")
    for needle in ("resultado", "alert", "ocupada", "disponible"):
        i = r2.text.lower().find(needle)
        if i >= 0:
            print(r2.text[max(0, i - 80) : i + 200])
            break
    else:
        print(r2.text[:1500])
