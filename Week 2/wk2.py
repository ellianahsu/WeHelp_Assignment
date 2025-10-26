# Task 1
characters = [
    {"name": "悟空", "x": 0, "y": 0, "side": "left"},
    {"name": "辛巴", "x": -3, "y": 3, "side": "left"},
    {"name": "貝吉塔", "x": -4, "y": -1, "side": "left"},
    {"name": "特南克斯", "x": 1, "y": -2, "side": "left"},
    {"name": "丁滿", "x": -1, "y": 4, "side": "right"},
    {"name": "弗利沙", "x": 4, "y": -1, "side": "right"},
]

def func1(name):
    c = next(char for char in characters if char["name"] == name)
    # next(iterator[, default]): one-way street, moves one step at a time
    distances = [(o["name"], abs(c["x"]-o["x"]) + abs(c["y"]-o["y"]) + (2 if c["side"] != o["side"] else 0))
                 for o in characters if o["name"] != name]
                # Tuple: [(name1, distance1), (name2, distance2),...]
                # Side Penalty: (2 if c["side"] != o["side"] else 0)
                # For Loop: for o in the characters if o["name"] != name, o is other character
    min_dist = min(d for n, d in distances) # get SECOND itme form each tuple
    max_dist = max(d for n, d in distances)

    nearest = "、".join(n for n, d in distances if d == min_dist)
    farthest = "、".join(n for n, d in distances if d == max_dist)

    print(f"最遠{farthest}；最近{nearest}")

print("=====Task 1=====")
func1("辛巴")      # 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空")      # 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")    # 最遠辛巴；最近特南克斯
func1("特南克斯")  # 最遠丁滿；最近悟空


# Task 2
services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800},
]

bookings = {"S1": [], "S2": [], "S3": []}

def func2(ss, start, end, criteria):
    available_services = []
    
    # For Loop 每個服務
    for service in ss:
        # Check time availability
        time_is_free = True # 假設時段是可預約的
        for booking in bookings[service["name"]]:
            if start < booking["end"] and end > booking["start"]:
            # 客戶時段跟現有預約重疊: 開始<結束 and 結束>開始
                time_is_free = False
                break
        
        if not time_is_free:
            continue # 跳過這個服務,檢查下一個
            
        # Check if meets criteria
        meets_requirement = False
        # 預設不符合條件
        if ">=" in criteria:
            parts = criteria.split(">=") #  "c>=800" → ["c", "880"]
            field = parts[0].strip() # field ="c"
            value = float(parts[1]) # value ="800.0"
            if field in service: # 檢查服務是否有"c"欄位
                meets_requirement = service[field] >= value # c>=800
                
        elif "<=" in criteria: 
            parts = criteria.split("<=")
            field = parts[0].strip()
            value = float(parts[1])
            if field in service:
                meets_requirement = service[field] <= value
                
        elif "=" in criteria: # "name=S1"
            parts = criteria.split("=")
            field = parts[0].strip()
            value = parts[1].strip().replace('"', '')
            if field == "name":
                meets_requirement = service["name"] == value # name =="S1"?
            elif field in service:
                meets_requirement = service[field] == float(value) 
        
        if meets_requirement:
            available_services.append(service)
            # if meet require, add 

    # If no services available
    if len(available_services) == 0:
        print("Sorry")
        return
    
    # Pick the best one
    chosen = available_services[0]
    
    # 如果有多個選項
    if len(available_services) > 1:
        field = criteria.split(">=")[0].strip() if ">=" in criteria else \
                criteria.split("<=")[0].strip() if "<=" in criteria else None
        
        if field in ("r", "c"):
            if ">=" in criteria:
                # For >=, pick minimum
                for s in available_services:
                    if s[field] < chosen[field]:
                        chosen = s
            elif "<=" in criteria:
                # For <=, pick maximum
                for s in available_services:
                    if s[field] > chosen[field]:
                        chosen = s
    
    print(chosen["name"])
    bookings[chosen["name"]].append({"start": start, "end": end})

print("=====Task 2=====")
func2(services, 15, 17, "c>=800")   # S3
func2(services, 11, 13, "r<=4")    # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5")  # S1
func2(services, 16, 18, "r>=4")    # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500")   # S2  


#  Task 3
#  [25, 23, 20, 21], [23, 21, 18, 19], [21, 19, 16, 17]...
#  每4個數字為一個循環 [-2, -3, +1, +2]
def func3(index):
    seq = [25]
    diffs = [-2, -3, 1, 2]

    for i in range(1, index + 1):
        diff = diffs[(i - 1) % len(diffs)]
        seq.append(seq[i - 1] + diff)

    print(seq[index])

print("=====Task 3=====")
func3(1)  # 23
func3(5)  # 21
func3(10)  # 16
func3(30)  # 6

# Task 4
def func4(sp, stat, n):
    # (available space, status bitmap, passenger number)

    avail_car = -1
    # 因0為可用車廂,不能使用0為place holder, -1為還沒找到車廂

    min_diff = float('inf') 
    # 'inf' 無限大

    for i in range(len(sp)): # len -> index num, 看每個車廂
        if stat[i] == '0': #判斷車廂是否能用, 只看可用的(0), 不能用(1)
            diff = abs(sp[i] - n) #車廂座位和需要的座位差多少
            # abs() 以距離來比較, 不是以方向
            if diff < min_diff: #這個車廂比之前找到的更好嗎？ min_diff(previous index)
                min_diff = diff # 更新最小差值
                avail_car = i  # 記住幾號車廂
    
    print(avail_car)
    return avail_car  #回傳最合適車廂編號



print("=====Task 4=====")
func4([3, 1, 5, 4, 3, 2], "101000", 2)  # 5
func4([1, 0, 5, 1, 3], "10100", 4)      # 4
func4([4, 6, 5, 8], "1000", 4)          # 2