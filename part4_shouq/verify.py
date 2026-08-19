#!/usr/bin/env python3
"""
فحص شامل لمشروع HBnB — Part 4

يشغّل السيرفر تلقائياً، يختبر كل مهمة، ثم يوقفه.
شغّليه من داخل مجلد part4_shouq بأمر واحد:

    python verify.py

ما يحتاج طرفية ثانية، وما يلمس قاعدة بياناتك — يبني وحدة مؤقتة.
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "http://127.0.0.1:5000/api/v1"

ok = 0
fail = 0
notes = []


def check(condition, label, detail=""):
    """يسجّل نتيجة فحص واحد."""
    global ok, fail
    if condition:
        ok += 1
        print(f"  ✅ {label}")
    else:
        fail += 1
        print(f"  ❌ {label}   {detail}")
        notes.append(label)


def head(title):
    print(f"\n════ {title} ════")


def request(method, path, body=None, token=None):
    """طلب HTTP يرجّع (الحالة، الرد)."""
    req = urllib.request.Request(API + path, method=method)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, data, timeout=15) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        raw = error.read()
        try:
            return error.code, json.loads(raw or b"null")
        except ValueError:
            return error.code, raw.decode(errors="replace")[:120]


# ══════════════════════════════════════════════════
#  الجزء الأول — الملفات والتنسيق (بدون سيرفر)
# ══════════════════════════════════════════════════

def check_files():
    head("الصفحات والملفات")
    for name in ("index.html", "login.html", "place.html", "add_review.html",
                 "styles.css", "scripts.js"):
        path = os.path.join(HERE, name)
        exists = os.path.isfile(path)
        lines = sum(1 for _ in open(path, encoding="utf-8-sig")) if exists else 0
        check(exists, f"{name} موجود ({lines} سطر)")

    head("الأصناف والمعرّفات المطلوبة")
    markup = ""
    for name in ("index.html", "login.html", "place.html", "add_review.html"):
        markup += open(os.path.join(HERE, name), encoding="utf-8-sig").read()
    for needle in ('class="logo"', "login-button", 'id="login-link"',
                   'id="places-list"', 'id="price-filter"', "place-card",
                   "details-button", 'id="place-details"', "place-info",
                   "review-card", 'id="add-review"', 'class="form"'):
        check(needle in markup, needle)

    head("القيم الثابتة المطلوبة في CSS")
    css = open(os.path.join(HERE, "styles.css"), encoding="utf-8-sig").read()
    for selector in (".place-card", ".review-card"):
        match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
        block = match.group(1) if match else ""
        for prop, value in (("margin", "20px"), ("padding", "10px"),
                            ("border", "1px solid #ddd"), ("border-radius", "10px")):
            found = re.search(rf"{prop}\s*:\s*{re.escape(value)}\s*;", block)
            check(bool(found), f"{selector} {prop}: {value}")

    head("ربط الصفحات بالكود والصور")
    for name in ("index.html", "login.html", "place.html", "add_review.html"):
        page = open(os.path.join(HERE, name), encoding="utf-8-sig").read()
        check('src="scripts.js"' in page, f"{name} يستدعي scripts.js")
        check('href="styles.css"' in page, f"{name} يستدعي styles.css")
    missing = [src for src in sorted(set(re.findall(r'src="(images/[^"]+)"', markup)))
               if not os.path.isfile(os.path.join(HERE, src))]
    check(not missing, "كل الصور موجودة", f"مفقودة: {missing}")

    head("إعدادات الاتصال")
    scripts = open(os.path.join(HERE, "scripts.js"), encoding="utf-8-sig").read()
    check("http://127.0.0.1:5000/api/v1" in scripts, "عنوان الـAPI صحيح في scripts.js")
    init = open(os.path.join(HERE, "app", "__init__.py"), encoding="utf-8-sig").read()
    check("CORS(app" in init, "CORS مفعّل في app/__init__.py")


# ══════════════════════════════════════════════════
#  الجزء الثاني — المهام الأربع (مع سيرفر حقيقي)
# ══════════════════════════════════════════════════

def check_api():
    head("المهمة 1 — تسجيل الدخول")
    status, data = request("POST", "/auth/login",
                           {"email": "omar@test.com", "password": "pass1234"})
    token = data.get("access_token") if isinstance(data, dict) else None
    check(status == 200 and bool(token), "دخول صحيح → 200 + توكن", f"({status})")
    if not token:
        return
    check(len(token.split(".")) == 3, "التوكن JWT بثلاثة أجزاء")
    status, _ = request("POST", "/auth/login",
                        {"email": "omar@test.com", "password": "wrong"})
    check(status == 401, "كلمة سر غلط → 401", f"({status})")
    status, _ = request("POST", "/auth/login",
                        {"email": "nobody@example.com", "password": "pass1234"})
    check(status == 401, "إيميل غير مسجّل → 401", f"({status})")

    head("المهمة 2 — قائمة الأماكن والفلتر")
    status, places = request("GET", "/places/")
    check(status == 200 and isinstance(places, list) and places,
          f"قائمة الأماكن → {len(places) if isinstance(places, list) else '?'} مكان")
    required = {"id", "title", "price", "description", "latitude", "longitude"}
    check(not (required - set(places[0])), "كل الحقول المطلوبة موجودة",
          f"ناقص: {required - set(places[0])}")
    check(all(place["price"] > 0 for place in places), "كل الأسعار أكبر من صفر")
    prices = sorted(place["price"] for place in places)
    print(f"     الأسعار: {prices}")
    for limit in (10, 50, 100):
        count = sum(1 for price in prices if price <= limit)
        check(count > 0, f"فلتر ≤{limit} يطلّع {count} مكان")

    head("المهمة 3 — تفاصيل مكان")
    place_id = places[0]["id"]
    status, details = request("GET", "/places/" + place_id)
    check(status == 200, "جلب التفاصيل → 200", f"({status})")
    check("owner" in details, "بيانات المالك موجودة")
    check("amenities" in details, f"المرافق موجودة ({len(details.get('amenities', []))})")
    print(f"     {details.get('title')} · ${details.get('price')}")
    status, _ = request("GET", "/places/does-not-exist")
    check(status == 404, "معرّف خاطئ → 404", f"({status})")

    head("المهمة 4 — إضافة مراجعة")
    status, reviews = request("GET", "/reviews/")
    check(status == 200 and isinstance(reviews, list),
          f"قائمة المراجعات → {len(reviews) if isinstance(reviews, list) else '?'}")
    check(all("place_id" in review for review in reviews),
          "كل مراجعة فيها place_id (الفلترة بالصفحة تشتغل)")

    reviewed = {review["place_id"] for review in reviews}
    free = [place for place in places if place["id"] not in reviewed]
    target = free[0]["id"] if free else place_id
    status, body = request("POST", "/reviews/",
                           {"text": "Calm and clean", "rating": 5, "place_id": target},
                           token)
    check(status == 201, "مراجعة جديدة → 201", f"({status}) {body}")
    status, _ = request("GET", "/reviews/")
    check(status == 200, "المراجعة انحفظت")
    status, body = request("POST", "/reviews/",
                           {"text": "Again", "rating": 4, "place_id": target}, token)
    check(status == 400 and "already" in str(body).lower(),
          "نفس المكان مرتين → 400", f"({status}) {body}")

    _, sara = request("POST", "/auth/login",
                      {"email": "sara@test.com", "password": "pass1234"})
    status, body = request("POST", "/reviews/",
                           {"text": "Mine", "rating": 5, "place_id": target},
                           sara.get("access_token"))
    check(status == 400 and "own" in str(body).lower(),
          "مراجعة مكانك → 400", f"({status}) {body}")
    status, _ = request("POST", "/reviews/",
                        {"text": "No token", "rating": 5, "place_id": target})
    check(status == 401, "بدون توكن → 401", f"({status})")
    for rating in (0, 9):
        status, _ = request("POST", "/reviews/",
                            {"text": "Bad", "rating": rating, "place_id": target}, token)
        check(status == 400, f"تقييم {rating} مرفوض → 400", f"({status})")

    head("الصلاحيات")
    status, _ = request("POST", "/amenities/", {"name": "Pool"}, token)
    check(status == 403, "مستخدم عادي يضيف مرفق → 403", f"({status})")
    _, admin = request("POST", "/auth/login",
                       {"email": "admin@test.com", "password": "123456"})
    status, _ = request("POST", "/amenities/", {"name": "Rooftop Pool"},
                        admin.get("access_token"))
    check(status == 201, "الأدمن يضيف مرفق → 201", f"({status})")


def main():
    print("╔" + "═" * 46 + "╗")
    print("║      فحص HBnB — Part 4 · Simple Web Client   ║")
    print("╚" + "═" * 46 + "╝")

    check_files()

    # قاعدة بيانات مؤقتة — قاعدتك الأصلية ما تنمس
    workdir = tempfile.mkdtemp(prefix="hbnb_verify_")
    env = {**os.environ, "PYTHONPATH": HERE,
           "HBNB_INSTANCE": workdir, "PYTHONIOENCODING": "utf-8"}
    server = None
    try:
        print("\n… تجهيز بيانات تجريبية وتشغيل السيرفر")
        subprocess.run([sys.executable, "seed_data.py"], cwd=HERE, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        server = subprocess.Popen([sys.executable, "run.py"], cwd=HERE, env=env,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                request("GET", "/places/")
                break
            except Exception:
                time.sleep(0.5)
        else:
            print("  ❌ ما قدرت أشغّل السيرفر على المنفذ 5000.")
            print("     تأكدي إنه مو شغّال أصلاً بطرفية ثانية.")
            return 1
        check_api()
    finally:
        if server:
            server.send_signal(signal.SIGTERM)
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
        shutil.rmtree(workdir, ignore_errors=True)

    print("\n" + "─" * 48)
    print(f"  النتيجة:  {ok} ناجح  ·  {fail} فاشل")
    if fail:
        print("\n  اللي يحتاج مراجعة:")
        for note in notes:
            print(f"    • {note}")
    else:
        print("  \U0001F389 كل شيء تمام — المشروع جاهز للتسليم.")
    print("─" * 48)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
