import sys

class GenerateAst:

    @staticmethod
    def main(args: list[str]):
        
        if len(args) != 1:
            print("Usage: generate_ast <output directory>", file=sys.stderr)
            sys.exit(64)

        output_dir = args[0]

        GenerateAst._define_ast(output_dir, "Expr", [
            "Binary    : Expr left, Token operator, Expr right",
            "Grouping  : Expr expression",
            "Literal   : Object value",
            "Unary     : Token operator, Expr rigth"
        ])
        
    @staticmethod
    def _define_ast(output_dir: str, base_name: str, types: list[str]):

        path = output_dir + "/" + base_name + ".py"
        
        with open(path, "w", encoding="utf-8") as writer:

            writer.write(f"class {base_name}:\n")
            writer.write("    pass\n")
            
            for type_def in types:
                class_name = type_def.split(":")[0].trim()
                fields = type_def.split(":")[1].trim()
                GenerateAst._define_type(writer, base_name, class_name, fields)
    
    @staticmethod
    def _define_type(writer, base_name: str, class_name: str, field_list: str):
        
        writer.write(f"class {class_name}({base_name}):\n")














if __name__== "__main__":
    
    GenerateAst.main(sys.argv[1:])














