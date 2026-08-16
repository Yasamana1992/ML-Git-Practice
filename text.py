word_list = input("please input your text: ").strip().lower().split()
word = word_list[0]
count = 0
equal = 0

for i in range(len(word_list)):
    if len(word_list[i]) == len(word):
        equal += 1
if len(word_list) == 1:
    print("text has only one word!")        
elif len(word_list) == equal:
    print("All words have same length")
else:
    for i in range(len(word_list)):
        if len(word_list[i]) < len(word):
            shrst = word_list[i]
        elif len(word_list[i]) > len(word):
            lngst = word_list[i]
        w = word_list[i]
        for char in w:
            if char != ' ':
                count += 1
    print("number of characters is ", count)
    print("number of words is ", len(word_list))
    print("shortest word is ", shrst)
    print("longest word is ", lngst)

cnt = 0
wanted = input("Which word do you want to count?").strip().lower()

if wanted in word_list:
    for j in range(len(word_list)):
        if word_list[j] == wanted:
            cnt += 1
    print(cnt)
else:
    print("The word should be in text!")