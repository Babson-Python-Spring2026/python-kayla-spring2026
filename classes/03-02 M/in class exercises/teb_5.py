# Goal: Accept numbers 1–5 only
# Keep asking until user enters a number between 1 and 5.

txt = 'enter 1-5'
while True: 
    try: 
        x = int(input(txt))
        if x < 1 or x > 5: 
            raise Exception('bad input try again: ')
        
    except ValueError: 
        txt= 'value error, try again: '
    except Exception as e: 
        print(e)