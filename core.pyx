# 导入Cython的math库
from libc.math cimport log

# 定义一个Cython函数，接受一个字符串列表作为参数
cpdef dict make_wordcost(list words):
    # 创建一个空字典来存储结果
    cdef dict result = {}
    # 遍历列表中的每个元素及其索引
    cdef int i
    cdef str k
    for i, k in enumerate(words):
        # 计算对数值并存储到字典中
        result[k] = log((i + 1) * log(len(words)))
    # 返回结果字典
    return result

# 定义一个Cython函数，接受一个字符串列表作为参数，并返回最长字符串的长度
cpdef int max_string_length(list words):
    # 检查列表是否为空，如果为空则返回0
    if not words:
        return 0
    
    # 初始化最大长度为列表中第一个字符串的长度
    cdef int max_len = len(words[0])
    
    # 遍历列表中的每个字符串
    cdef int len_x
    cdef str x
    for x in words:
        # 计算当前字符串的长度
        len_x = len(x)
        # 如果当前字符串的长度大于已知的最大长度，则更新最大长度
        if len_x > max_len:
            max_len = len_x
    
    # 返回最长字符串的长度
    return max_len

cpdef tuple best_match(int i, list cost, dict wordcost, str s, int maxword):
    cdef int k
    cdef int c
    cdef double min_cost = 9e999
    cdef int min_length = 0
    cdef tuple best_match_tuple = (min_cost, min_length)
    cdef int start_index = max(0, i - maxword)
    cdef int end_index = i
    cdef double candidate_cost = 9e999

    cdef list candidates = list(enumerate(reversed(cost[start_index:end_index])))

    for k, c in candidates:
        candidate_str = s[i-k-1:i] if i-k-1 >= 0 else ''  # Assuming s is a bytes object
        candidate_cost = wordcost.get(candidate_str.lower(), 9e999)
        if c + candidate_cost < min_cost:
            min_cost = c + candidate_cost
            min_length = k + 1
            best_match_tuple = (min_cost, min_length)

    return best_match_tuple
