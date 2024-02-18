"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing



class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """
    STATIC_KIND = "STATIC"
    ARG_KIND = "ARG"
    FIELD_KIND = "FIELD"
    VAR_KIND = "VAR"


    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self._class_symbol_table = {}
        self._scopes_array = [self._class_symbol_table, {}] #list of scopes, first search at the [-1] dictionary
        #class variable counter

        #map kind to its counter
        self._kind_counter_dic = {SymbolTable.VAR_KIND : 0,
                                  SymbolTable.ARG_KIND : 0,
                                  SymbolTable.FIELD_KIND : 0,
                                  SymbolTable.STATIC_KIND : 0}


    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self._kind_counter_dic[SymbolTable.VAR_KIND] = 0
        self._kind_counter_dic[SymbolTable.ARG_KIND] = 0
        self._scopes_array[-1].clear()


    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        self._get_kind_table(kind=kind)[name] = SymbolTable.VarData(var_type=type,
                                                                    kind=kind,
                                                                    index=self._kind_counter_dic[kind])
        self._kind_counter_dic[kind] += 1


    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        return self._kind_counter_dic[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        return self._get_var_data(func=SymbolTable.VarData.get_kind, name=name)


    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        return self._get_var_data(func=SymbolTable.VarData.get_type, name=name)


    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        return self._get_var_data(func=SymbolTable.VarData.get_index, name=name)

    def _get_var_data(self, func: typing.Callable, name):
        for dic in reversed(self._scopes_array):
            if name in dic.keys():
                return func(dic[name])
        return None


    class VarData:
        def __init__(self, var_type: str, kind: str, index: int):
            self._var_type = var_type
            self._kind = kind
            self._index = index

        def get_type(self):
            return self._var_type

        def get_kind(self):
            return self._kind

        def get_index(self):
            return self._index

    def _get_kind_table(self, kind : str) -> typing.Dict[str, VarData]:

       if kind in [SymbolTable.STATIC_KIND, SymbolTable.FIELD_KIND]:
           return self._scopes_array[0]
       return self._scopes_array[1]


#test
# table = SymbolTable()
# table.define("a", "int" ,"STATIC")
# table.define("b", "int", "STATIC")
# table.define("c", "int", "FIELD")
# table.define("d", "int", "FIELD")
# table.start_subroutine()
# table.define("w", "int", "VAR")
# table.define("q", "int", "VAR")
# table.define("y", "int", "ARG")
# table.start_subroutine()
# table.define("r", "int", "VAR")
# table.define("h", "int", "VAR")
# table.define("p", "int", "ARG")
# table.define("e", "int", "ARG")
#
# print(table.index_of("p"))