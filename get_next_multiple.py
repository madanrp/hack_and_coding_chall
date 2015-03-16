
def get_next_multiple(num):
    MAX_NUM = 2000
    power = [0 for i in range(MAX_NUM)]
    value = [0 for i in range(MAX_NUM)]

    tens = 1
    for i in range(1,MAX_NUM):
        value[i] = tens;

        for j in range(0, MAX_NUM):
            if power[j] and not power[(j + tens) % num] and power[j] != i:
                power[(j + tens) % num] = i

        if power[tens] == 0:
            power[tens] = i

        tens = (10 * tens) % num #remainder

        if(power[0]):
            break

    count = 0
    if power[0] != 0:
        i = num
        string = ""
        while num > 0:
            count -= 1
            while count > (power[i % num] - 1):
                string += "0"
                count -= 1
            count = power[ i % num] - 1
            string += "1"
            i = (num + i - value[power[i % num]]) % num
        while count > 0:
            string += "0"
            count -= 1

    return string
          

print get_next_multiple(4)
