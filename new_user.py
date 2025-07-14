import random
from datetime import datetime
import hashlib
import requests
import json

def load_devices_from_github():
    try:
        url = "https://raw.githubusercontent.com/yourusername/devices/main/devices.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return json.loads(response.text)
    except:
        pass
    return None

devices = load_devices_from_github() or {
    "iPhone": [
        {"model": "iPhone16,1", "name": "iPhone 15 Pro", "os": "iOS 17.1"},
        {"model": "iPhone15,5", "name": "iPhone 14 Pro Max", "os": "iOS 16.6"},
        {"model": "iPhone14,5", "name": "iPhone 13", "os": "iOS 16.5"}
    ],
    "Android": [
        {"model": "SM-S918U", "name": "Galaxy S23 Ultra", "os": "Android 13"},
        {"model": "SM-A146U", "name": "Galaxy A14 5G", "os": "Android 13"},
        {"model": "SM-F731U", "name": "Galaxy Z Flip 5", "os": "Android 13"},
        {"model": "Pixel 8 Pro", "name": "Pixel 8 Pro", "os": "Android 14"},
        {"model": "Pixel 7a", "name": "Pixel 7a", "os": "Android 13"},
        {"model": "XT2315-4", "name": "Moto G Power 5G", "os": "Android 13"},
        {"model": "CPH2451", "name": "OnePlus 11 5G", "os": "Android 13"},
        {"model": "LM-G900TM", "name": "LG Velvet 5G", "os": "Android 12"}
    ]
}

def generate_iphone_ua(device):
    ios_main = random.randint(15, 17)
    ios_sub = random.randint(0, 5)
    webkit = f"{random.randint(600, 615)}.1.{random.randint(10, 50)}"
    mobile_id = f"15E{random.randint(100, 500)}"
    return (
        f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_main}_{ios_sub} like Mac OS X) "
        f"AppleWebKit/{webkit} (KHTML, like Gecko) "
        f"Version/{ios_main}.{ios_sub} Mobile/{mobile_id} Safari/{webkit}"
    )

def generate_android_ua(device):
    chrome_ver = f"{random.randint(130, 137)}.0.{random.randint(1000, 9999)}.{random.randint(50, 200)}"
    return (
        f"Mozilla/5.0 (Linux; Android {device['os']}; {device['model']}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_ver} Mobile Safari/537.36"
    )

def get_daily_user_agents(user_secret="Fahim_123_@", num=500):
    today = datetime.now().strftime("%Y%m%d")
    combined_seed = today + user_secret + str(random.randint(1000, 9999))
    seed_hash = int(hashlib.sha256(combined_seed.encode()).hexdigest(), 16)
    random.seed(seed_hash)
    
    all_devices = devices["iPhone"] + devices["Android"]
    random.shuffle(all_devices)
    
    ua_list = []
    while len(ua_list) < num:
        for device in all_devices:
            ua = generate_iphone_ua(device) if "iPhone" in device["name"] else generate_android_ua(device)
            if ua not in ua_list:
                ua_list.append(ua)
                if len(ua_list) == num:
                    break
    return ua_list

if __name__ == "__main__":
    print("=" * 50)
    print("আজকের ৫০০টি ইউনিক UA (GitHub থেকে ডিভাইস আপডেট সহ):")
    print("=" * 50)
    print("\n".join(get_daily_user_agents()))