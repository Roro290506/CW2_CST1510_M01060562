from app_model.users import register_user, login_user
def main():
    while True:
        print("WElcome To The System!!")
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        
        if choice == '1':
            register_user() 
        elif choice == '2':
            print('Login successful!' if login_user() == True else 'Incorrect login.')
        elif choice == '3':
            print('Goodbye!')
            break
if __name__ == '__main__':
    main()




    
    
    
            
            
            
    