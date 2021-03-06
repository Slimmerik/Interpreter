from source.Type import tokenType
from source.Wraps import prt
import re


class Lexer:
    def __init__(self):
        pass

    def __str__(self):
        return "".join([": is_separator: ", str(self.is_separator(":"))," x is_separator: ", str(self.is_separator("x")), "\n",
        ": is_identifier: ", str(self.is_identifier(":"))," r6 is_identifier: ", str(self.is_identifier("r6")), "\n",
        ": is_keyword: ", str(self.is_keyword(":"))," pop is_keyword: ", str(self.is_keyword("pop")), "\n",
        ": is_point_to: ", str(self.is_point_to(":")), " ='a' is_point_to: ", str(self.is_point_to("='a'")), "\n",
        ": is_register: ", str(self.is_register(":")), " r5 is_register: ",str(self.is_register("r5")), "\n"
        ": is_directive: ", str(self.is_directive(":")), " .qweqwe is_directive: ", str(self.is_directive(".qweqwe")), "\n"
        ])

    @prt
    def string_from_file(self, file_location: str) -> str:
        with open(file_location, "r") as program:
            s = program.read()
        return str(s)

    @prt
    def is_separator(self, ch: str, sepList: list = None):
        if sepList == None:
            return self. is_separator(ch, tokenType.separators.value)
        elif len(sepList) == 0:
            return False
        elif sepList[0] == ch:
            return True
        elif sepList[0] != ch:
            return self.is_separator(ch, sepList[1:])

    @prt
    def is_identifier(self, chunc: str) -> bool:
        if re.match(r'\w*', chunc):
            return True
        else:
            return False

    @prt
    def is_keyword(self, chunc: str, keyList: list = None) -> bool:
        if keyList == None:
            return self.is_keyword(chunc, tokenType.keywords.value)
        elif len(keyList) == 0:
            return False
        elif keyList[0] == chunc:
            return True
        elif keyList[0] != chunc:
            return self.is_keyword(chunc, keyList[1:])

    @prt
    def is_operator(self, chr) -> bool:
        pass

    @prt
    def is_point_to(self, chunc: str) -> bool:
        if re.match(r'\=\'.\'', chunc):
            return True
        else:
            return False

    @prt
    def is_immed(self, chunc: str) -> bool:
        if re.match(r'#immed\d*', chunc):
            return True
        else:
            return False

    @prt
    def is_register(self, chunc: str, regList: list = None) -> bool:
        if regList == None:
            return self.is_register(chunc ,tokenType.registers.value)
        elif len(regList) == 0:
            return False
        elif regList[0] == chunc:
            return True
        elif regList[0] != chunc:
            return self.is_register(chunc, regList[1:])

    @prt
    def is_directive(self, chunc: str) -> bool:
        if chunc[0] == ".":
            return True
        else:
            return False

    # takes chunc string and returns token dict
    # <class 'dict'>:{'tokenType': <tokenType.directive: 'directive'>, 'value': '.cpu'}
    @prt
    def get_token(self, chunc: str) -> dict:
        if self.is_immed(chunc):
            return {"tokenType": tokenType.immed, "value": chunc}
        if self.is_keyword(chunc):
            return {"tokenType": tokenType.keyword, "value": chunc}
        elif self.is_directive(chunc):
            return {"tokenType": tokenType.directive, "value": chunc}
        elif self.is_register(chunc):
            return {"tokenType": tokenType.register, "value": chunc}
        elif self.is_point_to(chunc):
            return {"tokenType": tokenType.point_to, "value": chunc}
        elif self.is_separator(chunc):
            return {"tokenType": tokenType.separator, "value": chunc}
        elif self.is_identifier(chunc):
            return {"tokenType": tokenType.identifier, "value": chunc}
        return {"tokenType": None, "value": chunc}

    # Takes string and outputs list of dicts with tokenTypes and value
    # <class 'list'>:[<class 'dict'>: {'tokenType': <tokenType.directive: 'directive'>, 'value': '.cpu'}]
    @prt
    def Token_list_from_program(self, programStrng: str, tempString: str = "", tokenList: list = []) -> list:
        if len(programStrng) == 0:
            return tokenList[:] + [self.get_token(tempString)]
        elif self.is_separator(programStrng[0]) and len(tempString) == 0:
            return self.Token_list_from_program(programStrng[1:], "", tokenList + [self.get_token(programStrng[0])])
        elif self.is_separator(programStrng[0]) and len(tempString) != 0:
            return self.Token_list_from_program(programStrng[:], "", tokenList + [self.get_token(tempString)])
        elif programStrng[0] == " " and len(tempString) == 0 or programStrng[0] == "\n" and len(tempString) == 0:
            return self.Token_list_from_program(programStrng[1:], tempString, tokenList)
        elif programStrng[0] == " " and len(tempString) != 0 or programStrng[0] == "\n" and len(tempString) != 0:
            return self.Token_list_from_program(programStrng[1:], "", tokenList + [self.get_token(tempString)])
        else:
            return self.Token_list_from_program(programStrng[1:], tempString + programStrng[0], tokenList)





