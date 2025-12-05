tasks = []
while True:
    print("\n--- TO DO LIST ---")
    print("1. Add task")
    print("2. View tasks") 
    print("3. Delete tasks")
    print("4. Exit")
    choice = input("Choose an option: ")

if choice == "1":
    task = input("Enter new task: ")
    tasks.append(task)
    print("Task added!")
elif choice == "2":
    if len(tasks) == 0:
        print("No tasks yet!")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
elif choice == "3":
    task_number = int(input("Enter task number to delete: "))
    if 1 <= task_num <= len(tasks):
        tasks.pop(task_num - 1)
        print("Task deleted!")
    else:
        print("Invalid task number!")
elif choice == "4":
    print("Goodbye!")
    
else:
    print("Invalid choice, try again!")