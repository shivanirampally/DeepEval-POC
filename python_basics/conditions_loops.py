scores = [0.91, 0.82, 0.65, 0.74, 0.45]
threshold = 0.70
count_passed = 0
count_failed = 0
for score in scores:
    if score>=threshold :
      print(f"Score:{score} is above threshold:{threshold},status:Pass")
      count_passed+=1
    else:
       print(f"Score:{score} is below threshold:{threshold},status:Fail")
       count_failed+=1

print(f"Totalnumber of scores:{len(scores)}")
print(f"Number of passed scores:{count_passed}")
print(f"Number of failed scores:{count_failed}")

if count_passed == len(scores):
    print("Overall Status: PASS")
else:
    print("Overall Status: FAIL")