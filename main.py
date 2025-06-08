from canvas import Canvas
from factory import CommandFactory

class Main:
    def run(self):        
        canvas = Canvas()
        factory = CommandFactory(canvas)
        factory.print_help_text()
        while True:
            try:
                user_input = input("Please Enter a command. \n")
                if not user_input:
                    print("No input provided. Please try again.")
                input_arr = user_input.strip().split(" ")
                cmd = factory.get_command(input_arr)
                if cmd: 
                    cmd.process(input_arr)
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    main = Main()
    main.run()
