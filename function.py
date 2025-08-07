from define import WEIGHT_FACTORS,START_DATE,END_DATE,PROVINCES,FEMALE_NAMES,MALE_NAMES,SURNAMES
from datetime import datetime, timedelta
import numpy as np
import os

def cal_lastNum18(nums:str)->str:
    temp = 0
    for i in range(17):
        temp += int(nums[i]) * WEIGHT_FACTORS[i]
    temp = temp % 11
    if temp <2: 
        return str(1-temp)
    elif temp ==2:
        return 'X'
    else:
        return str(12-temp)
    
def summon_randDate7_14()->str:
    start_time = datetime(START_DATE[0],START_DATE[1],START_DATE[2])
    end_time = datetime(END_DATE[0],END_DATE[1],END_DATE[2])
    deltaTime = end_time-start_time
    
    random_days = np.random.randint(0,deltaTime.days+1)
    random_date = start_time + timedelta(days = random_days)
    
    return random_date.strftime("%Y%m%d")

def summon_rand1_6()->str:
    random_key = np.random.choice(list(PROVINCES.keys()))
    random_proID = PROVINCES[random_key]
    return random_proID+'0101'

def summon_rand15_17(flag:int)->str:
    if flag == 1:
        rand_sexID = np.random.randint(0,4)*2+1
    elif flag ==2:
        rand_sexID = np.random.randint(1,4)*2
    else:
        rand_sexID = np.random.randint(1,10)
    rand_front = np.random.randint(0,100)
    rand_front = "{:02d}".format(rand_front)
    return rand_front+str(rand_sexID)


def summon_randPersonID(flag:int)->str:
    newPersonID = ""
    newPersonID += summon_rand1_6()+summon_randDate7_14()+summon_rand15_17(flag)
    newPersonID += cal_lastNum18(newPersonID)
    return newPersonID

def summon_randChineseName(gender: int = 0) -> str:
    """
    随机生成中文姓名
    :param gender: 0随机,1男,2女
    :return: (姓名, 性别)
    """
    surname = np.random.choice(SURNAMES)
    
    if gender == 1:  # 男
        name = ''.join(np.random.choice(MALE_NAMES, size=np.random.randint(1, 3)))
        return f"{surname}{name}"
    elif gender == 2:  # 女
        name = ''.join(np.random.choice(FEMALE_NAMES,size=np.random.randint(1, 3)))
        return f"{surname}{name}"
    else:  # 随机
        if np.random.random() > 0.5:
            name = ''.join(np.random.choice(MALE_NAMES, size=np.random.randint(1, 3)))
            return f"{surname}{name}"
        else:
            name = ''.join(np.random.choice(FEMALE_NAMES, size=np.random.randint(1, 3)))
            return f"{surname}{name}"

def summon_newPerson(flag:int) -> tuple:
    # 保存到当前目录下的log子目录
    personID = summon_randPersonID(flag)
    personName = summon_randChineseName(2-personID%2)
    
    today = datetime.now().strftime("%Y%m%d")
    log_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(log_dir, exist_ok=True)  # 确保log目录存在
    filename = os.path.join(log_dir, f"{today}.txt")
    
    # 写入文件
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(personID+' '+personName + '\n')
    
    return (personID,personName)
    


