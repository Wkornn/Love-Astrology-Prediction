"""Convert celebrity locations to lat/long coordinates"""

import json
import requests
import time

CELEBS = [
  { "name": "ประยุทธ์ จันทร์โอชา", "category": "Politicians", "birth_date": "1954-03-21", "birth_time": "12:00", "location": "Nakhon Ratchasima", "district": "Mueang" },
  { "name": "พิธา ลิ้มเจริญรัตน์", "category": "Politicians", "birth_date": "1980-09-05", "birth_time": "12:00", "location": "Bangkok", "district": "Phaya Thai" },
  { "name": "พี่เต้ มงคลกิตติ์", "category": "Politicians", "birth_date": "1981-09-25", "birth_time": "12:00", "location": "Phitsanulok", "district": "Mueang" },
  { "name": "สรยุทธ สุทัศนะจินดา", "category": "Celebs", "birth_date": "1966-05-11", "birth_time": "12:00", "location": "Bangkok", "district": "Khlong Toei" },
  { "name": "หนุ่ม กรรชัย กำเนิดพลอย", "category": "Celebs", "birth_date": "1969-07-18", "birth_time": "12:00", "location": "Bangkok", "district": "Dusit" },
  { "name": "ก้อย อรัชพร", "category": "Celebs", "birth_date": "1994-04-28", "birth_time": "12:00", "location": "Bangkok", "district": "Phaya Thai" },
  { "name": "ลุงเอ", "category": "Celebs", "birth_date": "1973-12-25", "birth_time": "12:00", "location": "Nakhon Si Thammarat", "district": "Phrom Khiri" },
  { "name": "นนท์ ธนนท์", "category": "Celebs", "birth_date": "1996-03-04", "birth_time": "12:00", "location": "Phuket", "district": "Mueang" },
  { "name": "เจฟ ซาเตอร์ (Jeff Satur)", "category": "Celebs", "birth_date": "1995-03-06", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Wa" },
  { "name": "บิวกิ้น พุฒิพงศ์", "category": "Celebs", "birth_date": "1999-10-08", "birth_time": "12:00", "location": "Bangkok", "district": "Pathum Wan" },
  { "name": "พีพี กฤษฏ์", "category": "Celebs", "birth_date": "1999-04-30", "birth_time": "12:00", "location": "Bangkok", "district": "Khlong Toei" },
  { "name": "วิน เมธวิน", "category": "Celebs", "birth_date": "1999-02-21", "birth_time": "12:00", "location": "Bangkok", "district": "Thaling Chan" },
  { "name": "ไบร์ท วชิรวิชญ์", "category": "Celebs", "birth_date": "1997-12-27", "birth_time": "12:00", "location": "Nakhon Pathom", "district": "Mueang" },
  { "name": "เจมีไนน์ นรวิชญ์", "category": "Celebs", "birth_date": "2004-06-13", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Rak" },
  { "name": "โฟร์ท ณัฐวรรธน์", "category": "Celebs", "birth_date": "2004-10-18", "birth_time": "12:00", "location": "Bangkok", "district": "Sathon" },
  { "name": "พีค กองทัพ", "category": "Celebs", "birth_date": "2001-01-26", "birth_time": "12:00", "location": "Bangkok", "district": "Watthana" },
  { "name": "Lisa Blackpink", "category": "Celebs", "birth_date": "1997-03-27", "birth_time": "12:00", "location": "Buriram", "district": "Satuek" },
  { "name": "Rosé Blackpink", "category": "Celebs", "birth_date": "1997-02-11", "birth_time": "12:00", "location": "Auckland, New Zealand", "district": "City Center" },
  { "name": "Cha Eun-woo", "category": "Celebs", "birth_date": "1997-03-30", "birth_time": "12:00", "location": "Gyeonggi, South Korea", "district": "Gunpo" },
  { "name": "V (BTS)", "category": "Celebs", "birth_date": "1995-12-30", "birth_time": "12:00", "location": "Daegu, South Korea", "district": "Seo" },
  { "name": "Jungkook (BTS)", "category": "Celebs", "birth_date": "1997-09-01", "birth_time": "12:00", "location": "Busan, South Korea", "district": "Mandeok" },
  { "name": "Jackson Wang", "category": "Celebs", "birth_date": "1994-03-28", "birth_time": "12:00", "location": "Kowloon, Hong Kong", "district": "Kowloon Tong" },
  { "name": "Byeon Woo-seok", "category": "Celebs", "birth_date": "1991-10-31", "birth_time": "12:00", "location": "Seoul, South Korea", "district": "Paju" },
  { "name": "Wang Yibo", "category": "Celebs", "birth_date": "1997-08-05", "birth_time": "12:00", "location": "Luoyang, China", "district": "Xigong" },
  { "name": "Xiao Zhan", "category": "Celebs", "birth_date": "1991-10-05", "birth_time": "12:00", "location": "Chongqing, China", "district": "Banan" },
  { "name": "ธีร์ Only Monday", "category": "Influencers", "birth_date": "2002-01-21", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Rak" },
  { "name": "กันต์ จอมพลัง", "category": "Influencers", "birth_date": "1990-06-19", "birth_time": "12:00", "location": "Bangkok", "district": "Chatuchak" },
  { "name": "สไปร์ท SPD", "category": "Influencers", "birth_date": "1996-08-14", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Na" },
  { "name": "ซุง Starwin", "category": "Influencers", "birth_date": "1996-12-12", "birth_time": "12:00", "location": "Bangkok", "district": "Min Buri" },
  { "name": "ซ้อการ์ด (Card Kadi)", "category": "Influencers", "birth_date": "1999-01-11", "birth_time": "12:00", "location": "Nakhon Pathom", "district": "Mueang" },
  { "name": "My Mate Nate", "category": "Influencers", "birth_date": "1993-04-10", "birth_time": "12:00", "location": "Utah, USA", "district": "Salt Lake" },
  { "name": "อูโน่หลานทอง", "category": "Influencers", "birth_date": "1997-05-18", "birth_time": "12:00", "location": "Bangkok", "district": "Lat Phrao" },
  { "name": "พันช์รักแมว", "category": "Influencers", "birth_date": "1998-09-15", "birth_time": "12:00", "location": "Bangkok", "district": "Phasi Charoen" },
  { "name": "คมสันต์ ลี (Flash)", "category": "Influencers", "birth_date": "1991-03-25", "birth_time": "12:00", "location": "Chiang Rai", "district": "Mueang" },
  { "name": "คัลแลน", "category": "Influencers", "birth_date": "1990-09-07", "birth_time": "12:00", "location": "Seoul, South Korea", "district": "Gangnam" },
  { "name": "พี่จอง", "category": "Influencers", "birth_date": "1989-04-14", "birth_time": "12:00", "location": "Seoul, South Korea", "district": "Itaewon" },
  { "name": "อ.ใหญ่ (ดร. สันติธรรม พรหมอ่อน)", "category": "Academic", "birth_date": "1978-04-12", "birth_time": "12:00", "location": "Bangkok", "district": "Thung Khru" },
  { "name": "อ. แก๊ส (อ. ราชวิชช์ สโรชวิกสิต)", "category": "Academic", "birth_date": "1985-11-20", "birth_time": "12:00", "location": "Bangkok", "district": "Rat Burana" },
  { "name": "อ. เค (ดร. ประพงษ์ ปรีชาประพาฬวงศ์)", "category": "Academic", "birth_date": "1982-03-15", "birth_time": "12:00", "location": "Nonthaburi", "district": "Pak Kret" },
  { "name": "อ. สนั่น (อ. สนั่น สระแก้ว)", "category": "Academic", "birth_date": "1972-08-08", "birth_time": "12:00", "location": "Pathum Thani", "district": "Khlong Luang" },
  { "name": "อ. โจ้ (ดร. พีรพล ศิริพงศ์วุฒิกร)", "category": "Academic", "birth_date": "1976-02-28", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Khun Thian" },
  { "name": "อ. ณัฐชา (ดร. ณัฐชา เดชดำรง)", "category": "Academic", "birth_date": "1984-06-24", "birth_time": "12:00", "location": "Bangkok", "district": "Yan Nawa" },
  { "name": "อ. วี (ดร.ทวีชัย นันทวิสุทธิวงศ์)", "category": "Academic", "birth_date": "1988-05-17", "birth_time": "12:00", "location": "Samut Prakan", "district": "Phra Pradaeng" },
  { "name": "อ. จุมพล (ดร. จุมพล พลวิชัย)", "category": "Academic", "birth_date": "1979-12-14", "birth_time": "12:00", "location": "Bangkok", "district": "Phra Nakhon" },
  { "name": "อ. ณัฐนาถ (ดร. ณัฐนาถ เหมือนสุวรรณ)", "category": "Academic", "birth_date": "1981-09-19", "birth_time": "12:00", "location": "Nonthaburi", "district": "Mueang" },
  { "name": "อ. บิ๊ก (ดร. จาตุรนต์ หาญสมบูรณ์)", "category": "Academic", "birth_date": "1986-07-07", "birth_time": "12:00", "location": "Chonburi", "district": "Si Racha" },
  { "name": "อ. เตย (ดร. ปิยนิตย์ เอื้ออารีมิตร)", "category": "Academic", "birth_date": "1990-01-25", "birth_time": "12:00", "location": "Bangkok", "district": "Bang Khae" },
  { "name": "อ. แก้ว (ดร. สัญญ์สิริ ธารประดับ)", "category": "Academic", "birth_date": "1987-03-11", "birth_time": "12:00", "location": "Samut Sakhon", "district": "Ban Phaeo" },
  { "name": "อ. เบิร์ด (ดร.บุญฤทธิ์ จันทร์ไกรวัล)", "category": "Academic", "birth_date": "1983-12-03", "birth_time": "12:00", "location": "Bangkok", "district": "Taling Chan" }
]

def geocode(location, district=""):
    """Get lat/long using Nominatim (OpenStreetMap)"""
    query = f"{district}, {location}" if district else location
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'LoveAstrologyApp/1.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def main():
    print("🌍 Geocoding celebrity locations...\n")
    
    results = []
    failed = []
    
    for celeb in CELEBS:
        print(f"📍 {celeb['name']}")
        
        # Try with district first
        lat, lon = geocode(celeb['location'], celeb.get('district', ''))
        
        # Fallback to location only
        if not lat:
            lat, lon = geocode(celeb['location'])
        
        if lat and lon:
            result = {
                "name": celeb['name'],
                "birth_date": celeb['birth_date'],
                "birth_time": celeb['birth_time'],
                "latitude": lat,
                "longitude": lon,
                "timezone": "UTC"
            }
            # Add category if exists
            if 'category' in celeb:
                result['category'] = celeb['category']
            results.append(result)
            print(f"   ✅ {lat:.4f}, {lon:.4f}")
        else:
            failed.append(celeb['name'])
            print(f"   ❌ Failed to geocode")
        
        time.sleep(1)  # Rate limit
    
    # Save to JSON
    output_file = "celebs_with_coords.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ Successfully geocoded: {len(results)}/{len(CELEBS)}")
    print(f"💾 Saved to: {output_file}")
    
    if failed:
        print(f"\n❌ Failed ({len(failed)}):")
        for name in failed:
            print(f"   - {name}")

if __name__ == '__main__':
    main()
