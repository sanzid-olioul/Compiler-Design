from error import SyntaxError,ReturnStatementNotFound,AlreadyDefined
from tokenization import VariableDeclearation
import re
class FunctionGrabber:
    def __init__(self,source_code,line_number,function,return_type):
        self.source_code = source_code
        self.line_number = line_number
        self.return_type = return_type
        self.function = function
        self.function_body = []
        self.function_called = []
        self.variables = {}
        self.errors = []
        self.tokens ={'if_found':False,'if_true':False,'loop_found':False,'loop_condition':'','if_stack':[],'loop_stack':[],'loop_start':0,'loop_end':0,'loop_var':'','loop_inc':''}
    

    def variable_checker(self,line,itr):
        variable_grabber = VariableDeclearation()
        var = variable_grabber.update(line)
        if var:
            if var[1].isdigit():
                self.variables[var[0]]['value'] = var[1]
            else:
                self.variables[var[0]]['value'] = str(eval(var[1]))
                '''
                More to work
                1. adding two or more variable

                '''
        var = variable_grabber.decleard(line)
        if var:
            for val in var[1]:
                if self.variables.get(val,None):
                    err = AlreadyDefined('variable',val,'is already defined on line',self.variables[val]['line'])
                    self.errors.append(err)
                else:
                    self.variables[val] = {'type': var[0],'line':self.line_number[itr],'value':'Nan'}

        var = variable_grabber.initialized(line)
        if var:
            for val in var[0][1]:
                if self.variables.get(val,None):
                    err = AlreadyDefined('variable',val,'is already defined on line',self.variables[val]['line'])
                    self.errors.append(err)
                else:
                    self.variables[val] = {'type': var[0][0],'line':self.line_number[itr],'value':var[0][2]}
                    # print(var,"is the ....")

    def condition_checker(self,line):
        loop_cond = line
        self.tokens['loop_condition']= loop_cond
        temp1 = re.findall(r'(.*)\s*(?:<|>|<=|>=|==|&&|\|\|)\s*(.*)',loop_cond)
        # print(temp1)
        t1 = temp1[0][0]
        t2 = temp1[0][1]
        rpl1 = t1
        rpl2 = t2
        if not t1.isdigit():
            rpl1 = self.variables[t1]['value']
        if not t2.isdigit():
            rpl2 = self.variables[t2]['value']
        loop_cond = loop_cond.replace(t1,rpl1,1)
        loop_cond = loop_cond.replace(t2,rpl2,1)

        return eval(loop_cond)

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
        itr = start-1
        # for i in range(start,end+1):
        
        while itr < end:
            itr+=1
            if re.search(r".*;$",self.source_code[itr]):
                if re.search(r"(?:.*\{.*)|(?:.*\}.*)|(?:.*if\s*\(.*\).*)|(?:while\s*\(.+\).*)|(?:int|void|float|double|char)\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{?",self.source_code[itr]):
                    err = SyntaxError('Extra ; token on line '+ str(self.line_number[itr]))
                    self.errors.append(err)
            else:
                if not re.search(r"(?:.*\{.*)|(?:.*\}.*)|(?:.*if\s*\(.*\).*)|(?:while\s*\(.+\).*)|(?:int|void|float|double|char)\s+[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{?",self.source_code[itr]):
                    err = SyntaxError('No ; token on line '+ str(self.line_number[itr]))
                    self.errors.append(err)
            
            loop = re.findall(r"for\s*\(\s*(.*)\s*;\s*(.*)\s*;\s*(.*)\s*\)\s*\{?\s*",self.source_code[itr])
            if loop:
                self.tokens['loop_found'] = True
                self.variable_checker(loop[0][0]+";",itr)
                lpcnd =self.condition_checker(loop[0][1])
                inc_dec = re.findall(r"([a-zA-Z][a-zA-Z0-9]*)(\+\+|--)",loop[0][2])
                self.tokens['loop_var'] = inc_dec[0][0].strip()
                
                if inc_dec[0][1]=='++':
                    self.tokens['loop_inc'] = '++'
                else:
                    self.tokens['loop_inc'] = '--'
                # print(inc_dec)
                while itr <= end:
                    if re.search(r".*\{.*",self.source_code[itr]):
                        self.tokens['loop_stack'].append('{')
                        if len(self.tokens['loop_stack'])==1:
                            self.tokens['loop_start'] = itr+1

                    if re.search(r".*\}.*",self.source_code[itr]):
                        if len(self.tokens['loop_stack']):
                            self.tokens['loop_stack'].pop()
                            if len(self.tokens['loop_stack'])==0:
                                self.tokens['loop_end'] = itr
                    if len(self.tokens['loop_stack'])==0:
                        itr = self.tokens['loop_start']
                        break
                    itr+=1
                
                


            if re.search(r"if\s*\(.*\).*\{?",self.source_code[itr]):
                self.tokens['if_found'] = True
                condition = re.findall(r"if\s*\((.*)\)\{?",self.source_code[itr])[0]

                temp1 = re.findall(r'(.*)\s*(?:<=|>=|<|>|==|&&|\|\|)\s*(.*)',condition)
                t1 = temp1[0][0]
                t2 = temp1[0][1]
                rpl1 = t1
                rpl2 = t2
                if not t1.isdigit():
                    rpl1 = self.variables[t1]['value']
                if not t2.isdigit():
                    rpl2 = self.variables[t2]['value']
                condition = condition.replace(t1,rpl1)
                condition = condition.replace(t2,rpl2)



                if eval(condition):
                    self.tokens['if_true'] = True
                else:
                    while itr <= end:
                        if re.search(r".*\{.*",self.source_code[itr]):
                            self.tokens['if_stack'].append('{')
                        if re.search(r".*\}.*",self.source_code[itr]):
                            if len(self.tokens['if_stack']):
                                self.tokens['if_stack'].pop()
                        if len(self.tokens['if_stack'])==0:
                            break
                        itr+=1

            if re.search(".*else\\s*\\{?",self.source_code[itr]):
                if(self.tokens['if_found']):
                    self.tokens['if_found'] = False
                    if(self.tokens['if_true']):
                        self.tokens['if_true'] = False
                        while itr <= end:
                            if re.search(r".*\{.*",self.source_code[itr]):
                                self.tokens['if_stack'].append('{')
                            if re.search(r".*\}.*",self.source_code[itr]):
                                if len(self.tokens['if_stack']):
                                    self.tokens['if_stack'].pop()
                            if len(self.tokens['if_stack'])==0:
                                break
                            itr+=1

                else:
                    err = SyntaxError('there is no if condition found before else on '+ str(self.line_number[itr]))
                    self.errors.append(err)
                

            if re.search(r"printf\(.*\);",self.source_code[itr]):
                printf = re.findall(r"printf\(\s*\"(.*)\"(?:\s*,\s*(.*))?\);",self.source_code[itr])
                temp = re.findall(r'%d|%c|%lf|%f|%s',printf[0][0])
                temp_var = [itr.strip() for itr in printf[0][1].split(',')]
                if len(temp) == len(temp_var) or len(temp) == 0:
                    print_string = printf[0][0]
                    for i in range(len(temp)):
                        print_string = re.sub(r'%d|%c|%lf|%f|%s',self.variables[temp_var[i]]['value'],print_string,1)
                    print(print_string)

                else:
                    err = SyntaxError('insufficient variable given on line '+ str(self.line_number[itr]))
                    self.errors.append(err)

            
            func = re.findall(r"(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-0_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\([\w,\"%&]*\)\s*;",self.source_code[itr])
            if func:
                if self.variables.get(func[0][1],None):
                    err = AlreadyDefined('variable',func[0][1],'is already defined on line',self.variables[func[0][1]][1])
                    self.errors.append(err)
                else:
                    self.variables[func[0][1]] = [func[0][0],self.line_number[itr]]
                self.function_called.append((func[0][2],str(self.line_number[itr])))


            self.variable_checker(self.source_code[itr],itr)

            if self.tokens['loop_found']:
                if itr == self.tokens['loop_end']:
                    cond = self.condition_checker(self.tokens['loop_condition'])
                    
                    if cond:
                        itr = self.tokens['loop_start']-1
                        if self.tokens['loop_inc'] == "++":
                            self.variables[self.tokens['loop_var']]['value'] = str(int(self.variables[self.tokens['loop_var']]['value']) +1)
                        else:
                            self.variables[self.tokens['loop_var']]['value'] = str(int(self.variables[self.tokens['loop_var']]['value']) -1)


            if(re.search(r"return\s*.*;$",self.source_code[itr])):
                return_statement = True

        if self.return_type != 'void':
            if not return_statement:
                self.errors.append(ReturnStatementNotFound('No return statement found of '+self.return_type))
        return self.function_called,self.variables,self.errors