# Output the 3rd element of the following array to the console

num = [1, 2, 3, 4, 5]

arr = ["Hello", "Sowmya","Medisetty"]


print(arr)
#length of the array
print(len(arr))
print(arr[0])
print(arr[1])
print(arr[2])

print("Reversed:")

#reversed:  -1 refers to the last element, -2 to the second-to-last, and so on.
print(arr[-1])
print(arr[-2])
print(arr[-3])

#append: Adds an element to the end of the list.
arr.append("welcome to the team")
print(arr)

#insert: Adds an element at a specific position in the list.
arr.insert(1,"Ms")
print(arr)

#remove(): Removes the first occurrence of a specified item.
arr.remove("welcome to the team")
print(arr)

#pop(): Removes and returns an item at a specified index (or the last item if no index is specified).
arr.pop(1)
print(arr)

numbers = [1, 2, 3, 4, 5]
# Take a number as input and add it to the end of the list
new_number = 7
numbers.append(new_number)
#numbers.insert(5,new_number)
print(numbers)

combined_arr = arr+numbers
print(combined_arr)

#user inputs --string
arrStr = input().split()
#How are you ?
#['How', 'are', 'you', '?']
print(arrStr)

#integer
arrInt = list(map(int,input().split()))
#1520 6583
#[1520, 6583]
print(arrInt)

#tuples
data_tuples = (1,"hello",9.0, True,1)
#len(): This tells you how many items are in a tuple.
#count(): This tells you how many times a specific item appears in a tuple.
print(len(data_tuples))
print("No of times :" ,data_tuples.count(1))

for item in data_tuples :
    print(f"Value: {item}, Type: {type(item)}")

while True:
    try:
        num = int(input("Enter a number: "))
        #arr = list(map(int, input().split()))
        break
    except ValueError:
        print("Invalid input! Please enter a number.")

print("You entered:", num)

#----------------------

dict_countries = {"India": "New Delhi","USA" : "Washington, D.C.", "United Kingdom" : "London", "Japan":"Tokyo", "Australia" :"Canberra"}

def get_captials(country):
    return dict_countries.get(country)
name = input("Enter Country name:")
print ("Capital:", get_captials(name))

#
def get_capitals(country1):
    if country1 in dict_countries:
      return dict_countries[country1]
    else:
        print("Country not found")

student = {"Sowmya":"90",
             "Arjun": "75",
             "Arnav" : "95"
             }

def get_highest_score(higest_score) :
   name = max(higest_score, key=higest_score.get)
   return name, higest_score[name]

student, higest_score = get_highest_score(students)
print("Top student:", student)
print("Highest score:", higest_score)