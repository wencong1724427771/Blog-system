# dic = {'1':1}
# print(dic.get('2',2))  # 2


# print(list(zip(range(1,6),range(1,6))))

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(BASE_DIR)
print(BASE_DIR1)