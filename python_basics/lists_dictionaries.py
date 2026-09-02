#create a list of test case ids
test_case_ids = ["TC001","TC002","TC003","TC004"]
print("Testcase_IDs_in_List:",test_case_ids)

#print using for loop + index manipulation:
for i in range(len(test_case_ids)):
    print("Testcase_IDs_using_for_loop:",test_case_ids[i])

#print using for loop + Direct Iteration
for test_case_id in test_case_ids:
    print("Testcase_ID_Direct_Iteration:", test_case_id)

#Create dictonary of testcase details
test_case={
    "id": "TC001",
    "input": "What is the capital of France?",
    "expected_output": "Paris",
    "threshold": 0.8
}

#Add category to the testcase dictionary
test_case["category"] = "Geography"

#Print the testcase details using dictionary keys
print("\nTestcase with category:", test_case)
print("Testcase ID:", test_case["id"])
print("Testcase_Input:",test_case["input"])
print("Testcase_Expected_Output:",test_case["expected_output"])
print("Testcase_Threshold:",test_case["threshold"])
print("Testcase_category:",test_case["category"])