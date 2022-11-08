import re
class RemoveComments:
    def __init__(self,source_list):
        self.source_list = source_list
        self.raw_code = []
        self.line_number = []
    
    def get_code(self):
        self.__delete_comments()
        return ( self.raw_code,self.line_number)

    def __delete_comments(self):
        ln = len(self.source_list)
        flag = True
        for i in range(ln):
            line  = self.source_list[i]
            line = re.sub(r'^\s+|\s+$','',line)
            line = re.sub(r'//.*$','',line)

            if(re.match('/\*.*$',line)):
                flag = False
                line = re.sub(r'/\*.*$','',line)
                if line!= '':
                    self.raw_code.append(line)
                    self.line_number.append(i+1)
            if(re.match(r'^.*\*/',line)):
                flag = True
                line = re.sub(r'^.*\*/','',line)
                if line!= '':
                    self.raw_code.append(line)
                    self.line_number.append(i+1)
            
            if flag==True:
                if line!= '':
                    self.raw_code.append(line)
                    self.line_number.append(i+1)