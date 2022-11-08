from error import SyntaxError,ReturnStatementNotFound
import re
class FunctionGrabber:
    def __init__(self,source_code,line_number,function,return_type):
        self.source_code = source_code
        self.line_number = line_number
        self.return_type = return_type
        self.function = function
        self.function_body = []
        self.function_called = []
        self.errors = []
    
    def check(self):
        sz = len(self.source_code)
        braches = []
        start =0
        end = -1
        flag1 = False
        last_braches = -1
        return_statement = False
        for i in range(sz):
            regex = r"(?:int|void|float|double|char)\s+"+re.escape(self.function)+r"\s*\(\s*\)\s*\{?"
            if(re.search(regex,self.source_code[i])):
                flag1 =True
                start = i
            if flag1:
                if(re.search(r".*\{.*",self.source_code[i])):
                    braches.append(('{',i))
                    last_braches = i
                if(re.search(r".*\}.*",self.source_code[i])):
                    if(len(braches)):
                        braches.pop()
                    else:
                        err = SyntaxError('Extra } token on line '+ str(self.line_number[i]))
                        self.errors.append(err)
                if len(braches)==0 and last_braches!=-1:
                    end = i
                    flag1 = False
            else:
                if(re.search(r".*\{.*",self.source_code[i])):
                    braches.append(('{',i))
                if(re.search(r".*\}.*",self.source_code[i])):
                    if(len(braches)):
                        braches.pop()
                    else:
                        err = SyntaxError('Extra } token on line '+ str(self.line_number[i]))
                        self.errors.append(err)
        if(len(braches)):
            err = SyntaxError('Imbalance } token on line '+ str(braches[-1][1]))
            self.errors.append(err)

        for i in range(start,end+1):
            if re.search(r".*;$",self.source_code[i]):
                if re.search(r"(?:.*\{.*)|(?:.*\}.*)|(?:.*if\s*\(.*\).*)|(?:while\s*\(.+\).*)|(?:int|void|float|double|char)\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{?",self.source_code[i]):
                    err = SyntaxError('Extra ; token on line '+ str(self.line_number[i]))
                    self.errors.append(err)
            else:
                if not re.search(r"(?:.*\{.*)|(?:.*\}.*)|(?:.*if\s*\(.*\).*)|(?:while\s*\(.+\).*)|(?:int|void|float|double|char)\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{?",self.source_code[i]):
                    err = SyntaxError('No ; token on line '+ str(self.line_number[i]))
                    self.errors.append(err)
            func = re.match(r"(?:(?:int|float|double|char)\s+[a-zA-Z_][a-zA-Z0-0_]*\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\\([\\w,\"%&]*\\)\\s*;)?",self.source_code[i])
            if func:
              self.function_called.append((func.group(1),str(self.line_number[i])))
            if(re.search(r"return\s*.*;$",self.source_code[i])):
                return_statement = True

        if self.return_type != 'void':
            if not return_statement:
                self.errors.append(ReturnStatementNotFound('No return statement found of '+self.return_type))

        return self.function_called,self.errors