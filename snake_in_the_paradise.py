import sys

class Snake:
    
    _had_error = False

    @staticmethod
    def _main():
        
        args = sys.argv[1:]

        if len(args) > 1:
            print("Usage: Snake [script]")
            sys.exit(64)

        elif (len(args) == 1):
            Snake._runFile(args[0])

        else:
            Snake._runPrompt()
    
    @staticmethod
    def _runFile(path: str):
        
        file = open(path, "r")
        source = file.read()
        file.close()
        Snake._run(source)
        
        if (Snake._had_error):
            sys.exit(65)
    
    @staticmethod
    def _runPrompt():
        
        while True:
            
            line = input("Seduce Eve > ")
            
            if (line == "Take the apple"):
                print("You have left the paradise")
                break

            else:
                Snake._run(line)
                Snake._had_error = False

    @staticmethod
    def _run(source: str):
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        
        for i in tokens:
            print(i)

    @staticmethod
    def error(line: int, message: str):
        
        Snake._report(line, "", message)


    @staticmethod
    def _report(line: int, where: str, message: str):
        
        print(f"[line {line}] Error {where}: {message}")
        Snake._had_error = True


if __name__ == "__main__":

    Snake._main()










