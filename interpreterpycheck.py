import lexerpycheck
import parserpycheck


class pycheckesekusi:
    def __init__(self, tree, env, tabarray):
        self.env = env
        self.tabarray = {}
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == "program":
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == "angka":
            return node[1]

        if node[0] == "STRING":
            return node[1]

        # cetak
        if node[0] == "cetak":
            if node[1][0] == '"':
                print(node[1][1 : len(node[1]) - 1])
            else:
                return self.walkTree(node[1])

        # if
        if node[0] == "if_stmt":
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == "condition_eqeq":
            return self.walkTree(node[1]) == self.walkTree(node[2])
        elif node[0] == "ldsd":
            return self.walkTree(node[1]) >= self.walkTree(node[2])
        elif node[0] == "kdsd":
            return self.walkTree(node[1]) <= self.walkTree(node[2])
        elif node[0] == "ld":
            return self.walkTree(node[1]) > self.walkTree(node[2])
        elif node[0] == "kd":
            return self.walkTree(node[1]) < self.walkTree(node[2])
        elif node[0] == "tidaksama":
            return self.walkTree(node[1]) != self.walkTree(node[2])

        # func
        if node[0] == "fungsi_def":
            self.env[node[1]] = node[2]

        if node[0] == "fungsi_call":
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Fungsi '%s' belum dideklarasikan!" % node[1])
                return 0

        # operasi matematika
        if node[0] == "tambah":
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == "kurang":
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == "kali":
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == "bagi":
            return int(self.walkTree(node[1]) / self.walkTree(node[2]))

        # if node[0] == 'assign':
        #     self.env[node[1]] = self.walkTree(node[2])
        #     return node[1]

        if node[0] == "assign":
            var_name = node[1]
            var_value = self.walkTree(node[2])

            # Memeriksa apakah variabel merupakan objek TabArray
            if isinstance(var_value, TabArray):
                self.tabarray[var_name] = var_value
            else:
                self.env[var_name] = var_value

            return var_name

        if node[0] == "var":
            var_name = node[1]

            # Memeriksa apakah variabel merupakan objek TabArray
            if var_name in self.tabarray:
                return self.tabarray[var_name]
            elif var_name in self.env:
                return self.env[var_name]
            else:
                print("Variabel " + var_name + " belum dideklarasikan!")
                return 0

        # if node[0] == 'var':
        #     try:
        #         return self.env[node[1]]
        #     except LookupError:
        #         print("Variabel " + node[1] + " belum dideklarasikan!")
        #         return 0

        # untuk
        if node[0] == "for_loop":
            if node[1][0] == "for_loop_setup":
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == "for_loop_setup":
            return (self.walkTree(node[1]), self.walkTree(node[2]))


class TabArray:
    def __init__(self, tabmax):
        self.array = [None] * tabmax
        self.lastvar = None
        self.lastpar = None
        self.parsize = None
        self.varsize = None


if __name__ == "__main__":
    lexer = lexerpycheck.lexerpycheck()
    parser = parserpycheck.parserpycheck()
    env = {}
    tabarray = {}

    while True:
        try:
            text = input("pyCheck > ")
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            pycheckesekusi(tree, env, tabarray)
