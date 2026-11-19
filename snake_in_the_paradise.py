from scanner import Scanner
from snake_token import Token
from token_type import TokenType
from ast_printer import AstPrinter
from parser import Parser
from runtime_error import RunTimeError
from interpreter import Interpreter

import sys

class Snake:
   
    _interpreter = Interpreter()
    _had_error = False
    _had_runtime_error = False 

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

        if (Snake._had_runtime_error):
            sys.exit(70)
    
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
        parser = Parser(tokens)
        statements = parser.parse()

        if Snake._had_error:
            return 

        Snake._interpreter.interpret(statements) 

    @staticmethod
    def error(token: Token, message: str):
        
        if isinstance(token, Token):

            if token.token_type == TokenType.EOF:

                Snake._report(token.line, " at end", message)

            else:

                Snake._report(token.line, f" at '{token.lexeme}'", message)

        else:
            
            Snake._report(token, "", message)
    
    @staticmethod
    def runtime_error(error: RunTimeError):
        
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        Snake._had_runtime_error = True        

    @staticmethod
    def _report(line: int, where: str, message: str):
        
        print(f"[line {line}] Error {where}: {message}")
        Snake._had_error = True

if __name__ == "__main__":

    Snake._main()



