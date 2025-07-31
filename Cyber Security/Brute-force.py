import itertools
import time

target=input("Enter a Target:")
print(target)
possible_value="abcdefghijklmnopqrstuvwxyz0123456789@#$%%^$^&*^"
max_length=len(target)
def brute_force_password_cracker():
    attempts=0
    st=time.time()
    for i in range(1,max_length+1):
        for guess in itertools.product(possible_value,repeat=max_length):
            attempts+=1
            guess="".join(guess)
            print(guess)
            if guess==target:
                print(f"password found:{guess}")
                print(f"Time taken :{time.time()-st}seconds")
                print(f"Total Attempts:{attempts}")
                return
brute_force_password_cracker()


# import itertools
# import time

# def password_cracker(password):
#     characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#     attempts = 0
#     start_time = time.time()

#     for length in range(1, 6):  # Adjust the range for longer passwords if needed
#         for guess in itertools.product(characters, repeat=length):
#             attempts += 1
#             guess_password = ''.join(guess)
#             if guess_password == password:
#                 end_time = time.time()
#                 elapsed_time = end_time - start_time
#                 return f"Password '{password}' cracked! Attempts: {attempts}, Time taken: {elapsed_time:.2f} seconds"
    
#     return "Password not found within the given constraints."
