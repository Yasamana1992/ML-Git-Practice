num = int(input("input number of student: "))
s = []
sum = 0
a = 0

while a < num:
    try:
        for i in range(num):
            s.append(float(input("input grade: ")))
            sum += s[i]
            a += 1
    except ValueError:
        print("just number!")
        pass
    if (len(s) == num):
        break

mean = sum/num
highest = max(s)
lowest = min(s)

print("average: ", mean)
print("highest: ", highest)
print("lowest: ", lowest)