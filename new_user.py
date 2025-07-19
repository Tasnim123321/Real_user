import random
from datetime import datetime
import hashlib

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

def generate_iphone_ua(device):
    ios_main = random.randint(15, 17)
    ios_sub = random.randint(0, 5)
    webkit = f"{random.randint(600, 615)}.1.{random.randint(10, 50)}"
    mobile_id = f"15E{random.randint(100, 500)}"
    
    # Facebook App ভ্যারিয়েশন (70% চান্স)
    if random.random() < 0.7:
        fb_version = f"{random.randint(400, 500)}.0.0.{random.randint(10, 100)}"
        fb_build = f"{random.randint(100000, 999999)}"
        return (f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_main}_{ios_sub} like Mac OS X) "
                f"AppleWebKit/{webkit} (KHTML, like Gecko) "
                f"Mobile/{mobile_id} [FBAN/FBIOS;FBAV/{fb_version};FBBV/{fb_build};FBLC/en_US;]")
    # Chrome ভার্সন (30% চান্স)
    else:
        return (f"Mozilla/5.0 ({device['model']}; CPU iPhone OS {ios_main}_{ios_sub} like Mac OS X) "
                f"AppleWebKit/{webkit} (KHTML, like Gecko) "
                f"Version/{ios_main}.{ios_sub} Mobile/{mobile_id} Safari/{webkit}")

def generate_android_ua(device):
    chrome_ver = f"{random.randint(130, 137)}.0.{random.randint(1000, 9999)}.{random.randint(50, 200)}"
    
    # Facebook App ভ্যারিয়েশন (70% চান্স)
    if random.random() < 0.7:
        fb_version = f"{random.randint(400, 500)}.0.0.{random.randint(10, 100)}"
        fb_build = f"{random.randint(100000, 999999)}"
        return (f"Mozilla/5.0 (Linux; Android {device['os']}; {device['model']}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver} Mobile Safari/537.36 "
                f"[FB_IAB/FB4A;FBAV/{fb_version};FBBV/{fb_build};FBDM/{{density=2.5,width=1080,height=1920}};FBLC/en_US;]")
    # Chrome ভার্সন (30% চান্স)
    else:
        return (f"Mozilla/5.0 (Linux; Android {device['os']}; {device['model']}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver} Mobile Safari/537.36")

def get_daily_user_agents(user_secret="Fahim_123_@", num=500):
    today = datetime.now().strftime("%Y%m%d")
    combined_seed = today + user_secret + str(random.randint(1000, 9999))
    seed_hash = int(hashlib.sha256(combined_seed.encode()).hexdigest(), 16)
    random.seed(seed_hash)
    
    all_devices = devices["iPhone"] + devices["Android"]
    random.shuffle(all_devices)
    
    ua_list = []
    for _ in range(num):
        device = random.choice(all_devices)
        ua = generate_iphone_ua(device) if "iPhone" in device["name"] else generate_android_ua(device)
        ua_list.append(ua)
    return ua_list

if __name__ == "__main__":
    print("=" * 50)
    print("আজকের ৫০০টি ইউনিক UA (Facebook 70%, Chrome 30%):")
    print("=" * 50)
    print("\n".join(get_daily_user_agents()))
