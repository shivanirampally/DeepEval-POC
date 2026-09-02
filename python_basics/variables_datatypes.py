#Variables declaration
project_name = "Python Basics"
test_cases = 5
evaluation_threshold = 0.8
evaluation_enabled = True

#Print variables using print statement
print("project:",project_name)
#print variables using concate strings by type conversion
print("test_cases:"+str(test_cases))
#Print variables using Escape Characters in f-string formatting
print(f'evaluation_threshold: \"{evaluation_threshold}\"')
#F-String formatting
print(f'evaluation_enabled: {evaluation_enabled}')

#print using escape character \n (new line)
print("\nData types:")
#print datatype of variables using type()
print(type(project_name))
print(type(test_cases))
print(type(evaluation_threshold))
print(type(evaluation_enabled))