import random
import time
import hashlib
import json
from datetime import datetime

# ডিভাইস ডাটাবেস (অপরিবর্তিত)
DEVICES = {
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

def generate_user_seed(user_id):
    """ইউজার আইডি ভিত্তিক সিড জেনারেটর"""
    return int(hashlib.sha256(user_id.encode()).hexdigest(), 16)

def generate_ua(device, user_id):
    """ইউনিক UA জেনারেটর"""
    timestamp = int(time.time() * 1000)
    unique_num = (timestamp + generate_user_seed(user_id)) % 1000000
    
    if "iPhone" in device["name"]:
        ios_ver = f"{15 + (unique_num % 3)}_{unique_num % 6}"
        webkit = f"{600 + (unique_num % 16)}.1.{10 + (unique_num % 41)}"
        return f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/{webkit} (KHTML, like Gecko) Mobile/{unique_num % 100000} Safari/{webkit}"
    else:
        chrome_ver = f"{131 + (unique_num % 8)}.0.{6000 + (unique_num % 1001)}.{50 + (unique_num % 51)}"  # Chrome 131-138
        return f"Mozilla/5.0 (Linux; Android {device['os'].split('/')[0]}; {device['model']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"

def get_unique_ua_list(user_id, count=500):
    """ইউনিক UA লিস্ট জেনারেটর"""
    random.seed(generate_user_seed(user_id + datetime.now().strftime("%Y%m%d")))
    ua_dict = {}
    
    while len(ua_dict) < count:
        device = random.choice(DEVICES['iPhone'] + DEVICES['Android'])
        ua = generate_ua(device, user_id)
        ua_hash = hashlib.md5(ua.encode()).hexdigest()
        ua_dict[ua_hash] = ua
    
    return list(ua_dict.values())

if __name__ == "__main__":
    # ইউনিক আইডি (পরিবর্তন করলে নতুন UA পাবেন)
    USER_ID = "Fuck_you_beby"  # এখানে আপনার আইডি দিন
    
    # ৫০০টি ইউনিক UA জেনারেট
    ua_list = get_unique_ua_list(USER_ID)
    
    # JSON ফাইলে অটো সেভ
    output = {
        "user_id": USER_ID,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "total_ua": len(ua_list),
        "user_agents": ua_list
    }
    
    filename = f"ua_{datetime.now():%Y%m%d}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(ua_list)}টি ইউনিক UA জেনারেট হয়ে '{filename}' ফাইলে সেভ হয়েছে!")
