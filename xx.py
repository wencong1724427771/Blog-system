# dic = {'1':1}
# print(dic.get('2',2))  # 2


# print(list(zip(range(1,6),range(1,6))))

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(BASE_DIR)
print(BASE_DIR1)


# s = '111.2'
# print(s.split('.')[0])

# import re
#
# s = '/post/1.html'
#
# find_num = re.compile('(\d+)')
# res_pk = re.search(find_num,s).group()
# print(res_pk)