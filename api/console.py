from api.dictdiffer import DictDiffer
import code
import ast
import sys


class Console(code.InteractiveConsole):
    def compile_ast(self, src, filename="<input>", symbol="single"):
        """
        Takes code as string and parses it into an AST.

        Parameters
        ----------
        src: str
            The source code, in string format, to be parsed into an AST.
        """
        compiled_command = code.compile_command(src, filename, symbol)
        if compiled_command:
            self.latest_parsed = ast.parse(src, filename, symbol)
            CaptureExprs().visit(self.latest_parsed)
            self.clean_parsed = ast.parse(src, filename, symbol)
            return compile(self.latest_parsed, filename, symbol)

    def interact(self, banner=""):
        """Launches the interactive subshell and yields code provided by user."""
        self.compile = self.compile_ast
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        self.write(f"{str(banner)}\n")
        more = 0
        while True:
            self.latest_parsed = None
            # Manual DeepCopy
            deepcopy_locals = {}
            for key, value in self.locals.items():
                deepcopy_locals[key] = value
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                    while (not more) and line == "":
                        line = self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    traceback_0 = (
                        sys.last_traceback if hasattr(sys, "last_traceback") else None
                    )
                    more = self.push(line)
                    traceback_1 = (
                        sys.last_traceback if hasattr(sys, "last_traceback") else None
                    )
                    traceback = traceback_1 if traceback_0 != traceback_1 else None
                    differences = DictDiffer(self.locals, deepcopy_locals)
                    added = dict()
                    for var in differences.added() - {"__builtins__"}:
                        added[var] = self.locals[var]
                    changed = dict()
                    for var in differences.changed():
                        changed[var] = self.locals[var]
                    removed = dict()
                    for var in differences.removed():
                        removed[var] = deepcopy_locals[var]
                    if self.latest_parsed is not None:
                        yield {
                            "ast": self.clean_parsed,
                            "added": added,
                            "changed": changed,
                            "removed": removed,
                            "values": self.locals["__ast_parser__"],
                            "traceback": traceback,
                        }
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0


class CaptureExprs(ast.NodeTransformer):
    def visit_Expr(self, node):
        newnode = ast.copy_location(
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="__ast_parser__", ctx=ast.Load()),
                        attr="record",
                        ctx=ast.Load(),
                    ),
                    args=[node.value],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                )
            ),
            node,
        )
        ast.fix_missing_locations(newnode)
        return newnode


class Recorder(list):
    def record(self, value):
        self.append(value)
        return value
