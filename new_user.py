import random
from datetime import datetime
import hashlib
import json

# আপনার দেওয়া ডিভাইস লিস্ট (বিস্তারিত ভাবে রাখলাম)
devices = {
    "iPhone": [
        {"model": "iPhone16,1", "name": "iPhone 15 Pro", "os": "iOS 17.1"},
        {"model": "iPhone15,5", "name": "iPhone 14 Pro Max", "os": "iOS 16.6"},
        {"model": "iPhone14,5", "name": "iPhone 13", "os": "iOS 16.5"},
        {"model": "iPhone14,6", "name": "iPhone SE (2022)", "os": "iOS 15/16/17"},
        {"model": "iPhone13,1", "name": "iPhone 12 mini", "os": "iOS 14/15/16"},
        {"model": "iPhone11,8", "name": "iPhone XR", "os": "iOS 12/13/14/15"}
    ],
    "Android": [
        {"model": "SM-S918U", "name": "Galaxy S23 Ultra", "os": "Android 13"},
        {"model": "SM-A146U", "name": "Galaxy A14 5G", "os": "Android 13"},
        {"model": "SM-F731U", "name": "Galaxy Z Flip 5", "os": "Android 13"},
        {"model": "Pixel 8 Pro", "name": "Pixel 8 Pro", "os": "Android 14"},
        {"model": "Pixel 7a", "name": "Pixel 7a", "os": "Android 13"},
        {"model": "XT2315-4", "name": "Moto G Power 5G", "os": "Android 13"},
        {"model": "CPH2451", "name": "OnePlus 11 5G", "os": "Android 13"},
        {"model": "LM-G900TM", "name": "LG Velvet 5G", "os": "Android 12"},
        {"model": "SM-S906U", "name": "Galaxy S22+", "os": "Android 12/13"},
        {"model": "SM-A236U", "name": "Galaxy A23 5G", "os": "Android 12/13"},
        {"model": "SM-F936U", "name": "Galaxy Z Fold 4", "os": "Android 12/13"},
        {"model": "GB17L", "name": "Pixel 6a", "os": "Android 12/13"},
        {"model": "GD1YQ", "name": "Pixel 5", "os": "Android 11/12"},
        {"model": "BE2028", "name": "OnePlus Nord N20 5G", "os": "Android 11/12"},
        {"model": "LE2125", "name": "OnePlus 9 Pro", "os": "Android 11/12"},
        {"model": "XT2213-2", "name": "Moto G 5G (2023)", "os": "Android 12/13"},
        {"model": "XT2205-2", "name": "Moto Edge (2022)", "os": "Android 12"},
        {"model": "T817S", "name": "TCL 30 XE 5G", "os": "Android 12"},
        {"model": "TA-1390", "name": "Nokia X100", "os": "Android 11"}
    ]
}

def generate_unique_seed(user_id):
    """ইউনিক সিড জেনারেটর (ইউজার আইডি + তারিখ)"""
    today = datetime.now().strftime("%Y%m%d")
    combined = f"{today}_{user_id}"
    return int(hashlib.sha256(combined.encode()).hexdigest(), 16)

def generate_ua(device):
    """ডিভাইস অনুযায়ী ইউজার এজেন্ট জেনারেটর"""
    if "iPhone" in device["name"]:
        ios_ver = f"{random.randint(15, 17)}_{random.randint(0, 5)}"
        webkit = f"{random.randint(600, 615)}.1.{random.randint(10, 50)}"
        return (f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_ver} like Mac OS X) "
                f"AppleWebKit/{webkit} (KHTML, like Gecko) Mobile/15E{random.randint(100, 500)} Safari/{webkit}")
    else:
        android_ver = device['os'].split('/')[0]  # প্রথম ভার্সন নেয়া (Android 12/13 → 12)
        chrome_ver = f"{random.randint(100, 140)}.0.{random.randint(6000, 7000)}.{random.randint(50, 100)}"
        return (f"Mozilla/5.0 (Linux; Android {android_ver}; {device['model']}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver} Mobile Safari/537.36")

def get_daily_ua(user_id="Fahim_123", num=500):
    """প্রতিদিনের জন্য ইউনিক UA লিস্ট"""
    random.seed(generate_unique_seed(user_id))
    ua_set = set()
    
    while len(ua_set) < num:
        device = random.choice(devices["iPhone"] + devices["Android"])
        ua = generate_ua(device)
        ua_set.add(ua)
    
    return list(ua_set)

if __name__ == "__main__":
    USER_ID = "Fahim_123"  # আপনার ইউনিক আইডি
    ua_list = get_daily_ua(USER_ID)
    
    print("="*50)
    print(f"আজকের জন্য {len(ua_list)}টি ইউনিক UA:")
    print("="*50)
    print("\n".join(ua_list[:5]))  # শুধু প্রথম ৫টি দেখাবে
    
    # JSON ফাইলে সেভ
    today = datetime.now().strftime("%Y%m%d")
    with open(f"ua_{USER_ID}_{today}.json", "w") as f:
        json.dump({"user_agents": ua_list}, f, indent=2)
