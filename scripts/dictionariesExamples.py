student = {"Sowmya":"90",
             "Arjun": "75",
             "Arnav" : "95"
             }

def get_highest_score(higest_score) :
   name = max(higest_score, key=higest_score.get)
   return name, higest_score[name]

student, higest_score = get_highest_score(student)
print("Top student:", student)
print("Highest score:", higest_score)


#alernative
def highest_scores(student): 
   max_name =""
   max_score= -1

   for name,score in student.items:
       if score > max_score :
          max_score = score
          max_name= name

   return max_name,max_score

student1, higest_score2 = get_highest_score(student)
print("Top student:", student1)
print("Highest score:", higest_score2)
      
   