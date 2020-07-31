def calculate(data, findall):
    matches = findall(r"([abc])([-+]?)=([abc]?)([-+]?\d*)")
    for v1, sign, v2, number in matches:
        tmp = data.get(v2, 0) + int(number or 0)
        if sign:
            tmp = data[v1] + int(sign + '1') * tmp
        data[v1] = tmp
    return data
