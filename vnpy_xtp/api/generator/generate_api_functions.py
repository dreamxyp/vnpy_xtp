""""""
import importlib
from typing import Dict, List

type_dict = {
    'uint64_t': 'uint64_t',
    'uint32_t': 'uint32_t',
    'int64_t': 'int64_t',
    'int32_t': 'int32_t',
    'char': 'string',
    'double': 'float',
    "string": "string",
    "bool": "bool",
    "int": "int",
    "enum": "enum",
}


class ApiGenerator:
    """API生成器"""""

    def __init__(self, filename: str, prefix: str, name: str, class_name: str):
        """Constructor"""
        self.filename = filename
        self.prefix = prefix
        self.name = name
        self.class_name = class_name

        self.callbacks: Dict[str, dict] = {}
        self.functions: Dict[str, dict] = {}
        self.lines: Dict[str, str] = {}

        self.structs: Dict[str, dict] = {}
        self.enums: List[str] = []
        self.load_struct()
        self.check_enum()

    def check_enum(self):
        module = importlib.import_module("xtp_typedef")

        for name in dir(module):
            if "__" not in name:
                self.enums.append(name)

    def load_struct(self):
        """加载Struct"""
        module_names = ["xtp_struct_common", "xtp_struct_oms", "xtp_struct_quote"]

        for module_name in module_names:
            module = importlib.import_module(module_name)

            for name in dir(module):
                if "__" not in name:
                    self.structs[name] = getattr(module, name)

    def run(self):
        """运行生成"""
        self.f_cpp = open(self.filename, "r", encoding="UTF-8")

        for line in self.f_cpp:
            self.process_line(line)

        self.f_cpp.close()

        self.generate_header_on()
        self.generate_header_function()

        self.generate_source_callback()
        self.generate_source_function()
        self.generate_source_on()
        self.generate_source_module()

        print("API生成成功")

    def process_line(self, line: str):
        """处理每行"""
        line = line.replace(";", "")
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        line = line.replace("{}", "")

        if "virtual void On" in line:
            self.process_callback(line)
        elif "virtual int Query" in line:
            self.process_function(line)

    def process_callback(self, line: str):
        """处理回掉函数"""
        name = line[line.index("On"):line.index("(")]
        self.lines[name] = line

        d = self.generate_arg_dict(line)
        self.callbacks[name] = d

    def process_function(self, line: str):
        """处理主动函数"""
        name = line[line.index("Query"):line.index("(")]

        d = self.generate_arg_dict(line)
        self.functions[name] = d

    def generate_arg_dict(self, line: str):
        """生成参数字典"""
        args_str = line[line.index("(") + 1:line.index(")")]
        if not args_str:
            return {}
        args = args_str.split(",")

        d = {}
        for arg in args:
            words = arg.split(" ")
            words = [word for word in words if word]

            ptype = words[-2]

            if "*" in words[-2]:
                ptype = words[-2].replace("*", "")

            name = words[-1].replace("*", "")
            if "[" in name:
                name = name.split("[")[0]

            d[name] = ptype
        return d

    def generate_header_on(self):
        """"""
        filename = f"{self.prefix}_{self.name}_header_on.h"
        with open(filename, "w") as f:
            for name, d in self.callbacks.items():
                name = name.replace("On", "on")
                args_list = []

                for pname, ptype in d.items():
                    if ptype == "XTPRI":
                        args_list.append("const dict &error")
                    elif ptype in self.structs:
                        args_list.append("const dict &data")
                    elif ptype in self.enums:
                        args_list.append(f"int {pname}")
                    else:
                        args_list.append(f"{ptype} {pname}")

                args_str = ", ".join(args_list)
                line = f"virtual void {name}({args_str}) {{}};\n\n"

                f.write(line)

    def generate_header_function(self):
        """"""
        filename = f"{self.prefix}_{self.name}_header_function.h"
        with open(filename, "w") as f:
            for key, d in self.functions.items():

                args_list = []

                length = len(d)

                if length < 3:
                    for name_, ptype in d.items():
                        args_list.append(f"int {name_}")
                elif length == 3:
                    for name_, ptype in d.items():
                        if ptype == "int" or ptype in self.enums:
                            args_list.append(f"int {name_}")
                        elif ptype == "char":
                            args_list.append(f"string {name_}")

                        elif ptype in self.structs:
                            args_list.append("const dict &req")

                content = ", ".join(args_list)

                name = key.replace("Query", "query")
                line = f"int {name}({content});\n\n"
                f.write(line)

    def generate_source_callback(self):
        """"""
        filename = f"{self.prefix}_{self.name}_source_callback.cpp"
        with open(filename, "w") as f:
            for name, d in self.callbacks.items():
                on_name = name.replace("On", "on")

                line = self.lines[name]
                f.write(line.replace("virtual void ",
                                     f"void {self.class_name}::") + "\n")
                f.write("{\n")
                f.write("\tgil_scoped_acquire acquire;\n")

                args = []

                for pname, ptype in d.items():
                    if ptype == "XTPRI":
                        args.append("error")

                        f.write("\tdict error;\n")
                        f.write(f"\tif ({pname})\n")
                        f.write("\t{\n")
                        
                        struct_fields = self.structs[ptype]
                        for struct_field, struct_type in struct_fields.items():
                            f.write(
                                f"\t\terror[\"{struct_field}\"] = {pname}->{struct_field};\n")

                        f.write("\t}\n")
                    elif ptype in self.structs:
                        args.append("data")

                        f.write("\tdict data;\n")
                        f.write(f"\tif ({pname})\n")
                        f.write("\t{\n")

                        struct_fields = self.structs[ptype]
                        for struct_field, struct_type in struct_fields.items():
                            if struct_type == "enum":
                                f.write(
                                    f"\t\tdata[\"{struct_field}\"] = (int) {pname}->{struct_field};\n")
                            else:
                                f.write(
                                    f"\t\tdata[\"{struct_field}\"] = {pname}->{struct_field};\n")

                        f.write("\t}\n")
                    else:
                        args.append(pname)

                args_str = ", ".join(args)
                f.write(f"\tthis->{on_name}({args_str});\n")

                f.write("};\n\n")

    def generate_source_function(self):
        """"""
        filename = f"{self.prefix}_{self.name}_source_function.cpp"
        with open(filename, "w") as f:
            for name, d in self.functions.items():
                req_name = name.replace("Query", "query")

                args_list = []

                length = len(d)

                if length < 3:
                    for name_, ptype in d.items():
                        args_list.append(f"int {name_}")
                elif length == 3:
                    for name_, ptype in d.items():
                        if ptype == "int" or ptype in self.enums:
                            args_list.append(f"int {name_}")
                        elif ptype == "char":
                            args_list.append(f"string {name_}")

                        elif ptype in self.structs:
                            args_list.append("const dict &req")

                content = ", ".join(args_list)

                if list(d.values()):
                    ptype = list(d.values())[0]
                else:
                    pass

                f.write(
                    f"int {self.class_name}::{req_name}({content})\n")
                f.write("{\n")
                f.write(f"\t{ptype} myreq = {ptype}();\n")
                f.write("\tmemset(&myreq, 0, sizeof(myreq));\n")

                reqid = "reqid"
                if ptype in self.enums:
                    c = {v: k for k, v in d.items()}[ptype]
                    reqid = f"({ptype}) {c}"

                elif ptype in self.structs:
                    reqid = "reqid"
                    struct_fields = self.structs[ptype]
                    for struct_field, struct_type in struct_fields.items():
                        if struct_type == "string":
                            line = f"\tgetString(req, \"{struct_field}\", myreq.{struct_field});\n"
                        elif struct_type == "int":
                            line = f"\tmyreq.{struct_field} = getIntValue(req, \"{struct_field}\");\n"
                        elif struct_type == "enum":
                            if struct_field == "market":
                                line = f"\tmyreq.{struct_field} = (XTP_MARKET_TYPE) getIntValue(req, \"{struct_field}\");\n"

                            elif struct_field == "exchange_id":
                                line = f"\tmyreq.{struct_field} = (XTP_EXCHANGE_TYPE) getIntValue(req, \"{struct_field}\");\n"
                            # line = f"\tmyreq.{struct_field} = getIntValue(req, \"{struct_field}\");\n"
                        else:
                            line = f"\tget{struct_type.capitalize()}(req, \"{struct_field}\", &myreq.{struct_field});\n"
                        f.write(line)

                words = []
                a = content.split(",")[1:]
                if not a:
                    reqid = ""
                else:
                    for i in a:
                        if "int" in i:
                            words.append(i.replace("int", "").strip())

                    reqid = ", ".join(words)

                f.write(f"\tint i = this->api->{name}(&myreq, {reqid});\n")
                f.write("\treturn i;\n")
                f.write("};\n\n")

    def generate_source_on(self):
        """"""
        filename = f"{self.prefix}_{self.name}_source_on.cpp"
        with open(filename, "w") as f:
            for name, d in self.callbacks.items():
                on_name = name.replace("On", "on")

                args = []
                bind_args = ["void", self.class_name, on_name]

                for pname, ptype in d.items():
                    if ptype == "XTPRI":
                        args.append("const dict &error")
                        bind_args.append("error")
                    elif ptype in self.structs:
                        args.append("const dict &data")
                        bind_args.append("data")
                    elif ptype in self.enums:
                        args.append(f"int {pname}")
                        bind_args.append(pname)
                    else:
                        args.append(f"{ptype} {pname}")
                        bind_args.append(pname)


                args_str = ", ".join(args)
                bind_args_str = ", ".join(bind_args)

                f.write(f"void {on_name}({args_str}) override\n")
                f.write("{\n")
                f.write("\ttry\n")
                f.write("\t{\n")
                f.write(f"\t\tPYBIND11_OVERLOAD({bind_args_str});\n")
                f.write("\t}\n")
                f.write("\tcatch (const error_already_set &e)\n")
                f.write("\t{\n")
                f.write(f"\t\tcout << e.what() << endl;\n")
                f.write("\t}\n")
                f.write("};\n\n")

    def generate_source_module(self):
        """"""
        filename = f"{self.prefix}_{self.name}_source_module.cpp"
        with open(filename, "w") as f:
            for name in self.functions.keys():
                name = name.replace("Query", "query")
                f.write(f".def(\"{name}\", &{self.class_name}::{name})\n")

            f.write("\n")

            for name in self.callbacks.keys():
                name = name.replace("On", "on")
                f.write(f".def(\"{name}\", &{self.class_name}::{name})\n")

            f.write(";\n")


if __name__ == "__main__":
    md_generator = ApiGenerator("../include/xtp/xtp_quote_api.h", "xtp", "md", "MdApi")
    md_generator.run()

    td_generator = ApiGenerator("../include/xtp/xtp_trader_api.h", "xtp", "td", "TdApi")
    td_generator.run()
