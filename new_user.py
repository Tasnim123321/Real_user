import random
import time
import hashlib
import json
from datetime import datetime

# ডিভাইস ডাটাবেস (আপনার দেওয়া ডাটা)
DEVICES = {
    "iPhone": [
        {"model": "iPhone16,1", "name": "iPhone 15 Pro", "os": "iOS 17.1"},
        # ... আপনার বাকি ডিভাইস লিস্ট
    ],
    "Android": [
        {"model": "SM-S918U", "name": "Galaxy S23 Ultra", "os": "Android 13"},
        # ... আপনার বাকি ডিভাইস লিস্ট
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
        return f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/{webkit} Mobile/{unique_num % 100000} Safari/{webkit}"
    else:
        chrome_ver = f"{100 + (unique_num % 41)}.0.{6000 + (unique_num % 1001)}.{50 + (unique_num % 51)}"
        return f"Mozilla/5.0 (Linux; Android {device['os'].split('/')[0]}; {device['model']}) AppleWebKit/537.36 Chrome/{chrome_ver} Mobile Safari/537.36"

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
    # আপনার ইউনিক আইডি (এটি পরিবর্তন করলে সম্পূর্ণ নতুন UA পাবেন)
    USER_ID = "Fahim_123_#_SecretKey"
    
    # ৫০০টি ইউনিক UA জেনারেট
    ua_list = get_unique_ua_list(USER_ID)
    
    # JSON ফাইলে সেভ
    output = {
        "user_id": USER_ID,
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_ua": len(ua_list),
        "user_agents": ua_list
    }
    
    with open(f'ua_{USER_ID[:5]}_{datetime.now():%Y%m%d}.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(ua_list)}টি ইউনিক UA জেনারেট হয়ে সেভ হয়েছে!")
