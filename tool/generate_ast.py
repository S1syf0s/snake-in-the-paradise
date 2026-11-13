import sys

class GenerateAst:

    @staticmethod
    def main(args: list[str]):
        
        if len(args) != 1:
            print("Usage: generate_ast <output directory>", file=sys.stderr)
            sys.exit(64)

        output_dir = args[0]

        GenerateAst._define_ast(output_dir, "Expr", [
            "Binary    : left, operator, right",
            "Grouping  : expression",
            "Literal   : value",
            "Unary     : operator, right"
        ])
        
    @staticmethod
    def _define_ast(output_dir: str, base_name: str, types: list[str]):

        path = output_dir + "/" + base_name.lower() + ".py"
        
        with open(path, "w", encoding="utf-8") as writer:

            writer.write(f"class {base_name}:\n")
            writer.write("    pass\n\n")

            GenerateAst._defne_visitor(writer, base_name, types)

            for type_def in types:
                class_name = type_def.split(":")[0].strip()
                fields = type_def.split(":")[1].strip()
                GenerateAst._define_type(writer, base_name, class_name, fields)
    
    @staticmethod
    def _define_type(writer, base_name: str, class_name: str, field_list: str):
        
        writer.write(f"class {class_name}({base_name}):\n\n")
        
        writer.write(f"    def __init__(self, {field_list}):\n\n")
        
        fields = field_list.split(", ")
        for field in fields:
            writer.write(f"        self.{field} = {field}\n")
    
        writer.write("\n\n")

if __name__== "__main__":
    
    GenerateAst.main(sys.argv[1])





